# Session 15: Helm practice and rollback

Chart: `../final-devops-project/helm/`.

```sh
helm create scratch-chart
helm lint ../final-devops-project/helm
helm template homework ../final-devops-project/helm
helm install homework ../final-devops-project/helm
helm list
helm status homework
helm get values homework
helm upgrade homework ../final-devops-project/helm --set replicaCount=3
helm history homework
helm upgrade homework ../final-devops-project/helm --set replicaCount=4
helm rollback homework 1
helm status homework
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo bitnami/nginx
helm uninstall homework
```

Install/upgrade/rollback require a working Kubernetes cluster and a locally created `homework-api-secret`. `helm lint` and template rendering can run offline. This does not claim a cluster rollback occurred.
