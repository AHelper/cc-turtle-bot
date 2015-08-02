#!/bin/bash

./run-build.sh || exit
docker run --name turtle -it --rm -p 34299:34299 build/turtle ccturtlesrv
