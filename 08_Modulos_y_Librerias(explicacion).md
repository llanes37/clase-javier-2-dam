# 🐍 Clase 8 de Python — Módulos y Librerías (import, alias, estándar útil, archivos, JSON, tu módulo, pip) + IA

**Autor:** Joaquín Rodríguez — *Guía didáctica con enfoque práctico*
**Objetivo global:** Dominar el uso de **módulos** y **librerías** en Python: `import`, alias y `from ... import ...`, exploración con `dir()` y `__name__`, módulos estándar clave (`math`, `random`, `datetime`, `pathlib`, `json`), lectura/escritura de archivos, **serialización JSON**, **crear tu propio módulo**, e introducción a **librerías externas (pip)**. Cierre con **Laboratorio IA** y **Autoevaluación**.

---

## 🧭 Cómo usar este material

1. Ejecuta `08_modulos y librerias.py` y usa el **menú** (opciones **1–9**).
2. En cada sección: lee la **teoría**, ejecuta la **demo**, completa la **ZONA DEL ALUMNO (TODO)**.
3. Finaliza con la **Autoevaluación** para integrar todo.

> 💡 **Tip docente:** recalca la diferencia entre **importar** (reutilizar) y **programar desde cero**. Enseña a **no duplicar** funciones ya existentes en el estándar.

---

## 🧩 Mapa del temario (menú del programa)

1. `import`, alias (`as`) y `from ... import ...`
2. `math` y `random` (números y aleatoriedad)
3. `datetime` (fechas y horas)
4. `pathlib` + archivos de texto (leer/escribir)
5. `json` (serializar/deserializar)
6. Tu propio módulo (auto‑creado si no existe)
7. Librerías externas (pip) \[opcional]
8. Laboratorio IA (módulos creativos)
9. Autoevaluación final
10. Ejecutar TODO (1→9)

---

## SECCIÓN 1 · `import`, alias y `from ... import ...`

### 🎯 Objetivos

* Conocer formas de importación y cuándo usarlas.
* Identificar el nombre del módulo actual con `__name__`.
* Explorar contenido con `dir()`.

### 🧠 Teoría en claro

```py
import modulo              # usar: modulo.func()
import modulo as m         # alias: m.func()
from modulo import nombre  # usar directo: nombre()
from modulo import a, b    # importar símbolos concretos

# introspección
import math
print(__name__)     # "__main__" si es el script principal
print(dir(math))    # lista de símbolos públicos/privados del módulo
```

> **Regla práctica:** evita `from modulo import *` en proyectos reales (contamina el espacio de nombres y dificulta leer el origen de los símbolos).

### 👀 Demo guiada

* Mostrar `math.pi`, `sqrt(16)`, `__name__`, y un recorte de `dir(math)`.

### 🛠️ ZONA DEL ALUMNO · TODO

* **Área de círculo**: pide/captura `radio` (float, por defecto 3.0) y calcula `área = math.pi * r**2`. Muestra con 2 decimales.

---

## SECCIÓN 2 · `math` y `random` (utilidades numéricas y aleatorias)

### 🎯 Objetivos

* Utilizar funciones clave de `math`.
* Generar aleatorios reproducibles con `random`.

### 🧠 Teoría en claro

* `math`: `ceil`, `floor`, `sqrt`, `pow`, `factorial`, `pi`, `e`…
* `random`: `random()`, `randint(a,b)`, `choice(seq)`, `shuffle(lista)`, `sample(seq, k)`.

> **Tip:** para resultados reproducibles, usa `random.seed(42)` (u otra semilla) al comenzar.

### 👀 Demo guiada

* Mezclar una lista 1..10, generar un entero 1..100 y tomar una muestra de 3.

### 🛠️ ZONA DEL ALUMNO · TODO

* **Lote aleatorio**: genera 5 enteros 1..50 y muestra lista, **mínimo**, **máximo** y **media** (`sum/len`).

---

## SECCIÓN 3 · `datetime` (fechas y horas)

### 🎯 Objetivos

* Obtener tiempo actual y diferencias de tiempo.
* Formatear y parsear fechas de/desde texto.

### 🧠 Teoría en claro

* `datetime.now()`, `date.today()`, `timedelta(días, horas, ...)`
* Formateo con `strftime("%Y-%m-%d %H:%M:%S")`
* Parseo con `datetime.strptime(cadena, "%Y-%m-%d")`

> **Tip:** `datetime` ingenuas (naive) no llevan zona horaria; para apps serias, considera `zoneinfo` (Py≥3.9) o librerías como `pytz`.

### 👀 Demo guiada

* Imprimir "ahora" formateado, días hasta fin de año, parsear fecha objetivo `YYYY-MM-DD` y calcular días restantes.

### 🛠️ ZONA DEL ALUMNO · TODO

* **Recordatorio**: pide fecha (`YYYY-MM-DD`) y horas (`int`), súmalas con `timedelta(hours=...)` y muestra la fecha/hora final formateada.

---

## SECCIÓN 4 · `pathlib` + archivos de texto (leer/escribir)

### 🎯 Objetivos

* Trabajar con rutas de forma **multiplaforma**.
* Leer y escribir archivos de texto con codificación correcta.

### 🧠 Teoría en claro

* `Path.cwd()`, `Path("ruta")`, `.exists()`, `.write_text()`, `.read_text()`, `.stat()`
* Escritura de varias líneas: `"\n".join(lista)`
* **Codificación**: usa `encoding="utf-8"` para evitar problemas con acentos.

### 👀 Demo guiada

* Crear `demo_modulos.txt`, escribir 3 líneas, leerlas y mostrar tamaño en bytes.

### 🛠️ ZONA DEL ALUMNO · TODO

* **Tareas a archivo**: crea 3 tareas y escríbelas en `tareas.txt` (una por línea).
* Léelas y muéstralas **numeradas** (con `enumerate(start=1)`).

---

## SECCIÓN 5 · `json` (serializar y deserializar)

### 🎯 Objetivos

* Guardar estructuras Python en formato JSON y volver a cargarlas.
* Presentar JSON legible con `indent` y acentos con `ensure_ascii=False`.

### 🧠 Teoría en claro

* `json.dumps(obj, indent=2, ensure_ascii=False)` → **cadena**
* `json.loads(cadena)` → **obj Python**
* `json.dump(obj, archivo)` / `json.load(archivo)` con manejadores de archivo

> **Nota:** `datetime` **no** es serializable por defecto en JSON; convierte a cadena (`.strftime`) o a `timestamp`.

### 👀 Demo guiada

* Escribir `perfil.json` y volver a cargarlo; imprimir el dict resultante.

### 🛠️ ZONA DEL ALUMNO · TODO

* **Productos JSON**: crea lista de dicts `{nombre, precio}`, guárdala en `productos.json`, vuelve a leerla y muestra el **total** de precios.

---

## SECCIÓN 6 · Tu propio módulo (auto‑creado si no existe)

### 🎯 Objetivos

* Entender que un **módulo** es simplemente un **archivo `.py`** con funciones/clases.
* Crear un módulo, importarlo y reutilizar sus utilidades.

### 👀 Demo guiada

* Crear `utilidades_demo.py` con constantes (p. ej. `PI`) y funciones (`suma`, `es_par`, `area_circulo`).
* Importarlo como `import utilidades_demo as util` y usar sus funciones.

### 🛠️ ZONA DEL ALUMNO · TODO

* **Extender módulo**: añade en `utilidades_demo.py` la función `doble(n) → n*2`.
* Recarga con `import importlib, utilidades_demo; importlib.reload(utilidades_demo)` y pruébala.

> **Pitfall clásico:** **¡No** llames a tu script `random.py`, `json.py`, `math.py`, etc.! Sombrearás (shadowing) a los módulos estándar y los imports fallarán.

---

## SECCIÓN 7 · Librerías externas (pip) \[opcional]

### 🎯 Objetivos

* Conocer el flujo: **instalar → importar → usar**.
* Entender que la demo debe ser **segura** si el paquete no está disponible.

### 🧠 Teoría en claro

* Instalar (terminal): `pip install paquete`
* Importar: `import paquete` · `import paquete as alias` · `from paquete import nombre`

> **Ejemplos populares:** `requests` (HTTP), `pandas` (datos), `numpy` (numérico), `matplotlib` (gráficas).

### 👀 Demo guiada

* Comprobar si `requests` está instalado y mostrar su versión. (Si no, sugerir instalación).

### 🛠️ ZONA DEL ALUMNO · TODO

* **GET con externa**: si tienes `requests`, haz `GET` a `https://httpbin.org/get` y muestra `origin` y `headers`. Protege con `try/except` por si no hay conexión o paquete.

---

## SECCIÓN 8 · Laboratorio IA (módulos creativos)

### 🎯 Objetivos

* Practicar un flujo real integrando **datetime + pathlib + json + random**.
* Aprender a **separar responsabilidades** en funciones (leer/escribir/serializar).

### 🧰 Prompt Kit (copia/pega)

1. **Generación**

   > “Eres profesor de Python. Genera un programa de **35–50 líneas** que use:
   > • `datetime` para sellos de tiempo
   > • `pathlib` para guardar en `.txt` o `.json`
   > • `json` para serializar un pequeño historial
   > • `random` para simular datos
   > Tema: **registro de hábitos** o **simulador de ventas**. Devuelve **solo código Python**.”
2. **Alternativo**

   > “Crea una herramienta **agenda de tareas** que guarde/cargue un JSON con fechas (usa `strftime`). Incluye **dos funciones utilitarias** en un módulo aparte.”
3. **Mejora**

   > “Refactoriza separando lectura/escritura en funciones y añade **validaciones y mensajes de error** claros. Manténlo **< 50 líneas**.”

### 👀 Demo opcional (IA\_DEMO=True)

* Crear `demo_registro.json` con una entrada de ejemplo (hora + valor) usando `datetime.now()` + `json` + `Path.write_text()`.

### 🛠️ ZONA DEL ALUMNO · TODO

* Pide a la IA el miniprograma con el Prompt Kit, pégalo en tu zona de práctica y ejecútalo.
* Añade validaciones, manejo de errores y un **resumen final** en una línea.

---

## AUTOEVALUACIÓN FINAL · Registro simple con JSON + fechas

### 🎯 Objetivos

* Integrar **imports**, **archivos**, **JSON**, **fechas** y **agrupaciones** en un flujo único.

### 🛠️ Enunciado

Implementa un **registro de gastos**:

1. Pide/captura apuntes con: `concepto (str)` e `importe (float)`. Fecha opcional → si no se indica, usa `datetime.now()` formateado.
2. Guarda los datos en `gastos.json` usando `json` + `pathlib`. Si el archivo existe, **cárgalo y añade** (append seguro).
3. Al leer, muestra:

   * número de **movimientos**,
   * **total** gastado,
   * **gasto medio**,
   * **mayor gasto** (concepto/importe).
4. Línea final estilo dashboard:
   `"Movs:<n> | Total:<€> | Medio:<€> | Mayor:<concepto-€>"`

### 📏 Rúbrica

* **Correcto**: persiste JSON, resumen correcto, manejo simple de errores.
* **Excelente**: mensajes claros, validaciones de entrada, código organizado por funciones.

---

## APÉNDICE A · Patrones útiles

* **Lectura/escritura segura con Path**:

```py
from pathlib import Path
p = Path("datos.json")
if p.exists():
    datos = json.loads(p.read_text(encoding="utf-8"))
else:
    datos = []
p.write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")
```

* **Serializar fechas**:

```py
from datetime import datetime
fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

* **Recarga de módulo** (después de editar su código):

```py
import importlib, utilidades_demo
importlib.reload(utilidades_demo)
```

---

## APÉNDICE B · Buenas prácticas

* No sombreees módulos estándar nombrando tu archivo como ellos (`json.py`, `random.py`, ...).
* Coloca imports **arriba del archivo**; excepciones: imports dentro de funciones para evitar dependencias pesadas al iniciar.
* Usa `encoding="utf-8"` siempre que escribas/lea textos.
* Mantén las responsabilidades separadas: **leer**, **procesar**, **escribir**.

---

## APÉNDICE C · Retos extra

1. **Exportador CSV**: a partir de un JSON con ventas, genera un `.csv` (separa por `;`).
2. **Historial rotativo**: guarda registros con fecha y limita a los **últimos N** (p. ej., 100) elementos.
3. **Módulo `utils_texto.py`**: crea funciones `slugify`, `limpiar_espacios`, `resumen(texto, n)` y pruébalas.
4. **Seed controlado**: simula ventas con `random.seed()` para reproducibilidad y genera informes.

---

## ✅ Qué has aprendido

* Diferentes formas de `import` y cuándo usarlas.
* Uso de módulos estándar: `math`, `random`, `datetime`, `pathlib`, `json`.
* Lectura/escritura de archivos de texto y JSON con `Path`.
* Creación y recarga de **tu propio módulo**.
* Primeros pasos con **librerías externas (pip)**.
* Integración práctica con **Laboratorio IA** y **Autoevaluación**.

---
