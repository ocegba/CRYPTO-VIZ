# Utiliser l'image de base de Kafka Connect
FROM confluentinc/cp-kafka-connect:latest
USER root

# Installer le connecteur Elasticsearch Sink
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-elasticsearch:10.0.1

RUN confluent-hub install --no-prompt confluentinc/connect-transforms:latest

WORKDIR /app