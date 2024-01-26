#!/bin/bash 

# A brief pause to ensure Kafka Connect is fully operational
sleep 10

echo "Submitting connector configuration to Kafka Connect"c
curl -X POST -H "Content-Type: application/json" --data @./config/elasticsearch-sink.json http://localhost:8083/connectors
echo "Connector configuration submission attempted"
