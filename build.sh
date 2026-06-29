#!/usr/bin/env bash
# Script de build para Render (entorno Python nativo).
set -o errexit

pip install -r requirements.txt

# Reúne los estáticos (incluye el output.css de Tailwind ya compilado).
python manage.py collectstatic --no-input

# Aplica migraciones en la base de datos gestionada de Render.
python manage.py migrate

# Crea el superusuario desde variables de entorno si aún no existe (idempotente).
python manage.py ensure_superuser
