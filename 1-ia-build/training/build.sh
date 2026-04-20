#!/bin/bash

IMAGE_NAME=rps/training
IMAGE_TAG_CURRENT=1.0.0

echo "### Build new image ${IMAGE_NAME}:${IMAGE_TAG_CURRENT}"
docker build --no-cache --tag ${IMAGE_NAME}:${IMAGE_TAG_CURRENT} .