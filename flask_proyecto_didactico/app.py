# =========================================================================================
#  "YO! PROYECTO FLASK LISTO PARA PRACTICAR" - Version didactica y comentada
#  ---------------------------------------------------------------------------------
#  En esta clase practicaras:
#    * Crear una aplicacion Flask (init y configuracion)
#    * Rutas basicas (@app.route) y rutas con parametros
#    * Metodos HTTP (GET, POST) y lectura de datos
#    * Plantillas Jinja2 (archivos en templates/) con herencia (extends)
#    * Formularios HTML (POST) y query strings (GET)
#    * API JSON: endpoints que envian/reciben JSON con codigos HTTP
#    * Manejo de errores (404, 500) y hooks (before_request, after_request)
#    * TODOs para que practiques y mods sugeridos para IA
#
#  Requisitos previos:
#    - Python 3.10+ (o similar)
#    - Flask (pip install flask)
#
#  Como usar (Windows):
#    1) Crear entorno:  python -m venv env
#    2) Activar:        .\\env\\Scripts\\activate
#    3) Instalar:       pip install flask
#    4) Ejecutar:       python app.py   (desde esta carpeta)
#    5) Navegar:        http://127.0.0.1:5000/
#
#  Better Comments:
#    # ! importante   |  # * definicion/foco   |  # ? idea/nota
#    # TODO: practica |  # NOTE: apunte util   |  # // deprecado
#
#  Consejo: lee el archivo de arriba a abajo. Cada seccion esta comentada paso a paso.
# =========================================================================================

from __future__ import annotations

from typing import Any, Dict

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)


# =========================================================================================
#  * CONFIGURACION GLOBAL (para desarrolladores)
# =========================================================================================
DEBUG_MODE = True           # ! Activa recarga automatica y pagina de errores interactiva
ECHO_LOGS = True            # * Imprime logs en terminal de cada peticion
PAUSE_ON_DEMO = False       # ? True: pausa tras cada demo (usa input())


# =========================================================================================
#  SECCION 1 >> Inicializacion de la aplicacion Flask
# =========================================================================================
# ? Que es Flask?
#   - Framework web ligero y flexible de Python.
#   - Permite crear rutas (URLs), recibir datos, aplicar logica y devolver respuestas.
#
# * Crear la aplicacion:
#   - Flask(__name__): crea instancia; __name__ ayuda a encontrar recursos.
#   - app.config: diccionario de configuracion (debug, secreto, etc.).
app = Flask(__name__)

# ! Configuraciones utiles en desarrollo
app.config.update(
    JSON_AS_ASCII=False,         # * Permite acentos en JSON (sin escapar)
    TEMPLATES_AUTO_RELOAD=True,  # * Recarga plantillas si cambian (debug)
)


# =========================================================================================
#  SECCION 2 >> Rutas de la aplicacion (endpoints)
# =========================================================================================
# ? Que es una ruta?
#   - URL que el navegador solicita (ej: /saluda/Juan)
#   - Flask mapea la ruta a una funcion que devuelve respuesta (HTML, JSON, redirect, etc.)
#
# * @app.route(ruta, methods=[...]):
#   - Decorador que asocia una URL con una funcion Python
#   - methods: GET por defecto; POST, PUT, DELETE para APIs


@app.route("/")
def inicio():
    """Pagina principal.

    # * Que hace?
      - Renderiza templates/index.html
      - url_for('inicio'): genera URL de esta funcion (seguro para cambios).
    """
    return render_template("index.html", title="Inicio")


@app.route("/about")
def about():
    """Pagina informativa."""
    return render_template("about.html", title="Acerca de")


@app.route("/procesar", methods=["POST"])
def procesar():
    """Procesa formulario enviado por POST.

    # * Leer datos:
      - request.form.get("nombre"): valor del input name="nombre"
      - "".strip(): elimina espacios al inicio/final
    """
    nombre = (request.form.get("nombre") or "").strip()
    if not nombre:
        return redirect(url_for("inicio"))
    return render_template("resultado.html", title="Resultado", nombre=nombre)


@app.route("/saluda/<nombre>")
def saluda(nombre: str):
    """Saluda usando un parametro en la URL."""
    return f"Hola, {nombre}! :)"


@app.route("/suma/<int:a>/<int:b>")
def suma(a: int, b: int):
    """Suma dos numeros enteros recibidos en la URL."""
    resultado = a + b
    return f"<h2>{a} + {b} = {resultado}</h2>"


@app.route("/buscar")
def buscar():
    """Busca con parametros en la query string (?q=valor&page=2)."""
    q = request.args.get("q", "")
    page = int(request.args.get("page", 1))
    return jsonify(ok=True, q=q, page=page, total_results=42)


# =========================================================================================
#  SECCION 3 >> Mini API JSON (para frontend/JS)
# =========================================================================================
# ? Que es una API JSON?
#   - Endpoints que hablan con JavaScript, apps moviles, otros servidores.
#   - Intercambian datos en formato JSON: {"clave": "valor"}
#   - Metodos HTTP estandar: GET (leer), POST (crear), PUT (actualizar), DELETE (borrar)


@app.route("/api/echo")
def api_echo():
    """Echo API -> repite lo que mandas en query string."""
    q = request.args.get("q", "")
    return jsonify(ok=True, echo=q)


@app.route("/api/saludo", methods=["POST"])
def api_saludo():
    """Recibe JSON, devuelve JSON con mensaje personalizado."""
    data: Dict[str, Any] = request.get_json(silent=True) or {}
    nombre = str(data.get("nombre", "")).strip()

    if not nombre:
        # ! Status code 400: Bad Request
        return jsonify(ok=False, error="Campo 'nombre' requerido"), 400

    return jsonify(ok=True, mensaje=f"Hola, {nombre}!", status="success")


@app.route("/api/health")
def api_health():
    """Health check -> verifica que la app esta activa."""
    return jsonify(status="ok"), 200


@app.route("/api/calculadora/<operacion>/<int:a>/<int:b>")
def calculadora(operacion: str, a: int, b: int):
    """Calculadora simple como API."""
    operacion = operacion.lower()

    if operacion == "suma":
        resultado = a + b
    elif operacion == "resta":
        resultado = a - b
    elif operacion == "multiply":
        resultado = a * b
    elif operacion == "divide":
        if b == 0:
            return jsonify(ok=False, error="Division por cero"), 400
        resultado = a / b
    else:
        return jsonify(ok=False, error=f"Operacion '{operacion}' no valida"), 400

    return jsonify(ok=True, operacion=operacion, a=a, b=b, resultado=resultado)


# =========================================================================================
#  SECCION 4 >> Manejo de errores y hooks (before_request, after_request)
# =========================================================================================
# * Codigos HTTP comunes:
#   - 200 OK: exito
#   - 400 Bad Request: datos invalidos del cliente
#   - 404 Not Found: ruta no existe
#   - 500 Internal Server Error: error en el servidor


@app.errorhandler(404)
def not_found(_e):  # type: ignore[misc]
    """Ruta no encontrada."""
    return jsonify(error="Ruta no encontrada (404)", status=404, path=request.path), 404


@app.errorhandler(500)
def server_error(_e):  # type: ignore[misc]
    """Error interno del servidor."""
    return jsonify(error="Error interno del servidor (500)", status=500), 500


@app.route("/error-intencional")
def error_intencional():
    """Genera un error para ver el manejador 500 en accion."""
    raise RuntimeError("Fallo simulado para demostracion didactica")


@app.before_request
def before() -> None:
    """Hook: se ejecuta ANTES de procesar cada peticion."""
    if ECHO_LOGS:
        print(f"[before_request] {request.method} {request.path}")
    # TODO: Practica -> guarda datetime.now() en request para medir tiempos.


@app.after_request
def after(response):  # type: ignore[no-untyped-def]
    """Hook: se ejecuta DESPUES de cada peticion."""
    response.headers.setdefault("X-Ejemplo", "Flask-Tutorial-Didactico")
    response.headers.setdefault("X-Author", "Joaquin")
    return response


# =========================================================================================
#  SECCION 5 >> Laboratorio IA (disena tu propia ruta)
# =========================================================================================
# * PROMPT KIT para ChatGPT (copia/pega en ChatGPT)
#
# 1) PROMPT BASICO:
#    "Eres profesor de Flask. Genera una ruta Flask de 20-30 lineas que:
#     - Reciba parametros tipados en la URL (/ruta/<tipo:param>)
#     - Valide al menos 2 condiciones diferentes (if/elif/else)
#     - Devuelva JSON con estructura: {'ok': bool, 'resultado': cualquiera, 'errores': list}
#     - Incluya comentarios con Better Comments (# * # ! # ?)
#     Tema: convertidor de unidades (Celsius -> Fahrenheit) o clasificador de edad.
#     Solo codigo Python, sin explicaciones extra."
#
# 2) PROMPT DE MEJORA:
#    "Mejora esta ruta Flask para manejar division por cero, valores negativos,
#     y devolver codigos HTTP apropiados (200, 400, 500).
#     Manten el total de lineas bajo 40. Muestrame solo el codigo."
#
# 3) PROMPT CREATIVO:
#    "Crea una mini API REST (GET y POST) que maneje un pequeno carrito de compras:
#     - GET /api/carrito: devuelve items
#     - POST /api/carrito: anade item con {nombre, precio, cantidad}
#     Valida que precio > 0. Devuelve JSON con total actualizado.
#     Usa comentarios Better Comments. 30-50 lineas."
#
# ! TODO: (Tema: GENERA CON IA)
# 1) Abre https://chatgpt.com/
# 2) Copia uno de los PROMPTS arriba
# 3) Pega el codigo aqui abajo (descomenta) y ajusta la ruta:
#
# @app.route("/mi-ruta-ia")
# def mi_ruta_ia():
#     """Tu codigo generado por IA aqui"""
#     pass


# =========================================================================================
#  SECCION 6 >> Punto de entrada + ejecucion
# =========================================================================================
# ? Que es if __name__ == "__main__"?
#   - Bloque que se ejecuta SOLO si el archivo se corre directamente
#   - NO se ejecuta si se importa en otro modulo
#
# * Estructura tipica:
#   - Configuraciones finales
#   - app.run(): inicia el servidor

if __name__ == "__main__":
    # ! MODO DEBUG
    # Caracteristicas:
    # - Recarga automatica al guardar cambios (Debugger)
    # - Pagina de errores interactiva (Werkzeug debugger)
    # - Consola interactiva si necesitas
    print("=" * 80)
    print(">> Flask Tutorial didactico iniciandose...")
    print("=" * 80)
    print("\nURL LOCAL: http://127.0.0.1:5000/")
    print("Presiona Ctrl+C para parar el servidor\n")
    print("=" * 80 + "\n")

    # * Iniciar servidor
    app.run(debug=DEBUG_MODE)

    # ? Si quisieras ejecutar en PRODUCCION (no uses en desarrollo):
    # gunicorn -w 4 -b 0.0.0.0:8000 \"app:app\"
