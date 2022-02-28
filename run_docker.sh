#!/usr/bin/env bash

## Complete the following steps to get Docker running locally

# Step 1:
# Build image and add a descriptive tag
docker build . --tag=cn_news_clusters

# Step 2: 
docker ps

# Step 3: 
docker run -p 8000:80 cn_news_clusters