# =========================================================================================
#  🐍 PYTHON CLASE 2 — CONDICIONALES (if, elif, else) + Truthy/Falsy + Ternario + IA
#  ────────────────────────────────────────────────────────────────────────────────────────
#  📘 En esta clase practicarás:
#    * if, elif, else (flujo condicional básico)
#    * Expresiones booleanas con and / or / not
#    * Valores truthy / falsy y conversión bool()
#    * Operador ternario (expresión condicional en una línea)
#    * match/case básico (opcional, Python 3.10+)
#    * Laboratorio IA: programa creativo centrado en condicionales
#    * Autoevaluación final (mezcla de todo)
#
#  🎨 Better Comments:
#    # ! importante   ·  # * definición/foco   ·  # ? idea/nota
#    # TODO: práctica  ·  # NOTE: apunte útil   ·  # // deprecado
# =========================================================================================

from typing import Any, Callable

# * Configuración general ---------------------------------------------------------------
RUN_INTERACTIVE = True    # True: pedir datos al usuario; False: usar valores por defecto
PAUSE = False             # Pausa tras cada opción del menú
IA_DEMO = True            # Demo corta en Laboratorio IA

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
    """# * Convierte entrada al tipo deseado; si falla o no hay input, devuelve 'default'."""
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
#  SECCIÓN 1 · if básico (una condición) 
# =========================================================================================
def seccion_1():
    encabezado("SECCIÓN 1 · if básico (una condición)")

    # * TEORÍA
    # if <condición>:
    #     <bloque>
    # Si la condición es True, se ejecuta el bloque. La indentación define el bloque.

    # * DEMO
    edad = safe_input("Tu edad: ", int, default=17)
    if edad >= 18:
        print("Puedes entrar ✅")
    print("Fin de la comprobación.")

    # TODO: (Tema: MAYORÍA DE EDAD)
    # Pide/captura edad y si es >=18 imprime "Mayor de edad", si no, no imprimas nada.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 2 · if / else / elif (múltiples caminos)
# =========================================================================================
def seccion_2():
    encabezado("SECCIÓN 2 · if / else / elif")

    # * TEORÍA
    # if ...:
    #     ...
    # elif ...:
    #     ...
    # else:
    #     ...
    # Se evalúa de arriba a abajo; entra en la primera condición True y el resto se ignoran.

    # * DEMO (clasificador de notas 0–10)
    nota = safe_input("Nota (0-10): ", int, default=6)
    if nota >= 9:
        nivel = "Sobresaliente"
    elif nota >= 7:
        nivel = "Notable"
    elif nota >= 5:
        nivel = "Aprobado"
    else:
        nivel = "Suspenso"
    print(f"Nivel: {nivel}")

    # TODO: (Tema: SEMÁFORO)
    # Pide un color (rojo/amarillo/verde) y muestra:
    #  - "Para" si rojo
    #  - "Precaución" si amarillo
    #  - "Adelante" si verde
    # En cualquier otro caso, "Color no válido".
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 3 · Condiciones compuestas (and / or / not) + if anidado
# =========================================================================================
def seccion_3():
    encabezado("SECCIÓN 3 · and / or / not + if anidado")

    # * TEORÍA
    # Usa operadores lógicos para combinar condiciones:
    # - A and B   → True si ambas verdaderas
    # - A or  B   → True si alguna verdadera
    # - not A     → invierte el booleano

    # * DEMO (acceso a evento: mayor de edad y con entrada)
    edad = safe_input("Edad: ", int, default=20)
    tiene_entrada = safe_input("¿Tienes entrada? (s/n): ", str, default="s").lower() == "s"

    if edad >= 18 and tiene_entrada:
        print("Acceso concedido 🎟️")
    else:
        if edad < 18:
            print("Acceso denegado: menor de edad.")
        if not tiene_entrada:
            print("Acceso denegado: necesitas una entrada.")

    # TODO: (Tema: DESCUENTO TIENDA)
    # Pide/captura: es_estudiante (s/n) y total_compra (float).
    # Si es estudiante y total_compra >= 20 aplica 10% de descuento; si no, 0%.
    # Muestra "Total final: <importe>" con 2 decimales.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 4 · Truthy / Falsy + bool()
# =========================================================================================
def seccion_4():
    encabezado("SECCIÓN 4 · Truthy / Falsy + bool()")

    # * TEORÍA
    # En Python se consideran Falsy: 0, 0.0, "", [], {}, set(), None, False.
    # Todo lo demás suele ser Truthy.
    # Útil para escribir condiciones concisas: if lista:  (si no está vacía)

    # * DEMO
    nombre = safe_input("Escribe tu nombre (o deja vacío): ", str, default="")
    if nombre:   # True si no está vacío
        print(f"Hola, {nombre}")
    else:
        print("No has escrito nombre.")

    carrito = []  # lista vacía → Falsy
    if not carrito:
        print("El carrito está vacío 🛒")

    # TODO: (Tema: INICIO DE SESIÓN SIMPLE)
    # Pide/captura username (str). Si está vacío, imprime "Usuario requerido".
    # Si no está vacío, imprime "Bienvenido, <username>".
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 5 · Operador ternario (expresión condicional) 
# =========================================================================================
def seccion_5():
    encabezado("SECCIÓN 5 · Operador ternario (expresión condicional)")

    # * TEORÍA
    # <valor_si_true> if <condición> else <valor_si_false>
    # Útil para asignar o imprimir algo corto en una sola línea.

    # * DEMO (par / impar)
    n = safe_input("Número: ", int, default=7)
    mensaje = "Par" if n % 2 == 0 else "Impar"
    print(f"{n} → {mensaje}")

    # TODO: (Tema: GASTOS ENVÍO)
    # Si el total >= 30 → "Envío gratis", en caso contrario "Envío 3.99€", usando ternario.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 6 · match / case (opcional, Python 3.10+)
# =========================================================================================
def seccion_6():
    encabezado("SECCIÓN 6 · match / case (opcional)")

    # * TEORÍA
    # match <valor>:
    #   case "algo":
    #       ...
    #   case _:
    #       ...   ← comodín (default)
    # Útil para reemplazar varias ramas elif sobre un mismo valor.

    # * DEMO (rol de usuario)
    rol = safe_input("Rol (admin, editor, invitado): ", str, default="editor")

    try:
        # Si tu Python no soporta match/case, caerá al except.
        match rol:
            case "admin":
                permiso = "Acceso total"
            case "editor":
                permiso = "Puede editar contenidos"
            case "invitado":
                permiso = "Solo lectura"
            case _:
                permiso = "Rol desconocido"
        print(f"Permiso: {permiso}")
    except SyntaxError:
        print("Tu versión de Python no soporta match/case (se necesita 3.10+).")

    # TODO: (Tema: MENÚ DÍA)
    # Usa match/case para un menú según día ("lunes"..."domingo").
    # Muestra un plato distinto para 3 días y un mensaje genérico para el resto.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 7 · LABORATORIO IA (Condicionales creativos)
# =========================================================================================
def seccion_7_ia():
    encabezado("SECCIÓN 7 · Laboratorio IA (Condicionales creativos)")

    # * PROMPT KIT (copia/pega en ChatGPT)
    # 1) PROMPT BREVE:
    #    "Eres profesor de Python. Genera un programa de 25–40 líneas que use condicionales
    #     (if/elif/else), and/or/not y valores truthy/falsy. Tema: 'calculadora de descuentos
    #     con cupones'. Requisitos: variables en español, comentarios con # * y # TODO, sin
    #     funciones avanzadas ni librerías. Devuélveme SOLO código Python."
    #
    # 2) PROMPT ALTERNATIVO:
    #    "Crea un verificador de acceso a un concierto con edad, entrada, y hora (toque de queda).
    #     Usa if/elif/else y un ternario. Sin librerías, 30 líneas aprox. Solo código Python."
    #
    # 3) PROMPT DE MEJORA:
    #    "Mejora este código para manejar entradas vacías (truthy/falsy) y añade un resumen
    #     final de una sola línea. Manténlo por debajo de 40 líneas."

    # * DEMO opcional
    if IA_DEMO:
        # Mini-prototipo: validador de oferta
        precio = 25.0
        tiene_cupon = True
        aplica = "OFERTA" if (precio >= 20 and tiene_cupon) else "SIN OFERTA"
        print(f"Precio {precio}€ | Cupón: {tiene_cupon} → {aplica}")

    # TODO: (Tema: PROGRAMA PROPUESTO POR IA)
    # 1) Pide a ChatGPT el programa con el PROMPT KIT (elige tema).
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
    encabezado("AUTOEVALUACIÓN FINAL · Control de acceso + resumen de compra")

    # TODO: (ENUNCIADO)
    # 1) Pide/captura:
    #    - edad (int), tiene_entrada (s/n), total_compra (float), cupon (s/n), username (str)
    # 2) Lógica:
    #    - Si edad >= 18 y tiene_entrada → "Acceso concedido", si no → motivo(s) de denegación.
    #    - Si username está vacío → "Usuario requerido".
    #    - Si total_compra >= 30 o cupon == 's' → "Envío gratis", si no → "Envío 3.99€". (puede ser ternario)
    # 3) Usa truthy/falsy donde tenga sentido (username, listas vacías si las necesitas).
    # 4) (Opcional) Usa match/case para clasificar un tipo de usuario: admin, editor, invitado.
    # 5) Muestra una línea final tipo dashboard:
    #    "Usuario <username> | Acceso:<sí/no> | Total:<importe> | Envío:<gratis/3.99€>"
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  MENÚ PRINCIPAL
# =========================================================================================
def menu():
    while True:
        print_firma()
        print("MENÚ · Elige una opción")
        print("  1) if básico")
        print("  2) if / elif / else")
        print("  3) Condiciones compuestas + anidados")
        print("  4) Truthy / Falsy + bool()")
        print("  5) Operador ternario")
        print("  6) match / case (opcional)")
        print("  7) Laboratorio IA (Condicionales)")
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
