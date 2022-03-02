#!/usr/bin/env bash

export COLOR_TEST=$1
cluster_name="MyEKSCluster"
aws_region="us-east-1"

aws eks update-kubeconfig --region $aws_region --name $cluster_name

kubectl apply -f clustering-deployment-blue-green.yaml

