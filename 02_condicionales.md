# 🐍 Clase 2 de Python — Condicionales (if/elif/else), `and`/`or`/`not`, Truthy/Falsy, Ternario y `match/case` (+ Laboratorio IA)

**Autor:** Joaquín Rodríguez — *Guía didáctica para principiantes*
**Objetivo global:** Dominar el **flujo condicional** en Python con `if/elif/else`, operadores lógicos, noción de **truthy/falsy**, **operador ternario**, y (opcional) `match/case` (Python ≥ 3.10). Incluye prácticas guiadas, “ZONA DEL ALUMNO”, laboratorio con IA y autoevaluación.

---

## 🧭 Cómo usar este material

1. Lee cada sección en orden.
2. Ejecuta los **ejemplos** y completa los **TODO** en la *ZONA DEL ALUMNO*.
3. Cierra con la **Autoevaluación Final** para integrar todo.

> 💡 **Tip docente:** Para clase en directo, pide **casos límite** (0, negativo, cadena vacía, etc.) y que expliquen **por qué** ocurre cada resultado.

---

## 🧩 Mapa del temario

1. `if` básico
2. `if / elif / else`
3. Condiciones compuestas (`and`/`or`/`not`) + `if` anidado
4. Truthy / Falsy + `bool()`
5. Operador ternario
6. `match / case` (Python ≥ 3.10)
7. Laboratorio IA (condicionales creativos)
8. Autoevaluación final
9. Apéndices (patrones, estilo, errores comunes, retos extra)

---

## SECCIÓN 1 · `if` básico (una condición)

### 🎯 Objetivos

* Entender la estructura mínima de un `if` y la **indentación**.
* Practicar una **condición simple** sobre un dato de entrada.

### 🧠 Teoría en claro

```py
if <condición>:
    <bloque>  # Se ejecuta solo si la condición es True
# El resto del programa continúa aquí
```

* La condición se evalúa con comparadores: `>`, `<`, `>=`, `<=`, `==`, `!=`.
* Python **no** usa llaves; el **bloque** lo marca la **indentación** (convención: 4 espacios).

### 👀 Demo guiada

```py
edad = 19
if edad >= 18:
    print("Puedes entrar ✅")
print("Fin de la comprobación.")
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Mayoría de edad**: pide o fija una `edad`. Si `>= 18`, imprime **“Mayor de edad”**. No hagas nada en caso contrario.

---

## SECCIÓN 2 · `if / elif / else` (múltiples caminos)

### 🎯 Objetivos

* Encadenar **ramas** y comprender que se ejecuta **solo la primera condición True**.
* Crear **clasificadores** por rangos.

### 🧠 Teoría en claro

```py
if cond1:
    ...
elif cond2:
    ...
else:
    ...
```

Evaluación **de arriba a abajo**; al cumplirse una rama, las siguientes **no se evalúan**.

### 👀 Demo guiada · Clasificador de notas

```py
nota = 8.3
if nota >= 9:
    nivel = "Sobresaliente"
elif nota >= 7:
    nivel = "Notable"
elif nota >= 5:
    nivel = "Aprobado"
else:
    nivel = "Suspenso"
print(f"Tu nivel: {nivel}")
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Semáforo**: con `color` (`"rojo"`, `"amarillo"`, `"verde"`), imprime:

  * rojo → **“Para”**
  * amarillo → **“Precaución”**
  * verde → **“Adelante”**
  * otro → **“Color no válido”**

---

## SECCIÓN 3 · Condiciones compuestas `and` / `or` / `not` + `if` anidado

### 🎯 Objetivos

* Combinar condiciones con **lógicos**.
* Mostrar **mensajes específicos** con `if` anidados.

### 🧠 Teoría en claro

* `A and B` → True si **ambas** son verdaderas.
* `A or B`  → True si **alguna** es verdadera.
* `not A`   → **invierte** el booleano.

### 👀 Demo guiada · Acceso al evento

```py
edad = 17
tiene_entrada = True
if edad >= 18 and tiene_entrada:
    print("Acceso concedido 🎟️")
else:
    if edad < 18:
        print("Acceso denegado: menor de edad")
    if not tiene_entrada:
        print("Acceso denegado: necesitas una entrada")
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Descuento tienda**: `es_estudiante` (True/False) y `total` (float).

  * Si `es_estudiante and total >= 20` → 10% descuento. Si no → 0%.
  * Muestra el **total final** y el **motivo** (p.ej., “no cumple mínimo”).

---

## SECCIÓN 4 · Truthy / Falsy + `bool()`

### 🎯 Objetivos

* Entender qué valores se consideran **verdaderos** o **falsos** al evaluar condiciones.
* Evitar errores por asumir que cualquier cosa “existe” y es True.

### 🧠 Teoría en claro

* **Falsy** en Python: `0`, `0.0`, `""`, `[]`, `()`, `{}`, `set()`, `None`, `False`.
* Todo lo demás tiende a ser **Truthy**.
* `bool(valor)` devuelve el booleano correspondiente.

### 👀 Demo guiada

```py
print(bool(0))       # False
print(bool("hola"))  # True
print(bool([]))      # False
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Validador de nombre**: si `nombre` es cadena **no vacía**, imprime `"¡Hola, <nombre>!"`; si no, `"Nombre requerido"`.

---

## SECCIÓN 5 · Operador ternario (expresión condicional)

### 🎯 Objetivos

* Escribir condiciones **compactas** en una sola línea manteniendo legibilidad.

### 🧠 Teoría en claro

```py
mensaje = "mayor" if edad >= 18 else "menor"
```

Formato: `<valor_si_true> if <condición> else <valor_si_false>`.

### 👀 Demo guiada

```py
puntaje = 72
estado = "APTO" if puntaje >= 60 else "NO APTO"
print(estado)
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Envío gratis**: `total >= 50` → `"Envío gratis"`; si no, `"Envío 3.99€"`, con ternario.

---

## SECCIÓN 6 · `match / case` (Python ≥ 3.10)

### 🎯 Objetivos

* Usar **coincidencia de patrones** para mejorar legibilidad en decisiones múltiples.

### 🧠 Teoría en claro

```py
match valor:
    case 1:
        ...
    case 2 | 3:
        ...
    case _:
        ...  # comodín (default)
```

### 👀 Demo guiada · Días laborales/festivos

```py
dia = "sabado"
match dia.lower():
    case "lunes" | "martes" | "miercoles" | "jueves" | "viernes":
        print("Día laborable")
    case "sabado" | "domingo":
        print("Fin de semana 🎉")
    case _:
        print("Valor desconocido")
```

### 🛠️ ZONA DEL ALUMNO · TODO

* **Menú simple**: con `opcion` (1–3), usa `match` para imprimir:

  * 1 → “Altas”
  * 2 → “Bajas”
  * 3 → “Consultas”
  * otro → “Opción no válida”

---

## SECCIÓN 7 · Laboratorio IA (condicionales creativos)

### 🎯 Objetivos

* Aprender a **pedir** a la IA miniprogramas que **usen condicionales** con claridad didáctica.
* Integrar el código y **mejorarlo** (validaciones, mensajes, resumen final).

### 🧰 Prompt Kit (copia/pega y ejecuta lo que te dé la IA)

1. **Generación**

   > “Eres profesor de Python. Genera un programa **de 35–45 líneas** que use `if/elif/else`, `and/or/not`, **ternario** y (si es posible) **match/case**. Tema: **‘sistema de entradas para concierto’** con validaciones (edad, stock, tipo de entrada). Nombres de variables en español, comentarios claros. Devuelve **SOLO código Python**.”

2. **Mejora**

   > “Ahora añade **3 casos de prueba** en comentarios (entrada/salida esperada), un **resumen final** con f-string, y **mensajes de error específicos**. Manténlo < 60 líneas.”

3. **Extensión**

   > “Incluye un bloque de **valores por defecto** si no hay entrada del usuario (modo demo), y separa la lógica en **2 funciones** pequeñas.”

### 🛠️ ZONA DEL ALUMNO · TODO

* Pide a la IA con el Prompt Kit, **pega** el código que te entregue y **ejecútalo**.
* Añade **tus propios casos límite** (edad = 0, stock = 0, etc.).
* Escribe un **análisis** de 3–5 líneas: ¿qué mejoraste y por qué?

---

## SECCIÓN 8 · Autoevaluación final (mini-proyecto)

### 🎯 Objetivos

* Integrar condicionales, lógicos, truthy/falsy, ternario y `match`.

### 🛠️ Tareas

1. **Entrada/valores**: Define o pide `nombre (str)`, `edad (int)`, `importe (float)`, `tipo_cliente (str)` en `{"normal","premium"}`.
2. **Validación**: si `not nombre` → “Nombre requerido”. Si `edad < 0` → “Edad inválida”.
3. **Reglas**:

   * Si `edad < 18` → **no puede comprar**.
   * Si `tipo_cliente == "premium"` **y** `importe >= 50` → **20%** de descuento.
   * Si `tipo_cliente == "normal"` **y** `importe >= 100` → **10%** de descuento.
   * En otro caso → **0%**.
4. **Ternario**: crea `estado_envio = "Envío gratis"` si total ≥ 60, si no `"Envío 3.99€"`.
5. **match/case**: según `tipo_cliente` imprime un **mensaje de bienvenida** (“👑 Premium” / “😊 Normal” / “Tipo desconocido”).
6. **Resumen final** (una línea):
   `"[OK] <nombre> | edad:<edad> | tipo:<tipo_cliente> | base:<importe:.2f> | desc:<aplicado%> | total:<total:.2f> | <estado_envio>"`

### 📏 Rúbrica rápida

* **Correcto**: controla entradas, aplica descuentos bien, usa ternario y `match`.
* **Excelente**: mensajes de error claros, casos límite probados, código legible.

---

## APÉNDICE A · Patrones útiles

* **Guard clauses** (salidas tempranas):

  ```py
  def puede_acceder(edad, tiene_entrada):
      if edad < 18:
          return False, "Menor de edad"
      if not tiene_entrada:
          return False, "Sin entrada"
      return True, "Adelante"
  ```
* **Normalización** de texto: `valor_normalizado = valor.strip().lower()`.
* **Rangos ordenados** (de mayor a menor) evitan solapamientos en clasificadores.

---

## APÉNDICE B · Estilo y buenas prácticas

* Nombres **descriptivos**: `total_con_descuento`, `es_estudiante`.
* Indentación **4 espacios**, evita mezclar tabs.
* Comentarios tipo **Better Comments**:

  * `# !` importante, `# *` definición, `# ?` idea, `# TODO:` tarea.
* Mensajes de error **amables y específicos**.

---

## APÉNDICE C · Errores comunes y cómo evitarlos

* **Olvidar `else`** necesario → añade rama por defecto si esperas todos los casos.
* **Comparar cadenas con mayúsculas/minúsculas** → usa `.lower()` para comparar.
* **Truthy/Falsy inesperado** (ej. `if []:`) → repasa la lista de falsy.
* **División por cero** en ramas “no esperadas” → valida antes de operar.
* **Lógica duplicada** en varias ramas → extrae a una función.

---

## APÉNDICE D · Retos extra (sube el nivel)

1. **Clasificador por niveles** (5–6 categorías) con `match` y rangos.
2. **Sistema de login**: 3 intentos, mensajes específicos; bloquea después con `not`.
3. **Carrito inteligente**: aplica cupones (`"ENVIO"`, `"-10%"`) con `match`.
4. **Simulador de becas**: decide concesión en base a renta, nota media y distancia al centro (`and`/`or`).

---

## ✅ Qué has aprendido

* Estructuras `if`, `elif`, `else`.
* Operadores lógicos `and`, `or`, `not` y **if** anidados.
* Concepto **Truthy/Falsy** y uso de `bool()`.
* **Ternario** para decisiones compactas.
* `match/case` para decisiones claras (Python ≥ 3.10).
* Diseñar, probar y **explicar** decisiones con casos límite.

---
