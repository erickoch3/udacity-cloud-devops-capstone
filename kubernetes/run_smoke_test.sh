#!/usr/bin/env bash
TEST_URL="a6628da774c9343ab937a6901b6bf011-1261375217.us-east-1.elb.amazonaws.com"
sleep 15
if curl "$TEST_URL" --max-time 1 | grep "Chinese"
  then
    echo "Success"
    exit 0
  else
    echo "Fail"
    exit 1
fi

