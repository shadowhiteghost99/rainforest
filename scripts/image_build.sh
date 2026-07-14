#!/bin/bash

TAG_PARAM="${1}"
TAG="${TAG_PARAM:-dev}"

echo "docker build -t rainforest:${TAG} ."
docker build -t rainforest:${TAG} .
