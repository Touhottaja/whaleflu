#!/bin/bash
docker build -t whaleflu_infected . --target=infected
docker build -t whaleflu_base . --target=base
docker build -t whaleflu_c2c . --target=c2c
