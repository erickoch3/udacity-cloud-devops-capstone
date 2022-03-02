#!/usr/bin/env bash

# Build an image and add a descriptive tag
docker build . --tag=cn_news_clusters

# List docker containers.
docker ps

# Run a cluster with the image.
docker run -p 8080:80 cn_news_clusters