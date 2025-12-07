# =========================================================================================
#  🌐 FLASK TUTORIAL EN UN SOLO ARCHIVO — Versión didáctica y comentada
#  ────────────────────────────────────────────────────────────────────────────────────────
#  📘 En esta clase practicarás:
#    * Crear una aplicación Flask (inicialización y configuración)
#    * Rutas básicas (@app.route) y rutas con parámetros
#    * Métodos HTTP (GET, POST) y lectura de datos
#    * Plantillas Jinja2 inline (render_template_string) con herencia (extends)
#    * Formularios HTML (POST) y query strings (GET)
#    * API JSON: endpoints que envían/reciben JSON con códigos de estado HTTP
#    * Manejo de errores (404, 500) y hooks (before_request, after_request)
#    * Prácticas guiadas con TODO y laboratorio IA
#
#  🎯 Requisitos previos:
#    - Python 3.8+
#    - Flask (pip install flask)
#    - Conocimiento de HTTP GET/POST y JSON básico
#
#  📋 CÓMO USAR (Windows):
#    1) Crear entorno:  python -m venv env
#    2) Activar:        .\env\Scripts\activate
#    3) Instalar:       pip install flask
#    4) Ejecutar:       python "cursos/Curso Python/14_flask_tutorial.py"
#    5) Navegar:        http://127.0.0.1:5000/
#    6) Ver logs en terminal: muestra GET/POST, códigos de estado, tiempos
#
#  🎨 Better Comments:
#    # ! importante   ·  # * definición/foco   ·  # ? idea/nota
#    # TODO: práctica  ·  # NOTE: apunte útil   ·  # // deprecado
#
#  💡 Consejo: Lee el archivo de arriba a abajo. Cada sección está comentada paso a paso.
#     Prueba los enlaces en http://127.0.0.1:5000/ y abre DevTools (F12) para ver peticiones.
# =========================================================================================

from __future__ import annotations

from typing import Any, Dict, Callable

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template_string,
    request,
    url_for,
)

# =========================================================================================
#  * CONFIGURACIÓN GLOBAL (para desarrolladores)
# =========================================================================================
DEBUG_MODE = True           # ! Activa recarga automática y página de errores interactiva
ECHO_LOGS = True            # Imprime logs en terminal de cada petición
PAUSE_ON_DEMO = False       # True: pausa tras cada demostración (opcional)



# =========================================================================================
#  SECCIÓN 1 · Inicialización de la aplicación Flask
# =========================================================================================
# ? ¿Qué es Flask?
#   - Un framework web ligero y flexible de Python.
#   - Permite crear rutas (URLs), recibir datos, procesar lógica y devolver respuestas.
#
# * Crear la aplicación:
#   - Flask(__name__): crea instancia; __name__ ayuda a encontrar recursos.
#   - app.config: diccionario de configuración (debug, secreto, etc.).
app = Flask(__name__)

# ! Configuraciones útiles en desarrollo
app.config.update(
    JSON_AS_ASCII=False,         # * Permite acentos en JSON (sin escapar)
    TEMPLATES_AUTO_RELOAD=True,  # * Recarga plantillas si cambian (debug)
)



# =========================================================================================
#  SECCIÓN 2 · Plantillas Jinja2 "inline" (guardadas en variables)
# =========================================================================================
# ? ¿Por qué inline?
#   - En producción, las plantillas están en archivos en carpeta templates/.
#   - Aquí usamos DictLoader para simplificar: todo en UN ARCHIVO.
#   - Ideal para aprendizaje rápido.
#
# * Jinja2: motor de plantillas con:
#   - {{ variable }}: imprime valor
#   - {% if ... %}: condicionales
#   - {% extends %}: herencia de plantillas
#   - {% block ... %}: bloques reemplazables
#
# ! BASE_HTML: plantilla base con navbar, estructura común
# * INDEX_HTML: página principal (extiende BASE_HTML)
# * RESULTADO_HTML: resultado tras procesar formulario
# * ABOUT_HTML: página informativa

# ? BASE_HTML: estructura común a todas las páginas
BASE_HTML = """<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ title or 'Flask Tutorial' }}</title>
    <!-- ! Bootstrap 5: librería CSS para diseño rápido -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body { font-family: 'Segoe UI', sans-serif; }
      .code-block { background: #f5f5f5; padding: 10px; border-radius: 5px; font-family: monospace; }
      .section-title { color: #0d6efd; font-weight: bold; margin-top: 20px; }
    </style>
  </head>
  <body class="bg-light">
    <!-- ! Barra de navegación con enlaces a rutas principales -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
      <div class="container">
        <a class="navbar-brand" href="{{ url_for('inicio') }}">
          🌐 Flask Tutorial
        </a>
        <div class="navbar-nav">
          <a class="nav-link" href="{{ url_for('inicio') }}">Inicio</a>
          <a class="nav-link" href="{{ url_for('about') }}">Acerca de</a>
          <a class="nav-link" href="{{ url_for('api_health') }}">Estado API</a>
        </div>
      </div>
    </nav>
    <main class="container">
      {% block content %}{% endblock %}
    </main>
    <footer class="mt-5 py-3 text-center text-muted border-top">
      <small>Flask Tutorial — Didáctico • Autor: Joaquín • https://clasesonlinejoaquin.es/</small>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>"""

# ? INDEX_HTML: página principal con todos los ejemplos
INDEX_HTML = """{% extends 'base.html' %}{% block content %}
  <div class="row mb-4">
    <div class="col-md-8">
      <div class="card shadow-sm">
        <div class="card-body">
          <h1 class="h3 mb-3">🚀 Bienvenido a Flask</h1>
          <p class="lead">Esta es tu primera aplicación web. Aquí practicarás:</p>
          <ul>
            <li>Rutas y parámetros</li>
            <li>Formularios (POST)</li>
            <li>API JSON</li>
            <li>Manejo de errores</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card bg-info text-white">
        <div class="card-body">
          <h5 class="card-title">💡 Consejo</h5>
          <p class="card-text small">Abre DevTools (F12) y ve la pestaña Network. Verás cada petición que hace tu navegador.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- ! SECCIÓN 1: FORMULARIO HTML (POST) -->
  <div class="card shadow-sm mb-4">
    <div class="card-header bg-primary text-white">
      <h5 class="mb-0">1️⃣ Formulario (POST)</h5>
    </div>
    <div class="card-body">
      <p class="text-muted small">📝 Método POST: envía datos al servidor de forma segura (sin mostrar en URL).</p>
      <form action="{{ url_for('procesar') }}" method="post" class="row gy-2">
        <div class="col-12 col-md-8">
          <label for="nombre" class="form-label">Tu nombre:</label>
          <input type="text" id="nombre" name="nombre" class="form-control" 
                 placeholder="Escribe tu nombre aquí" required>
        </div>
        <div class="col-12 col-md-4 d-flex align-items-end">
          <button type="submit" class="btn btn-primary w-100">✉️ Enviar</button>
        </div>
      </form>
      <div class="code-block mt-2 small">
        <code>&lt;form action="/procesar" method="post"&gt;</code><br>
        <code>  &lt;input name="nombre" ...&gt;</code><br>
        <code>&lt;/form&gt;</code>
      </div>
    </div>
  </div>

  <!-- ! SECCIÓN 2: RUTAS CON PARÁMETROS -->
  <div class="card shadow-sm mb-4">
    <div class="card-header bg-success text-white">
      <h5 class="mb-0">2️⃣ Rutas con parámetros (/ruta/valor)</h5>
    </div>
    <div class="card-body">
      <p class="text-muted small">📍 Los parámetros van en la URL. Haz clic en los enlaces:</p>
      <ul class="list-group">
        <li class="list-group-item">
          <a href="{{ url_for('saluda', nombre='Joaquín') }}">/saluda/Joaquín</a>
          <small class="text-muted d-block">Parámetro: nombre (string)</small>
        </li>
        <li class="list-group-item">
          <a href="{{ url_for('saluda', nombre='Python') }}">/saluda/Python</a>
          <small class="text-muted d-block">Prueba con otro valor</small>
        </li>
        <li class="list-group-item">
          <a href="{{ url_for('suma', a=3, b=5) }}">/suma/3/5</a>
          <small class="text-muted d-block">Parámetros tipados: int (3) + int (5)</small>
        </li>
        <li class="list-group-item">
          <a href="{{ url_for('suma', a=10, b=20) }}">/suma/10/20</a>
          <small class="text-muted d-block">Otro ejemplo: 10 + 20</small>
        </li>
      </ul>
      <div class="code-block mt-3 small">
        <code>@app.route("/saluda/&lt;nombre&gt;")</code><br>
        <code>def saluda(nombre: str): ...</code>
      </div>
    </div>
  </div>

  <!-- ! SECCIÓN 3: QUERY STRINGS (GET) -->
  <div class="card shadow-sm mb-4">
    <div class="card-header bg-warning text-dark">
      <h5 class="mb-0">3️⃣ Query Strings (?param=valor)</h5>
    </div>
    <div class="card-body">
      <p class="text-muted small">🔍 Los parámetros van DESPUÉS del ? sin cambiar la ruta.</p>
      <ul class="list-group">
        <li class="list-group-item">
          <a href="{{ url_for('buscar') }}?q=flask&page=1">/buscar?q=flask&page=1</a>
          <small class="text-muted d-block">Búsqueda: flask, página: 1</small>
        </li>
        <li class="list-group-item">
          <a href="{{ url_for('buscar') }}?q=python&page=2">/buscar?q=python&page=2</a>
          <small class="text-muted d-block">Búsqueda: python, página: 2</small>
        </li>
      </ul>
      <div class="code-block mt-3 small">
        <code>q = request.args.get("q", "")</code><br>
        <code>page = request.args.get("page", 1)</code>
      </div>
    </div>
  </div>

  <!-- ! SECCIÓN 4: API JSON -->
  <div class="card shadow-sm mb-4">
    <div class="card-header bg-danger text-white">
      <h5 class="mb-0">4️⃣ API JSON (GET/POST)</h5>
    </div>
    <div class="card-body">
      <p class="text-muted small">🔗 Endpoints que devuelven JSON (formato de datos ligero).</p>
      <ul class="list-group">
        <li class="list-group-item">
          <code>GET</code> <a href="{{ url_for('api_echo') }}?q=hola">/api/echo?q=hola</a>
          <small class="text-muted d-block">Devuelve: {"ok": true, "echo": "hola"}</small>
        </li>
        <li class="list-group-item">
          <code>GET</code> <a href="{{ url_for('api_health') }}">/api/health</a>
          <small class="text-muted d-block">Estado de la API: {"status": "ok"}</small>
        </li>
        <li class="list-group-item">
          <code>POST</code> /api/saludo
          <small class="text-muted d-block">
            Abre DevTools → Network → haz POST con JSON: {"nombre": "Ada"}
          </small>
        </li>
      </ul>
      <div class="code-block mt-3 small">
        <code>return jsonify(ok=True, echo=q)</code>
      </div>
    </div>
  </div>

  <!-- ! SECCIÓN 5: MANEJO DE ERRORES -->
  <div class="card shadow-sm mb-4">
    <div class="card-header bg-secondary text-white">
      <h5 class="mb-0">5️⃣ Manejo de errores (HTTP 404, 500)</h5>
    </div>
    <div class="card-body">
      <p class="text-muted small">⚠️ Prueba a acceder a rutas que no existen o que generan errores:</p>
      <ul class="list-group">
        <li class="list-group-item">
          <a href="/ruta-que-no-existe">❌ 404 — No encontrado</a>
          <small class="text-muted d-block">La ruta no existe en la app</small>
        </li>
        <li class="list-group-item">
          <a href="{{ url_for('error_intencional') }}">⚡ 500 — Error intencional</a>
          <small class="text-muted d-block">Provoca un error controlado</small>
        </li>
      </ul>
    </div>
  </div>

  <!-- ! SECCIÓN 6: REFERENCIAS Y RECURSOS -->
  <div class="card shadow-sm">
    <div class="card-header bg-light">
      <h5 class="mb-0">📚 Recursos</h5>
    </div>
    <div class="card-body">
      <ul class="small">
        <li><strong>Flask:</strong> https://flask.palletsprojects.com/</li>
        <li><strong>Jinja2:</strong> https://jinja.palletsprojects.com/</li>
        <li><strong>HTTP:</strong> GET, POST, códigos de estado (200, 404, 500...)</li>
        <li><strong>JSON:</strong> {"clave": "valor"} — formato estándar en web</li>
      </ul>
    </div>
  </div>
{% endblock %}"""

# ? RESULTADO_HTML: se muestra tras procesar el formulario
RESULTADO_HTML = """{% extends 'base.html' %}{% block content %}
  <div class="card shadow-sm">
    <div class="card-body">
      <div class="alert alert-success" role="alert">
        <h4 class="alert-heading">✅ ¡Enviado correctamente!</h4>
        <p>Hola, <strong>{{ nombre }}</strong>!</p>
        <hr>
        <p class="mb-0">Tu formulario se procesó por POST. El servidor recibió el nombre y devolvió esta página.</p>
      </div>
      <a href="{{ url_for('inicio') }}" class="btn btn-outline-primary">← Volver al inicio</a>
    </div>
  </div>
{% endblock %}"""

# ? ABOUT_HTML: información sobre la app
ABOUT_HTML = """{% extends 'base.html' %}{% block content %}
  <div class="card shadow-sm">
    <div class="card-header bg-light">
      <h3 class="mb-0">ℹ️ Acerca de esta aplicación</h3>
    </div>
    <div class="card-body">
      <h5 class="mt-3">🎯 Objetivo:</h5>
      <p>Aprender Flask desde cero mediante ejemplos prácticos en un <strong>único archivo</strong>.</p>

      <h5 class="mt-3">✨ Características:</h5>
      <ul>
        <li><strong>Plantillas Jinja2 inline:</strong> Guardadas en variables, no en archivos físicos.</li>
        <li><strong>DictLoader:</strong> Simula que las plantillas son archivos reales.</li>
        <li><strong>Rutas con parámetros:</strong> Tipado automático (int, str, float).</li>
        <li><strong>Formularios POST:</strong> request.form para recibir datos.</li>
        <li><strong>Query strings GET:</strong> request.args para parámetros en URL.</li>
        <li><strong>API JSON:</strong> endpoints que devuelven JSON con códigos HTTP.</li>
        <li><strong>Manejadores de errores:</strong> @app.errorhandler(404), (500).</li>
        <li><strong>Hooks (before/after):</strong> Se ejecutan antes/después de cada petición.</li>
      </ul>

      <h5 class="mt-3">📂 Estructura de código:</h5>
      <div class="code-block small">
        1. Inicialización de la app<br>
        2. Plantillas Jinja2<br>
        3. Rutas (endpoints)<br>
        4. Mini API JSON<br>
        5. Manejo de errores<br>
        6. Punto de entrada (if __name__ == "__main__")
      </div>

      <h5 class="mt-3">💡 Próximos pasos:</h5>
      <ul>
        <li>Lee el archivo comentado paso a paso.</li>
        <li>Modifica las rutas y plantillas.</li>
        <li>Añade nuevas rutas y funciones.</li>
        <li>Conecta una base de datos SQLite o PostgreSQL.</li>
        <li>Despliega en Heroku, Render, PythonAnywhere...</li>
      </ul>
    </div>
  </div>
{% endblock %}"""

# * Registrar las plantillas en el loader de Jinja2
from jinja2 import DictLoader

app.jinja_loader = DictLoader({
    "base.html": BASE_HTML,
    "index.html": INDEX_HTML,
    "resultado.html": RESULTADO_HTML,
    "about.html": ABOUT_HTML,
})
BASE_HTML = """<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ title or 'Flask Tutorial' }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
      <div class="container">
        <a class="navbar-brand" href="{{ url_for('inicio') }}">Flask Tutorial</a>
        <div class="navbar-nav">
          <a class="nav-link" href="{{ url_for('inicio') }}">Inicio</a>
          <a class="nav-link" href="{{ url_for('about') }}">Acerca de</a>
          <a class="nav-link" href="{{ url_for('api_echo') }}?q=hola">API</a>
        </div>
      </div>
    </nav>
    <main class="container">
      {% block content %}{% endblock %}
    </main>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>"""

INDEX_HTML = """{% extends 'base.html' %}{% block content %}
  <div class="card shadow-sm">
    <div class="card-body">
      <h1 class="h4 mb-3">Bienvenido a tu primera app Flask</h1>
      <p class="text-muted">Esta página reúne enlaces para explorar rutas, formularios y API.</p>

      <h2 class="h5 mt-4">1) Formulario (POST)</h2>
      <form action="{{ url_for('procesar') }}" method="post" class="row gy-2">
        <div class="col-12 col-md-8">
          <label for="nombre" class="form-label">Nombre</label>
          <input type="text" id="nombre" name="nombre" class="form-control" placeholder="Escribe tu nombre" required>
        </div>
        <div class="col-12 col-md-4 d-flex align-items-end">
          <button type="submit" class="btn btn-primary w-100">Enviar</button>
        </div>
      </form>

      <h2 class="h5 mt-4">2) Rutas con parámetros</h2>
      <ul>
        <li><a href="{{ url_for('saluda', nombre='Joaquín') }}">/saluda/Joaquín</a></li>
        <li><a href="{{ url_for('suma', a=3, b=5) }}">/suma/3/5</a> (suma 3 + 5)</li>
      </ul>

      <h2 class="h5 mt-4">3) Query strings (GET)</h2>
      <ul>
        <li><a href="{{ url_for('buscar') }}?q=flask&page=2">/buscar?q=flask&page=2</a></li>
      </ul>

      <h2 class="h5 mt-4">4) Mini API</h2>
      <ul>
        <li><code>GET</code> <a href="{{ url_for('api_echo') }}?q=hola">/api/echo?q=hola</a></li>
        <li><code>POST</code> /api/saludo con JSON: {"nombre": "Ada"}</li>
        <li><code>GET</code> <a href="{{ url_for('api_health') }}">/api/health</a> (estado)</li>
      </ul>

      <h2 class="h5 mt-4">5) Errores</h2>
      <ul>
        <li><a href="/ruta-que-no-existe">404 — No encontrado</a></li>
        <li><a href="{{ url_for('error_intencional') }}">500 — Error intencional</a></li>
      </ul>

      <hr>
      <small class="text-muted">
        Tip: inspecciona este archivo para leer los comentarios y entender cada parte.
      </small>
    </div>
  </div>
{% endblock %}"""

RESULTADO_HTML = """{% extends 'base.html' %}{% block content %}
  <div class="alert alert-success" role="alert">
    Hola, <strong>{{ nombre }}</strong>!
  </div>
  <a href="{{ url_for('inicio') }}" class="btn btn-outline-secondary">Volver</a>
{% endblock %}"""

ABOUT_HTML = """{% extends 'base.html' %}{% block content %}
  <h1 class="h4">Acerca de</h1>
  <p>Esta aplicación está pensada para aprendizaje rápido de Flask.</p>
  <ul>
    <li>Usa <code>render_template_string</code> y un <em>loader</em> en memoria.</li>
    <li>Muestra rutas con parámetros, formularios y JSON.</li>
    <li>Incluye manejadores de errores 404 y 500.</li>
  </ul>
{% endblock %}"""


# Registrar las plantillas anteriores en el loader de Jinja2 como si fueran archivos
from jinja2 import DictLoader

app.jinja_loader = DictLoader({
    "base.html": BASE_HTML,
    "index.html": INDEX_HTML,
    "resultado.html": RESULTADO_HTML,
    "about.html": ABOUT_HTML,
})


# =========================================================================================
#  SECCIÓN 3 · Rutas de la aplicación (endpoints)
# =========================================================================================
# ? ¿Qué es una ruta?
#   - URL que el navegador solicita (ej: /saluda/Juan)
#   - Flask mapea la ruta a una función que devuelve respuesta (HTML, JSON, redirección, etc.)
#
# * @app.route(ruta, methods=[...]):
#   - Decorador que asocia una URL con una función Python
#   - methods: GET por defecto; POST, PUT, DELETE para APIs
#
# ! SECCIÓN 3.1: Ruta simple (sin parámetros)
@app.route("/")
def inicio():
    """🏠 Página principal.
    
    # * ¿Qué hace?
      - Devuelve la plantilla INDEX_HTML renderizada con Jinja2.
      - url_for('inicio'): genera la URL de esta función (seguro para cambios).
    
    # ? Prueba:
      - Navega a http://127.0.0.1:5000/
    """
    return render_template_string(INDEX_HTML, title="Inicio")


# ! SECCIÓN 3.2: Otra ruta simple
@app.route("/about")
def about():
    """ℹ️ Página informativa.
    
    # * Similar a inicio(), pero devuelve otra plantilla.
    """
    return render_template_string(ABOUT_HTML, title="Acerca de")


# ! SECCIÓN 3.3: Formulario POST (recibir datos del cliente)
@app.route("/procesar", methods=["POST"])
def procesar():
    """📨 Procesa formulario enviado por POST.
    
    # ? ¿Qué es POST?
      - Cliente envía datos SEGUROS (no aparecen en URL)
      - Content-Type: application/x-www-form-urlencoded
    
    # * ¿Cómo leer los datos?
      - request.form.get("nombre"): obtiene el valor del campo <input name="nombre">
      - "".strip(): elimina espacios al inicio/final
    
    # ! Validación:
      - Si el campo está vacío → redirigimos a inicio()
      - Si tiene valor → mostramos resultado
    """
    nombre = (request.form.get("nombre") or "").strip()
    if not nombre:
        # * Redirecciona sin procesar si no hay nombre
        return redirect(url_for("inicio"))
    return render_template_string(RESULTADO_HTML, title="Resultado", nombre=nombre)


# ! SECCIÓN 3.4: Ruta con parámetro (tipo string)
@app.route("/saluda/<nombre>")
def saluda(nombre: str):
    """👋 Saluda a alguien por su nombre.
    
    # * <nombre>: parámetro en la URL
      - String por defecto
      - Ejemplos: /saluda/Juan → nombre="Juan"
                  /saluda/Python → nombre="Python"
    
    # ? Type hints:
      - nombre: str  → declara que esperamos string (opcional, didáctico)
    
    # NOTE: Prueba estos enlaces:
      - http://127.0.0.1:5000/saluda/Joaquín
      - http://127.0.0.1:5000/saluda/Python
    """
    return f"Hola, {nombre}! 👋"


# ! SECCIÓN 3.5: Ruta con parámetros tipados (conversión automática)
@app.route("/suma/<int:a>/<int:b>")
def suma(a: int, b: int):
    """🧮 Suma dos números enteros.
    
    # * <int:a> y <int:b>: parámetros tipados
      - Flask convierte automáticamente a int
      - Si no es un número → error 404
    
    # ? Otros tipos soportados:
      - <int:numero>       → entero
      - <float:precio>     → decimal
      - <path:ruta>        → incluye barras (/)
      - <uuid:id>          → UUID válido
    
    # NOTE: Prueba:
      - http://127.0.0.1:5000/suma/10/20  → 30
      - http://127.0.0.1:5000/suma/abc/5  → 404 (abc no es int)
    """
    resultado = a + b
    return f"<h2>{a} + {b} = {resultado}</h2>"


# ! SECCIÓN 3.6: Query strings (GET con parámetros opcionales)
@app.route("/buscar")
def buscar():
    """🔍 Busca con parámetros en la query string.
    
    # ? ¿Qué son query strings?
      - Parámetros después del ? en la URL
      - Ejemplos: /buscar?q=flask&page=2
                  /buscar?q=python
    
    # * request.args.get(clave, default):
      - Lee el parámetro 'q' de la URL, por defecto ""
      - Lee el parámetro 'page', convertimos a int con default 1
    
    # ! jsonify():
      - Convierte un diccionario a JSON automáticamente
      - Content-Type: application/json
    
    # NOTE: Ejemplos:
      - http://127.0.0.1:5000/buscar?q=flask&page=1
      - http://127.0.0.1:5000/buscar?q=python&page=3
    """
    q = request.args.get("q", "")
    page = int(request.args.get("page", 1))
    return jsonify(ok=True, q=q, page=page, total_results=42)



# =========================================================================================
#  SECCIÓN 4 · Mini API JSON (para aplicaciones frontend/JavaScript)
# =========================================================================================
# ? ¿Qué es una API JSON?
#   - Endpoints que comunican con JavaScript, aplicaciones móviles, otros servidores
#   - Intercambian datos en formato JSON: {"clave": "valor"}
#   - Métodos HTTP estándar: GET (leer), POST (crear), PUT (actualizar), DELETE (borrar)
#
# * Ventajas:
#   - Ligero y fácil de parsear
#   - REST: interfaz estándar y predecible
#   - Desacoplado del HTML (reutilizable en múltiples frontends)
#
# ! SECCIÓN 4.1: API GET simple (devuelve lo que recibe)
@app.route("/api/echo")
def api_echo():
    """🔊 Echo API — repite lo que mandas en query string.
    
    # * Ejemplo:
      - GET /api/echo?q=hola
      - Respuesta: {"ok": true, "echo": "hola"}
    
    # ? Status code 200 (implícito):
      - Por defecto Flask devuelve 200 OK
    
    # TODO: (Tema: PRACTÍCANDO GET)
    # 1) Prueba esta ruta desde el navegador:
    #    http://127.0.0.1:5000/api/echo?q=flask
    # 2) Abre DevTools (F12) → Network → verás respuesta JSON
    # 3) Modifica para devolver más datos (ej: timestamp, user_agent)
    """
    q = request.args.get("q", "")
    return jsonify(ok=True, echo=q)


# ! SECCIÓN 4.2: API POST (recibe JSON, devuelve JSON)
@app.route("/api/saludo", methods=["POST"])
def api_saludo():
    """👋 Recibe JSON, devuelve JSON con mensaje personalizado.
    
    # ? ¿Cómo probar?
      - Opción 1: curl desde terminal
        curl -X POST -H "Content-Type: application/json" \\
             -d '{"nombre":"Ada"}' http://127.0.0.1:5000/api/saludo
      
      - Opción 2: JavaScript (Fetch API)
        fetch('/api/saludo', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({nombre: 'Ada'})
        }).then(r => r.json()).then(d => console.log(d))
      
      - Opción 3: DevTools Console (copiar y pegar)
    
    # * request.get_json(silent=True):
      - Lee el body como JSON
      - silent=True: devuelve None si no es JSON válido (sin error)
      - {} por defecto si no hay datos
    
    # ! Validación:
      - Si 'nombre' está vacío → error 400 Bad Request
      - Si todo bien → 200 OK con mensaje
    
    # TODO: (Tema: PRACTICANDO POST)
    # 1) Abre DevTools Console (F12)
    # 2) Copia y pega (ajusta "Ada"):
    #    fetch('/api/saludo', {
    #      method: 'POST',
    #      headers: {'Content-Type': 'application/json'},
    #      body: JSON.stringify({nombre: 'Ada'})
    #    }).then(r => r.json()).then(d => console.log(d))
    # 3) Mira la respuesta en la consola
    """
    data: Dict[str, Any] = request.get_json(silent=True) or {}
    nombre = str(data.get("nombre", "")).strip()
    
    if not nombre:
        # ! Status code 400: Bad Request
        return jsonify(ok=False, error="Campo 'nombre' requerido"), 400
    
    return jsonify(ok=True, mensaje=f"Hola, {nombre}! 👋", status="success")


# ! SECCIÓN 4.3: Health check (monitorización, tests)
@app.route("/api/health")
def api_health():
    """❤️ Health check — verifica que la app está activa.
    
    # ? Uso:
      - DevOps y monitoreo
      - Balanceadores de carga
      - Tests de integración
    
    # * Simplemente devuelve:
      - {"status": "ok"}
      - Status code 200
    
    # NOTE: En producción podrías añadir:
      - Verificación de base de datos
      - Chequeo de memoria/CPU
      - Versión de la app
    """
    return jsonify(status="ok", timestamp="2025-11-16"), 200


# ! SECCIÓN 4.4: API con manejo de errores más elaborado
@app.route("/api/calculadora/<operacion>/<int:a>/<int:b>")
def calculadora(operacion: str, a: int, b: int):
    """🧮 Calculadora simple como API.
    
    # * Parámetros:
      - operacion: "suma", "resta", "multiply", "divide"
      - a, b: números enteros
    
    # ? Ejemplo:
      - GET /api/calculadora/suma/5/3
      - Respuesta: {"ok": true, "resultado": 8}
    
    # ! Validación:
      - Operación desconocida → error 400
      - División por cero → error 400
    """
    operacion = operacion.lower()
    
    if operacion == "suma":
        resultado = a + b
    elif operacion == "resta":
        resultado = a - b
    elif operacion == "multiply":
        resultado = a * b
    elif operacion == "divide":
        if b == 0:
            return jsonify(ok=False, error="División por cero"), 400
        resultado = a / b
    else:
        return jsonify(ok=False, error=f"Operación '{operacion}' no válida"), 400
    
    return jsonify(ok=True, operacion=operacion, a=a, b=b, resultado=resultado)



# =========================================================================================
#  SECCIÓN 5 · Manejo de errores y hooks (before_request, after_request)
# =========================================================================================
# ? ¿Qué son los manejadores de errores?
#   - Funciones que se ejecutan cuando ocurre un error HTTP (404, 500, etc.)
#   - Devuelven respuestas personalizadas en lugar de la página por defecto de Flask
#
# * Códigos HTTP comunes:
#   - 200 OK: éxito
#   - 400 Bad Request: datos inválidos del cliente
#   - 404 Not Found: ruta no existe
#   - 500 Internal Server Error: error en el servidor
#
# ! SECCIÓN 5.1: Manejador 404 (ruta no encontrada)
@app.errorhandler(404)
def not_found(_e):  # type: ignore[misc]
    """❌ Ruta no encontrada.
    
    # * Cuándo se dispara:
      - Usuario accede a una URL que NO tiene asociada una función
      - Ej: /ruta-que-no-existe
    
    # ! Devolvemos JSON con:
      - error: descripción
      - status: código HTTP (404)
    
    # NOTE: El segundo argumento (error object) no lo usamos, por eso _e
    """
    return jsonify(error="Ruta no encontrada (404)", status=404, path=request.path), 404


# ! SECCIÓN 5.2: Manejador 500 (error del servidor)
@app.errorhandler(500)
def server_error(_e):  # type: ignore[misc]
    """⚡ Error interno del servidor.
    
    # * Cuándo se dispara:
      - Ocurre un error no manejado en el código (excepción)
      - Ej: división por cero, acceso a diccionario inválido, etc.
    
    # ! En debug=True (desarrollo):
      - Flask muestra página interactiva con traceback
      - Muy útil para diagnosticar
    
    # ! En debug=False (producción):
      - Se ejecuta este manejador
      - Devolvemos JSON genérico (sin exponer internals)
    """
    return jsonify(error="Error interno del servidor (500)", status=500), 500


# ! SECCIÓN 5.3: Ruta que provoca error deliberadamente
@app.route("/error-intencional")
def error_intencional():
    """💥 Genera un error para ver el manejador 500 en acción.
    
    # * Útil para:
      - Probar manejadores de errores
      - Entender cómo Flask maneja excepciones
      - Verificar logging en producción
    """
    raise RuntimeError("Fallo simulado para demostración didáctica")


# ! SECCIÓN 5.4: Hook before_request (se ejecuta ANTES de cada petición)
@app.before_request
def before() -> None:
    """⏱️ Hook: se ejecuta ANTES de procesar cada petición.
    
    # ? Casos de uso:
      - Validar autenticación
      - Iniciar cronómetro (benchmark)
      - Conectar a base de datos
      - Logs
      - Validar CSRF tokens
    
    # ! En este ejemplo no hacemos nada (opcional, didáctico)
    # ? TODO: Práctico — Medir tiempo de respuesta
    # 1) Descomenta el código abajo:
    #    from datetime import datetime
    #    request._start_time = datetime.now()
    # 2) En after_request, calcula: datetime.now() - request._start_time
    # 3) Añade el tiempo a las cabeceras: X-Response-Time
    """
    pass


# ! SECCIÓN 5.5: Hook after_request (se ejecuta DESPUÉS de cada petición)
@app.after_request
def after(response):  # type: ignore[no-untyped-def]
    """📤 Hook: se ejecuta DESPUÉS de procesar cada petición.
    
    # ? Casos de uso:
      - Añadir cabeceras personalizadas
      - CORS (compartir recursos entre dominios)
      - Logs de acceso
      - Validación de respuesta
      - Estadísticas/métricas
    
    # * Ejemplo: añadir cabecera X-Ejemplo
      - Los navegadores (y APIs) verán: X-Ejemplo: Flask-Tutorial
    
    # ! Siempre devolvemos response (IMPORTANTE)
    """
    response.headers.setdefault("X-Ejemplo", "Flask-Tutorial-Mejorado")
    response.headers.setdefault("X-Author", "Joaquin")
    return response



# =========================================================================================
#  SECCIÓN 6 · Laboratorio IA (Diseña tu propia ruta)
# =========================================================================================
# * PROMPT KIT para ChatGPT (copia/pega en ChatGPT)
#
# 1) PROMPT BÁSICO:
#    "Eres profesor de Flask. Genera una ruta Flask de 20-30 líneas que:
#     - Reciba parámetros tipados en la URL (/ruta/<tipo:param>)
#     - Valide al menos 2 condiciones diferentes (if/elif/else)
#     - Devuelva JSON con estructura: {'ok': bool, 'resultado': cualquiera, 'errores': list}
#     - Incluya comentarios con Better Comments (# * # ! # ?)
#     Tema: convertidor de unidades (Celsius ↔ Fahrenheit) o clasificador de edad.
#     Solo código Python, sin explicaciones extra."
#
# 2) PROMPT DE MEJORA:
#    "Mejora esta ruta Flask para manejar división por cero, valores negativos,
#     y devolver códigos HTTP apropiados (200, 400, 500).
#     Mantén el total de líneas bajo 40. Muéstrame solo el código."
#
# 3) PROMPT CREATIVO:
#    "Crea una mini API REST (GET y POST) que maneje un pequeño carrito de compras:
#     - GET /api/carrito: devuelve items
#     - POST /api/carrito: añade item con {nombre, precio, cantidad}
#     Valida que precio > 0. Devuelve JSON con total actualizado.
#     Usa comentarios Better Comments. 30-50 líneas."
#
# ! TODO: (Tema: GENERA CON IA)
# 1) Abre https://chatgpt.com/
# 2) Copia uno de los PROMPTS arriba
# 3) Pega el código aquí abajo (descomenta):

# def mi_ruta_ia():
#     """Tu código generado por IA aquí"""
#     pass


# =========================================================================================
#  SECCIÓN 7 · Punto de entrada + ejecución
# =========================================================================================
# ? ¿Qué es if __name__ == "__main__"?
#   - Bloque que se ejecuta SOLO si el archivo se corre directamente
#   - NO se ejecuta si se importa en otro módulo
#
# * Estructura típica:
#   - Configuraciones finales
#   - app.run(): inicia el servidor
#
# ! app.run(debug=True):
#   - debug=True: recarga automática, página de errores interactiva
#   - host="0.0.0.0": accesible desde cualquier IP (default: localhost)
#   - port=5000: puerto (default)
#   - threaded=True: soporta múltiples peticiones simultáneas

if __name__ == "__main__":
    # ! MODO DEBUG
    # Características:
    # - Recarga automática al guardar cambios (Debugger)
    # - Página de errores interactiva (Werkzeug debugger)
    # - Console interactiva si necesitas
    print("=" * 80)
    print("🚀 Flask Tutorial iniciándose...")
    print("=" * 80)
    print("\n📌 URL LOCAL: http://127.0.0.1:5000/")
    print("📌 PRESIONA Ctrl+C para parar el servidor\n")
    print("=" * 80 + "\n")
    
    # * Iniciar servidor
    app.run(debug=DEBUG_MODE)

    # ? Si quisieras ejecutar en PRODUCCIÓN (no uses en desarrollo):
    # gunicorn -w 4 -b 0.0.0.0:8000 "14_flask_tutorial:app"
    # (-w 4 = 4 workers; -b 0.0.0.0:8000 = puerto 8000)


