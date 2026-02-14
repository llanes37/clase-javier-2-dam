# Soluciones - Lección 04: MVVM y UI State

## Ejercicio 1: Contador con ViewModel

```kotlin
// CounterViewModel.kt
class CounterViewModel : ViewModel() {

    private val _count = MutableStateFlow(0)
    val count: StateFlow<Int> = _count.asStateFlow()

    val canDecrement: StateFlow<Boolean> = _count.map { it > 0 }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), false)

    fun increment() {
        _count.value++
    }

    fun decrement() {
        if (_count.value > 0) {
            _count.value--
        }
    }

    fun reset() {
        _count.value = 0
    }
}

// CounterScreen.kt
@Composable
fun CounterScreen(
    viewModel: CounterViewModel = viewModel()
) {
    val count by viewModel.count.collectAsState()
    val canDecrement by viewModel.canDecrement.collectAsState()

    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = count.toString(),
            fontSize = 72.sp,
            fontWeight = FontWeight.Bold
        )

        Spacer(Modifier.height(32.dp))

        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            Button(
                onClick = { viewModel.decrement() },
                enabled = canDecrement
            ) {
                Text("-")
            }

            Button(onClick = { viewModel.reset() }) {
                Text("Reset")
            }

            Button(onClick = { viewModel.increment() }) {
                Text("+")
            }
        }
    }
}
```

---

## Ejercicio 2: Lista con UiState sealed class

```kotlin
// Models
data class Product(
    val id: Int,
    val name: String,
    val price: Double
)

// UiState
sealed class ProductUiState {
    object Loading : ProductUiState()
    data class Success(val products: List<Product>) : ProductUiState()
    data class Error(val message: String) : ProductUiState()
    object Empty : ProductUiState()
}

// ViewModel
class ProductViewModel : ViewModel() {

    private val _uiState = MutableStateFlow<ProductUiState>(ProductUiState.Loading)
    val uiState: StateFlow<ProductUiState> = _uiState.asStateFlow()

    private val sampleProducts = listOf(
        Product(1, "Laptop", 999.99),
        Product(2, "Mouse", 29.99),
        Product(3, "Teclado", 79.99)
    )

    init {
        loadProducts()
    }

    fun loadProducts() {
        viewModelScope.launch {
            _uiState.value = ProductUiState.Loading
            
            delay(2000) // Simular carga
            
            // 50% éxito, 50% error
            if (Random.nextBoolean()) {
                _uiState.value = ProductUiState.Success(sampleProducts)
            } else {
                _uiState.value = ProductUiState.Error("Error al cargar productos")
            }
        }
    }

    fun retry() {
        loadProducts()
    }
}

// Screen
@Composable
fun ProductScreen(
    viewModel: ProductViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    Box(modifier = Modifier.fillMaxSize()) {
        when (val state = uiState) {
            is ProductUiState.Loading -> {
                CircularProgressIndicator(
                    modifier = Modifier.align(Alignment.Center)
                )
            }
            
            is ProductUiState.Success -> {
                LazyColumn {
                    items(state.products, key = { it.id }) { product ->
                        ProductItem(product)
                    }
                }
            }
            
            is ProductUiState.Error -> {
                Column(
                    modifier = Modifier.align(Alignment.Center),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Icon(
                        imageVector = Icons.Default.Warning,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.error,
                        modifier = Modifier.size(48.dp)
                    )
                    Spacer(Modifier.height(16.dp))
                    Text(state.message)
                    Spacer(Modifier.height(16.dp))
                    Button(onClick = { viewModel.retry() }) {
                        Text("Reintentar")
                    }
                }
            }
            
            is ProductUiState.Empty -> {
                Text(
                    text = "No hay productos",
                    modifier = Modifier.align(Alignment.Center)
                )
            }
        }
    }
}

@Composable
fun ProductItem(product: Product) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(product.name, fontWeight = FontWeight.Bold)
            }
            Text(
                text = "${product.price} €",
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary
            )
        }
    }
}
```

---

## Ejercicio 3: Formulario con ViewModel

```kotlin
// UiState
data class LoginUiState(
    val email: String = "",
    val password: String = "",
    val isLoading: Boolean = false,
    val error: String? = null,
    val isLoggedIn: Boolean = false
) {
    val isEmailValid: Boolean
        get() = email.contains("@")
    
    val isPasswordValid: Boolean
        get() = password.length >= 6
    
    val canLogin: Boolean
        get() = isEmailValid && isPasswordValid && !isLoading
}

// ViewModel
class LoginViewModel : ViewModel() {

    private val _uiState = MutableStateFlow(LoginUiState())
    val uiState: StateFlow<LoginUiState> = _uiState.asStateFlow()

    fun onEmailChange(email: String) {
        _uiState.update { it.copy(email = email, error = null) }
    }

    fun onPasswordChange(password: String) {
        _uiState.update { it.copy(password = password, error = null) }
    }

    fun login() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            
            delay(2000) // Simular llamada
            
            val email = _uiState.value.email
            
            if (email == "error@test.com") {
                _uiState.update { 
                    it.copy(isLoading = false, error = "Credenciales inválidas") 
                }
            } else {
                _uiState.update { 
                    it.copy(isLoading = false, isLoggedIn = true) 
                }
            }
        }
    }

    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }
}

// Screen
@Composable
fun LoginScreen(
    viewModel: LoginViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    if (uiState.isLoggedIn) {
        // Pantalla de éxito
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Icon(
                    imageVector = Icons.Default.CheckCircle,
                    contentDescription = null,
                    tint = Color.Green,
                    modifier = Modifier.size(64.dp)
                )
                Spacer(Modifier.height(16.dp))
                Text("¡Login exitoso!", fontSize = 24.sp)
            }
        }
        return
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Iniciar sesión",
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold
        )

        Spacer(Modifier.height(32.dp))

        OutlinedTextField(
            value = uiState.email,
            onValueChange = viewModel::onEmailChange,
            label = { Text("Email") },
            isError = uiState.email.isNotEmpty() && !uiState.isEmailValid,
            supportingText = {
                if (uiState.email.isNotEmpty() && !uiState.isEmailValid) {
                    Text("Email inválido")
                }
            },
            enabled = !uiState.isLoading,
            modifier = Modifier.fillMaxWidth(),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email)
        )

        Spacer(Modifier.height(16.dp))

        OutlinedTextField(
            value = uiState.password,
            onValueChange = viewModel::onPasswordChange,
            label = { Text("Contraseña") },
            isError = uiState.password.isNotEmpty() && !uiState.isPasswordValid,
            supportingText = {
                if (uiState.password.isNotEmpty() && !uiState.isPasswordValid) {
                    Text("Mínimo 6 caracteres")
                }
            },
            enabled = !uiState.isLoading,
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier.fillMaxWidth()
        )

        // Error
        uiState.error?.let { error ->
            Spacer(Modifier.height(16.dp))
            Card(
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.errorContainer
                ),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = error,
                    color = MaterialTheme.colorScheme.onErrorContainer,
                    modifier = Modifier.padding(16.dp)
                )
            }
        }

        Spacer(Modifier.height(24.dp))

        Button(
            onClick = viewModel::login,
            enabled = uiState.canLogin,
            modifier = Modifier.fillMaxWidth()
        ) {
            if (uiState.isLoading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(20.dp),
                    color = MaterialTheme.colorScheme.onPrimary
                )
            } else {
                Text("Iniciar sesión")
            }
        }
    }
}
```

---

## Ejercicio 4: Todo App completa

```kotlin
// Models
data class Task(
    val id: Int,
    val title: String,
    val description: String,
    val completed: Boolean,
    val priority: Priority
)

enum class Priority { LOW, MEDIUM, HIGH }
enum class TaskFilter { ALL, PENDING, COMPLETED }

// UiState
data class TodoUiState(
    val tasks: List<Task> = emptyList(),
    val filter: TaskFilter = TaskFilter.ALL,
    val isAddingTask: Boolean = false,
    val newTaskTitle: String = "",
    val newTaskDescription: String = "",
    val newTaskPriority: Priority = Priority.MEDIUM,
    val error: String? = null
) {
    val filteredTasks: List<Task>
        get() = tasks.filter { task ->
            when (filter) {
                TaskFilter.ALL -> true
                TaskFilter.PENDING -> !task.completed
                TaskFilter.COMPLETED -> task.completed
            }
        }

    val pendingCount: Int
        get() = tasks.count { !it.completed }

    val completedCount: Int
        get() = tasks.count { it.completed }

    val canAddTask: Boolean
        get() = newTaskTitle.isNotBlank()
}

// ViewModel
class TodoViewModel : ViewModel() {

    private val _uiState = MutableStateFlow(TodoUiState())
    val uiState: StateFlow<TodoUiState> = _uiState.asStateFlow()

    private var nextId = 1

    fun setFilter(filter: TaskFilter) {
        _uiState.update { it.copy(filter = filter) }
    }

    fun showAddDialog() {
        _uiState.update { it.copy(isAddingTask = true) }
    }

    fun hideAddDialog() {
        _uiState.update {
            it.copy(
                isAddingTask = false,
                newTaskTitle = "",
                newTaskDescription = "",
                newTaskPriority = Priority.MEDIUM
            )
        }
    }

    fun onTitleChange(title: String) {
        _uiState.update { it.copy(newTaskTitle = title) }
    }

    fun onDescriptionChange(description: String) {
        _uiState.update { it.copy(newTaskDescription = description) }
    }

    fun onPriorityChange(priority: Priority) {
        _uiState.update { it.copy(newTaskPriority = priority) }
    }

    fun addTask() {
        val state = _uiState.value
        if (!state.canAddTask) return

        val newTask = Task(
            id = nextId++,
            title = state.newTaskTitle,
            description = state.newTaskDescription,
            completed = false,
            priority = state.newTaskPriority
        )

        _uiState.update {
            it.copy(
                tasks = it.tasks + newTask,
                isAddingTask = false,
                newTaskTitle = "",
                newTaskDescription = "",
                newTaskPriority = Priority.MEDIUM
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

// Screen
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TodoScreen(
    viewModel: TodoViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Mis Tareas") },
                actions = {
                    Text(
                        "${uiState.pendingCount} pendientes",
                        modifier = Modifier.padding(end = 16.dp)
                    )
                }
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = { viewModel.showAddDialog() }) {
                Icon(Icons.Default.Add, "Añadir")
            }
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            // Filter chips
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                TaskFilter.entries.forEach { filter ->
                    FilterChip(
                        selected = uiState.filter == filter,
                        onClick = { viewModel.setFilter(filter) },
                        label = {
                            Text(
                                when (filter) {
                                    TaskFilter.ALL -> "Todas"
                                    TaskFilter.PENDING -> "Pendientes"
                                    TaskFilter.COMPLETED -> "Completadas"
                                }
                            )
                        }
                    )
                }
            }

            // Task list
            if (uiState.filteredTasks.isEmpty()) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text("No hay tareas")
                }
            } else {
                LazyColumn {
                    items(uiState.filteredTasks, key = { it.id }) { task ->
                        TaskItem(
                            task = task,
                            onToggle = { viewModel.toggleTask(task.id) },
                            onDelete = { viewModel.deleteTask(task.id) }
                        )
                    }
                }
            }
        }
    }

    // Add task dialog
    if (uiState.isAddingTask) {
        AddTaskDialog(
            title = uiState.newTaskTitle,
            description = uiState.newTaskDescription,
            priority = uiState.newTaskPriority,
            canAdd = uiState.canAddTask,
            onTitleChange = viewModel::onTitleChange,
            onDescriptionChange = viewModel::onDescriptionChange,
            onPriorityChange = viewModel::onPriorityChange,
            onAdd = viewModel::addTask,
            onDismiss = viewModel::hideAddDialog
        )
    }
}

@Composable
fun TaskItem(
    task: Task,
    onToggle: () -> Unit,
    onDelete: () -> Unit
) {
    val priorityColor = when (task.priority) {
        Priority.HIGH -> Color.Red
        Priority.MEDIUM -> Color(0xFFFFA500)
        Priority.LOW -> Color.Green
    }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp)
    ) {
        Row(
            modifier = Modifier.padding(8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(8.dp)
                    .background(priorityColor, CircleShape)
            )

            Spacer(Modifier.width(8.dp))

            Checkbox(
                checked = task.completed,
                onCheckedChange = { onToggle() }
            )

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = task.title,
                    fontWeight = FontWeight.Bold,
                    textDecoration = if (task.completed) TextDecoration.LineThrough else null
                )
                if (task.description.isNotEmpty()) {
                    Text(
                        text = task.description,
                        fontSize = 12.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }

            IconButton(onClick = onDelete) {
                Icon(Icons.Default.Delete, "Eliminar")
            }
        }
    }
}

@Composable
fun AddTaskDialog(
    title: String,
    description: String,
    priority: Priority,
    canAdd: Boolean,
    onTitleChange: (String) -> Unit,
    onDescriptionChange: (String) -> Unit,
    onPriorityChange: (Priority) -> Unit,
    onAdd: () -> Unit,
    onDismiss: () -> Unit
) {
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Nueva tarea") },
        text = {
            Column {
                OutlinedTextField(
                    value = title,
                    onValueChange = onTitleChange,
                    label = { Text("Título") },
                    modifier = Modifier.fillMaxWidth()
                )

                Spacer(Modifier.height(8.dp))

                OutlinedTextField(
                    value = description,
                    onValueChange = onDescriptionChange,
                    label = { Text("Descripción") },
                    modifier = Modifier.fillMaxWidth()
                )

                Spacer(Modifier.height(16.dp))

                Text("Prioridad:")
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Priority.entries.forEach { p ->
                        FilterChip(
                            selected = priority == p,
                            onClick = { onPriorityChange(p) },
                            label = { Text(p.name) }
                        )
                    }
                }
            }
        },
        confirmButton = {
            Button(onClick = onAdd, enabled = canAdd) {
                Text("Añadir")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancelar")
            }
        }
    )
}
```

---

## Ejercicio 6 (Bonus): Testing de ViewModel

```kotlin
class TodoViewModelTest {

    @Test
    fun `addTask adds task to list`() {
        val viewModel = TodoViewModel()
        
        viewModel.onTitleChange("Nueva tarea")
        viewModel.addTask()
        
        val state = viewModel.uiState.value
        assertEquals(1, state.tasks.size)
        assertEquals("Nueva tarea", state.tasks[0].title)
        assertFalse(state.tasks[0].completed)
    }

    @Test
    fun `addTask with empty title does nothing`() {
        val viewModel = TodoViewModel()
        
        viewModel.addTask()
        
        val state = viewModel.uiState.value
        assertTrue(state.tasks.isEmpty())
    }

    @Test
    fun `toggleTask changes completed status`() {
        val viewModel = TodoViewModel()
        viewModel.onTitleChange("Test")
        viewModel.addTask()
        
        val taskId = viewModel.uiState.value.tasks[0].id
        viewModel.toggleTask(taskId)
        
        assertTrue(viewModel.uiState.value.tasks[0].completed)
        
        viewModel.toggleTask(taskId)
        assertFalse(viewModel.uiState.value.tasks[0].completed)
    }

    @Test
    fun `deleteTask removes task from list`() {
        val viewModel = TodoViewModel()
        viewModel.onTitleChange("Test")
        viewModel.addTask()
        
        val taskId = viewModel.uiState.value.tasks[0].id
        viewModel.deleteTask(taskId)
        
        assertTrue(viewModel.uiState.value.tasks.isEmpty())
    }

    @Test
    fun `filter shows only matching tasks`() {
        val viewModel = TodoViewModel()
        
        // Add pending task
        viewModel.onTitleChange("Pending")
        viewModel.addTask()
        
        // Add completed task
        viewModel.onTitleChange("Completed")
        viewModel.addTask()
        val completedId = viewModel.uiState.value.tasks[1].id
        viewModel.toggleTask(completedId)
        
        // Test ALL filter
        assertEquals(2, viewModel.uiState.value.filteredTasks.size)
        
        // Test PENDING filter
        viewModel.setFilter(TaskFilter.PENDING)
        assertEquals(1, viewModel.uiState.value.filteredTasks.size)
        assertEquals("Pending", viewModel.uiState.value.filteredTasks[0].title)
        
        // Test COMPLETED filter
        viewModel.setFilter(TaskFilter.COMPLETED)
        assertEquals(1, viewModel.uiState.value.filteredTasks.size)
        assertEquals("Completed", viewModel.uiState.value.filteredTasks[0].title)
    }

    @Test
    fun `pendingCount and completedCount are correct`() {
        val viewModel = TodoViewModel()
        
        viewModel.onTitleChange("Task 1")
        viewModel.addTask()
        viewModel.onTitleChange("Task 2")
        viewModel.addTask()
        
        val taskId = viewModel.uiState.value.tasks[0].id
        viewModel.toggleTask(taskId)
        
        assertEquals(1, viewModel.uiState.value.pendingCount)
        assertEquals(1, viewModel.uiState.value.completedCount)
    }
}
```
