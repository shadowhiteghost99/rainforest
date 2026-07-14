#!/bin/bash

tag="dev"

docker run -d --name dev --mount type=bind,source="$(pwd)",target=/app "rainforest:${tag}" sh -c "while true; do date '+%Y-%m-%d %H:%M:%S'; sleep 600; done"
