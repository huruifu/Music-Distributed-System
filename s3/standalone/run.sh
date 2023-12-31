#!/usr/bin/env bash
# Run the service with the code for A1
set -o nounset
set -o errexit

if [[ $# -gt 1  || $# == 1 && "${1}"  != "--detached" ]]
then
  echo "Usage: ${0} [--detached]"
  exit 1
fi

if [[ $# -eq 1 ]]
then
  target=run-s3-detached
else
  target=run-s3
fi

make VER=v0.75 HWD=${HWD} ${target}