#!/bin/bash

# Ping all instances in the network to update ARP table
ping 192.168.0.1 -c 1
ping 192.168.0.2 -c 1
ping 192.168.0.3 -c 1
ping 192.168.0.4 -c 1

# Start the ssh service and keep the container running
service ssh start && tail -f /dev/null
