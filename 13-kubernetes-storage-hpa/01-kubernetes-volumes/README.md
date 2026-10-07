# Kubernetes storage concepts

- `emptyDir`: temporary directory shared by containers in one Pod; removed with the Pod.
- `hostPath`: mounts a node path; ties workloads to node layout and can expose host files. Avoid for application data.
- PersistentVolume (PV): cluster storage resource, provisioned by an administrator or dynamically.
- PersistentVolumeClaim (PVC): workload request for capacity and access mode.
- StorageClass: selects a provisioner and storage parameters; PVCs can trigger dynamic provisioning.

Example PVC is `../../final-devops-project/kubernetes/storage-demo.yaml`. Apply and inspect with `kubectl apply -f ...`, `kubectl get pvc,pv,storageclass`. Provisioning depends on a configured default StorageClass. Database persistence in Compose uses the named `database-data` volume.
