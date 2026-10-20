# Homework completion checks — 21 October 2026 (IST)

Local corrections and validation passed. All three authenticated AWS plans were subsequently applied, independently verified and destroyed. [Actual execution and absence checks](../aws-execution/README.md) establish successful provisioning/cleanup; the earlier planning snapshots alone do not.

| Check | Actual result | Evidence |
|---|---|---|
| Four deployment strategies in local Minikube | PASS: rolling v1→v2 (4 replicas), blue→green→blue (3 each), canary 9:1 endpoints with 86 stable/14 canary responses from 100 requests and stable-only rollback, Recreate with 3 replacement Pods | [results](strategy-results.json), [commands/output/exit codes](strategy-commands.json), [run output](strategy-run.txt) |
| Lab isolation/cleanup | Existing `minikube` profile restarted with `--keep-context`; only newly created namespace `homework-strategy-check` deleted | [startup](minikube-start.txt), [command journal](strategy-commands.json) |
| API unit tests | Four tests passed; test process was given empty DATABASE_URL so tests do not use a configured production database | [actual unittest output](api-unit-tests.txt) |
| Helm chart | Lint/render passed; no cluster apply | [lint](helm-lint.txt), [render](helm-render.txt) |
| Shell/Python helpers, Terraform formatting, mutation guards | PASS; wrapper rejects apply/destroy with expected exit 2 | [record](local-validation.json) |
| Authenticated Terraform init/fmt/validate/plan | PASS for all three projects, 26 additions total; zero planned changes/deletions; later apply/verification/cleanup succeeded separately | [AWS command records](../aws-plans/command-results.json), [plans and source/hash metadata](../aws-plans/summary.json), [run output](aws-plans-run.txt) |
| Private files/evidence references | Saved plans/input snapshots ignored; source/plan hashes checked; local Markdown links and limited credential-signature scan checked | [validation record](local-validation.json) |

The strategy checker adapts only Service type to ClusterIP and removes NodePort fields in test copies to avoid cluster-wide port collisions with existing labs. Deployment sources, labels/selectors and target ports are preserved. Versioned HTTP output, endpoints and rollout readiness were measured; continuous zero-downtime HTTP availability, exact request weighting and downtime duration were not. Some startup readiness probes briefly failed before the rollouts completed; these are not hidden by claiming uninterrupted availability.

The initial planning was read-only. After owner authorization, only the newly created homework AWS resources were deployed and deleted; no preexisting AWS resource or existing Kubernetes resource was deleted. This repository's AWS plans are independent of RelayDesk's running EKS deployment. The original active EKS context was preserved; local lab commands explicitly target `minikube`.

The accidental CLI-output file was moved to ignored private storage. The previously untracked multi-container screenshot was visually inspected, retained under a descriptive name and linked from the lifecycle guide with its original October 8 date. The preexisting removal of an unrelated-project Argo screenshot was preserved; this repository's actual final-project Argo evidence remains linked.

Computer Use returned no browser/app surfaces during the initial check. A subsequent pass captured [five genuine terminal screenshots](../screenshots-2026-10-21/README.md) using Foot/Grim, including the missing plan image, saved AWS lifecycle excerpts and freshly queried CI status. The AWS captures explicitly label saved output and do not rerun deployment. See [AWS-HOMEWORK.md](../../AWS-HOMEWORK.md) for resource/cost/cleanup scope and completed execution/cleanup proof.

## Final hosted CI and publication

[Run 39500684657](https://github.com/pranav7796/devopsHomework/actions/runs/39500684657), source `a372702`, completed successfully: all test/security steps, Docker build, Trivy, GHCR publication and GitOps image-tag advancement passed. [Metadata](ci-success.json). Initial false-positive failures and their local reproduction are retained; [scope checks](gitleaks-scope-check.json) show only the exact public image line at its exact path is exempt, while changed values, other paths and extra text still trigger the scanner. This successful source run precedes the documentation-only publication of its metadata.
