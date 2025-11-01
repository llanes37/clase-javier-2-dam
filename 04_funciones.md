# 🐍 Clase 4 de Python — Funciones (Versión Básica)

**Autor:** Joaquín Rodríguez — *Guía didáctica adaptada a nivel inicial*
**Objetivo global:** Aprender a definir y usar funciones en Python sin complicaciones avanzadas. Practicaremos:

* Funciones sin parámetros.
* Funciones con parámetros (posicionales).
* Uso de `return` (devolver valores).
* Parámetros con valores por defecto y keyword args.
* Scope básico (variables locales vs externas).
* Buenas prácticas iniciales.
* Laboratorio IA con funciones sencillas.
* Autoevaluación final.

---

## 🧭 Cómo usar este material

1. Ejecuta `04_funciones.py` y utiliza el menú (opciones **1–9**).
2. Revisa la teoría, ejecuta las demos, completa los **TODO** en la zona del alumno.
3. Finaliza con la **Autoevaluación final**.

> 💡 **Tip docente:** Motiva a los alumnos a escribir sus propias funciones en papel antes de probarlas en el IDE, para interiorizar bien la estructura.

---

## 🧩 Mapa del temario (menú del programa)

1. Funciones **sin parámetros** (solo ejecutan una tarea).
2. Funciones **con parámetros** (posicionales).
3. `return` (devolver valores).
4. Parámetros con valores por defecto · keyword args.
5. Scope básico (local vs. externo).
6. Buenas prácticas (puras vs. con efectos).
7. Laboratorio IA (funciones sencillas).
8. Autoevaluación final.
9. Ejecutar TODO (1→8).

---

## SECCIÓN 1 · Funciones SIN parámetros

### 🎯 Objetivos

* Crear funciones que **solo ejecuten algo** sin necesitar datos externos.

### 👀 Demo guiada

```py
def linea():
    print("-" * 40)

def saludar():
    print("¡Bienvenido/a al curso de Python!")

saludar()
linea()
print("Este mensaje va debajo de una línea separadora.")
linea()
```

### 🛠️ ZONA DEL ALUMNO · TODO

* Crea `banner()` que imprima:

  ```
  ======
    Hola  
  ======
  ```
* Llama 2 veces a la función.

---

## SECCIÓN 2 · Funciones CON parámetros (posicionales)

### 🎯 Objetivos

* Pasar **valores externos** a la función.
* Reutilizar la misma función con distintos parámetros.

### 👀 Demo guiada

```py
def saludar_a(nombre):
    print(f"Hola, {nombre} 👋")

def repetir(texto, veces):
    for _ in range(veces):
        print(texto)

saludar_a("Ana")
repetir("Aprendiendo funciones...", 2)
```

### 🛠️ ZONA DEL ALUMNO · TODO

* Define `mostrar_cuadricula(simbolo, ancho)` que imprima una línea con `simbolo` repetido `ancho` veces.
* Llama con `#`, `*` y `=` cambiando los anchos.

---

## SECCIÓN 3 · return (devolver valores)

### 🎯 Objetivos

* Usar `return` para **guardar resultados** y reutilizarlos.

### 👀 Demo guiada

```py
def cuadrado(n):
    return n * n

def suma(a, b):
    return a + b

print("Cuadrado:", cuadrado(4))
print("Suma 2+3:", suma(2, 3))
```

### 🛠️ ZONA DEL ALUMNO · TODO

* Define `precio_con_iva(base, iva)` que devuelva `base * (1 + iva/100)`.
* Prueba con `100, 21`.

---

## SECCIÓN 4 · Parámetros por defecto y uso por nombre

### 🎯 Objetivos

* Evitar repetir valores comunes con **parámetros por defecto**.
* Usar **keyword args** para mayor claridad.

### 👀 Demo guiada

```py
def saludo(nombre="Invitado"):
    print(f"Hola, {nombre}")

def precio_final(base, iva=21, descuento=0):
    return base * (1 + iva/100) * (1 - descuento/100)

saludo()
saludo("Alicia")
print("precio_final(100) →", precio_final(100))
print("precio_final(base=200, descuento=10) →", precio_final(base=200, descuento=10))
```

### 🛠️ ZONA DEL ALUMNO · TODO

* Crea `repetir_msg(msg="Hola", veces=2)` que imprima `msg` tantas veces.
* Llama por posición y por keyword.

---

## SECCIÓN 5 · Scope básico (local vs. externo)

### 🎯 Objetivos

* Diferenciar variables **locales** y **externas**.
* Fomentar el patrón entradas → salidas, evitando globales.

### 👀 Demo guiada

```py
def incrementar(contador, paso=1):
    return contador + paso

c = 0
c = incrementar(c)
c = incrementar(c, 2)
print("Contador:", c)

x = 10
def duplicar_local(x):
    x = x * 2
    return x

print("x externa:", x, "| duplicada:", duplicar_local(x), "| tras llamar:", x)
```

### 🛠️ ZONA DEL ALUMNO · TODO

* Define `agregar_saldo(saldo, cantidad)` que devuelva nuevo saldo.
* Empieza en 0, haz 3 operaciones (2 ingresos, 1 gasto) y muestra saldo final.

---

## SECCIÓN 6 · Buenas prácticas iniciales

### 🎯 Objetivos

* Entender funciones **puras** vs. con efectos.
* Usar nombres claros y descriptivos.

### 👀 Demo guiada

```py
def area_rect_print(base, altura):
    print("Área:", base * altura)

def area_rect(base, altura):
    return base * altura

area_rect_print(3, 4)
res = area_rect(3, 4)
print("Área reutilizable:", res, "→ puedo usarlo en otra operación:", res + 10)
```

### 🛠️ ZONA DEL ALUMNO · TODO

* Define `media(a, b, c)` que devuelva la media de 3 números.
* Muestra: `"La media es X"` con 2 decimales.

---

## SECCIÓN 7 · Laboratorio IA (funciones sencillas)

### 🎯 Objetivos

* Practicar con prompts a IA para generar programas de funciones simples.
* Integrar el código y mejorarlo.

### 🧰 Prompt Kit

1. **Generación**

   > “Eres profesor de Python. Genera un programa de 20–30 líneas con 4–5 funciones simples (sin tipos avanzados) que calcule: `precio_final(base, iva=21)`, `aplicar_descuento(total, dto)`, `sumar(a,b)`, `es_par(n)`, `imprimir_ticket(total)`. Incluye comentarios con `# *` y `# TODO`. Solo código Python.”

2. **Alternativo**

   > “Crea funciones para una mini‑calculadora: sumar/restar/multiplicar/dividir (con if para división por 0) y una función `mostrar_menu()`. 20–30 líneas. Sin librerías.”

3. **Mejora**

   > “Refactoriza para que las funciones devuelvan valores (puras) y solo imprimir en una capa final.”

### 🛠️ ZONA DEL ALUMNO · TODO

* Pide a la IA el miniprograma con el Prompt Kit, pégalo en `mi_programa_ia()`.
* Ejecútalo desde el menú y modifícalo con mejoras.

---

## AUTOEVALUACIÓN FINAL · Calculadora simple

### 🎯 Objetivos

* Integrar lo aprendido en funciones sencillas.

### 🛠️ Enunciado

Implementa y prueba:

1. `mostrar_titulo()` → imprime “CALCULADORA” con un marco.
2. `sumar`, `restar`, `multiplicar`, `dividir` (si `b==0` devuelve “Error”).
3. `precio_con_iva(base, iva=21)` → devuelve el total.
4. `total_compra(p1, p2, p3)` → suma 3 precios.

**Demostración**:

* Llama a `mostrar_titulo()`.
* Calcula y muestra: `sumar(5,7)`, `dividir(10,0)`, `precio_con_iva(100)`, `total_compra(3,4,5)`.
* Imprime una última línea tipo dashboard:
  `"Suma:<..> | Div:<..> | IVA:<..> | Total:<..>"`

---

## APÉNDICE A · Buenas prácticas

* Nombres de funciones con **verbos** (`calcular_total`, `obtener_media`).
* Mantén funciones **cortas y claras**.
* Evita `global`; usa patrón entrada → salida.
* Prefiere funciones puras siempre que sea posible.

---

## APÉNDICE B · Retos extra

1. Función `es_primo(n)` → True/False.
2. `contar_vocales(texto)` que devuelva nº de vocales.
3. `tabla_multiplicar(n)` que imprima tabla 1–10.
4. `convertir_segundos(s)` → (h,m,s).

---

## ✅ Qué has aprendido

* Crear funciones básicas con y sin parámetros.
* Usar `return` para devolver valores.
* Definir valores por defecto y llamar con keyword args.
* Diferenciar variables locales y externas.
* Aplicar buenas prácticas iniciales.
* Integrar todo en una **calculadora simple** como autoevaluación.

---
