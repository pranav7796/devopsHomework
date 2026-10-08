# Session 17: DevSecOps

Workflow gates: Bandit (SAST), pip-audit (Python SCA), Gitleaks (secret scan), and Trivy (HIGH/CRITICAL image CVEs with fixed versions considered). Image publication depends on all checks passing. The Actions token is scoped to package publishing; PRs only read repository contents. Review findings rather than suppressing them. Pin third-party actions to reviewed full commit SHAs before hardened production use; this educational workflow currently uses version tags.

The [8 October 2026 hosted run](https://github.com/pranav7796/devopsHomework/actions/runs/37801718339) passed `test-and-security` and `publish`. [Screenshot evidence](../final-devops-project/evidence/github-actions.png) shows the successful pipeline; the run retains the individual scan logs and Gitleaks SARIF artifact.
