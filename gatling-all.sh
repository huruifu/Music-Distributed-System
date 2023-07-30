#!/usr/bin/env bash
# Run Gatling from container
set -o nounset
set -o errexit

if [[ $# -ne 1 ]]
then
  echo "Usage: ${0} USER_COUNT"
  exit 1
fi

docker container run --detach --rm \
  -v ${PWD}/gatling/results:/opt/gatling/results \
  -v ${PWD}/gatling:/opt/gatling/user-files \
  -v ${PWD}/gatling/target:/opt/gatling/target \
  -e CLUSTER_IP=`tools/getip.sh kubectl istio-system svc/istio-ingressgateway` \
  -e USERS=${1} \
  -e SIM_NAME=ReadUserPostMusicPutPlaylistSim \
  --label gatling \
  ghcr.io/scp-2021-jan-cmpt-756/gatling:3.4.2 \
  -s proj756.ReadUserPostMusicPutPlaylistSim