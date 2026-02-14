# Ejercicios - Lección 06: Listas y rendimiento

## Ejercicio 1: Lista básica con estados

Crea una pantalla que muestre una lista de contactos con todos los estados posibles.

### Requisitos

- Estados: Loading, Success, Error, Empty
- Cada contacto: avatar (inicial), nombre, teléfono
- Usa key con el ID del contacto
- Botón de retry cuando hay error

### Datos

```kotlin
data class Contact(
    val id: Int,
    val name: String,
    val phone: String
)
```

### Criterios de aceptación

- [ ] Los 4 estados se muestran correctamente
- [ ] Usa LazyColumn con key
- [ ] El botón retry funciona
- [ ] El avatar muestra la inicial del nombre

---

## Ejercicio 2: Lista con headers sticky

Crea una lista de productos agrupados por categoría con headers pegajosos.

### Requisitos

- Productos agrupados por categoría
- Headers que se quedan fijos al hacer scroll
- Cada producto: nombre, precio, en stock (boolean)

### Datos

```kotlin
val productosPorCategoria = mapOf(
    "Electrónica" to listOf(
        Product(1, "Laptop", 999.99, true),
        Product(2, "Mouse", 29.99, true),
        Product(3, "Teclado", 79.99, false)
    ),
    "Ropa" to listOf(
        Product(4, "Camiseta", 19.99, true),
        Product(5, "Pantalón", 49.99, true)
    ),
    "Hogar" to listOf(
        Product(6, "Lámpara", 39.99, true),
        Product(7, "Alfombra", 89.99, false)
    )
)
```

### Criterios de aceptación

- [ ] Headers son sticky
- [ ] Productos agotados se muestran diferente
- [ ] Usa stickyHeader correctamente

---

## Ejercicio 3: Grid de imágenes

Crea una galería de imágenes en formato grid.

### Requisitos

- Grid de 3 columnas
- Cada celda es cuadrada (aspect ratio 1:1)
- Al pulsar, muestra un toast/snackbar con el ID
- Usa colores como placeholder de imágenes

### Criterios de aceptación

- [ ] Usa LazyVerticalGrid
- [ ] 3 columnas fijas
- [ ] Celdas cuadradas
- [ ] Click funciona correctamente

---

## Ejercicio 4: Pull to Refresh

Añade pull-to-refresh a una lista de noticias.

### Requisitos

- Lista de noticias (título, fecha, resumen)
- Pull-to-refresh funcional
- Durante refresh: indicador visible
- Simular carga de 2 segundos
- Añadir nuevas noticias al refrescar

### Criterios de aceptación

- [ ] Pull-to-refresh funciona
- [ ] Indicador se muestra durante la carga
- [ ] Se añaden nuevas noticias
- [ ] Usa PullToRefreshBox (Material 3)

---

## Ejercicio 5: Scroll y FAB

Crea una lista con un FAB que aparece/desaparece según el scroll.

### Requisitos

- Lista larga de elementos
- FAB "scroll to top" que aparece al hacer scroll hacia abajo
- FAB desaparece cuando estás arriba
- Animación suave al aparecer/desaparecer
- Click en FAB hace scroll animado al inicio

### Criterios de aceptación

- [ ] FAB aparece solo al hacer scroll
- [ ] AnimatedVisibility para mostrar/ocultar
- [ ] animateScrollToItem funciona
- [ ] derivedStateOf para detectar posición

---

## Ejercicio 6: Paginación infinita

Implementa scroll infinito (cargar más al llegar al final).

### Requisitos

- Lista inicial de 20 elementos
- Al llegar cerca del final (5 items), cargar 10 más
- Indicador de carga al final de la lista
- Máximo 100 elementos (luego no cargar más)

### ViewModel sugerido

```kotlin
data class PaginatedUiState(
    val items: List<Item> = emptyList(),
    val isLoading: Boolean = false,
    val isLoadingMore: Boolean = false,
    val hasMore: Boolean = true
)
```

### Criterios de aceptación

- [ ] Carga inicial de 20 items
- [ ] Detecta scroll cerca del final
- [ ] Carga 10 más automáticamente
- [ ] Indicador de carga visible
- [ ] Para de cargar al llegar a 100

---

## Ejercicio 7 (Bonus): Lista con selección múltiple

Crea una lista con modo de selección múltiple.

### Requisitos

- Lista de archivos (nombre, tamaño, tipo)
- Long-press activa modo selección
- En modo selección: checkbox visible
- Contador de seleccionados en header
- Botón "Eliminar seleccionados"

### Criterios de aceptación

- [ ] Long-press activa selección
- [ ] Checkbox funciona
- [ ] Contador actualiza correctamente
- [ ] Eliminar quita los seleccionados
- [ ] Vuelve a modo normal al no quedar seleccionados

---

## Entrega

1. Cada ejercicio en un archivo separado
2. Incluye Preview para cada pantalla
3. Verifica que no hay warnings de rendimiento en Logcat
4. Crea rama y PR
