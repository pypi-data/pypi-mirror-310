#!/bin/bash
set -o errexit -o pipefail -o nounset
rm -fr dist/*
python3 -m build

echo "Use pypi on dashlane (without vpn)"
twine upload dist/*

export TWINE_USERNAME=python-gw
export NEXUS_REPOSITORY_URL=https://nexus.gatewatcher.com/repository
export TWINE_REPOSITORY_URL=${NEXUS_REPOSITORY_URL}/pypi-gw-prod/
twine upload dist/* -p "j2A3XjBt3Rg2pq9ro6YtN8wCbxhmvUV7"


