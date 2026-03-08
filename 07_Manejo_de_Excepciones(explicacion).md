# 🐍 Clase 7 de Python — Manejo de Excepciones (try/except/else/finally, raise, custom) + IA

**Autor:** Joaquín Rodríguez — *Guía didáctica para principiantes con enfoque robusto*
**Objetivo global:** Dominar el manejo de **errores y excepciones en Python** usando `try/except`, capturas múltiples, bloques `else/finally`, `raise`, excepciones personalizadas, patrones de validación y reintento, `assert` y buenas prácticas. Finaliza con **Laboratorio IA** y **Autoevaluación**.

---

## 🧭 Cómo usar este material

1. Ejecuta `07_Manejo de Excepciones.py` y usa el menú (opciones **1–9**).
2. En cada sección: **lee la teoría**, prueba la **demo**, completa la **ZONA DEL ALUMNO**.
3. Finaliza con la **Autoevaluación final** para practicar todos los conceptos juntos.

> 💡 **Tip docente:** Haz que el alumnado provoque errores adrede (división entre 0, índice fuera de rango, entrada vacía) para ver cómo Python responde.

---

## 🧩 Mapa del temario (menú del programa)

1. `try/except` básico
2. Múltiples `except` y jerarquía de errores
3. Bloques `else` y `finally`
4. Lanzar excepciones con `raise`
5. Excepciones personalizadas
6. Patrones de validación y reintento seguro
7. `assert` y buenas prácticas
8. Laboratorio IA (mini‑programa robusto)
9. Autoevaluación final
10. Ejecutar TODO (1→9)

---

## SECCIÓN 1 · try/except básico

### 🎯 Objetivos

* Manejar errores con `try/except` para evitar que el programa se detenga.
* Capturar errores esperados (p. ej. `ValueError`).

### 🧠 Teoría

```py
try:
    # código que puede fallar
except TipoDeError:
    # qué hacer si ocurre ese error
```

Evita `except` sin tipo: captura solo lo que esperas.

### 👀 Demo guiada

```py
texto = input("Introduce un número entero: ")
try:
    n = int(texto)
    print("OK, entero:", n)
except ValueError:
    print("Ese texto no es un entero.")
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **División segura**: pide dos números y divide `a/b`. Captura:

  * `ValueError` (conversión inválida).
  * `ZeroDivisionError` (si `b=0`).

---

## SECCIÓN 2 · Múltiples except y jerarquía de errores

### 🎯 Objetivos

* Usar varios `except` según el error.
* Respetar el orden: de específico a general.

### 👀 Demo guiada

```py
arr = [10, 20, 30]
try:
    idx = int(input("Índice (0..2): "))
    print("Elemento:", arr[idx])
except ValueError as e:
    print("Conversión inválida:", e)
except IndexError as e:
    print("Índice fuera de rango:", e)
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Diccionario seguro**: dado `{'a':1, 'b':2}`, pide clave y muestra valor.

  * Captura `KeyError` si no existe.
  * Captura `ValueError` si la clave se trata mal (ej. convertir a int).

---

## SECCIÓN 3 · else y finally

### 🎯 Objetivos

* Usar `else` para ejecutar código si **NO** hubo excepción.
* Usar `finally` para ejecutar código **siempre** (ej. cerrar recursos).

### 👀 Demo guiada

```py
try:
    x = 10 / int(input("Divisor: "))
    print("Resultado:", x)
except ZeroDivisionError:
    print("No puedes dividir entre cero.")
else:
    print("Operación completada sin errores.")
finally:
    print("Fin de la operación (se ejecuta siempre).")
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Login simple**: pide usuario y contraseña (`admin/1234`).

  * Si ambos correctos → `else: print("Login OK")`.
  * En `finally`: imprime `"Cerrando sesión..."`.

---

## SECCIÓN 4 · raise (lanzar excepciones) y validación

### 🎯 Objetivos

* Lanzar errores cuando se violen condiciones.
* Crear funciones más seguras.

### 👀 Demo guiada

```py
def leer_edad(texto: str) -> int:
    if texto.strip() == "":
        raise ValueError("La edad es requerida")
    edad = int(texto)
    if edad < 0:
        raise ValueError("La edad no puede ser negativa")
    return edad
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Precio válido**: `leer_precio(texto)` que lance `ValueError` si vacío o <0.
* Úsalo en un `try/except` para mostrar precio válido o error.

---

## SECCIÓN 5 · Excepciones personalizadas

### 🎯 Objetivos

* Definir errores propios heredando de `Exception`.
* Usarlos en lógica de negocio.

### 👀 Demo guiada

```py
class SaldoInsuficiente(Exception):
    pass

class Cuenta:
    def __init__(self, saldo=0):
        self.saldo = saldo
    def pagar(self, importe):
        if importe > self.saldo:
            raise SaldoInsuficiente("Saldo insuficiente")
        self.saldo -= importe
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Stock agotado**: Crea `class StockAgotado(Exception)`.
* Función `vender(stock, unidades)` que lance `StockAgotado` si `unidades > stock`.
* Maneja la excepción con un mensaje útil.

---

## SECCIÓN 6 · Patrones de validación / reintento seguro

### 🎯 Objetivos

* Reintentar varias veces con control de errores.
* Usar `else` tras el bucle si no hubo éxito.

### 👀 Demo guiada

```py
intentos_max = 3
for i in range(1, intentos_max+1):
    try:
        n = int(input(f"Introduce entero (intento {i}): "))
        break
    except ValueError:
        print("No es un entero.")
else:
    print("Agotados los intentos.")
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Pedir float**: función `pedir_float(msg, intentos=3)` que reintente.
* Prueba leyendo un precio.

---

## SECCIÓN 7 · assert (opcional) y buenas prácticas

### 🎯 Objetivos

* Usar `assert` para comprobar condiciones en desarrollo.
* Recordar: no usar para validaciones críticas de usuario.

### 👀 Demo guiada

```py
def dividir(a,b):
    assert b != 0, "b no puede ser 0"
    return a/b
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Verificar lista**: función `media(lista)` que haga `assert lista, "Lista vacía"`.
* Si lista válida, devuelve media.
* Prueba con `[]` y `[1,2,3]`.

---

## SECCIÓN 8 · Laboratorio IA (programa robusto con entradas)

### 🎯 Objetivos

* Generar con IA un mini‑programa de 30–45 líneas con excepciones.
* Mejorar el código integrando buenas prácticas vistas.

### 🧰 Prompt Kit

1. **Generación**

   > “Eres profesor de Python. Genera un programa (30–45 líneas) que pida datos (nombre, unidades, precio), calcule total con cupones y maneje excepciones (`ValueError`, `ZeroDivisionError`). Usa `try/except`, `else/finally` y al menos un `raise`. Solo código Python.”

2. **Alternativo**

   > “Crea un conversor de divisas con validación (reintentos 3). Lanza `ValueError` si importe <0 y excepción personalizada `TipoMonedaDesconocido`. ≤ 45 líneas.”

3. **Mejora**

   > “Añade un resumen final en una línea y separa la lógica en funciones con docstrings. Mantén ≤50 líneas.”

### 🛠️ ZONA DEL ALUMNO · TODO

* Pide a la IA el código con el Prompt Kit y pégalo en `mi_programa_ia()`.
* Ejecuta, valida y mejora con resúmenes o validaciones.

---

## AUTOEVALUACIÓN FINAL · Caja registradora robusta

### 🎯 Objetivos

* Combinar todo en un flujo robusto.

### 🛠️ Enunciado

1. `leer_float(msg)` con reintento (3) y `ValueError` controlado.
2. `class DescuentoInvalido(Exception)` para cupones fuera 0–100%.
3. `total_con_descuento(base, unidades, desc)` que lance:

   * `DescuentoInvalido` si desc no está en rango.
   * `ValueError` si base<0 o unidades<=0.
4. Flujo principal:

   * Pide base, unidades, desc.
   * Calcula total con `try/except/else/finally`.
   * En `finally`: `print("Cierre de operación")`.
5. Resumen tipo dashboard:
   `"Base:<€> | Unidades:<n> | Desc:<%> | Total:<€> | Estado:<OK/ERROR>"`

### 📏 Rúbrica

* **Correcto**: controla errores, usa excepciones personalizadas, bloque finally.
* **Excelente**: validaciones claras, mensajes descriptivos, dashboard formateado.

---

## APÉNDICE A · Patrones útiles

* **try/except en cascada:**

```py
try:
    ...
except ValueError:
    ...
except Exception as e:
    print("Error genérico:", e)
```

* **Reintento seguro:**

```py
for _ in range(3):
    try:
        ...
        break
    except ValueError:
        print("Intenta de nuevo")
else:
    print("Falló tras 3 intentos")
```

* **Custom exception mínima:**

```py
class MiError(Exception):
    pass
```

---

## APÉNDICE B · Buenas prácticas

* Captura **solo lo necesario**.
* Mensajes claros y específicos en cada excepción.
* Usa `else`/`finally` para separar la lógica.
* Prefiere excepciones personalizadas para tu dominio.
* No abuses de `assert` en producción.
* Documenta las funciones con docstrings.

---

## ✅ Qué has aprendido

* Capturar errores con `try/except`.
* Manejar múltiples `except` y jerarquías.
* Usar bloques `else` y `finally`.
* Lanzar errores con `raise`.
* Definir excepciones personalizadas.
* Aplicar patrones de validación y reintento.
* Validar con `assert` en desarrollo.
* Construir un **mini‑programa robusto** y una **caja registradora** integradora.

---
