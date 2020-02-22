#!/bin/bash

UUID=$(curl http://localhost:5000/arithmetic/$1 -d @arguments.json -s | sed -nE 's/.*"uuid": "(.*)"}/\1/p')
echo $UUID
curl http://localhost:5000/arithmetic/$UUID
echo ""
