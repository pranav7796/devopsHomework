# Kubernetes Pod Lifecycle Lab

This lab demonstrates the major Pod lifecycle situations using small, independent YAML files.

## Recommended

1. Running
2. Pending
3. Init container
4. Readiness
5. Liveness
6. Startup probe
7. Succeeded
8. Failed
9. CrashLoopBackOff
10. ImagePullBackOff
11. Multi-container Pod
12. Graceful termination

## Start the live watch

Run this in Terminal 1:

```bash
kubectl get pods -w
```

Then apply examples from another terminal.

## Basic commands

Create:
```bash
kubectl apply -f 01-running.yaml
```

Watch:
```bash
kubectl get pods -w
```

Detailed lifecycle:
```bash
kubectl describe pod lifecycle-running
```

Logs:
```bash
kubectl logs lifecycle-running
```

Container state:
```bash
kubectl get pod lifecycle-running -o jsonpath='{.status.containerStatuses[0].state}'
```

Full YAML/status:
```bash
kubectl get pod lifecycle-running -o yaml
```

Delete:
```bash
kubectl delete pod lifecycle-running
```

## Important note about STATUS

`kubectl get pods` may display values such as:

- Pending
- Running
- Completed
- Error
- CrashLoopBackOff
- ImagePullBackOff
- ContainerCreating
- Terminating

These are not all official Pod phases.

Official Pod phases are:

- Pending
- Running
- Succeeded
- Failed
- Unknown

Container states are:

- Waiting
- Running
- Terminated

## 1. Running

```bash
kubectl apply -f 01-running.yaml
kubectl get pod lifecycle-running
```

Expected:
```text
NAME                READY   STATUS    RESTARTS
lifecycle-running   1/1     Running   0
```

In the isolated `session10-lifecycle` namespace, the Pod reached `1/1 Running` with `nginx:1.27-alpine`; `kubectl describe` showed `State: Running` and `Ready: True`. [Live output screenshot](01-running.png).

## 2. Pending

```bash
kubectl apply -f 02-pending.yaml
kubectl get pod lifecycle-pending
kubectl describe pod lifecycle-pending
```

This requests impossible CPU/memory resources, so on a normal small cluster it should remain Pending.

The exact message depends on the cluster.

In `session10-lifecycle`, the Pod remained `0/1 Pending`; `kubectl describe` showed a `100Gi` memory request and `FailedScheduling: Insufficient memory`. [Live output screenshot](02-pending.png).

## 3. Succeeded

```bash
kubectl apply -f 03-succeeded.yaml
kubectl get pod lifecycle-succeeded
kubectl logs lifecycle-succeeded
```

Expected status:
```text
Completed
```

Pod phase:
```text
Succeeded
```

The local Pod finished as `Completed` with phase `Succeeded` and exit code `0`; its log ends with `Task completed successfully`. [Live output screenshot](03-succeeded.png).

## 4. Failed

```bash
kubectl apply -f 04-failed.yaml
kubectl get pod lifecycle-failed
kubectl logs lifecycle-failed
```

Expected status:
```text
Error
```

Pod phase:
```text
Failed
```

The local Pod ended in `Error` with phase `Failed` and exit code `1`; its log says `Task failed`. [Live output screenshot](04-failed.png).

## 5. CrashLoopBackOff

```bash
kubectl apply -f 05-crashloopbackoff.yaml
kubectl get pod lifecycle-crashloop -w
```

The container starts, exits with code 1, gets restarted, and keeps failing.

In `session10-lifecycle`, the container exited with code `1` and entered a restart backoff. The status can cycle between `Running`, `Error`, and `CrashLoopBackOff`; the captured `describe` output shows the terminated state and `BackOff` event. [Live output screenshot](05-crashloopbackoff.png).

Inspect:
```bash
kubectl describe pod lifecycle-crashloop
kubectl logs lifecycle-crashloop
kubectl logs lifecycle-crashloop --previous
```

## 6. ImagePullBackOff

```bash
kubectl apply -f 06-imagepullbackoff.yaml
kubectl get pod lifecycle-image-error
kubectl describe pod lifecycle-image-error
```

The image tag intentionally does not exist.

The local Pod showed `ImagePullBackOff`; `kubectl describe` identified the invalid image and pull failure. [Live output screenshot](06-imagepullbackoff.png).

## 7. Readiness probe

```bash
kubectl apply -f 07-readiness.yaml
kubectl get pod lifecycle-readiness -w
```

Inspect:
```bash
kubectl describe pod lifecycle-readiness
```

Important teaching point:

```text
Running != Ready
```

Readiness answers:
"Should this Pod receive traffic?"

The local readiness Pod reached `1/1 Running`; `kubectl describe` showed `Ready: True` and an HTTP probe on port `80`. [Live output screenshot](07-readiness.png).

## 8. Liveness probe

```bash
kubectl apply -f 08-liveness.yaml
kubectl get pod lifecycle-liveness -w
```

The health file is removed after 20 seconds. The liveness probe then fails and Kubernetes restarts the container.

Watch:
```bash
kubectl get pod lifecycle-liveness -w
```

Look at:
```text
RESTARTS
```

The local liveness Pod restarted after its health file was removed; `kubectl get` showed `RESTARTS 1` and `kubectl describe` showed the configured probe. [Live output screenshot](08-liveness.png).

## 9. Startup probe

```bash
kubectl apply -f 09-startup.yaml
kubectl get pod lifecycle-startup -w
```

The application intentionally takes 30 seconds to start.

The startup probe gives it time before normal health management takes over.

The local Pod reached `1/1 Running` after its delayed start; logs showed `Application started`, and `kubectl describe` showed the startup probe. [Live output screenshot](09-startup.png).

## 10. Init container

```bash
kubectl apply -f 10-init-container.yaml
kubectl get pod lifecycle-init -w
```

Inspect:
```bash
kubectl describe pod lifecycle-init
kubectl logs lifecycle-init -c setup
```

Teaching point:

```text
Init container runs first
        ↓
Init completes
        ↓
Main container starts
```

The local Pod reached `1/1 Running`; init logs ended with `Init complete`, and `kubectl describe` showed the init container `Completed` before the Nginx container ran. [Live output screenshot](10-init-container.png).

## 11. Multi-container Pod

```bash
kubectl apply -f 11-multi-container.yaml
kubectl get pod lifecycle-multi-container
```

Expected:
```text
2/2
```

View individual container logs:
```bash
kubectl logs lifecycle-multi-container -c app
kubectl logs lifecycle-multi-container -c sidecar
```

The local Pod reached `2/2 Running`; `kubectl describe` showed both `app` and `sidecar` containers running and ready. [Live output screenshot](11-multi-container.png).

Teaching point:

```text
One Pod
  ├── app container
  └── sidecar container
```

## 12. Graceful termination

```bash
kubectl apply -f 12-termination.yaml
kubectl get pod lifecycle-termination
```

Then in another terminal:

```bash
kubectl delete pod lifecycle-termination
```

Watch:
```bash
kubectl get pod lifecycle-termination -w
```

The process handles SIGTERM, performs cleanup, and exits.

In `session10-lifecycle`, `kubectl get pod -w` showed the Pod move from `1/1 Running` through `Terminating` to `Completed` after deletion. A later `kubectl get` confirmed the Pod was gone. [Live output screenshot](12-termination.png).

## Cleanup everything

```bash
kubectl delete -f .
```

If you want to remove only these lab Pods:

```bash
kubectl delete pod lifecycle-running lifecycle-pending lifecycle-succeeded lifecycle-failed lifecycle-crashloop lifecycle-image-error lifecycle-readiness lifecycle-liveness lifecycle-startup lifecycle-init lifecycle-multi-container lifecycle-termination
```

## Suggested teaching flow

Use:

```bash
kubectl get pods -w
```

while applying each YAML.

For every example ask students:

1. What state/status do you see?
2. Is the container running?
3. Is the Pod ready?
4. Did the container restart?
5. Why did this happen?
6. Which command would you use to debug it?

The three most useful debugging commands are:

```bash
kubectl get pod <pod>
kubectl describe pod <pod>
kubectl logs <pod>
```
