FROM python:3.9-bookworm

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libgl1 \
    libgl1-mesa-dri \
    libglib2.0-0 \
    libgles2 \
    libegl1 \
    python3-av \
    ffmpeg \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libavfilter-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Mise à jour de pip et installation des dépendances
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copier tout le code source dans le conteneur
# Copier le dossier models spécifiquement pour être sûr

COPY . .

# Exposer le port Streamlit
EXPOSE 8501

# Commande par défaut pour lancer l'application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]