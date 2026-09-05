#!/usr/bin/env bash

set -e

red='\033[0;31m'
green='\033[0;32m'
yellow='\033[1;33m'
no_colour='\033[0m'

export TEST_DATABASE_URL="postgres://local:password@localhost:5432/acp_migrations_test_db?sslmode=disable"
migrations_dir="backend/db/migrations"

echo -e "${yellow}Testing migrations from ${migrations_dir}${no_colour}"
echo -e "${yellow}Using TEST_DATABASE_URL=${TEST_DATABASE_URL}${no_colour}"

cleanup() {
  echo -e "${yellow}Dropping test DB${no_colour}"
  dbmate -e TEST_DATABASE_URL --no-dump-schema drop || echo -e "${red}Failed to drop test DB${no_colour}"
}
trap cleanup EXIT

if ! dbmate -e TEST_DATABASE_URL --no-dump-schema --wait create; then
  echo -e "${red}Failed to create test DB${no_colour}"
  trap - EXIT
  exit 1
fi

echo -e "${yellow}→ Running all migrations${no_colour}"
if ! dbmate -e TEST_DATABASE_URL --no-dump-schema -d "$migrations_dir" migrate; then
  echo -e "${red}Migration failed${no_colour}"
  exit 1
fi

echo -e "${yellow}← Rolling back all migrations${no_colour}"
while true; do
  set +e
  output=$(dbmate -e TEST_DATABASE_URL --no-dump-schema -d "$migrations_dir" rollback 2>&1)
  exit_code=$?
  set -e
  echo "$output"

  if [[ "$output" == *"can't rollback: no migrations have been applied"* ]] && [[ "$exit_code" -eq 2 ]]; then
    echo "↑ This is an expected error that indicates all migrations were successfully downed"
    break
  elif [[ "$exit_code" -ne 0 ]]; then
    echo -e "${red}Unexpected error while rolling back${no_colour}"
    exit 1
  fi
done

echo -e "${green}✔ All migrations were successful${no_colour}"
