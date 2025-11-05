# Challenge: API de Recetas con FastAPI

Este proyecto es una API RESTful desarrollada con FastAPI, SQLAlchemy (asíncrono) y Pydantic v2 para gestionar usuarios, recetas, ingredientes y reseñas. La aplicación cumple con una serie de requerimientos técnicos que demuestran buenas prácticas en el desarrollo de APIs modernas.

---

## ✅ Características Principales

### 1. Configuración Inicial y Modelado
- **API con Entidades y Relaciones:** Se ha creado una API con una entidad principal (`User`) y entidades secundarias (`Recipe`, `Review`, `Ingredient`).
- **Relaciones 1:N y N:M:**
    - **Uno a muchos (1:N):** `User` <-> `Recipe` y `User`/`Recipe` <-> `Review`.
    - **Muchos a muchos (N:M):** `Recipe` <-> `Ingredient`.
- **Migraciones con Alembic:** Se utiliza Alembic para gestionar la evolución del esquema de la base de datos de manera incremental.
- **Operaciones Asíncronas:** Todas las operaciones de base de datos se realizan de forma asíncrona utilizando `asyncpg` y `SQLAlchemy`.

### 2. Soft Delete y Mixins
- **Implementación de Soft Delete:** Las entidades no se eliminan físicamente. En su lugar, se marcan como eliminadas a través de un campo `deleted_at`.
- **Mixin Reutilizable:** El comportamiento de `soft-delete` se implementa a través de un `SoftDeleteMixin` para ser reutilizado en diferentes modelos.
- **Query Personalizada:** Un listener de eventos de SQLAlchemy filtra automáticamente los elementos eliminados en todas las consultas, a menos que se indique explícitamente lo contrario.

### 3. Timestamps Genéricos
- **Campos de Timestamp:** Todos los modelos incluyen campos `created_at` y `updated_at`, gestionados a través de un `TimestampMixin` reutilizable.

### 4. Protección de Endpoints
- **Autenticación con JWT:** Se utiliza OAuth2 con JSON Web Tokens (JWT) para proteger los endpoints de creación, modificación y eliminación.
- **Endpoints de Autenticación:** Se incluyen endpoints para el registro (`/auth/register`) y el login (`/auth/login`).

### 5. Routers y Middleware
- **Lógica Separada en Routers:** La lógica de la API está organizada por entidad en módulos de routers (`users.py`, `recipes.py`, etc.).
- **Middleware Personalizado:** Se ha implementado un middleware para registrar el tiempo de procesamiento de cada solicitud.

---

## 🚀 Cómo Empezar

### Prerrequisitos
- Python 3.11+
- Docker (opcional, para despliegue)
- Una base de datos PostgreSQL en ejecución.

### 1. Configuración del Entorno Local
1.  **Clonar el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd challenger-fastapi-crud
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar las variables de entorno:**
    Crea un archivo `.env` en la raíz del proyecto a partir del archivo `.env.example` (si existiera) o créalo desde cero con las siguientes variables:
    ```env
    DB_NAME=nombre_de_tu_bd
    DB_USER=usuario_de_tu_bd
    DB_PASSWORD=contraseña_de_tu_bd
    DB_HOST=localhost
    DB_PORT=5432

    SECRET_KEY=tu_clave_secreta_muy_segura
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5.  **Ejecutar las migraciones:**
    Asegúrate de que tu base de datos PostgreSQL esté en funcionamiento y luego ejecuta:
    ```bash
    alembic upgrade head
    ```

6.  **Iniciar la aplicación:**
    ```bash
    uvicorn main:app --reload
    ```
    La API estará disponible en `http://127.0.0.1:8000` y la documentación interactiva en `http://127.0.0.1:8000/docs`.

### 2. Despliegue con Docker
1.  **Construir la imagen de Docker:**
    ```bash
    docker build -t fastapi-recipe-api .
    ```

2.  **Ejecutar el contenedor:**
    Asegúrate de pasar las variables de entorno necesarias.
    ```bash
    docker run -p 8000:8000 --env-file .env fastapi-recipe-api
    ```
    El contenedor ejecutará las migraciones automáticamente al iniciar y luego lanzará la aplicación.

---

## Endpoints de la API

La API está organizada en los siguientes routers:

-   `/auth`: Registro y login de usuarios.
-   `/users`: Operaciones CRUD para usuarios, incluyendo la gestión del perfil del usuario autenticado.
-   `/recipes`: Operaciones CRUD completas para recetas, incluyendo la gestión de sus ingredientes.
-   `/ingredients`: Operaciones CRUD para los ingredientes.
-   `/reviews`: Operaciones CRUD para las reseñas de las recetas.

Para más detalles sobre cada endpoint, consulta la documentación interactiva en `/docs`.
