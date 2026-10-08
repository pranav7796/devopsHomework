# Session 14: Kubernetes troubleshooting

```sh
kubectl get pods -o wide
kubectl describe pod POD
kubectl logs POD --previous
kubectl exec POD -- printenv
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl explain deployment.spec
kubectl top pods
```

| Symptom | Investigation | Likely cause and fix |
|---|---|---|
| CrashLoopBackOff | `describe`, current and previous logs | Process exits/configuration error; fix command/config and redeploy. |
| ErrImagePull / ImagePullBackOff | Pod events, image field, registry auth | Wrong tag or missing pull credentials; fix image reference/Secret. |
| Pending | `describe`, node capacity, PVC events | Unschedulable requests, taints, or unbound claim; resolve capacity/constraints/storage. |
| ContainerCreating | Pod events, CSI/CNI and node status | Image pull, mount or networking setup failure; inspect the named event. |
| Service unreachable | Service selector, EndpointSlices, targetPort, readiness | Correct labels/ports and ensure Ready endpoints. |
| DNS failure | `/etc/resolv.conf`, `nslookup`, CoreDNS pods/logs | Check service name/namespace, CoreDNS health/config and NetworkPolicy. |
| Configuration issue | `describe`, `printenv`, mounted files | Correct ConfigMap/Secret key and restart pods after env changes. |

## Isolated Pod failure drill

Apply [`broken-pods.yaml`](broken-pods.yaml) to the disposable `session14-debug` namespace. It creates five independent faults; the healthy `homework` release stays untouched. Commands actually run:

```sh
kubectl apply -f 14-kubernetes-troubleshooting/broken-pods.yaml
kubectl get pods -n session14-debug -o wide
kubectl get events -n session14-debug --sort-by=.lastTimestamp
kubectl describe pod crash-loop -n session14-debug
kubectl describe pod bad-image -n session14-debug
kubectl describe pod pending-node -n session14-debug
kubectl describe pod missing-volume -n session14-debug
kubectl describe pod missing-key -n session14-debug
kubectl logs crash-loop -n session14-debug
kubectl explain pod.spec.nodeSelector
kubectl top pods -n homework
```

| Problem | Before output and investigation | Root cause | Fix and verification |
|---|---|---|---|
| CrashLoopBackOff | `crash-loop` repeatedly exited; events said `Back-off restarting failed container` | The command exits with status 1 | Replace with a long running command; Pod Ready and logs show healthy startup |
| ErrImagePull / ImagePullBackOff | `bad-image` alternated these states; events show registry DNS failed while resolving an intentionally invalid tag | The image reference is invalid; local Minikube registry DNS also failed | Use the locally loaded `nginx:1.27-alpine`; Pod Ready |
| Pending | `pending-node` had no assigned node; scheduler said node selector did not match | Selector names a nonexistent node | Remove selector; Pod schedules and becomes Ready |
| ContainerCreating | `missing-volume` had `FailedMount`: ConfigMap absent | Required volume source does not exist | Create `session14-absent-config`; Pod Ready |
| Configuration | `missing-key` showed `CreateContainerConfigError`; event said `APP_MODE` key absent | ConfigMap has only `WRONG_KEY` | Supply `APP_MODE`; Pod Ready and `kubectl exec` prints `healthy` |

The fixed resource values are in [`fixed-pods.yaml`](fixed-pods.yaml). Pods have immutable commands and node selectors, so delete only these five disposable Pods and reapply their corrected definitions after adding the repaired ConfigMaps. Record real before and after output/screenshots. Service, DNS and Pod networking drills are documented separately below.

Actual local before state: `bad-image` showed `ImagePullBackOff`, `crash-loop` restarted repeatedly with BackOff events, `missing-key` showed `CreateContainerConfigError`, `missing-volume` stayed in `ContainerCreating` with `FailedMount`, and `pending-node` stayed `Pending` with `FailedScheduling`. [Before screenshot](session14-pods-before.png).

After replacing only these five Pods using `fixed-pods.yaml`, `kubectl wait --for=condition=Ready pod --all -n session14-debug --timeout=90s` succeeded. All five showed `1/1 Running`; `kubectl logs crash-loop` returned `healthy startup`, and `kubectl exec missing-key -- printenv APP_MODE` returned `healthy`.

[After screenshot](session14.png) captures the five Ready Pods and both successful checks.

Reproducible broken examples are also in `../09-kubernetes-pods-deployments/troubleshooting/` and `../10-kubernetes-services/troubleshooting/`; do not apply them to a production namespace.

## Isolated Service, DNS and Pod networking drill

[`network-broken.yaml`](network-broken.yaml) creates three independent problems in `session14-debug`:

| Problem | Before output and investigation | Root cause | Intended fix |
|---|---|---|---|
| Service connectivity | `kubectl get endpoints session14-web` showed `<none>`; requests to the Service IP were refused | Service selector `app=wrong-label` does not match the ready `session14-web` Pod | Apply the matching selector from [`network-fixed.yaml`](network-fixed.yaml) and request the Service again |
| DNS | `nslookup session14-wbe.session14-debug.svc.cluster.local` returned `NXDOMAIN`; `session14-web.session14-debug.svc.cluster.local` resolved to `10.98.188.51` | Misspelled Service name (`wbe` instead of `web`) | Use the correct FQDN and confirm resolution |
| Pod networking | `wget http://10.244.0.59:8080` from another Pod returned `Connection refused`; `wget http://127.0.0.1:8080` inside `loopback-only` returned `session14-network-ok` | The app binds only to loopback, so the Pod IP cannot accept connections | Recreate the disposable Pod bound to `0.0.0.0:8080` and retry by Pod IP |

Actual troubleshooting commands include `kubectl get pods,svc,endpoints -n session14-debug`, `kubectl describe svc session14-web -n session14-debug`, `kubectl exec network-client -- nslookup ...`, `kubectl exec network-client -- wget ...`, and `kubectl exec loopback-only -- wget ...`. The main `homework` release is unaffected.

[Before screenshot](session14troubleshooting.png) captures all three real failures. After applying `network-fixed.yaml`, the Service endpoint was `10.244.0.58:80`; the correct FQDN resolved to `10.98.188.51`; a request to `http://session14-web` returned the Nginx page. The recreated `loopback-only` Pod had IP `10.244.0.61`, and a request from `network-client` to port 8080 returned `session14-network-ok`.

[After screenshot](networkafter.png) captures the repaired endpoint, DNS, Service HTTP and direct Pod-IP response.
