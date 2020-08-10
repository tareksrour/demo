#!/bin/bash
nohup consul agent -bind $PRIVATE_IP_ADDRESS \
    -advertise $PRIVATE_IP_ADDRESS \
    -join consul_server \
    -node $NODE\
    -dns-port 53 \
    -data-dir /data \
    -config-dir /etc/consul.d \
    -enable-local-script-checks &

./tmp/wait-for-it.sh mongo_1:27017 -- mongo --host mongo_1 /tmp/config.js
