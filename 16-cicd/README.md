# Session 16: CI/CD

GitHub Actions workflow: `../.github/workflows/devsecops.yml`. CI checks out code and runs tests/scans/build on pushes and pull requests. On a push to `main`, the gated publish job logs in to GHCR using the short-lived `GITHUB_TOKEN` and publishes a commit-SHA image. CD to Kubernetes is performed through Argo CD reconciliation from Git rather than a CI-held cluster credential.

The [8 October 2026 Actions run](https://github.com/pranav7796/devopsHomework/actions/runs/37801718339) completed successfully on `main`: both `test-and-security` and `publish` passed. [Screenshot evidence](../final-devops-project/evidence/github-actions.png) shows both green jobs. Workflow logs and build artifacts are available from the run; no credentials are committed.
