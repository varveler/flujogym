# FlujoGym - Sistema de Gestión de Rutinas de Ejercicio

Herramienta para que los usuarios puedan registrar y gestionar sus rutinas de ejercicio. Desarrollada con Django, Django Rest Framework, y desplegada usando Docker. Implementa autenticación JWT para seguridad de la API.

## Tecnologías Utilizadas

- Django 5.1
- Django Rest Framework
- PostgreSQL
- Docker & Docker Compose
- Simple JWT
- Nginx (servidor web)
- Gunicorn (servidor WSGI)
- RabbitMQ & Celery (para tareas asíncronas)
- 

## Características

- Gestión de usuarios y autenticación JWT
- CRUD completo de ejercicios y rutinas
- Programación de rutinas por día y hora
- API REST
- Contenedores Docker para fácil despliegue
- Procesamiento asíncrono con Celery (futura implementación de tareas)

## Requisitos
- Docker y Docker Compose

## Instalación y Despliegue

1. Clonar el repositorio:
```bash
git clone git@github.com:varveler/flujogym.git
cd flujogym
```

2. Construir y levantar los contenedores:
```bash
docker-compose up --build
```

3. Acceder al admin de Django:

- URL: http://localhost/admin/
- Usuario: sebastian
- Contraseña: flujogym

## Ejemplos de Uso de la API

A continuación, se muestra un ejemplo completo de cómo usar la API para crear y programar una rutina de ejercicios.





### 1. Obtener Token JWT

```bash
curl -X POST http://localhost/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "sebastian",
    "password": "flujogym"
  }'
```

La respuesta incluirá tu token de acceso:
```json
{
    "access": "OiJKV1QiLC...",
    "refresh": "ejdsKV1QiLC..."
}
```

### 2. Crear una Nueva Rutina

**Nota**: Reemplaza `TU_TOKEN_AQUI` con el **access** token JWT que se obtiene en el paso 1. 


```bash
curl -X POST http://localhost/api/rutinas/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Rutina de Piernas",
    "descripcion": "Rutina enfocada en piernas y glúteos",
    "nivel_dificultad": "intermedio",
    "duracion_estimada": 45
  }'
```

### 3. Agregar Ejercicios a la Rutina

**Nota**: Reemplaza `TU_TOKEN_AQUI` con el **access** token JWT que se obtiene en el paso 1. 


```bash
# Agregar primer ejercicio (sentadillas)
curl -X POST http://localhost/api/ejercicios-en-rutina/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "rutina": 2,
    "ejercicio": 1,
    "orden": 1,
    "series": 4,
    "repeticiones": "12",
    "descanso": 90
  }'

# Agregar segundo ejercicio (peso muerto)
curl -X POST http://localhost/api/ejercicios-en-rutina/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "rutina": 2,
    "ejercicio": 2,
    "orden": 2,
    "series": 3,
    "repeticiones": "10",
    "descanso": 120
  }'
```

### 4. Programar la Rutina

**Nota**: Reemplaza `TU_TOKEN_AQUI` con el **access** token JWT que se obtiene en el paso 1. 


```bash
# Programar para martes
curl -X POST http://localhost/api/programaciones/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "rutina": 2,
    "dia_semana": "MAR",
    "hora": "19:00:00",
    "activa": true
  }'

# Programar para jueves
curl -X POST http://localhost/api/programaciones/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "rutina": 2,
    "dia_semana": "JUE",
    "hora": "19:00:00",
    "activa": true
  }'
```

### 5. Verificar las Creaciones

**Nota**: Reemplaza `TU_TOKEN_AQUI` con el **access** token JWT que se obtiene en el paso 1. 

```bash
# Ver todas las rutinas
curl -X GET http://localhost/api/rutinas/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI"

# Ver todas las programaciones
curl -X GET http://localhost/api/programaciones/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```






## Estructura del Proyecto

```
flujogym/
│
├── docker/
│   ├── nginx
│   │    ├── conf/default.conf
│   │    └── Dockerfile
│   ├── db/.env
│   └── rabbitmq/.env
│
├── flujogym/ # Proyecto Django
│   ├── flujogym
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── celery.py
│   │   └── wsgi.py
│   ├── usuarios/
│   └── rutinas/
│
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## API Endpoints

### Autenticación
- `POST /api/token/` - Obtener token JWT
- `POST /api/token/refresh/` - Refrescar token JWT
- `POST /api/token/verify/` - Verificar token JWT

### Usuarios
- `GET /api/usuarios/` - Listar usuarios
- `POST /api/usuarios/` - Crear usuario
- `GET /api/usuarios/{id}/` - Detalle de usuario

### Rutinas
- `GET /api/rutinas/` - Listar rutinas
- `POST /api/rutinas/` - Crear rutina
- `GET /api/rutinas/{id}/` - Detalle de rutina
- `PUT /api/rutinas/{id}/` - Actualizar rutina
- `DELETE /api/rutinas/{id}/` - Eliminar rutina

### Ejercicios
- `GET /api/ejercicios/` - Listar ejercicios
- `POST /api/ejercicios/` - Crear ejercicio
- `GET /api/ejercicios/{id}/` - Detalle de ejercicio

### Programaciones
- `GET /api/programaciones/` - Listar programaciones
- `POST /api/programaciones/` - Crear programación

## Modelos de Datos

### Usuario
- username
- email
- fecha_nacimiento
- fecha_inscripcion
- activo

### Ejercicio
- nombre
- descripcion
- grupo_muscular
- equipamiento_necesario

### Rutina
- nombre
- descripcion
- nivel_dificultad
- duracion_estimada
- creada_por
- fecha_creacion

### ProgramacionRutina
- usuario
- rutina
- dia_semana
- hora
- activa

