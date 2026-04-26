# =========================================================================================
#  🐍 PYTHON CLASE 1 — Variables, Entradas, Colecciones y Operadores (+ Laboratorio IA)
#  ────────────────────────────────────────────────────────────────────────────────────────
#  📘 En esta clase aprenderás:
#    * Qué es una variable y cómo mostrarla con f-strings.
#    * Cómo pedir datos al usuario de manera segura.
#    * Listas y diccionarios como colecciones esenciales.
#    * Operadores aritméticos, de comparación, lógicos y de asignación.
#    * Laboratorio IA: usar ChatGPT como compañero para crear un miniprograma con variables.
#    * Ejercicios prácticos en cada sección + una autoevaluación final.
#
#  🎨 Convención de comentarios (Better Comments):
#    # ! importante   ·  # * definición/foco   ·  # ? idea/nota
#    # TODO: práctica  ·  # NOTE: apunte útil   ·  # // deprecado
# =========================================================================================

from typing import Any, Callable

# * Configuración general ---------------------------------------------------------------
RUN_INTERACTIVE = True   # True: pedir datos al usuario; False: usar valores por defecto
PAUSE = False            # Pausa tras cada opción del menú
IA_DEMO = True           # Muestra una demo corta en Laboratorio IA (pon False si no quieres)

# * Utilidades --------------------------------------------------------------------------
def print_firma():
    print("\n" + "=" * 80)
    print("Autor: joaquin  |  Página web: https://clasesonlinejoaquin.es/")
    print("=" * 80 + "\n")

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
    print("\n" + "="*80)
    print(titulo)
    print("="*80)

# =========================================================================================
#  SECCIÓN 1 · VARIABLES BÁSICAS + f-strings
# =========================================================================================
def seccion_1():
    encabezado("SECCIÓN 1 · VARIABLES BÁSICAS + f-strings")

    # * TEORÍA
    # Una variable es un NOMBRE que guarda un DATO en memoria.
    # Python infiere el tipo automáticamente (str, int, float, bool…).
    # f-strings permiten mezclar variables dentro de cadenas: f"Hola {nombre}"

    # * DEMO
    nombre = "Alicia"
    edad = 19
    altura = 1.68
    activa = True
    print(f"Perfil → {nombre}, {edad} años, {altura} m, activa={activa}")

    # TODO: (Tema: PERFIL RÁPIDO)
    # Crea y muestra: usuario (str), ciudad (str), puntos (int), activo (bool).
    # Salida: "Usuario <usuario> de <ciudad> | Puntos: <puntos> | Activo: <activo>"
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

# =========================================================================================
#  SECCIÓN 2 · ENTRADA SEGURA (input) + mini-cálculos
# =========================================================================================
def seccion_2():
    encabezado("SECCIÓN 2 · Entrada segura (input) + mini-cálculos")

    # * TEORÍA
    # Usa input() para leer; convierte al tipo que necesites (int/float).
    # safe_input() da valores por defecto si no hay entrada o hay error.

    # * DEMO
    unidades = safe_input("¿Unidades? ", int, default=3)
    precio   = safe_input("¿Precio/ud? ", float, default=12.5)
    total    = unidades * precio
    print(f"Total compra → {total:.2f} €")

    # TODO: (Tema: CONVERSOR SENCILLO)
    # Pide kilómetros (float) y conviértelos a millas (1 km = 0.621371).
    # Muestra el resultado con 2 decimales.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 3 · LISTAS y DICCIONARIOS
# =========================================================================================
def seccion_3():
    encabezado("SECCIÓN 3 · Listas y Diccionarios")

    # * TEORÍA
    # Lista = colección ordenada y mutable (append, pop, slices).
    # Diccionario = pares clave:valor para representar datos con nombre.

    # * DEMO · LISTAS
    cursos = ["HTML", "CSS", "Python"]
    cursos.append("JavaScript")
    print(f"Cursos → {cursos} | Primero={cursos[0]} | Sublista[1:3]={cursos[1:3]}")

    # * DEMO · DICCIONARIOS
    alumno = {"nombre": "Lucía", "edad": 20, "premium": False}
    alumno["premium"] = True
    alumno["pais"] = "España"
    print(f"Alumno → {alumno}")

    # TODO: (Tema: AGENDA)
    # 1) Lista 'tareas' con 3 tareas (str). Añade 1 y muestra total, primera y última.
    # 2) Diccionario 'contacto' con: nombre, telefono, email. Actualiza telefono y añade 'ciudad'.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    tareas = ["Estudiar Python", "Hacer ejercicios", "Repasar apuntes"]
    tareas.append("Preparar examen")
    print(f"Tareas ({len(tareas)}) -> Primera: {tareas[0]} | �ltima: {tareas[-1]}")

    contacto = {
        "nombre": "Javier",
        "telefono": "600111222",
        "email": "javier@email.com",
    }
    contacto["telefono"] = "699888777"
    contacto["ciudad"] = "Madrid"
    print(f"Contacto -> {contacto}")


# =========================================================================================
#  SECCIÓN 4 · OPERADORES (aritméticos, comparación, lógicos y asignación)
# =========================================================================================
def seccion_4():
    encabezado("SECCIÓN 4 · Operadores")

    # * TEORÍA
    # Aritméticos: + - * / // % **
    # Comparación: > < >= <= == !=
    # Lógicos: and / or / not
    # Asignación compuesta: += -= *= /= //= %= **=

    # * DEMO
    print("Aritméticos:", 2+2, 10-3, 8*3, 30/6, 21%5, 21//5, 2**3)
    print("Comparaciones:", 5>6, 5<6, 8>=6, 5==5, "Ana" < "Pepe")
    print("Lógicos:", True and False, True or False, not True)
    x = 5; x += 3; x *= 2
    print("Asignaciones:", x)

    # TODO: (Tema: CALCULADORA MINI)
    # Pide dos números y muestra:
    # - todas las operaciones básicas (+, -, *, /, //, %, **)
    # - 3 comparaciones (>, <, ==) y una combinación lógica (ej: a>0 and b>0)
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

    a = safe_input("Primer n�mero: ", float, default=10)
    b = safe_input("Segundo n�mero: ", float, default=3)

    print("Operaciones:")
    print(f"{a} + {b} = {a + b}")
    print(f"{a} - {b} = {a - b}")
    print(f"{a} * {b} = {a * b}")
    print(f"{a} / {b} = {a / b}" if b != 0 else "Divisi�n: no se puede dividir entre 0")
    print(f"{a} // {b} = {a // b}" if b != 0 else "Divisi�n entera: no se puede dividir entre 0")
    print(f"{a} % {b} = {a % b}" if b != 0 else "M�dulo: no se puede dividir entre 0")
    print(f"{a} ** {b} = {a ** b}")

    print("Comparaciones:")
    print(f"{a} > {b} -> {a > b}")
    print(f"{a} < {b} -> {a < b}")
    print(f"{a} == {b} -> {a == b}")
    print(f"(a > 0 and b > 0) -> {a > 0 and b > 0}")

# =========================================================================================
#  SECCIÓN 5 · LABORATORIO IA (Variables creativas)
# =========================================================================================
def seccion_5_ia():
    encabezado("SECCIÓN 5 · Laboratorio IA (Variables creativas)")

    # * TEORÍA (guía de uso con IA)
    # ! Objetivo: usar ChatGPT para que te proponga un miniprograma (20–40 líneas)
    # ! que utilice variables, listas y operadores, y luego adaptarlo a tu gusto.
    #
    # * Cómo pedirlo (PROMPT KIT):
    #   1) PROMPT BREVE
    #      "Eres profesor de Python. Genera un programa de 30 líneas que use variables,
    #       listas y operadores. Tema: 'carrito de la compra sencillo' (sin librerías).
    #       Requisitos: nombres de variables en español, comentarios claros (# * / # TODO),
    #       sin clases ni funciones avanzadas. Devuélveme SOLO código Python."
    #
    #   2) PROMPT ALTERNATIVO
    #      "Crea un marcador de partido con variables, lista de anotaciones y
    #       operadores. Añade inputs opcionales (si no hay input, usa valores por defecto)."
    #
    #   3) PROMPT DE MEJORA
    #      "Mejora este código para que tenga 2 comprobaciones de errores y un resumen final
    #       formateado en 1 línea. Manténlo por debajo de 40 líneas."
    #
    # ? Consejos:
    #   - Pide SIEMPRE 'solo código Python' para poder pegarlo aquí sin limpiar.
    #   - Si falla algo, copia el error completo y pídele a la IA: “Arréglalo paso a paso”.

    # * DEMO opcional (apagable con IA_DEMO=False): marcador simple
    if IA_DEMO:
        equipo_a = "Rojo"
        equipo_b = "Azul"
        puntos_a = [2, 3, 1]     # lista de anotaciones
        puntos_b = [3, 2, 2]
        total_a = sum(puntos_a)  # operadores + función integrada
        total_b = sum(puntos_b)
        ganador = equipo_a if total_a > total_b else (equipo_b if total_b > total_a else "Empate")
        print(f"Marcador demo → {equipo_a}:{total_a}  vs  {equipo_b}:{total_b}  | Resultado: {ganador}")

    # TODO: (Tema: PROGRAMA PROPUESTO POR IA)
    # 1) Pídele a ChatGPT el miniprograma con el PROMPT KIT (elige tema).
    # 2) Copia el código que te devuelva y pégalo en la ZONA DEL ALUMNO (respeta la indentación).
    # 3) Ejecútalo desde el menú para probarlo y modifícalo a tu gusto.
    #
    # --- ZONA DEL ALUMNO — Pega aquí tu programa de la IA -------------------------------
    # Ejemplo de “envoltorio” por si quieres aislarlo:
    #
    # def mi_programa_ia():
    #     # pega aquí el código que te generó la IA (puedes usar safe_input si quieres)
    #     # ...
    #     pass
    #
    # mi_programa_ia()
    #
    # -------------------------------------------------------------------------------


# =========================================================================================
#  AUTOEVALUACIÓN FINAL (mezcla de todo)
# =========================================================================================
def autoevaluacion():
    encabezado("AUTOEVALUACIÓN FINAL · Proyecto Integrador")

    # TODO: (Tema: GESTOR PERSONAL)
    # 1) Variables: nombre_usuario (str), edad (int), ciudad (str), activo (bool).
    # 2) Entrada y cálculo: unidades (int), precio (float), total = unidades*precio.
    # 3) Lista 'tareas' (3 + añadir 1) y mostrar total, primera y última.
    # 4) Diccionario 'perfil' con nombre, edad, ciudad, activo, y añadir 'puntos'.
    # 5) Operadores: usar 2 números y mostrar suma, resta y comparación.
    # 6) Línea final resumen con f-string:
    #    "Usuario <nombre> | Tareas:<n> | Total compra:<importe> €"
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  MENÚ PRINCIPAL
# =========================================================================================
def menu():
    while True:
        print_firma()
        print("MENÚ · Elige una opción")
        print("  1) Variables básicas")
        print("  2) Entrada segura + cálculos")
        print("  3) Listas y Diccionarios")
        print("  4) Operadores")
        print("  5) Laboratorio IA (Variables creativas)")
        print("  6) Autoevaluación final")
        print("  7) Ejecutar TODO (1→6)")
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
        elif op == 5: seccion_5_ia(); pause()
        elif op == 6: autoevaluacion(); pause()
        elif op == 7:
            seccion_1(); seccion_2(); seccion_3(); seccion_4(); seccion_5_ia(); autoevaluacion(); pause()
        else:
            print("! Elige una opción del 0 al 7.")

# =========================================================================================
#  EJECUCIÓN
# =========================================================================================
if __name__ == "__main__":
    menu()
