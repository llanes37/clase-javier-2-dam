# Flask Didactico (Avanzado) - MVC ligero con Blueprints

Version mas completa del proyecto didactico: app factory, blueprints, servicios y modelos simples.

## 1) Estructura
- `app.py` -> entrada; crea la app con `create_app()`.
- `proyecto_avanzado/__init__.py` -> app factory, registro de blueprints, hook de logs.
- `config.py` -> configs Dev/Prod.
- `models.py` -> dataclass Item + datos de ejemplo.
- `controllers/items.py` -> servicio CRUD en memoria.
- `routes/web.py` -> vistas HTML (home, detalle, about, crear).
- `routes/api.py` -> API JSON (listar, detalle, crear, actualizar stock).
- `templates/` -> plantillas base, index, detalle_item, about.

## 2) Instalacion rapida
```bash
cd "cursos/Curso Python/flask_proyecto_didactico (avanzado)"
python -m venv env
.\env\Scripts\activate
pip install flask
python app.py
```
Abre: http://127.0.0.1:5000/

## 3) Rutas web
- `/` : lista de items + formulario rapido de creacion.
- `/item/<id>` : detalle de item.
- `/about` : notas de arquitectura y practicas sugeridas.
- `/crear` (POST) : crea item simple.

## 4) API JSON
- `GET /api/items` : lista.
- `GET /api/items/<id>` : detalle.
- `POST /api/items` : crea item con JSON `{nombre, precio, stock}`.
- `PATCH /api/items/<id>/stock` : actualiza stock `{stock: n}`.

## 5) Ejercicios de ampliacion
- Cambia el servicio a SQLite o SQLAlchemy.
- Agrega validaciones y mensajes flash en web.
- Implementa autenticacion basica para la API (header X-API-Key).
- Escribe tests con `pytest` para la API.
- Anade paginacion y filtros en `/api/items`.

## 6) SQLite opcional (pasos)
- Archivo: `controllers/items_sqlite.py` (servicio alternativo con CRUD en SQLite).
- Para activarlo:
  1. Ejecuta `python -c "from proyecto_avanzado.controllers.items_sqlite import init_db; init_db()"`.
  2. En `routes/web.py` y `routes/api.py`, importa `sqlite_items_service` y úsalo en lugar de `items_service`.
  3. Reinicia la app y prueba el flujo (datos persistirán en `proyecto_avanzado/instance/items.db`).
- Mantuvimos la API del servicio similar para que cambiar sea simple.

## 7) Tips
- Ajusta `ProdConfig` si despliegas (DEBUG False, SECRET_KEY real).
- Usa `flask --app app run` si prefieres CLI.
- Revisa los comentarios `# ! # * # ? TODO` en cada modulo para guiarte.
