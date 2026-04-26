# 🎮 Steam Store Clone - Tienda de Videojuegos

## 📘 Descripción

Proyecto didáctico que implementa una tienda de videojuegos inspirada en [Steam](https://store.steampowered.com/), desarrollado con **Flask** y **Bootstrap 5**. Este proyecto está basado en los conceptos de la **Sección 5** del curso:

- **Listas de diccionarios** para el catálogo de juegos
- **Ordenación con key/lambda** para filtros y ordenamiento
- **min/max/sum** para estadísticas y precios
- **Comprensiones de listas** para filtrado dinámico
- **CRUD completo** con API REST

---

## 🚀 Características

### Catálogo de Juegos
- ✅ 16 juegos con información detallada
- ✅ Imágenes, videos y capturas de pantalla
- ✅ Requisitos del sistema
- ✅ Valoraciones y reseñas
- ✅ Múltiples plataformas (PC, PlayStation, Xbox, Nintendo)

### Funcionalidades
- 🛒 **Carrito de compras** - Añadir, eliminar, comprar
- ❤️ **Lista de deseos** - Guardar juegos para después
- 📚 **Biblioteca** - Juegos comprados
- 🔍 **Búsqueda** - Por nombre y etiquetas
- 🏷️ **Filtros avanzados** - Categoría, precio, ofertas, gratis
- 📊 **Ordenación** - Por nombre, precio, valoración, fecha, popularidad
- ⭐ **Sistema de reseñas** - Valorar y comentar juegos

### Diseño
- 🎨 Tema oscuro estilo Steam
- 📱 Diseño responsive
- ✨ Animaciones y transiciones suaves
- 🎯 Interfaz intuitiva

---

## 📁 Estructura del Proyecto

```
steam_store/
├── app.py                    # Aplicación Flask principal
├── README.md                 # Este archivo
├── templates/
│   ├── base.html            # Plantilla base con navbar y footer
│   ├── index.html           # Página principal
│   ├── tienda.html          # Catálogo de juegos
│   ├── detalle_juego.html   # Detalle de un juego
│   ├── carrito.html         # Carrito de compras
│   ├── biblioteca.html      # Biblioteca de juegos
│   ├── wishlist.html        # Lista de deseos
│   └── 404.html             # Página de error
└── static/
    ├── css/                 # Estilos CSS
    ├── js/                  # JavaScript
    └── img/                 # Imágenes
```

---

## 🛠️ Instalación

### 1. Requisitos
- Python 3.8 o superior
- Flask

### 2. Instalar Flask
```bash
pip install flask
```

### 3. Ejecutar la aplicación
```bash
cd steam_store
python app.py
```

### 4. Abrir en el navegador
Visita: **http://127.0.0.1:5000**

---

## 📊 API REST

### Endpoints disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/juegos` | Obtener todos los juegos |
| GET | `/api/juego/<id>` | Obtener un juego por ID |
| GET | `/api/buscar?q=texto` | Buscar juegos |
| GET | `/api/estadisticas` | Estadísticas de la tienda |
| GET | `/api/carrito` | Ver carrito |
| POST | `/api/carrito/agregar` | Añadir al carrito |
| DELETE | `/api/carrito/eliminar/<id>` | Eliminar del carrito |
| DELETE | `/api/carrito/vaciar` | Vaciar carrito |
| POST | `/api/carrito/comprar` | Procesar compra |
| POST | `/api/wishlist/agregar` | Añadir a wishlist |
| DELETE | `/api/wishlist/eliminar/<id>` | Eliminar de wishlist |
| POST | `/api/review` | Añadir reseña |

### Ejemplos de uso

```python
# Obtener juegos por categoría ordenados por precio
GET /api/juegos?categoria=RPG&orden=precio

# Buscar juegos
GET /api/buscar?q=witcher

# Añadir al carrito
POST /api/carrito/agregar
Body: {"id": 1}
```

---

## 🎯 Conceptos de la Sección 5 Aplicados

### 1. Listas de diccionarios
```python
catalogo_juegos = [
    {"id": 1, "nombre": "Cyberpunk 2077", "precio": 59.99, ...},
    {"id": 2, "nombre": "The Witcher 3", "precio": 9.99, ...},
]
```

### 2. Ordenación con key/lambda
```python
# Ordenar por precio ascendente
ordenados = sorted(catalogo_juegos, key=lambda j: j["precio"])

# Ordenar por valoración descendente
mejor_valorados = sorted(catalogo_juegos, key=lambda j: j["valoracion"], reverse=True)
```

### 3. Comprensiones de listas
```python
# Filtrar juegos con descuento
ofertas = [j for j in catalogo_juegos if j["descuento"] > 0]

# Filtrar juegos gratis
gratis = [j for j in catalogo_juegos if j["precio"] == 0]

# Buscar por nombre
resultados = [j for j in catalogo_juegos if "witcher" in j["nombre"].lower()]
```

### 4. min/max/sum con key
```python
# Juego más barato
mas_barato = min(catalogo_juegos, key=lambda j: j["precio"])

# Mejor valorado
mejor = max(catalogo_juegos, key=lambda j: j["valoracion"])

# Total del carrito
total = sum(item["precio"] * item["cantidad"] for item in carrito)
```

---

## 📸 Capturas de Pantalla

### Página Principal
- Carrusel de juegos destacados
- Ofertas especiales
- Mejor valorados
- Nuevos lanzamientos

### Tienda
- Catálogo completo
- Filtros por categoría, precio, ofertas
- Ordenación múltiple
- Vista de tarjetas

### Detalle del Juego
- Video/imagen principal
- Capturas de pantalla
- Descripción completa
- Requisitos del sistema
- Sistema de reseñas
- Juegos similares

### Carrito
- Lista de items
- Resumen de precios
- Ahorro por descuentos
- Proceso de compra

---

## 🔧 Personalización

### Añadir nuevos juegos
Edita el archivo `app.py` y añade nuevos diccionarios al `catalogo_juegos`:

```python
{
    "id": 17,
    "nombre": "Nuevo Juego",
    "descripcion": "Descripción del juego",
    "precio": 49.99,
    "precio_original": 49.99,
    "descuento": 0,
    "categoria": "RPG",
    ...
}
```

### Modificar estilos
Los estilos CSS están en la plantilla `base.html`. Puedes modificar las variables CSS:

```css
:root {
    --steam-dark: #171a21;
    --steam-accent: #66c0f4;
    --steam-green: #5c7e10;
    ...
}
```

---

## 📚 Recursos Educativos

Este proyecto enseña:

1. **Flask**
   - Rutas y vistas
   - Templates con Jinja2
   - API REST
   - Manejo de formularios

2. **Python**
   - Listas y diccionarios
   - Funciones lambda
   - Comprensiones
   - Funciones built-in (sorted, min, max, sum)

3. **Frontend**
   - Bootstrap 5
   - CSS personalizado
   - JavaScript asíncrono (fetch API)
   - Diseño responsive

---

## 👨‍🏫 Autor

**Joaquín** - [clasesonlinejoaquin.es](https://clasesonlinejoaquin.es/)

---

## 📄 Licencia

Este proyecto es para fines educativos.

---

## 🎮 ¡Disfruta aprendiendo!

```
╔══════════════════════════════════════════════════════════════╗
║   🎮 STEAM STORE CLONE - Proyecto Didáctico Python Flask    ║
║   ══════════════════════════════════════════════════════    ║
║   📊 16 juegos en el catálogo                               ║
║   📁 12 categorías disponibles                              ║
║   🌐 Servidor: http://127.0.0.1:5000                        ║
╚══════════════════════════════════════════════════════════════╝
```
