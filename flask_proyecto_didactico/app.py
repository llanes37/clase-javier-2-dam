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
#   - URL que el navegador solicita (ej: /saluda/Juan/Perez/20)
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


@app.route("/saluda/<nombre>/<apellido>/<int:edad>")
def saluda(nombre: str, apellido: str, edad: int):
    """Saluda usando parametros en la URL."""
    return f"Hola, {nombre} {apellido}! Tienes {edad} anos :)"


@app.route("/suma/<int:a>/<int:b>")
def suma(a: int, b: int):
    """Suma dos numeros enteros recibidos en la URL."""
    resultado = a + b
    return f"<h2>{a} + {b} = {resultado}</h2>"


@app.route("/resta/<int:a>/<int:b>")
def resta(a: int, b: int):
    """Resta dos numeros enteros recibidos en la URL."""
    resultado = a - b
    return f"<h2>{a} - {b} = {resultado}</h2>"


@app.route("/multiplicacion/<int:a>/<int:b>")
def multiplicacion(a: int, b: int):
    """Multiplica dos numeros enteros recibidos en la URL."""
    resultado = a * b
    return f"<h2>{a} * {b} = {resultado}</h2>"


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
    operacion_resuelta = operacion

    if operacion == "suma":
        resultado = a + b
    elif operacion == "resta":
        resultado = a - b
    elif operacion in ("multiply", "multiplicacion", "multiplicar"):
        operacion_resuelta = "multiplicacion"
        resultado = a * b
    elif operacion == "divide":
        if b == 0:
            return jsonify(ok=False, error="Division por cero"), 400
        resultado = a / b
    else:
        return jsonify(ok=False, error=f"Operacion '{operacion}' no valida"), 400

    return jsonify(ok=True, operacion=operacion_resuelta, a=a, b=b, resultado=resultado)


@app.route("/api/mejores-juegos")
def api_mejores_juegos():
    """API: Mejores videojuegos de cada categoría - Actualizado Diciembre 2025.
    
    Fuentes: Steam, Epic Games, GOG, itch.io, GameJolt, Ubisoft Connect
    """
    mejores_juegos = {
        # ═══════════════════════════════════════════════════════════════════════
        # 🎮 RPG - Los mejores juegos de rol de 2024-2025
        # ═══════════════════════════════════════════════════════════════════════
        "rpg": [
            {
                "id": 1,
                "nombre": "Baldur's Gate 3",
                "plataforma": "Steam, GOG, PlayStation 5, Xbox Series X",
                "rating": 9.6,
                "precio": 59.99,
                "desarrollador": "Larian Studios",
                "año": 2023,
                "descripcion": "GOTY 2023. RPG épico basado en D&D con libertad narrativa sin precedentes",
                "imagen": "baldurs-gate-3",
                "tags": ["RPG", "Por Turnos", "Fantasía", "Cooperativo"],
                "fuente": "Steam/GOG"
            },
            {
                "id": 2,
                "nombre": "Elden Ring: Shadow of the Erdtree",
                "plataforma": "Steam, PlayStation, Xbox",
                "rating": 9.5,
                "precio": 39.99,
                "desarrollador": "FromSoftware",
                "año": 2024,
                "descripcion": "La expansión masiva del GOTY 2022 con nuevas zonas y jefes devastadores",
                "imagen": "elden-ring-dlc",
                "tags": ["Souls-like", "Mundo Abierto", "Difícil", "Fantasía Oscura"],
                "fuente": "Steam"
            },
            {
                "id": 3,
                "nombre": "The Witcher 3: Wild Hunt - Complete Edition",
                "plataforma": "Steam, GOG, Epic Games, Consolas",
                "rating": 9.8,
                "precio": 9.99,
                "desarrollador": "CD Projekt Red",
                "año": 2015,
                "descripcion": "La obra maestra atemporal. Geralt de Rivia en su mejor aventura, ahora con mejoras next-gen",
                "imagen": "witcher-3",
                "tags": ["RPG", "Mundo Abierto", "Fantasía", "Historia Rica"],
                "fuente": "GOG/Steam"
            },
            {
                "id": 4,
                "nombre": "Cyberpunk 2077: Ultimate Edition",
                "plataforma": "Steam, GOG, Epic Games, Consolas",
                "rating": 9.2,
                "precio": 59.99,
                "desarrollador": "CD Projekt Red",
                "año": 2020,
                "descripcion": "Night City redimido. Incluye Phantom Liberty, la expansión aclamada por la crítica",
                "imagen": "cyberpunk-2077",
                "tags": ["RPG", "Cyberpunk", "Mundo Abierto", "Futurista"],
                "fuente": "GOG/Steam"
            },
            {
                "id": 5,
                "nombre": "Persona 5 Royal",
                "plataforma": "Steam, PlayStation, Xbox, Nintendo Switch",
                "rating": 9.4,
                "precio": 59.99,
                "desarrollador": "Atlus",
                "año": 2019,
                "descripcion": "El JRPG definitivo. Estilo único, historia profunda y banda sonora icónica",
                "imagen": "persona-5-royal",
                "tags": ["JRPG", "Por Turnos", "Estilo de Vida", "Anime"],
                "fuente": "Steam"
            },
            {
                "id": 6,
                "nombre": "Disco Elysium - The Final Cut",
                "plataforma": "Steam, GOG, Epic Games, Consolas",
                "rating": 9.3,
                "precio": 39.99,
                "desarrollador": "ZA/UM",
                "año": 2019,
                "descripcion": "RPG revolucionario sin combate. Detective amnésico en un mundo único",
                "imagen": "disco-elysium",
                "tags": ["RPG", "Narrativo", "Detective", "Indie"],
                "fuente": "GOG"
            },
            {
                "id": 7,
                "nombre": "Dragon's Dogma 2",
                "plataforma": "Steam, PlayStation 5, Xbox Series X",
                "rating": 8.8,
                "precio": 69.99,
                "desarrollador": "Capcom",
                "año": 2024,
                "descripcion": "RPG de acción con el revolucionario sistema de Pawns y combate espectacular",
                "imagen": "dragons-dogma-2",
                "tags": ["RPG", "Acción", "Fantasía", "Mundo Abierto"],
                "fuente": "Steam"
            },
            {
                "id": 8,
                "nombre": "Pathfinder: Wrath of the Righteous",
                "plataforma": "Steam, GOG, Consolas",
                "rating": 9.0,
                "precio": 49.99,
                "desarrollador": "Owlcat Games",
                "año": 2021,
                "descripcion": "CRPG épico con cientos de horas de contenido y múltiples caminos míticos",
                "imagen": "pathfinder-wotr",
                "tags": ["CRPG", "Por Turnos", "Fantasía", "Táctico"],
                "fuente": "GOG"
            }
        ],

        # ═══════════════════════════════════════════════════════════════════════
        # ⚔️ ACCIÓN - Juegos de acción más valorados
        # ═══════════════════════════════════════════════════════════════════════
        "accion": [
            {
                "id": 9,
                "nombre": "God of War Ragnarök",
                "plataforma": "Steam, PlayStation",
                "rating": 9.5,
                "precio": 59.99,
                "desarrollador": "Santa Monica Studio",
                "año": 2024,
                "descripcion": "Kratos y Atreus enfrentan el Ragnarök en esta épica conclusión nórdica",
                "imagen": "god-of-war-ragnarok",
                "tags": ["Acción", "Aventura", "Mitología", "Narrativo"],
                "fuente": "Steam"
            },
            {
                "id": 10,
                "nombre": "Devil May Cry 5: Special Edition",
                "plataforma": "Steam, Consolas",
                "rating": 9.1,
                "precio": 29.99,
                "desarrollador": "Capcom",
                "año": 2019,
                "descripcion": "El rey del hack and slash estilizado con combate frenético y satisfactorio",
                "imagen": "dmc5",
                "tags": ["Acción", "Hack and Slash", "Estilizado"],
                "fuente": "Steam"
            },
            {
                "id": 11,
                "nombre": "Star Wars Outlaws",
                "plataforma": "Ubisoft Connect, Epic Games, Consolas",
                "rating": 8.5,
                "precio": 69.99,
                "desarrollador": "Massive Entertainment",
                "año": 2024,
                "descripcion": "Primer mundo abierto de Star Wars. Vive como un forajido en la galaxia",
                "imagen": "star-wars-outlaws",
                "tags": ["Acción", "Mundo Abierto", "Ciencia Ficción", "Sigilo"],
                "fuente": "Ubisoft Connect"
            },
            {
                "id": 12,
                "nombre": "HITMAN World of Assassination",
                "plataforma": "Steam, Epic Games, Consolas",
                "rating": 9.0,
                "precio": 69.99,
                "desarrollador": "IO Interactive",
                "año": 2024,
                "descripcion": "La trilogía completa del Agente 47. Sandbox de asesinato perfecto",
                "imagen": "hitman-woa",
                "tags": ["Acción", "Sigilo", "Sandbox", "Estrategia"],
                "fuente": "Epic Games"
            },
            {
                "id": 13,
                "nombre": "Sekiro: Shadows Die Twice",
                "plataforma": "Steam, PlayStation, Xbox",
                "rating": 9.4,
                "precio": 59.99,
                "desarrollador": "FromSoftware",
                "año": 2019,
                "descripcion": "GOTY 2019. Combate de espadas más preciso y satisfactorio jamás creado",
                "imagen": "sekiro",
                "tags": ["Acción", "Souls-like", "Japón Feudal", "Difícil"],
                "fuente": "Steam"
            },
            {
                "id": 14,
                "nombre": "Monster Hunter: World",
                "plataforma": "Steam, PlayStation, Xbox",
                "rating": 9.1,
                "precio": 29.99,
                "desarrollador": "Capcom",
                "año": 2018,
                "descripcion": "Caza épica de monstruos con combate profundo y satisfactorio",
                "imagen": "mh-world",
                "tags": ["Acción", "Cooperativo", "Caza", "RPG"],
                "fuente": "Steam"
            }
        ],

        # ═══════════════════════════════════════════════════════════════════════
        # 🗺️ AVENTURA - Experiencias narrativas inolvidables
        # ═══════════════════════════════════════════════════════════════════════
        "aventura": [
            {
                "id": 15,
                "nombre": "Red Dead Redemption 2",
                "plataforma": "Steam, Epic Games, Consolas",
                "rating": 9.7,
                "precio": 59.99,
                "desarrollador": "Rockstar Games",
                "año": 2019,
                "descripcion": "La obra maestra del salvaje oeste. Arthur Morgan en una historia inolvidable",
                "imagen": "rdr2",
                "tags": ["Aventura", "Mundo Abierto", "Western", "Narrativo"],
                "fuente": "Steam"
            },
            {
                "id": 16,
                "nombre": "Hogwarts Legacy",
                "plataforma": "Steam, Epic Games, Consolas",
                "rating": 8.9,
                "precio": 59.99,
                "desarrollador": "Avalanche Software",
                "año": 2023,
                "descripcion": "Vive tu fantasía de Hogwarts en el siglo XIX con magia y exploración",
                "imagen": "hogwarts-legacy",
                "tags": ["Aventura", "RPG", "Mundo Abierto", "Magia"],
                "fuente": "Steam"
            },
            {
                "id": 17,
                "nombre": "It Takes Two",
                "plataforma": "Steam, Origin, Consolas",
                "rating": 9.3,
                "precio": 39.99,
                "desarrollador": "Hazelight Studios",
                "año": 2021,
                "descripcion": "GOTY 2021. Aventura cooperativa obligatoria con mecánicas siempre frescas",
                "imagen": "it-takes-two",
                "tags": ["Aventura", "Cooperativo", "Plataformas", "Narrativo"],
                "fuente": "Steam"
            },
            {
                "id": 18,
                "nombre": "A Plague Tale: Requiem",
                "plataforma": "Steam, Xbox Game Pass, Consolas",
                "rating": 8.7,
                "precio": 49.99,
                "desarrollador": "Asobo Studio",
                "año": 2022,
                "descripcion": "Secuela épica con historia emotiva y gráficos impresionantes",
                "imagen": "plague-tale-requiem",
                "tags": ["Aventura", "Sigilo", "Narrativo", "Medieval"],
                "fuente": "Steam"
            },
            {
                "id": 19,
                "nombre": "Outer Wilds",
                "plataforma": "Steam, Epic Games, Consolas",
                "rating": 9.5,
                "precio": 24.99,
                "desarrollador": "Mobius Digital",
                "año": 2019,
                "descripcion": "Exploración espacial única con bucle temporal. Experiencia irrepetible",
                "imagen": "outer-wilds",
                "tags": ["Aventura", "Exploración", "Misterio", "Indie"],
                "fuente": "Steam"
            },
            {
                "id": 20,
                "nombre": "Immortals Fenyx Rising",
                "plataforma": "Ubisoft Connect, Epic Games, Consolas",
                "rating": 8.3,
                "precio": 59.99,
                "desarrollador": "Ubisoft Quebec",
                "año": 2020,
                "descripcion": "Aventura mitológica griega con puzzles creativos y humor encantador",
                "imagen": "immortals-fenyx",
                "tags": ["Aventura", "Mitología", "Mundo Abierto", "Puzzle"],
                "fuente": "Ubisoft Connect"
            }
        ],

        # ═══════════════════════════════════════════════════════════════════════
        # 🔫 SHOOTER/FPS - Los mejores tiradores de 2024-2025
        # ═══════════════════════════════════════════════════════════════════════
        "shooter": [
            {
                "id": 21,
                "nombre": "Counter-Strike 2",
                "plataforma": "Steam",
                "rating": 8.8,
                "precio": 0,
                "desarrollador": "Valve",
                "año": 2023,
                "descripcion": "El shooter táctico definitivo, ahora con Source 2 y tick rate mejorado",
                "imagen": "cs2",
                "tags": ["FPS", "Táctico", "Competitivo", "E-Sports"],
                "fuente": "Steam"
            },
            {
                "id": 22,
                "nombre": "S.T.A.L.K.E.R. 2: Heart of Chornobyl",
                "plataforma": "Steam, GOG, Xbox",
                "rating": 8.9,
                "precio": 59.99,
                "desarrollador": "GSC Game World",
                "año": 2024,
                "descripcion": "El regreso legendario a la Zona. Supervivencia hardcore en Chernóbil",
                "imagen": "stalker-2",
                "tags": ["FPS", "Supervivencia", "Horror", "Mundo Abierto"],
                "fuente": "GOG/Steam"
            },
            {
                "id": 23,
                "nombre": "DOOM Eternal",
                "plataforma": "Steam, Bethesda, Consolas",
                "rating": 9.2,
                "precio": 39.99,
                "desarrollador": "id Software",
                "año": 2020,
                "descripcion": "Shooter frenético perfecto. Rip and tear hasta que esté hecho",
                "imagen": "doom-eternal",
                "tags": ["FPS", "Acción", "Demonic", "Frenético"],
                "fuente": "Steam"
            },
            {
                "id": 24,
                "nombre": "Destiny 2: The Final Shape",
                "plataforma": "Steam, Epic Games, Consolas",
                "rating": 8.5,
                "precio": 49.99,
                "desarrollador": "Bungie",
                "año": 2024,
                "descripcion": "La conclusión épica de la saga Luz vs Oscuridad con raids épicos",
                "imagen": "destiny-2-final-shape",
                "tags": ["FPS", "Looter", "MMO", "Cooperativo"],
                "fuente": "Steam/Epic"
            },
            {
                "id": 25,
                "nombre": "Valorant",
                "plataforma": "Riot Games",
                "rating": 8.7,
                "precio": 0,
                "desarrollador": "Riot Games",
                "año": 2020,
                "descripcion": "FPS táctico con habilidades únicas. El nuevo rey del competitivo",
                "imagen": "valorant",
                "tags": ["FPS", "Táctico", "Competitivo", "E-Sports"],
                "fuente": "Riot Games"
            },
            {
                "id": 26,
                "nombre": "Call of Duty: Black Ops 6",
                "plataforma": "Steam, Battle.net, Consolas",
                "rating": 8.4,
                "precio": 69.99,
                "desarrollador": "Treyarch",
                "año": 2024,
                "descripcion": "El nuevo COD con campaña aclamada y sistema de movimiento omni",
                "imagen": "cod-bo6",
                "tags": ["FPS", "Multijugador", "Zombies", "Campaña"],
                "fuente": "Steam"
            }
        ],

        # ═══════════════════════════════════════════════════════════════════════
        # 👻 HORROR - Los más terroríficos de 2024-2025
        # ═══════════════════════════════════════════════════════════════════════
        "horror": [
            {
                "id": 27,
                "nombre": "Alan Wake 2",
                "plataforma": "Epic Games, PlayStation 5, Xbox Series X",
                "rating": 9.1,
                "precio": 59.99,
                "desarrollador": "Remedy Entertainment",
                "año": 2023,
                "descripcion": "Obra maestra del horror psicológico. Narrativa revolucionaria",
                "imagen": "alan-wake-2",
                "tags": ["Horror", "Thriller", "Narrativo", "Psicológico"],
                "fuente": "Epic Games"
            },
            {
                "id": 28,
                "nombre": "Resident Evil 4 Remake",
                "plataforma": "Steam, Consolas",
                "rating": 9.3,
                "precio": 59.99,
                "desarrollador": "Capcom",
                "año": 2023,
                "descripcion": "El remake perfecto. León Kennedy en su misión más icónica, reinventada",
                "imagen": "re4-remake",
                "tags": ["Horror", "Acción", "Survival", "Remake"],
                "fuente": "Steam"
            },
            {
                "id": 29,
                "nombre": "Silent Hill 2 Remake",
                "plataforma": "Steam, PlayStation 5",
                "rating": 9.0,
                "precio": 69.99,
                "desarrollador": "Bloober Team",
                "año": 2024,
                "descripcion": "El regreso del horror psicológico definitivo. James busca a Mary en Silent Hill",
                "imagen": "silent-hill-2-remake",
                "tags": ["Horror", "Psicológico", "Survival", "Remake"],
                "fuente": "Steam"
            },
            {
                "id": 30,
                "nombre": "Dead Space Remake",
                "plataforma": "Steam, Origin, Consolas",
                "rating": 8.9,
                "precio": 59.99,
                "desarrollador": "Motive Studio",
                "año": 2023,
                "descripcion": "Isaac Clarke contra los Necromorphs en el USG Ishimura reimaginado",
                "imagen": "dead-space-remake",
                "tags": ["Horror", "Ciencia Ficción", "Survival", "Remake"],
                "fuente": "Steam"
            },
            {
                "id": 31,
                "nombre": "Amnesia: The Bunker",
                "plataforma": "Steam, GOG, Consolas",
                "rating": 8.6,
                "precio": 24.99,
                "desarrollador": "Frictional Games",
                "año": 2023,
                "descripcion": "Horror inmersivo en un búnker de la WWI con amenaza procedural",
                "imagen": "amnesia-bunker",
                "tags": ["Horror", "Supervivencia", "Indie", "Atmosférico"],
                "fuente": "Steam/GOG"
            },
            {
                "id": 32,
                "nombre": "Lethal Company",
                "plataforma": "Steam",
                "rating": 9.5,
                "precio": 9.99,
                "desarrollador": "Zeekerss",
                "año": 2023,
                "descripcion": "Horror cooperativo viral. Explora lunas abandonadas con tus amigos",
                "imagen": "lethal-company",
                "tags": ["Horror", "Cooperativo", "Indie", "Multijugador"],
                "fuente": "Steam"
            }
        ],

        # ═══════════════════════════════════════════════════════════════════════
        # 🏰 ESTRATEGIA - Pensamiento táctico y gestión
        # ═══════════════════════════════════════════════════════════════════════
        "estrategia": [
            {
                "id": 33,
                "nombre": "Total War: Warhammer III",
                "plataforma": "Steam, Epic Games",
                "rating": 9.0,
                "precio": 59.99,
                "desarrollador": "Creative Assembly",
                "año": 2022,
                "descripcion": "La culminación épica de la trilogía con el mapa mortal combinado",
                "imagen": "tw-warhammer-3",
                "tags": ["Estrategia", "Fantasía", "Por Turnos", "RTS"],
                "fuente": "Steam"
            },
            {
                "id": 34,
                "nombre": "Manor Lords",
                "plataforma": "Steam, GOG",
                "rating": 9.2,
                "precio": 39.99,
                "desarrollador": "Slavic Magic",
                "año": 2024,
                "descripcion": "City builder medieval con batallas tácticas. El indie del año",
                "imagen": "manor-lords",
                "tags": ["Estrategia", "City Builder", "Medieval", "Indie"],
                "fuente": "GOG/Steam"
            },
            {
                "id": 35,
                "nombre": "Crusader Kings III",
                "plataforma": "Steam, GOG, Xbox Game Pass",
                "rating": 9.1,
                "precio": 49.99,
                "desarrollador": "Paradox Interactive",
                "año": 2020,
                "descripcion": "Simulador de dinastías medieval. Drama, intriga y conquista",
                "imagen": "ck3",
                "tags": ["Estrategia", "Gran Estrategia", "Medieval", "RPG"],
                "fuente": "Steam"
            },
            {
                "id": 36,
                "nombre": "Age of Mythology: Retold",
                "plataforma": "Steam, Xbox",
                "rating": 8.7,
                "precio": 29.99,
                "desarrollador": "World's Edge",
                "año": 2024,
                "descripcion": "El clásico RTS mitológico remasterizado con gráficos modernos",
                "imagen": "aom-retold",
                "tags": ["Estrategia", "RTS", "Mitología", "Remake"],
                "fuente": "Steam"
            },
            {
                "id": 37,
                "nombre": "Civilization VI",
                "plataforma": "Steam, Epic Games, Consolas",
                "rating": 9.0,
                "precio": 59.99,
                "desarrollador": "Firaxis Games",
                "año": 2016,
                "descripcion": "El rey de la estrategia 4X. Una partida más y son las 4AM",
                "imagen": "civ6",
                "tags": ["Estrategia", "4X", "Por Turnos", "Histórico"],
                "fuente": "Steam"
            },
            {
                "id": 38,
                "nombre": "Northgard",
                "plataforma": "Steam, GOG",
                "rating": 8.5,
                "precio": 29.99,
                "desarrollador": "Shiro Games",
                "año": 2018,
                "descripcion": "RTS vikingo accesible pero profundo con múltiples condiciones de victoria",
                "imagen": "northgard",
                "tags": ["Estrategia", "RTS", "Vikingos", "Indie"],
                "fuente": "Steam"
            }
        ],

        # ═══════════════════════════════════════════════════════════════════════
        # 🎲 INDIE - Las joyas independientes más aclamadas
        # ═══════════════════════════════════════════════════════════════════════
        "indie": [
            {
                "id": 39,
                "nombre": "Hades II (Early Access)",
                "plataforma": "Steam, Epic Games",
                "rating": 9.4,
                "precio": 29.99,
                "desarrollador": "Supergiant Games",
                "año": 2024,
                "descripcion": "Melinoë busca a Cronos. El roguelike más esperado, ya es increíble",
                "imagen": "hades-2",
                "tags": ["Roguelike", "Acción", "Mitología", "Indie"],
                "fuente": "Steam"
            },
            {
                "id": 40,
                "nombre": "Balatro",
                "plataforma": "Steam, GOG, Consolas",
                "rating": 9.6,
                "precio": 14.99,
                "desarrollador": "LocalThunk",
                "año": 2024,
                "descripcion": "Roguelike de poker adictivo. Simple de aprender, imposible de dejar",
                "imagen": "balatro",
                "tags": ["Roguelike", "Cartas", "Estrategia", "Indie"],
                "fuente": "Steam/GOG"
            },
            {
                "id": 41,
                "nombre": "Hollow Knight",
                "plataforma": "Steam, GOG, Consolas",
                "rating": 9.7,
                "precio": 14.99,
                "desarrollador": "Team Cherry",
                "año": 2017,
                "descripcion": "Metroidvania perfecto. Hallownest espera con 50+ horas de contenido",
                "imagen": "hollow-knight",
                "tags": ["Metroidvania", "Plataformas", "Difícil", "Indie"],
                "fuente": "Steam/GOG"
            },
            {
                "id": 42,
                "nombre": "Celeste",
                "plataforma": "Steam, Epic Games, itch.io, Consolas",
                "rating": 9.5,
                "precio": 19.99,
                "desarrollador": "Extremely OK Games",
                "año": 2018,
                "descripcion": "Plataformas de precisión con mensaje profundo sobre salud mental",
                "imagen": "celeste",
                "tags": ["Plataformas", "Difícil", "Narrativo", "Indie"],
                "fuente": "itch.io/Steam"
            },
            {
                "id": 43,
                "nombre": "Cult of the Lamb",
                "plataforma": "Steam, GOG, Consolas",
                "rating": 9.0,
                "precio": 24.99,
                "desarrollador": "Massive Monster",
                "año": 2022,
                "descripcion": "Gestiona tu culto y lucha en mazmorras. Estilo adorable, gameplay profundo",
                "imagen": "cult-of-the-lamb",
                "tags": ["Roguelike", "Gestión", "Acción", "Indie"],
                "fuente": "GOG/Steam"
            },
            {
                "id": 44,
                "nombre": "Stardew Valley",
                "plataforma": "Steam, GOG, itch.io, Consolas, Móvil",
                "rating": 9.8,
                "precio": 14.99,
                "desarrollador": "ConcernedApe",
                "año": 2016,
                "descripcion": "El simulador de granja definitivo. Relajante, profundo y adictivo",
                "imagen": "stardew-valley",
                "tags": ["Simulación", "Granja", "Relajante", "Indie"],
                "fuente": "Steam/GOG/itch.io"
            },
            {
                "id": 45,
                "nombre": "Undertale",
                "plataforma": "Steam, GOG, itch.io, Consolas",
                "rating": 9.6,
                "precio": 9.99,
                "desarrollador": "Toby Fox",
                "año": 2015,
                "descripcion": "RPG donde nadie tiene que morir. Revolucionó la narrativa indie",
                "imagen": "undertale",
                "tags": ["RPG", "Narrativo", "Retro", "Indie"],
                "fuente": "itch.io/Steam"
            },
            {
                "id": 46,
                "nombre": "Vampire Survivors",
                "plataforma": "Steam, itch.io, Móvil",
                "rating": 9.4,
                "precio": 4.99,
                "desarrollador": "poncle",
                "año": 2022,
                "descripcion": "Bullet heaven adictivo. Sobrevive 30 minutos contra hordas infinitas",
                "imagen": "vampire-survivors",
                "tags": ["Roguelike", "Acción", "Indie", "Casual"],
                "fuente": "Steam/itch.io"
            }
        ],

        # ═══════════════════════════════════════════════════════════════════════
        # 🎯 SIMULACIÓN - Los mejores simuladores
        # ═══════════════════════════════════════════════════════════════════════
        "simulacion": [
            {
                "id": 47,
                "nombre": "Microsoft Flight Simulator 2024",
                "plataforma": "Steam, Xbox",
                "rating": 8.8,
                "precio": 69.99,
                "desarrollador": "Asobo Studio",
                "año": 2024,
                "descripcion": "El simulador de vuelo más realista. El mundo entero a escala 1:1",
                "imagen": "msfs-2024",
                "tags": ["Simulación", "Vuelo", "Realista", "Mundo Abierto"],
                "fuente": "Steam"
            },
            {
                "id": 48,
                "nombre": "Cities: Skylines II",
                "plataforma": "Steam, Xbox Game Pass",
                "rating": 7.8,
                "precio": 49.99,
                "desarrollador": "Colossal Order",
                "año": 2023,
                "descripcion": "City builder definitivo con escala masiva y simulación profunda",
                "imagen": "cities-skylines-2",
                "tags": ["Simulación", "City Builder", "Gestión", "Sandbox"],
                "fuente": "Steam"
            },
            {
                "id": 49,
                "nombre": "Euro Truck Simulator 2",
                "plataforma": "Steam",
                "rating": 9.5,
                "precio": 19.99,
                "desarrollador": "SCS Software",
                "año": 2012,
                "descripcion": "Conduce camiones por Europa. Sorprendentemente relajante y adictivo",
                "imagen": "ets2",
                "tags": ["Simulación", "Conducción", "Relajante", "Multijugador"],
                "fuente": "Steam"
            },
            {
                "id": 50,
                "nombre": "No Man's Sky",
                "plataforma": "Steam, GOG, Consolas",
                "rating": 9.0,
                "precio": 59.99,
                "desarrollador": "Hello Games",
                "año": 2016,
                "descripcion": "De desastre a obra maestra. Exploración espacial infinita, ahora increíble",
                "imagen": "no-mans-sky",
                "tags": ["Simulación", "Exploración", "Supervivencia", "Espacio"],
                "fuente": "GOG/Steam"
            },
            {
                "id": 51,
                "nombre": "Planet Zoo",
                "plataforma": "Steam",
                "rating": 8.9,
                "precio": 44.99,
                "desarrollador": "Frontier Developments",
                "año": 2019,
                "descripcion": "Construye y gestiona el zoo de tus sueños con animales realistas",
                "imagen": "planet-zoo",
                "tags": ["Simulación", "Gestión", "Animales", "Sandbox"],
                "fuente": "Steam"
            }
        ],

        # ═══════════════════════════════════════════════════════════════════════
        # ⚽ DEPORTES Y CARRERAS - Competición virtual
        # ═══════════════════════════════════════════════════════════════════════
        "deportes": [
            {
                "id": 52,
                "nombre": "EA Sports FC 25",
                "plataforma": "Steam, EA App, Consolas",
                "rating": 7.5,
                "precio": 69.99,
                "desarrollador": "EA Sports",
                "año": 2024,
                "descripcion": "El sucesor de FIFA con FC IQ y nuevas mecánicas tácticas",
                "imagen": "fc-25",
                "tags": ["Deportes", "Fútbol", "Multijugador", "Competitivo"],
                "fuente": "Steam"
            },
            {
                "id": 53,
                "nombre": "F1 24",
                "plataforma": "Steam, EA App, Consolas",
                "rating": 8.2,
                "precio": 69.99,
                "desarrollador": "Codemasters",
                "año": 2024,
                "descripcion": "La temporada oficial de F1 con handling mejorado y modo carrera",
                "imagen": "f1-24",
                "tags": ["Deportes", "Carreras", "Simulación", "Competitivo"],
                "fuente": "Steam"
            },
            {
                "id": 54,
                "nombre": "Forza Horizon 5",
                "plataforma": "Steam, Xbox",
                "rating": 9.2,
                "precio": 59.99,
                "desarrollador": "Playground Games",
                "año": 2021,
                "descripcion": "Racing arcade perfecto en México. Gráficos espectaculares y diversión pura",
                "imagen": "forza-horizon-5",
                "tags": ["Carreras", "Arcade", "Mundo Abierto", "Multijugador"],
                "fuente": "Steam"
            },
            {
                "id": 55,
                "nombre": "Gran Turismo 7",
                "plataforma": "PlayStation, Steam (próximamente)",
                "rating": 8.8,
                "precio": 69.99,
                "desarrollador": "Polyphony Digital",
                "año": 2022,
                "descripcion": "El simulador de conducción real. Coches reales, física realista",
                "imagen": "gt7",
                "tags": ["Carreras", "Simulación", "Realista", "Competitivo"],
                "fuente": "PlayStation"
            },
            {
                "id": 56,
                "nombre": "NBA 2K25",
                "plataforma": "Steam, Consolas",
                "rating": 7.8,
                "precio": 69.99,
                "desarrollador": "Visual Concepts",
                "año": 2024,
                "descripcion": "El simulador de basketball más completo con MyCareer renovado",
                "imagen": "nba-2k25",
                "tags": ["Deportes", "Basketball", "Simulación", "Competitivo"],
                "fuente": "Steam"
            }
        ],

        # ═══════════════════════════════════════════════════════════════════════
        # 🧩 PUZZLE - Desafía tu mente
        # ═══════════════════════════════════════════════════════════════════════
        "puzzle": [
            {
                "id": 57,
                "nombre": "Portal 2",
                "plataforma": "Steam, Consolas",
                "rating": 9.8,
                "precio": 9.99,
                "desarrollador": "Valve",
                "año": 2011,
                "descripcion": "El puzzle game perfecto. GLaDOS, portales y humor inolvidable",
                "imagen": "portal-2",
                "tags": ["Puzzle", "Primera Persona", "Cooperativo", "Humor"],
                "fuente": "Steam"
            },
            {
                "id": 58,
                "nombre": "The Talos Principle 2",
                "plataforma": "Steam, Consolas",
                "rating": 9.1,
                "precio": 29.99,
                "desarrollador": "Croteam",
                "año": 2023,
                "descripcion": "Puzzles filosóficos en un mundo post-humano. Secuela superior",
                "imagen": "talos-principle-2",
                "tags": ["Puzzle", "Filosofía", "Primera Persona", "Narrativo"],
                "fuente": "Steam"
            },
            {
                "id": 59,
                "nombre": "Baba Is You",
                "plataforma": "Steam, itch.io, Consolas",
                "rating": 9.4,
                "precio": 14.99,
                "desarrollador": "Hempuli",
                "año": 2019,
                "descripcion": "Puzzle donde cambias las reglas del juego. Genio puro del diseño",
                "imagen": "baba-is-you",
                "tags": ["Puzzle", "Lógica", "Indie", "Innovador"],
                "fuente": "Steam/itch.io"
            },
            {
                "id": 60,
                "nombre": "Return of the Obra Dinn",
                "plataforma": "Steam, GOG, Consolas",
                "rating": 9.3,
                "precio": 19.99,
                "desarrollador": "Lucas Pope",
                "año": 2018,
                "descripcion": "Detective en barco fantasma. Estilo visual único, lógica brillante",
                "imagen": "obra-dinn",
                "tags": ["Puzzle", "Detective", "Indie", "Narrativo"],
                "fuente": "Steam/GOG"
            }
        ],

        # ═══════════════════════════════════════════════════════════════════════
        # 🌐 MULTIJUGADOR/LIVE SERVICE - Juegos para jugar con amigos
        # ═══════════════════════════════════════════════════════════════════════
        "multijugador": [
            {
                "id": 61,
                "nombre": "Fortnite",
                "plataforma": "Epic Games, Consolas, Móvil",
                "rating": 8.5,
                "precio": 0,
                "desarrollador": "Epic Games",
                "año": 2017,
                "descripcion": "El battle royale que definió una generación. Siempre evolucionando",
                "imagen": "fortnite",
                "tags": ["Battle Royale", "Shooter", "Free-to-Play", "Multijugador"],
                "fuente": "Epic Games"
            },
            {
                "id": 62,
                "nombre": "Genshin Impact",
                "plataforma": "PC, PlayStation, Móvil",
                "rating": 8.7,
                "precio": 0,
                "desarrollador": "miHoYo/HoYoverse",
                "año": 2020,
                "descripcion": "Action RPG gacha con mundo abierto espectacular y actualizaciones constantes",
                "imagen": "genshin-impact",
                "tags": ["RPG", "Gacha", "Mundo Abierto", "Free-to-Play"],
                "fuente": "Epic Games"
            },
            {
                "id": 63,
                "nombre": "Helldivers 2",
                "plataforma": "Steam, PlayStation 5",
                "rating": 8.8,
                "precio": 39.99,
                "desarrollador": "Arrowhead Game Studios",
                "año": 2024,
                "descripcion": "Shooter cooperativo con humor satírico. Por la Súper Tierra!",
                "imagen": "helldivers-2",
                "tags": ["Shooter", "Cooperativo", "Acción", "Humor"],
                "fuente": "Steam"
            },
            {
                "id": 64,
                "nombre": "Deep Rock Galactic",
                "plataforma": "Steam, Xbox",
                "rating": 9.4,
                "precio": 29.99,
                "desarrollador": "Ghost Ship Games",
                "año": 2020,
                "descripcion": "Enanos espaciales mineros. Cooperativo perfecto. ROCK AND STONE!",
                "imagen": "deep-rock-galactic",
                "tags": ["Cooperativo", "Shooter", "Indie", "Procedural"],
                "fuente": "Steam"
            },
            {
                "id": 65,
                "nombre": "Sea of Thieves",
                "plataforma": "Steam, Xbox",
                "rating": 8.6,
                "precio": 39.99,
                "desarrollador": "Rare",
                "año": 2018,
                "descripcion": "Aventuras piratas con amigos. Batallas navales y tesoros",
                "imagen": "sea-of-thieves",
                "tags": ["Aventura", "Piratas", "Cooperativo", "Mundo Abierto"],
                "fuente": "Steam"
            }
        ],

        # ═══════════════════════════════════════════════════════════════════════
        # 🆓 FREE TO PLAY - Los mejores juegos gratuitos
        # ═══════════════════════════════════════════════════════════════════════
        "gratis": [
            {
                "id": 66,
                "nombre": "Path of Exile 2 (Early Access)",
                "plataforma": "Steam, Consolas",
                "rating": 9.0,
                "precio": 0,
                "desarrollador": "Grinding Gear Games",
                "año": 2024,
                "descripcion": "El ARPG más profundo se reinventa. Endgame infinito y builds ilimitados",
                "imagen": "poe2",
                "tags": ["ARPG", "Loot", "Difícil", "Free-to-Play"],
                "fuente": "Steam"
            },
            {
                "id": 67,
                "nombre": "Warframe",
                "plataforma": "Steam, Consolas",
                "rating": 9.1,
                "precio": 0,
                "desarrollador": "Digital Extremes",
                "año": 2013,
                "descripcion": "Space ninjas con contenido infinito. El F2P más generoso",
                "imagen": "warframe",
                "tags": ["Acción", "Looter", "Cooperativo", "Free-to-Play"],
                "fuente": "Steam"
            },
            {
                "id": 68,
                "nombre": "League of Legends",
                "plataforma": "Riot Games",
                "rating": 8.5,
                "precio": 0,
                "desarrollador": "Riot Games",
                "año": 2009,
                "descripcion": "El MOBA más jugado del mundo. E-Sports legendario",
                "imagen": "lol",
                "tags": ["MOBA", "Estrategia", "Competitivo", "Free-to-Play"],
                "fuente": "Riot Games"
            },
            {
                "id": 69,
                "nombre": "Apex Legends",
                "plataforma": "Steam, Origin, Consolas",
                "rating": 8.4,
                "precio": 0,
                "desarrollador": "Respawn Entertainment",
                "año": 2019,
                "descripcion": "Battle royale con movimiento fluido y habilidades únicas",
                "imagen": "apex-legends",
                "tags": ["Battle Royale", "FPS", "Competitivo", "Free-to-Play"],
                "fuente": "Steam"
            },
            {
                "id": 70,
                "nombre": "Dota 2",
                "plataforma": "Steam",
                "rating": 9.0,
                "precio": 0,
                "desarrollador": "Valve",
                "año": 2013,
                "descripcion": "MOBA hardcore con la curva de aprendizaje más profunda",
                "imagen": "dota2",
                "tags": ["MOBA", "Estrategia", "Competitivo", "Free-to-Play"],
                "fuente": "Steam"
            }
        ]
    }

    return jsonify(ok=True, mejores_juegos=mejores_juegos, total_categorias=len(mejores_juegos), actualizado="Diciembre 2025"), 200


@app.route("/api/mejores-juegos/<categoria>")
def api_mejores_juegos_por_categoria(categoria: str):
    """API: Mejores videojuegos de una categoría específica."""
    # Obtener todos los juegos
    respuesta = api_mejores_juegos()
    datos = respuesta[0].get_json()
    
    categoria_lower = categoria.lower()
    
    if categoria_lower not in datos.get("mejores_juegos", {}):
        return jsonify(
            ok=False, 
            error=f"Categoría '{categoria}' no encontrada",
            categorias_disponibles=list(datos.get("mejores_juegos", {}).keys())
        ), 404
    
    juegos = datos["mejores_juegos"][categoria_lower]
    return jsonify(
        ok=True, 
        categoria=categoria_lower,
        total=len(juegos),
        juegos=juegos
    ), 200


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
#  SECCION 5 >> CRUD VIDEOJUEGOS (Storage en memoria)
# =========================================================================================
# * Almacenamiento en memoria (se pierde al reiniciar)
# TODO: En produccion, usar una base de datos real (SQLite, PostgreSQL, etc.)

videojuegos_storage: Dict[int, Dict[str, Any]] = {}
videojuego_contador = 0

# * Almacenamiento de amigos
amigos_storage: Dict[int, Dict[str, Any]] = {}
amigo_contador = 0


@app.route("/videojuegos", methods=["POST"])
def agregar_videojuego():
    """Agregar un nuevo videojuego (CREATE)."""
    nombre_juego = (request.form.get("nombre_juego") or "").strip()
    genero = (request.form.get("genero") or "").strip()
    comprador = (request.form.get("comprador") or "").strip()
    precio = request.form.get("precio", "0")
    descripcion = (request.form.get("descripcion") or "").strip()
    tiene_a2f = request.form.get("tiene_a2f") == "on"

    # Convertir precio a float
    try:
        precio = float(precio)
    except ValueError:
        precio = 0.0

    if not nombre_juego or not genero or not comprador:
        return redirect(request.referrer or url_for("inicio"))

    global videojuego_contador
    videojuego_contador += 1

    videojuegos_storage[videojuego_contador] = {
        "id": videojuego_contador,
        "nombre": nombre_juego,
        "genero": genero,
        "comprador": comprador,
        "precio": precio,
        "descripcion": descripcion,
        "tiene_a2f": tiene_a2f,
        "compartido_con": []
    }

    return redirect(request.referrer or url_for("inicio"))


@app.route("/api/videojuegos", methods=["GET"])
def api_videojuegos():
    """Obtener todos los videojuegos (READ)."""
    videos_list = list(videojuegos_storage.values())
    return jsonify(ok=True, videojuegos=videos_list)


@app.route("/api/videojuegos/compartir", methods=["POST"])
def compartir_videojuego():
    """Compartir un videojuego con un amigo o familiar (UPDATE)."""
    data = request.get_json(silent=True) or {}
    jid = data.get("id")
    amigo = (data.get("amigo") or "").strip()
    tipo_relacion = data.get("tipo_relacion", "amigo")

    if not jid or not amigo:
        return jsonify(ok=False, error="ID o amigo invalido"), 400

    if jid not in videojuegos_storage:
        return jsonify(ok=False, error="Videojuego no encontrado"), 404

    # Guardar con el tipo de relación
    compartido_info = {"nombre": amigo, "tipo": tipo_relacion}
    
    # Verificar si ya está compartido
    compartidos = videojuegos_storage[jid]["compartido_con"]
    ya_existe = any(c.get("nombre") == amigo if isinstance(c, dict) else c == amigo for c in compartidos)
    
    if not ya_existe:
        videojuegos_storage[jid]["compartido_con"].append(compartido_info)

    return jsonify(ok=True, mensaje=f"Compartido con {amigo} ({tipo_relacion})")


@app.route("/api/videojuegos/<int:vid>", methods=["PUT"])
def actualizar_videojuego(vid: int):
    """Actualizar un videojuego (UPDATE)."""
    if vid not in videojuegos_storage:
        return jsonify(ok=False, error="Videojuego no encontrado"), 404

    data = request.get_json(silent=True) or {}
    
    # Actualizar campos
    if "nombre" in data:
        videojuegos_storage[vid]["nombre"] = (data.get("nombre") or "").strip()
    if "genero" in data:
        videojuegos_storage[vid]["genero"] = (data.get("genero") or "").strip()
    if "comprador" in data:
        videojuegos_storage[vid]["comprador"] = (data.get("comprador") or "").strip()
    if "precio" in data:
        try:
            videojuegos_storage[vid]["precio"] = float(data.get("precio", 0))
        except (ValueError, TypeError):
            videojuegos_storage[vid]["precio"] = 0.0
    if "descripcion" in data:
        videojuegos_storage[vid]["descripcion"] = (data.get("descripcion") or "").strip()
    if "tiene_a2f" in data:
        videojuegos_storage[vid]["tiene_a2f"] = bool(data.get("tiene_a2f"))

    return jsonify(ok=True, mensaje="Videojuego actualizado", videojuego=videojuegos_storage[vid])


@app.route("/api/videojuegos/<int:vid>", methods=["DELETE"])
def eliminar_videojuego(vid: int):
    """Eliminar un videojuego (DELETE)."""
    if vid not in videojuegos_storage:
        return jsonify(ok=False, error="Videojuego no encontrado"), 404

    del videojuegos_storage[vid]
    return jsonify(ok=True, mensaje="Videojuego eliminado")


# =========================================================================================
#  SECCION 5.1 >> CRUD AMIGOS
# =========================================================================================

@app.route("/amigos", methods=["POST"])
def agregar_amigo():
    """Agregar un nuevo amigo (CREATE)."""
    nombre = (request.form.get("nombre_amigo") or "").strip()
    email = (request.form.get("email_amigo") or "").strip()
    plataforma = (request.form.get("plataforma") or "").strip()
    
    if not nombre:
        return redirect(request.referrer or url_for("inicio"))

    global amigo_contador
    amigo_contador += 1

    amigos_storage[amigo_contador] = {
        "id": amigo_contador,
        "nombre": nombre,
        "email": email,
        "plataforma": plataforma,
        "estado": "desconectado",
        "ultimo_acceso": "Nunca"
    }

    return redirect(request.referrer or url_for("inicio"))


@app.route("/api/amigos", methods=["GET"])
def api_amigos():
    """Obtener todos los amigos (READ)."""
    amigos_list = list(amigos_storage.values())
    return jsonify(ok=True, amigos=amigos_list)


@app.route("/api/amigos/<int:aid>/estado", methods=["POST"])
def cambiar_estado_amigo(aid: int):
    """Cambiar estado de conexión del amigo (UPDATE)."""
    if aid not in amigos_storage:
        return jsonify(ok=False, error="Amigo no encontrado"), 404
    
    data = request.get_json(silent=True) or {}
    nuevo_estado = data.get("estado", "desconectado")
    
    # Validar estados válidos
    estados_validos = ["conectado", "ausente", "desconectado", "inactivo"]
    if nuevo_estado not in estados_validos:
        nuevo_estado = "desconectado"
    
    amigos_storage[aid]["estado"] = nuevo_estado
    if nuevo_estado == "conectado":
        from datetime import datetime
        amigos_storage[aid]["ultimo_acceso"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    return jsonify(ok=True, mensaje=f"Estado cambiado a {nuevo_estado}")


@app.route("/api/amigos/<int:aid>", methods=["DELETE"])
def eliminar_amigo(aid: int):
    """Eliminar un amigo (DELETE)."""
    if aid not in amigos_storage:
        return jsonify(ok=False, error="Amigo no encontrado"), 404

    del amigos_storage[aid]
    return jsonify(ok=True, mensaje="Amigo eliminado")


# =========================================================================================
#  SECCION 6 >> Laboratorio IA (disena tu propia ruta)
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
