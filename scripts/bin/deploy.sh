#!/usr/bin/env bash

set -e

host="ubuntu@18.169.122.197"
key=".ssh/art-commission-platform-api.pem"
repo="https://github.com/Charlie-Eeles/art-commission-platform.git"
remote="/home/ubuntu/art-commission-platform"
env_file="backend/.env.production"

ssh -i "$key" "$host" "
    set -e

    sudo apt-get update
    sudo apt-get install -y git docker.io docker-compose-v2
    sudo systemctl enable --now docker

    if [ ! -d '$remote/.git' ]; then
        git clone '$repo' '$remote'
    fi

    cd '$remote'
    git fetch origin main
    git reset --hard origin/main
    git clean -fd
"

scp -i "$key" \
    "$env_file" \
    "$host:$remote/backend/.env"

ssh -i "$key" "$host" "
    set -e

    chmod 600 '$remote/backend/.env'

    cd '$remote'

    sudo docker compose -f compose.production.yml up \
        -d \
        --build \
        --remove-orphans
"
