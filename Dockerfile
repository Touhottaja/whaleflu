FROM ubuntu:22.04 AS base

RUN apt-get update -y
RUN apt-get install -y \
    iputils-ping \
    iproute2 \
    vim \
    python3 \
    net-tools \
    openssh-client \
    openssh-server

# Set an unsecure password for the root user
RUN echo 'root:root' | chpasswd

# Command to start the ssh service and keep the container running
CMD service ssh start && tail -f /dev/null

### Base image for target machines
FROM base AS whaleflu_base

# Generate ssh key with poor password
RUN mkdir -p /root/.ssh && \
    ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -q -N "root"

# Allow root login via ssh
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

### Infected machine image
FROM whaleflu_base as infected
COPY whaleflu.py .

### C2C image
FROM base as c2c
COPY whaleflu_c2c.py .
