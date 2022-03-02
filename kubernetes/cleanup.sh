#!/usr/bin/env bash
if ! [[ "$1" =~ ^(blue|green)$ ]]
  then
    echo "Usage: $0 [blue / green]"
    exit 1
fi
KILL_COLOR=$1
cluster_name="MyEKSCluster"
aws_region="us-east-1"

aws eks update-kubeconfig --region $aws_region --name $cluster_name

kubectl delete deployment.apps/clustering-deployment-$KILL_COLOR
