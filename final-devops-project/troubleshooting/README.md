# Final troubleshooting challenge

The two faults below were reproduced and repaired in the disposable `homework-drill` namespace on 8 October 2026. The healthy `homework` release was left intact. The broken manifests are excluded from Helm and Argo CD.

## Problems, investigation and root causes

| Problem | Before output | Investigation and root cause | Fix |
|---|---|---|---|
| API image cannot start | `broken-image-demo` Deployment `0/1`; Pod `ErrImagePull`, followed by `ImagePullBackOff` | `kubectl describe pods -l app=broken-image-demo -n homework-drill` showed an attempt to pull `devops-homework-final-api:tag-that-does-not-exist`. The tag is deliberately invalid; the local cluster also could not resolve Docker Hub. | Apply [`fixed-image.yaml`](fixed-image.yaml), which uses the locally loaded `devops-homework-final-api:latest` image with `imagePullPolicy: Never`. |
| Service has no backend | `broken-service-demo` endpoints `<none>` | `kubectl describe svc broken-service-demo -n homework-drill` showed selector `app=no-such-pod`; the Deployment's Pod label is `app=broken-image-demo`. | Apply [`fixed-service.yaml`](fixed-service.yaml) with the matching selector. |

## Reproduce and repair

From the repository root, with the final API image loaded into Minikube:

```sh
kubectl create namespace homework-drill
kubectl apply -n homework-drill \
  -f final-devops-project/troubleshooting/bad-image.yaml \
  -f final-devops-project/troubleshooting/bad-service.yaml
kubectl get deploy,pods,svc,endpoints -n homework-drill -o wide
kubectl describe pods -l app=broken-image-demo -n homework-drill
kubectl describe svc broken-service-demo -n homework-drill

kubectl apply -n homework-drill \
  -f final-devops-project/troubleshooting/fixed-image.yaml \
  -f final-devops-project/troubleshooting/fixed-service.yaml
kubectl rollout status deployment/broken-image-demo -n homework-drill
kubectl run drill-client -n homework-drill --image=busybox:1.36 \
  --image-pull-policy=Never --restart=Never --command -- sleep 3600
kubectl wait --for=condition=Ready pod/drill-client -n homework-drill --timeout=60s
kubectl get deploy,pods,svc,endpoints -n homework-drill -o wide
kubectl get endpointslice -n homework-drill \
  -l kubernetes.io/service-name=broken-service-demo -o wide
kubectl exec drill-client -n homework-drill -- wget -qO- http://broken-service-demo/health
kubectl logs deployment/broken-image-demo -n homework-drill --tail=5
```

## Observed verification

Before repair, the API Deployment was `0/1`, its Pod was in `ErrImagePull`, and the Service had no endpoints. After repair, the rollout completed, the Deployment and API Pod were `1/1 Ready`, and the Service endpoint was `10.244.0.78:8000`. Its EndpointSlice listed the same Pod IP. The separate `drill-client` Pod received `{"status":"healthy"}` through the Service; API logs recorded `GET /health` with HTTP 200.

The fixed image manifest is for this local Minikube exercise. On another cluster, replace the image with an accessible published tag and choose an appropriate pull policy. The drill namespace can be removed after reviewing its resources with `kubectl delete namespace homework-drill`.
