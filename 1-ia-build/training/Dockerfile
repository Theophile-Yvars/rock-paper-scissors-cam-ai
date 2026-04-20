# Utilisation d'une image Python légère
FROM python:3.9-bookworm

# Définition du répertoire de travail
WORKDIR /app

# Installation des dépendances système nécessaires pour OpenCV et MediaPipe
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copie du fichier des prérequis et installation
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copie du reste du code source
COPY . .

# Exposer le port de Streamlit
EXPOSE 8501

# Lancement de l'application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]