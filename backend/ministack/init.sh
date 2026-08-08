#!/usr/bin/env bash
set -euo pipefail

aws s3 mb s3://portfolio-images || true
aws s3 sync /seed-images s3://portfolio-images
