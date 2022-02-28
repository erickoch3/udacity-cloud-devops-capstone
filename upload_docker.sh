#!/usr/bin/env bash
# This file tags and uploads an image to Docker Hub

# Assumes that an image is built via `run_docker.sh`

username="ewkoch3"
repo_name="base"
tag="cn_news_clusters"

# Step 1:
# Create dockerpath
dockerpath="$username/$repo_name"

# Step 2:  
# Authenticate & tag
echo "Docker ID and Image: $dockerpath"
docker login --username=$username
docker tag $tag $dockerpath:$tag

# Step 3:
# Push image to a docker repository
docker push "$dockerpath:$tag"