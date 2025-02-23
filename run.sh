#!/bin/bash

# Default values
DEFAULT_URL="https://example.com"
DEFAULT_BROWSERS="chromium,firefox"

# Use provided URL or default
URL=${1:-$DEFAULT_URL}
BROWSERS=${2:-$DEFAULT_BROWSERS}

# Build and run
docker-compose build
docker-compose run cross-browser-test --url "$URL" --browsers "$BROWSERS"