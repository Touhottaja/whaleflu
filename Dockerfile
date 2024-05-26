FROM ubuntu:22.04 as base

RUN apt-get update -y
RUN apt-get install -y \
    iputils-ping \
    iproute2

CMD ["bash"]
