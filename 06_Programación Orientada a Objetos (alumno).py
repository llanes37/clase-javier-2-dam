# =========================================================================================
#  🧑‍🎓 PYTHON · PLANTILLA DEL ALUMNO — Clase 6
#  Tema: Programación Orientada a Objetos (clases, __init__, atributos, dunder, property,
#        herencia y composición) + mini‑proyecto
#  Cómo usar este archivo:
#   1) Lee cada sección (Objetivos + Guía) y completa las ZONAS DEL ALUMNO (TODO).
#   2) Ejecuta este archivo y usa el menú para probar tus soluciones.
#   3) Ejercicios genéricos (tienda, biblioteca, perfiles) sin código ejemplo en secciones.
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
#  SECCIÓN 1 · Clases y objetos (atributos y métodos)
# =========================================================================================
def seccion_1_clases_objetos():
    encabezado("SECCIÓN 1 · Clases y objetos (atributos y métodos)")
    print("Objetivo: crear clases con atributos de instancia y métodos simples.\n")

    # * Teoría clave
    # * class Nombre: def __init__(self,...): self.atrib = valor   ·   def metodo(self): ...

    # ? Cómo funciona el ejercicio
    # - Crea Persona(nombre, edad) con presentar() → "Soy <nombre> y tengo <edad> años".
    # - Crea 2 personas y muestra su presentación.
    #
    # TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
    # Escribe tu clase y una pequeña demostración.
    # -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 2 · __init__ y self (inicialización de estado)
# =========================================================================================
def seccion_2_init_self():
    encabezado("SECCIÓN 2 · __init__ y self (inicialización de estado)")
    print("Objetivo: inicializar estado y añadir métodos que lo modifican.\n")

    # * Teoría clave
    # * __init__ recibe datos y configura atributos; self es la instancia actual.

    # ? Cómo funciona el ejercicio
    # - Libro(titulo, autor, paginas) con ficha() → "<titulo> de <autor> (<pag> pags)".
    # - Crea 2 libros y muestra su ficha.
    #
    # TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
    # Implementa la clase y una breve demostración.
    # -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 3 · Atributos de clase · @classmethod · @staticmethod
# =========================================================================================
def seccion_3_class_attrs():
    encabezado("SECCIÓN 3 · Atributos de clase · @classmethod · @staticmethod")
    print("Objetivo: distinguir datos de clase/instancia y crear fábricas y utilidades.\n")

    # * Teoría clave
    # * Atributo de clase: compartido. @classmethod: devuelve cls(...). @staticmethod: util puro.

    # ? Cómo funciona el ejercicio
    # - Producto(IVA=21) con @classmethod desde_linea("nombre;precio") y precio_con_iva().
    #
    # TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
    # Implementa la clase con atributo de clase, el classmethod y el método de instancia.
    # -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 4 · Dunder methods (__str__, __repr__, __eq__, __len__)
# =========================================================================================
def seccion_4_dunder():
    encabezado("SECCIÓN 4 · Dunder methods (__str__, __repr__, __eq__, __len__)" )
    print("Objetivo: mejorar impresión/depuración/comparación y, si aplica, longitud.\n")

    # * Teoría clave
    # * __str__ (humano), __repr__ (depuración), __eq__ (igualdad lógica), __len__ (tamaño).

    # ? Cómo funciona el ejercicio
    # - Punto(x,y): __str__ → "(x,y)", __repr__ → "Punto(x=.., y=..)", __eq__ por coords.
    # - Demuestra impresión y comparación.
    #
    # TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
    # Implementa la clase y una breve demo.
    # -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 5 · Encapsulación con @property (getter/setter con validación)
# =========================================================================================
def seccion_5_property():
    encabezado("SECCIÓN 5 · Encapsulación con @property (getter/setter)")
    print("Objetivo: validar campos mediante propiedades y setters.\n")

    # * Teoría clave
    # * @property define lectura, setter valida y mantiene invariantes.

    # ? Cómo funciona el ejercicio
    # - Termometro con celsius y fahrenheit (ambos properties). Valida celsius > -273.15.
    #
    # TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
    # Implementa la clase y demuestra set en fahrenheit y lectura en celsius.
    # -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 6 · Herencia simple y super()
# =========================================================================================
def seccion_6_herencia():
    encabezado("SECCIÓN 6 · Herencia simple y super()")
    print("Objetivo: crear jerarquías y sobreescribir métodos reutilizando con super().\n")

    # * Teoría clave
    # * Subclase hereda de clase base; super().__init__ reutiliza inicialización.

    # ? Cómo funciona el ejercicio
    # - Empleado(Persona) con salario: float y ficha() → "<nombre> - <salario>€".
    # - Crea 2 empleados, muestra presentarse() (heredado) y ficha().
    #
    # TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
    # Implementa las clases y una pequeña demostración.
    # -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 7 · Composición (objetos que contienen otros objetos)
# =========================================================================================
def seccion_7_composicion():
    encabezado("SECCIÓN 7 · Composición (objetos que contienen otros objetos)")
    print("Objetivo: modelar relaciones tiene‑un y calcular totales.\n")

    # * Teoría clave
    # * Un objeto contiene otros (lista de objetos) y agrega/consulta su estado.

    # ? Cómo funciona el ejercicio
    # - Biblioteca que contiene Libros; métodos añadir(libro) y buscar_por_autor(autor)->list[str].
    # - Demuestra con 3 libros.
    #
    # TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
    # Implementa las clases y demuestra su uso.
    # -------------------------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 8 · Autoevaluación final (Tienda POO)
# =========================================================================================
def seccion_8_autoevaluacion():
    encabezado("SECCIÓN 8 · Autoevaluación final (Tienda POO)")
    print("Objetivo: integrar clases, propiedades, dunder, composición y herencia.\n")

    # TODO: ZONA DEL ALUMNO ---------------------------------------------------------------
    # Implementa:
    # 1) Producto(nombre:str, precio:float) con __str__/__repr__ y __eq__ por nombre.
    # 2) Cliente(nombre:str, saldo:float) con @property saldo (no negativo) y cargar(+€).
    # 3) Carrito con add(p), total(), __len__().
    # 4) Pedido(cliente, carrito) con pagar() si saldo >= total.
    # 5) ClienteVIP(Cliente) que aplica 10% descuento automático en pagar().
    # 6) Demostración y resumen final (1 línea) tipo dashboard.
    # -------------------------------------------------------------------------------


# =========================================================================================
#  MENÚ para ejecutar tus ejercicios por secciones
# =========================================================================================
def menu():
    # Modo no interactivo: ejecuta TODO una vez y sale (evita bucles infinitos)
    if not RUN_INTERACTIVE:
        seccion_1_clases_objetos()
        seccion_2_init_self()
        seccion_3_class_attrs()
        seccion_4_dunder()
        seccion_5_property()
        seccion_6_herencia()
        seccion_7_composicion()
        seccion_8_autoevaluacion()
        return

    # Modo interactivo: menú con bucle y opción de salida
    while True:
        print("\n===== MENÚ DEL ALUMNO · Clase 6 (POO) =====")
        print("  1) Clases y objetos")
        print("  2) __init__ y self")
        print("  3) Atributos de clase · classmethod · staticmethod")
        print("  4) Dunder methods")
        print("  5) @property (encapsulación)")
        print("  6) Herencia y super()")
        print("  7) Composición")
        print("  8) Autoevaluación final (Tienda POO)")
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
            seccion_1_clases_objetos(); pause()
        elif op == 2:
            seccion_2_init_self(); pause()
        elif op == 3:
            seccion_3_class_attrs(); pause()
        elif op == 4:
            seccion_4_dunder(); pause()
        elif op == 5:
            seccion_5_property(); pause()
        elif op == 6:
            seccion_6_herencia(); pause()
        elif op == 7:
            seccion_7_composicion(); pause()
        elif op == 8:
            seccion_8_autoevaluacion(); pause()
        elif op == 9:
            seccion_1_clases_objetos(); seccion_2_init_self(); seccion_3_class_attrs(); seccion_4_dunder(); seccion_5_property(); seccion_6_herencia(); seccion_7_composicion(); seccion_8_autoevaluacion(); pause()
        else:
            print("! Elige una opción del 0 al 9.")


if __name__ == "__main__":
    menu()

# *******************************************************************************************
# * IMPORTANTE: NO SE PERMITE EL USO DE INTELIGENCIA ARTIFICIAL PARA RESOLVER ESTE EXAMEN. *
# * SOLO PUEDES UTILIZAR LOS APUNTES CREADOS POR TI COMO REFERENCIA.                       *
# *******************************************************************************************

# -------------------------------------------------------------------------------------------
# * SECCIÓN 1: Ejemplo básico de clases y objetos (2 PUNTOS)
# TODO: Crea una clase `Soldado` que tenga:
#   - Dos atributos: `nombre` y `rango`.
#   - Un método `mostrar_informacion` que imprima los valores de estos atributos.

class Soldado:
    pass  # Escribe el código aquí


# -------------------------------------------------------------------------------------------
# * SECCIÓN 2: Atributos y métodos (3 PUNTOS)
# TODO: Crea una clase `UnidadMilitar` con:
#   - Atributos: `nombre_unidad`, `tipo_unidad`, `estado` (por defecto "inactivo").
#   - Métodos:
#       - `activar`: Cambia el estado a "activo".
#       - `desactivar`: Cambia el estado a "inactivo".
#       - `mostrar_informacion`: Imprime todos los atributos.

class UnidadMilitar:
    pass  # Escribe el código aquí


# -------------------------------------------------------------------------------------------
# * SECCIÓN 3: Herencia (2 PUNTOS)
# TODO: Crea una clase `UnidadEspecial` que herede de `UnidadMilitar` y:
#   - Tenga un atributo adicional: `especialidad`.
#   - Sobrescriba el método `mostrar_informacion` para incluir la especialidad.

class UnidadEspecial(UnidadMilitar):
    pass  # Escribe el código aquí


# -------------------------------------------------------------------------------------------
# * SECCIÓN 4: Encapsulación (3 PUNTOS)
# TODO: Crea una clase `SoldadoPrivado` con:
#   - Atributos privados: `__nombre` y `__codigo_id`.
#   - Métodos:
#       - `obtener_nombre`: Devuelve `__nombre`.
#       - `cambiar_codigo_id`: Cambia `__codigo_id` solo si tiene al menos 5 caracteres.

class SoldadoPrivado:
    pass  # Escribe el código aquí
