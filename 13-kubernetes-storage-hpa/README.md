# Session 13: Storage, HPA and probes

## Deliverables

- Volume documentation: [`01-kubernetes-volumes/README.md`](01-kubernetes-volumes/README.md) covers `emptyDir`, `hostPath`, PV, PVC, StorageClass and dynamic provisioning.
- HPA YAML: [`hpa.yml`](hpa.yml), applied in the `homework` namespace.
- Load generator: [`load-generator.yml`](load-generator.yml), a 16-worker BusyBox Job that requests the `homework` Service.
- HPA output: actual local Minikube output below.
- Screenshots: [actual HPA, CPU, Pod and PVC evidence](session13.png).
- Mini project: the functional API, PostgreSQL StatefulSet with bound PVC, probes, Service and HPA in `../final-devops-project/`. The source assignment does not specify a separate Session 13 mini-project brief.
- README documentation: this file and the volume guide.

## Hands-on commands

The final Helm chart was installed in a local Minikube `homework` namespace with its database Secret and locally loaded images. Metrics Server was enabled. From the repository root:

```sh
kubectl apply -f 13-kubernetes-storage-hpa/hpa.yml
kubectl get hpa,pods -n homework
kubectl top pods -n homework
kubectl apply -f 13-kubernetes-storage-hpa/load-generator.yml
kubectl get hpa,pods -n homework
kubectl top pods -n homework
kubectl describe hpa homework -n homework
kubectl delete job homework-load-generator -n homework
```

## Observed output, 7 October 2026

Before corrected load generation, `kubectl get hpa -n homework` reported `cpu: 2%/70%`, `REPLICAS 2`. `kubectl top pods` reported approximately `1m` CPU for each API Pod. The first load Job used the wrong Service name and printed `wget: bad address 'homework-api'`; it was deleted and replaced with the corrected manifest above.

After about three minutes of corrected load:

```text
$ kubectl get hpa,pods -n homework
NAME                                           REFERENCE             TARGETS         MINPODS   MAXPODS   REPLICAS
horizontalpodautoscaler.autoscaling/homework   Deployment/homework   cpu: 150%/70%   2         8         8

NAME                                READY   STATUS
pod/homework-785cc6d764-7787m       1/1     Running
pod/homework-785cc6d764-9d96b       1/1     Running
pod/homework-785cc6d764-b9jmk       1/1     Running
pod/homework-785cc6d764-dnpkf       1/1     Running
pod/homework-785cc6d764-l9pqg       1/1     Running
pod/homework-785cc6d764-pqrnj       1/1     Running
pod/homework-785cc6d764-r4xr8       1/1     Running
pod/homework-785cc6d764-zfqnd       1/1     Running
pod/homework-db-0                   1/1     Running
pod/homework-load-generator-rxccp   1/1     Running

$ kubectl top pods -n homework
NAME                            CPU(cores)   MEMORY(bytes)
homework-785cc6d764-7787m       84m          27Mi
homework-785cc6d764-9d96b       74m          28Mi
homework-db-0                   499m         38Mi
homework-load-generator-rxccp   97m          7Mi
```

The HPA reached its configured maximum of eight replicas. The Job was then deleted. The PostgreSQL claim remained `Bound` at 1 GiB. These values are one local observation, not guaranteed results in every cluster.

A second live run on 7 October 2026 again reached eight Ready API Pods; the screenshot shows `cpu: 119%/70%`, `REPLICAS 8`, a Bound claim and `SuccessfulRescale` events. The load Job was deleted after capture.
