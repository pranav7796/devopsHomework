# Monitoring, observability and GitOps

Metrics are numeric time series used for trends and alerts; logs are timestamped event records; traces connect a request across services. Together they help explain system behavior. Kubernetes monitoring commonly collects node, workload, and application metrics plus container logs; tracing adds request paths. Prometheus scrapes metrics and evaluates alert rules; Grafana visualizes configured data sources. This repo includes a Prometheus scrape configuration and Grafana provisioning, but needs a running cluster and installed monitoring stack to produce live dashboards/alerts.

GitOps treats version-controlled desired state as the source of truth. An in-cluster controller continuously compares live resources with Git and reconciles drift. Argo CD application declaration is in `../final-devops-project/gitops/`; installing Argo CD and syncing require cluster access. No Synced/Healthy state is claimed.
