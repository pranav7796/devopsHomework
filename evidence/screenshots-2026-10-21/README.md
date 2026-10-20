# Screenshot evidence — 21 October 2026 (IST)

Five genuine screenshots were captured from a dedicated opaque Foot terminal using Grim on this machine's Wayland desktop. All five were visually inspected for readable, complete output. No image was synthesized or edited, and no AWS resources were created for these captures.

The AWS screenshots display **excerpts from the saved authenticated execution logs**, not a fresh deployment or AWS Console pages. Their headers show the original execution dates and explicitly state that the temporary resources were destroyed. Full source files and exact original commands/exit codes remain available alongside the images. The CI panel displays a fresh GitHub API response for the completed run, retrieved immediately before capture.

| Screenshot | Source / purpose |
|---|---|
| [Terraform plan](../../terraform-cloud/evidence/terraform-plan.png) | Missing Session 19 deliverable: all 11 planned resource addresses and the actual plan totals, from [s19-plan.txt](../aws-plans/s19-plan.txt) |
| [Session 18 lifecycle](s18-evidence.png) | S3 apply, security controls, destroy and absence checks |
| [Session 19 lifecycle](s19-evidence.png) | EC2/S3 apply, HTTP 200 response, destroy, terminated instance and absent VPC/disk/bucket |
| [Final-project lifecycle](final-evidence.png) | Independent final-project EC2/S3 execution and cleanup |
| [Successful CI](ci-evidence.png) | [Run 39501169416](https://github.com/pranav7796/devopsHomework/actions/runs/39501169416): tests, Bandit, pip-audit, Gitleaks, build, Trivy, publish and GitOps tag update |

[Capture provenance](provenance.json) records actual terminal/capture commands, UTC times, image hashes and hashes of the displayed source files. [CI response](ci-run.json) retains the queried job/step results. [Capture helper](capture.py) preserves the exact extraction and capture method; it is specific to this desktop and only reads evidence/GitHub. It never applies Terraform or changes AWS. The API run screenshot proves the named run, not any later documentation commit.

The Computer Use connector still returned no app/browser surfaces; the system's dedicated screenshot tools supplied the capture path. Existing historical screenshots were retained under their original filenames and dates. There are no AWS Console screenshots of the now-deleted homework resources; these terminal captures do not claim otherwise.
