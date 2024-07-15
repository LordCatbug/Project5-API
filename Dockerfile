# Utiliser une image de base officielle de Python avec une version compatible de GLIBC
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . .

# Installer les dépendances
RUN python -m venv venv
RUN . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Exposer le port de l'application
EXPOSE 8000

# Définir la commande de démarrage
CMD ["./venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
