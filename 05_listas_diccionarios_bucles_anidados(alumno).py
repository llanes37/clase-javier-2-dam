# =========================================================================================
#  🧑‍🎓 PYTHON · PLANTILLA DEL ALUMNO — Clase 5
#  Tema: Listas, Diccionarios, Iteración y Bucles Anidados (+ ordenación y comprensiones)
#  Cómo usar este archivo:
#   1) Lee cada sección (Objetivos + Guía) y completa las ZONAS DEL ALUMNO (TODO).
#   2) Ejecuta este archivo y usa el menú para probar tus soluciones.
#   3) Ejercicios genéricos (agenda, inventario, perfiles) válidos para cualquier contexto.
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
#  SECCIÓN 1 · Listas — creación, acceso, slicing y métodos
# =========================================================================================
def seccion_1_listas():
	encabezado("SECCIÓN 1 · Listas — creación, acceso, slicing y métodos")
	print("Objetivo: crear/modificar listas y practicar acceso por índice y slices.\n")

	# * Teoría clave
	# * Métodos útiles: append, insert, remove, pop, sort, reverse.

	# ? Cómo funciona el ejercicio
	# - Crea lista con 4 ciudades.
	# - Inserta una en la posición 2 y elimina la última.
	# - Muestra longitud, primera, última y slice 1:3.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Escribe aquí tu solución siguiendo los puntos anteriores.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 2 · Diccionarios — acceso, actualización y utilidades
# =========================================================================================
def seccion_2_diccionarios():
	encabezado("SECCIÓN 2 · Diccionarios — acceso, actualización y utilidades")
	print("Objetivo: crear/actualizar diccionarios y recorrer sus elementos.\n")

	# * Teoría clave
	# * Utilidades: get, keys, values, items. Accede como dic[clave] y actualiza con asignación.

	# ? Cómo funciona el ejercicio
	# - Crea 'contacto' con nombre, telefono, email.
	# - Actualiza telefono, añade ciudad y muestra sus items (clave: valor).
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa el diccionario y las operaciones solicitadas.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 3 · Iterar diccionarios (keys / values / items)
# =========================================================================================
def seccion_3_iterar_dicc():
	encabezado("SECCIÓN 3 · Iterar diccionarios (keys / values / items)")
	print("Objetivo: recorrer diccionarios de forma clara.\n")

	# * Teoría clave
	# * for k in dic; for v in dic.values(); for k, v in dic.items().

	# ? Cómo funciona el ejercicio
	# - Con {"A":10, "B":0, "C":7} muestra: X -> stock OK si >0; si no, sin stock.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Recorre items y muestra el mensaje adecuado.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 4 · Estructuras anidadas + bucles anidados
# =========================================================================================
def seccion_4_anidadas():
	encabezado("SECCIÓN 4 · Estructuras anidadas + bucles anidados")
	print("Objetivo: manejar listas de diccionarios con bucles anidados.\n")

	# * Teoría clave
	# * Colecciones dentro de colecciones: lista de dicts, dict de listas, etc.

	# ? Cómo funciona el ejercicio
	# - Crea lista de dicts con clases y alumnos (lista de nombres).
	# - Muestra "Clase X:" y luego cada alumno con guion.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa la estructura y el recorrido anidado.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 5 · Ordenación con key/lambda + min/max/sum
# =========================================================================================
def seccion_5_ordenacion():
	encabezado("SECCIÓN 5 · Ordenación con key/lambda + min/max/sum")
	print("Objetivo: ordenar y calcular agregados en colecciones.\n")

	# * Teoría clave
	# * sorted(lista, key=lambda x: ...), min/max con key, sum con generadores.

	# ? Cómo funciona el ejercicio
	# - Lista de dicts con {"nombre":..., "nota":...}.
	# - Ordénalos por nota desc y muestra: "Mejor alumno: <nombre> (<nota>)".
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa la lista, la ordenación y el mensaje de mejor alumno.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 6 · Comprensiones (listas y diccionarios) [opcional]
# =========================================================================================
def seccion_6_comprensiones():
	encabezado("SECCIÓN 6 · Comprensiones (listas y diccionarios) [opcional]")
	print("Objetivo: crear colecciones de forma concisa con comprensiones.\n")

	# * Teoría clave
	# * [expr for x in lista if cond]  ·  {k:v for k,v in dic.items() if cond}

	# ? Cómo funciona el ejercicio
	# - Dado un dict producto→stock, crea otro dict solo con stock>0.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa la comprensión de diccionario filtrando los que tengan stock positivo.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 7 · Autoevaluación final (inventario)
# =========================================================================================
def seccion_7_autoevaluacion():
	encabezado("SECCIÓN 7 · Autoevaluación final (inventario)")
	print("Objetivo: integrar listas, diccionarios, bucles anidados, ordenación y comprensiones.\n")

	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# 1) Crea lista de dicts inventario con {nombre, categoria, precio, stock}.
	# 2) Agrupa por categoria (dict de listas) y recórrelo con bucles anidados.
	# 3) Ordena por precio asc y muestra top 3 más baratos.
	# 4) Calcula valor total del stock (precio*stock).
	# 5) Comprensión: {nombre: precio_con_iva} con IVA=21%.
	# 6) Resumen final (1 línea):
	#    "Items:<n> | Categorías:<m> | Valor stock:<€> | Barato:<nombre-precio>"
	# -------------------------------------------------------------------------------


# =========================================================================================
#  MENÚ para ejecutar tus ejercicios por secciones
# =========================================================================================
def menu():
	# Modo no interactivo: ejecuta TODO una vez y sale (evita bucles infinitos)
	if not RUN_INTERACTIVE:
		seccion_1_listas()
		seccion_2_diccionarios()
		seccion_3_iterar_dicc()
		seccion_4_anidadas()
		seccion_5_ordenacion()
		seccion_6_comprensiones()
		seccion_7_autoevaluacion()
		return

	# Modo interactivo: menú con bucle y opción de salida
	while True:
		print("\n===== MENÚ DEL ALUMNO · Clase 5 (Listas, Diccionarios y Anidados) =====")
		print("  1) Listas (creación y métodos)")
		print("  2) Diccionarios (acceso y utilidades)")
		print("  3) Iterar diccionarios")
		print("  4) Estructuras anidadas + bucles anidados")
		print("  5) Ordenación + min/max/sum")
		print("  6) Comprensiones [opcional]")
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
			seccion_1_listas(); pause()
		elif op == 2:
			seccion_2_diccionarios(); pause()
		elif op == 3:
			seccion_3_iterar_dicc(); pause()
		elif op == 4:
			seccion_4_anidadas(); pause()
		elif op == 5:
			seccion_5_ordenacion(); pause()
		elif op == 6:
			seccion_6_comprensiones(); pause()
		elif op == 7:
			seccion_7_autoevaluacion(); pause()
		elif op == 8:
			seccion_1_listas(); seccion_2_diccionarios(); seccion_3_iterar_dicc(); seccion_4_anidadas(); seccion_5_ordenacion(); seccion_6_comprensiones(); seccion_7_autoevaluacion(); pause()
		else:
			print("! Elige una opción del 0 al 8.")


if __name__ == "__main__":
	menu()

# -------------------------------------------------------------------------------------------
# * SECCIÓN 1: LISTAS EN PYTHON
# ? Las listas son colecciones ordenadas que pueden almacenar múltiples elementos en una sola variable.
# ? En administración de sistemas, las listas pueden usarse para almacenar registros de usuarios conectados o servicios activos.
# -------------------------------------------------------------------------------------------

# * Ejemplo básico: Lista de usuarios conectados
# Crea una lista que contenga varios nombres de usuarios que están conectados al servidor.

# TODO: CREA AQUÍ TU LISTA DE USUARIOS CONECTADOS


# * Acceder a elementos de la lista
# Para acceder a un elemento de la lista, se utiliza el índice. Los índices empiezan en 0.

# TODO: ACCEDE AQUÍ A ALGÚN ELEMENTO DE LA LISTA UTILIZANDO EL ÍNDICE


# * Modificar elementos de una lista
# Puedes cambiar el valor de un elemento accediendo a su índice y asignando un nuevo valor.

# TODO: MODIFICA AQUÍ UNO DE LOS ELEMENTOS DE TU LISTA


# -------------------------------------------------------------------------------------------
# * SECCIÓN 2: DICCIONARIOS EN PYTHON
# ? Los diccionarios permiten almacenar pares de clave-valor. Son útiles cuando necesitamos relacionar elementos.
# ? En administración de sistemas, los diccionarios pueden usarse para guardar información clave sobre un servidor.
# -------------------------------------------------------------------------------------------

# * Ejemplo básico: Información de un servidor
# Crea un diccionario que almacene la información clave de un servidor, como su nombre, dirección IP y estado.

# TODO: CREA AQUÍ TU DICCIONARIO CON LA INFORMACIÓN DEL SERVIDOR


# * Acceder a los valores del diccionario
# Para obtener el valor de una clave en el diccionario, simplemente usa el nombre de la clave.

# TODO: ACCEDE AQUÍ A LOS VALORES DE TU DICCIONARIO UTILIZANDO LAS CLAVES


# * Modificar valores en el diccionario
# Puedes cambiar el valor asociado a una clave accediendo directamente a ella.

# TODO: MODIFICA AQUÍ UNO DE LOS VALORES EN TU DICCIONARIO


# -------------------------------------------------------------------------------------------
# * SECCIÓN 3: BUCLES ANIDADOS
# ? Un bucle anidado es un bucle dentro de otro bucle. Se utiliza cuando necesitamos trabajar con estructuras de datos más complejas.
# -------------------------------------------------------------------------------------------

# * Ejemplo: Combinación de listas y diccionarios
# Imagina que tienes varios servidores, y cada servidor tiene una lista de servicios activos.
# Utiliza bucles anidados para recorrer cada servidor y mostrar todos sus servicios.

# TODO: CREA AQUÍ UNA LISTA DE DICCIONARIOS PARA ALMACENAR LA INFORMACIÓN DE VARIOS SERVIDORES Y SUS SERVICIOS


# -------------------------------------------------------------------------------------------
# * AUTOEVALUACIÓN FINAL:
# 1. Crea una lista de diccionarios donde cada diccionario contenga la información de un servidor (nombre, IP y lista de servicios).
# 2. Usa un bucle anidado para iterar sobre los servidores y sus servicios.
# 3. Modifica el estado de un servicio en un servidor específico y muestra los cambios.
# -------------------------------------------------------------------------------------------

# TODO: ESCRIBE AQUÍ TU CÓDIGO PARA LA AUTOEVALUACIÓN FINAL
