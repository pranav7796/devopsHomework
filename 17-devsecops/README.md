# Session 17: DevSecOps

Workflow gates: Bandit (SAST), pip-audit (Python SCA), Gitleaks (secret scan), and Trivy (HIGH/CRITICAL image CVEs with fixed versions considered). Image publication depends on all checks passing. The Actions token is scoped to package publishing; PRs only read repository contents. Review findings rather than suppressing them. Pin third-party actions to reviewed full commit SHAs before hardened production use; this educational workflow currently uses version tags. A successful remote run and published image require pushing to GitHub.
