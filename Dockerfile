# Używamy lekkiego obrazu Pythona
FROM python:3.11-slim

# Ustawiamy zmienne środowiskowe, żeby Python nie tworzył plików .pyc i nie buforował wyjścia
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Katalog roboczy
WORKDIR /app

# Instalacja zależności systemowych dla PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalacja bibliotek Pythona
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie reszty kodu
COPY . /app/

# Komenda startowa
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]