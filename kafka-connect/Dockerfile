# Utiliser l'image de base de Kafka Connect
FROM confluentinc/cp-kafka-connect:latest
USER root

# Installer le connecteur Elasticsearch Sink
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-elasticsearch:latest

RUN confluent-hub install --no-prompt confluentinc/connect-transforms:latest

RUN curl -O http://client.hub.confluent.io/confluent-hub-client-latest.tar.gz
RUN mkdir confluent-hub-client-latest
RUN tar -xf confluent-hub-client-latest.tar.gz -C confluent-hub-client-latest
RUN ./confluent-hub-client-latest/bin/confluent-hub install --no-prompt --verbose --component-dir /usr/share/confluent-hub-components confluentinc/kafka-connect-elasticsearch:10.0.1
