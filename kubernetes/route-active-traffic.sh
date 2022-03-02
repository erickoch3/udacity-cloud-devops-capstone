#!/usr/bin/env bash
if [ $1 -ne "blue" && $1 -ne "green" ]
  then
    echo "Usage: $0 [blue / green]"
    exit 1
fi
export COLOR_ACTIVE=$1
cluster_name="MyEKSCluster"
aws_region="us-east-1"

aws eks update-kubeconfig --region $aws_region --name $cluster_name

envsubst < kubernetes/route.yaml | kubectl create -f -

