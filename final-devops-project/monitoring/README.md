# Local monitoring demo

Start the final API Compose stack first. Then set a local Grafana admin password and start monitoring:

```sh
export GRAFANA_ADMIN_PASSWORD='choose-a-local-password'
docker compose -f final-devops-project/monitoring/compose.yaml up -d
docker compose -f final-devops-project/monitoring/compose.yaml ps
```

Prometheus runs on `http://localhost:9090`; Grafana runs on `http://localhost:3000`. Query `up{job="homework-api"}`, `homework_http_requests_total`, `node_cpu_seconds_total`, and `node_memory_MemAvailable_bytes`. A `HomeworkApiDown` rule triggers if API scraping fails for a minute. Application logs are visible with `docker compose -f final-devops-project/docker/compose.yaml logs api`. Stop monitoring with `docker compose -f final-devops-project/monitoring/compose.yaml down`. Metrics are only live while both stacks run.
