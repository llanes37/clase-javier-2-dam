# Ejercicios - Lección 08: Coroutines y Flow

## Ejercicio 1: Cargas paralelas

### Instrucciones

Crea una pantalla de dashboard que carga 3 secciones en paralelo:
- Usuarios recientes
- Posts populares
- Estadísticas

### Requisitos

- Las 3 llamadas deben ejecutarse en paralelo con `async`
- Mostrar loading mientras cargan
- Mostrar cada sección cuando esté lista (no esperar a todas)
- Si una falla, las otras deben seguir funcionando

### Criterios de aceptación

- [ ] Las llamadas se ejecutan en paralelo
- [ ] Cada sección tiene su propio estado de loading
- [ ] Un error no afecta a las otras secciones
- [ ] Usa `async/await` correctamente

---

## Ejercicio 2: Contador con Flow

### Instrucciones

Crea un contador que incrementa cada segundo automáticamente.

### Requisitos

- Flow que emite números del 1 al 60
- Botón para pausar/reanudar
- Botón para reiniciar
- Mostrar el tiempo en formato MM:SS

### Criterios de aceptación

- [ ] El contador incrementa cada segundo
- [ ] Pausar detiene el contador
- [ ] Reanudar continúa desde donde estaba
- [ ] Reiniciar vuelve a 0

---

## Ejercicio 3: Búsqueda con debounce

### Instrucciones

Implementa una barra de búsqueda que busca mientras escribes.

### Requisitos

- Debounce de 500ms
- Mostrar "Buscando..." durante la búsqueda
- Cancelar búsqueda anterior si hay nueva
- Mostrar resultados o "Sin resultados"

### Datos simulados

```kotlin
suspend fun searchProducts(query: String): List<String> {
    delay(1000) // Simular latencia
    return listOf("Laptop", "Mouse", "Teclado", "Monitor", "Webcam")
        .filter { it.contains(query, ignoreCase = true) }
}
```

### Criterios de aceptación

- [ ] Debounce funciona (no busca en cada tecla)
- [ ] `flatMapLatest` cancela búsquedas anteriores
- [ ] UI muestra estados correctamente

---

## Ejercicio 4: Combine de filtros

### Instrucciones

Lista de productos con filtros combinados:
- Búsqueda por texto
- Filtro por categoría
- Filtro por rango de precio

### Requisitos

- 3 StateFlows para los filtros
- `combine` para unir los filtros
- Actualización reactiva cuando cambia cualquier filtro

### Modelo de datos

```kotlin
data class Product(
    val id: Int,
    val name: String,
    val category: String,
    val price: Double
)

val categories = listOf("Todos", "Electrónica", "Ropa", "Hogar")
```

### Criterios de aceptación

- [ ] Los 3 filtros se combinan correctamente
- [ ] La lista se actualiza reactivamente
- [ ] "Todos" en categoría muestra todo
- [ ] El rango de precio funciona

---

## Ejercicio 5: Eventos con SharedFlow

### Instrucciones

Implementa un sistema de notificaciones usando SharedFlow.

### Requisitos

- ViewModel emite eventos de navegación y mensajes
- La UI reacciona a los eventos (snackbar, navegación)
- Los eventos no se pierden si la UI está en background

### Eventos

```kotlin
sealed class UiEvent {
    data class ShowSnackbar(val message: String) : UiEvent()
    data class Navigate(val route: String) : UiEvent()
    object ShowDialog : UiEvent()
}
```

### Criterios de aceptación

- [ ] SharedFlow configurado correctamente
- [ ] Eventos se recolectan en LaunchedEffect
- [ ] Snackbar se muestra
- [ ] Navegación funciona

---

## Ejercicio 6: Polling con Flow

### Instrucciones

Implementa actualización automática cada 30 segundos.

### Requisitos

- Flow que emite datos cada 30 segundos
- Indicador de "Última actualización: hace X segundos"
- Botón para forzar actualización
- Pausar polling cuando la app está en background

### Criterios de aceptación

- [ ] Datos se actualizan automáticamente
- [ ] Muestra tiempo desde última actualización
- [ ] Actualización manual funciona
- [ ] Polling se pausa en background

---

## Ejercicio 7 (Bonus): StateFlow con stateIn

### Instrucciones

Convierte un Flow del repositorio a StateFlow en el ViewModel.

### Requisitos

- Repository expone `Flow<List<Item>>`
- ViewModel convierte a `StateFlow` con `stateIn`
- Usa `WhileSubscribed(5000)` para eficiencia
- La UI usa `collectAsState()`

### Código base

```kotlin
class ItemRepository {
    fun observeItems(): Flow<List<Item>> = flow {
        while (true) {
            emit(fetchItems())
            delay(10000)
        }
    }
}
```

### Criterios de aceptación

- [ ] `stateIn` configurado correctamente
- [ ] El flow se inicia solo cuando hay observadores
- [ ] Se para 5 segundos después de perder observadores
- [ ] La UI recibe actualizaciones

---

## Entrega

1. Un archivo por ejercicio
2. Incluye comentarios explicando el flujo
3. Usa `@Preview` para las pantallas
4. Crea rama y PR
