# =========================================================================================
#  🐍 PYTHON CLASE 9 — ENTRADA Y SALIDA DE ARCHIVOS (E/S)
#  ────────────────────────────────────────────────────────────────────────────────────────
#  📘 En esta clase practicarás:
#    * open() y with (context manager) · modos: 'r' 'w' 'a' 'rb' 'wb'
#    * Texto: read(), readline(), readlines(), iterar líneas, encoding UTF-8
#    * Escritura incremental y logs
#    * pathlib para rutas, exists(), mkdir(), glob(), rename(), unlink()
#    * CSV con csv.reader / csv.writer
#    * JSON con json.load / json.dump (ensure_ascii, indent)
#    * Binarios: lectura/escritura y copias por bloques
#    * Errores comunes de E/S y manejo con excepciones
#    * Laboratorio IA y Autoevaluación integradora
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
#  SECCIÓN 1 · open() y with · modos básicos de texto
# =========================================================================================
def seccion_1():
    encabezado("SECCIÓN 1 · open() y with · modos básicos de texto")

    # * TEORÍA
    # open(ruta, modo, encoding="utf-8")
    #  - 'w' escribe (crea/sobrescribe) · 'a' añade · 'r' lee
    #  - with open(...) as f:  cierra automáticamente (context manager)

    # * DEMO
    from pathlib import Path
    ruta = Path("demo_io.txt")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("Primera línea\n")
        f.write("Segunda línea\n")
    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read()
    print("Contenido de demo_io.txt:")
    print(contenido)

    # TODO: (Tema: NOTA RÁPIDA)
    # Pide/captura una frase (por defecto "Hola archivo") y guárdala en 'nota.txt'.
    # Lee el archivo y muéstralo por pantalla.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # from pathlib import Path
    # frase = safe_input("Escribe una frase: ", str, default="Hola archivo")
    # Path("nota.txt").write_text(frase, encoding="utf-8")
    # print(Path("nota.txt").read_text(encoding="utf-8"))

# =========================================================================================
#  SECCIÓN 2 · Leer texto: read(), readline(), readlines(), iterar líneas
# =========================================================================================
def seccion_2():
    encabezado("SECCIÓN 2 · Lecturas de texto (read / readline / readlines)")

    # * TEORÍA
    # read()      → todo el archivo (cuidado si es muy grande)
    # readline()  → una línea (incluye '\n' si existe)
    # readlines() → lista de líneas
    # for linea in f:  → iteración eficiente línea a línea

    # * DEMO (creamos un archivo de ejemplo)
    from pathlib import Path
    ruta = Path("poema.txt")
    ruta.write_text("uno\ndos\ntres\ncuatro\n", encoding="utf-8")

    with open(ruta, "r", encoding="utf-8") as f:
        print("read():", repr(f.read()))
    with open(ruta, "r", encoding="utf-8") as f:
        print("readline():", repr(f.readline()))
    with open(ruta, "r", encoding="utf-8") as f:
        print("readlines():", [l.strip() for l in f.readlines()])

    print("Iterar líneas (strip):")
    for i, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), start=1):
        print(f"{i:02d}: {linea}")

    # TODO: (Tema: CONTADOR DE LÍNEAS Y PALABRAS)
    # Lee 'poema.txt' y muestra: número de líneas y número total de palabras.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

# =========================================================================================
#  SECCIÓN 3 · Escribir y añadir (append) · mini-logs
# =========================================================================================
def seccion_3():
    encabezado("SECCIÓN 3 · Escritura y append · mini-logs")

    # * TEORÍA
    # modo 'w' sobrescribe · modo 'a' añade al final.
    # Siempre añade '\n' al final de cada línea si quieres líneas separadas.

    # * DEMO
    from pathlib import Path
    from datetime import datetime
    log = Path("log.txt")
    with open(log, "w", encoding="utf-8") as f:
        f.write("Inicio del log\n")
    with open(log, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] Evento A\n")
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] Evento B\n")
    print(log.read_text(encoding="utf-8"))

    # TODO: (Tema: APÉNDICE DE EVENTOS)
    # Pide/captura un evento (por defecto "Login OK") y añádelo a log.txt con timestamp ISO.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

# =========================================================================================
#  SECCIÓN 4 · pathlib para rutas · exists/mkdir/glob/rename/unlink
# =========================================================================================
def seccion_4():
    encabezado("SECCIÓN 4 · pathlib (rutas) · exists/mkdir/glob/rename/unlink")

    # * TEORÍA
    # from pathlib import Path
    # Path.cwd(), Path("carpeta")/ "archivo.txt"
    # p.exists(), p.is_file(), p.is_dir()
    # p.mkdir(parents=True, exist_ok=True)
    # list(p.glob("*.txt"))  → patrón
    # p.rename(nuevo_nombre), p.unlink()  → borrar archivo

    # * DEMO
    from pathlib import Path
    carpeta = Path("data_io")
    carpeta.mkdir(exist_ok=True)
    for i in range(1, 4):
        (carpeta / f"f{i}.txt").write_text(f"archivo {i}", encoding="utf-8")
    print("TXT en carpeta:", [p.name for p in carpeta.glob("*.txt")])

    # renombrar el primero
    f1 = carpeta / "f1.txt"
    if f1.exists():
        f1.rename(carpeta / "f1_renombrado.txt")
    print("Tras renombrar:", [p.name for p in carpeta.glob("*.txt")])

    # TODO: (Tema: LIMPIEZA SELECTIVA)
    # Crea 'data_tmp' con 3 .log y 2 .txt. Borra solo los .log y muestra lo que queda.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

# =========================================================================================
#  SECCIÓN 5 · CSV (leer y escribir)
# =========================================================================================
def seccion_5():
    encabezado("SECCIÓN 5 · CSV (leer y escribir)")

    # * TEORÍA
    # import csv
    # with open(..., newline='', encoding='utf-8') as f:
    #   writer = csv.writer(f); writer.writerow([...]); writer.writerows(lista_filas)
    #   reader = csv.reader(f);  next(reader) para saltar cabecera
    # O con DictReader / DictWriter (por nombres de columna)

    import csv
    from pathlib import Path

    archivo = Path("alumnos.csv")
    with open(archivo, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["nombre", "nota"])
        w.writerows([["Ana", 8], ["Luis", 6], ["María", 9]])

    print("Leemos CSV:")
    with open(archivo, "r", newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        cab = next(r)
        print("Cabecera:", cab)
        for fila in r:
            print("Fila:", fila)

    # TODO: (Tema: CSV + COLUMNA APROBADO)
    # Lee 'alumnos.csv' y crea 'alumnos_out.csv' añadiendo una columna 'aprobado' (nota>=5).
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

# =========================================================================================
#  SECCIÓN 6 · JSON (serializar / deserializar)
# =========================================================================================
def seccion_6():
    encabezado("SECCIÓN 6 · JSON (serializar / deserializar)")

    # * TEORÍA
    # import json
    # json.dump(obj, f, ensure_ascii=False, indent=2)  · json.load(f)
    # json.dumps / json.loads para cadena en memoria

    import json
    from pathlib import Path

    productos = [
        {"nombre": "cuaderno", "precio": 2.5},
        {"nombre": "bolígrafo", "precio": 1.2},
    ]
    Path("productos.json").write_text(
        json.dumps(productos, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    cargado = json.loads(Path("productos.json").read_text(encoding="utf-8"))
    print("JSON cargado:", cargado)

    # TODO: (Tema: LISTA DE TAREAS JSON)
    # Crea una lista de tareas (dict con 'texto' y 'hecha': bool), guárdala en 'tareas.json'
    # y vuelve a leerla mostrando cuántas están hechas y cuántas pendientes.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

# =========================================================================================
#  SECCIÓN 7 · Binarios · leer/escribir y copias por bloques
# =========================================================================================
def seccion_7():
    encabezado("SECCIÓN 7 · Binarios (rb/wb) y copias por bloques")

    # * TEORÍA
    # with open("archivo", "rb") as f:  data = f.read(1024)   # bloques
    # with open("destino", "wb") as g:  g.write(bloque)
    # Útil para copiar imágenes, PDFs, etc. (no los manipules como texto).

    from pathlib import Path

    # * DEMO · creamos un binario pequeño y lo copiamos
    src = Path("demo.bin")
    if not src.exists():
        # 256 bytes (0..255)
        src.write_bytes(bytes(range(256)))
    dst = Path("demo_copia.bin")
    with open(src, "rb") as f, open(dst, "wb") as g:
        while True:
            bloque = f.read(64)
            if not bloque:
                break
            g.write(bloque)
    print(f"Copia OK → {dst} ({dst.stat().st_size} bytes)")
    print("Primeros 16 bytes (hex):", src.read_bytes()[:16].hex())

    # TODO: (Tema: ESPIAR CABECERA)
    # Lee los primeros 8 bytes de 'demo.bin' y muéstralos en hex. Muestra su tamaño total.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

# =========================================================================================
#  SECCIÓN 8 · Errores comunes en E/S y manejo con excepciones
# =========================================================================================
def seccion_8():
    encabezado("SECCIÓN 8 · Errores comunes de E/S y excepciones")

    # * TEORÍA
    # FileNotFoundError, PermissionError, UnicodeDecodeError, json.JSONDecodeError
    # Patrón típico:
    # try: abrir/leer
    # except FileNotFoundError: crear por defecto o avisar
    # except ...: manejar

    from pathlib import Path
    import json

    # * DEMO · archivo inexistente
    try:
        print(Path("no_existe.txt").read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("No existe 'no_existe.txt' → creando con contenido por defecto.")
        Path("no_existe.txt").write_text("creado por defecto\n", encoding="utf-8")

    # * DEMO · JSON inválido
    Path("malo.json").write_text("{invalido: true", encoding="utf-8")
    try:
        json.loads(Path("malo.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print("JSON inválido:", e)

    # TODO: (Tema: LECTOR SEGURO JSON)
    # Implementa load_json_safe(ruta) que devuelva {} ante errores y, si no existe, lo cree vacío.
    # Pruébalo con 'config.json'.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

# =========================================================================================
#  SECCIÓN 9 · Laboratorio IA (persistencia sencilla)
# =========================================================================================
def seccion_9_ia():
    encabezado("SECCIÓN 9 · Laboratorio IA (persistencia sencilla)")

    # * PROMPT KIT (copia/pega en ChatGPT)
    # 1) PROMPT BREVE:
    #    "Eres profesor de Python. Genera un programa de 35–50 líneas que implemente
    #     un gestor de notas (texto) con:
    #       - pathlib para rutas y carpeta 'notas'
    #       - crear/listar/leer/borrar notas .txt
    #     Requisitos: variables en español, comentarios con # * y # TODO, manejo de errores
    #     básicos (FileNotFoundError). Devuélveme SOLO código Python."
    #
    # 2) PROMPT ALTERNATIVO:
    #    "Crea una agenda de tareas persistente con JSON: añadir, listar, marcar hecha,
    #     guardar y cargar (append seguro si existe). Sin librerías externas."
    #
    # 3) PROMPT DE MEJORA:
    #    "Refactoriza separando funciones de E/S (leer_json, escribir_json) y añade
    #     protección de UnicodeDecodeError. Mantén el total bajo 50 líneas."

    # * DEMO opcional
    if IA_DEMO:
        from pathlib import Path
        notas = Path("notas")
        notas.mkdir(exist_ok=True)
        (notas/"demo.txt").write_text("Mi primera nota 📓", encoding="utf-8")
        print("Demo IA → creada 'notas/demo.txt'")

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
    encabezado("AUTOEVALUACIÓN FINAL · Gestor de gastos (texto/JSON/CSV)")

    # TODO: (ENUNCIADO)
    # Implementa un gestor de gastos con persistencia:
    #
    # 1) Carpeta 'datos' (pathlib). Archivos:
    #    - 'gastos.txt'   → cada línea: "concepto;importe"
    #    - 'gastos.json'  → lista de dicts {"concepto":..., "importe":..., "fecha":...}
    #    - 'gastos.csv'   → columnas: concepto, importe, fecha
    #
    # 2) Flujo:
    #    - Añade 3 apuntes (si RUN_INTERACTIVE=False, usa valores por defecto).
    #    - Escribe los tres formatos (txt/json/csv) con encoding utf-8 (y newline='' en CSV).
    #    - Vuelve a leerlos y calcula:
    #        · nº de movimientos, total y gasto medio
    #        · mayor gasto (concepto/importe)
    #
    # 3) Manejo de errores:
    #    - Protege la lectura con try/except para FileNotFoundError y JSONDecodeError.
    #
    # 4) Línea final tipo dashboard:
    #    "Movs:<n> | Total:<€> | Medio:<€> | Mayor:<concepto-€>"
    #
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

# =========================================================================================
#  MENÚ PRINCIPAL
# =========================================================================================
def menu():
    while True:
        print_firma()
        print("MENÚ · Elige una opción")
        print("  1) open() y with · texto")
        print("  2) Lecturas (read/readline/readlines)")
        print("  3) Escritura y append · logs")
        print("  4) pathlib (rutas y utilidades)")
        print("  5) CSV")
        print("  6) JSON")
        print("  7) Binarios · copias por bloques")
        print("  8) Errores de E/S y excepciones")
        print("  9) Laboratorio IA (persistencia)")
        print(" 10) Autoevaluación final")
        print(" 11) Ejecutar TODO (1→10)")
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
        elif op == 8: seccion_8(); pause()
        elif op == 9: seccion_9_ia(); pause()
        elif op == 10: autoevaluacion(); pause()
        elif op == 11:
            seccion_1(); seccion_2(); seccion_3(); seccion_4(); seccion_5(); seccion_6(); seccion_7(); seccion_8(); seccion_9_ia(); autoevaluacion(); pause()
        else:
            print("! Elige una opción del 0 al 11.")

# =========================================================================================
#  EJECUCIÓN
# =========================================================================================
if __name__ == "__main__":
    menu()
