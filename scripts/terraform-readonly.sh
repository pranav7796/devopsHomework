#!/usr/bin/env bash
set -euo pipefail

case "${1:-}" in
  terraform-s3-demo|terraform-cloud|final-devops-project/terraform) project="$1" ;;
  *) echo 'First argument must name one of the three homework Terraform directories.' >&2; exit 2 ;;
esac
shift
case "${1:-}" in
  init|fmt|validate|plan|show|output|version|providers) ;;
  *) echo 'Only read-only Terraform commands are supported; apply/destroy require separate approval.' >&2; exit 2 ;;
esac
root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
export AWS_CONFIG_FILE="$root/scripts/aws-login.config"
export AWS_PROFILE=devops-new
export AWS_REGION=ap-southeast-2
export AWS_EC2_METADATA_DISABLED=true
exec terraform -chdir="$root/$project" "$@"
