# Lección 04: MVVM y UI State

## Objetivos

- Entender el patrón MVVM en Android
- Implementar ViewModel con Compose
- Modelar estados de UI con sealed class
- Usar StateFlow con collectAsState
- Separar lógica de negocio de la UI

---

## 1. ¿Por qué MVVM?

### Problema sin arquitectura

```kotlin
// ❌ Mal: Todo mezclado en la UI
@Composable
fun UserScreen() {
    var users by remember { mutableStateOf<List<User>>(emptyList()) }
    var loading by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) {
        loading = true
        try {
            users = api.getUsers()  // Llamada de red en composable
        } catch (e: Exception) {
            error = e.message
        }
        loading = false
    }
    // ... UI
}
```

**Problemas:**
- Lógica de negocio en la UI
- Difícil de testear
- Estado disperso
- Se pierde al rotar el dispositivo

### Solución: MVVM

```
┌─────────────────────────────────────────────────┐
│                     View                         │
│              (Composables)                       │
│                                                  │
│  • Muestra UI                                    │
│  • Reacciona a eventos del usuario              │
│  • Observa el estado del ViewModel              │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│                  ViewModel                       │
│                                                  │
│  • Mantiene el estado de la UI                  │
│  • Contiene lógica de presentación              │
│  • Sobrevive a cambios de configuración         │
│  • Expone StateFlow/LiveData                    │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│                Model / Repository                │
│                                                  │
│  • Acceso a datos (API, DB)                     │
│  • Lógica de negocio                            │
└─────────────────────────────────────────────────┘
```

---

## 2. ViewModel básico

### Dependencia

```kotlin
// build.gradle.kts
implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
```

### Crear un ViewModel

```kotlin
class CounterViewModel : ViewModel() {
    
    private val _count = MutableStateFlow(0)
    val count: StateFlow<Int> = _count.asStateFlow()

    fun increment() {
        _count.value++
    }

    fun decrement() {
        _count.value--
    }
}
```

### Usar en Compose

```kotlin
@Composable
fun CounterScreen(
    viewModel: CounterViewModel = viewModel()
) {
    val count by viewModel.count.collectAsState()

    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text("Contador: $count", fontSize = 24.sp)

        Row {
            Button(onClick = { viewModel.decrement() }) {
                Text("-")
            }
            Spacer(Modifier.width(16.dp))
            Button(onClick = { viewModel.increment() }) {
                Text("+")
            }
        }
    }
}
```

**Import necesario:**
```kotlin
import androidx.lifecycle.viewmodel.compose.viewModel
```

---

## 3. UiState con sealed class

### El problema de múltiples estados

```kotlin
// ❌ Mal: Estados separados, fácil tener estados inválidos
class UserViewModel : ViewModel() {
    val users = MutableStateFlow<List<User>>(emptyList())
    val loading = MutableStateFlow(false)
    val error = MutableStateFlow<String?>(null)
    
    // ¿Qué pasa si loading=true Y error!=null?
    // Estado inválido posible
}
```

### Solución: Sealed class

```kotlin
// ✅ Bien: Un solo estado que representa todas las posibilidades
sealed class UserUiState {
    object Loading : UserUiState()
    data class Success(val users: List<User>) : UserUiState()
    data class Error(val message: String) : UserUiState()
    object Empty : UserUiState()
}
```

### ViewModel con UiState

```kotlin
class UserViewModel(
    private val repository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<UserUiState>(UserUiState.Loading)
    val uiState: StateFlow<UserUiState> = _uiState.asStateFlow()

    init {
        loadUsers()
    }

    fun loadUsers() {
        viewModelScope.launch {
            _uiState.value = UserUiState.Loading
            
            try {
                val users = repository.getUsers()
                _uiState.value = if (users.isEmpty()) {
                    UserUiState.Empty
                } else {
                    UserUiState.Success(users)
                }
            } catch (e: Exception) {
                _uiState.value = UserUiState.Error(
                    e.message ?: "Error desconocido"
                )
            }
        }
    }
}
```

### UI que consume UiState

```kotlin
@Composable
fun UserScreen(
    viewModel: UserViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    when (val state = uiState) {
        is UserUiState.Loading -> LoadingIndicator()
        is UserUiState.Success -> UserList(users = state.users)
        is UserUiState.Error -> ErrorMessage(
            message = state.message,
            onRetry = { viewModel.loadUsers() }
        )
        is UserUiState.Empty -> EmptyState()
    }
}

@Composable
fun LoadingIndicator() {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        CircularProgressIndicator()
    }
}

@Composable
fun ErrorMessage(message: String, onRetry: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(message, color = MaterialTheme.colorScheme.error)
        Spacer(Modifier.height(16.dp))
        Button(onClick = onRetry) {
            Text("Reintentar")
        }
    }
}

@Composable
fun EmptyState() {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Text("No hay datos disponibles")
    }
}
```

---

## 4. Data class para UiState complejo

Cuando el estado tiene muchos campos, usa data class:

```kotlin
data class TaskListUiState(
    val tasks: List<Task> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val filter: TaskFilter = TaskFilter.ALL,
    val searchQuery: String = ""
) {
    val filteredTasks: List<Task>
        get() = tasks
            .filter { task ->
                when (filter) {
                    TaskFilter.ALL -> true
                    TaskFilter.PENDING -> !task.completed
                    TaskFilter.COMPLETED -> task.completed
                }
            }
            .filter { task ->
                searchQuery.isEmpty() || 
                task.title.contains(searchQuery, ignoreCase = true)
            }
    
    val isEmpty: Boolean
        get() = !isLoading && error == null && filteredTasks.isEmpty()
}

enum class TaskFilter {
    ALL, PENDING, COMPLETED
}
```

### ViewModel con data class UiState

```kotlin
class TaskViewModel(
    private val repository: TaskRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(TaskListUiState())
    val uiState: StateFlow<TaskListUiState> = _uiState.asStateFlow()

    init {
        loadTasks()
    }

    fun loadTasks() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            
            try {
                val tasks = repository.getTasks()
                _uiState.update { it.copy(tasks = tasks, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update { 
                    it.copy(
                        isLoading = false, 
                        error = e.message ?: "Error"
                    ) 
                }
            }
        }
    }

    fun setFilter(filter: TaskFilter) {
        _uiState.update { it.copy(filter = filter) }
    }

    fun setSearchQuery(query: String) {
        _uiState.update { it.copy(searchQuery = query) }
    }

    fun toggleTask(taskId: Int) {
        _uiState.update { state ->
            state.copy(
                tasks = state.tasks.map { task ->
                    if (task.id == taskId) task.copy(completed = !task.completed)
                    else task
                }
            )
        }
    }
}
```

---

## 5. Eventos de UI (one-shot)

Para eventos que solo deben procesarse una vez (navegación, snackbar):

```kotlin
class TaskViewModel : ViewModel() {
    // Estado persistente
    private val _uiState = MutableStateFlow(TaskListUiState())
    val uiState: StateFlow<TaskListUiState> = _uiState.asStateFlow()

    // Eventos one-shot
    private val _events = MutableSharedFlow<TaskEvent>()
    val events: SharedFlow<TaskEvent> = _events.asSharedFlow()

    fun deleteTask(taskId: Int) {
        viewModelScope.launch {
            try {
                repository.deleteTask(taskId)
                _uiState.update { state ->
                    state.copy(tasks = state.tasks.filter { it.id != taskId })
                }
                _events.emit(TaskEvent.ShowSnackbar("Tarea eliminada"))
            } catch (e: Exception) {
                _events.emit(TaskEvent.ShowSnackbar("Error al eliminar"))
            }
        }
    }

    fun onTaskClick(taskId: Int) {
        viewModelScope.launch {
            _events.emit(TaskEvent.NavigateToDetail(taskId))
        }
    }
}

sealed class TaskEvent {
    data class ShowSnackbar(val message: String) : TaskEvent()
    data class NavigateToDetail(val taskId: Int) : TaskEvent()
}
```

### Consumir eventos en Compose

```kotlin
@Composable
fun TaskScreen(
    viewModel: TaskViewModel = viewModel(),
    onNavigateToDetail: (Int) -> Unit
) {
    val uiState by viewModel.uiState.collectAsState()
    val snackbarHostState = remember { SnackbarHostState() }

    // Observar eventos
    LaunchedEffect(Unit) {
        viewModel.events.collect { event ->
            when (event) {
                is TaskEvent.ShowSnackbar -> {
                    snackbarHostState.showSnackbar(event.message)
                }
                is TaskEvent.NavigateToDetail -> {
                    onNavigateToDetail(event.taskId)
                }
            }
        }
    }

    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) { padding ->
        // ... contenido
    }
}
```

---

## 6. Inyección de dependencias simple

Sin librerías, pasando dependencias manualmente:

### Repository

```kotlin
interface TaskRepository {
    suspend fun getTasks(): List<Task>
    suspend fun addTask(task: Task)
    suspend fun deleteTask(id: Int)
}

class TaskRepositoryImpl(
    private val api: TaskApi,
    private val dao: TaskDao
) : TaskRepository {
    override suspend fun getTasks(): List<Task> {
        return try {
            val remote = api.getTasks()
            dao.insertAll(remote)
            remote
        } catch (e: Exception) {
            dao.getAll()  // Fallback a local
        }
    }
    // ...
}
```

### ViewModel Factory

```kotlin
class TaskViewModel(
    private val repository: TaskRepository
) : ViewModel() {
    // ...
}

// Factory para crear el ViewModel con dependencias
class TaskViewModelFactory(
    private val repository: TaskRepository
) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(TaskViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return TaskViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
```

### Uso en Compose

```kotlin
@Composable
fun TaskScreen(
    repository: TaskRepository  // Pasado desde arriba
) {
    val viewModel: TaskViewModel = viewModel(
        factory = TaskViewModelFactory(repository)
    )
    // ...
}
```

---

## 7. Patrón completo: ejemplo Todo

```kotlin
// === Models ===
data class Task(
    val id: Int,
    val title: String,
    val completed: Boolean
)

// === UiState ===
data class TodoUiState(
    val tasks: List<Task> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val newTaskTitle: String = ""
) {
    val canAddTask: Boolean
        get() = newTaskTitle.isNotBlank() && !isLoading
}

// === ViewModel ===
class TodoViewModel : ViewModel() {

    private val _uiState = MutableStateFlow(TodoUiState())
    val uiState: StateFlow<TodoUiState> = _uiState.asStateFlow()

    private var nextId = 1

    fun onNewTaskTitleChange(title: String) {
        _uiState.update { it.copy(newTaskTitle = title) }
    }

    fun addTask() {
        val title = _uiState.value.newTaskTitle
        if (title.isBlank()) return

        val newTask = Task(
            id = nextId++,
            title = title,
            completed = false
        )

        _uiState.update { state ->
            state.copy(
                tasks = state.tasks + newTask,
                newTaskTitle = ""
            )
        }
    }

    fun toggleTask(taskId: Int) {
        _uiState.update { state ->
            state.copy(
                tasks = state.tasks.map { task ->
                    if (task.id == taskId) task.copy(completed = !task.completed)
                    else task
                }
            )
        }
    }

    fun deleteTask(taskId: Int) {
        _uiState.update { state ->
            state.copy(tasks = state.tasks.filter { it.id != taskId })
        }
    }
}

// === UI ===
@Composable
fun TodoScreen(
    viewModel: TodoViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    Column(modifier = Modifier.fillMaxSize()) {
        // Input para nueva tarea
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            OutlinedTextField(
                value = uiState.newTaskTitle,
                onValueChange = viewModel::onNewTaskTitleChange,
                modifier = Modifier.weight(1f),
                placeholder = { Text("Nueva tarea...") },
                singleLine = true
            )
            
            Spacer(Modifier.width(8.dp))
            
            Button(
                onClick = viewModel::addTask,
                enabled = uiState.canAddTask
            ) {
                Text("Añadir")
            }
        }

        // Lista de tareas
        LazyColumn {
            items(uiState.tasks, key = { it.id }) { task ->
                TaskRow(
                    task = task,
                    onToggle = { viewModel.toggleTask(task.id) },
                    onDelete = { viewModel.deleteTask(task.id) }
                )
            }
        }
    }
}

@Composable
fun TaskRow(
    task: Task,
    onToggle: () -> Unit,
    onDelete: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Checkbox(
            checked = task.completed,
            onCheckedChange = { onToggle() }
        )
        
        Text(
            text = task.title,
            modifier = Modifier.weight(1f),
            textDecoration = if (task.completed) TextDecoration.LineThrough else null
        )
        
        IconButton(onClick = onDelete) {
            Icon(Icons.Default.Delete, contentDescription = "Eliminar")
        }
    }
}
```

---

## Resumen

| Concepto | Descripción |
|----------|-------------|
| ViewModel | Mantiene estado, sobrevive a rotación |
| StateFlow | Stream de estado observable |
| collectAsState | Convierte Flow a State de Compose |
| UiState sealed class | Estados mutuamente excluyentes |
| UiState data class | Estado con múltiples campos |
| update {} | Actualiza MutableStateFlow de forma segura |
| viewModelScope | Scope para coroutines del ViewModel |

---

## Siguiente paso

→ [ejercicios.md](ejercicios.md)
