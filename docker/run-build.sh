#!/bin/bash

rm -rf files
mkdir files
cp ../ccturtle files -r || exit 1
cp ../static files -r || exit 1
cp ../setup.py files/ || exit 1
docker build -t build/turtle . || exit 1

