#!/bin/bash
SERVER="$1"
USER="$2"
TOKEN="$3"

docker login "$SERVER" --username "$USER" --password "$TOKEN" --tls-verify=false
