#!/usr/bin/env bash
TEST_URL="a00d1e37d2cf14c77a6ce2447da47529-1852105403.us-east-1.elb.amazonaws.com"
if curl "$TEST_URL" --max-time 1 | grep "Chinese"
  then
    echo "Success"
    exit 0
  else
    echo "Fail"
    exit 1
fi

