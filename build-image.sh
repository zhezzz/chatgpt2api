#!/usr/bin/env sh
set -e

if [ -n "$PLATFORM" ]; then
  docker buildx build --platform "$PLATFORM" --target app -t chatgpt2api:latest --load .
else
  docker buildx build --target app -t chatgpt2api:latest --load .
fi
