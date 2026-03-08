# 🐍 Clase 6 de Python — Programación Orientada a Objetos (POO)

**Autor:** Joaquín Rodríguez — *Guía didáctica para principiantes con enfoque práctico*
**Objetivo global:** Dominar los **fundamentos de POO en Python**: clases, objetos, atributos/métodos, `__init__` y `self`, **atributos de clase** vs. **instancia**, `@classmethod`/`@staticmethod`, **dunder methods** (`__str__`, `__repr__`, `__eq__`, `__len__`), **encapsulación con `@property`**, **herencia** y **composición**. Cierra con **Laboratorio IA** y **Autoevaluación**.

---

## 🧭 Cómo usar este material

1. Ejecuta `06_Programación Orientada a Objetos.py` y utiliza el **menú** (opciones **1–10**).
2. En cada sección: **lee la teoría**, ejecuta la **demo**, completa la **ZONA DEL ALUMNO (TODO)**.
3. Termina con la **Autoevaluación**: diseña una mini‑“Tienda” POO con composición y herencia.

> 💡 **Tip docente**: pide explicar en voz alta *por qué* se usa `self`, cuándo un dato debe ser **de instancia** o **de clase**, y por qué `@property` mejora el diseño.

---

## 🧩 Mapa del temario (menú del programa)

1. Clases y objetos (atributos y métodos)
2. `__init__` y `self` (inicialización de estado)
3. Atributos de clase · `@classmethod` · `@staticmethod`
4. Representación y dunder methods (`__str__`/`__repr__`/`__eq__`/`__len__`)
5. Encapsulación con `@property` (getter/setter con validación)
6. Herencia simple y `super()`
7. Composición (objetos que **tienen** otros objetos)
8. Laboratorio IA (mini‑proyecto POO)
9. Autoevaluación final (mezcla de todo)
10. Ejecutar TODO (1→9)

---

## SECCIÓN 1 · Clases y objetos (atributos y métodos)

### 🎯 Objetivos

* Crear clases con **atributos de instancia** y **métodos**.
* Entender que `self` es la **instancia actual**.

### 🧠 Teoría en claro

```py
class Nombre:
    def __init__(self, ...):
        self.atributo = valor
    def metodo(self, ...):
        return ...
```

* **Objeto** = instancia concreta de una clase.

### 👀 Demo guiada

```py
class Producto:
    def __init__(self, nombre: str, precio: float):
        self.nombre = nombre
        self.precio = precio
    def info(self) -> str:
        return f"{self.nombre} - {self.precio:.2f} €"

p = Producto("Cuaderno", 2.5)
print(p.info())
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Persona simple**: `class Persona(nombre, edad)` con `presentar()` → `"Soy <nombre> y tengo <edad> años"`.
  Crea 2 personas y muestra su presentación.

---

## SECCIÓN 2 · `__init__` y `self` (inicialización de estado)

### 🎯 Objetivos

* Comprender que `__init__` **inicializa** la instancia.
* Añadir **métodos** que cambian el estado.

### 👀 Demo guiada

```py
class Cuenta:
    def __init__(self, titular: str, saldo_inicial: float = 0.0):
        self.titular = titular
        self.saldo = saldo_inicial
    def depositar(self, cantidad: float):
        self.saldo += cantidad
    def mostrar(self) -> str:
        return f"{self.titular} | Saldo: {self.saldo:.2f} €"

c = Cuenta("Alicia", 50); c.depositar(25)
print(c.mostrar())
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Libro**: `class Libro(titulo, autor, paginas:int)` con `ficha()` → `"<titulo> de <autor> (<pag> pags)"`.
  Crea 2 libros y muestra su ficha.

---

## SECCIÓN 3 · Atributos de clase · `@classmethod` · `@staticmethod`

### 🎯 Objetivos

* Distinguir **atributos de instancia** (`self.x`) de **clase** (`Clase.x`).
* Usar `@classmethod` como **fábricas** y `@staticmethod` como **utilidades**.

### 👀 Demo guiada

```py
class Usuario:
    contador = 0  # atributo de clase
    def __init__(self, nombre: str):
        self.nombre = nombre
        Usuario.contador += 1
    @classmethod
    def desde_cadena(cls, texto: str):  # p.ej. "nombre:ana"
        _, nombre = texto.split(":"); return cls(nombre)
    @staticmethod
    def normalizar(texto: str) -> str:
        return texto.strip().title()

u1 = Usuario("lucía"); u2 = Usuario.desde_cadena("nombre:ana")
print(Usuario.contador, Usuario.normalizar("  hola mundo  "))
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Producto factoría + IVA**: `class Producto(IVA=21)` con `@classmethod desde_linea("nombre;precio")` y método `precio_con_iva()`.

---

## SECCIÓN 4 · Dunder methods: `__str__`, `__repr__`, `__eq__`, `__len__`

### 🎯 Objetivos

* Mejorar **impresión**, **depuración** y **comparación** de objetos.
* Sumar unidades con `__len__` cuando tenga sentido.

### 👀 Demo guiada

```py
class Item:
    def __init__(self, nombre: str, unidades: int):
        self.nombre, self.unidades = nombre, unidades
    def __str__(self):
        return f"{self.nombre} x{self.unidades}"
    def __repr__(self):
        return f"Item({self.nombre!r}, {self.unidades!r})"
    def __eq__(self, other):
        return isinstance(other, Item) and self.nombre == other.nombre

class Carrito:
    def __init__(self):
        self.items: list[Item] = []
    def add(self, it: Item):
        self.items.append(it)
    def __len__(self) -> int:
        return sum(i.unidades for i in self.items)
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Punto**: `class Punto(x, y)` con `__str__ → "(x,y)"`, `__repr__ → "Punto(x=..., y=...)"`, y `__eq__` por coordenadas.
  Imprime dos puntos y su comparación.

---

## SECCIÓN 5 · Encapsulación y `@property` (getter/setter con validación)

### 🎯 Objetivos

* Encapsular campos con `@property` y validar en el **setter**.
* Evitar estados inválidos (p. ej., saldos negativos).

### 👀 Demo guiada

```py
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
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Termómetro**: `class Termometro` con `celsius` y `fahrenheit` (ambos properties).
  Valida `celsius > -273.15`. Fórmulas:
  `F = C * 9/5 + 32`  ·  `C = (F - 32) * 5/9`
  Demuestra set en **fahrenheit** y lectura en **celsius**.

---

## SECCIÓN 6 · Herencia simple y `super()`

### 🎯 Objetivos

* Crear jerarquías **Padre → Hijo** y **sobre‑escribir** métodos.
* Reusar inicialización con `super().__init__()`.

### 👀 Demo guiada

```py
class Persona:
    def __init__(self, nombre: str):
        self.nombre = nombre
    def presentarse(self):
        return f"Hola, soy {self.nombre}"

class Estudiante(Persona):
    def __init__(self, nombre: str, curso: str):
        super().__init__(nombre)
        self.curso = curso
    def presentarse(self):
        return f"{super().presentarse()} y estudio {self.curso}"
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Empleado**: `class Empleado(Persona)` con `salario: float` y `ficha()` → `"<nombre> - <salario>€"`.
  Crea 2 empleados, muestra **presentación** y **ficha**.

---

## SECCIÓN 7 · Composición (objetos que contienen otros objetos)

### 🎯 Objetivos

* Modelar relaciones **tiene‑un** (e.g., `Carrito` **tiene** `Productos`).
* Calcular totales agregando atributos de objetos contenidos.

### 👀 Demo guiada

```py
class Producto:
    def __init__(self, nombre: str, precio: float):
        self.nombre, self.precio = nombre, precio

class Carrito:
    def __init__(self):
        self.items: list[Producto] = []
    def agregar(self, p: Producto):
        self.items.append(p)
    def total(self) -> float:
        return round(sum(p.precio for p in self.items), 2)
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Biblioteca**: `class Biblioteca` con lista de `Libros`.
  Métodos: `añadir(libro)`, `buscar_por_autor(autor) -> list[str]` (títulos).
  Demuestra su uso con 3 libros.

---

## SECCIÓN 8 · Laboratorio IA (POO creativa)

### 🎯 Objetivos

* Pedir a la IA un **mini‑sistema POO** y **mejorarlo**.

### 🧰 Prompt Kit (copia/pega y ejecuta)

1. **Generación**

   > “Eres profesor de Python. Diseña un mini‑sistema POO (35–50 líneas) con:
   > • Clases `Usuario` y `Pedido`; `Usuario` tiene un `Carrito` (composición) con `Productos`.
   > • `@property` para validar saldo del Usuario; `__str__/__repr__` mínimos.
   > • Un método de Usuario para **pagar pedido** (usa `total()` del carrito).
   > Devuelve **SOLO código Python**, sin librerías.”

2. **Alternativo**

   > “Crea `Juego`, `Jugador`, `Partida` con herencia (`JugadorHumano`/`JugadorIA`), marcador y resumen final. Usa `@classmethod` para crear desde texto. ≤ 40 líneas.”

3. **Mejora**

   > “Añade un **método estático** de validación y un `__eq__` útil. Mantén ≤ 50 líneas.”

### 🛠️ ZONA DEL ALUMNO · TODO

* Pide el miniproyecto con el **Prompt Kit**, pégalo en tu zona de práctica y ejecútalo.
* Añade **validaciones**, **docstrings** y un **resumen final** (una sola línea).

---

## AUTOEVALUACIÓN FINAL · Tienda POO

### 🎯 Objetivos

* Integrar **clases**, **propiedades**, **dunder methods**, **composición** y **herencia**.

### 🛠️ Enunciado

Implementa un pequeño dominio **“Tienda”**:

1. `Producto(nombre:str, precio:float)` con `__str__/__repr__` y `__eq__` por nombre.
2. `Cliente(nombre:str, saldo:float)` con `@property saldo` (no negativo) y método `cargar(+€)`.
3. `Carrito` con composición de `Producto` (lista). Métodos: `add(p)`, `total()`, `__len__()`.
4. `Pedido(cliente, carrito)` → `pagar()` descuenta del cliente si `saldo >= total`.
5. **Herencia**: `ClienteVIP(Cliente)` aplica **10% descuento** automático (sobrescribe `pagar()`).
6. **Demostración**: crea 3 productos, un cliente y un VIP, simula pedidos y muestra **dashboard**:
   `"Cliente:<nom> Saldo:<€> | ClienteVIP:<nom> Saldo:<€> | Items:<len> Total:<€>"`

### 📏 Rúbrica rápida

* **Correcto**: clases bien definidas, composición, herencia simple y `@property` funcional.
* **Excelente**: `__str__/__repr__/__eq__` claros, validaciones sólidas, resumen final legible.

---

## APÉNDICE A · Patrones y decisiones de diseño

* **¿Atributo de clase o de instancia?**

  Usa **clase** para información **compartida** (p.ej., IVA, contador de instancias).
  Usa **instancia** para datos **propios** de cada objeto.

* **Fábricas con `@classmethod`**: permiten **múltiples constructores** (p.ej., `desde_cadena`).

* **`@staticmethod`**: utilidades “puros” sin dependencias de `self`/`cls`.

* **`__eq__` vs identidad**: `a == b` (igualdad lógica) no es lo mismo que `a is b` (misma referencia).

* **`__repr__`**: que sea **no ambiguo** y útil para depurar; idealmente, que permita re‑crear el objeto.

---

## APÉNDICE B · Buenas prácticas (POO en Python)

* Nombres **claros** y consistentes; métodos **pequeños** con una sola responsabilidad.
* Evita `global`; **devuelve valores** o encapsula el estado.
* Usa `@property` para validar estados y mantener **invariantes**.
* Documenta con **docstrings** y añade **type hints** para legibilidad.
* Considera `dataclasses` cuando tengas **clases de datos** simples (no imprescindible, pero útil).

---

## APÉNDICE C · Errores comunes (y cómo evitarlos)

* Olvidar `self` en la firma de métodos de instancia.
* Usar **atributos de clase mutables** (listas/dicts) como contenedores “compartidos” sin querer.
* `@property` con **recursión infinita** (asignar a `self.saldo` dentro del setter de `saldo` en vez de a `self._saldo`).
* Confundir `__str__` con `__repr__` o no implementar `__eq__` cuando comparas objetos semánticos.
* No validar en setters: estados inválidos (p.ej., `saldo < 0`).

---

## APÉNDICE D · Retos extra (para subir el nivel)

1. **Polimorfismo**: `MedioPago` → `Tarjeta`, `PayPal`, `SaldoMonedero` con un método común `pagar(total)`.
2. **Mixins**: `LogMixin` que añade trazas a clases existentes (`__repr__` enriquecido).
3. **Igualdad y hashing**: añade `__hash__` coherente con `__eq__` para usar objetos como claves.
4. **Dataclasses**: re‑escribe `Producto` y `Cliente` como `@dataclass` e interpreta el `repr` generado.
5. **Tests rápidos**: añade 3 `doctest` dentro de docstrings y ejecútalos con `python -m doctest -v`.

---

## ✅ Qué has aprendido

* Crear clases, instancias y métodos con `self`.
* Inicializar estado con `__init__`.
* Diferenciar atributos **de clase** y **de instancia**, y usar `@classmethod`/`@staticmethod`.
* Representar y comparar objetos con **dunder methods**.
* Encapsular y validar con `@property`.
* Aplicar **herencia** y **composición** para modelar dominios reales.
* Construir un **mini‑proyecto POO** de principio a fin.

---
