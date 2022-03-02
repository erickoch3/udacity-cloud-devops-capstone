#!/usr/bin/env bash
if kubectl get pods | grep "blue"
  then
    echo "Active deployment is 'blue'."
    export COLOR_ACTIVE="blue"
    export COLOR_TEST="green"
  else
    echo "Active deployment is 'green'."
    export COLOR_ACTIVE="green"
    export COLOR_TEST="blue"
fi

