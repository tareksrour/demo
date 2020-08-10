#!/bin/bash

ISMASTER=$(mongo --quiet --eval 'db.isMaster().ismaster')
if [ "$ISMASTER" = "true" ]
then
    exit 0
else
    exit 2
fi
