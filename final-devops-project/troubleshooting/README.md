# Final troubleshooting challenge

Use a disposable namespace such as `homework-drill`. Keep the healthy `homework` release intact. The sample YAML files intentionally fail and are excluded from Helm/Argo CD.

## ImagePullBackOff

1. **Problem:** `bad-image.yaml` references a nonexistent image tag.
2. **Symptoms:** Pod reports `ErrImagePull`, then `ImagePullBackOff`.
3. **Investigation:** `kubectl apply -n homework-drill -f bad-image.yaml`; `kubectl get pods -n homework-drill`; `kubectl describe pod -n homework-drill -l app=broken-image-demo` (use actual Pod name for `describe`).
4. **Root cause:** Registry cannot serve that tag.
5. **Fix:** Change to an available image tag, then reapply in the drill namespace.
6. **Verification:** `kubectl rollout status deployment/broken-image-demo -n homework-drill`; check Pod Ready and logs.

## Empty Service endpoints

1. **Problem:** `bad-service.yaml` selects `app: no-such-pod`.
2. **Symptoms:** `kubectl get endpoints -n homework-drill broken-service-demo` has no addresses; traffic fails.
3. **Investigation:** `kubectl describe svc -n homework-drill broken-service-demo`; `kubectl get pods -n homework-drill --show-labels`.
4. **Root cause:** Service selector and Pod labels differ.
5. **Fix:** Change Service selector to the label on an existing Ready Pod and reapply.
6. **Verification:** EndpointSlice includes the Pod IP; a request through the Service returns HTTP 200.

For CrashLoopBackOff, Pending, DNS, probes and configuration issues see `../../14-kubernetes-troubleshooting/README.md`. Capture before/after output only after running each drill; no success is claimed here. Cleanup drill resources with `kubectl delete namespace homework-drill` after confirming it contains only the exercise.
