#!/bin/bash

cp ../ccturtle files -r
cp ../static files -r
cp ../setup.py files/
docker build -t build/turtle .

