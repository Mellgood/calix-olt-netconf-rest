# Usa un'immagine Python ufficiale come base
FROM python:3.11-slim

# Imposta la working directory nel container
WORKDIR /app

# Copia solo requirements.txt all'inizio, per sfruttare la cache Docker
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia tutto tranne venv e gli script .sh
COPY . .

# Aggiungi un .dockerignore per escludere venv/ e *.sh

# Esponi la porta
EXPOSE 3333

# Comando di avvio, da personalizzare secondo la tua app
CMD ["python", "main.py"]
