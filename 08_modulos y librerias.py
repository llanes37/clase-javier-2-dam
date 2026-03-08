# =========================================================================================
#  🐍 PYTHON CLASE 8 — MÓDULOS Y LIBRERÍAS
#  ────────────────────────────────────────────────────────────────────────────────────────
#  📘 En esta clase practicarás:
#    * import básicos: alias (as), from ... import ..., dir(), __name__
#    * Módulos estándar MUY útiles: math, random, datetime, pathlib, json
#    * Archivos de texto con Path y serialización JSON
#    * Crear y usar tu propio módulo (auto-generado si no existe)
#    * (Opcional) Librerías externas (pip): ejemplo con requests (si está instalada)
#    * Laboratorio IA y Autoevaluación final
#
#  🎨 Better Comments:
#    # ! importante   ·  # * definición/foco   ·  # ? idea/nota
#    # TODO: práctica  ·  # NOTE: apunte útil   ·  # // deprecado
# =========================================================================================

from typing import Any, Callable, Dict, List
import sys

# * Configuración general ---------------------------------------------------------------
RUN_INTERACTIVE = True   # True: pedir datos al usuario; False: usar valores por defecto
PAUSE = False            # Pausa tras cada opción del menú
IA_DEMO = True           # Demo corta en Laboratorio IA

# * Firma del curso ----------------------------------------------------------------------
def print_firma():
    print("\n" + "=" * 80)
    print("Autor: joaquin  |  Página web: https://clasesonlinejoaquin.es/")
    print("=" * 80 + "\n")

# * Utilidades comunes -------------------------------------------------------------------
def pause(msg="Pulsa Enter para continuar..."):
    if not PAUSE:
        return
    try:
        input(msg)
    except EOFError:
        pass

def safe_input(prompt: str, caster: Callable[[str], Any], default: Any) -> Any:
    """# * Convierte la entrada al tipo deseado; si falla o no hay input, devuelve 'default'."""
    if not RUN_INTERACTIVE:
        return default
    try:
        raw = input(prompt)
        if raw.strip() == "":
            return default
        return caster(raw)
    except (ValueError, EOFError):
        print("! Entrada no válida; usando valor por defecto.")
        return default

def encabezado(titulo: str):
    print("\n" + "=" * 80)
    print(titulo)
    print("=" * 80)

# =========================================================================================
#  SECCIÓN 1 · import, alias y from ... import ...
# =========================================================================================
def seccion_1():
    encabezado("SECCIÓN 1 · import, alias y from ... import ...")

    # * TEORÍA
    # import modulo                → usa modulo.func()
    # import modulo as m           → alias: m.func()
    # from modulo import nombre    → usa nombre() directo
    # dir(modulo)                  → lista de símbolos del módulo
    # __name__                     → nombre del módulo actual (en script principal es "__main__")

    # * DEMO
    import math as m
    from math import sqrt

    print("pi:", m.pi)
    print("sqrt(16):", sqrt(16))
    print("__name__ de este archivo:", __name__)
    print("Símbolos de math (recortado):", [x for x in dir(m) if not x.startswith("_")][:8], "...")

    # TODO: (Tema: ÁREA DE CÍRCULO)
    # Pide/captura un radio (float, por defecto 3.0) y calcula el área usando math.pi.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # r = safe_input("Radio: ", float, default=3.0)
    # area = m.pi * (r ** 2)
    # print(f"Área: {area:.2f}")

# =========================================================================================
#  SECCIÓN 2 · math y random (utilidades numéricas y aleatorias)
# =========================================================================================
def seccion_2():
    encabezado("SECCIÓN 2 · math y random")

    # * TEORÍA
    # math: ceil, floor, sqrt, pow, factorial, pi, e...
    # random: randint(a,b), random(), choice(seq), shuffle(lista), sample(seq, k)

    # * DEMO
    import math, random

    print("ceil(2.1) →", math.ceil(2.1), "| floor(2.9) →", math.floor(2.9))
    numeros = list(range(1, 11))
    random.shuffle(numeros)
    print("Números mezclados:", numeros)
    print("Un número al azar 1..100:", random.randint(1, 100))
    print("Muestra de 3:", random.sample(numeros, 3))

    # TODO: (Tema: LOTE ALEATORIO)
    # Genera 5 enteros aleatorios 1..50 y muestra: lista, mínimo, máximo y media (sum/len).
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # import random
    # lote = [random.randint(1, 50) for _ in range(5)]
    # print(lote, min(lote), max(lote), sum(lote)/len(lote))

# =========================================================================================
#  SECCIÓN 3 · datetime (fechas y horas)
# =========================================================================================
def seccion_3():
    encabezado("SECCIÓN 3 · datetime (fechas y horas)")

    # * TEORÍA
    # datetime.now(), date.today(), timedelta(días/horas), strftime() para formatear,
    # datetime.strptime(cadena, formato) para parsear texto → fecha.

    # * DEMO
    from datetime import datetime, timedelta

    ahora = datetime.now()
    print("Ahora:", ahora.strftime("%Y-%m-%d %H:%M:%S"))
    fin_anio = datetime(ahora.year, 12, 31)
    faltan = (fin_anio - ahora).days
    print(f"Días hasta fin de año: {faltan}")

    # Parsear una fecha de entrada
    fecha_txt = safe_input("Fecha objetivo (YYYY-MM-DD): ", str, default="2025-12-31")
    try:
        objetivo = datetime.strptime(fecha_txt, "%Y-%m-%d")
        print("Objetivo:", objetivo.strftime("%A %d %B %Y"))
        print("Faltan días:", (objetivo - ahora).days)
    except ValueError as e:
        print("Formato inválido. Usa YYYY-MM-DD")

    # TODO: (Tema: RECORDATORIO)
    # Pide una fecha (YYYY-MM-DD) y horas (int). Suma con timedelta y muestra la fecha/hora final formateada.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

# =========================================================================================
#  SECCIÓN 4 · pathlib + archivos de texto (leer/escribir)
# =========================================================================================
def seccion_4():
    encabezado("SECCIÓN 4 · pathlib + archivos de texto")

    # * TEORÍA
    # Path.cwd(), Path("ruta"), .exists(), .read_text(), .write_text(), .read_bytes(), .write_bytes()
    # Para añadir varias líneas: "\n".join(lista)

    from pathlib import Path

    carpeta = Path.cwd()
    fichero = carpeta / "demo_modulos.txt"

    # * DEMO: escribir y leer
    lineas = ["Primera línea", "Segunda línea", "Tercera línea"]
    fichero.write_text("\n".join(lineas), encoding="utf-8")
    contenido = fichero.read_text(encoding="utf-8")
    print("Escrito en:", fichero)
    print("Contenido leído:")
    print(contenido)
    print("Tamaño (bytes):", fichero.stat().st_size)

    # TODO: (Tema: TAREAS A ARCHIVO)
    # 1) Pide/captura 3 tareas (o usa por defecto una lista) y escríbelas en 'tareas.txt' (una por línea).
    # 2) Léelas y muéstralas numeradas.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # tareas = ["pagar", "estudiar", "entrenar"]
    # path_t = Path("tareas.txt")
    # path_t.write_text("\n".join(tareas), encoding="utf-8")
    # for i, linea in enumerate(path_t.read_text(encoding="utf-8").splitlines(), start=1):
    #     print(f"{i}. {linea}")

# =========================================================================================
#  SECCIÓN 5 · json (serializar y deserializar)
# =========================================================================================
def seccion_5():
    encabezado("SECCIÓN 5 · json (serializar y deserializar)")

    # * TEORÍA
    # json.dump(obj, archivo) / json.load(archivo)
    # json.dumps(obj) / json.loads(cadena)
    # Tip: indent=2 para que quede legible, ensure_ascii=False para acentos.

    import json
    from pathlib import Path

    perfil = {"nombre": "Lucía", "edad": 20, "premium": True}
    Path("perfil.json").write_text(
        json.dumps(perfil, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    # Leerlo de nuevo:
    cargado = json.loads(Path("perfil.json").read_text(encoding="utf-8"))
    print("Perfil JSON →", cargado)

    # TODO: (Tema: PRODUCTOS JSON)
    # Crea una lista de dicts con nombre y precio, guárdala en 'productos.json' y vuelve a leerla.
    # Muestra el total de precios.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

# =========================================================================================
#  SECCIÓN 6 · Tu propio módulo (auto-creado si no existe)
# =========================================================================================
def seccion_6():
    encabezado("SECCIÓN 6 · Tu propio módulo")

    # * TEORÍA
    # Un módulo no es más que un .py con funciones/constantes/clases.
    # Estructura básica:
    #   # utilidades_demo.py
    #   def suma(a,b): return a+b
    #   if __name__ == '__main__':   # código solo si se ejecuta directamente
    #       ... pruebas ...

    import importlib.util
    from pathlib import Path

    nombre_mod = "utilidades_demo.py"
    path_mod = Path(nombre_mod)

    if not path_mod.exists():
        path_mod.write_text(
            '''"""
# * utilidades_demo — módulo de ejemplo
"""
PI = 3.14159

def suma(a: float, b: float) -> float:
    return a + b

def es_par(n: int) -> bool:
    return n % 2 == 0

def area_circulo(r: float) -> float:
    return PI * (r ** 2)

if __name__ == "__main__":
    # Pruebas rápidas si se ejecuta directamente
    print("suma(2,3)=", suma(2,3))
    print("es_par(4)=", es_par(4))
    print("area_circulo(3)=", area_circulo(3))
''',
            encoding="utf-8"
        )
        print("Módulo 'utilidades_demo.py' creado.")

    # Importarlo y usarlo:
    import utilidades_demo as util
    print("util.PI →", util.PI)
    print("util.suma(2,5) →", util.suma(2, 5))
    print("util.es_par(7) →", util.es_par(7))
    print("util.area_circulo(4) →", util.area_circulo(4))

    # TODO: (Tema: EXTENDER MÓDULO)
    # Abre 'utilidades_demo.py' y añade una función doble(n) que devuelva n*2.
    # Reimporta el módulo (usa importlib.reload) y pruébala.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # import importlib, utilidades_demo
    # importlib.reload(utilidades_demo)
    # print(utilidades_demo.doble(10))

# =========================================================================================
#  SECCIÓN 7 · Librerías externas (pip) [opcional y protegido]
# =========================================================================================
def seccion_7():
    encabezado("SECCIÓN 7 · Librerías externas (pip) [opcional]")

    # * TEORÍA
    # Instalación (en terminal):
    #   pip install <paquete>
    # Importar en tu script:
    #   import paquete   ·  import paquete as alias   ·  from paquete import nombre
    # Ejemplo popular: requests (peticiones HTTP), pandas (datos), numpy (numérico).

    # * DEMO segura (no obligamos a tener conexión ni el paquete instalado)
    try:
        import requests
        print("requests instalado. Versión:", requests.__version__)
        print("Ejemplo de uso (comentado):")
        print("  resp = requests.get('https://api.github.com')  → resp.status_code, resp.json()")
    except Exception:
        print("requests NO está instalado. Prueba en tu entorno: pip install requests")

    # TODO: (Tema: PRUEBA CON EXTERNA)
    # Si tienes requests instalado, haz un GET a 'https://httpbin.org/get'
    # y muestra el 'origin' y las cabeceras 'headers'. Protege con try/except.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

# =========================================================================================
#  SECCIÓN 8 · Laboratorio IA (herramienta con módulos)
# =========================================================================================
def seccion_8_ia():
    encabezado("SECCIÓN 8 · Laboratorio IA (módulos creativos)")

    # * PROMPT KIT (copia/pega en ChatGPT)
    # 1) PROMPT BREVE:
    #    "Eres profesor de Python. Genera un programa de 35–50 líneas que use:
    #     - datetime para sellos de tiempo
    #     - pathlib para guardar en un archivo .txt o .json
    #     - json para serializar un pequeño historial
    #     - random para simular datos
    #     Tema: 'registro de hábitos' o 'simulador de ventas'. Solo código Python."
    #
    # 2) PROMPT ALTERNATIVO:
    #    "Crea una herramienta 'agenda de tareas' que guarde y cargue un JSON con fechas
    #     (datetime → strftime). Incluye dos funciones utilitarias en un módulo aparte."
    #
    # 3) PROMPT DE MEJORA:
    #    "Refactoriza separando lectura/escritura en funciones y añadiendo validaciones y
    #     mensajes de error claros. Manténlo bajo 50 líneas."

    # * DEMO opcional
    if IA_DEMO:
        from datetime import datetime
        from pathlib import Path
        import json
        registro = [{"momento": datetime.now().strftime("%H:%M:%S"), "valor": 10}]
        Path("demo_registro.json").write_text(json.dumps(registro, indent=2), encoding="utf-8")
        print("Demo IA → 'demo_registro.json' creado con 1 entrada.")

    # TODO: (Tema: PROGRAMA PROPUESTO POR IA)
    # 1) Pide a ChatGPT el miniprograma con el PROMPT KIT.
    # 2) Pega el código debajo y ejecútalo desde el menú.
    # 3) Modifícalo a tu gusto.
    #
    # --- ZONA DEL ALUMNO ---------------------------------------------------------------
    # def mi_programa_ia():
    #     # pega aquí el código que te generó la IA
    #     pass
    # mi_programa_ia()

# =========================================================================================
#  AUTOEVALUACIÓN FINAL (mezcla de todo)
# =========================================================================================
def autoevaluacion():
    encabezado("AUTOEVALUACIÓN FINAL · Registro simple con JSON + fechas")

    # TODO: (ENUNCIADO)
    # Implementa un "registro de gastos" que:
    # 1) Pida/capture varios apuntes (fecha opcional → si no, usa datetime.now()) con: concepto (str), importe (float).
    # 2) Los guarde en 'gastos.json' usando json + pathlib (append seguro: carga si existe y añade).
    # 3) Al leer, muestre:
    #    - número de movimientos
    #    - total gastado
    #    - gasto medio
    #    - mayor gasto (concepto/importe)
    # 4) Línea final tipo dashboard:
    #    "Movs:<n> | Total:<€> | Medio:<€> | Mayor:<concepto-€>"
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

# =========================================================================================
#  MENÚ PRINCIPAL
# =========================================================================================
def menu():
    while True:
        print_firma()
        print("MENÚ · Elige una opción")
        print("  1) import/alias/from ... import")
        print("  2) math y random")
        print("  3) datetime")
        print("  4) pathlib + archivos")
        print("  5) json")
        print("  6) Tu propio módulo")
        print("  7) Librerías externas (pip) [opcional]")
        print("  8) Laboratorio IA (módulos)")
        print("  9) Autoevaluación final")
        print(" 10) Ejecutar TODO (1→9)")
        print("  0) Salir")

        try:
            op = int(input("Opción: "))
        except Exception:
            print("! Opción no válida.")
            continue

        if op == 0:
            print("¡Hasta la próxima!")
            print_firma()
            break
        elif op == 1: seccion_1(); pause()
        elif op == 2: seccion_2(); pause()
        elif op == 3: seccion_3(); pause()
        elif op == 4: seccion_4(); pause()
        elif op == 5: seccion_5(); pause()
        elif op == 6: seccion_6(); pause()
        elif op == 7: seccion_7(); pause()
        elif op == 8: seccion_8_ia(); pause()
        elif op == 9: autoevaluacion(); pause()
        elif op == 10:
            seccion_1(); seccion_2(); seccion_3(); seccion_4(); seccion_5(); seccion_6(); seccion_7(); seccion_8_ia(); autoevaluacion(); pause()
        else:
            print("! Elige una opción del 0 al 10.")

# =========================================================================================
#  EJECUCIÓN
# =========================================================================================
if __name__ == "__main__":
    menu()
