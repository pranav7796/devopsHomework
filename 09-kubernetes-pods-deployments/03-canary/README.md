# Canary Deployment Strategy

## What is a Canary Deployment?

A **Canary Deployment** is a risk-reduction strategy where a new version receives a small share of traffic while the stable version continues serving the rest. With the Kubernetes Service shown here, the endpoint ratio approximates that share over many new connections; it does not set an exact percentage of users or requests.

The name comes from mining history: coal miners used to carry canary birds into mines. If the canary died, it warned the miners of toxic gas before the gas could harm them. Similarly, the canary pods absorb any defects in a new release before all users are impacted.

```text
                     [SERVICE] (port 30030)
                          |
          [kube-proxy distributes requests across ALL pods]
                          |
     +--------------------+------------------------+
     |         |         |         |         |     |
     v         v         v         v         v     v
[stable] [stable] [stable] [stable] [stable] ... [canary]
  v1       v1       v1       v1       v1     (x9)  v2 (x1)
       9 stable endpoints : 1 canary endpoint
```

---

## Why Do We Need Canary?

### Problems with Rolling Update and Blue-Green:
* **Rolling Update:** Replica replacement alone does not configure a precise traffic weight; requests can reach the new version once its Pods become Ready.
* **Blue-Green:** The switch is all-or-nothing (100% flip). If v2 has a subtle bug that only appears under high traffic conditions, you discover it after all users are on v2.

### Benefits of Canary:
* A small share of endpoint traffic reaches v2 while you validate it; the replica ratio does not guarantee an exact share of users or requests.
* You can observe real production metrics (error rate, response time, CPU usage) for v2 before promoting it to 100%.
* If the canary shows problems, scale it to 0 replicas. The replica ratio limits exposure approximately; it does not prove how many users saw a defect.

---

## How Traffic Split Works in Kubernetes (Pod Ratio Math)

The Service selects all Ready Pods with the shared `app: myapp-canary` label. A standard Kubernetes Service does not configure a precise traffic weight or promise exact round-robin request distribution. The 9:1 replica ratio makes canary exposure approximate over many new connections; observed request percentages vary, especially when clients reuse connections. Use a traffic-splitting ingress or a rollout controller when a precise weight is required.

| Stable Replicas | Canary Replicas | Total Pods | Approximate Canary Endpoint Share |
| :--- | :--- | :--- | :--- |
| 9 | 1 | 10 | 10% |
| 8 | 2 | 10 | 20% |
| 5 | 5 | 10 | 50% |
| 2 | 8 | 10 | 80% |
| 0 | 10 | 10 | 100% (fully promoted) |

---

## Important Points

* **The Service selects BOTH stable and canary pods** using only the shared label (`app: myapp-canary`). The `track: stable` and `track: canary` labels are for human identification only — not for routing.
* Kubernetes-native canary is **approximate** (uses pod-ratio math). For precise percentage control (e.g. exactly 5.3%), use **Argo Rollouts**, **Flagger**, or an Ingress-level traffic split (e.g. NGINX Ingress weight annotations).
* Monitor the canary for at least **1 full traffic cycle** (15-30 minutes in production) before increasing traffic.
* Always define alerting thresholds BEFORE the canary goes live: "If error rate > 1% on canary pods for 5 minutes, auto-rollback."

---

## Production Use Cases

* Google, Netflix, and Meta use canary deployments for every single code push to production.
* Feature flags are often combined with canary: send 10% of traffic to new pods AND enable the new feature flag only for those 10%.
* Machine learning model updates: serve the new model to 5% of users, compare prediction accuracy vs the old model, then promote.

---

## Code Files

| File | Purpose |
| :--- | :--- |
| `deployment-stable.yaml` | 9 replicas of v1 (stable, dark background) — 9 of 10 matching endpoints |
| `deployment-canary.yaml` | 1 replica of v2 (canary, orange background) — 1 of 10 matching endpoints |
| `service.yaml` | NodePort Service on `30030`, selecting both stable and canary pods |

---

## Step-by-Step Commands

### Step 1: Deploy Stable v1 (9 Ready Endpoints)
```bash
kubectl apply -f 03-canary/deployment-stable.yaml
```

Wait until all 9 stable pods are running:
```bash
kubectl rollout status deployment/app-stable
```

### Step 2: Deploy the Service
```bash
kubectl apply -f 03-canary/service.yaml
```

### Step 3: Test — All Traffic Goes to Stable v1
```bash
for i in $(seq 1 10); do curl -s http://$(minikube ip):30030 | grep -o "STABLE v1\|CANARY v2"; done
```

Expected output (10 out of 10 requests hit stable):
```text
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
```

### Step 4: Deploy Canary v2 (1 of 10 Ready Endpoints)
```bash
kubectl apply -f 03-canary/deployment-canary.yaml
```

Wait until the canary pod is running:
```bash
kubectl get pods -l app=myapp-canary --show-labels
```

Expected output (9 stable + 1 canary = 10 pods total):
```text
NAME                           READY   STATUS    LABELS
app-stable-6d7f8c5b4-2mqpt    1/1     Running   app=myapp-canary,track=stable,version=v1
app-stable-6d7f8c5b4-4krgn    1/1     Running   app=myapp-canary,track=stable,version=v1
app-stable-6d7f8c5b4-7jxqz    1/1     Running   app=myapp-canary,track=stable,version=v1
...  (9 stable total)
app-canary-9b6d4e7c8-5fmpx    1/1     Running   app=myapp-canary,track=canary,version=v2
```

### Step 5: Verify Traffic Split in Real Time
```bash
for i in $(seq 1 20); do curl -s http://$(minikube ip):30030 | grep -o "STABLE v1\|CANARY v2"; done
```

Illustrative output only; twenty requests can produce a different count, including no canary response:
```text
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
CANARY v2
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
```

### Step 6: Increase Canary Endpoint Share to 30% (3 of 10 Ready Pods)
```bash
kubectl scale deployment app-canary --replicas=3
kubectl scale deployment app-stable --replicas=7
```

Verify endpoints updated:
```bash
kubectl get endpoints myapp-canary-service
# Now shows 10 endpoints: 7 stable IPs + 3 canary IPs
```

Re-run the traffic test:
```bash
for i in $(seq 1 10); do curl -s http://$(minikube ip):30030 | grep -o "STABLE v1\|CANARY v2"; done
# Count observed responses; a ten-request sample need not match the endpoint ratio.
```

### Step 7A: Promote Canary to 100% (Canary is Healthy)
```bash
# Scale canary to full replicas and remove stable
kubectl scale deployment app-canary --replicas=9
kubectl scale deployment app-stable --replicas=0
```

Once only canary endpoints remain, new requests reach v2:
```bash
for i in $(seq 1 5); do curl -s http://$(minikube ip):30030 | grep -o "STABLE v1\|CANARY v2"; done
# CANARY v2 x5
```

After confirming stable, clean up old stable deployment:
```bash
kubectl delete deployment app-stable
```

### Step 7B: Rollback Canary (Canary is Broken)
```bash
kubectl scale deployment app-canary --replicas=0
kubectl scale deployment app-stable --replicas=9
```

Once endpoints update, new connections reach stable v1. Existing connections can take longer to drain:
```bash
for i in $(seq 1 5); do curl -s http://$(minikube ip):30030 | grep -o "STABLE v1\|CANARY v2"; done
# STABLE v1 x5
```

---

## Cleanup
```bash
kubectl delete -f 03-canary/service.yaml
kubectl delete -f 03-canary/deployment-canary.yaml
kubectl delete -f 03-canary/deployment-stable.yaml
```
