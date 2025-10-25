# 🐍 Clase 1 de Python — Variables, Entradas, Colecciones y Operadores (+ Laboratorio IA)

**Autor:** Joaquín Rodríguez — _Material didáctico para tu curso de iniciación a Python_  
**Objetivo global:** Sentar unas bases sólidas de programación con Python trabajando **variables**, **entradas con seguridad**, **listas y diccionarios**, **operadores** y un **laboratorio con IA**. El archivo base incluye un **menú** con secciones, utilidades de entrada segura y una **autoevaluación final**. :contentReference[oaicite:0]{index=0}

---

## 🧭 Cómo usar este material

1. **Ejecuta el archivo** `01_variable.py` para ver el **menú** con todas las secciones. Desde ahí puedes recorrerlas una a una o lanzarlas todas seguidas. :contentReference[oaicite:1]{index=1}  
2. El script trae **conmutadores** para adaptar la experiencia:  
   - `RUN_INTERACTIVE`: pide datos reales por teclado (True) o usa **valores por defecto** (False).  
   - `PAUSE`: pausa entre secciones.  
   - `IA_DEMO`: activa/desactiva una pequeña demostración del laboratorio de IA. :contentReference[oaicite:2]{index=2}
3. Se incluyen utilidades:
   - `safe_input(prompt, caster, default)`: **lee, castea y devuelve** un valor con **fallback** si hay error o no hay entrada.  
   - `print_firma()` y `encabezado(titulo)` para presentación. :contentReference[oaicite:3]{index=3}

> **Sugerencia del profe:**  
> Durante clase usa `RUN_INTERACTIVE=True`. Para grabaciones, pruebas rápidas o ejecución en entornos sin teclado, cambia a `False` y el código correrá con **datos de ejemplo**.

---

## 🧩 Estructura por secciones

El menú del programa ofrece:  
**1) Variables** · **2) Entrada segura** · **3) Listas y Diccionarios** · **4) Operadores** · **5) Laboratorio IA** · **6) Autoevaluación** · **7) Ejecutar todo**. :contentReference[oaicite:4]{index=4}

---

## SECCIÓN 1 · Variables básicas y f-strings

### 🎯 Objetivos
- Comprender qué es una **variable** y cómo Python **infieren tipos** (str, int, float, bool).
- Mostrar información formateada con **f-strings**: `f"Hola {nombre}"`. :contentReference[oaicite:5]{index=5}

### 🧠 Teoría en claro
- **Variable**: nombre que referencia un valor en memoria.  
- **Tipado dinámico**: no declaras tipos; Python los infiere.  
- **f-strings**: interpolan variables de forma legible y eficiente.

### 👀 Demo guiada
El ejemplo crea un **perfil** con nombre, edad, altura y activo, y lo muestra en una línea mediante f-string. Úsalo de plantilla para tus propios datos. :contentReference[oaicite:6]{index=6}

### 🛠️ Práctica (TODO)
**“Perfil rápido”**: crea `usuario (str)`, `ciudad (str)`, `puntos (int)`, `activo (bool)` y muestra:  
`"Usuario <usuario> de <ciudad> | Puntos: <puntos> | Activo: <activo>"`. :contentReference[oaicite:7]{index=7}

### ✅ Checklist de dominio
- [ ] Sé declarar variables con nombres significativos.  
- [ ] Sé cuándo usar `int`, `float`, `str`, `bool`.  
- [ ] Sé formatear con `f"{var:.2f}"` para decimales.

---

## SECCIÓN 2 · Entrada segura (input) + mini-cálculos

### 🎯 Objetivos
- Pedir datos por teclado de forma **robusta**.
- Calcular totales con números enteros y decimales.

### 🧠 Teoría en claro
- `input()` devuelve **texto** → conviértelo con `int()` o `float()`.  
- Usa `safe_input(prompt, caster, default)` para **evitar errores**: si el usuario pulsa Enter vacío o escribe mal, **devuelve un valor por defecto** y el programa **no se rompe**. :contentReference[oaicite:8]{index=8}

### 👀 Demo guiada
Se piden `unidades (int)` y `precio (float)`, se calcula `total = unidades * precio` y se muestra con 2 decimales: `f"{total:.2f} €"`. Si `RUN_INTERACTIVE=False`, se usan valores por defecto. :contentReference[oaicite:9]{index=9}

### 🛠️ Práctica (TODO)
**“Conversor sencillo”**: pide kilómetros (`float`) y conviértelos a **millas** (1 km = **0.621371**). Muestra con 2 decimales.

### 🔎 Tips de calidad
- Valida siempre las entradas; documenta el **rango aceptable** (p.ej., no negativos).  
- Da **feedback** claro cuando uses un valor por defecto (el programa ya lo hace). :contentReference[oaicite:10]{index=10}

---

## SECCIÓN 3 · Listas y Diccionarios

### 🎯 Objetivos
- Dominar colecciones básicas: **listas** (ordenadas y mutables) y **diccionarios** (pares `clave: valor`).  
- Practicar operaciones: `append`, `pop`, **slicing**, acceso y actualización de claves. :contentReference[oaicite:11]{index=11}

### 🧠 Teoría en claro
- **Lista**: `cursos = ["HTML", "CSS"]`; añade con `append()`, accede con índices, corta con `cursos[1:3]`.  
- **Diccionario**: `alumno = {"nombre": "Lucía", "edad": 20}`; actualiza/añade con `alumno["premium"] = True`. :contentReference[oaicite:12]{index=12}

### 👀 Demo guiada
- Lista `cursos`: se añade `"JavaScript"`, se muestra la lista completa, el primer elemento y un **slice**.  
- Diccionario `alumno`: se marca `premium=True` y se añade `pais="España"`. :contentReference[oaicite:13]{index=13}

### 🛠️ Práctica (TODO)
1) **Agenda de tareas**: crea una lista `tareas` con 3 elementos, añade 1, muestra **total**, **primera** y **última**.  
2) **Contacto**: crea `contacto = {nombre, telefono, email}`; actualiza `telefono` y añade `ciudad`. :contentReference[oaicite:14]{index=14}

### 🧩 Errores típicos
- Índices fuera de rango `IndexError`.  
- Claves inexistentes en dict (`KeyError`): usa `in` o `get("clave", valor_por_defecto)`.

---

## SECCIÓN 4 · Operadores (aritméticos, comparación, lógicos, asignación)

### 🎯 Objetivos
- Usar con soltura **operadores**: `+ - * / // % **`, comparaciones `> < >= <= == !=`, lógicos `and or not` y **asignación compuesta** `+= -= *= ...`. :contentReference[oaicite:15]{index=15}

### 👀 Demo guiada
- Se imprimen resultados de operaciones aritméticas, comparaciones (incluida comparación lexicográfica de cadenas) y lógicas.  
- Se muestra una variable `x` modificada con `+=` y `*=`. :contentReference[oaicite:16]{index=16}

### 🛠️ Práctica (TODO)
**“Calculadora mini”**: pide dos números y muestra:
- Todas las operaciones básicas `+ - * / // % **`.  
- Tres comparaciones (`>`, `<`, `==`) y una **combinación lógica** (ej. `a>0 and b>0`). :contentReference[oaicite:17]{index=17}

### 🧩 Errores típicos
- División por cero.  
- Enteros vs. floats: el operador `/` devuelve **float**; usa `//` para división entera.

---

## SECCIÓN 5 · Laboratorio IA (Variables creativas)

### 🎯 Objetivos
- Aprender a **pedirle a la IA** que genere **miniprogramas** útiles (20–40 líneas) con requisitos pedagógicos.  
- Integrar el código generado en tu práctica y **mejorarlo** iterativamente. :contentReference[oaicite:18]{index=18}

### 🧰 “Prompt Kit” recomendado
1. **Prompt breve (generación)**  
   > “Eres profesor de Python. Genera un programa de **30 líneas** que use **variables, listas y operadores**. Tema: **‘carrito de la compra sencillo’** (sin librerías). Requisitos: **nombres en español**, **comentarios claros** (# * / # TODO), **sin clases ni funciones avanzadas**. Devuélveme **SOLO código Python**.” :contentReference[oaicite:19]{index=19}  
2. **Prompt alternativo (tema deporte/juego)**  
   > “Crea un **marcador de partido** con variables, lista de anotaciones y operadores. Añade **inputs opcionales** (si no hay input, usa valores por defecto).” :contentReference[oaicite:20]{index=20}  
3. **Prompt de mejora**  
   > “Mejora este código para que tenga **2 comprobaciones de errores** y un **resumen final** formateado en 1 línea. **Manténlo < 40 líneas**.” :contentReference[oaicite:21]{index=21}

### 👀 Demo opcional (IA_DEMO=True)
Se muestra un **marcador** con listas de puntos por equipo, suma con `sum()` y **operador ternario** para decidir el ganador. Puedes apagarlo con `IA_DEMO=False`. :contentReference[oaicite:22]{index=22}

### 🛠️ Práctica (TODO)
1) Pide a la IA un miniprograma con el **Prompt Kit** (elige tema).  
2) **Copia** el código que te devuelva y **pégalo** en la **ZONA DEL ALUMNO** de esta sección.  
3) **Ejecuta y adapta**: añade validaciones o un resumen final con f-string. :contentReference[oaicite:23]{index=23}

> **Consejo:** cuando pidas código a la IA, especifica **“solo código Python”** para pegarlo tal cual. Si algo falla, copia **el error completo** y pide: “**Arréglalo paso a paso**”. :contentReference[oaicite:24]{index=24}

---

## 🏁 Autoevaluación final · Proyecto integrador

### 🎯 Objetivos
- Integrar todo lo aprendido en un **mini-proyecto** con variables, entrada segura, colecciones y operadores. :contentReference[oaicite:25]{index=25}

### 🛠️ Tareas (TODO)
1) Variables: `nombre_usuario (str)`, `edad (int)`, `ciudad (str)`, `activo (bool)`.  
2) Entrada y cálculo: `unidades (int)`, `precio (float)`, `total = unidades * precio`.  
3) Lista `tareas`: 3 iniciales + 1 añadida; muestra total, primera y última.  
4) Diccionario `perfil`: nombre, edad, ciudad, activo; añade `puntos`.  
5) Operadores: con dos números, muestra **suma**, **resta** y una **comparación**.  
6) **Resumen final** (una sola línea con f-string):  
   `"Usuario <nombre> | Tareas:<n> | Total compra:<importe> €"`. :contentReference[oaicite:26]{index=26}

### 📏 Rúbrica rápida
- **Correcto**: todas las partes completadas, entradas validadas, salida clara y formateada.  
- **Excelente**: mensajes de error útiles, funciones auxiliares, pruebas con valores límite.

---

## 🧩 Apéndice A · Menú principal y flujo de uso

El programa presenta un **menú interactivo** con las opciones **0–7** y ejecuta la sección elegida. La opción **7** recorre **todas** las secciones de forma encadenada. Ideal para una **demo completa** en clase. :contentReference[oaicite:27]{index=27}

> **Nota:** si introduces una opción inválida, el programa te avisa y vuelve a pedir selección. :contentReference[oaicite:28]{index=28}

---

## 🧩 Apéndice B · Convención “Better Comments”

El archivo usa una convención de comentarios para **enfatizar** ideas:
- `# !` importante — `# *` definición/foco — `# ?` idea/nota  
- `# TODO:` práctica — `# NOTE:` apunte útil — `# //` deprecado  
Úsala también en tu código para guiar al alumno. :contentReference[oaicite:29]{index=29}

---

## 🚀 Retos extra (para subir el nivel)

1. **Formateo pro**: muestra importes con separadores de miles (`f"{n:,.2f}"`).  
2. **Validación fuerte**: crea `input_entero_positivo()` que repita la pregunta hasta obtener un entero ≥ 0.  
3. **Mini-reportes**: a partir de `tareas` y `perfil`, genera un informe en 3 líneas y otra versión en **una sola línea** (estilo “dashboard”).  
4. **Diccionarios anidados**: gestiona múltiples alumnos con una lista de diccionarios y filtra por `premium == True`.  
5. **IA + pruebas**: pide a la IA un programa y añádele **2 tests manuales** (bloques que impriman “OK/FAIL” comparando salida esperada vs. real).

---

## 🧯 Solución de problemas comunes

- **EOFError** o ejecución sin entrada: pon `RUN_INTERACTIVE=False` o usa `safe_input` para garantizar **valores por defecto**. :contentReference[oaicite:30]{index=30}  
- **ValueError al castear**: envuelve las conversiones con `safe_input(..., int/float, default)` y comunica el fallback al usuario (ya lo hace la función). :contentReference[oaicite:31]{index=31}  
- **Cortes de flujo**: activa `PAUSE=True` para avanzar sección a sección en directo. :contentReference[oaicite:32]{index=32}

---

## 📦 Qué has aprendido

- Fundamentos de **variables** y **f-strings**.  
- **Entrada segura** con manejo de errores y valores por defecto.  
- Trabajo con **listas** y **diccionarios**.  
- Uso de **operadores** esenciales.  
- Cómo **pedir, integrar y mejorar** código generado por **IA**.  
- Un **menú didáctico** para practicar progresivamente y una **autoevaluación** integradora. :contentReference[oaicite:33]{index=33}

> Este material está pensado para **explicar, practicar y evaluar**. Siéntete libre de ampliarlo con nuevas secciones (p.ej., **condicionales** y **bucles**) siguiendo el mismo patrón y estilo de comentarios.

---
