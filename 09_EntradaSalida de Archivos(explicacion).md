# 🐍 Clase 9 de Python — Entrada/Salida de Archivos (E/S)

**Autor:** Joaquín Rodríguez — *Guía didáctica práctica y robusta*
**Objetivo global:** Dominar la **lectura y escritura** de archivos en Python: `open()` + `with`, modos de apertura (`r/w/a` y binarios `rb/wb`), lectura por líneas, **append** y **logs**, **`pathlib`** para rutas, **CSV** y **JSON**, **copias por bloques** para binarios, manejo de **errores comunes** y un **Laboratorio IA** + **Autoevaluación** integradora.

> 🎨 **Convención de comentarios** (Better Comments):
> `# !` importante · `# *` definición/foco · `# ?` idea/nota · `# TODO:` práctica · `# NOTE:` apunte · `# //` deprecado

---

## 🧭 Cómo usar este material

1. Ejecuta `09_EntradaSalida de Archivos.py` para abrir el **menú** (0–11).
2. En cada sección: **lee la teoría**, prueba la **demo**, completa la **ZONA DEL ALUMNO (TODO)**.
3. Activa `RUN_INTERACTIVE=True` para pedir datos reales; usa `False` para demos automáticas.
4. Usa `PAUSE=True` si presentas en vivo; avanza sección a sección.
5. El **Laboratorio IA** propone prompts listos para copiar/pegar y montar un mini‑proyecto.

---

## 🧩 Mapa del temario (menú del programa)

1. `open()` y `with` · modos de texto
2. Lectura de texto: `read` / `readline` / `readlines` / iteración
3. Escritura y **append** · mini‑logs con timestamp
4. `pathlib` para rutas (`exists`, `mkdir`, `glob`, `rename`, `unlink`)
5. **CSV** con `csv.reader` / `csv.writer`
6. **JSON** con `json.load` / `json.dump`
7. **Binarios** (copias por bloques `rb/wb`)
8. **Errores comunes** de E/S y manejo con excepciones
9. **Laboratorio IA** (persistencia sencilla)
10. **Autoevaluación final**
11. **Ejecutar TODO** (1→10)

---

## Utilidades del script (ya incluidas)

* `safe_input(prompt, caster, default)` → Entrada segura con **fallback** y casting.
* `encabezado(titulo)` → Títulos bonitos entre separadores.
* `pause()` → Pausa si `PAUSE=True`.
* `print_firma()` → Firma del curso al inicio del menú.

---

## SECCIÓN 1 · `open()` y `with` · modos básicos de texto

### 🎯 Objetivos

* Abrir/crear archivos de texto en **UTF‑8** y cerrarlos **automáticamente** con `with` (context manager).
* Diferenciar `w` (sobrescribe), `a` (añade), `r` (lee).

### 🧠 Teoría en claro

```py
# Esqueleto típico
a = open("ruta.txt", "w", encoding="utf-8")
a.write("línea\n"); a.close()  # ❌ no recomendado si olvidas cerrar

with open("ruta.txt", "w", encoding="utf-8") as f:  # ✅ recomendado
    f.write("Primera línea\n")
```

### 👀 Demo guiada

* Crea `demo_io.txt`, escribe dos líneas y léelo completo (texto en consola).

### 🛠️ ZONA DEL ALUMNO · TODO — **Nota rápida**

* Pide/captura una frase (por defecto: *"Hola archivo"*), guárdala en `nota.txt` y vuelve a leerla mostrando el contenido.

> 💡 **Tips**: 1) Siempre `encoding="utf-8"` para acentos/emoji. 2) Añade `"\n"` al final si quieres líneas separadas.

---

## SECCIÓN 2 · Lecturas de texto: `read` / `readline` / `readlines` / iteración

### 🎯 Objetivos

* Elegir la estrategia de lectura según el tamaño del archivo.
* Numerar y limpiar líneas con `.splitlines()` / `.strip()`.

### 🧠 Teoría en claro

* `f.read()` → lee **todo** (ojo con archivos grandes).
* `f.readline()` → lee **una** línea (con `\n` si existe).
* `f.readlines()` → devuelve **lista** de líneas.
* `for linea in f:` → **streaming** línea a línea (memoria eficiente).

### 👀 Demo guiada

* Genera `poema.txt` y muestra ejemplos con las tres funciones y con iteración numerada.

### 🛠️ ZONA DEL ALUMNO · TODO — **Contador de líneas y palabras**

* Lee `poema.txt` y muestra: **nº líneas** y **nº total de palabras**.

> 💡 **Tip**: `sum(len(l.split()) for l in lineas)` para contar palabras separadas por espacios.

---

## SECCIÓN 3 · Escritura y **append** · mini‑logs con timestamp

### 🎯 Objetivos

* Diferenciar **sobrescritura** (`w`) vs **añadir** (`a`).
* Registrar eventos en **log.txt** con **ISO 8601**.

### 🧠 Teoría en claro

* `"w"` crea o **borra** el contenido previo.
* `"a"` **conserva** y añade al final.
* **Timestamps**: `datetime.now().isoformat(timespec='seconds')`.

### 👀 Demo guiada

* Escribe `Inicio del log` y añade dos eventos fechados (A/B).

### 🛠️ ZONA DEL ALUMNO · TODO — **Apéndice de eventos**

* Pide/captura un evento (por defecto: *"Login OK"*) y añádelo a `log.txt` con timestamp ISO.

---

## SECCIÓN 4 · `pathlib` para rutas · `exists/mkdir/glob/rename/unlink`

### 🎯 Objetivos

* Trabajar con rutas **multiplataforma** (`Path`) y utilidades de carpetas/archivos.
* Listar por patrón, renombrar y borrar.

### 🧠 Teoría en claro

```py
from pathlib import Path
p = Path("carpeta")
p.mkdir(exist_ok=True)
[p.name for p in p.glob("*.txt")]    # listar TXT
(p/"f1.txt").rename(p/"f1_renombrado.txt")
(p/"f2.txt").unlink()                 # borrar
```

### 👀 Demo guiada

* Crea `data_io/` con `f1.txt..f3.txt`, renombra `f1.txt` → `f1_renombrado.txt` y lista los `.txt`.

### 🛠️ ZONA DEL ALUMNO · TODO — **Limpieza selectiva**

* Crea `data_tmp/` con **3** `.log` y **2** `.txt`.
* Borra **solo** los `.log` y muestra lo que queda.

> 💡 **Tip**: usa `for p in carpeta.glob("*.log"): p.unlink()`.

---

## SECCIÓN 5 · **CSV** (leer y escribir)

### 🎯 Objetivos

* Escribir y leer CSV de forma **segura** (`newline=''`, UTF‑8).
* Usar cabecera y recorrer filas con `csv.reader`.

### 🧠 Teoría en claro

```py
import csv
with open("datos.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["nombre", "nota"])      # cabecera
    w.writerows([["Ana",8],["Luis",6]])

with open("datos.csv", "r", newline="", encoding="utf-8") as f:
    r = csv.reader(f)
    cab = next(r)
    for fila in r:
        ...
```

### 👀 Demo guiada

* Crea `alumnos.csv` (nombre, nota) y léelo mostrando cabecera + filas.

### 🛠️ ZONA DEL ALUMNO · TODO — **Aprobado/Suspenso**

* Lee `alumnos.csv` y crea `alumnos_out.csv` añadiendo columna `aprobado` (`nota >= 5`).

> 💡 **Extra**: prueba **`csv.DictReader/DictWriter`** para trabajar por nombre de columna.

---

## SECCIÓN 6 · **JSON** (serializar / deserializar)

### 🎯 Objetivos

* Serializar estructuras Python a JSON y volver a cargarlas.
* Hacer JSON **legible** con `indent` y mantener acentos con `ensure_ascii=False`.

### 🧠 Teoría en claro

```py
import json
s = json.dumps(obj, ensure_ascii=False, indent=2)   # → cadena
obj = json.loads(s)                                 # ← de cadena
# Archivos
dump/load con manejadores, o Path.read_text()/write_text() + dumps/loads
```

### 👀 Demo guiada

* Guarda `productos.json` con lista de dicts y vuélvelo a leer; imprime el dict cargado.

### 🛠️ ZONA DEL ALUMNO · TODO — **Tareas JSON**

* Crea lista de tareas `[{texto, hecha: bool}]`, guárdala en `tareas.json` y vuelve a leerla mostrando **hechas** vs **pendientes**.

> 💡 **Tip**: JSON **no** serializa `datetime` de serie; guarda fechas formateadas (`strftime`) o `timestamp`.

---

## SECCIÓN 7 · **Binarios** · leer/escribir y **copias por bloques**

### 🎯 Objetivos

* Copiar archivos binarios sin corromperlos (no tratarlos como texto).
* Leer/escribir en **chunks** (bloques) para no cargar todo en memoria.

### 🧠 Teoría en claro

```py
with open(src, "rb") as f, open(dst, "wb") as g:
    while (bloque := f.read(64)):
        g.write(bloque)
```

### 👀 Demo guiada

* Crea `demo.bin` (256 bytes) y copia a `demo_copia.bin`, mostrando el tamaño y los 16 primeros bytes en **hex**.

### 🛠️ ZONA DEL ALUMNO · TODO — **Espiar cabecera**

* Lee los **primeros 8 bytes** de `demo.bin` en **hex** y muestra el **tamaño total**.

> 💡 **Extra**: ajusta el tamaño de bloque (p. ej., 64 KiB) para archivos grandes.

---

## SECCIÓN 8 · Errores comunes de E/S y manejo con excepciones

### 🎯 Objetivos

* Manejar `FileNotFoundError`, `PermissionError`, `UnicodeDecodeError`, `json.JSONDecodeError`.
* Implementar **lecturas seguras** con valores por defecto.

### 🧠 Teoría en claro

Patrón típico:

```py
from pathlib import Path
import json
try:
    datos = json.loads(Path("config.json").read_text(encoding="utf-8"))
except FileNotFoundError:
    datos = {}; Path("config.json").write_text("{}", encoding="utf-8")
except json.JSONDecodeError as e:
    print("JSON inválido:", e); datos = {}
```

### 👀 Demo guiada

* Muestra lectura de archivo inexistente (se crea por defecto) y parseo de `malo.json` con captura de `JSONDecodeError`.

### 🛠️ ZONA DEL ALUMNO · TODO — **`load_json_safe`**

* Implementa `load_json_safe(ruta)` que devuelva `{}` ante errores y cree el archivo vacío si no existe.
* Pruébalo con `config.json`.

---

## SECCIÓN 9 · Laboratorio IA (persistencia sencilla)

### 🎯 Objetivos

* Generar con IA un **gestor de notas**/agenda usando `pathlib` y/o `json`.
* Separar responsabilidades: **leer**, **procesar**, **escribir**.

### 🧰 Prompt Kit (copia/pega)

1. **Generación**

   > “Eres profesor de Python. Genera un programa de **35–50 líneas** que implemente un **gestor de notas** con `pathlib`: crear/listar/leer/borrar notas `.txt` en carpeta `notas/`. Variables en español, comentarios con `# *` y `# TODO`, y manejo básico de `FileNotFoundError`. **Solo código Python**.”
2. **Alternativo**

   > “Crea una **agenda de tareas** persistente con **JSON**: añadir, listar, marcar hecha, guardar y cargar (append seguro si existe). **Solo código Python**.”
3. **Mejora**

   > “Refactoriza separando funciones de E/S (`leer_json`, `escribir_json`) y añade **protección** ante `UnicodeDecodeError`. Mantén el total **< 50 líneas**.”

### 👀 Demo opcional (IA\_DEMO=True)

* Crea carpeta `notas/` y un fichero `demo.txt` con contenido de prueba.

### 🛠️ ZONA DEL ALUMNO · TODO — **Pega y ejecuta tu mini‑programa**

* Solicita a la IA el miniproyecto con el Prompt Kit, **pégalo** debajo de la zona indicada en el script y ejecútalo desde el menú.

---

## AUTOEVALUACIÓN FINAL · Gestor de gastos (texto/JSON/CSV)

### 🎯 Objetivos

* Integrar **texto + JSON + CSV** con rutas y manejo de errores.

### 🛠️ Enunciado

1. Carpeta `datos/` con:

   * `gastos.txt` → `concepto;importe` por línea.
   * `gastos.json` → lista de dicts `{concepto, importe, fecha}`.
   * `gastos.csv` → columnas `concepto, importe, fecha`.
2. Flujo:

   * Añade **3 apuntes** (valores por defecto si `RUN_INTERACTIVE=False`).
   * Escribe **los tres formatos** (usa `utf-8` y `newline=''` en CSV).
   * Vuelve a **leer** y calcula: nº movimientos, **total**, **media** y **mayor gasto** (concepto/importe).
3. Manejo de errores: protege lecturas con `try/except` para `FileNotFoundError` y `JSONDecodeError`.
4. **Resumen final** tipo dashboard:
   `"Movs:<n> | Total:<€> | Medio:<€> | Mayor:<concepto-€>"`

### 📏 Rúbrica rápida

* **Correcto**: persiste y lee los tres formatos; métricas correctas.
* **Excelente**: validaciones, mensajes claros, funciones auxiliares limpias.

---

## Apéndice A · Trucos y patrones útiles

* **Lectura perezosa** (streaming) para archivos grandes:

  ```py
  with open("grande.txt", "r", encoding="utf-8") as f:
      for i, linea in enumerate(f, 1):
          if i % 100000 == 0: print(i)
  ```
* **Tamaños de bloque** recomendados (binario): 64 KiB–1 MiB según disco/red.
* **CSV** con separador `;` (países hispanos): `csv.writer(f, delimiter=';')`.
* **Fechas** legibles: `datetime.now().strftime("%Y-%m-%d %H:%M:%S")`.
* **`Path.glob('**/*.txt')`** para búsqueda recursiva.

---

## Apéndice B · Errores frecuentes (y cómo evitarlos)

* Olvidar `encoding` y ver caracteres raros → usa `utf-8` **siempre**.
* Sobrescribir por error con `w` → si dudas, usa `a` o comprueba existencia antes.
* Leer binarios en modo texto → **nunca** abras imágenes/PDFs con `"r"`.
* No cerrar archivos → usa `with` (se cierra solo incluso ante excepciones).
* CSV sin `newline=''` en Windows → líneas en blanco dobles; añade el parámetro.
* Manejar JSON roto sin try/except → captura `JSONDecodeError` y recupera.

---

## ✅ Qué has aprendido

* Abrir/leer/escribir archivos de texto y binario de forma segura.
* Usar `with` para **cierre automático** y evitar fugas.
* Operar con rutas mediante **`pathlib`**.
* Trabajar con **CSV** y **JSON** de manera robusta.
* Copiar binarios por **bloques** sin agotar memoria.
* Manejar **errores comunes** de E/S.
* Construir un mini‑proyecto de **persistencia** integrando varias técnicas.

---
