# 🐍 Clase 5 de Python — Listas, Diccionarios y Bucles Anidados (+ ordenación, comprensiones, IA)

**Autor:** Joaquín Rodríguez — *Guía didáctica para principiantes*
**Objetivo global:** Dominar colecciones en Python (**listas y diccionarios**), trabajar con **bucles anidados**, aprender a **ordenar con key/lambda**, practicar **comprensiones** y cerrar con un **laboratorio IA** + autoevaluación final.

---

## 🧭 Cómo usar este material

1. Ejecuta `05_listas_diccionarios_bucles_anidados.py` y usa el menú (opciones **1–9**).
2. Revisa teoría + demos y completa los **TODO** en la **ZONA DEL ALUMNO**.
3. Termina con la **Autoevaluación final** para integrar todo.

> 💡 **Tip docente:** plantea ejemplos cercanos (agenda, inventario, perfiles) para que el alumnado entienda la utilidad real de las colecciones.

---

## 🧩 Mapa del temario (menú del programa)

1. Listas: creación, acceso, slicing y métodos
2. Diccionarios: acceso, actualización y utilidades
3. Iterar diccionarios (keys/values/items)
4. Estructuras anidadas + bucles anidados
5. Ordenación con key/lambda + min/max/sum
6. Comprensiones (listas y diccionarios) \[opcional]
7. Laboratorio IA (colecciones creativas)
8. Autoevaluación final
9. Ejecutar TODO (1→8)

---

## SECCIÓN 1 · Listas — creación, acceso, slicing y métodos

### 🎯 Objetivos

* Crear y modificar listas.
* Usar métodos comunes (`append`, `insert`, `remove`, `pop`, `sort`, `reverse`).

### 👀 Demo guiada

```py
productos = ["bolígrafo", "cuaderno", "grapas"]
productos.append("carpeta")
productos.insert(1, "regla")
productos.remove("grapas")
print(productos)
```

### 🛠️ ZONA DEL ALUMNO · TODO

* Crea lista con 4 ciudades. Inserta una en la posición 2. Elimina la última.
* Muestra longitud, primera, última y slice 1:3.

---

## SECCIÓN 2 · Diccionarios — acceso, actualización y utilidades

### 🎯 Objetivos

* Crear y actualizar diccionarios.
* Usar `.get()`, `.keys()`, `.values()`, `.items()`.

### 👀 Demo guiada

```py
perfil = {"nombre": "Lucía", "edad": 20, "premium": False}
perfil["premium"] = True
perfil["puntos"] = perfil.get("puntos", 0) + 50
print(perfil)
print(perfil.items())
```

### 🛠️ ZONA DEL ALUMNO · TODO

* Crea `contacto` con nombre, teléfono y email.
* Actualiza el teléfono, añade ciudad y muestra todos sus items en líneas.

---

## SECCIÓN 3 · Iterar diccionarios (keys / values / items)

### 🎯 Objetivos

* Recorrer diccionarios con `for`.
* Diferenciar claves, valores e items.

### 👀 Demo guiada

```py
precios = {"bolígrafo": 1.2, "cuaderno": 2.5}
for nombre, precio in precios.items():
    print(f"{nombre}: {precio:.2f} €")
```

### 🛠️ ZONA DEL ALUMNO · TODO

* Con `{"A":10, "B":0, "C":7}` muestra `X -> stock OK` si >0, si no `sin stock`.

---

## SECCIÓN 4 · Estructuras anidadas + bucles anidados

### 🎯 Objetivos

* Manejar colecciones dentro de colecciones.
* Usar bucles anidados para recorrer estructuras.

### 👀 Demo guiada

```py
catalogo = [
    {"nombre": "Pack Estudio", "items": ["cuaderno", "bolígrafo"]},
    {"nombre": "Pack Oficina", "items": ["carpeta", "grapas"]},
]
for pack in catalogo:
    print(pack["nombre"])
    for item in pack["items"]:
        print(" -", item)
```

### 🛠️ ZONA DEL ALUMNO · TODO

* Lista de dicts con clases y alumnos.
* Recorre y muestra: `Clase X:` y luego alumnos con guion.

---

## SECCIÓN 5 · Ordenación con key/lambda + min/max/sum

### 🎯 Objetivos

* Ordenar listas de dicts con `sorted(..., key=...)`.
* Usar `min`, `max`, `sum` con key o generadores.

### 👀 Demo guiada

```py
productos = [
  {"nombre": "cuaderno", "precio": 2.5},
  {"nombre": "carpeta", "precio": 3.6},
]
ordenados = sorted(productos, key=lambda p: p["precio"])
mas_barato = min(productos, key=lambda p: p["precio"])
total = sum(p["precio"] for p in productos)
```

### 🛠️ ZONA DEL ALUMNO · TODO

* Lista de dicts con `{"nombre":..., "nota":...}`.
* Ordénalos por nota descendente y muestra: `Mejor alumno: <nombre> (<nota>)`.

---

## SECCIÓN 6 · Comprensiones (listas y diccionarios) \[opcional]

### 🎯 Objetivos

* Usar comprensiones para crear colecciones de forma compacta.

### 👀 Demo guiada

```py
nums = [1,2,3,4,5,6]
pares_cuadrados = [n*n for n in nums if n%2==0]
precios = {"A":10, "B":5}
con_iva = {k: round(v*1.21,2) for k,v in precios.items()}
```

### 🛠️ ZONA DEL ALUMNO · TODO

* Dado un dict producto→stock, crea otro dict solo con los que `stock>0`.

---

## SECCIÓN 7 · Laboratorio IA (Colecciones creativas)

### 🎯 Objetivos

* Aprender a pedir miniprogramas con colecciones y bucles anidados.
* Integrar y mejorar el código.

### 🧰 Prompt Kit

1. **Generación**

   > “Eres profesor de Python. Genera un programa (30–45 líneas) que use listas, diccionarios y bucles anidados. Tema: **inventario de tienda** con categorías y precios. Incluye sorted con key y resumen final. Solo código Python.”

2. **Alternativo**

   > “Crea un **gestor de clases** con lista de dicts (clase, alumnos) que permita agregar/borrar y ordenar por tamaño de clase.”

3. **Mejora**

   > “Optimiza con comprensiones y min/max/sum con key. Mantén <45 líneas.”

### 👀 Demo opcional

```py
catalogo = [
 {"nombre": "cuaderno", "precio": 2.5},
 {"nombre": "pendrive", "precio": 9.9},
]
barato = min(catalogo, key=lambda x: x["precio"])
print(barato)
```

### 🛠️ ZONA DEL ALUMNO · TODO

* Pide a la IA el código con el Prompt Kit, pégalo en `mi_programa_ia()` y ejecútalo.

---

## SECCIÓN 8 · Autoevaluación final

### 🎯 Objetivos

* Integrar listas, diccionarios, bucles anidados, ordenación y comprensiones.

### 🛠️ Enunciado

1. Crea lista de dicts `inventario` con `{nombre, categoria, precio, stock}`.
2. Muestra productos agrupados por categoría (dict + bucle anidado).
3. Ordena por precio asc y muestra top 3 más baratos.
4. Calcula valor total del stock (`precio*stock`).
5. Usa comprensión para `{nombre: precio_con_iva}`.
6. Resumen final:
   `"Items:<n> | Categorías:<m> | Valor stock:<€> | Barato:<nombre-precio>"`

### 📏 Rúbrica

* **Correcto**: cumple requisitos.
* **Excelente**: validaciones, orden claro, resumen formateado.

---

## APÉNDICE A · Patrones útiles

* **Lista de diccionarios:**

```py
alumnos = [
 {"nombre":"Ana", "nota":8},
 {"nombre":"Luis", "nota":6},
]
```

* **Agrupación en dict:**

```py
grupo = {"A":[1,2], "B":[3,4]}
```

* **Comprensión filtrada:**

```py
{p:stock for p,stock in inv.items() if stock>0}
```

---

## APÉNDICE B · Buenas prácticas

* Usa nombres descriptivos (`inventario`, `contacto`).
* Prefiere `get()` para valores opcionales.
* En bucles anidados, cuida la indentación.
* Usa comprensiones para crear colecciones de forma clara.

---

## APÉNDICE C · Retos extra

1. **Diccionario de frecuencias**: contar palabras en un texto.
2. **Ranking**: ordenar alumnos y mostrar top 5.
3. **Inventario avanzado**: añadir función para vender producto y actualizar stock.
4. **Cruce de datos**: de 2 listas (`nombres`, `notas`), crear lista de dicts.

---

## ✅ Qué has aprendido

* Manejar listas: creación, acceso, métodos.
* Usar diccionarios: acceso, actualización, utilidades.
* Recorrer diccionarios con `for`.
* Trabajar con estructuras anidadas y bucles anidados.
* Ordenar con `sorted`, `min`, `max`, `sum`.
* Usar comprensiones para listas y dicts.
* Aplicar todo en un proyecto integrador (inventario).

---
