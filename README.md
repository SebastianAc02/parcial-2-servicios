[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/P4r71VR8)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23781168&assignment_repo_type=AssignmentRepo)

# Parcial 2 - REST API con Microservicios

API REST para gestión de notas personales con integración a jsonplaceholder. Implementada con arquitectura de microservicios usando Flask, SQLAlchemy y Docker.

## Arquitectura

El proyecto está dividido en dos microservicios independientes:

- **notes-service** (puerto 5001): CRUD de notas con SQLite
- **external-service** (puerto 5002): proxy a jsonplaceholder.typicode.com
- **gateway** (nginx, puerto 5000): enruta las peticiones a cada servicio

Cada servicio sigue la arquitectura en capas: Routes → Services → Repositories → Models.

## Cómo correr

### Con Docker (recomendado)

```bash
docker compose up --build
```

La API queda disponible en `http://localhost:5000`.

### Sin Docker

```bash
# notes-service
cd notes-service
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask run --port 5001

# external-service (en otra terminal)
cd external-service
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask run --port 5002
```

## Endpoints

### Notas
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /notes | Listar notas (filtro: `?completed=true\|false`) |
| GET | /notes/{id} | Obtener nota por ID |
| POST | /notes | Crear nota |
| PUT | /notes/{id} | Actualizar nota |
| DELETE | /notes/{id} | Eliminar nota |

### Externos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /external/users | Usuarios de jsonplaceholder |
| GET | /external/posts | Posts de jsonplaceholder |
| GET | /external/posts/{userId} | Posts por usuario |

## Tests

```bash
# notes-service
cd notes-service && pytest --cov=app -v

# external-service
cd external-service && pytest --cov=app -v
```

Coverage actual: **97%** (notes-service) y **100%** (external-service).
