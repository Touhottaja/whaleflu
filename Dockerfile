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

# Ensure that the package lists are updated again before proceeding to
# install python3-pip dependencies and python3-pip
RUN apt-get update -y
RUN apt-get install -y \
    libc-dev-bin \
    libc6-dev \
    libc-devtools \
    python3-pip

# Set an unsecure password for the root user
RUN echo 'root:root' | chpasswd

COPY init.sh /usr/local/bin/init.sh
RUN chmod +x /usr/local/bin/init.sh

ENTRYPOINT ["/usr/local/bin/init.sh"]

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
