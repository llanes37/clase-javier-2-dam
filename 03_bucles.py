# =========================================================================================
#  🐍 PYTHON CLASE 3 — BUCLES (for, while, range, enumerate, break/continue/else) + IA
#  ────────────────────────────────────────────────────────────────────────────────────────
#  📘 En esta clase practicarás:
#    * for básico sobre listas
#    * range() para secuencias numéricas
#    * enumerate() para índice + valor
#    * while con condición (y patrón anti-bucle-infinito)
#    * break, continue y for-else (bloque else tras recorrer sin break)
#    * Bucles anidados (tablas simples)
#    * (Opcional) Comprensiones de listas
#    * Laboratorio IA: miniprograma con bucles
#    * Autoevaluación final (mezcla de todo)
#
#  🎨 Better Comments:
#    # ! importante   ·  # * definición/foco   ·  # ? idea/nota
#    # TODO: práctica  ·  # NOTE: apunte útil   ·  # // deprecado
# =========================================================================================

from typing import Any, Callable

# * Configuración general ---------------------------------------------------------------
RUN_INTERACTIVE = True   # True: pedir datos al usuario; False: usar valores por defecto
PAUSE = False            # Pausa tras cada opción del menú
IA_DEMO = True           # Muestra una demo corta en el Laboratorio IA

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
#  SECCIÓN 1 · for básico (recorrer una lista)
# =========================================================================================
def seccion_1():
    encabezado("SECCIÓN 1 · for básico (recorrer una lista)")

    # * TEORÍA
    # for <elemento> in <colección>:
    #     <bloque>
    # Recorre cada elemento de la colección en orden.

    # * DEMO
    frutas = ["manzana", "plátano", "pera"]
    texto = "Frutas:"
    for f in frutas:
        texto += f" {f}"
    print(texto)

    # TODO: (Tema: NOMBRES)
    # Recorre una lista de nombres y muestra "Hola, <nombre>" para cada uno.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # nombres = ["Ana", "Luis", "María"]
    # for n in nombres:
    #     print(f"Hola, {n}")

# =========================================================================================
#  SECCIÓN 2 · range() (secuencias numéricas)
# =========================================================================================
def seccion_2():
    encabezado("SECCIÓN 2 · range() (secuencias numéricas)")

    # * TEORÍA
    # range(fin)                → 0..fin-1
    # range(inicio, fin)        → inicio..fin-1
    # range(inicio, fin, paso)  → con incremento/decremento
    # Útil para contar, sumar, repetir tareas.

    # * DEMO · suma 1..n
    n = safe_input("n para sumar 1..n: ", int, default=5)
    total = 0
    for i in range(1, n + 1):
        total += i
    print(f"Suma 1..{n} = {total}")

    # TODO: (Tema: TABLA DE MULTIPLICAR)
    # Pide/captura un número 't' (por defecto 4) y muestra su tabla del 1 al 10.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # t = safe_input("Tabla de: ", int, default=4)
    # for i in range(1, 11):
    #     print(f"{t} x {i} = {t*i}")

# =========================================================================================
#  SECCIÓN 3 · enumerate() (índice + valor)
# =========================================================================================
def seccion_3():
    encabezado("SECCIÓN 3 · enumerate() (índice + valor)")

    # * TEORÍA
    # enumerate(lista, start=0) → produce pares (indice, valor).
    # Muy útil para numerar resultados de forma limpia.

    # * DEMO
    lista_compra = ["pan", "leche", "huevos"]
    for idx, item in enumerate(lista_compra, start=1):
        print(f"{idx}. {item}")

    # TODO: (Tema: TAREAS)
    # Crea lista 'tareas' y muéstralas numeradas desde 1.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # tareas = ["pagar", "estudiar", "entrenar"]
    # for i, t in enumerate(tareas, start=1):
    #     print(f"{i}. {t}")

# =========================================================================================
#  SECCIÓN 4 · while (repite mientras la condición sea True)
# =========================================================================================
def seccion_4():
    encabezado("SECCIÓN 4 · while (condición)")

    # * TEORÍA
    # while <condición>:
    #     <bloque>
    # ¡Cuidado con los bucles infinitos! Asegura que la condición cambie.
    # Patrón común: contador con límite de intentos.

    # * DEMO · PIN con 3 intentos
    PIN_CORRECTO = "1234"
    intentos = 0
    autenticado = False
    while intentos < 3 and not autenticado:
        pin = safe_input("PIN: ", str, default=PIN_CORRECTO if intentos == 0 else "0000")
        autenticado = (pin == PIN_CORRECTO)
        intentos += 1
    print("Acceso" + (" concedido" if autenticado else " denegado"))

    # TODO: (Tema: CONTADOR)
    # Usa while para imprimir los números del 1 al 5 (incluidos).
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # i = 1
    # while i <= 5:
    #     print(i)
    #     i += 1

# =========================================================================================
#  SECCIÓN 5 · break, continue y for-else
# =========================================================================================
def seccion_5():
    encabezado("SECCIÓN 5 · break, continue y for-else")

    # * TEORÍA
    # break    → sale del bucle inmediatamente.
    # continue → salta a la siguiente iteración.
    # for ... else: el 'else' se ejecuta si NO hubo 'break' (se recorrió completo).

    # * DEMO · búsqueda con for-else
    datos = [3, 7, 10, 12]
    objetivo = 9
    for d in datos:
        if d == objetivo:
            print("Encontrado")
            break
    else:
        print("No encontrado (for-else)")

    # * DEMO · continue (saltando negativos)
    numeros = [5, -2, 4, -1, 6]
    positivos = []
    for n in numeros:
        if n < 0:
            continue
        positivos.append(n)
    print(f"Solo positivos: {positivos}")

    # TODO: (Tema: SUMA POSITIVOS / CORTE EN CERO)
    # Recorre una lista de enteros; suma solo positivos. Si aparece un 0, corta (break).
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # datos = [1, 3, -2, 5, 0, 4]
    # total = 0
    # for x in datos:
    #     if x == 0:
    #         break
    #     if x > 0:
    #         total += x
    # print("Total positivos hasta el corte:", total)

# =========================================================================================
#  SECCIÓN 6 · Bucles anidados (tablas)
# =========================================================================================
def seccion_6():
    encabezado("SECCIÓN 6 · Bucles anidados (tablas)")

    # * TEORÍA
    # Un bucle dentro de otro. Útil para tablas, cuadrículas, combinaciones.

    # * DEMO · tabla 1..3 x 1..3
    for fila in range(1, 4):
        linea = []
        for col in range(1, 4):
            linea.append(fila * col)
        print(linea)

    # TODO: (Tema: CUADRÍCULA)
    # Pide 'filas' y 'columnas' y dibuja una cuadrícula de '*' de ese tamaño.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # filas = safe_input("Filas: ", int, default=3)
    # cols  = safe_input("Columnas: ", int, default=5)
    # for _ in range(filas):
    #     print("*" * cols)

# =========================================================================================
#  SECCIÓN 7 · Comprensiones de listas (opcional)
# =========================================================================================
def seccion_7():
    encabezado("SECCIÓN 7 · Comprensiones de listas (opcional)")

    # * TEORÍA
    # [expr for x in coleccion if condicion]
    # Azúcar sintáctico para crear listas de forma concisa.

    # * DEMO
    nums = [1, 2, 3, 4, 5]
    cuadrados = [x * x for x in nums]
    pares = [x for x in nums if x % 2 == 0]
    print("Cuadrados:", cuadrados, "| Pares:", pares)

    # TODO: (Tema: PRECIOS + IVA)
    # Dada una lista de precios base, crea otra con el 21% de IVA aplicado (redondeo a 2 decimales).
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # precios = [10, 3.5, 20]
    # con_iva = [round(p * 1.21, 2) for p in precios]
    # print(con_iva)

# =========================================================================================
#  SECCIÓN 8 · Laboratorio IA (Bucles creativos)
# =========================================================================================
def seccion_8_ia():
    encabezado("SECCIÓN 8 · Laboratorio IA (Bucles creativos)")

    # * PROMPT KIT (copia/pega en ChatGPT)
    # 1) PROMPT BREVE:
    #    "Eres profesor de Python. Genera un programa de 25–40 líneas que use for/while,
    #     range/enumerate y break/continue. Tema: 'carrito de la compra con descuentos por
    #     volumen'. Requisitos: variables en español, comentarios con # * y # TODO, sin
    #     librerías ni clases. Devuélveme SOLO código Python."
    #
    # 2) PROMPT ALTERNATIVO:
    #    "Crea un minijuego 'Adivina el número': genera un número secreto (usar fijo si
    #     no hay random) y permite hasta 5 intentos con pistas (mayor/menor). Usa while y break."
    #
    # 3) PROMPT DE MEJORA:
    #    "Optimiza el código con enumerate y un resumen final en una línea. Mantén 30–40 líneas."

    # * DEMO opcional
    if IA_DEMO:
        # Mini-demo: suma solo pares del 1 al 10
        suma_pares = sum([n for n in range(1, 11) if n % 2 == 0])
        print("Suma de pares 1..10:", suma_pares)

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
    encabezado("AUTOEVALUACIÓN FINAL · Gestor simple con bucles")

    # TODO: (ENUNCIADO)
    # 1) Crea un menú en bucle while con opciones:
    #    1) Añadir tarea  2) Listar tareas (numeradas con enumerate)
    #    3) Eliminar por número  4) Mostrar suma de tareas con más de N caracteres
    #    5) Tabla de multiplicar de un número  0) Salir
    # 2) Usa range/enumerate donde corresponda. Evita bucles infinitos.
    # 3) Opcional: for-else para avisar si no se encuentra un índice al eliminar.
    # 4) Muestra un resumen final en una línea: 
    #    "Total tareas:<n> | Largas:<m> | Última acción:<texto>"
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

# =========================================================================================
#  MENÚ PRINCIPAL
# =========================================================================================
def menu():
    while True:
        print_firma()
        print("MENÚ · Elige una opción")
        print("  1) for básico (listas)")
        print("  2) range() (secuencias numéricas)")
        print("  3) enumerate() (índice + valor)")
        print("  4) while (condición)")
        print("  5) break / continue / for-else")
        print("  6) Bucles anidados (tablas)")
        print("  7) Comprensiones (opcional)")
        print("  8) Laboratorio IA (Bucles)")
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
