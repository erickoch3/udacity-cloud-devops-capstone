#!/usr/bin/env bash
if ! [[ "$1" =~ ^(blue|green)$ ]]
  then
    echo "Usage: $0 [blue / green]"
    exit 1
fi
if [ $1 = "blue" ]
  then
    export COLOR_ACTIVE="blue"
    export COLOR_TEST="green"
  else
    export COLOR_ACTIVE="green"
    export COLOR_TEST="blue"
fi
cluster_name="MyEKSCluster"
aws_region="us-east-1"

aws eks update-kubeconfig --region $aws_region --name $cluster_name

envsubst < kubernetes/ingress.yaml | kubectl apply -f -

