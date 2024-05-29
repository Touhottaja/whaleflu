# whaleflu
Whaleflu is a dumb malware I'm developing for fun. Strictly for educational purposes.

The malware attempts to detect instances in the network and multiply itself over discovered instances, kind of like a botnet.

## Starting Scenarion & Goal
![Whaleflu graph](img/whaleflu_chart.png)  
The starting scenario is that the malware has already infected one machine in the network (marked with red) and it's calling back home (c2c, marked with blue). Communicataion happens over simple Python scripts [whaleflu_c2c.py](whaleflu_c2c.py) and [whaleflu.py](whaleflu.py)

## Environment
The sandbox environment consists of multiple Ubuntu Docker containers, connected via Docker network.

### Requirements
- [Docker Engine](https://docs.docker.com/engine/install/ubuntu/)

## Running the virtual environment
Build the images all at once via:
```sh
$ chmod +x build_containers.sh
$ ./build_containers.sh
```
or build them individually:  
- Build the infected image from Dockerfile: `$ docker build -t whaleflu_infected . --target=infected`
- Build the non-infected image from Dockerfile: `$ docker build -t whaleflu_base . --target=base`
- Build the C2C image from Dockerfile: `$ docker build -t whaleflu_c2c . --target=c2c`

After the Docker images have been build:
- Start the environment: `$ docker compose up --detach`
- You can enter the individual containers by first getting the container ID via `$ docker ps` and then running: `$ docker exec -it [<Container ID>] bash`

The container based on images `whaleflu_c2c` and `whaleflu_infected` have scripts `whaleflu_c2c.py` and `whaleflu.py`, respectively. You can enter each container via `$ docker exec -it [<Container ID>] bash` and execute the scripts via `$ python3 [<whaleflu_c2c.py || whaleflu.py>]`. The containers use these scripts to communicate with each other, you can think of it as the malware is calling back home. Simply put `whaleflu_c2c.py` is the C2C server, `whaleflu.py` is the client.

### Additional instructions, debugging
To get the IP address of the containers, run: `$ docker inspect [<Container ID>] |grep "IPAddress"`

To test the network connection is fine, you can enter one of the containers and ping the another:
```sh
$ docker exec -it [<Container ID>] bash
# Inside of the container
$ ping [<IP of the other container>]
64 bytes from XXX.XXX.X.X: icmp_seq=1 ttl=64 time=0.110 ms
```
