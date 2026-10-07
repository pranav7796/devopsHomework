# Session 12: ConfigMaps, Secrets, Ingress and Troubleshooting

The required standalone resource files are [`configmap.yaml`](configmap.yaml), [`secret.yaml`](secret.yaml), and [`ingress.yaml`](ingress.yaml). The Secret YAML deliberately contains no credential and must **not** be applied without local values. The runnable plain Kubernetes stack is in `../final-devops-project/kubernetes/base.yaml` and `postgres.yaml`; the Helm equivalent is in `../final-devops-project/helm/`. Create the Secret locally and never commit its rendered output:

```sh
read -rsp 'Local database password (URL-safe characters): ' DB_PASSWORD; echo
DATABASE_URL="postgresql://homework:${DB_PASSWORD}@homework-db:5432/homework"
kubectl create secret generic homework-api-secret --from-literal=DB_PASSWORD="$DB_PASSWORD" --from-literal=DATABASE_URL="$DATABASE_URL" --dry-run=client -o yaml | kubectl apply -f -
unset DB_PASSWORD DATABASE_URL
kubectl apply -f ../final-devops-project/kubernetes/postgres.yaml
kubectl apply -f ../final-devops-project/kubernetes/base.yaml
kubectl exec deploy/homework-api -- printenv PORT
kubectl get ingress,svc,pods
```

A ConfigMap holds non-sensitive configuration. A Secret separates sensitive values, but base64 encoding is not encryption; use RBAC and encryption at rest or an external secret manager. Ingress is the routing rule; an Ingress Controller implements it. The Ingress resource alone cannot route traffic because it is only API configuration; ingress-nginx watches it and programs an Nginx proxy. Other controllers include Traefik and AWS Load Balancer Controller. Install a controller before testing `homework.local`. A Service selects the application Pods and gives the controller a stable backend. `kubectl port-forward svc/homework-api 8080:80` checks that backend independently.

The local Helm deployment uses release name `homework` in namespace `homework`. Its ConfigMap key `PORT=8000` and Secret key `DATABASE_URL` are injected into the API Pod. Verify without disclosing the password:

```sh
kubectl get configmap homework -n homework -o jsonpath='{.data.PORT}'; echo
API_POD=$(kubectl get pod -n homework -l app.kubernetes.io/name=homework-api -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n homework "$API_POD" -c api -- /bin/sh -c 'printf "PORT=%s DATABASE_URL_present=%s\n" "$PORT" "${DATABASE_URL:+yes}"'
```

Observed locally: `8000` and `PORT=8000 DATABASE_URL_present=yes`. The Helm release is upgraded with `--set ingress.enabled=true` after the controller is ready. Test routing with `curl --resolve homework.local:80:$(minikube ip) http://homework.local/health` (or `curl -H 'Host: homework.local' http://$(minikube ip)/health`).

Actual local Ingress result: the ingress-nginx controller was `1/1 Running`, `kubectl get ingress homework -n homework -o wide` reported `192.168.49.2`, and the routed `/health` request returned `{"status":"healthy"}`. The ConfigMap and Secret injection check returned `PORT=8000 DATABASE_URL_present=yes`. [Screenshot evidence](kubernetes12.png).

## Isolated troubleshooting exercise

1. Problem: Service routes to no pods in isolated namespace `session12-debug`.
2. Apply [`troubleshooting/broken-service.yaml`](troubleshooting/broken-service.yaml). The Pod label is `app: session12-web`; the Service selector is `app: wrong-label`.
3. Investigate with `kubectl get pods,svc,endpoints -n session12-debug`, `kubectl describe svc session12-web -n session12-debug`, and `kubectl get pods -n session12-debug --show-labels`.
4. Root cause: the Service selector differs from the Pod label, so there are no ready endpoints and requests fail.
5. Fix with `kubectl apply -f troubleshooting/fixed-service.yaml`.
6. Verify the endpoint appears and HTTP from a temporary BusyBox client returns Nginx HTML. Capture genuine before and after screenshots.

Local before evidence: the Pod was `1/1 Running`, but `endpoints/session12-web` showed `<none>`; `kubectl describe svc` showed selector `app=wrong-label` while `kubectl get pods --show-labels` showed `app=session12-web`. [Before screenshot](kubernetes12session.png).

Local fix: applying `troubleshooting/fixed-service.yaml` changed the Service selector to `app=session12-web`; its endpoint became `10.244.0.41:80`. A BusyBox client request to `http://session12-web` returned the Nginx welcome HTML. Capture the after state before cleaning up the demo namespace.

[After screenshot](kuberenetes12troubleshooting.png) shows the populated endpoint, correct selector and successful client response.

Do not change the working base manifests to stage the broken scenario.
