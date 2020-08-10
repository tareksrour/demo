#!/bin/bash
export PRIVATE_IP_ADDRESS=$( ifconfig | sed -n '2 p' | awk '{print $2}')

nohup consul agent -bind $PRIVATE_IP_ADDRESS \
    -advertise $PRIVATE_IP_ADDRESS \
    -join consul_server \
    -node $NODE\
    -dns-port 53 \
    -data-dir /data \
    -config-dir /etc/consul.d \
    -enable-local-script-checks &

mongod --bind_ip_all --port $MONGO_PORT --dbpath /data/db --replSet "rs0"
