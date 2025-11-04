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

### Requerimiento 2: Soft Delete y Mixins

- [x] **Implementación de Soft Delete:** Los modelos heredan de un `SoftDeleteMixin` que añade el campo `deleted_at`.
- [x] **Mixin Reutilizable:** Se ha creado un mixin para el comportamiento de soft delete.
- [x] **Query Personalizada:** Se ha implementado un listener de eventos de SQLAlchemy que filtra automáticamente los elementos eliminados en todas las consultas ORM.

### Requerimiento 3: Timestamps Genéricos

- [x] **Campos de Timestamp:** Todos los modelos incluyen los campos `created_at` y `updated_at`.
- [x] **Mixin de Timestamp:** Estos campos se gestionan de manera genérica a través de un `TimestampMixin` reutilizable.