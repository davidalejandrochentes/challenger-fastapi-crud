#!/bin/bash

# Ejecutar las migraciones de Alembic
alembic upgrade head

# Iniciar la aplicación con Uvicorn
exec uvicorn main:app --host 0.0.0.0 --port 8000
