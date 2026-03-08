# =========================================================================================
#  🧑‍🎓 PYTHON · PLANTILLA DEL ALUMNO — Clase 7
#  Tema: Manejo de Excepciones (try/except/else/finally, múltiples except, raise, custom,
#        reintento, assert) + práctica
#  Cómo usar este archivo:
#   1) Lee cada sección (Objetivos + Guía) y completa las ZONAS DEL ALUMNO (TODO).
#   2) Ejecuta este archivo y usa el menú para probar tus soluciones.
#   3) Ejercicios genéricos y claros, sin ejemplos resueltos en las secciones.
# =========================================================================================

from typing import Any, Callable

# * Conmutadores de ejecución -------------------------------------------------------------
RUN_INTERACTIVE = True   # True: menú interactivo; False: ejecuta TODO una vez y sale
PAUSE = False            # Pausa tras cada sección (útil en clase)

# * Utilidades ---------------------------------------------------------------------------
def pause(msg: str = "Pulsa Enter para continuar..."):
	if not PAUSE:
		return
	try:
		input(msg)
	except EOFError:
		pass

def encabezado(titulo: str):
	print("\n" + "=" * 80)
	print(titulo)
	print("=" * 80)

def safe_input(prompt: str, caster: Callable[[str], Any], default: Any) -> Any:
	"""
	Convierte la entrada al tipo deseado; si falla o no hay input, devuelve 'default'.
	Si RUN_INTERACTIVE=False, devuelve directamente el valor por defecto.
	"""
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

# =========================================================================================
#  SECCIÓN 1 · try/except básico
# =========================================================================================
def seccion_1_try_except():
	encabezado("SECCIÓN 1 · try/except básico")
	print("Objetivo: capturar errores esperados para que el programa no se detenga.\n")

	# * Teoría clave
	# * Captura errores concretos (p.ej., ValueError) y ofrece mensajes claros.

	# ? Cómo funciona el ejercicio
	# - División segura: pide dos números y divide a/b.
	# - Captura ValueError y ZeroDivisionError con mensajes útiles.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa la división segura con try/except.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 2 · Múltiples except y jerarquía
# =========================================================================================
def seccion_2_multiples_except():
	encabezado("SECCIÓN 2 · Múltiples except y jerarquía")
	print("Objetivo: usar varios except específicos (de más específico a más general).\n")

	# * Teoría clave
	# * Ordena los except de específico a general; opcionalmente captura Exception como comodín.

	# ? Cómo funciona el ejercicio
	# - Diccionario seguro: dado {'a':1, 'b':2}, pide clave y muestra valor.
	# - Captura KeyError y ValueError (si tratas mal la clave).
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa los except adecuados y muestra mensajes claros.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 3 · else y finally
# =========================================================================================
def seccion_3_else_finally():
	encabezado("SECCIÓN 3 · else y finally")
	print("Objetivo: usar else si NO hubo error y finally para cerrar siempre.\n")

	# * Teoría clave
	# * else corre solo si no hubo excepción; finally corre siempre (ideal para limpiar recursos).

	# ? Cómo funciona el ejercicio
	# - Login simple: pide usuario y contraseña ('admin'/'1234').
	# - Si OK → else: print("Login OK"); en finally: print("Cerrando sesión...").
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa try/except/else/finally según el enunciado.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 4 · raise (validación) y excepciones personalizadas
# =========================================================================================
def seccion_4_raise_custom():
	encabezado("SECCIÓN 4 · raise (validación) y excepciones personalizadas")
	print("Objetivo: lanzar errores cuando se violen condiciones y definir custom exceptions.\n")

	# * Teoría clave
	# * raise ValueError(...) para validar. Custom = class MiError(Exception): pass

	# ? Cómo funciona el ejercicio
	# - leer_precio(texto) → lanza ValueError si vacío o <0.
	# - class StockAgotado(Exception) y vender(stock, unidades) que la lance si unidades>stock.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa la función, la clase de excepción y una pequeña demostración.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 5 · Reintento seguro y assert (opcional)
# =========================================================================================
def seccion_5_reintento_assert():
	encabezado("SECCIÓN 5 · Reintento seguro y assert (opcional)")
	print("Objetivo: reintentar N veces ante errores y usar assert en desarrollo.\n")

	# * Teoría clave
	# * for intentos: try/except ... break · else del for si no hubo break.
	# * assert solo en desarrollo para condiciones internas.

	# ? Cómo funciona el ejercicio
	# - pedir_float(msg, intentos=3) que reintente hasta N o falle con mensaje.
	# - media(lista) con assert lista, "Lista vacía".
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa pedir_float y media con assert; prueba ambos casos.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 6 · Autoevaluación final (caja registradora robusta)
# =========================================================================================
def seccion_6_autoevaluacion():
	encabezado("SECCIÓN 6 · Autoevaluación final (caja registradora robusta)")
	print("Objetivo: combinar try/except múltiples, else/finally, raise y custom exceptions.\n")

	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# 1) leer_float(msg) con reintento (3) y ValueError controlado.
	# 2) class DescuentoInvalido(Exception) para cupones fuera 0–100%.
	# 3) total_con_descuento(base, unidades, desc):
	#    - raise DescuentoInvalido si desc fuera de rango.
	#    - raise ValueError si base<0 o unidades<=0.
	# 4) Flujo principal con try/except/else/finally.
	# 5) Resumen final (1 línea) tipo dashboard.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  MENÚ para ejecutar tus ejercicios por secciones
# =========================================================================================
def menu():
	# Modo no interactivo: ejecuta TODO una vez y sale (evita bucles infinitos)
	if not RUN_INTERACTIVE:
		seccion_1_try_except()
		seccion_2_multiples_except()
		seccion_3_else_finally()
		seccion_4_raise_custom()
		seccion_5_reintento_assert()
		seccion_6_autoevaluacion()
		return

	# Modo interactivo: menú con bucle y opción de salida
	while True:
		print("\n===== MENÚ DEL ALUMNO · Clase 7 (Excepciones) =====")
		print("  1) try/except básico")
		print("  2) Múltiples except y jerarquía")
		print("  3) else y finally")
		print("  4) raise y custom exceptions")
		print("  5) Reintento y assert")
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
			break
		elif op == 1:
			seccion_1_try_except(); pause()
		elif op == 2:
			seccion_2_multiples_except(); pause()
		elif op == 3:
			seccion_3_else_finally(); pause()
		elif op == 4:
			seccion_4_raise_custom(); pause()
		elif op == 5:
			seccion_5_reintento_assert(); pause()
		elif op == 6:
			seccion_6_autoevaluacion(); pause()
		elif op == 7:
			seccion_1_try_except(); seccion_2_multiples_except(); seccion_3_else_finally(); seccion_4_raise_custom(); seccion_5_reintento_assert(); seccion_6_autoevaluacion(); pause()
		else:
			print("! Elige una opción del 0 al 7.")


if __name__ == "__main__":
	menu()

# -------------------------------------------------------------------------------------------
# * SECCIÓN 1: INTRODUCCIÓN AL MANEJO DE EXCEPCIONES EN PYTHON
# ? En programación, no todo sale como se espera. A veces, ocurren errores que pueden hacer 
# ? que un programa falle. Python nos permite manejar esos errores usando `try` y `except`.
# ? De esta forma, el programa sigue funcionando sin bloquearse.
# -------------------------------------------------------------------------------------------

# * EJEMPLO BÁSICO DE TRY Y EXCEPT:
# ? Imagina que estás trabajando con un sistema de control de dispositivos electrónicos.
# ? A veces, un usuario puede introducir un dato incorrecto (por ejemplo, letras en lugar de números).
# ? Usamos `try` para intentar convertir un valor de texto en número y `except` para manejar cualquier error.

# TODO: Escribe el código que intente convertir el ID de un dispositivo en un número entero
# TODO: Si ocurre un error, muestra un mensaje de "ID no válido".


# -------------------------------------------------------------------------------------------
# * SECCIÓN 2: MANEJO DE MÚLTIPLES EXCEPCIONES
# ? A veces, pueden ocurrir diferentes tipos de errores. Por ejemplo, el usuario podría intentar 
# ? introducir un valor inválido o realizar una operación que no es posible (como dividir por cero).
# ? Podemos manejar diferentes tipos de errores usando varios bloques `except`.
# -------------------------------------------------------------------------------------------

# * EJEMPLO: Control de energía en dispositivos.
# ? Vamos a pedir al usuario que introduzca la cantidad de energía que quiere asignar a un dispositivo.
# ? Pero, ¿qué pasa si el usuario introduce un valor incorrecto o intenta asignar 0 energía?

# TODO: Escribe el código para capturar diferentes tipos de errores, como:
# - Valor no válido (si el usuario introduce texto en lugar de números)
# - Dividir por cero (si el usuario introduce 0 en una operación que lo prohiba)


# -------------------------------------------------------------------------------------------
# * SECCIÓN 3: USO DEL BLOQUE FINALLY
# ? El bloque `finally` siempre se ejecuta al final de un bloque `try` y `except`, 
# ? incluso si ocurre un error. Es útil para asegurarte de que algunas acciones siempre se realicen,
# ? como apagar un dispositivo o guardar información crítica.
# -------------------------------------------------------------------------------------------

# * EJEMPLO: Imagina que estás operando un sistema de seguridad. Queremos asegurarnos de que,
# ? aunque ocurra un error, el sistema siempre se apague de forma segura al final.
# TODO: Implementa el código para usar `finally` en un ejemplo donde siempre se cierre el sistema,
# TODO: sin importar si ocurre un error.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 4: CAPTURAR TODAS LAS EXCEPCIONES
# ? En algunos casos, no podemos predecir qué tipo de error ocurrirá. En estos casos, 
# ? podemos usar `except Exception` para capturar cualquier error, sin importar cuál sea.
# -------------------------------------------------------------------------------------------

# * EJEMPLO: Monitorización de una red.
# ? Si estás monitorizando la actividad de una red y ocurre un error inesperado, 
# ? es importante que el sistema no se detenga por completo.

# TODO: Escribe el código para manejar cualquier error inesperado usando `except Exception`.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 5: LANZAR EXCEPCIONES PERSONALIZADAS
# ? En ciertos casos, es útil crear y lanzar tus propios errores o excepciones, 
# ? especialmente cuando necesitas validar ciertos datos antes de continuar.
# ? Usamos `raise` para lanzar excepciones personalizadas.
# -------------------------------------------------------------------------------------------

# * EJEMPLO: Validación de acceso a un sistema seguro.
# ? Vamos a comprobar si un usuario tiene permisos para acceder a un sistema militar. 
# ? Si no tiene el nivel adecuado, lanzaremos una excepción personalizada que indique que el acceso no está permitido.

# TODO: Escribe el código para validar los permisos del usuario y lanzar una excepción personalizada 
# TODO: si no tiene el nivel necesario.


# -------------------------------------------------------------------------------------------
# * AUTOEVALUACIÓN FINAL:
# 1. Solicita al usuario que introduzca el ID de un dispositivo y el número de horas que ha estado activo.
# 2. Captura los posibles errores:
#    - Si el usuario introduce un valor no válido, muestra un mensaje de error adecuado.
#    - Si intenta dividir por cero o realizar otra operación no válida, muestra el error correspondiente.
# 3. Asegúrate de que al final, el programa siempre muestra "Operación completada" usando `finally`.
# -------------------------------------------------------------------------------------------

# TODO: Escribe aquí el código de la autoevaluación que maneje los errores y siempre finalice la operación.
