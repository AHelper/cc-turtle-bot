#!/bin/bash

./run-build.sh || exit
docker rm turtle
docker run --name turtle -it build/turtle /bin/bash

