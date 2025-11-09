# =========================================================================================
#  🐍 PYTHON CLASE 6 — PROGRAMACIÓN ORIENTADA A OBJETOS (POO)
#  ────────────────────────────────────────────────────────────────────────────────────────
#  📘 En esta clase practicarás:
#    * Clases y objetos: atributos y métodos
#    * __init__ y uso de self
#    * Atributos de clase vs. de instancia · @classmethod · @staticmethod
#    * Representación y dunder methods: __str__/__repr__/__eq__/__len__ (opcional)
#    * Encapsulación con properties (@property, setter con validación)
#    * Herencia simple y super()
#    * Composición (objetos que contienen otros objetos)
#    * Laboratorio IA (mini-proyecto orientado a objetos)
#    * Autoevaluación final (mezcla de todo)
#
#  🎨 Better Comments:
#    # ! importante   ·  # * definición/foco   ·  # ? idea/nota
#    # TODO: práctica  ·  # NOTE: apunte útil   ·  # // deprecado
# =========================================================================================

from typing import Any, List

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

def safe_input(prompt: str, caster, default):
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
#  SECCIÓN 1 · Clases y objetos (atributos y métodos)
# =========================================================================================
def seccion_1():
    encabezado("SECCIÓN 1 · Clases y objetos (atributos y métodos)")

    # * TEORÍA
    # class Nombre:
    #     # atributos (datos) y métodos (funciones) que actúan sobre esos datos
    #     def metodo(self, ...): ...
    # self → referencia al propio objeto (instancia).

    # * DEMO
    class Producto:
        def __init__(self, nombre: str, precio: float):
            self.nombre = nombre
            self.precio = precio

        def info(self) -> str:
            return f"{self.nombre} - {self.precio:.2f} €"

    p = Producto("Cuaderno", 2.5)
    print("Producto DEMO →", p.info())

    # TODO: (Tema: PERSONA SIMPLE)
    # Crea clase Persona con atributos nombre y edad, y un método presentar() que devuelva
    # "Soy <nombre> y tengo <edad> años".
    # Instancia 2 personas y muestra su presentación.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 2 · __init__ y self (inicialización de estado)
# =========================================================================================
def seccion_2():
    encabezado("SECCIÓN 2 · __init__ y self")

    # * TEORÍA
    # __init__ se ejecuta al crear el objeto: inicializa atributos de instancia.

    # * DEMO
    class Cuenta:
        def __init__(self, titular: str, saldo_inicial: float = 0.0):
            self.titular = titular          # atributo de instancia
            self.saldo = saldo_inicial

        def depositar(self, cantidad: float):
            self.saldo += cantidad

        def mostrar(self) -> str:
            return f"{self.titular} | Saldo: {self.saldo:.2f} €"

    c = Cuenta("Alicia", 50)
    c.depositar(25)
    print("Cuenta DEMO →", c.mostrar())

    # TODO: (Tema: LIBRO)
    # Clase Libro con titulo (str), autor (str) y paginas (int). Método ficha() → "<titulo> de <autor> (<pag> pags)".
    # Crea 2 libros y muestra su ficha.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 3 · Atributos de clase, @classmethod y @staticmethod
# =========================================================================================
def seccion_3():
    encabezado("SECCIÓN 3 · Atributos de clase, classmethod y staticmethod")

    # * TEORÍA
    # - Atributo de instancia: pertenece a cada objeto (self.algo).
    # - Atributo de clase: compartido por todas las instancias (Clase.algo).
    # - @classmethod: recibe la clase (cls) → factorías alternativas.
    # - @staticmethod: utilidades que no usan ni self ni cls.

    # * DEMO
    class Usuario:
        contador = 0  # atributo de clase

        def __init__(self, nombre: str):
            self.nombre = nombre
            Usuario.contador += 1

        @classmethod
        def desde_cadena(cls, texto: str):
            # "nombre:Lucía" → Usuario("Lucía")
            _, nombre = texto.split(":")
            return cls(nombre)

        @staticmethod
        def normalizar(texto: str) -> str:
            return texto.strip().title()

    u1 = Usuario("lucía")
    u2 = Usuario.desde_cadena("nombre:ana")
    print("Usuarios creados:", Usuario.contador)
    print("Normalizado:", Usuario.normalizar("   hola mundo  "))

    # TODO: (Tema: PRODUCTO FACTORÍA)
    # Crea clase Producto con atributo de clase IVA=21. Crea un @classmethod desde_linea("nombre;precio")
    # que devuelva un Producto. Añade método precio_con_iva() y comprueba con 2 productos.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 4 · Representación y dunder methods (__str__/__repr__/__eq__/__len__)
# =========================================================================================
def seccion_4():
    encabezado("SECCIÓN 4 · __str__/__repr__/__eq__/__len__")

    # * TEORÍA
    # __str__  → representación "bonita" para humanos (print)
    # __repr__ → representación para desarrolladores (debug)
    # __eq__   → igualdad personalizada (==)
    # __len__  → longitud (len(obj)) si aplica

    # * DEMO
    class Item:
        def __init__(self, nombre: str, unidades: int):
            self.nombre = nombre
            self.unidades = unidades

        def __str__(self) -> str:
            return f"{self.nombre} x{self.unidades}"

        def __repr__(self) -> str:
            return f"Item({self.nombre!r}, {self.unidades!r})"

        def __eq__(self, other: Any) -> bool:
            return isinstance(other, Item) and self.nombre == other.nombre

    class Carrito:
        def __init__(self):
            self.items: List[Item] = []

        def add(self, item: Item):
            self.items.append(item)

        def __len__(self) -> int:
            return sum(i.unidades for i in self.items)

    i1, i2, i3 = Item("bolígrafo", 2), Item("bolígrafo", 2), Item("cuaderno", 1)
    print("i1 == i2 ?", i1 == i2, "| i1 == i3 ?", i1 == i3)
    carro = Carrito(); carro.add(i1); carro.add(i3)
    print("Carrito unidades (len):", len(carro))
    print("Mostrar item:", str(i1))
    print("Debug item:", repr(i1))

    # TODO: (Tema: REPR BONITO)
    # Crea clase Punto(x, y) con __str__ como "(x,y)" y __repr__ como "Punto(x=..., y=...)".
    # Compara igualdad por coordenadas e imprime dos puntos y su comparación.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 5 · Encapsulación y propiedades (@property)
# =========================================================================================
def seccion_5():
    encabezado("SECCIÓN 5 · Encapsulación y properties")

    # * TEORÍA
    # Convención de "privado": _atributo o __atributo (name mangling).
    # @property  → getter como atributo
    # @<prop>.setter → validaciones al asignar

    # * DEMO
    class CuentaSegura:
        def __init__(self, titular: str, saldo: float = 0.0):
            self.titular = titular
            self._saldo = 0.0
            self.saldo = saldo  # usa setter

        @property
        def saldo(self) -> float:
            return self._saldo

        @saldo.setter
        def saldo(self, valor: float):
            if valor < 0:
                raise ValueError("El saldo no puede ser negativo")
            self._saldo = valor

    cs = CuentaSegura("Ana", 100.0)
    cs.saldo += 20
    print(f"Saldo de {cs.titular}: {cs.saldo:.2f} €")

    # TODO: (Tema: TEMPERATURA)
    # Clase Termometro con propiedad celsius (float) y propiedad fahrenheit (convierte).
    # Validar que celsius > -273.15. Demuestra set en fahrenheit y lectura en celsius.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 6 · Herencia simple y super()
# =========================================================================================
def seccion_6():
    encabezado("SECCIÓN 6 · Herencia simple y super()")

    # * TEORÍA
    # class Hija(Padre):  → hereda atributos y métodos
    # super().__init__(...) para inicializar la parte de la clase base
    # Override: redefinir un método en la hija

    # * DEMO
    class Persona:
        def __init__(self, nombre: str):
            self.nombre = nombre

        def presentarse(self) -> str:
            return f"Hola, soy {self.nombre}"

    class Estudiante(Persona):
        def __init__(self, nombre: str, curso: str):
            super().__init__(nombre)
            self.curso = curso

        def presentarse(self) -> str:      # override
            base = super().presentarse()
            return f"{base} y estudio {self.curso}"

    e = Estudiante("Lucas", "Python")
    print(e.presentarse())

    # TODO: (Tema: EMPLEADO)
    # Clase Empleado(Persona) con salario (float) y método ficha() → "<nombre> - <salario>€".
    # Crea 2 empleados y muestra su presentación y ficha.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 7 · Composición (objetos que contienen otros objetos)
# =========================================================================================
def seccion_7():
    encabezado("SECCIÓN 7 · Composición (objetos dentro de objetos)")

    # * TEORÍA
    # Un objeto "tiene un" conjunto de otros objetos. Ej: Carrito tiene Items.

    # * DEMO
    class Producto:
        def __init__(self, nombre: str, precio: float):
            self.nombre = nombre
            self.precio = precio

    class Carrito:
        def __init__(self):
            self.items: List[Producto] = []

        def agregar(self, p: Producto):
            self.items.append(p)

        def total(self) -> float:
            return round(sum(p.precio for p in self.items), 2)

    carro = Carrito()
    carro.agregar(Producto("Cuaderno", 2.5))
    carro.agregar(Producto("Bolígrafo", 1.2))
    print("Total carrito:", carro.total(), "€")

    # TODO: (Tema: BIBLIOTECA)
    # Clase Biblioteca con lista de Libros. Métodos: añadir(libro), buscar_por_autor(autor) → lista títulos.
    # Demuestra su uso con 3 libros.
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  SECCIÓN 8 · Laboratorio IA (POO creativa)
# =========================================================================================
def seccion_8_ia():
    encabezado("SECCIÓN 8 · Laboratorio IA (POO creativa)")

    # * PROMPT KIT (copia/pega en ChatGPT)
    # 1) PROMPT BREVE:
    #    "Eres profesor de Python. Diseña un mini-sistema POO (35–50 líneas) con:
    #     - Clases Usuario y Pedido; Usuario tiene un Carrito (composición) con Productos.
    #     - @property para validar saldo del Usuario; __str__/__repr__ mínimos.
    #     - Un método de Usuario para pagar pedido (usa total del carrito).
    #     Devuélveme SOLO código Python, sin librerías."
    #
    # 2) PROMPT ALTERNATIVO:
    #    "Crea clases Juego, Jugador y Partida: herencia simple (JugadorHumano/JugadorIA),
    #     marcador y resumen final. Usa @classmethod para crear desde texto. 40 líneas."
    #
    # 3) PROMPT DE MEJORA:
    #    "Mejora el diseño con un método estático de validación y un __eq__ útil. Mantén 50 líneas."

    # * DEMO opcional
    if IA_DEMO:
        class DemoUser:
            def __init__(self, nombre: str, saldo: float = 0.0):
                self.nombre = nombre
                self._saldo = saldo

            @property
            def saldo(self) -> float:
                return self._saldo

            def __str__(self):
                return f"{self.nombre}({self._saldo:.2f}€)"

        print("Demo IA →", DemoUser("Ana", 15.5))

    # TODO: (Tema: PROGRAMA PROPUESTO POR IA)
    # 1) Pide a ChatGPT el miniproyecto con el PROMPT KIT.
    # 2) Pega el código debajo y ejecútalo desde el menú.
    # 3) Modifícalo a tu gusto.
    #
    # --- ZONA DEL ALUMNO ---------------------------------------------------------------
    # def mi_proyecto_ia():
    #     # pega aquí el código que te generó la IA
    #     pass
    # mi_proyecto_ia()


# =========================================================================================
#  AUTOEVALUACIÓN FINAL (mezcla de todo)
# =========================================================================================
def autoevaluacion():
    encabezado("AUTOEVALUACIÓN FINAL · Tienda POO")

    # TODO: (ENUNCIADO)
    # Implementa un pequeño dominio “Tienda”:
    #
    # 1) Clase Producto(nombre:str, precio:float) con __str__/__repr__ y __eq__ por nombre.
    # 2) Clase Cliente(nombre:str, saldo:float) con @property saldo (no negativo) y método cargar(+€).
    # 3) Clase Carrito con composición de productos (lista). Métodos: add(p), total(), __len__().
    # 4) Clase Pedido(cliente, carrito):
    #    - método pagar(): si saldo >= total → descuenta y devuelve True; si no, False.
    # 5) Herencia simple:
    #    - ClienteVIP(Cliente): aplica 10% descuento automático en pedidos (sobrescribe pagar()).
    # 6) Demostración:
    #    - Crea 3 productos, un cliente y un cliente VIP. Simula un pedido con cada uno.
    #    - Muestra un “dashboard” final:
    #      "Cliente:<nom> Saldo:<€> | ClienteVIP:<nom> Saldo:<€> | Items:<len> Total:<€>"
    #
    # --- ZONA DEL ALUMNO -----------------------------------------------------------------


# =========================================================================================
#  MENÚ PRINCIPAL
# =========================================================================================
def menu():
    while True:
        print_firma()
        print("MENÚ · Elige una opción")
        print("  1) Clases y objetos")
        print("  2) __init__ y self")
        print("  3) Atributos de clase / classmethod / staticmethod")
        print("  4) Representación y dunders")
        print("  5) Encapsulación y properties")
        print("  6) Herencia simple y super()")
        print("  7) Composición")
        print("  8) Laboratorio IA (POO)")
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
