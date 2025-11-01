# =========================================================================================
#  🧑‍🎓 PYTHON · PLANTILLA DEL ALUMNO — Clase 3
#  Tema: Bucles for/while, range, enumerate, break/continue, anidados, comprensiones
#  Cómo usar este archivo:
#   1) Lee cada sección (Objetivos + Guía) y completa las ZONAS DEL ALUMNO (TODO).
#   2) Ejecuta este archivo y usa el menú para probar tus soluciones.
#   3) Importante: evita bucles infinitos; en modo no interactivo se ejecuta una vez y sale.
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
#  SECCIÓN 1 · Bucle for con range()
# =========================================================================================
def seccion_1_for_rango():
	encabezado("SECCIÓN 1 · Bucle for con range()")
	print("Objetivo: iterar sobre secuencias numéricas con range(inicio, fin[, paso]).\n")

	# * Teoría clave
	# * range(a,b) genera a..b-1; úsalo para contar o repetir acciones.

	# ? Cómo funciona el ejercicio
	# - Muestra los números del 1 al 5 (o crea una tabla de multiplicar sencilla).
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Recorre range(1, 6) y muestra por pantalla el número en cada iteración.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 2 · Bucle for con listas
# =========================================================================================
def seccion_2_for_listas():
	encabezado("SECCIÓN 2 · Bucle for con listas")
	print("Objetivo: recorrer colecciones (listas) elemento a elemento.\n")

	# * Teoría clave
	# * for elemento in lista: ...

	# ? Cómo funciona el ejercicio
	# - Crea una lista de frutas o productos (p.ej., ["manzana","pan","leche"]).
	# - Recorre la lista y muestra un mensaje para cada elemento.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa el recorrido de la lista mostrando cada elemento.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 3 · for con índice usando enumerate()
# =========================================================================================
def seccion_3_enumerate():
	encabezado("SECCIÓN 3 · for con índice usando enumerate()")
	print("Objetivo: obtener índice y valor al iterar.\n")

	# * Teoría clave
	# * enumerate(lista, start=1) devuelve (indice, valor) en cada iteración.

	# ? Cómo funciona el ejercicio
	# - Partiendo de una lista de tareas, imprime "<i>. <tarea>" numerando desde 1.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Usa enumerate(lista, start=1) para imprimir índice y nombre de la tarea.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 4 · Bucle while (condición) — Evitar bucles infinitos
# =========================================================================================
def seccion_4_while_logs():
	encabezado("SECCIÓN 4 · Bucle while (condición) — evita bucles infinitos")
	print("Objetivo: repetir mientras se cumpla una condición y cortar cuando deje de cumplirse.\n")

	# * Teoría clave
	# * while condicion: ...  · Asegura cambiar la condición dentro del bucle para evitar bucles infinitos.

	# ? Cómo funciona el ejercicio
	# - Imprime los números del 1 al 5 usando while.
	# - Asegúrate de actualizar el contador dentro del bucle.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa el while que cuente de 1 a 5 sin quedarse en bucle infinito.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 5 · Bucle while con condición externa
# =========================================================================================
def seccion_5_while_carga_cpu():
	encabezado("SECCIÓN 5 · Bucle while con condición externa")
	print("Objetivo: modificar una variable hasta alcanzar un umbral seguro.\n")

	# * Teoría clave
	# * Controla y actualiza la variable de condición en cada iteración.

	# ? Cómo funciona el ejercicio
	# - Cuenta atrás: parte de n=5 y llega hasta 0.
	# - Muestra mensajes adecuados y termina sin quedarse en bucle.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa la cuenta atrás con while y evita bucles infinitos.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 6 · Gestión de usuarios conectados (for + condiciones)
# =========================================================================================
def seccion_6_usuarios():
	encabezado("SECCIÓN 6 · Gestión de usuarios conectados")
	print("Objetivo: combinar bucles con condiciones para procesar estructuras.\n")

	# * Teoría clave
	# * Recorre lista de diccionarios y decide según un booleano (conectado True/False).

	# ? Cómo funciona el ejercicio
	# - Crea lista de tareas con claves texto y completado (True/False).
	# - Recorre y muestra mensajes distintos para completadas vs pendientes.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa el recorrido y la lógica de mensajes con if.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 7 · Automatización de copias de seguridad
# =========================================================================================
def seccion_7_backups():
	encabezado("SECCIÓN 7 · Automatización de copias de seguridad")
	print("Objetivo: aplicar bucles para ejecutar una acción repetidamente.\n")

	# * Teoría clave
	# * Un for puede simular acciones sobre varios elementos (servidores, rutas, etc.).

	# ? Cómo funciona el ejercicio
	# - Crea lista de destinatarios y simula el envío de un recordatorio a cada uno.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa el bucle que recorra y muestre el recordatorio enviado a cada destinatario.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 8 · Autoevaluación final (mini‑proyecto)
# =========================================================================================
def seccion_8_autoevaluacion():
	encabezado("SECCIÓN 8 · Autoevaluación final")
	print("Objetivo: integrar for, while, range, enumerate y control de flujo.\n")

	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# 1) Crea una lista con 3 nombres y recórrelos mostrando un saludo para cada uno.
	# 2) Bucle while que cuente desde 1 hasta 5.
	# 3) Usa enumerate para listar tareas numeradas; si aparece una cadena vacía, corta con break.
	# 4) Imprime un resumen final en 1 línea con datos relevantes de tu práctica.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  MENÚ para ejecutar tus ejercicios por secciones
# =========================================================================================
def menu():
	# Modo no interactivo: ejecuta TODO una vez y sale (evita bucles infinitos)
	if not RUN_INTERACTIVE:
		seccion_1_for_rango()
		seccion_2_for_listas()
		seccion_3_enumerate()
		seccion_4_while_logs()
		seccion_5_while_carga_cpu()
		seccion_6_usuarios()
		seccion_7_backups()
		seccion_8_autoevaluacion()
		return

	# Modo interactivo: menú con bucle y opción de salida
	while True:
		print("\n===== MENÚ DEL ALUMNO · Clase 3 (Bucles) =====")
		print("  1) for con range()")
		print("  2) for con listas")
		print("  3) for con enumerate()")
		print("  4) while (logs) — evita bucles infinitos")
		print("  5) while (carga CPU)")
		print("  6) Gestión de usuarios")
		print("  7) Copias de seguridad")
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
			break
		elif op == 1:
			seccion_1_for_rango(); pause()
		elif op == 2:
			seccion_2_for_listas(); pause()
		elif op == 3:
			seccion_3_enumerate(); pause()
		elif op == 4:
			seccion_4_while_logs(); pause()
		elif op == 5:
			seccion_5_while_carga_cpu(); pause()
		elif op == 6:
			seccion_6_usuarios(); pause()
		elif op == 7:
			seccion_7_backups(); pause()
		elif op == 8:
			seccion_8_autoevaluacion(); pause()
		elif op == 9:
			seccion_1_for_rango(); seccion_2_for_listas(); seccion_3_enumerate(); seccion_4_while_logs(); seccion_5_while_carga_cpu(); seccion_6_usuarios(); seccion_7_backups(); seccion_8_autoevaluacion(); pause()
		else:
			print("! Elige una opción del 0 al 9.")


if __name__ == "__main__":
	menu()

# -------------------------------------------------------------------------------------------
# * SECCIÓN 1: EJEMPLO BÁSICO DE BUCLES FOR EN PYTHON
# ? LOS BUCLES FOR PERMITEN ITERAR SOBRE UN RANGO O UNA COLECCIÓN DE ELEMENTOS, COMO LISTAS.
# ? SON IDEALES CUANDO CONOCEMOS EL NÚMERO DE VECES QUE QUEREMOS REPETIR UNA OPERACIÓN.
# -------------------------------------------------------------------------------------------

# * BUCLE FOR: ITERANDO SOBRE UN RANGO DE NÚMEROS
# ? ESTE EJEMPLO SIMULA LA COMPROBACIÓN DE LA DISPONIBILIDAD DE SERVIDORES DEL 1 AL 5.
# ? RANGE(1, 6) GENERA UNA SECUENCIA DE NÚMEROS DEL 1 AL 5.

# TODO: ESCRIBE AQUÍ TU CÓDIGO PARA ITERAR SOBRE UN RANGO Y COMPROBAR LA DISPONIBILIDAD DE LOS SERVIDORES.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 2: BUCLE FOR CON LISTAS
# ? PODEMOS UTILIZAR LOS BUCLES FOR PARA ITERAR SOBRE ELEMENTOS DE UNA LISTA. 
# ? ESTE EJEMPLO SIMULA LA COMPROBACIÓN DEL ESTADO DE SERVICIOS EN UN SERVIDOR.
# -------------------------------------------------------------------------------------------

# * CREA UNA LISTA DE SERVICIOS QUE QUEREMOS MONITOREAR.

# TODO: ESCRIBE AQUÍ TU CÓDIGO PARA ITERAR SOBRE UNA LISTA DE SERVICIOS Y COMPROBAR SU ESTADO.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 3: BUCLE FOR CON ÍNDICE USANDO ENUMERATE()
# ? A VECES NECESITAMOS TANTO EL ÍNDICE COMO EL VALOR AL ITERAR SOBRE UNA LISTA.
# ? CON ENUMERATE(), OBTENEMOS EL ÍNDICE Y EL VALOR SIMULTÁNEAMENTE.
# -------------------------------------------------------------------------------------------

# TODO: ESCRIBE AQUÍ TU CÓDIGO USANDO ENUMERATE PARA IMPRIMIR EL ÍNDICE Y EL NOMBRE DEL SERVICIO.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 4: BUCLE WHILE
# ? EL BUCLE WHILE SE UTILIZA CUANDO NO SABEMOS CUÁNTAS VECES SE DEBE REPETIR EL BUCLE. 
# ? CONTINÚA EJECUTÁNDOSE MIENTRAS UNA CONDICIÓN SEA VERDADERA.
# -------------------------------------------------------------------------------------------

# * MONITOREA UN ARCHIVO DE LOGS HASTA DETECTAR UN ERROR.

# TODO: ESCRIBE AQUÍ TU CÓDIGO PARA ITERAR SOBRE LOS LOGS USANDO UN BUCLE WHILE HASTA ENCONTRAR UN ERROR.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 5: BUCLE WHILE CON UNA CONDICIÓN EXTERNA
# ? ESTE EJEMPLO SIMULA LA MONITORIZACIÓN DE LA CARGA DEL CPU DE UN SERVIDOR HASTA QUE LLEGUE A UN NIVEL ACEPTABLE.
# -------------------------------------------------------------------------------------------

# * SUPÓN QUE LA CARGA INICIAL DEL CPU ES DEL 95%. MONITOREA LA CARGA HASTA QUE BAJE A UN NIVEL SEGURO.

# TODO: ESCRIBE AQUÍ TU CÓDIGO PARA REDUCIR LA CARGA DEL CPU USANDO UN BUCLE WHILE.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 6: GESTIÓN DE USUARIOS CONECTADOS A UN SERVIDOR
# ? SUPONGAMOS QUE TENEMOS UNA LISTA DE USUARIOS Y NECESITAMOS REALIZAR UNA ACCIÓN SEGÚN SI ESTÁN CONECTADOS O NO.
# -------------------------------------------------------------------------------------------

# TODO: ESCRIBE AQUÍ TU CÓDIGO PARA GESTIONAR UNA LISTA DE USUARIOS Y MOSTRAR SI ESTÁN CONECTADOS O NO.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 7: AUTOMATIZACIÓN DE COPIAS DE SEGURIDAD
# ? SUPONGAMOS QUE NECESITAMOS REALIZAR COPIAS DE SEGURIDAD PARA UNA LISTA DE SERVIDORES.
# -------------------------------------------------------------------------------------------

# TODO: ESCRIBE AQUÍ TU CÓDIGO PARA AUTOMATIZAR UNA COPIA DE SEGURIDAD EN UNA LISTA DE SERVIDORES.


# -------------------------------------------------------------------------------------------
# * AUTOEVALUACIÓN FINAL:
# 1. CREA UNA LISTA QUE ALMACENE 3 DIRECCIONES IP DE SERVIDORES.
# 2. USA UN BUCLE FOR PARA REALIZAR UNA "VERIFICACIÓN" EN CADA SERVIDOR.
# 3. CREA UNA VARIABLE QUE REPRESENTE LA CARGA INICIAL DEL CPU DE UN SERVIDOR.
# 4. UTILIZA UN BUCLE WHILE PARA SIMULAR LA REDUCCIÓN GRADUAL DE LA CARGA DEL CPU HASTA UN NIVEL ACEPTABLE (75%).
# 5. IMPRIME EL RESULTADO FINAL CUANDO LA CARGA DEL CPU SEA SEGURA.
# -------------------------------------------------------------------------------------------

# TODO: ESCRIBE AQUÍ TU CÓDIGO PARA LA AUTOEVALUACIÓN FINAL.
