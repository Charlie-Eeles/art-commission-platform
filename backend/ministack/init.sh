#!/usr/bin/env bash
set -euo pipefail

aws s3 mb s3://portfolio-images || true
