
# 🌐 Flask: Guía Completa para Empezar desde Cero

**Versión didáctica — Acorde con 02_condicionales.py**

Autor: Joaquín | Web: https://clasesonlinejoaquin.es/

---

## 📘 ¿Qué es Flask?

Flask es un **framework de desarrollo web minimalista y ligero** para Python. Es ideal tanto para principiantes que quieren aprender a crear aplicaciones web simples como para desarrolladores avanzados que necesitan un control completo y flexibilidad.

### ✨ Características principales

- **Ligero y modular**: Código reducido, máxima flexibilidad
- **Extensible**: Ecosistema de extensiones para BD, autenticación, etc.
- **Compatible con WSGI**: Integración eficiente con servidores web
- **Perfecto para aprender**: Ideal para entender HTTP, rutas, formularios, APIs JSON
- **Escalable**: Desde prototipos rápidos hasta aplicaciones complejas

### 🎯 Casos de uso

✅ Aplicaciones web tradicionales (HTML + CSS + JS)  
✅ APIs REST (endpoints que devuelven JSON)  
✅ Microservicios  
✅ Prototipado rápido  
✅ Aplicaciones de una página (SPA backend)  

---

## 🚀 Instalación rápida

### Paso 1: Crear entorno virtual

```bash
python -m venv env
```

### Paso 2: Activar (Windows)

```bash
.\env\Scripts\activate
```

### Paso 3: Instalar Flask

```bash
pip install flask
```

### Paso 4: Verificar instalación

```bash
python -c "import flask; print(flask.__version__)"
```

---

## 💡 Conceptos clave de Flask

### 1️⃣ La aplicación Flask

```python
from flask import Flask

app = Flask(__name__)  # Crea la aplicación

if __name__ == "__main__":
    app.run(debug=True)  # Inicia el servidor
```

**? ¿Qué hace `__name__`?**
- Flask lo usa para encontrar recursos (plantillas, archivos estáticos)
- Recomendado dejarlo así

**? ¿Qué es `debug=True`?**
- Recarga automática al guardar cambios
- Página de errores interactiva
- ⚠️ Nunca uses en producción

---

### 2️⃣ Rutas (URLs y funciones)

Una **ruta** mapea una URL a una función Python:

```python
@app.route("/")
def inicio():
    return "Página principal"

@app.route("/about")
def about():
    return "Página de información"
```

| URL | Función | Respuesta |
|-----|---------|-----------|
| `http://localhost:5000/` | `inicio()` | "Página principal" |
| `http://localhost:5000/about` | `about()` | "Página de información" |

**! IMPORTANTE**: La indentación y el decorador `@app.route()` son críticos.

---

### 3️⃣ Parámetros en la URL

Puedes capturar valores dinámicos de la URL:

```python
# Parámetro string
@app.route("/saluda/<nombre>")
def saluda(nombre):
    return f"Hola, {nombre}!"
# http://localhost:5000/saluda/Juan → "Hola, Juan!"

# Parámetro tipado (int)
@app.route("/suma/<int:a>/<int:b>")
def suma(a, b):
    return f"{a} + {b} = {a + b}"
# http://localhost:5000/suma/10/20 → "10 + 20 = 30"
```

**Tipos soportados:**
- `<string:var>` → texto (por defecto)
- `<int:var>` → número entero
- `<float:var>` → número decimal
- `<path:var>` → texto con barras (/)
- `<uuid:var>` → identificador único

---

### 4️⃣ Métodos HTTP (GET, POST, PUT, DELETE)

Flask soporta diferentes métodos HTTP:

```python
# GET: solicita datos (por defecto)
@app.route("/datos")
def obtener_datos():
    return "Datos aquí"

# POST: envía datos
@app.route("/crear", methods=["POST"])
def crear():
    return "Datos recibidos"

# GET + POST
@app.route("/formulario", methods=["GET", "POST"])
def formulario():
    return "GET o POST"
```

**? ¿Cuándo usar cada uno?**
- **GET**: Solicitar información (sin efectos secundarios)
- **POST**: Enviar datos (crear/modificar)
- **PUT**: Actualizar completamente
- **DELETE**: Eliminar

---

### 5️⃣ Formularios HTML (POST)

Para enviar datos desde HTML a Flask:

```html
<!-- formulario.html -->
<form action="/procesar" method="post">
    <input type="text" name="nombre" placeholder="Tu nombre">
    <button type="submit">Enviar</button>
</form>
```

```python
# app.py
from flask import request

@app.route("/procesar", methods=["POST"])
def procesar():
    nombre = request.form.get("nombre", "")  # Captura del formulario
    return f"Hola, {nombre}!"
```

**! IMPORTANTE**: 
- Formulario: `method="post"`
- Python: `request.form.get()`

---

### 6️⃣ Plantillas Jinja2

```python
from flask import render_template

@app.route("/")
def inicio():
    nombre = "Ada"
    return render_template("index.html", nombre=nombre)
```

```html
<!-- templates/index.html -->
<h1>Hola, {{ nombre }}!</h1>
{% if nombre == "Ada" %}
    <p>¡La inventora del primer algoritmo!</p>
{% endif %}
```

**Sintaxis Jinja2:**
- `{{ variable }}` → imprime variable
- `{% if ... %}...{% endif %}` → condicionales
- `{% for x in lista %}...{% endfor %}` → bucles
- `{% extends "base.html" %}` → herencia

---

### 7️⃣ Query Strings (parámetros GET)

Parámetros después del `?` en la URL:

```python
@app.route("/buscar")
def buscar():
    q = request.args.get("q", "")  # Parámetro 'q'
    page = request.args.get("page", 1)  # Parámetro 'page'
    return f"Buscando: {q}, página: {page}"
```

Uso:
```
http://localhost:5000/buscar?q=flask&page=2
```

**? ¿GET vs POST?**
- **GET** (query strings): visible en URL, datos pequeños
- **POST** (formularios): seguro, datos grandes

---

### 8️⃣ API JSON (GET/POST)

Devolver JSON en lugar de HTML:

```python
from flask import jsonify

# GET: devuelve JSON
@app.route("/api/users")
def obtener_usuarios():
    usuarios = [
        {"id": 1, "nombre": "Ada"},
        {"id": 2, "nombre": "Bob"},
    ]
    return jsonify(usuarios=usuarios)

# POST: recibe JSON
@app.route("/api/crear", methods=["POST"])
def crear_usuario():
    data = request.get_json()  # Recibe JSON del cliente
    nombre = data.get("nombre")
    return jsonify(ok=True, mensaje=f"Usuario {nombre} creado"), 201
```

**JavaScript (cliente):**
```javascript
// GET
fetch('/api/users')
  .then(r => r.json())
  .then(d => console.log(d))

// POST
fetch('/api/crear', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({nombre: 'Ada'})
})
  .then(r => r.json())
  .then(d => console.log(d))
```

---

### 9️⃣ Manejo de errores

```python
# Error 404 (no encontrado)
@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Ruta no encontrada"), 404

# Error 500 (error interno)
@app.errorhandler(500)
def server_error(e):
    return jsonify(error="Error del servidor"), 500

# Provocar error
@app.route("/error")
def error():
    raise RuntimeError("Error intencional")
```

**Códigos HTTP comunes:**
- 200 OK ✅
- 201 Created ✅
- 400 Bad Request ❌
- 404 Not Found ❌
- 500 Internal Error ❌

---

### 🔟 Hooks (before/after request)

Funciones que se ejecutan antes/después de cada petición:

```python
@app.before_request
def antes():
    """Se ejecuta ANTES de procesar la petición"""
    print(f"Petición a: {request.path}")

@app.after_request
def despues(response):
    """Se ejecuta DESPUÉS de procesar la petición"""
    response.headers["X-Custom"] = "Mi Header"
    return response
```

**Casos de uso:**
- Validar autenticación
- Medir tiempo de respuesta
- Iniciar conexión a BD
- Añadir cabeceras CORS

---

## 📂 Estructura de proyecto recomendada

```
mi_proyecto/
├── app.py                 # Archivo principal
├── requirements.txt       # Dependencias
├── env/                   # Entorno virtual
├── templates/             # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   └── formulario.html
├── static/                # CSS, JS, imágenes
│   ├── css/
│   ├── js/
│   └── images/
└── README.md             # Documentación
```

---

## 🔗 Comparación con condicionales.py

| Aspecto | 02_condicionales.py | 14_flask_tutorial.py |
|--------|-------------------|----------------------|
| Estructura | Menú interactivo | Aplicación web |
| Entrada | input() terminal | Navegador HTTP |
| Salida | print() terminal | HTML + JSON |
| Comentarios | Better Comments | Better Comments ✅ |
| Prácticas | TODOs integrados | TODOs + archivo separado |
| IA | Prompts KIT ChatGPT | Prompts KIT ChatGPT ✅ |
| Didáctico | Muy comentado | Muy comentado ✅ |

**Diferencia clave:**
- Condicionales: lógica pura (CLI)
- Flask: aplicación web (frontend + backend)

---

## 🎓 Tu primer servidor web (5 minutos)

### 1️⃣ Crear archivo `app_rapida.py`

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return """
    <h1>Bienvenido a mi primer servidor web 🚀</h1>
    <ul>
        <li><a href="/saluda/Juan">Saluda a Juan</a></li>
        <li><a href="/suma/5/3">Suma: 5 + 3</a></li>
    </ul>
    """

@app.route("/saluda/<nombre>")
def saluda(nombre):
    return f"<h2>Hola, {nombre}! 👋</h2><a href='/'>Volver</a>"

@app.route("/suma/<int:a>/<int:b>")
def suma(a, b):
    resultado = a + b
    return f"<h2>{a} + {b} = {resultado}</h2><a href='/'>Volver</a>"

if __name__ == "__main__":
    app.run(debug=True)
```

### 2️⃣ Ejecutar

```bash
python app_rapida.py
```

### 3️⃣ Abrir navegador

```
http://127.0.0.1:5000/
```

**✅ ¡Listo! Tu primer servidor web funcionando.**

---

## 📚 Recursos de aprendizaje

### Oficial
- 📖 [Documentación Flask](https://flask.palletsprojects.com/)
- 📖 [Jinja2 Templates](https://jinja.palletsprojects.com/)

### HTTP y Web
- 📖 [HTTP Status Codes](https://httpwg.org/specs/rfc9110.html#status.codes)
- 📖 [JSON.org](https://www.json.org/)
- 📖 [REST API Best Practices](https://restfulapi.net/)

### Extensiones populares
- **Flask-SQLAlchemy**: ORM para bases de datos
- **Flask-Login**: Autenticación de usuarios
- **Flask-CORS**: Compartir recursos entre dominios
- **Flask-WTF**: Manejo de formularios seguro

---

## ❓ Preguntas frecuentes

### P: ¿Cuál es la diferencia entre Flask y Django?
**R**: 
- **Flask**: minimalista, perfecto para aprender, APIs
- **Django**: "todo incluido", para proyectos grandes

### P: ¿Flask es seguro para producción?
**R**: Sí, con configuración adecuada:
- Gunicorn/uWSGI (servidor WSGI)
- Nginx/Apache (proxy inverso)
- SSL/HTTPS
- Validación de entrada

### P: ¿Los datos persisten entre reinicios?
**R**: No. Están en RAM. Necesitas BD para persistencia.

### P: ¿Cómo despliego en la nube?
**R**: Opciones populares:
- Heroku (simple)
- PythonAnywhere (Python-friendly)
- Render (moderno)
- AWS/Azure (complejo pero potente)

---

## 🎯 Próximos pasos

1. **Ejecuta** el `14_flask_tutorial.py` completo
2. **Lee** los comentarios del código
3. **Practica** con `PRACTICAS_FLASK.md`
4. **Experimenta** modificando rutas y plantillas
5. **Avanza** a base de datos, autenticación, despliegue

---

## 📝 Resumen

Flask es un framework web potente pero sencillo. Te permite:
- ✅ Crear rutas (URLs)
- ✅ Recibir parámetros (URL, formularios, JSON)
- ✅ Devolver respuestas (HTML, JSON)
- ✅ Manejar errores
- ✅ Crear APIs REST

**Recuerda:** Empieza simple, aprende los conceptos, luego escala.

---

**¡Ahora tienes todo para crear tu primera aplicación web! 🌐**

Autor: Joaquín | https://clasesonlinejoaquin.es/

