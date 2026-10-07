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
| 10 Deployments, four strategies, Pod lifecycle | IMPLEMENTED | User confirmed Session 10 was already completed; existing work in `09-kubernetes-pods-deployments/` preserved. |
| 11 Five Services, comparisons, FQDN and CoreDNS | VERIFIED | `10-kubernetes-services/`: 5/5 Services deployed in `session11`, Ready backends, ClusterIP/NodePort/LoadBalancer HTTP, ExternalName CNAME, headless DNS and per-Pod HTTP; real output appended to README. |

## Sessions 12–21 and final project

| Session / requirement | Status | Evidence / notes |
|---|---|---|
| 12 ConfigMap, Secret, Ingress, troubleshooting | VERIFIED | ConfigMap and Secret injection, ingress-nginx `/health` route, and isolated broken/fixed Service checked; three genuine screenshots linked in README. |
| 13 Storage, HPA, load generator, mini project | VERIFIED | `hpa.yml`, load Job, volume guide and mini project; local HPA scaled 2→8 twice with actual CPU/output and genuine `session13.png`. |
| 14 Kubernetes troubleshooting commands and failure scenarios | IN PROGRESS | Five isolated Pod failure cases were investigated and fixed; genuine before/after screenshots captured. Service, DNS and Pod networking drills remain. |
| 15 Helm commands and rollback project | USER ACTION REQUIRED | Chart lint passed and local revisions 1→2→3→4 include rollback to 1; screenshot and remaining command evidence still required. |
| 16 CI/CD GitHub Actions demo | IN PROGRESS | Implement test/build workflow. |
| 17 DevSecOps scans and gates | IN PROGRESS | Bandit and pip-audit passed locally; Gitleaks, Trivy and hosted workflow run still pending. |
| 18 Terraform S3 demo and AWS service research | USER ACTION REQUIRED | Exact S3 files including public-only `terraform.tfvars`, AWS notes, fmt/init/validate passed; plan/apply/show/output/destroy require AWS credentials. |
| 19 Terraform cloud architecture | USER ACTION REQUIRED | VPC/EC2/S3 config fmt/init/validate passed; plan/apply/destroy and screenshots require AWS credentials. |
| 20 Monitoring, observability and GitOps | IN PROGRESS | Implement Prometheus/Grafana and Argo CD declarations. |
| 21 Final end-to-end DevOps project and troubleshooting | IN PROGRESS | Implement a runnable API, tests, image, Kubernetes, Helm and pipeline. |
| Final README and architecture | IMPLEMENTED | Root and final-project READMEs include architecture diagrams and runbooks. |
| Screenshot/evidence checklist | IMPLEMENTED | `SCREENSHOT_CHECKLIST.md` lists genuine captures and destinations; no fabricated images. |
| Presentation | IMPLEMENTED | Assignment does not request a presentation; no slide deck required. |

## Environment verification

- Docker Engine 29.7.2 is accessible outside the command sandbox; final API/DB and six Session 06 app containers were built and started.
- Minikube v1.37.0 is Ready. Its CNI and Metrics Server images were loaded from the host because cluster registry DNS failed.
- Helm 3.22.0 and Terraform 1.16.5 are installed. Both Terraform projects validated with the AWS provider; no AWS infrastructure was created.
- AWS CLI is not installed; no AWS plan/apply can be claimed.
- Public GitHub remote exists, but this task does not push changes.
