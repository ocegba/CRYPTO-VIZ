# Utiliser l'image de base de Kafka Connect
FROM confluentinc/cp-kafka-connect:latest
USER root

# Installer le connecteur Elasticsearch Sink
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-elasticsearch:latest

RUN confluent-hub install --no-prompt confluentinc/connect-transforms:latest

WORKDIR /app

# Copier le script d'initialisation dans le conteneur
COPY init-kafka-connect.sh /app/init-kafka-connect.sh

# Donner les droits d'exécution au script
RUN chmod +x /app/init-kafka-connect.sh

# Exécuter le script pendant le build (commented out for now)
# RUN /app/init-kafka-connect.sh

# Définir l'utilisateur par défaut pour Kafka Connect
USER 1001
