# =========================================================================================
#  🐍 PYTHON CLASE 4 — FUNCIONES (BÁSICO) · sin tipos ni temas avanzados
#  ────────────────────────────────────────────────────────────────────────────────────────
#  📘 En esta clase practicarás:
#    * Funciones sin parámetros (solo ejecutan una tarea)
#    * Funciones con parámetros (posicionales)
#    * return (devolver valores) y reutilizar resultados
#    * Parámetros con valores por defecto · uso por nombre (keyword)
#    * Scope básico (variables locales vs. externas) y patrón “entradas→salidas”
#    * Buenas prácticas: funciones puras vs. con efectos, nombres claros
#    * Laboratorio IA y Autoevaluación (mezcla de todo)
#
#  🎨 Better Comments:
#    # ! importante   ·  # * definición/foco   ·  # ? idea/nota
#    # TODO: práctica  ·  # NOTE: apunte útil   ·  # // deprecado
# =========================================================================================

# * Configuración general ---------------------------------------------------------------
RUN_INTERACTIVE = True   # True: pide datos por teclado; False: usa valores por defecto
PAUSE = False            # Pausa al acabar cada sección
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

def safe_input(prompt, caster, default):
    """# * Convierte la entrada al tipo deseado; si falla o no hay input, devuelve 'default'."""
    if not RUN_INTERACTIVE:
        return default
    try:
        raw = input(prompt)
        if raw.strip() == "":
            return default
        return caster(raw)
    except Exception:
        print("! Entrada no válida; usando valor por defecto.")
        return default

def encabezado(titulo):
    print("\n" + "=" * 80)
    print(titulo)
    print("=" * 80)

# =========================================================================================
#  SECCIÓN 1 · Funciones SIN parámetros (una tarea concreta)
# =========================================================================================
def seccion_1():
    encabezado("SECCIÓN 1 · Funciones SIN parámetros")

    # * TEORÍA
    # def nombre():
    #     <bloque>             # hace algo (p. ej. imprimir), no necesita datos externos
    # Llamada: nombre()

    # * DEMO
    def linea():
        print("-" * 40)

    def saludar():
        print("¡Bienvenido/a al curso de Python!")

    saludar()
    linea()
    print("Este mensaje va debajo de una línea separadora.")
    linea()

    # TODO: (Tema: BANNER SENCILLO)
    # Crea una función banner() que imprima 3 líneas:
    #   "======"
    #   "  Hola  "
    #   "======"
    # Llama a la función 2 veces.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # def banner():
    #     ...
    # banner()
    # banner()

# =========================================================================================
#  SECCIÓN 2 · Funciones CON parámetros (posicionales)
# =========================================================================================
def seccion_2():
    encabezado("SECCIÓN 2 · Funciones CON parámetros")

    # * TEORÍA
    # def nombre(par1, par2):
    #     <usa par1 y par2>
    # Llamada: nombre(valor1, valor2)

    # * DEMO
    def saludar_a(nombre):
        print(f"Hola, {nombre} 👋")

    def repetir(texto, veces):
        for _ in range(veces):
            print(texto)

    nombre = safe_input("Tu nombre: ", str, default="Invitado")
    saludar_a(nombre)
    repetir("Aprendiendo funciones...", 2)

    # TODO: (Tema: MOSTRAR CUADRÍCULA)
    # Crea mostrar_cuadricula(simbolo, ancho) que imprima una línea con 'simbolo' repetido 'ancho' veces.
    # Llama 3 veces con distintos parámetros.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # def mostrar_cuadricula(simbolo, ancho):
    #     ...
    # mostrar_cuadricula("#", 8)
    # mostrar_cuadricula("*", 5)
    # mostrar_cuadricula("=", 10)

# =========================================================================================
#  SECCIÓN 3 · return (devolver valores) y reutilizarlos
# =========================================================================================
def seccion_3():
    encabezado("SECCIÓN 3 · return (devolver valores)")

    # * TEORÍA
    # def f(x):
    #     resultado = x * x
    #     return resultado
    # Usar el valor: y = f(5)

    # * DEMO
    def cuadrado(n):
        return n * n

    def suma(a, b):
        return a + b

    n = safe_input("Número para elevar al cuadrado: ", int, default=4)
    print("Cuadrado:", cuadrado(n))
    print("Suma 2+3:", suma(2, 3))

    # TODO: (Tema: PRECIO CON IVA)
    # Escribe precio_con_iva(base, iva) que devuelva base * (1 + iva/100).
    # Imprime el resultado para base=100, iva=21.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # def precio_con_iva(base, iva):
    #     ...
    # print(precio_con_iva(100, 21))

# =========================================================================================
#  SECCIÓN 4 · Parámetros con valores por defecto · uso por nombre
# =========================================================================================
def seccion_4():
    encabezado("SECCIÓN 4 · Parámetros por defecto · uso por nombre")

    # * TEORÍA
    # Valores por defecto:
    #   def saludar(nombre="Invitado"):
    #       print("Hola", nombre)
    # Uso por nombre (keyword):
    #   imprimir_linea(texto="Hola", veces=3)

    # * DEMO
    def saludo(nombre="Invitado"):
        print(f"Hola, {nombre}")

    def precio_final(base, iva=21, descuento=0):
        return base * (1 + iva/100) * (1 - descuento/100)

    saludo()
    saludo("Alicia")
    print("precio_final(100) →", precio_final(100))
    print("precio_final(base=200, descuento=10) →", precio_final(base=200, descuento=10))

    # TODO: (Tema: MENSAJE REPETIDO)
    # Crea repetir_msg(msg="Hola", veces=2) que imprima msg tantas veces.
    # Llama por posición y por nombre (keyword).
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # def repetir_msg(msg="Hola", veces=2):
    #     ...
    # repetir_msg("Python", 3)
    # repetir_msg(veces=2, msg="Mundo")

# =========================================================================================
#  SECCIÓN 5 · Scope básico (variables locales vs. externas)
# =========================================================================================
def seccion_5():
    encabezado("SECCIÓN 5 · Scope básico (local vs. externo)")

    # * TEORÍA
    # Las variables dentro de una función son LOCALES a esa función.
    # Buen patrón: pasar valores de entrada y devolver resultados (evita usar 'global').

    # * DEMO · contador sin globales
    def incrementar(contador, paso=1):
        contador = contador + paso
        return contador

    c = 0
    c = incrementar(c)        # 1
    c = incrementar(c, 2)     # 3
    print("Contador:", c)

    # * DEMO · local vs. externo
    x = 10
    def duplicar_local(x):
        x = x * 2    # esta 'x' es local; no cambia la 'x' externa
        return x

    print("x externa:", x, "| x duplicada dentro:", duplicar_local(x), "| x externa tras llamar:", x)

    # TODO: (Tema: AHORRO)
    # Crea agregar_saldo(saldo, cantidad) que devuelva el nuevo saldo.
    # Empieza con saldo=0 y realiza 3 operaciones (dos ingresos y un gasto). Muestra el saldo final.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # def agregar_saldo(saldo, cantidad):
    #     ...
    # saldo = 0
    # saldo = agregar_saldo(saldo, 20)
    # saldo = agregar_saldo(saldo, -5)
    # saldo = agregar_saldo(saldo, 10)
    # print("Saldo final:", saldo)

# =========================================================================================
#  SECCIÓN 6 · Buenas prácticas (puras vs. con efectos) + mini guía
# =========================================================================================
def seccion_6():
    encabezado("SECCIÓN 6 · Buenas prácticas con funciones")

    # * TEORÍA (mini guía)
    # - Una función = una sola tarea clara.
    # - Nombres de verbos: calcular_total, obtener_media, mostrar_menu...
    # - Preferir devolver valores (funciones “puras”) frente a imprimir dentro.
    # - Si imprimes, que sea por decisión de “presentación”, no de “cálculo”.

    # * DEMO · dos formas de hacer lo mismo
    def area_rect_print(base, altura):
        print("Área:", base * altura)  # efecto (imprimir)

    def area_rect(base, altura):
        return base * altura           # pura (devuelve valor)

    area_rect_print(3, 4)
    resultado = area_rect(3, 4)
    print("Área (reutilizable):", resultado, "→ puedo usarlo en otra operación:", resultado + 10)

    # TODO: (Tema: MEDIA)
    # Implementa media(a, b, c) que devuelva la media de 3 números.
    # Úsala para imprimir un mensaje: "La media es X" con 2 decimales.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------
    # def media(a, b, c):
    #     ...
    # m = media(5, 7, 9)
    # print(f"La media es {m:.2f}")

# =========================================================================================
#  SECCIÓN 7 · Laboratorio IA (funciones sencillas)
# =========================================================================================
def seccion_7_ia():
    encabezado("SECCIÓN 7 · Laboratorio IA (funciones sencillas)")

    # * PROMPT KIT (copia/pega en ChatGPT)
    # 1) PROMPT BREVE:
    #    "Eres profesor de Python. Genera un programa de 20–30 líneas con 4–5 funciones
    #     simples (sin tipos ni temas avanzados) que calcule:
    #     - precio_final(base, iva=21)  · aplicar_descuento(total, dto)
    #     - sumar(a,b)  · es_par(n)  · imprimir_ticket(total)
    #     Incluye comentarios con # * y # TODO. Solo código Python."
    #
    # 2) PROMPT ALTERNATIVO:
    #    "Crea funciones para una mini-calculadora: sumar/restar/multiplicar/dividir (con if para
    #     división por 0) y una función mostrar_menu(). 20–30 líneas. Sin librerías."
    #
    # 3) PROMPT DE MEJORA:
    #    "Refactoriza para que las funciones devuelvan valores (puras) y solo imprimir en una capa final."

    # * DEMO opcional
    if IA_DEMO:
        def es_par(n): return n % 2 == 0
        print("Demo IA → 8 par?:", es_par(8))

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
#  AUTOEVALUACIÓN FINAL (mezcla de todo · funciones básicas)
# =========================================================================================
def autoevaluacion():
    encabezado("AUTOEVALUACIÓN FINAL · Calculadora simple + precios")

    # TODO: (ENUNCIADO)
    # Implementa y prueba estas funciones:
    #
    # 1) mostrar_titulo()                 → imprime "CALCULADORA" con un marco.
    # 2) sumar(a,b) / restar(a,b) / multiplicar(a,b) / dividir(a,b)  (si b==0, devuelve "Error").
    # 3) precio_con_iva(base, iva=21)     → devuelve el total.
    # 4) total_compra(p1, p2, p3)         → recibe 3 precios y devuelve la suma.
    #
    # Demostración:
    #  - Llama a mostrar_titulo()
    #  - Calcula y muestra: sumar(5,7), dividir(10,0), precio_con_iva(100), total_compra(3,4,5)
    #  - Imprime una última línea tipo dashboard:
    #    "Suma: <..> | Div: <..> | IVA: <..> | Total: <..>"
    #
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------

# =========================================================================================
#  MENÚ PRINCIPAL
# =========================================================================================
def menu():
    while True:
        print_firma()
        print("MENÚ · Elige una opción")
        print("  1) Funciones SIN parámetros")
        print("  2) Funciones CON parámetros")
        print("  3) return (devolver valores)")
        print("  4) Parámetros por defecto · uso por nombre")
        print("  5) Scope básico (local vs. externo)")
        print("  6) Buenas prácticas")
        print("  7) Laboratorio IA")
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
