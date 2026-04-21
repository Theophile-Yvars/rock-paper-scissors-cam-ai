#!/bin/bash

IMAGE_NAME=rock-paper-scissors-backend
IMAGE_TAG_CURRENT=1.0.0

echo "### Build new image ${IMAGE_NAME}:${IMAGE_TAG_CURRENT}"
docker build  --tag ${IMAGE_NAME}:${IMAGE_TAG_CURRENT} .