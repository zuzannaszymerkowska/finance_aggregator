# Używamy lekkiego obrazu Pythona
FROM python:3.11-slim

# Ustawienia środowiskowe
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Katalog roboczy
WORKDIR /app

# Instalacja zależności systemowych (potrzebne dla psycopg2 i innych)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalacja zależności Pythona
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie reszty projektu
COPY . .

# Nadanie uprawnień skryptowi build.sh
RUN chmod +x build.sh

# Port, na którym działa Django
EXPOSE 8000

# Komenda startowa
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]