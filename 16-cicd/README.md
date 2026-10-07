# Session 16: CI/CD

GitHub Actions workflow: `../.github/workflows/devsecops.yml`. CI checks out code and runs tests/scans/build on pushes and pull requests. On a push to `main`, the gated publish job logs in to GHCR using the short-lived `GITHUB_TOKEN` and publishes a commit-SHA image. CD to Kubernetes is performed through Argo CD reconciliation from Git rather than a CI-held cluster credential.

Push the repository and inspect **Actions** to capture a real successful run. No remote workflow run is claimed from this local checkout. Workflow logs are visible in the run; no credentials are committed.
