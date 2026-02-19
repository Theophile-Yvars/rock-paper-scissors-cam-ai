#!/bin/bash

IMAGE_NAME=rock-paper-scissors-backend
IMAGE_TAG_CURRENT=0.0.0

cp ../../models/gesture_model.h5 .  

echo "### Build new image ${IMAGE_NAME}:${IMAGE_TAG_CURRENT}"
docker build  --tag ${IMAGE_NAME}:${IMAGE_TAG_CURRENT} .