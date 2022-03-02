#!/usr/bin/env bash
if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit 1
fi
export COLOR_TEST=$1
cluster_name="MyEKSCluster"
aws_region="us-east-1"

aws eks update-kubeconfig --region $aws_region --name $cluster_name

envsubst < kubernetes/clustering-deployment-blue-green.yaml | kubectl apply -f -
envsubst < kubernetes/ingress.yaml | kubectl apply -f -
