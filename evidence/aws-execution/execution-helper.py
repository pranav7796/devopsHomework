"""Execute the owner-reviewed homework plans sequentially and remove only their new resources."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request

ROOT = Path('/home/pranav/Projects/devopsHomework')
OUT = ROOT / 'evidence/aws-execution'
OUT.mkdir(parents=True, exist_ok=True)
ENV = {**os.environ, 'AWS_CONFIG_FILE': str(ROOT/'scripts/aws-login.config'), 'AWS_PROFILE': 'devops-new', 'AWS_REGION': 'ap-southeast-2', 'AWS_DEFAULT_REGION': 'ap-southeast-2', 'AWS_EC2_METADATA_DISABLED': 'true', 'AWS_PAGER': ''}
summary=json.loads((ROOT/'evidence/aws-plans/summary.json').read_text())
records=json.loads((OUT/'command-results.json').read_text()) if (OUT/'command-results.json').exists() else []
results=json.loads((OUT/'summary.json').read_text())['projects'] if (OUT/'summary.json').exists() else []
def now(): return datetime.now(timezone.utc).isoformat()
def run(name,command,timeout=900,ok=(0,),save=True):
    start=now(); print('START',name,flush=True)
    completed=subprocess.run(command,cwd=ROOT,env=ENV,text=True,capture_output=True,timeout=timeout)
    attempt=1+sum(x['name']==name for x in records)
    stem=name if attempt==1 else name+'-retry-'+str(attempt)
    record={'name':name,'command':command,'started_at_utc':start,'finished_at_utc':now(),'exit_code':completed.returncode}
    if save:
        (OUT/(stem+'.txt')).write_text(completed.stdout)
        record['stdout']=stem+'.txt'
    if completed.stderr:
        (OUT/(stem+'-stderr.txt')).write_text(completed.stderr)
        record['stderr']=stem+'-stderr.txt'
    records.append(record);(OUT/'command-results.json').write_text(json.dumps(records,indent=2)+'\n')
    print('END',name,completed.returncode,flush=True)
    if completed.returncode not in ok: raise RuntimeError(f'{name} failed (exit {completed.returncode}); inspect recorded output')
    return completed
def aws(name,*args,ok=(0,),timeout=180):
    result=run(name,['aws',*args,'--profile','devops-new','--region','ap-southeast-2','--output','json','--no-cli-pager'],timeout,ok)
    if result.returncode: return result
    return json.loads(result.stdout) if result.stdout.strip() else None
def tf(tag,project,name,*args,ok=(0,),save=True):
    return run(tag+'-'+name,['terraform','-chdir='+project,*args],timeout=1200,ok=ok,save=save)
def state_values(tag,project,name):
    return json.loads(tf(tag,project,name,'show','-json',save=False).stdout)
def save_results():
    (OUT/'summary.json').write_text(json.dumps({'account':'525426877661','region':'ap-southeast-2','updated_at_utc':now(),'scope':'Only three reviewed homework plans; no preexisting AWS resource or RelayDesk mutation authorized','projects':results},indent=2)+'\n')
identity=aws('identity-before','sts','get-caller-identity')
assert identity['Account']=='525426877661'
with urllib.request.urlopen('https://checkip.amazonaws.com',timeout=10) as response:
    assert response.read().decode().strip()+'/32'==summary['admin_cidr'],'Trusted egress changed; replan before deploying'
before=aws('relaydesk-before','eks','describe-cluster','--name','relaydesk-capstone','--query','cluster.{arn:arn,status:status,version:version,vpc:resourcesVpcConfig.vpcId}')
assert before['status']=='ACTIVE'
for project in summary['projects']:
    directory=project['directory'];tag={'terraform-s3-demo':'s18','terraform-cloud':'s19','final-devops-project/terraform':'final'}[directory]
    assert hashlib.sha256((ROOT/project['saved_plan']).read_bytes()).hexdigest()==project['plan_sha256']
    for filename,digest in project['source_sha256'].items(): assert hashlib.sha256((ROOT/directory/filename).read_bytes()).hexdigest()==digest
    initial=tf(tag,directory,'state-before','state','list',ok=(0,1))
    if initial.returncode==1: assert 'No state file was found' in initial.stderr
    existing=initial.stdout.strip()
    prior=next((x for x in results if x['project']==directory),None)
    if prior and prior.get('cleanup')=='PASS':
        assert not existing,'Previously cleaned project unexpectedly contains resources'
        print('SKIP verified and cleaned project',tag,flush=True)
        continue
    if existing:
        assert prior and prior.get('apply')=='PASS' and prior.get('created_ids'),'Unexpected preexisting managed state; refusing to touch it'
        current=state_values(tag,directory,'resume-state-values')
        actual_ids={x['address']:x['values'].get('id') for x in current['values']['root_module']['resources'] if x.get('mode')=='managed'}
        assert actual_ids==prior['created_ids'],'Managed IDs do not match the new resources recorded by this execution'
    reviewed=json.loads(tf(tag,directory,'review-plan','show','-json','tfplan-completion',save=False).stdout)
    assert reviewed['variables']['aws_region']['value']=='ap-southeast-2'
    assert reviewed['configuration']['provider_config']['aws']['expressions']['allowed_account_ids']['constant_value']==['525426877661']
    assert all(x['change']['actions']==['create'] for x in reviewed['resource_changes'])
    entry=prior or {'project':directory,'exercise':tag,'reviewed_plan_sha256':project['plan_sha256'],'started_at_utc':now(),'bucket':project['bucket'],'apply':'NOT_RUN','verification':'NOT_RUN','cleanup':'NOT_RUN'}
    if not prior: results.append(entry)
    save_results()
    applied=False; verify_error=None
    try:
        if entry['apply']!='PASS':
            tf(tag,directory,'apply','apply','-input=false','-no-color','tfplan-completion')
        applied=True;entry['apply']='PASS';save_results()
        tf(tag,directory,'show','show','-no-color')
        outputs=json.loads(tf(tag,directory,'output','output','-json').stdout)
        state=state_values(tag,directory,'state-values')
        resources=state.get('values',{}).get('root_module',{}).get('resources',[])
        managed={x['address']:x for x in resources if x.get('mode')=='managed'}
        assert set(managed)=={x['address'] for x in project['changes']}
        entry['created_ids']={k:v['values'].get('id') for k,v in managed.items()}
        bucket=outputs['bucket_name']['value'];assert bucket==project['bucket']
        tags=aws(tag+'-bucket-tags','s3api','get-bucket-tagging','--bucket',bucket)
        assert {'Key':'Project','Value':'devopsHomework'} in tags['TagSet']
        block=aws(tag+'-bucket-public-access','s3api','get-public-access-block','--bucket',bucket)
        assert all(block['PublicAccessBlockConfiguration'].values())
        version=aws(tag+'-bucket-versioning','s3api','get-bucket-versioning','--bucket',bucket);assert version['Status']=='Enabled'
        encryption=aws(tag+'-bucket-encryption','s3api','get-bucket-encryption','--bucket',bucket)
        assert encryption['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']=='AES256'
        location=aws(tag+'-bucket-location','s3api','get-bucket-location','--bucket',bucket);assert location['LocationConstraint']=='ap-southeast-2'
        if tag!='s18':
            instance=managed['aws_instance.demo']['values']['id'];vpc=managed['aws_vpc.project']['values']['id']
            entry.update(instance_id=instance,vpc_id=vpc,public_ip=outputs['instance_public_ip']['value']);save_results()
            aws(tag+'-instance-status-wait','ec2','wait','instance-status-ok','--instance-ids',instance,timeout=720)
            detail=aws(tag+'-instance','ec2','describe-instances','--instance-ids',instance)
            actual=detail['Reservations'][0]['Instances'][0]
            assert actual['InstanceType']=='t3.micro' and actual['VpcId']==vpc and actual['State']['Name']=='running'
            assert {x['Key']:x['Value'] for x in actual['Tags']}['Project']=='devopsHomework'
            entry['volume_ids']=[b['Ebs']['VolumeId'] for b in actual['BlockDeviceMappings'] if 'Ebs' in b];save_results()
            aws(tag+'-vpc','ec2','describe-vpcs','--vpc-ids',vpc)
            aws(tag+'-routes','ec2','describe-route-tables','--filters','Name=vpc-id,Values='+vpc)
            security=aws(tag+'-security','ec2','describe-security-groups','--group-ids',managed['aws_security_group.web']['values']['id'])
            for permission in security['SecurityGroups'][0]['IpPermissions']:
                assert permission['FromPort'] in (22,80) and permission['ToPort']==permission['FromPort']
                assert [x['CidrIp'] for x in permission['IpRanges']]==[summary['admin_cidr']]
            url='http://'+entry['public_ip'];attempts=[]
            for attempt in range(60):
                try:
                    with urllib.request.urlopen(url,timeout=5) as response:
                        body=response.read().decode();status=response.status
                    assert status==200 and body.strip()=='DevOps homework'
                    attempts.append({'at_utc':now(),'status':status,'body':body})
                    (OUT/(tag+'-http.txt')).write_text('GET '+url+'\nHTTP '+str(status)+'\n'+body)
                    break
                except (OSError,AssertionError) as error:
                    attempts.append({'at_utc':now(),'error':str(error)})
                    if attempt==59:raise
                    time.sleep(5)
            (OUT/(tag+'-http-attempts.json')).write_text(json.dumps(attempts,indent=2)+'\n')
        entry['verification']='PASS';save_results()
    except Exception as error:
        entry['verification']='FAIL';entry['error']=str(error);verify_error=error;save_results()
    finally:
        # A partial apply may leave new managed objects: clean only that reviewed state.
        state_list=tf(tag,directory,'state-before-cleanup','state','list').stdout.strip()
        if state_list:
            allowed_state={x['address'] for x in project['changes']}
            if tag!='s18':allowed_state.add('data.aws_availability_zones.available')
            assert set(state_list.splitlines()).issubset(allowed_state)
            snapshot=str(ROOT/project['input_snapshot'])
            tf(tag,directory,'destroy-plan','plan','-destroy','-input=false','-no-color','-var-file='+snapshot,'-out=tfplan-cleanup')
            destruction=json.loads(tf(tag,directory,'review-destroy','show','-json','tfplan-cleanup',save=False).stdout)
            changes=[x for x in destruction.get('resource_changes',[]) if x.get('mode')=='managed']
            assert changes and all(x['change']['actions']==['delete'] for x in changes)
            assert {x['address'] for x in changes}.issubset({x['address'] for x in project['changes']})
            audit={'reviewed_at_utc':now(),'saved_plan_sha256':hashlib.sha256((ROOT/directory/'tfplan-cleanup').read_bytes()).hexdigest(),'actions':[{'address':x['address'],'actions':x['change']['actions'],'id':x['change']['before'].get('id')} for x in changes],'only_new_reviewed_homework_addresses':True}
            (OUT/(tag+'-cleanup-audit.json')).write_text(json.dumps(audit,indent=2)+'\n')
            tf(tag,directory,'destroy','apply','-input=false','-no-color','tfplan-cleanup')
        assert not tf(tag,directory,'state-after-cleanup','state','list').stdout.strip()
        absent=aws(tag+'-bucket-after-cleanup','s3api','head-bucket','--bucket',project['bucket'],ok=(0,254,255))
        assert isinstance(absent,subprocess.CompletedProcess) and absent.returncode in (254,255)
        assert ('404' in absent.stderr or 'Not Found' in absent.stderr),'Bucket absence not established'
        if entry.get('instance_id'):
            aws(tag+'-terminated-wait','ec2','wait','instance-terminated','--instance-ids',entry['instance_id'],timeout=600)
            detail=aws(tag+'-instance-after-cleanup','ec2','describe-instances','--instance-ids',entry['instance_id'])
            assert detail['Reservations'][0]['Instances'][0]['State']['Name']=='terminated'
            vpc_check=aws(tag+'-vpc-after-cleanup','ec2','describe-vpcs','--vpc-ids',entry['vpc_id'],ok=(0,254))
            assert isinstance(vpc_check,subprocess.CompletedProcess) and 'InvalidVpcID.NotFound' in vpc_check.stderr
            for volume in entry.get('volume_ids',[]):
                for attempt in range(24):
                    check=aws(tag+'-volume-after-cleanup-'+volume,'ec2','describe-volumes','--volume-ids',volume,ok=(0,254))
                    if isinstance(check,subprocess.CompletedProcess) and 'InvalidVolume.NotFound' in check.stderr:break
                    if attempt==23:raise RuntimeError('New root volume still present after cleanup: '+volume)
                    time.sleep(5)
        entry['cleanup']='PASS';entry['finished_at_utc']=now();save_results()
    if verify_error:raise verify_error
after=aws('relaydesk-after','eks','describe-cluster','--name','relaydesk-capstone','--query','cluster.{arn:arn,status:status,version:version,vpc:resourcesVpcConfig.vpcId}')
assert before==after
assert all(x['apply']==x['verification']==x['cleanup']=='PASS' for x in results)
save_results();print('PASS: all homework plans applied, verified and cleaned; RelayDesk cluster unchanged and ACTIVE.',flush=True)
