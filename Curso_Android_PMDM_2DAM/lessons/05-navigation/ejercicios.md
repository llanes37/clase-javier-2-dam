# Ejercicios - Lección 05: Navigation Compose

## Ejercicio 1: Navegación básica

### Instrucciones

Crea una app con 3 pantallas:
1. **Home**: Muestra título y botón "Ir a About"
2. **About**: Muestra información y botón "Ir a Contact"
3. **Contact**: Muestra datos de contacto y botón "Volver al inicio"

El botón "Volver al inicio" debe limpiar todo el back stack.

### Criterios de aceptación

- [ ] Las 3 pantallas existen y navegan correctamente
- [ ] El back button del sistema funciona
- [ ] "Volver al inicio" limpia el back stack (no se puede volver atrás)
- [ ] Usa sealed class para definir las rutas

---

## Ejercicio 2: Navegación con argumentos

### Instrucciones

Crea una app de lista de productos:

1. **ProductListScreen**: Lista de productos
2. **ProductDetailScreen**: Detalle de un producto (recibe productId)

Datos de ejemplo:
```kotlin
data class Product(val id: Int, val name: String, val price: Double, val description: String)

val products = listOf(
    Product(1, "Laptop", 999.99, "Potente laptop para trabajo"),
    Product(2, "Mouse", 29.99, "Mouse ergonómico"),
    Product(3, "Teclado", 79.99, "Teclado mecánico RGB")
)
```

### Criterios de aceptación

- [ ] La lista muestra todos los productos
- [ ] Al pulsar un producto, navega al detalle
- [ ] El detalle muestra la información correcta del producto
- [ ] El productId se pasa como argumento en la ruta

---

## Ejercicio 3: Bottom Navigation

### Instrucciones

Crea una app con bottom navigation y 3 secciones:
1. **Home**: Lista de items
2. **Search**: Barra de búsqueda
3. **Profile**: Información de perfil

Requisitos:
- El icono seleccionado debe destacarse
- Al cambiar de tab, el estado se mantiene
- Al pulsar un tab ya seleccionado, no debe hacer nada

### Criterios de aceptación

- [ ] Bottom bar con 3 items
- [ ] Navegación funciona correctamente
- [ ] El tab activo se resalta
- [ ] `launchSingleTop` y `restoreState` configurados

---

## Ejercicio 4: Navegación con argumentos opcionales

### Instrucciones

Crea una pantalla de búsqueda con filtros:

1. **SearchScreen**: 
   - Recibe `query` (opcional, default "")
   - Recibe `category` (opcional, default "all")
   
2. Desde Home, permite navegar a SearchScreen:
   - Sin argumentos (búsqueda vacía)
   - Con query predefinido
   - Con query y categoría

### Criterios de aceptación

- [ ] Los argumentos opcionales funcionan
- [ ] Si no se pasa query, usa string vacío
- [ ] Si no se pasa category, usa "all"
- [ ] La URL de navegación es correcta

---

## Ejercicio 5: Resultado de navegación

### Instrucciones

Crea un flujo de selección:

1. **MainScreen**: Muestra el item seleccionado (o "Ninguno")
2. **PickerScreen**: Lista de opciones para elegir

Al seleccionar en PickerScreen:
- Vuelve a MainScreen
- Pasa el item seleccionado como resultado
- MainScreen muestra el item seleccionado

### Criterios de aceptación

- [ ] MainScreen muestra "Ninguno" inicialmente
- [ ] PickerScreen muestra lista de opciones
- [ ] Al seleccionar, vuelve con el resultado
- [ ] MainScreen muestra el item seleccionado
- [ ] Usa `savedStateHandle` para pasar el resultado

---

## Ejercicio 6: App completa con navegación

### Instrucciones

Crea una app de notas con:

**Pantallas:**
1. NoteListScreen (lista de notas)
2. NoteDetailScreen (ver nota completa)
3. NoteEditScreen (crear/editar nota)
4. SettingsScreen (configuración)

**Navegación:**
- Desde lista: ver detalle, crear nueva, ir a settings
- Desde detalle: editar, volver
- Desde editar: guardar y volver al detalle
- Desde settings: volver

**Estructura de datos:**
```kotlin
data class Note(
    val id: Int,
    val title: String,
    val content: String,
    val createdAt: Long
)
```

### Criterios de aceptación

- [ ] Todas las pantallas existen
- [ ] La navegación funciona correctamente
- [ ] Los argumentos (noteId) se pasan bien
- [ ] Crear nota vs editar nota se diferencia por argumento
- [ ] El back stack es coherente

---

## Ejercicio 7 (Bonus): Deep links

### Instrucciones

Configura deep links para la app de productos:

- `https://miapp.com/products` → Lista
- `https://miapp.com/product/123` → Detalle del producto 123

### Criterios de aceptación

- [ ] Los deep links están configurados en NavHost
- [ ] El AndroidManifest tiene los intent-filter
- [ ] Puedes probar con: `adb shell am start -W -a android.intent.action.VIEW -d "https://miapp.com/product/1"`

---

## Entrega

1. Organiza las pantallas en package `ui/screens/`
2. Las rutas en `navigation/Routes.kt` o `navigation/Screen.kt`
3. El NavHost en `navigation/AppNavigation.kt`
4. Crea rama y PR
