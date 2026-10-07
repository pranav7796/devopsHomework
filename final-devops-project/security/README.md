# Security gates

The executable pipeline is at repository root `.github/workflows/devsecops.yml`; the copy under `final-devops-project/.github/workflows/` satisfies the final deliverable tree. Keep the two files identical when changing the workflow.

| Gate | Tool | Failure behavior |
|---|---|---|
| SAST | Bandit | Fails on medium/high confidence and medium/high severity findings (`-ll`) |
| SCA | pip-audit | Fails on vulnerable pinned Python dependencies |
| Secret scanning | Gitleaks | Fails when a secret pattern is found in repository content/history |
| Container image scanning | Trivy | Fails on fixable high/critical OS or library findings |

Do not bypass a finding merely to obtain a green badge. The publish job waits for every gate, then publishes a commit-tagged GHCR image and advances the Helm image tag in Git for Argo CD. GitHub's short-lived token needs package write and repository content write permission for this job. It does not need AWS keys.

For local checks, run `bandit -r final-devops-project/application -ll` and `pip-audit -r final-devops-project/application/requirements.txt` after installing the tools in an isolated environment. The current machine's local scan result is reported in `../../PROGRESS.md`; a hosted Actions result still requires a GitHub push.
