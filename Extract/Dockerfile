# Utilisez une image Python officielle comme base
FROM python:3.9-slim

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers de dépendance dans le conteneur
COPY requirements.txt .

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le contenu du répertoire local vers le répertoire de travail du conteneur
COPY . .

# Commande à exécuter lors du démarrage du conteneur
CMD ["python", "./producer.py"]
