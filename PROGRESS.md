# Assignment Progress

Status meanings: **NOT STARTED**, **IN PROGRESS**, **IMPLEMENTED**, **VERIFIED**, **USER ACTION REQUIRED**. VERIFIED means a real local check completed; writing a manifest or documenting a command is only IMPLEMENTED.

## Sessions 01–11 (existing repository work)

| Session / requirement | Status | Evidence / notes |
|---|---|---|
| 01–02 Linux links, user management, journalctl, cheat sheet | IMPLEMENTED | `01-linux-fundamentals/`; existing notes and screenshots. |
| 03 System information shell script and report | IMPLEMENTED | `02-shell-scripting/system-information-script/`; existing output and screenshots. |
| 04 Networking command practice | IMPLEMENTED | `03-networking-fundamentals/command-practice/`. |
| 05 Git commit and cherry-pick practice | IMPLEMENTED | `04-git-github/`; existing commands and screenshots. |
| 06 Six Docker Hello World applications | IMPLEMENTED | All six images built and containers started from `05-docker-fundamentals/docker-compose.yml`; fresh HTTP check still pending. |
| 07 Multistage build and three application types | IMPLEMENTED | `06-dockerfiles-images/`; existing screenshots, fresh build not yet run. |
| 08 Docker networks, host mode, bind mount, overlay research | IMPLEMENTED | `07-docker-networking-volumes/`; sample DB password replaced with environment input. |
| 09 Kubernetes fundamentals and Minikube | VERIFIED | Local Minikube v1.37 node Ready with CoreDNS and system Pods; existing tutorial notes/screenshots remain in `08-kubernetes-fundamentals/`. |
| 10 Deployments, four strategies, Pod lifecycle | IMPLEMENTED | Existing strategy work preserved; all 12 Pod lifecycle YAML examples were run in `session10-lifecycle`, with individual output screenshots linked from the lifecycle README. |
| 11 Five Services, comparisons, FQDN and CoreDNS | VERIFIED | `10-kubernetes-services/`: 5/5 Services deployed in `session11`, Ready backends, ClusterIP/NodePort/LoadBalancer HTTP, ExternalName CNAME, headless DNS and per-Pod HTTP; real output appended to README. |

## Sessions 12–21 and final project

| Session / requirement | Status | Evidence / notes |
|---|---|---|
| 12 ConfigMap, Secret, Ingress, troubleshooting | VERIFIED | ConfigMap and Secret injection, ingress-nginx `/health` route, and isolated broken/fixed Service checked; three genuine screenshots linked in README. |
| 13 Storage, HPA, load generator, mini project | VERIFIED | `hpa.yml`, load Job, volume guide and mini project; local HPA scaled 2→8 twice with actual CPU/output and genuine `session13.png`. |
| 14 Kubernetes troubleshooting commands and failure scenarios | VERIFIED | Five isolated Pod failures and separate Service, DNS and Pod networking failures were investigated and fixed; genuine before/after screenshots captured. |
| 15 Helm commands and rollback project | VERIFIED | Chart lint passed; local revisions 1→2→3→4 include rollback to 1, and `helm-rollback.png` captures revision 4 deployed with 2/2 Pods Ready. The disposable release was uninstalled and `helm-uninstall.png` captures its absence while `homework` remains. |
| 16 CI/CD GitHub Actions demo | VERIFIED | Hosted Actions run `37801718339` passed test/security and publish jobs; genuine screenshot saved in `final-devops-project/evidence/github-actions.png`. |
| 17 DevSecOps scans and gates | VERIFIED | Hosted run `37801718339` passed Bandit, pip-audit, Gitleaks, Trivy, and gated image publication; run logs and screenshot retained. |
| 18 Terraform S3 demo and AWS service research | USER ACTION REQUIRED | Exact S3 files including public-only `terraform.tfvars`, AWS notes, fmt/init/validate passed; plan/apply/show/output/destroy require AWS credentials. |
| 19 Terraform cloud architecture | USER ACTION REQUIRED | VPC/EC2/S3 config fmt/init/validate passed; plan/apply/destroy and screenshots require AWS credentials. |
| 20 Monitoring, observability and GitOps | VERIFIED | Local API, Prometheus, Grafana, node-exporter, CPU/memory/request metrics, logs, health and alert rule checked; live Grafana screenshot captured. Historical Session 20 Argo CD screenshot shows `session20-app` Synced/Healthy with two Ready Pods, sourced from `devops-heros.git`. |
| 21 Final end-to-end DevOps project and troubleshooting | USER ACTION REQUIRED | API tests, image build, local Kubernetes/Helm, hosted security pipeline, monitoring and local Argo CD chart reconciliation verified; `homework-api-local` was Synced/Healthy with 2/2 API replicas and 1/1 PostgreSQL, and its Service returned a healthy response and stored a visit. Its screenshot is linked from the final README. Two isolated faults were reproduced and repaired. AWS infrastructure and deployment of the published GHCR image through the normal Application remain unverified. |
| Final README and architecture | IMPLEMENTED | Root and final-project READMEs include architecture diagrams and runbooks. |
| Screenshot/evidence checklist | IMPLEMENTED | `SCREENSHOT_CHECKLIST.md` lists genuine captures and destinations; no fabricated images. |
| Presentation | IMPLEMENTED | Assignment does not request a presentation; no slide deck required. |

## Environment verification

- Docker Engine 29.7.2 is accessible outside the command sandbox; final API/DB and six Session 06 app containers were built and started.
- Minikube v1.37.0 is Ready. Its CNI and Metrics Server images were loaded from the host because cluster registry DNS failed.
- Helm 3.22.0 and Terraform 1.16.5 are installed. Both Terraform projects validated with the AWS provider; no AWS infrastructure was created.
- AWS CLI is not installed; no AWS plan/apply can be claimed.
- The repository was pushed to its public GitHub remote for the hosted CI/CD demonstration; run `37801718339` passed.
