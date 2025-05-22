# Usa un'immagine Python ufficiale come base
FROM python:3.11-slim

# Aggiungi le dipendenze necessarie per la compilazione dei pacchetti Python (come cffi, lxml)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Imposta la working directory nel container
WORKDIR /app

# Copia solo requirements.txt all'inizio, per sfruttare la cache Docker
COPY requirements.txt .

# Aggiorna pip e installa le dipendenze, usando --no-cache-dir per ridurre la dimensione
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia tutto tranne venv e gli script .sh
COPY . .

# Esponi la porta (modifica la porta in base alla tua app)
EXPOSE 3333

# Aggiungi un .dockerignore per escludere venv/ e *.sh
# .dockerignore dovrebbe includere almeno:
# venv/
# *.sh

# Comando di avvio, da personalizzare secondo la tua app
CMD ["python", "main.py"]
