# Usa una versione leggera di Python
FROM python:3.11

# Copia lo script di entrypoint dentro il container
COPY entrypoint.sh /app/entrypoint.sh

# Rendi lo script eseguibile
RUN chmod +x /app/entrypoint.sh

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file dei requisiti e installa le dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice del progetto
COPY . .

# Espone la porta per il server Django
EXPOSE 8000

# Usa lo script come entrypoint
CMD ["sh", "/app/entrypoint.sh"]




# Comando di avvio del server Django
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "table_tomic.wsgi:application"]