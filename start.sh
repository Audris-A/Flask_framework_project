#!/bin/bash
app="docker.projecttwo"
docker build -t ${app} .
docker run -d -p 56733:80 \
  --name=${app} \
  -v $PWD:/project ${app}
