# Lección 08: Coroutines y Flow

## Objetivos

- Entender coroutines y scopes
- Usar Flow para streams reactivos
- Implementar StateFlow y SharedFlow
- Manejar cancelación y errores
- Combinar y transformar Flows

---

## 1. Coroutines básicas

### ¿Qué son las coroutines?

Código asíncrono que parece síncrono. Permiten operaciones no bloqueantes sin callbacks.

```kotlin
// ❌ Bloqueante - congela la UI
fun loadData() {
    val data = networkCall()  // Bloquea hasta completar
    showData(data)
}

// ✅ Con coroutines - no bloquea
suspend fun loadData() {
    val data = networkCall()  // Suspende, no bloquea
    showData(data)
}
```

### Lanzar coroutines

```kotlin
// En ViewModel
viewModelScope.launch {
    // Código asíncrono aquí
    val users = repository.getUsers()
    _uiState.value = users
}
```

### Scopes principales

| Scope | Uso | Ciclo de vida |
|-------|-----|---------------|
| `viewModelScope` | ViewModels | Hasta que ViewModel se destruya |
| `lifecycleScope` | Activities/Fragments | Hasta que se destruyan |
| `rememberCoroutineScope` | Composables | Hasta que salgan de composición |
| `GlobalScope` | ❌ Evitar | Nunca se cancela |

---

## 2. Dispatchers

Determinan en qué hilo se ejecuta la coroutine:

```kotlin
viewModelScope.launch(Dispatchers.Main) {
    // Hilo principal - actualizar UI
}

viewModelScope.launch(Dispatchers.IO) {
    // Hilo I/O - red, base de datos
}

viewModelScope.launch(Dispatchers.Default) {
    // Hilo CPU - cálculos pesados
}
```

### Cambiar de dispatcher

```kotlin
viewModelScope.launch {
    // En Main por defecto
    
    val data = withContext(Dispatchers.IO) {
        // Cambiar a IO para llamada de red
        api.getData()
    }
    
    // Volver a Main automáticamente
    _uiState.value = data
}
```

---

## 3. suspend functions

Funciones que pueden suspenderse:

```kotlin
suspend fun getUsers(): List<User> {
    return withContext(Dispatchers.IO) {
        api.getUsers()
    }
}

suspend fun loadUserWithPosts(userId: Int): UserWithPosts {
    return coroutineScope {
        // Ejecutar en paralelo
        val userDeferred = async { api.getUser(userId) }
        val postsDeferred = async { api.getPosts(userId) }
        
        UserWithPosts(
            user = userDeferred.await(),
            posts = postsDeferred.await()
        )
    }
}
```

---

## 4. Flow básico

Flow emite múltiples valores a lo largo del tiempo:

```kotlin
// Crear un Flow
fun countFlow(): Flow<Int> = flow {
    for (i in 1..10) {
        delay(1000)
        emit(i)  // Emitir valor
    }
}

// Recolectar valores
viewModelScope.launch {
    countFlow().collect { value ->
        println("Recibido: $value")
    }
}
```

### Flow vs suspend function

```kotlin
// suspend fun: un solo valor
suspend fun getUser(): User

// Flow: múltiples valores en el tiempo
fun observeUser(): Flow<User>
```

---

## 5. StateFlow

Flow especial para estado de UI:

```kotlin
class UserViewModel : ViewModel() {
    
    // Estado mutable privado
    private val _uiState = MutableStateFlow(UserUiState())
    
    // Exposición pública inmutable
    val uiState: StateFlow<UserUiState> = _uiState.asStateFlow()
    
    fun loadUsers() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            
            val users = repository.getUsers()
            
            _uiState.update { it.copy(users = users, isLoading = false) }
        }
    }
}
```

### En Compose

```kotlin
@Composable
fun UserScreen(viewModel: UserViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    
    // La UI se recompone cuando uiState cambia
}
```

### Características de StateFlow

- Siempre tiene un valor (requiere valor inicial)
- Solo emite si el valor cambia (distintos)
- Hot flow (emite aunque no haya colectores)

---

## 6. SharedFlow

Para eventos que no deben perderse:

```kotlin
class UserViewModel : ViewModel() {
    
    private val _events = MutableSharedFlow<UiEvent>()
    val events: SharedFlow<UiEvent> = _events.asSharedFlow()
    
    fun saveUser() {
        viewModelScope.launch {
            repository.saveUser()
            _events.emit(UiEvent.ShowSnackbar("Usuario guardado"))
        }
    }
}

sealed class UiEvent {
    data class ShowSnackbar(val message: String) : UiEvent()
    object NavigateBack : UiEvent()
}
```

### Recolectar en Compose

```kotlin
@Composable
fun UserScreen(viewModel: UserViewModel = viewModel()) {
    val snackbarHostState = remember { SnackbarHostState() }
    
    LaunchedEffect(Unit) {
        viewModel.events.collect { event ->
            when (event) {
                is UiEvent.ShowSnackbar -> {
                    snackbarHostState.showSnackbar(event.message)
                }
                UiEvent.NavigateBack -> {
                    // Navegar
                }
            }
        }
    }
}
```

---

## 7. Operadores de Flow

### map - Transformar valores

```kotlin
repository.observeUsers()
    .map { users -> users.filter { it.isActive } }
    .collect { activeUsers -> /* ... */ }
```

### filter - Filtrar valores

```kotlin
repository.observePrices()
    .filter { it > 0 }
    .collect { price -> /* ... */ }
```

### combine - Combinar Flows

```kotlin
val searchQuery = MutableStateFlow("")
val category = MutableStateFlow("all")

val filteredProducts = combine(
    searchQuery,
    category,
    repository.observeProducts()
) { query, cat, products ->
    products.filter { product ->
        product.name.contains(query, ignoreCase = true) &&
        (cat == "all" || product.category == cat)
    }
}
```

### flatMapLatest - Cancelar anterior

```kotlin
searchQuery
    .debounce(300)
    .flatMapLatest { query ->
        repository.search(query)  // Cancela búsqueda anterior
    }
    .collect { results -> /* ... */ }
```

### debounce - Esperar antes de emitir

```kotlin
searchQuery
    .debounce(500)  // Esperar 500ms sin cambios
    .collect { query ->
        performSearch(query)
    }
```

### distinctUntilChanged - Solo si cambia

```kotlin
_uiState
    .map { it.selectedItem }
    .distinctUntilChanged()  // Solo si selectedItem cambia
    .collect { item -> /* ... */ }
```

---

## 8. Manejo de errores

### catch operator

```kotlin
repository.observeData()
    .catch { e ->
        emit(emptyList())  // Valor por defecto
        // o: throw e para propagar
    }
    .collect { data -> /* ... */ }
```

### try-catch en collect

```kotlin
viewModelScope.launch {
    try {
        repository.observeData().collect { data ->
            _uiState.value = data
        }
    } catch (e: Exception) {
        _uiState.update { it.copy(error = e.message) }
    }
}
```

### onEach para side effects

```kotlin
repository.observeData()
    .onEach { Log.d("TAG", "Recibido: $it") }
    .catch { Log.e("TAG", "Error", it) }
    .collect { /* ... */ }
```

---

## 9. stateIn y shareIn

### stateIn - Convertir Flow a StateFlow

```kotlin
class UserRepository {
    fun observeUsers(): Flow<List<User>> = /* ... */
}

class UserViewModel(repository: UserRepository) : ViewModel() {
    
    val users: StateFlow<List<User>> = repository.observeUsers()
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )
}
```

### SharingStarted opciones

| Opción | Comportamiento |
|--------|----------------|
| `Eagerly` | Empieza inmediatamente |
| `Lazily` | Empieza con el primer colector |
| `WhileSubscribed(ms)` | Para cuando no hay colectores (con delay) |

---

## 10. Cancelación

Las coroutines se cancelan automáticamente:

```kotlin
// En ViewModel
override fun onCleared() {
    super.onCleared()
    // viewModelScope se cancela automáticamente
}

// Cancelación manual
val job = viewModelScope.launch {
    // trabajo...
}

job.cancel()  // Cancelar
```

### Verificar cancelación

```kotlin
suspend fun heavyWork() {
    for (i in 1..1000) {
        ensureActive()  // Lanza si está cancelado
        // o: yield()   // Permite cancelación
        processItem(i)
    }
}
```

---

## Ejemplo completo

```kotlin
data class SearchUiState(
    val query: String = "",
    val results: List<Product> = emptyList(),
    val isSearching: Boolean = false
)

class SearchViewModel(
    private val repository: ProductRepository
) : ViewModel() {
    
    private val _searchQuery = MutableStateFlow("")
    
    val uiState: StateFlow<SearchUiState> = _searchQuery
        .debounce(300)
        .flatMapLatest { query ->
            if (query.isBlank()) {
                flowOf(SearchUiState())
            } else {
                flow {
                    emit(SearchUiState(query = query, isSearching = true))
                    val results = repository.search(query)
                    emit(SearchUiState(query = query, results = results))
                }
            }
        }
        .catch { e ->
            emit(SearchUiState(query = _searchQuery.value))
        }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = SearchUiState()
        )
    
    fun onQueryChange(query: String) {
        _searchQuery.value = query
    }
}
```

---

## Resumen

| Concepto | Uso |
|----------|-----|
| `suspend` | Función que puede pausarse |
| `viewModelScope.launch` | Lanzar coroutine en ViewModel |
| `withContext` | Cambiar dispatcher |
| `async/await` | Ejecución paralela |
| `Flow` | Stream de valores |
| `StateFlow` | Estado reactivo |
| `SharedFlow` | Eventos one-shot |
| `collect` | Recoger valores del flow |
| `combine` | Combinar múltiples flows |
| `stateIn` | Convertir Flow a StateFlow |

---

## Siguiente paso

→ [ejercicios.md](ejercicios.md)
