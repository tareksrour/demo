#!/bin/bash
export IP_ADDRESS=$( ifconfig | sed -n '2 p' | awk '{print $2}')

# Start Consul Agent in Server mode
consul agent -server \
    -bind $IP_ADDRESS \
    -advertise $IP_ADDRESS \
    -node $NODE \
    -client 0.0.0.0 \
    -dns-port 53 \
    -data-dir /data \
    -ui -bootstrap
