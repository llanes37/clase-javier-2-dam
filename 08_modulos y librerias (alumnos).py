# =========================================================================================
#  🧑‍🎓 PYTHON · PLANTILLA DEL ALUMNO — Clase 8
#  Tema: Módulos y Librerías (import, alias, from, stdlib: math/datetime/random/time,
#        módulos personalizados) + autoevaluación
#  Cómo usar este archivo:
#   1) Lee cada sección (Objetivos + Guía) y completa las ZONAS DEL ALUMNO (TODO).
#   2) Ejecuta este archivo y usa el menú para probar tus soluciones.
#   3) Usa ejemplos genéricos y claros; sin soluciones copiadas en las secciones.
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
#  SECCIÓN 1 · Introducción a módulos: import, alias y from
# =========================================================================================
def seccion_1_intro_modulos():
	encabezado("SECCIÓN 1 · Introducción a módulos: import, alias y from")
	print("Objetivo: entender cómo traer funcionalidades de otros archivos o librerías.\n")

	# * Teoría clave
	# * import modulo · import modulo as m · from modulo import funcion
	# * La stdlib de Python incluye muchos módulos listos para usar.

	# ? Cómo funciona el ejercicio
	# - Escribe tres líneas de import distintos: import, alias y from ... import ...
	# - No hace falta ejecutar nada todavía; solo practica los import.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Añade aquí ejemplos de import (en comentarios o reales) para practicar.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 2 · math: operaciones matemáticas
# =========================================================================================
def seccion_2_math():
	encabezado("SECCIÓN 2 · math: operaciones matemáticas")
	print("Objetivo: usar funciones comunes como sqrt, sin y conversión a radianes.\n")

	# * Teoría clave
	# * math.sqrt(x)  ·  math.pow(a,b)  ·  math.radians(grados) y math.sin(radianes)

	# ? Cómo funciona el ejercicio
	# - Calcula la raíz cuadrada de 16.
	# - Calcula el seno de 90 grados (pista: radians(90) → sin(...)).
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Importa math y realiza los cálculos anteriores imprimiendo los resultados.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 3 · datetime: fechas y horas
# =========================================================================================
def seccion_3_datetime():
	encabezado("SECCIÓN 3 · datetime: fechas y horas")
	print("Objetivo: obtener fecha/hora actual, crear fechas y calcular diferencias.\n")

	# * Teoría clave
	# * from datetime import datetime, date, timedelta  ·  datetime.now()

	# ? Cómo funciona el ejercicio
	# - Muestra fecha y hora actual.
	# - Crea una fecha personalizada (por ejemplo, 1 enero 2025) y muestra cuántos días faltan.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa los imports y las operaciones de fecha/tiempo indicadas.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 4 · random: números y elecciones aleatorias
# =========================================================================================
def seccion_4_random():
	encabezado("SECCIÓN 4 · random: números y elecciones aleatorias")
	print("Objetivo: generar valores aleatorios de forma sencilla.\n")

	# * Teoría clave
	# * random.randint(a,b)  ·  random.choice(lista)

	# ? Cómo funciona el ejercicio
	# - Genera un entero aleatorio entre 1 y 100.
	# - Elige un color al azar de ["rojo","verde","azul","amarillo"].
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Importa random y realiza las operaciones; imprime el resultado.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 5 · time: pausas y medición simple
# =========================================================================================
def seccion_5_time():
	encabezado("SECCIÓN 5 · time: pausas y medición simple")
	print("Objetivo: pausar ejecuciones y medir tiempos sencillos.\n")

	# * Teoría clave
	# * time.sleep(segundos)  ·  time.perf_counter() para medir duración.

	# ? Cómo funciona el ejercicio
	# - Pausa el programa 2 segundos.
	# - (Opcional) Mide el tiempo que tarda en ejecutarse una pequeña operación.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Importa time, usa sleep y (si quieres) perf_counter para medir.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 6 · Módulos personalizados (crear y usar)
# =========================================================================================
def seccion_6_modulos_personalizados():
	encabezado("SECCIÓN 6 · Módulos personalizados (crear y usar)")
	print("Objetivo: organizar tu propio código en archivos reutilizables.\n")

	# * Teoría clave
	# * Un módulo es un .py; puedes importarlo desde otro archivo si está en el mismo directorio.

	# ? Cómo funciona el ejercicio
	# - Crea utilidades.py con saludar(nombre) y calcular_area_rectangulo(ancho, alto).
	# - Importa y usa estas funciones desde este archivo.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Crea el módulo y escribe aquí los import/llamadas de prueba.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 7 · Autoevaluación final (mix de módulos)
# =========================================================================================
def seccion_7_autoevaluacion():
	encabezado("SECCIÓN 7 · Autoevaluación final (mix de módulos)")
	print("Objetivo: combinar math, datetime, random, time y un módulo propio en un mini‑ejercicio.\n")

	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# 1) Con math: seno y coseno de un ángulo en grados (usa radians).
	# 2) Con datetime: crea una fecha objetivo y calcula días hasta esa fecha.
	# 3) Con random: genera 5 números aleatorios entre 1 y 50.
	# 4) Con time: pausa 3 segundos entre mensajes.
	# 5) Con un módulo propio: función saludar() y calcular_area_triángulo(base, altura).
	# 6) Muestra un resumen final en una línea con los datos calculados.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  MENÚ para ejecutar tus ejercicios por secciones
# =========================================================================================
def menu():
	# Modo no interactivo: ejecuta TODO una vez y sale (evita bucles infinitos)
	if not RUN_INTERACTIVE:
		seccion_1_intro_modulos()
		seccion_2_math()
		seccion_3_datetime()
		seccion_4_random()
		seccion_5_time()
		seccion_6_modulos_personalizados()
		seccion_7_autoevaluacion()
		return

	# Modo interactivo: menú con bucle y opción de salida
	while True:
		print("\n===== MENÚ DEL ALUMNO · Clase 8 (Módulos y Librerías) =====")
		print("  1) Intro a módulos (import/alias/from)")
		print("  2) math")
		print("  3) datetime")
		print("  4) random")
		print("  5) time")
		print("  6) Módulos personalizados")
		print("  7) Autoevaluación final")
		print("  8) Ejecutar TODO (1→7)")
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
			seccion_1_intro_modulos(); pause()
		elif op == 2:
			seccion_2_math(); pause()
		elif op == 3:
			seccion_3_datetime(); pause()
		elif op == 4:
			seccion_4_random(); pause()
		elif op == 5:
			seccion_5_time(); pause()
		elif op == 6:
			seccion_6_modulos_personalizados(); pause()
		elif op == 7:
			seccion_7_autoevaluacion(); pause()
		elif op == 8:
			seccion_1_intro_modulos(); seccion_2_math(); seccion_3_datetime(); seccion_4_random(); seccion_5_time(); seccion_6_modulos_personalizados(); seccion_7_autoevaluacion(); pause()
		else:
			print("! Elige una opción del 0 al 8.")


if __name__ == "__main__":
	menu()

# -------------------------------------------------------------------------------------------
# * SECCIÓN 1: INTRODUCCIÓN A MÓDULOS Y LIBRERÍAS EN PYTHON
# ? En Python, un módulo es un archivo que contiene código (funciones, variables, clases, etc.)
# ? Las librerías son colecciones de módulos que podemos utilizar para ahorrar tiempo y reutilizar código.
# ? Python viene con muchos módulos ya instalados, que podemos usar sin tener que escribir todo desde cero.
# -------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------
# * SECCIÓN 2: USO DEL MÓDULO 'MATH'
# ? El módulo `math` incluye funciones matemáticas que nos permiten hacer cálculos como raíces cuadradas,
# ? potencias, y funciones trigonométricas como el seno y el coseno.
# -------------------------------------------------------------------------------------------

# * Ejemplo: Calcular la raíz cuadrada de un número
# ? Usamos la función `sqrt()` del módulo `math` para calcular la raíz cuadrada.
# TODO: Escribe el código para calcular la raíz cuadrada de 16 usando el módulo `math`.

# * Ejemplo: Calcular el valor del seno de 90 grados
# ? Para trabajar con ángulos, primero convertimos los grados a radianes con `radians()` y luego
# ? usamos la función `sin()` para calcular el seno.
# TODO: Escribe el código para calcular el seno de 90 grados con el módulo `math`.

# -------------------------------------------------------------------------------------------
# * SECCIÓN 3: USO DEL MÓDULO 'DATETIME'
# ? El módulo `datetime` nos permite trabajar con fechas y horas.
# -------------------------------------------------------------------------------------------

# * Ejemplo: Obtener la fecha y hora actual
# ? La función `datetime.now()` devuelve la fecha y hora actuales.
# TODO: Escribe el código para mostrar la fecha y hora actuales usando el módulo `datetime`.

# * Ejemplo: Crear una fecha personalizada
# ? Podemos crear una fecha personalizada usando `date()` del módulo `datetime`.
# TODO: Escribe el código para crear la fecha del 1 de enero de 2025 usando el módulo `datetime`.

# -------------------------------------------------------------------------------------------
# * SECCIÓN 4: USO DEL MÓDULO 'RANDOM'
# ? El módulo `random` nos permite generar números aleatorios y hacer selecciones al azar.
# -------------------------------------------------------------------------------------------

# * Ejemplo: Generar un número entero aleatorio
# ? Usamos la función `randint()` para generar un número entero aleatorio entre 1 y 100.
# TODO: Escribe el código para generar un número aleatorio entre 1 y 100 usando `random`.

# * Ejemplo: Seleccionar un elemento al azar de una lista
# ? La función `choice()` selecciona un elemento al azar de una lista.
# TODO: Escribe el código para elegir un servicio al azar de una lista como ["SSH", "Apache", "MySQL"].

# -------------------------------------------------------------------------------------------
# * SECCIÓN 5: USO DEL MÓDULO 'TIME'
# ? El módulo `time` permite pausar el programa durante un tiempo determinado o medir cuánto tiempo tarda en ejecutarse algo.
# -------------------------------------------------------------------------------------------

# * Ejemplo: Pausar el programa por 2 segundos
# ? Usamos `time.sleep()` para detener la ejecución del programa durante el tiempo que deseemos.
# TODO: Escribe el código para pausar el programa durante 2 segundos usando el módulo `time`.

# -------------------------------------------------------------------------------------------
# * SECCIÓN 6: CREACIÓN DE MÓDULOS PERSONALIZADOS
# ? Podemos crear nuestros propios módulos para organizar mejor nuestro código.
# ? Esto nos permite reutilizar funciones y mejorar la estructura de nuestro programa.
# -------------------------------------------------------------------------------------------

# * Ejemplo: Crear un módulo personalizado
# ? Podemos escribir funciones en un archivo `.py` y luego importarlo en otro archivo como un módulo.
# TODO: Crea un archivo `utilidades.py` con las funciones `saludar()` y `calcular_area_rectangulo()`.

# * Ejemplo: Usar el módulo personalizado
# ? Una vez creado el archivo `utilidades.py`, podemos importarlo en nuestro archivo principal.
# TODO: Importa las funciones `saludar()` y `calcular_area_rectangulo()` desde el módulo `utilidades`.

# -------------------------------------------------------------------------------------------
# * AUTOEVALUACIÓN FINAL:
# 1. Usa el módulo `math` para calcular el seno y coseno de un ángulo en grados.
# 2. Crea una fecha personalizada con el módulo `datetime` y calcula cuántos días faltan hasta esa fecha.
# 3. Genera 5 números aleatorios entre 1 y 50 usando `random.randint`.
# 4. Pausa el programa por 3 segundos usando el módulo `time.sleep()`.
# 5. Crea un módulo personalizado que contenga una función para saludar y otra para calcular el área de un triángulo.
# -------------------------------------------------------------------------------------------
