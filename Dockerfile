FROM ubuntu:22.04 as base

RUN apt-get update -y
RUN apt-get install -y \
    iputils-ping \
    iproute2 \
    vim \
    python3 \
    net-tools

### Infected machine image
FROM base as infected
COPY whaleflu.py .

### C2C image
FROM base as c2c
COPY whaleflu_c2c.py .
