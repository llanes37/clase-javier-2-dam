# =========================================================================================
#  🧑‍🎓 PYTHON · PLANTILLA DEL ALUMNO — Clase 4
#  Tema: Funciones (def, parámetros, return, valores por defecto, scope) + mini‑proyecto
#  Cómo usar este archivo:
#   1) Lee cada sección (Objetivos + Guía) y completa las ZONAS DEL ALUMNO (TODO).
#   2) Ejecuta este archivo y usa el menú para probar tus soluciones.
#   3) No hay código ejemplo en las secciones: escribe tus propias funciones.
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
#  SECCIÓN 1 · Función básica (def + return)
# =========================================================================================
def seccion_1_funcion_basica():
	encabezado("SECCIÓN 1 · Función básica (def + return)")
	print("Objetivo: crear una función sencilla que devuelva un valor.\n")

	# * Teoría clave
	# * def nombre(par1, par2): ...  · Usa return para devolver resultados reutilizables.

	# ? Cómo funciona el ejercicio
	# - Crea una función que reciba un nombre y devuelva "Hola, <nombre>".
	# - Llama a la función y muestra el resultado.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Define y usa la función de saludo.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 2 · Parámetros y validaciones simples
# =========================================================================================
def seccion_2_parametros():
	encabezado("SECCIÓN 2 · Parámetros y validaciones simples")
	print("Objetivo: recibir datos y validar mínimamente antes de operar.\n")

	# * Teoría clave
	# * Convierte tipos si hace falta (int/float) y valida entradas (no vacías, rangos, etc.).

	# ? Cómo funciona el ejercicio
	# - Define una función que reciba nota (0-10) y asistencia (%) y devuelva un texto de estado.
	# - Considera: si nota >= 5 y asistencia >= 75 → "APTO"; si no → "NO APTO" (justifica el motivo).
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa la función y pruébala con algunos valores.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 3 · Valores por defecto y keyword args
# =========================================================================================
def seccion_3_por_defecto():
	encabezado("SECCIÓN 3 · Valores por defecto y keyword args")
	print("Objetivo: simplificar llamadas con parámetros por defecto y por nombre.\n")

	# * Teoría clave
	# * Define valores por defecto y permite llamadas claras con nombre=valor.

	# ? Cómo funciona el ejercicio
	# - Implementa precio_final(base, iva=21, descuento=0) -> total.
	# - Llama por posición y por palabra clave.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Escribe la función y realiza 2-3 llamadas de ejemplo.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 4 · Scope básico (local vs externo)
# =========================================================================================
def seccion_4_scope():
	encabezado("SECCIÓN 4 · Scope básico (local vs externo)")
	print("Objetivo: entender que las variables dentro de la función no modifican las externas.\n")

	# * Teoría clave
	# * Evita globales; usa patrón entrada → salida. Devuelve nuevos valores.

	# ? Cómo funciona el ejercicio
	# - Crea incrementar(contador, paso=1) que devuelva el nuevo contador.
	# - Actualiza un contador externo llamándola varias veces y muestra el resultado.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa la función y pruébala.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 5 · Funciones que procesan colecciones
# =========================================================================================
def seccion_5_colecciones():
	encabezado("SECCIÓN 5 · Funciones que procesan colecciones")
	print("Objetivo: recorrer listas/diccionarios dentro de funciones.\n")

	# * Teoría clave
	# * Diseña funciones que reciban colecciones y devuelvan resultados (no impriman si no es necesario).

	# ? Cómo funciona el ejercicio
	# - Define resumen_notas(lista) -> (aprobados, suspensos, media).
	# - Devuelve los tres valores y muéstralos luego con print.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa la función y pruébala con una lista de notas.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 6 · Componer funciones (una llama a otras)
# =========================================================================================
def seccion_6_composicion():
	encabezado("SECCIÓN 6 · Componer funciones (una llama a otras)")
	print("Objetivo: reutilizar pequeñas funciones para tareas mayores.\n")

	# * Teoría clave
	# * Divide y vencerás: funciones pequeñas, claras; una función orquesta el proceso.

	# ? Cómo funciona el ejercicio
	# - Crea 2–3 funciones pequeñas (p.ej., sumar, aplicar_descuento, formatear_resumen).
	# - Crea una función principal que las llame y devuelva un resultado final.
	#
	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa las funciones y muestra el resultado de la función principal.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 7 · Autoevaluación final (mini‑proyecto)
# =========================================================================================
def seccion_7_autoevaluacion():
	encabezado("SECCIÓN 7 · Autoevaluación final")
	print("Objetivo: integrar def, parámetros, return, por defecto y composición.\n")

	# TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
	# Implementa y prueba:
	# 1) mostrar_titulo() → imprime un título enmarcado.
	# 2) sumar(a,b), restar(a,b), multiplicar(a,b), dividir(a,b) → dividir debe manejar b==0.
	# 3) precio_con_iva(base, iva=21) -> float.
	# 4) total_compra(precios: lista[float]) -> float (suma de todos los elementos).
	# 5) resumen_final(total) -> str que devuelva una línea tipo dashboard.
	# Demostración: llama a las funciones anteriores y muestra el resumen.
	# -------------------------------------------------------------------------------


# =========================================================================================
#  MENÚ para ejecutar tus ejercicios por secciones
# =========================================================================================
def menu():
	# Modo no interactivo: ejecuta TODO una vez y sale (evita bucles infinitos)
	if not RUN_INTERACTIVE:
		seccion_1_funcion_basica()
		seccion_2_parametros()
		seccion_3_por_defecto()
		seccion_4_scope()
		seccion_5_colecciones()
		seccion_6_composicion()
		seccion_7_autoevaluacion()
		return

	# Modo interactivo: menú con bucle y opción de salida
	while True:
		print("\n===== MENÚ DEL ALUMNO · Clase 4 (Funciones) =====")
		print("  1) Función básica (def + return)")
		print("  2) Parámetros y validaciones")
		print("  3) Por defecto y keyword args")
		print("  4) Scope básico")
		print("  5) Funciones con colecciones")
		print("  6) Componer funciones")
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
			seccion_1_funcion_basica(); pause()
		elif op == 2:
			seccion_2_parametros(); pause()
		elif op == 3:
			seccion_3_por_defecto(); pause()
		elif op == 4:
			seccion_4_scope(); pause()
		elif op == 5:
			seccion_5_colecciones(); pause()
		elif op == 6:
			seccion_6_composicion(); pause()
		elif op == 7:
			seccion_7_autoevaluacion(); pause()
		elif op == 8:
			seccion_1_funcion_basica(); seccion_2_parametros(); seccion_3_por_defecto(); seccion_4_scope(); seccion_5_colecciones(); seccion_6_composicion(); seccion_7_autoevaluacion(); pause()
		else:
			print("! Elige una opción del 0 al 8.")


if __name__ == "__main__":
	menu()

# -------------------------------------------------------------------------------------------
# * SECCIÓN 1: EJEMPLO BÁSICO DE UNA FUNCIÓN EN PYTHON
# ? Una función en Python es un bloque de código que solo se ejecuta cuando es llamada.
# ? Las funciones pueden tomar parámetros, que son valores que se le pasan para que la función los use.
# ? Después de realizar sus tareas, una función puede devolver un valor usando "return".
# ? Crear funciones ayuda a organizar el código, hacerlo más fácil de leer y reutilizable.
# -------------------------------------------------------------------------------------------

# * FUNCIÓN PARA SALUDAR A UN OFICIAL DE SISTEMAS
# ? Esta función pide al usuario su nombre y rango, y devuelve un mensaje de bienvenida.
# ? Recuerda: Usamos la función input() para pedir datos al usuario, y return para devolver un mensaje.

# TODO: Escribe aquí tu código para definir y llamar a la función de saludo.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 2: FUNCIÓN PARA CALCULAR EL USO DE RECURSOS (CPU Y MEMORIA)
# ? En esta función, le pedimos al usuario que introduzca dos valores: el uso de CPU y el uso de memoria.
# ? Si el usuario no introduce un valor para la memoria, podemos asignar un valor por defecto usando una condición.
# ? Recuerda que puedes convertir los datos que recibe la función en otros tipos, como convertir un texto (string) en número (int).
# -------------------------------------------------------------------------------------------

# * SOLICITAR EL USO DE CPU Y MEMORIA, CON UN VALOR POR DEFECTO SI EL USUARIO NO INTRODUCE NADA.
# ? En este ejercicio, la memoria será opcional y si no se introduce un valor, se usará un valor por defecto (2048 MB).

# TODO: Escribe aquí tu código para definir y llamar a la función que calcula el uso de recursos.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 3: FUNCIÓN PARA GESTIONAR USUARIOS DEL SISTEMA
# ? En administración de sistemas, es importante gestionar usuarios y sus privilegios.
# ? En esta función, le pediremos al usuario que introduzca el nombre de un usuario y si tiene privilegios de administrador.
# ? Usamos condiciones (if/else) para devolver diferentes mensajes según si el usuario es o no administrador.
# -------------------------------------------------------------------------------------------

# * SOLICITAR EL NOMBRE DEL USUARIO Y VERIFICAR SI TIENE PRIVILEGIOS DE ADMINISTRADOR.
# ? Si el usuario tiene privilegios, mostramos un mensaje que diga que tiene acceso completo; si no, indicamos que tiene acceso limitado.

# TODO: Escribe aquí tu código para definir y llamar a la función de gestión de usuarios.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 4: FUNCIÓN PARA COMPROBAR EL ESTADO DE LOS SERVICIOS CRÍTICOS
# ? Un servidor generalmente ejecuta varios servicios importantes, como SSH, VPN, Firewall, entre otros.
# ? Esta función recorre una lista de servicios críticos y verifica si están funcionando correctamente.
# ? Usamos un bucle (for) para iterar sobre la lista de servicios y comprobar su estado.
# -------------------------------------------------------------------------------------------

# * COMPROBAR EL ESTADO DE LOS SERVICIOS CRÍTICOS QUE DEBEN ESTAR FUNCIONANDO EN EL SERVIDOR.
# ? La función iterará sobre la lista de servicios, comprobando su estado uno por uno.

# TODO: Escribe aquí tu código para definir y llamar a la función de comprobación de servicios.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 5: FUNCIÓN PARA MONITORIZAR SERVIDORES EN LA RED
# ? En un sistema en red, hay varios servidores conectados. Esta función pide al usuario que introduzca el estado de cada servidor.
# ? Dependiendo de la respuesta del usuario (si está o no disponible), se almacenarán los servidores que están en buen estado.
# ? Esta función usa un bucle para verificar el estado de cada servidor en la lista.
# -------------------------------------------------------------------------------------------

# * MONITORIZAR UNA LISTA DE SERVIDORES Y MOSTRAR CUÁLES ESTÁN DISPONIBLES.
# ? Si el servidor está disponible, lo añadimos a una lista de servidores disponibles; si no, mostramos un aviso de alerta.

# TODO: Escribe aquí tu código para definir y llamar a la función que monitoriza los servidores.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 6: FUNCIÓN CON VARIOS PARÁMETROS Y RETURN
# ? Las funciones también pueden aceptar parámetros. Los parámetros son valores que le pasamos a la función para que los use.
# ? En esta sección, crearemos una función que suma dos números y devuelve el resultado.
# ? La palabra clave "return" se usa para devolver un valor desde la función al lugar donde fue llamada.
# -------------------------------------------------------------------------------------------

# * SUMAR DOS NÚMEROS Y DEVOLVER EL RESULTADO.
# ? Los parámetros de la función serán dos números, y devolverá la suma de estos números.

# TODO: Escribe aquí tu código para definir y llamar a la función que suma dos números.


# -------------------------------------------------------------------------------------------
# * SECCIÓN 7: FUNCIÓN QUE LLAMA A OTRAS FUNCIONES
# ? Es posible que una función llame a otras funciones dentro de su código para ejecutar varias tareas en conjunto.
# ? En este caso, creamos una función que llamará a las funciones anteriores para ejecutar todo un proceso automatizado.
# -------------------------------------------------------------------------------------------

# * LLAMAR A TODAS LAS FUNCIONES PREVIAMENTE DEFINIDAS PARA COMPLETAR UN PROCESO.
# ? Esta función puede servir como un "resumen" donde llamamos a varias funciones que hemos definido antes.

# TODO: Escribe aquí tu código para definir y llamar a una función que ejecute un proceso completo.


# -------------------------------------------------------------------------------------------
# * AUTOEVALUACIÓN FINAL:
# ? En esta parte, combinaremos todo lo aprendido.
# 1. Solicita el nombre de un usuario del sistema y salúdale usando una función.
# 2. Solicita el uso de CPU y memoria de un servidor y muestra los resultados usando una función.
# 3. Solicita el estado de tres servidores y registra cuáles están disponibles.
# 4. Solicita la suma de dos números y devuelve el resultado.
# 5. Llama a todas las funciones definidas anteriormente en un proceso completo.
# -------------------------------------------------------------------------------------------

# TODO: Escribe aquí tu código para la autoevaluación final que incluya todas las funciones que has definido.
