# Proyecto Flask Didactico (paso a paso)

Guia completa para entender y extender una mini app Flask con rutas, formularios, JSON y manejo de errores. Pensada para practicas guiadas y para que el alumno agregue sus propias mejoras.

## 1) Objetivo del proyecto
- Ver en un solo lugar: rutas, formularios POST, query strings GET, APIs JSON, errores y hooks.
- Usar comentarios tipo "Better Comments" (# !, # *, # ?, TODO) para leer el flujo rapido.
- Servir como base para ejercicios crecientes (basico -> intermedio -> avanzado).

## 2) Requisitos y stack
- Python 3.10+ y pip.
- Dependencias: `flask` (y opcionalmente `gunicorn` para despliegue).
- Estructura simple en un solo folder (sin bases de datos ni archivos estaticos adicionales).

## 3) Estructura de archivos
- `app.py` : Logica Flask y rutas comentadas.
- `templates/base.html` : Layout con navbar y bloque `{% block content %}`.
- `templates/index.html` : Ejemplos (formulario POST, rutas con parametros, query strings, API).
- `templates/resultado.html` : Respuesta del formulario POST.
- `templates/about.html` : Explica la app y proximos pasos.

## 4) Puesta en marcha rapida
```bash
cd "cursos/Curso Python/flask_proyecto_didactico"
python -m venv env
.\env\Scripts\activate   # Windows
pip install flask
python app.py
```
Abre en el navegador: http://127.0.0.1:5000/

## 5) Flujo simplificado
1. Usuario visita `/` y ve ejemplos.
2. Envia formulario a `/procesar` (POST) -> valida -> renderiza `resultado.html`.
3. En APIs JSON, el cliente manda datos -> validacion -> respuesta JSON con codigo HTTP.
4. Hooks `before_request` y `after_request` se ejecutan en cada peticion (logs y cabeceras).

## 6) Rutas web principales
- `/` : Home con formulario y enlaces de practica.
- `/about` : Explica la estructura de la app.
- `/procesar` (POST) : Recibe nombre, valida y responde.
- `/saluda/<nombre>` : Parametro en la URL.
- `/suma/<int:a>/<int:b>` : Parametros tipados (int).
- `/buscar?q=valor&page=n` : Lee query strings y devuelve JSON.

## 7) Endpoints de API JSON
- `GET /api/echo?q=hola` : Devuelve lo que recibas por `q`.
- `POST /api/saludo` con JSON `{"nombre": "Ada"}` : Saludo personalizado (400 si falta nombre).
- `GET /api/health` : Health check.
- `GET /api/calculadora/<operacion>/<int:a>/<int:b>` : suma, resta, multiply, divide (400 si operacion invalida o division por cero).

## 8) Manejo de errores y hooks
- 404 y 500 devuelven JSON con mensaje y status.
- `before_request`: imprime logs (editable para medir tiempos).
- `after_request`: agrega cabeceras de ejemplo (`X-Ejemplo`, `X-Author`).

## 9) Ejercicios para alumnos
### Basico
1) Cambia el formulario para pedir email y edad; valida que email no este vacio y edad sea numero > 0.
2) En `/buscar`, agrega parametro opcional `lang` y devuelvelo en el JSON.
3) En `/api/echo`, agrega la hora del servidor en la respuesta.

### Intermedio
4) Mide tiempo de respuesta: guarda `datetime.now()` en `before_request` y calcula en `after_request`; agrega cabecera `X-Response-Time`.
5) Crea `/api/carrito`:
   - GET: devuelve lista en memoria.
   - POST: recibe `{nombre, precio, cantidad}`, valida `precio > 0` y `cantidad >= 1`, devuelve total acumulado.
6) Protege una ruta con una clave simple en headers (ej: `X-API-Key`); si falta, responde 401.

### Avanzado
7) Integra SQLite:
   - Crea tabla `visitas` (id, nombre, creado_en).
   - En `/procesar`, inserta el nombre y muestra el total de visitas.
8) Anade tests con `pytest` para `/api/echo`, `/api/saludo` y `/api/calculadora`.
9) Prepara despliegue:
   - Genera `requirements.txt`.
   - Agrega comando `gunicorn app:app`.
   - Crea configuracion simple para Render/Fly.io/PythonAnywhere.

## 10) Tips de depuracion
- Activa/desactiva `DEBUG_MODE` en `app.py` para controlar el debugger.
- Usa prints en `before_request` para ver metodo y ruta.
- Revisa respuestas JSON con DevTools -> pestana Network.

## 11) Checklist antes de entregar practica
- [ ] Formulario valida datos y los muestra sin errores.
- [ ] Rutas con parametros funcionan con enteros y strings.
- [ ] Endpoints API devuelven codigos correctos (200/400) y JSON valido.
- [ ] Manejadores 404/500 responden en JSON.
- [ ] README actualizado con los cambios nuevos.

## 12) Preguntas de repaso (auto-evaluacion)
1) Que diferencia hay entre parametros de ruta y query strings?
2) Cuando devolverias 400 vs 500 en una API?
3) Donde agregarias cabeceras personalizadas y por que?
4) Como probarias un POST JSON sin interfaz grafica?
5) Que cambiarias para pasar de desarrollo a produccion?

## 13) Ideas de ampliacion
- Anadir CORS en `after_request` para consumir la API desde otra web.
- Usar Blueprints si el proyecto crece.
- Integrar autentificacion con tokens JWT simples.
- Agregar un mini front en JS que consuma `/api/carrito`.
