# whaleflu
Whaleflu is a dumb malware I'm developing for fun. Do not use for malicious purposes, thank you :)

## Environment
The sandbox environment consists of multiple Ubuntu Docker containers, connected via Docker network.

### Requirements
- [Docker Engine](https://docs.docker.com/engine/install/ubuntu/)

## Running the virtual environment
1. Build the image from Dockerfile: `$ docker build -t ubuntu_sandbox .`
2. Start the environment: `$ docker compose up`
3. In another terminal, check the status: `$ docker ps`

### Additional instructions, debugging
To get the IP address of the containers, run: `$ docker inspect [<Container ID>] |grep "IPAddress"`

To test the network connection is fine, you can enter one of the containers and ping the another:
```sh
$ docker exec -it [<Container ID>] bash
# Inside of the container
$ ping [<IP of the other container>]
64 bytes from XXX.XXX.X.X: icmp_seq=1 ttl=64 time=0.110 ms
```
