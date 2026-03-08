# =========================================================================================
#  🧑‍🎓 PYTHON · PLANTILLA DEL ALUMNO — Clase 9
#  Tema: Entrada/Salida de Archivos (texto) — abrir, leer, escribir, with, excepciones
#  Cómo usar este archivo:
#   1) Lee cada sección (Objetivos + Guía) y completa las ZONAS DEL ALUMNO (TODO).
#   2) Ejecuta este archivo y usa el menú para probar tus soluciones.
#   3) Mantén los ejemplos genéricos (p.ej., datos de personas) y evita datos sensibles.
# =========================================================================================

from typing import Any, Callable

# * Conmutadores -------------------------------------------------------------------------
RUN_INTERACTIVE = True   # True: menú interactivo; False: ejecuta TODO una vez
PAUSE = False

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
#  SECCIÓN 1 · Abrir y leer un archivo (modo 'r')
# =========================================================================================
def seccion_1_leer_archivo():
	encabezado("SECCIÓN 1 · Abrir y leer un archivo (modo 'r')")
	print("Objetivo: cargar el contenido completo de un archivo de texto.\n")

	# ? Cómo funciona el ejercicio
	# - Crea (si no existe) un archivo 'archivo.txt' con algún texto de ejemplo.
	# - Abre el archivo en modo lectura ('r') y muestra su contenido con read().
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Escribe el código para leer y mostrar el contenido de 'archivo.txt'.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 2 · Escribir en archivos: 'w' (sobrescribir) y 'a' (añadir)
# =========================================================================================
def seccion_2_escritura_archivo():
	encabezado("SECCIÓN 2 · Escribir en archivos: 'w' y 'a'")
	print("Objetivo: crear/sobrescribir y añadir texto a un archivo.\n")

	# ? Cómo funciona el ejercicio
	# - Con 'w' creas o sobrescribes; con 'a' añades al final.
	# - Escribe varias líneas de texto genéricas (nombre, edad, ciudad).
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Crea o sobrescribe un archivo con varias líneas y luego añade otra línea con 'a'.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 3 · Leer línea a línea: readline()/readlines() y for
# =========================================================================================
def seccion_3_leer_linea_a_linea():
	encabezado("SECCIÓN 3 · Leer línea a línea")
	print("Objetivo: procesar un archivo sin cargarlo entero en memoria.\n")

	# ? Cómo funciona el ejercicio
	# - Abre un archivo y recórrelo línea a línea mostrando cada línea con su número.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa la lectura línea a línea e imprime con un contador.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 4 · with: cierre automático y código más seguro
# =========================================================================================
def seccion_4_with_context_manager():
	encabezado("SECCIÓN 4 · with: cierre automático")
	print("Objetivo: utilizar 'with' para abrir/leer/escribir sin olvidar cerrar.\n")

	# ? Cómo funciona el ejercicio
	# - Usa with open(...) as f: para leer o escribir y mostrar el contenido o confirmación.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Reescribe un ejercicio previo utilizando 'with' y comprueba que el archivo queda cerrado.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 5 · Manejo de excepciones con archivos
# =========================================================================================
def seccion_5_excepciones_archivos():
	encabezado("SECCIÓN 5 · Manejo de excepciones con archivos")
	print("Objetivo: evitar que el programa falle si el archivo no existe u ocurre un error.\n")

	# ? Cómo funciona el ejercicio
	# - Intenta abrir un archivo inexistente y captura la excepción (FileNotFoundError).
	# - Muestra un mensaje claro al usuario.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa try/except al abrir/leer un archivo que puede no existir.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 6 · Autoevaluación: CRUD simple con archivo de texto
# =========================================================================================
def seccion_6_autoevaluacion():
	encabezado("SECCIÓN 6 · Autoevaluación: CRUD simple con archivo de texto")
	print("Objetivo: practicar escritura, añadido, lectura y manejo de errores en conjunto.\n")

	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# 1) Crea 'datos.txt' y escribe nombre, edad y ciudad (una por línea).
	# 2) Añade una línea adicional con tu email (o un dato genérico).
	# 3) Lee el archivo línea por línea y muestra cada línea numerada.
	# 4) Implementa manejo de excepciones para el caso de archivo inexistente.
	# 5) (Opcional) Implementa una pequeña búsqueda por palabra dentro del archivo.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  MENÚ
# =========================================================================================
def menu():
	if not RUN_INTERACTIVE:
		seccion_1_leer_archivo()
		seccion_2_escritura_archivo()
		seccion_3_leer_linea_a_linea()
		seccion_4_with_context_manager()
		seccion_5_excepciones_archivos()
		seccion_6_autoevaluacion()
		return

	while True:
		print("\n===== MENÚ DEL ALUMNO · Clase 9 (Archivos) =====")
		print("  1) Leer archivo (r)")
		print("  2) Escribir/Añadir (w/a)")
		print("  3) Leer línea a línea")
		print("  4) with (context manager)")
		print("  5) Excepciones con archivos")
		print("  6) Autoevaluación")
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
			seccion_1_leer_archivo(); pause()
		elif op == 2:
			seccion_2_escritura_archivo(); pause()
		elif op == 3:
			seccion_3_leer_linea_a_linea(); pause()
		elif op == 4:
			seccion_4_with_context_manager(); pause()
		elif op == 5:
			seccion_5_excepciones_archivos(); pause()
		elif op == 6:
			seccion_6_autoevaluacion(); pause()
		elif op == 7:
			seccion_1_leer_archivo(); seccion_2_escritura_archivo(); seccion_3_leer_linea_a_linea(); seccion_4_with_context_manager(); seccion_5_excepciones_archivos(); seccion_6_autoevaluacion(); pause()
		else:
			print("! Elige una opción del 0 al 7.")


if __name__ == "__main__":
	menu()

# -------------------------------------------------------------------------------------------
# * SECCIÓN 1: CONCEPTOS BÁSICOS DE ENTRADA/SALIDA DE ARCHIVOS (I/O) EN PYTHON
# ? La entrada/salida de archivos (I/O) nos permite leer y escribir datos en archivos.
# ? Podemos trabajar tanto con archivos de texto como con archivos binarios.
# -------------------------------------------------------------------------------------------

# * ABRIR Y LEER UN ARCHIVO
# ? Para leer un archivo en Python, usamos la función `open()` y le indicamos que queremos leerlo con el modo 'r'.
# ? Luego, usamos `read()` para leer el contenido completo del archivo.

# TODO: Escribe el código para abrir un archivo llamado 'archivo.txt', leerlo y mostrar su contenido.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 2: ESCRITURA EN ARCHIVOS
# ? Podemos escribir datos en un archivo usando el modo 'w' (escritura) o 'a' (añadir).
# ? El modo 'w' sobrescribe todo el contenido anterior, mientras que el modo 'a' añade al final.

# * ESCRITURA EN ARCHIVO
# ? Si abrimos un archivo con el modo 'w', cualquier contenido anterior se perderá.
# ? Si usamos el modo 'a', el contenido nuevo se añadirá al final del archivo.

# TODO: Escribe el código para crear o sobrescribir un archivo con algunas líneas de texto.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 3: LEER UN ARCHIVO LÍNEA POR LÍNEA
# ? Leer un archivo completo puede no ser siempre eficiente. A veces necesitamos leerlo línea por línea.
# ? Para esto, usamos `readline()` que lee una línea a la vez, o `readlines()` que lee todas las líneas y las convierte en una lista.

# * LEER LÍNEA POR LÍNEA
# ? Podemos leer un archivo línea por línea y procesar cada línea de manera individual.

# TODO: Escribe el código para abrir un archivo y leerlo línea por línea, mostrando cada línea en pantalla.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 4: USO DE `WITH` PARA MANEJAR ARCHIVOS
# ? La declaración `with` en Python nos permite manejar archivos sin tener que preocuparnos por cerrarlos.
# ? Cuando salimos del bloque `with`, Python cierra el archivo automáticamente.

# * USAR `WITH` PARA LEER ARCHIVOS
# ? Usar `with` es la forma más recomendada de trabajar con archivos en Python, ya que evita posibles errores si olvidamos cerrar el archivo.

# TODO: Escribe el código para leer un archivo usando la declaración `with` y mostrar su contenido.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 5: MANEJO DE EXCEPCIONES CON ARCHIVOS
# ? A veces, el archivo que queremos abrir no existe, o puede haber errores al leer o escribir.
# ? Para evitar que el programa falle, usamos un bloque `try-except` para manejar estos errores.

# * MANEJAR ERRORES AL LEER ARCHIVOS
# ? Usamos `try-except` para capturar errores cuando trabajamos con archivos, como cuando intentamos abrir un archivo que no existe.

# TODO: Escribe el código para intentar leer un archivo inexistente y manejar el error usando `try-except`.


# -------------------------------------------------------------------------------------------
# * AUTOEVALUACIÓN FINAL:
# 1. Crea un archivo llamado 'datos.txt' y escribe en él tu nombre, rango y unidad.
# 2. Añade una línea adicional con tu número de identificación.
# 3. Lee el archivo línea por línea y muestra cada línea en pantalla.
# 4. Implementa manejo de excepciones para asegurarte de que no haya errores si el archivo no existe.
# -------------------------------------------------------------------------------------------

# TODO: Escribe el código completo para resolver la autoevaluación final.
