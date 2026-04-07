#!/bin/bash

ROOT_URL=$1
THREADS=8
CONNECTIONS=100
DURATION=15s

URLS=(
  "$ROOT_URL/api/projects"
  "$ROOT_URL/api/skills"
  "$ROOT_URL/api/photographs"
  "$ROOT_URL/api/data"
  "$ROOT_URL/fetch?limit=10&offset=0"
)

for url in "${URLS[@]}"
do
    echo "Testing: $url" | tee -a ../artifacts/wrk_results.txt
    wrk -t$THREADS -c$CONNECTIONS -d$DURATION --latency $url | tee -a ../artifacts/wrk_results.txt
    echo "---------------------------------------" | tee -a ../artifacts/wrk_results.txt
done

echo "Load test complete." | tee -a ../artifacts/wrk_results.txt
