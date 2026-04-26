# =========================================================================================
#  🐍 PYTHON CLASE 5 — LISTAS, DICCIONARIOS y BUCLES ANIDADOS (+ ordenación, comprensiones, IA)
#  ────────────────────────────────────────────────────────────────────────────────────────
#  📘 En esta clase practicarás:
#    * Listas: creación, acceso, slicing y métodos (append, insert, remove, pop, sort, reverse)
#    * Diccionarios: acceso/actualización, get(), keys/values/items()
#    * Iteración sobre diccionarios
#    * Estructuras anidadas (lista de diccionarios / diccionario con listas) + bucles anidados
#    * Ordenación con key / lambda, min/max/sum con key
#    * Comprensiones de listas y diccionarios (opcional)
#    * Laboratorio IA y Autoevaluación integradora
#
#  🎨 Better Comments:
#    # ! importante   ·  # * definición/foco   ·  # ? idea/nota
#    # TODO: práctica  ·  # NOTE: apunte útil   ·  # // deprecado
# =========================================================================================

from typing import Any, Callable, Dict, List

# * Configuración general ---------------------------------------------------------------
RUN_INTERACTIVE = True   # True: pedir datos al usuario; False: valores por defecto
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
#  SECCIÓN 1 · LISTAS — creación, acceso, slicing y métodos
# =========================================================================================
def seccion_1():
    encabezado("SECCIÓN 1 · Listas — creación, acceso, slicing y métodos")

    # * TEORÍA
    # lista = [elem1, elem2, ...]
    # Acceso por índice: lista[i]   ·  Slicing: lista[i:j]  ·  len(lista)
    # Métodos útiles: append, insert, remove, pop, sort, reverse, index, count

    # * DEMO
    productos = ["bolígrafo", "cuaderno", "grapas", "folios"]
    productos.append("marcador")
    productos.append("carpeta")
    productos.insert(1, "regla")
    productos.remove("grapas")
    primero, sub = productos[0], productos[1:3]
    productos.sort()             # orden alfabético
    productos.reverse()          # invertimos
    print("Productos:", productos)
    print("Primero:", primero, "| Sublista 1:3:", sub)

    # TODO: (Tema: LISTA DE CIUDADES)
    # 1) Crea lista con 4 ciudades. Inserta una en la posición 2. Elimina la última.
    # 2) Muestra: longitud, primera, última y el slice 1:3.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

    ciudades = ["Madrid", "Barcelona", "Valencia", "Valladolid"]
    ciudades.insert(2, "Burgos")
    ciudades.pop(-1)
    print("Ciudades:", ciudades)

    # Bucle que imprime si encuentra Madrid
    for ciudad in ciudades:
        if ciudad == "Madrid":
            print("¡Encontrado Madrid en la lista!")


# =========================================================================================
#  SECCIÓN 2 · DICCIONARIOS — acceso, actualización y utilidades
# =========================================================================================
def seccion_2():
    encabezado("SECCIÓN 2 · Diccionarios — acceso, actualización y utilidades")

    # * TEORÍA
    # dic = {"clave": valor, ...}
    # Acceso: dic["clave"]  · get("clave", por_defecto)
    # Añadir/actualizar: dic["clave"] = valor
    # Eliminar: del dic["clave"]   ·  Utilidades: keys(), values(), items()

    # * DEMO
    perfil: Dict[str, Any] = {"nombre": "Lucía", "edad": 20, "premium": False}
    perfil["premium"] = True
    perfil["puntos"] = perfil.get("puntos", 0) + 50   # get con por defecto
    print("Perfil:", perfil)
    print("Claves:", list(perfil.keys()))
    print("Valores:", list(perfil.values()))
    print("Items:", list(perfil.items()))

    # TODO: (Tema: CONTACTO)
    # Crea un dict 'contacto' con nombre, telefono y email.
    # Actualiza el teléfono, añade 'ciudad' y muestra sus items en una línea por item.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 3 · Iterar diccionarios (keys / values / items)
# =========================================================================================
def seccion_3():
    encabezado("SECCIÓN 3 · Iterar diccionarios (keys/values/items)")

    # * TEORÍA
    # for k in dic: ...            (recorre claves)
    # for v in dic.values(): ...
    # for k, v in dic.items(): ...

    # * DEMO
    precios = {"bolígrafo": 1.2, "cuaderno": 2.5, "carpeta": 3.6}
    for nombre, precio in precios.items():
        print(f"{nombre}: {precio:.2f} €")

    # TODO: (Tema: NOTAS DE ALUMNOS)
    # Crea un dict con 3 alumnos y sus notas {"Ana": 8.5, "Carlos": 6.0, "María": 9.2}
    # Recorre con items() y muestra "X -> APROBADO" si nota>=5, si no "SUSPENSO".
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    notas = {"Ana": 8.5, "Carlos": 4.2, "María": 9.2}
    for alumno, nota in notas.items():
        estado = "APROBADO" if nota >= 5 else "SUSPENSO"
        print(f"{alumno} -> {estado} (nota: {nota})")


# =========================================================================================
#  SECCIÓN 4 · Estructuras anidadas + bucles anidados
# =========================================================================================
def seccion_4():
    encabezado("SECCIÓN 4 · Estructuras anidadas + bucles anidados")

    # * TEORÍA
    # - Lista de diccionarios (p. ej., productos con campos)
    # - Diccionario con listas (p. ej., categorías -> lista de items)
    # Recorremos con bucles anidados: for x in lista:  for y in x["campo"]: ...

    # * DEMO · Lista de diccionarios + recorrer servicios de cada uno
    catalogo = [
        {"nombre": "Pack Estudio", "items": ["cuaderno", "bolígrafo", "regla"]},
        {"nombre": "Pack Oficina", "items": ["carpeta", "grapas", "bolígrafo"]},
    ]
    for pack in catalogo:
        print(f"\n{pack['nombre']} →")
        for item in pack["items"]:
            print("  -", item)

    # TODO: (Tema: CLASES Y ALUMNOS)
    # Crea una lista de diccionarios, cada uno con: "clase" (str) y "alumnos" (lista de str).
    # Recorre y muestra: "Clase <clase>:" y cada alumno con guion.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 5 · Ordenación con key / lambda + min/max/sum con key
# =========================================================================================
def seccion_5():
    encabezado("SECCIÓN 5 · Ordenación con key/lambda + min/max/sum con key")

    # * TEORÍA
    # sorted(lista, key=func)  · list.sort(key=func)  · reverse=True para descendente
    # min(lista, key=func) / max(lista, key=func)
    # sum(x["precio"] for x in lista)  (generador)

    # * DEMO
    productos = [
        {"nombre": "cuaderno", "precio": 2.5},
        {"nombre": "carpeta", "precio": 3.6},
        {"nombre": "bolígrafo", "precio": 1.2},
    ]
    ordenados = sorted(productos, key=lambda p: p["precio"])
    mas_barato = min(productos, key=lambda p: p["precio"])
    total = sum(p["precio"] for p in productos)
    print("Ordenados por precio asc:", ordenados)
    print("Más barato:", mas_barato)
    print("Total:", round(total, 2))

    # TODO: (Tema: TOP ALUMNOS)
    # Dada una lista de dicts con {"nombre":..., "nota":...}, ordénalos por nota desc y
    # muestra el primero como "Mejor alumno: <nombre> (<nota>)".
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 6 · Comprensiones (listas y diccionarios) [opcional]
# =========================================================================================
def seccion_6():
    encabezado("SECCIÓN 6 · Comprensiones (listas y diccionarios) [opcional]")

    # * TEORÍA
    # Lista: [expr for x in coleccion if condicion]
    # Diccionario: {k_expr: v_expr for x in coleccion if condicion}

    # * DEMO
    nums = [1, 2, 3, 4, 5, 6]
    pares_cuadrados = [n*n for n in nums if n % 2 == 0]
    precios = {"A": 10, "B": 5, "C": 20}
    con_iva = {k: round(v * 1.21, 2) for k, v in precios.items()}
    print("Pares^2:", pares_cuadrados)
    print("Con IVA:", con_iva)

    # TODO: (Tema: FILTRO DE INVENTARIO)
    # Dado un dict producto->stock, crea otro dict solo con los que stock>0.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 7 · Laboratorio IA (Colecciones creativas)
# =========================================================================================
def seccion_7_ia():
    encabezado("SECCIÓN 7 · Laboratorio IA (Colecciones creativas)")

    # * PROMPT KIT (copia/pega en ChatGPT)
    # 1) PROMPT BREVE:
    #    "Eres profesor de Python. Genera un programa de 30–45 líneas que use listas,
    #     diccionarios y bucles anidados. Tema: 'inventario de tienda con categorías y
    #     precios'. Requisitos: variables en español, comentarios con # * y # TODO,
    #     sorted con key para ordenar por precio y un resumen final. Solo código Python."
    #
    # 2) PROMPT ALTERNATIVO:
    #    "Crea un 'gestor de clases' con lista de diccionarios (clase, alumnos) que permita
    #     agregar/borrar y ordenar por tamaño de clase. Sin librerías. 30–40 líneas."
    #
    # 3) PROMPT DE MEJORA:
    #    "Optimiza con comprensiones y min/max/sum con key. Manténlo bajo 45 líneas."

    # * DEMO opcional
    if IA_DEMO:
        catalogo = [
            {"nombre": "cuaderno", "precio": 2.5, "categoria": "papelería"},
            {"nombre": "marcador", "precio": 1.8, "categoria": "papelería"},
            {"nombre": "pendrive", "precio": 9.9, "categoria": "tech"},
        ]
        barato = min(catalogo, key=lambda x: x["precio"])
        print("Demo IA → Más barato:", barato["nombre"], barato["precio"])

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
    encabezado("AUTOEVALUACIÓN FINAL · Inventario + Reporte")

    # TODO: (ENUNCIADO)
    # 1) Crea una lista de diccionarios 'inventario', cada uno con:
    #       {"nombre": str, "categoria": str, "precio": float, "stock": int}
    # 2) Muestra:
    #    - Productos por categoría (bucle anidado sobre un dict agrupado).
    #    - Ordena por precio asc y muestra el top 3 más baratos.
    #    - Total del valor de stock (sum(p['precio']*p['stock'])).
    # 3) Usa comprensiones para crear un dict {nombre:precio_con_iva} (21%).
    # 4) Línea final tipo dashboard:
    #    "Items:<n> | Categorías:<m> | Valor stock:<€> | Barato:<nombre-precio>"
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  MENÚ PRINCIPAL
# =========================================================================================
def menu():
    while True:
        print_firma()
        print("MENÚ · Elige una opción")
        print("  1) Listas: acceso y métodos")
        print("  2) Diccionarios: acceso y utilidades")
        print("  3) Iterar diccionarios")
        print("  4) Estructuras anidadas + bucles anidados")
        print("  5) Ordenación con key / lambda")
        print("  6) Comprensiones (opcional)")
        print("  7) Laboratorio IA (Colecciones)")
        print("  8) Autoevaluación final")
        print("  9) Ejecutar TODO (1→8)")
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
        elif op == 7: seccion_7_ia(); pause()
        elif op == 8: autoevaluacion(); pause()
        elif op == 9:
            seccion_1(); seccion_2(); seccion_3(); seccion_4(); seccion_5(); seccion_6(); seccion_7_ia(); autoevaluacion(); pause()
        else:
            print("! Elige una opción del 0 al 9.")

# =========================================================================================
#  EJECUCIÓN
# =========================================================================================
if __name__ == "__main__":
    menu()
