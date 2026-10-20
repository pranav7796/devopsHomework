# Assignment Progress

Status meanings: **NOT STARTED**, **IN PROGRESS**, **IMPLEMENTED**, **VERIFIED**, **USER ACTION REQUIRED**. VERIFIED means a real local check completed; writing a manifest or documenting a command is only IMPLEMENTED.

## Sessions 01–11 (existing repository work)

| Session / requirement | Status | Evidence / notes |
|---|---|---|
| 01–02 Linux links, user management, journalctl, cheat sheet | IMPLEMENTED | `01-linux-fundamentals/`; existing notes and screenshots. |
| 03 System information shell script and report | VERIFIED | Ran the script in its homework folder on 9 Oct 2026 with real input; date, host, username, `df -h`, and process output were captured in the README and `system-report/process.log`. The process log stores process names/usage without full command-line arguments. |
| 04 Networking command practice | IMPLEMENTED | `03-networking-fundamentals/command-practice/`. |
| 05 Git commit and cherry-pick practice | VERIFIED | Ran both isolated lab scripts; confirmed `git commit -a` omitted the untracked file and the cherry-picked feature commit appeared on `main`. Temporary lab repositories were removed. |
| 06 Six Docker Hello World applications | VERIFIED | All six Compose containers were running and HTTP checks on ports 8101–8106 returned Hello World on 8 October 2026; existing screenshots remain in each application directory. |
| 07 Multistage build and three application types | VERIFIED | On 9 Oct 2026, built all four images and ran the multi-stage, Node.js, Python, and Java apps. HTTP checks returned the required text on ports 8080, 8201, 8202, and 8203; `docker compose ps` showed all four containers running. Fresh command output is in `06-dockerfiles-images/evidence/README.md`. |
| 08 Docker networks, host mode, bind mount, overlay research | VERIFIED | Isolated Compose project: backend resolved and pinged frontend/database and connected to MySQL on 3306; Apache returned its default page on host port 80; bind-mounted Nginx showed `Hello students`, reflected the update without restart, then the original file was restored. Overlay behavior and multi-host constraints are documented; no Swarm was initialized. |
| 09 Kubernetes fundamentals and Minikube | VERIFIED | Local Minikube v1.37 node Ready with CoreDNS and system Pods; existing tutorial notes/screenshots remain in `08-kubernetes-fundamentals/`. |
| 10 Deployments, four strategies, Pod lifecycle | VERIFIED | On 21 Oct 2026 (IST), all four strategies passed real rollout/HTTP checks in a disposable local Minikube namespace: rolling v1→v2, blue→green→blue routing, canary 9:1 endpoints (86 stable/14 canary responses from 100 requests) and stable-only rollback, recreate with replacement Pod UIDs. Service copies used ClusterIP to avoid existing NodePort conflicts. Only the new test namespace was deleted. See `evidence/completion-2026-10-21/strategy-results.json`; continuous zero-downtime HTTP availability was not measured. Historical lifecycle screenshots remain separately dated. |
| 11 Five Services, comparisons, FQDN and CoreDNS | VERIFIED | `10-kubernetes-services/`: 5/5 Services deployed in `session11`, Ready backends, ClusterIP/NodePort/LoadBalancer HTTP, ExternalName CNAME, headless DNS and per-Pod HTTP; real output appended to README. |

## Sessions 12–21 and final project

| Session / requirement | Status | Evidence / notes |
|---|---|---|
| 12 ConfigMap, Secret, Ingress, troubleshooting | VERIFIED | ConfigMap and Secret injection, ingress-nginx `/health` route, and isolated broken/fixed Service checked; three genuine screenshots linked in README. |
| 13 Storage, HPA, load generator, mini project | VERIFIED | `hpa.yml`, load Job, volume guide and mini project; local HPA scaled 2→8 twice with actual CPU/output and genuine `session13.png`. |
| 14 Kubernetes troubleshooting commands and failure scenarios | VERIFIED | Five isolated Pod failures and separate Service, DNS and Pod networking failures were investigated and fixed; genuine before/after screenshots captured. |
| 15 Helm commands and rollback project | VERIFIED | Chart lint passed; local revisions 1→2→3→4 include rollback to 1, and `helm-rollback.png` captures revision 4 deployed with 2/2 Pods Ready. The disposable release was uninstalled and `helm-uninstall.png` captures its absence while `homework` remains. |
| 16 CI/CD GitHub Actions demo | VERIFIED | Completion run `39500684657` for `a372702` passed test/security and publish jobs, including GHCR publication and the GitOps image-tag update. API metadata is in `evidence/completion-2026-10-21/ci-success.json`; [new CI terminal evidence](evidence/screenshots-2026-10-21/ci-evidence.png) additionally shows successful run `39501169416`. The October 8 screenshot remains historical. |
| 17 DevSecOps scans and gates | VERIFIED | Completion run `39500684657` passed Bandit, pip-audit, Gitleaks and Trivy, then image publication. The precise public-image-line false-positive exception and positive/negative scanner checks are documented in `final-devops-project/security/README.md`; no gate was disabled. |
| 18 Terraform S3 demo and AWS service research | VERIFIED | S3 project and service notes are present. Authenticated Sydney init/fmt/validate and 4-addition plan passed on 21 Oct 2026 (IST). The reviewed S3 plan was applied; versioning/encryption/public-access controls and Sydney location checked; deployed-state show/output captured; destroy completed and bucket absence independently confirmed. See `evidence/aws-execution/`. |
| 19 Terraform cloud architecture | VERIFIED | Account-guarded VPC/EC2/S3 configuration and safe input example are present. Its own authenticated 11-addition Sydney plan passed. Apply, healthy t3.micro status, real HTTP `DevOps homework`, restricted ingress, S3 controls, show/output and destroy passed. Instance terminated, VPC/root disk/bucket absent; see `evidence/aws-execution/`. [Terminal screenshots](evidence/screenshots-2026-10-21/README.md) now show labeled saved execution/cleanup excerpts. |
| 20 Monitoring, observability and GitOps | VERIFIED | Local API, Prometheus, Grafana, node-exporter, CPU/memory/request metrics, logs, health and alert rule checked; live Grafana screenshot captured. The project's own final-project Argo CD screenshot shows its Helm chart Synced and Healthy in Minikube. |
| 21 Final end-to-end DevOps project and troubleshooting | VERIFIED | API tests, image build, local Kubernetes/Helm, hosted security pipeline, monitoring and Argo CD reconciliation verified. Terraform copy includes input examples, architecture diagram, and private/versioned/encrypted S3 controls; fmt and validate pass locally. This copy's own authenticated 11-addition Sydney plan passed on 21 Oct 2026 (IST); this copy was separately applied, verified via EC2 HTTP and S3 APIs, and destroyed with independent absence checks. Two isolated faults were previously reproduced and repaired. |
| Final README and architecture | IMPLEMENTED | Root and final-project READMEs include architecture diagrams and runbooks. |
| Screenshot/evidence checklist | IMPLEMENTED | `SCREENSHOT_CHECKLIST.md` lists captures and destinations. AWS screenshots must come from this project's own execution. |
| Presentation | IMPLEMENTED | Assignment does not request a presentation; no slide deck required. |

## Environment verification

- Docker Engine 29.7.2 is accessible outside the command sandbox; final API/DB and six Session 06 app containers were built and started.
- Minikube v1.37.0 is Ready. Its CNI and Metrics Server images were loaded from the host because cluster registry DNS failed.
- Terraform 1.16.5 with locked AWS provider 5.100.0 initialized, formatted and validated all three homework projects. These plans were subsequently applied and all newly created homework infrastructure was independently confirmed removed. Historical Docker/cluster versions above refer to their original check dates; local Minikube was restarted for the new isolated strategy checks without changing the active EKS context.
- AWS CLI 2.34.32 is installed. On 21 Oct 2026 (IST), STS confirmed `devops-new`, account `525426877661`; all three projects produced real Sydney plans. All three homework apply/verification/show/output/destroy exercises subsequently passed; see `evidence/aws-execution/`. Credentials, state, saved plans and private input snapshots are excluded from Git.
- The repository was pushed to its public GitHub remote for the hosted CI/CD demonstration; run `37801718339` passed.

## Completion check — 21 October 2026 (IST)

The local fixes, validation and all three temporary AWS lifecycles are complete. [Current check results](evidence/completion-2026-10-21/README.md) and [reviewed AWS plans/cost/cleanup scope](AWS-HOMEWORK.md) and [execution/absence evidence](evidence/aws-execution/README.md) distinguish the dated plan snapshots from the later successful provisioning and teardown. No RelayDesk infrastructure was changed. A later desktop capture pass added [five genuine terminal screenshots](evidence/screenshots-2026-10-21/README.md): the missing plan, three AWS lifecycles and current successful CI. AWS images explicitly show dated saved logs; no new AWS resources were created.
