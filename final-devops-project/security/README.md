# Security gates

The executable pipeline is at repository root `.github/workflows/devsecops.yml`; the copy under `final-devops-project/.github/workflows/` satisfies the final deliverable tree. Keep the two files identical when changing the workflow.

| Gate | Tool | Failure behavior |
|---|---|---|
| SAST | Bandit | Fails on medium/high confidence and medium/high severity findings (`-ll`) |
| SCA | pip-audit | Fails on vulnerable pinned Python dependencies |
| Secret scanning | Gitleaks | Fails when a secret pattern is found in repository content/history |
| Container image scanning | Trivy | Fails on fixable high/critical OS or library findings |

Do not bypass a finding merely to obtain a green badge. The publish job waits for every gate, then publishes a commit-tagged GHCR image and advances the Helm image tag in Git for Argo CD. GitHub's short-lived token needs package write and repository content write permission for this job. It does not need AWS keys.

For local checks, run `bandit -r final-devops-project/application -ll` and `pip-audit -r final-devops-project/application/requirements.txt` after installing the tools in an isolated environment. The current machine's local scan result is reported in `../../PROGRESS.md`; the [successful hosted run](https://github.com/pranav7796/devopsHomework/actions/runs/37801718339) includes all four security gates.

## Captured Helm-output false positive — October 21, 2026 (IST)

The [first completion CI run](https://github.com/pranav7796/devopsHomework/actions/runs/39498942669) passed tests, Bandit and pip-audit, then reported one `generic-api-key` finding at line 48 of `evidence/completion-2026-10-21/helm-render.txt`. That value is the public immutable image tag already present in `final-devops-project/helm/values.yaml` before the audit, not a credential. The captured output is preserved without annotation or rewriting.

The root `.gitleaksignore` excludes only this finding's exact commit/file/rule/line fingerprint, using [Gitleaks 8.24.3's documented fingerprint mechanism](https://github.com/gitleaks/gitleaks/blob/v8.24.3/README.md#gitleaksignore). No rule or evidence directory is excluded, and new findings remain subject to the existing failure gate. The exception does not claim that every future scan is clean.
