# Ejercicios - Lección 04: MVVM y UI State

## Ejercicio 1: Contador con ViewModel

### Instrucciones

Refactoriza el contador de la lección anterior para usar ViewModel:

1. Crea `CounterViewModel` con:
   - Estado del contador
   - Funciones: increment(), decrement(), reset()
   - El contador no puede bajar de 0

2. Crea `CounterScreen` que use el ViewModel

### Criterios de aceptación

- [ ] El contador sobrevive a la rotación del dispositivo
- [ ] El ViewModel expone StateFlow
- [ ] La UI usa collectAsState()
- [ ] El botón reset vuelve a 0
- [ ] El botón - se deshabilita cuando count == 0

---

## Ejercicio 2: Lista con UiState sealed class

### Instrucciones

Crea una pantalla que muestre una lista de productos con estados:

1. Define `ProductUiState` como sealed class con:
   - Loading
   - Success(products: List<Product>)
   - Error(message: String)
   - Empty

2. Crea `ProductViewModel` que:
   - Simule una carga de datos (delay de 2 segundos)
   - 50% de probabilidad de éxito, 50% de error (para probar)
   - Tenga función `retry()`

3. Crea `ProductScreen` que muestre UI diferente para cada estado

### Datos de ejemplo

```kotlin
data class Product(
    val id: Int,
    val name: String,
    val price: Double
)

val sampleProducts = listOf(
    Product(1, "Laptop", 999.99),
    Product(2, "Mouse", 29.99),
    Product(3, "Teclado", 79.99)
)
```

### Criterios de aceptación

- [ ] Se muestra Loading mientras carga
- [ ] Se muestra la lista si tiene éxito
- [ ] Se muestra Error con botón retry si falla
- [ ] El when sobre UiState es exhaustivo
- [ ] El estado sobrevive a rotación

---

## Ejercicio 3: Formulario con ViewModel

### Instrucciones

Crea un formulario de login con ViewModel:

1. Define `LoginUiState` como data class:
   ```kotlin
   data class LoginUiState(
       val email: String = "",
       val password: String = "",
       val isLoading: Boolean = false,
       val error: String? = null,
       val isLoggedIn: Boolean = false
   )
   ```

2. Crea `LoginViewModel` con:
   - Funciones para actualizar email y password
   - Función login() que simule llamada (2s delay)
   - Validación: email debe contener @, password mín 6 chars
   - Si el email es "error@test.com", simula error

3. Crea `LoginScreen` con:
   - Campos email y password
   - Botón login (deshabilitado si inválido o loading)
   - Indicador de carga
   - Mensaje de error si falla
   - Mensaje de éxito si login ok

### Criterios de aceptación

- [ ] La validación funciona correctamente
- [ ] El botón se deshabilita durante la carga
- [ ] Los errores se muestran y se pueden limpiar
- [ ] El estado "logged in" se muestra correctamente

---

## Ejercicio 4: Todo App completa

### Instrucciones

Implementa una app de tareas completa con MVVM:

1. Define `Task`:
   ```kotlin
   data class Task(
       val id: Int,
       val title: String,
       val description: String,
       val completed: Boolean,
       val priority: Priority
   )
   
   enum class Priority { LOW, MEDIUM, HIGH }
   ```

2. Define `TodoUiState`:
   ```kotlin
   data class TodoUiState(
       val tasks: List<Task>,
       val filter: TaskFilter,
       val isAddingTask: Boolean,
       val newTaskTitle: String,
       val newTaskDescription: String,
       val newTaskPriority: Priority,
       val error: String?
   )
   
   enum class TaskFilter { ALL, PENDING, COMPLETED }
   ```

3. Implementa `TodoViewModel` con:
   - addTask()
   - toggleTask(id)
   - deleteTask(id)
   - setFilter(filter)
   - Propiedades computadas: filteredTasks, pendingCount, completedCount

4. Implementa la UI con:
   - Lista de tareas filtrable
   - Chips o tabs para filtros
   - Diálogo o sección para añadir tarea
   - Indicador de tareas pendientes/completadas

### Criterios de aceptación

- [ ] CRUD completo funciona
- [ ] Los filtros funcionan correctamente
- [ ] Se puede añadir tarea con título, descripción y prioridad
- [ ] Las tareas completadas se ven diferente
- [ ] El estado sobrevive a rotación

---

## Ejercicio 5: Eventos one-shot

### Instrucciones

Extiende el ejercicio anterior añadiendo:

1. SharedFlow para eventos:
   - `ShowSnackbar(message: String)`
   - `ConfirmDelete(taskId: Int)`

2. Al eliminar una tarea:
   - Mostrar diálogo de confirmación
   - Si confirma, eliminar y mostrar snackbar
   - Si cancela, no hacer nada

3. Al completar una tarea:
   - Mostrar snackbar "Tarea completada"

### Criterios de aceptación

- [ ] Los eventos se emiten correctamente
- [ ] El snackbar se muestra
- [ ] El diálogo de confirmación funciona
- [ ] Los eventos no se re-disparan al rotar

---

## Ejercicio 6 (Bonus): Testing de ViewModel

### Instrucciones

Escribe tests unitarios para `TodoViewModel`:

```kotlin
class TodoViewModelTest {
    
    @Test
    fun `addTask adds task to list`() {
        // Arrange
        val viewModel = TodoViewModel()
        
        // Act
        viewModel.onNewTaskTitleChange("Nueva tarea")
        viewModel.addTask()
        
        // Assert
        val state = viewModel.uiState.value
        assertEquals(1, state.tasks.size)
        assertEquals("Nueva tarea", state.tasks[0].title)
    }
    
    @Test
    fun `toggleTask changes completed status`() {
        // ...
    }
    
    @Test
    fun `deleteTask removes task from list`() {
        // ...
    }
    
    @Test
    fun `filter shows only matching tasks`() {
        // ...
    }
}
```

### Criterios de aceptación

- [ ] Mínimo 4 tests
- [ ] Tests pasan
- [ ] Cubren addTask, toggleTask, deleteTask, filter

---

## Entrega

1. Crea los ViewModels y Screens en archivos separados
2. Organiza en packages: `ui/`, `viewmodel/`, `model/`
3. Verifica que todo compila y funciona
4. Crea rama y PR
