#!/usr/bin/env bash
# This file deploys a container to Kubernetes (EKS)

cluster_name="MyEKSCluster"
aws_region="us-east-1"
username="ewkoch3"
repo_name="base"
tag="cn_news_clusters"
dockerpath="$username/$repo_name:$tag"
name="clustering"

# First, we need to set up our kubeconfig
aws eks update-kubeconfig --region $aws_region --name $cluster_name

# Describe our Kubernetes service to confirm connection.
kubectl get svc

# Run in Docker Hub container with kubernetes
kubectl run $name\
    --image=$dockerpath\
    --port=80 --labels app=$name

# List kubernetes pods to check if it's deploying.
kubectl get pods

