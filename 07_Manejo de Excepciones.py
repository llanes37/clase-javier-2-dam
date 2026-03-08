# =========================================================================================
#  🐍 PYTHON CLASE 7 — MANEJO DE EXCEPCIONES (try/except/else/finally, raise, custom) + IA
#  ────────────────────────────────────────────────────────────────────────────────────────
#  📘 En esta clase practicarás:
#    * try / except (básico)
#    * Capturas específicas, múltiples except y jerarquía de errores
#    * else y finally (código que corre si NO hubo excepción / siempre)
#    * Lanzar errores con raise y validar entradas
#    * Excepciones personalizadas (clases que heredan de Exception)
#    * Patrones habituales de validación y reintento seguro
#    * (Opcional) assert y buenas prácticas
#    * Laboratorio IA: mini-programa robusto con entradas del usuario
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
#  SECCIÓN 1 · try/except básico
# =========================================================================================
def seccion_1():
    encabezado("SECCIÓN 1 · try/except básico")

    # * TEORÍA
    # try:
    #     # código que puede fallar
    # except TipoDeError:
    #     # qué hacer si ocurre ese error
    # Captura solo lo que esperas: evita except sin tipo.

    # * DEMO
    texto = safe_input("Introduce un número entero: ", str, default="abc")
    try:
        n = int(texto)
        print("OK, entero:", n)
    except ValueError:
        print("Ese texto no es un entero.")

    # TODO: (Tema: DIVISIÓN SEGURA)
    # Pide dos números y divide a/b. Captura ValueError (conversiones) y ZeroDivisionError.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 2 · Múltiples except y jerarquía de errores
# =========================================================================================
def seccion_2():
    encabezado("SECCIÓN 2 · Múltiples except y jerarquía")

    # * TEORÍA
    # El orden importa: captura primero errores específicos y luego más generales.
    # except ValueError as e:  (te da el mensaje original en 'e')

    # * DEMO
    datos = safe_input("Introduce un índice (0..2): ", str, default="1")
    arr = [10, 20, 30]
    try:
        idx = int(datos)                 # ValueError si no es número
        print("Elemento:", arr[idx])     # IndexError si fuera de rango
    except ValueError as e:
        print("Conversión inválida:", e)
    except IndexError as e:
        print("Índice fuera de rango:", e)

    # TODO: (Tema: DICCIONARIO SEGURO)
    # Dado un dict {'a':1, 'b':2}, pide una clave y muestra su valor.
    # Captura KeyError (si no existe) y ValueError (si formateas la clave a int por error).
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 3 · else y finally
# =========================================================================================
def seccion_3():
    encabezado("SECCIÓN 3 · else y finally")

    # * TEORÍA
    # try:
    #     ...
    # except ...:
    #     ...
    # else:      # se ejecuta si NO hubo excepción
    #     ...
    # finally:   # se ejecuta SIEMPRE (haya o no error), ideal para limpiar/ cerrar recursos

    # * DEMO (simulación de apertura/cierre de "recurso")
    recurso_abierto = False
    try:
        recurso_abierto = True
        print("Recurso abierto")
        x = 10 / safe_input("Divisor (0=fallo): ", int, default=2)
        print("Resultado:", x)
    except ZeroDivisionError:
        print("No puedes dividir entre cero.")
    else:
        print("Operación completada sin errores.")
    finally:
        if recurso_abierto:
            print("Cerrando recurso...")
            recurso_abierto = False

    # TODO: (Tema: LOGIN SIMPLE)
    # Simula un login: pide usuario y contraseña (por defecto: usuario 'admin', pass '1234').
    # Si están vacíos, lanza ValueError (lo veremos en la siguiente sección).
    # Aquí solo practica else/finally: muestra "Login OK" en else y "Cerrando sesión..." en finally.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 4 · raise (lanzar excepciones) y validación
# =========================================================================================
def seccion_4():
    encabezado("SECCIÓN 4 · raise y validación")

    # * TEORÍA
    # raise ValueError("mensaje descriptivo")
    # Lanza un error cuando una precondición no se cumple.

    # * DEMO
    def leer_edad(texto: str) -> int:
        if texto.strip() == "":
            raise ValueError("La edad es requerida")
        edad = int(texto)  # puede lanzar ValueError
        if edad < 0:
            raise ValueError("La edad no puede ser negativa")
        return edad

    try:
        edad = leer_edad(safe_input("Edad: ", str, default=""))
        print("Edad válida:", edad)
    except ValueError as e:
        print("Error de validación:", e)

    # TODO: (Tema: PRECIO VÁLIDO)
    # Implementa leer_precio(texto) que lance ValueError si vacío o < 0.
    # Úsalo dentro de un try/except para mostrar el precio válido o el mensaje de error.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 5 · Excepciones personalizadas
# =========================================================================================
def seccion_5():
    encabezado("SECCIÓN 5 · Excepciones personalizadas")

    # * TEORÍA
    # class MiError(Exception):
    #     pass
    # Útil para señalar situaciones propias de tu dominio con mensajes claros.

    # * DEMO
    class SaldoInsuficiente(Exception):
        """# * Error de negocio cuando no hay saldo para una operación."""
        pass

    class Cuenta:
        def __init__(self, saldo: float = 0.0):
            self.saldo = saldo

        def pagar(self, importe: float):
            if importe > self.saldo:
                raise SaldoInsuficiente(f"Saldo {self.saldo:.2f} < Importe {importe:.2f}")
            self.saldo -= importe
            return self.saldo

    cuenta = Cuenta(20.0)
    try:
        nuevo = cuenta.pagar(25.0)
        print("Pago OK. Saldo:", nuevo)
    except SaldoInsuficiente as e:
        print("No se pudo pagar:", e)

    # TODO: (Tema: STOCK AGOTADO)
    # Crea error personalizado StockAgotado y función vender(stock, unidades) que lance StockAgotado
    # si unidades > stock. Maneja la excepción e imprime un mensaje útil.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 6 · Patrones de validación / reintento seguro
# =========================================================================================
def seccion_6():
    encabezado("SECCIÓN 6 · Patrones de validación / reintento")

    # * TEORÍA
    # Patrón reintento:
    # for _ in range(intentos_max):
    #     try:  ...  break
    #     except:    avisar y seguir
    # else:  # si no hiciste break
    #     # agotados los intentos

    # * DEMO · pedir entero con 3 intentos
    intentos_max = 3
    n = None
    for intento in range(1, intentos_max + 1):
        try:
            n = int(safe_input(f"Introduce entero (intento {intento}/{intentos_max}): ", str, default="x"))
            break
        except ValueError:
            print("No es un entero.")
    else:
        print("Agotados los intentos.")
    print("Valor introducido:", n)

    # TODO: (Tema: LECTURA FLOAT)
    # Implementa pedir_float(mensaje, intentos=3) con el patrón anterior. Pruébalo leyendo un precio.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 7 · (Opcional) assert y buenas prácticas
# =========================================================================================
def seccion_7():
    encabezado("SECCIÓN 7 · assert (opcional) y buenas prácticas")

    # * TEORÍA
    # assert condición, "mensaje"
    # Lanza AssertionError si la condición es False. Útil para verificar invariantes en desarrollo.
    # No usar para lógica de usuario final (puede deshabilitarse con -O).

    # * DEMO
    def dividir(a: float, b: float) -> float:
        assert b != 0, "b no puede ser 0"
        return a / b

    try:
        print(dividir(10, 2))
        print(dividir(10, 0))  # AssertionError
    except AssertionError as e:
        print("Fallo de aserción:", e)

    # TODO: (Tema: VERIFICAR LISTA)
    # Escribe una función media(lista) que haga assert lista, "Lista vacía".
    # Si la lista es válida, devuelve la media. Prueba con [] y con [1,2,3].
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 8 · Laboratorio IA (programa robusto con entradas)
# =========================================================================================
def seccion_8_ia():
    encabezado("SECCIÓN 8 · Laboratorio IA (programa robusto con entradas)")

    # * PROMPT KIT (copia/pega en ChatGPT)
    # 1) PROMPT BREVE:
    #    "Eres profesor de Python. Genera un programa de 30–45 líneas que pida datos por
    #     teclado (nombre, unidades, precio) y calcule un total, aplicando cupones. Debe usar
    #     try/except (ValueError y ZeroDivisionError), else/finally y al menos un raise con
    #     mensaje claro. Solo código Python, sin librerías."
    #
    # 2) PROMPT ALTERNATIVO:
    #    "Crea un conversor de divisas que valide entradas con reintentos (3) y lance
    #     ValueError cuando el importe sea negativo. Añade una excepción personalizada
    #     TipoMonedaDesconocido. Solo código Python."
    #
    # 3) PROMPT DE MEJORA:
    #    "Mejora el programa para imprimir un resumen final en una línea y separar la lógica
    #     en 2–3 funciones con docstrings. Mantén 35–50 líneas."

    # * DEMO opcional
    if IA_DEMO:
        try:
            unidades = int("x")  # forzamos ValueError
        except ValueError:
            print("Demo IA → Manejando conversión inválida correctamente.")

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
    encabezado("AUTOEVALUACIÓN FINAL · Caja registradora robusta")

    # TODO: (ENUNCIADO)
    # Implementa una mini “caja registradora” con:
    #
    # 1) Función leer_float(msg) con reintento (3) y ValueError controlado (usa try/except).
    # 2) Clase DescuentoInvalido(Exception) para cupones fuera de 0–100%.
    # 3) Función total_con_descuento(base: float, unidades: int, desc: float) -> float
    #    - Lanza DescuentoInvalido si desc está fuera de rango.
    #    - Lanza ValueError si base<0 o unidades<=0.
    # 4) Flujo principal:
    #    - Pide base, unidades, descuento. Calcula total con try/except/else/finally.
    #    - En finally imprime "Cierre de operación" siempre.
    # 5) Línea final tipo dashboard:
    #    "Base:<€> | Unidades:<n> | Desc:<%> | Total:<€> | Estado:<OK/ERROR>"
    #
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  MENÚ PRINCIPAL
# =========================================================================================
def menu():
    while True:
        print_firma()
        print("MENÚ · Elige una opción")
        print("  1) try/except básico")
        print("  2) Múltiples except y jerarquía")
        print("  3) else y finally")
        print("  4) raise y validación")
        print("  5) Excepciones personalizadas")
        print("  6) Patrones de validación / reintento")
        print("  7) assert (opcional)")
        print("  8) Laboratorio IA")
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
