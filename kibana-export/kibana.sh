#!/bin/bash

# Elasticsearch and Kibana details
ELASTICSEARCH_URL="http://localhost:9200"
KIBANA_URL="http://localhost:5601"
INDEX=".kibana"
DASHBOARD_FILE="./export.ndjson"

# Import the dashboard
curl -X POST "$KIBANA_URL/api/saved_objects/_import" \
  -H "kbn-xsrf: true" \
  --form file=@$DASHBOARD_FILE