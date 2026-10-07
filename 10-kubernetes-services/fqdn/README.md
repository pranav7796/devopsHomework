# Fully Qualified Domain Name (FQDN) in Kubernetes

**Student Details:**  
Name: Pranav Bharadwaj  
Roll Number: **24bcs10006**

---

## 1. What is an FQDN?

An **FQDN (Fully Qualified Domain Name)** is the complete, unambiguous domain name specifying an exact location in the Domain Name System (DNS) hierarchy. It includes all domain levels, including the top-level domain.

In Kubernetes, every Service and Pod gets an automatic internal FQDN registered in CoreDNS.

---

## 2. Anatomy of a Kubernetes Service FQDN

A standard Kubernetes Service FQDN follows this structure:

```text
<service-name>.<namespace>.svc.<cluster-domain>
```

For example, a service named `backend` in the `production` namespace within standard cluster domain `cluster.local`:
```text
backend.production.svc.cluster.local
```

### Breakdown of Components:
1. **Service Name (`backend`)**: The `metadata.name` specified in the Service manifest.
2. **Namespace (`production`)**: The namespace where the Service is deployed.
3. **Resource Type (`svc`)**: Identifies the resource as a Service in the cluster.
4. **Cluster Domain (`cluster.local`)**: The default root DNS zone for the Kubernetes cluster.

---

## 3. Namespace-Based DNS Resolution

Kubernetes configures `/etc/resolv.conf` inside every Pod with search domains:

```text
nameserver 10.96.0.10
search <namespace>.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

### Resolution Rules:
- **Same Namespace Communication:**  
  A pod in `production` can access `backend` using just the short name:
  ```bash
  curl http://backend:8080
  ```
  The resolver appends `production.svc.cluster.local` automatically.

- **Cross-Namespace Communication:**  
  A pod in `frontend` namespace accessing `backend` in `production` namespace must specify at least:
  ```bash
  curl http://backend.production:8080
  # Or full FQDN:
  curl http://backend.production.svc.cluster.local:8080
  ```

---

## 4. Pod-to-Service Communication Flow

```text
+--------------+       1. DNS Query: "backend"       +-----------+
|  Client Pod  | ----------------------------------> |  CoreDNS  |
|              | <---------------------------------- |           |
+--------------+       2. Returns ClusterIP          +-----------+
       |
       | 3. Connect to ClusterIP:8080
       v
+--------------+
|  kube-proxy  | (iptables / IPVS rule)
+--------------+
       |
       +--------------------+
       | Load-balances      |
       v                    v
+--------------+     +--------------+
|  Backend #1  |     |  Backend #2  |
|  10.244.0.5  |     |  10.244.0.6  |
+--------------+     +--------------+
```

---

## 5. Pod FQDNs (Headless Services & StatefulSets)

For StatefulSets associated with a headless Service (`spec.clusterIP: None`):
```text
<pod-name>.<service-name>.<namespace>.svc.<cluster-domain>
```

Example for MongoDB replica 0:
```text
mongodb-0.mongodb-service.database.svc.cluster.local
```
This enables direct, stable addressing of individual stateful pods.
