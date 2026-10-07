# CoreDNS in Kubernetes

**Student Details:**  
Name: Pranav Bharadwaj  
Roll Number: **24bcs10006**

---

## 1. What is CoreDNS?

**CoreDNS** is a flexible, extensible DNS server written in Go that acts as the default internal cluster DNS service for Kubernetes. It runs as a Deployment in the `kube-system` namespace and is backed by the `kube-dns` Service.

---

## 2. Why Kubernetes Uses CoreDNS

- **Dynamic Service Discovery**: As pods scale up, down, or get rescheduled, their IP addresses change constantly. CoreDNS continuously watches the Kubernetes API server for Service and EndpointSlice changes and updates DNS records immediately without service restarts.
- **Pluggable Architecture**: Implemented as a chain of plugins (e.g., `kubernetes`, `forward`, `cache`, `errors`, `health`, `prometheus`, `loop`).
- **Low Resource Footprint & High Performance**: Lightweight, memory-safe, and capable of handling thousands of queries per second per instance.

---

## 3. How DNS Resolution Works in Kubernetes

1. **Pod Configuration**: When a Pod is scheduled, `kubelet` configures `/etc/resolv.conf` with:
   - `nameserver`: Points to the ClusterIP of `kube-dns` service (e.g., `10.96.0.10`).
   - `search`: Search paths (`<ns>.svc.cluster.local`, `svc.cluster.local`, `cluster.local`).
   - `options ndots:5`: If the query has fewer than 5 dots, search domains are appended first.
2. **Cluster Queries**: If a query matches `*.cluster.local`, the `kubernetes` plugin resolves it against Kubernetes Services or Endpoints.
3. **External Queries**: If a query is for an external domain (e.g., `google.com`), CoreDNS forwards it via the `forward` plugin to upstream resolvers (typically `/etc/resolv.conf` on the host).

---

## 4. CoreDNS Configuration (Corefile)

The CoreDNS configuration is stored in a ConfigMap named `coredns` in the `kube-system` namespace:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
           lameduck 5s
        }
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }
```

---

## 5. Troubleshooting Kubernetes DNS Issues

### Step 1: Verify CoreDNS Pods & Service
```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl get svc -n kube-system -l k8s-app=kube-dns
```

### Step 2: Check CoreDNS Logs
```bash
kubectl logs -n kube-system -l k8s-app=kube-dns
```

### Step 3: Run Interactive DNS Lookup Pod
```bash
kubectl run dnsutils --image=tianon/true --restart=Never
# Or test using nslookup from a busybox pod:
kubectl run -it --rm test-dns --image=busybox:1.36 --restart=Never -- nslookup kubernetes.default
```

### Common Root Causes & Fixes:
1. **CoreDNS in CrashLoopBackOff**: Often caused by DNS loops (`loop` plugin detecting upstream loop to itself). Fix by pointing host DNS to upstream public DNS servers (8.8.8.8) rather than 127.0.0.53.
2. **Missing Endpoints for Service**: Service selector does not match Pod labels. Check `kubectl get endpoints <service-name>`.
3. **NetworkPolicy Blocking DNS**: Ensure egress on port 53 (UDP/TCP) to `kube-system` is permitted.
