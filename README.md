# Challenge FastAPI - Backend

### Requerimiento 1: Configuración Inicial y Modelado

- [x] **API con Entidades y Relaciones:** Se ha creado la estructura de la API con una entidad principal (`User`) y entidades secundarias (`Recipe`, `Review`, `Ingredient`).
- [x] **Relaciones 1:N y N:M:**
    - Se han implementado las relaciones **uno a muchos** (1:N) entre `User` <-> `Recipe` y `User`/`Recipe` <-> `Review`.
    - Se ha implementado la relación **muchos a muchos** (N:M) entre `Recipe` <-> `Ingredient`.
- [x] **Migraciones Evolutivas con Alembic:**
    - Se generó una migración inicial para las tablas base.
    - Se generó una segunda migración para añadir la relación N:M, demostrando un flujo de trabajo evolutivo.
- [x] **Operaciones Asíncronas:** El proyecto está configurado para utilizar operaciones de base de datos asíncronas con SQLAlchemy y `asyncpg`.
