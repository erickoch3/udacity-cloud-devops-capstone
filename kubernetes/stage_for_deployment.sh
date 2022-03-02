#!/usr/bin/env bash
cluster_name="MyEKSCluster"
aws_region="us-east-1"

aws eks update-kubeconfig --region $aws_region --name $cluster_name

echo "'$COLOR_ACTIVE' is the active deployment."
echo "We are deploying the '$COLOR_TEST' environment."

envsubst < kubernetes/clustering-deployment-blue-green.yaml | kubectl apply -f -
