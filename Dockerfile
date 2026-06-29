FROM python:3.13-slim

# Evita .pyc y fuerza salida sin buffer (logs en tiempo real)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema (psycopg[binary] trae libpq, esto cubre compilaciones extra)
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 curl gettext \
    && rm -rf /var/lib/apt/lists/*

# Tailwind CSS CLI standalone (sin necesidad de Node)
RUN curl -fsSL -o /usr/local/bin/tailwindcss \
        https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64 \
    && chmod +x /usr/local/bin/tailwindcss

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
