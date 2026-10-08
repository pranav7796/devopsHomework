# Session 15: Helm commands and rollback

The mini project is the working API, PostgreSQL, Service, ConfigMap, Ingress and HPA chart in [`../final-devops-project/helm/`](../final-devops-project/helm/). Its [`values.yaml`](../final-devops-project/helm/values.yaml) and templates are committed. A database Secret is created locally and never committed.

## Command practice performed locally

| Command | Purpose and observed output |
|---|---|
| `helm create /tmp/session15-practice-chart` | Scaffolded a disposable chart; printed `Creating /tmp/session15-practice-chart`. |
| `helm lint final-devops-project/helm` | Validated chart structure: `1 chart(s) linted, 0 chart(s) failed`. |
| `helm template session15-demo final-devops-project/helm ...` | Rendered ConfigMap, Service and Deployment YAML with local values. |
| `helm repo add bitnami https://charts.bitnami.com/bitnami` | Added the Bitnami chart repository. |
| `helm repo update` | Successfully updated both configured repositories. |
| `helm repo list` | Listed `prometheus-community`; Bitnami was then added. |
| `helm search repo bitnami/nginx` | Found `bitnami/nginx` chart version `25.2.1` in the local index. |
| `helm install session15-demo ... -n homework --wait` | Revision 1 deployed in Minikube. |
| `helm list -n homework` | Listed both the healthy `homework` release and `session15-demo`. |
| `helm status session15-demo -n homework` | Reported `STATUS: deployed`. |
| `helm get values session15-demo -n homework` | Showed the local image override and disabled database, Ingress and HPA for this disposable release. |
| `helm upgrade session15-demo ...` | Revisions 2 and 3 deployed with 3 then 4 replicas. |
| `helm history session15-demo -n homework` | Listed install, two upgrades and rollback revisions. |
| `helm rollback session15-demo 1 -n homework --wait` | Created revision 4 with `Rollback to 1`. |
| `helm uninstall session15-demo -n homework` | Removed the disposable release; `helm list -n homework` still showed `homework`, and `helm status session15-demo -n homework` returned `release: not found`. |

## Complete rollback workflow

The `homework` release previously completed an install, two upgrades and rollback. A separate disposable release repeated the full sequence on 8 October 2026, leaving the main release untouched:

```sh
helm install session15-demo final-devops-project/helm -n homework \
  --set database.enabled=false --set ingress.enabled=false --set autoscaling.enabled=false \
  --set image.repository=devops-homework-final-api --set image.tag=latest \
  --set image.pullPolicy=Never --wait --timeout=120s
helm upgrade session15-demo final-devops-project/helm -n homework --reuse-values --set replicaCount=3 --wait --timeout=120s
kubectl rollout status deployment/session15-demo -n homework
# 3/3 Ready
helm upgrade session15-demo final-devops-project/helm -n homework --reuse-values --set replicaCount=4 --wait --timeout=120s
kubectl rollout status deployment/session15-demo -n homework
# 4/4 Ready
helm rollback session15-demo 1 -n homework --wait --timeout=120s
kubectl rollout status deployment/session15-demo -n homework
# 2/2 Ready
helm history session15-demo -n homework
helm status session15-demo -n homework
```

The actual `helm history` showed revision 1 install, revisions 2 and 3 upgrades, and revision 4 `Rollback to 1` with `deployed` status. The Deployment was `2/2` Ready after rollback. [The rollback screenshot](helm-rollback.png) captures these results before uninstalling the disposable release.

After the rollback capture, `helm uninstall session15-demo -n homework` reported `release "session15-demo" uninstalled`. The [uninstall screenshot](helm-uninstall.png) shows the main `homework` release still deployed and the disposable release absent.
