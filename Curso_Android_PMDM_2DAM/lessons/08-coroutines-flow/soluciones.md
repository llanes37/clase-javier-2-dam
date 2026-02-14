# Soluciones - Lección 08: Coroutines y Flow

## Ejercicio 1: Cargas paralelas

```kotlin
data class DashboardUiState(
    val usersState: SectionState<List<User>> = SectionState.Loading,
    val postsState: SectionState<List<Post>> = SectionState.Loading,
    val statsState: SectionState<Stats> = SectionState.Loading
)

sealed class SectionState<out T> {
    object Loading : SectionState<Nothing>()
    data class Success<T>(val data: T) : SectionState<T>()
    data class Error(val message: String) : SectionState<Nothing>()
}

class DashboardViewModel : ViewModel() {
    
    private val _uiState = MutableStateFlow(DashboardUiState())
    val uiState: StateFlow<DashboardUiState> = _uiState.asStateFlow()
    
    init {
        loadDashboard()
    }
    
    fun loadDashboard() {
        // Resetear estados
        _uiState.value = DashboardUiState()
        
        viewModelScope.launch {
            // Lanzar las 3 cargas en paralelo
            val usersJob = async { loadUsers() }
            val postsJob = async { loadPosts() }
            val statsJob = async { loadStats() }
            
            // No necesitamos await aquí porque cada uno actualiza su estado
        }
    }
    
    private suspend fun loadUsers() {
        try {
            delay(1500) // Simular red
            val users = listOf(User(1, "Ana"), User(2, "Luis"))
            _uiState.update { it.copy(usersState = SectionState.Success(users)) }
        } catch (e: Exception) {
            _uiState.update { it.copy(usersState = SectionState.Error(e.message ?: "Error")) }
        }
    }
    
    private suspend fun loadPosts() {
        try {
            delay(2000)
            val posts = listOf(Post(1, "Título 1"), Post(2, "Título 2"))
            _uiState.update { it.copy(postsState = SectionState.Success(posts)) }
        } catch (e: Exception) {
            _uiState.update { it.copy(postsState = SectionState.Error(e.message ?: "Error")) }
        }
    }
    
    private suspend fun loadStats() {
        try {
            delay(1000)
            val stats = Stats(users = 100, posts = 500)
            _uiState.update { it.copy(statsState = SectionState.Success(stats)) }
        } catch (e: Exception) {
            _uiState.update { it.copy(statsState = SectionState.Error(e.message ?: "Error")) }
        }
    }
}

@Composable
fun DashboardScreen(viewModel: DashboardViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    
    LazyColumn(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        item {
            Text("Dashboard", style = MaterialTheme.typography.headlineMedium)
            Spacer(Modifier.height(16.dp))
        }
        
        item { SectionCard("Usuarios", uiState.usersState) { users ->
            users.forEach { Text(it.name) }
        }}
        
        item { SectionCard("Posts", uiState.postsState) { posts ->
            posts.forEach { Text(it.title) }
        }}
        
        item { SectionCard("Estadísticas", uiState.statsState) { stats ->
            Text("Usuarios: ${stats.users}")
            Text("Posts: ${stats.posts}")
        }}
    }
}

@Composable
fun <T> SectionCard(
    title: String,
    state: SectionState<T>,
    content: @Composable (T) -> Unit
) {
    Card(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(title, fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(8.dp))
            
            when (state) {
                is SectionState.Loading -> CircularProgressIndicator(Modifier.size(24.dp))
                is SectionState.Error -> Text(state.message, color = Color.Red)
                is SectionState.Success -> content(state.data)
            }
        }
    }
}
```

---

## Ejercicio 2: Contador con Flow

```kotlin
class CounterViewModel : ViewModel() {
    
    private val _isPaused = MutableStateFlow(false)
    private val _counter = MutableStateFlow(0)
    
    val counter: StateFlow<Int> = _counter.asStateFlow()
    val isPaused: StateFlow<Boolean> = _isPaused.asStateFlow()
    
    private var timerJob: Job? = null
    
    init {
        startTimer()
    }
    
    private fun startTimer() {
        timerJob = viewModelScope.launch {
            while (_counter.value < 3600) {  // Max 1 hora
                if (!_isPaused.value) {
                    delay(1000)
                    _counter.value++
                } else {
                    delay(100)  // Esperar mientras está pausado
                }
            }
        }
    }
    
    fun togglePause() {
        _isPaused.value = !_isPaused.value
    }
    
    fun reset() {
        _counter.value = 0
    }
}

@Composable
fun CounterScreen(viewModel: CounterViewModel = viewModel()) {
    val counter by viewModel.counter.collectAsState()
    val isPaused by viewModel.isPaused.collectAsState()
    
    val minutes = counter / 60
    val seconds = counter % 60
    val timeFormatted = "%02d:%02d".format(minutes, seconds)
    
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = timeFormatted,
            style = MaterialTheme.typography.displayLarge,
            fontFamily = FontFamily.Monospace
        )
        
        Spacer(Modifier.height(32.dp))
        
        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            Button(onClick = { viewModel.togglePause() }) {
                Text(if (isPaused) "Reanudar" else "Pausar")
            }
            
            OutlinedButton(onClick = { viewModel.reset() }) {
                Text("Reiniciar")
            }
        }
    }
}
```

---

## Ejercicio 3: Búsqueda con debounce

```kotlin
data class SearchUiState(
    val query: String = "",
    val results: List<String> = emptyList(),
    val isSearching: Boolean = false,
    val hasSearched: Boolean = false
)

class SearchViewModel : ViewModel() {
    
    private val _searchQuery = MutableStateFlow("")
    
    private val _uiState = MutableStateFlow(SearchUiState())
    val uiState: StateFlow<SearchUiState> = _uiState.asStateFlow()
    
    init {
        viewModelScope.launch {
            _searchQuery
                .debounce(500)
                .distinctUntilChanged()
                .flatMapLatest { query ->
                    if (query.isBlank()) {
                        flowOf(SearchUiState())
                    } else {
                        flow {
                            emit(SearchUiState(query = query, isSearching = true))
                            val results = searchProducts(query)
                            emit(SearchUiState(
                                query = query,
                                results = results,
                                hasSearched = true
                            ))
                        }
                    }
                }
                .collect { state ->
                    _uiState.value = state
                }
        }
    }
    
    fun onQueryChange(query: String) {
        _searchQuery.value = query
        _uiState.update { it.copy(query = query) }
    }
    
    private suspend fun searchProducts(query: String): List<String> {
        delay(1000)
        return listOf("Laptop", "Mouse", "Teclado", "Monitor", "Webcam", "Auriculares")
            .filter { it.contains(query, ignoreCase = true) }
    }
}

@Composable
fun SearchScreen(viewModel: SearchViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        OutlinedTextField(
            value = uiState.query,
            onValueChange = viewModel::onQueryChange,
            label = { Text("Buscar productos") },
            modifier = Modifier.fillMaxWidth(),
            leadingIcon = { Icon(Icons.Default.Search, null) }
        )
        
        Spacer(Modifier.height(16.dp))
        
        when {
            uiState.isSearching -> {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    CircularProgressIndicator(Modifier.size(20.dp))
                    Spacer(Modifier.width(8.dp))
                    Text("Buscando...")
                }
            }
            uiState.hasSearched && uiState.results.isEmpty() -> {
                Text("Sin resultados para '${uiState.query}'")
            }
            uiState.results.isNotEmpty() -> {
                LazyColumn {
                    items(uiState.results) { result ->
                        Card(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                            Text(result, modifier = Modifier.padding(16.dp))
                        }
                    }
                }
            }
        }
    }
}
```

---

## Ejercicio 4: Combine de filtros

```kotlin
data class Product(
    val id: Int,
    val name: String,
    val category: String,
    val price: Double
)

data class FilterUiState(
    val query: String = "",
    val category: String = "Todos",
    val minPrice: Float = 0f,
    val maxPrice: Float = 1000f,
    val products: List<Product> = emptyList()
)

class FilterViewModel : ViewModel() {
    
    private val allProducts = listOf(
        Product(1, "Laptop", "Electrónica", 999.0),
        Product(2, "Mouse", "Electrónica", 29.0),
        Product(3, "Camiseta", "Ropa", 19.0),
        Product(4, "Pantalón", "Ropa", 49.0),
        Product(5, "Lámpara", "Hogar", 39.0),
        Product(6, "Monitor", "Electrónica", 299.0)
    )
    
    private val _query = MutableStateFlow("")
    private val _category = MutableStateFlow("Todos")
    private val _priceRange = MutableStateFlow(0f..1000f)
    
    val categories = listOf("Todos", "Electrónica", "Ropa", "Hogar")
    
    val uiState: StateFlow<FilterUiState> = combine(
        _query,
        _category,
        _priceRange
    ) { query, category, priceRange ->
        val filtered = allProducts.filter { product ->
            val matchesQuery = query.isBlank() || 
                product.name.contains(query, ignoreCase = true)
            val matchesCategory = category == "Todos" || 
                product.category == category
            val matchesPrice = product.price >= priceRange.start && 
                product.price <= priceRange.endInclusive
            
            matchesQuery && matchesCategory && matchesPrice
        }
        
        FilterUiState(
            query = query,
            category = category,
            minPrice = priceRange.start,
            maxPrice = priceRange.endInclusive,
            products = filtered
        )
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = FilterUiState(products = allProducts)
    )
    
    fun onQueryChange(query: String) { _query.value = query }
    fun onCategoryChange(category: String) { _category.value = category }
    fun onPriceRangeChange(range: ClosedFloatingPointRange<Float>) { 
        _priceRange.value = range 
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FilterScreen(viewModel: FilterViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        OutlinedTextField(
            value = uiState.query,
            onValueChange = viewModel::onQueryChange,
            label = { Text("Buscar") },
            modifier = Modifier.fillMaxWidth()
        )
        
        Spacer(Modifier.height(16.dp))
        
        Text("Categoría")
        LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            items(viewModel.categories) { cat ->
                FilterChip(
                    selected = uiState.category == cat,
                    onClick = { viewModel.onCategoryChange(cat) },
                    label = { Text(cat) }
                )
            }
        }
        
        Spacer(Modifier.height(16.dp))
        
        Text("Precio: ${uiState.minPrice.toInt()}€ - ${uiState.maxPrice.toInt()}€")
        RangeSlider(
            value = uiState.minPrice..uiState.maxPrice,
            onValueChange = viewModel::onPriceRangeChange,
            valueRange = 0f..1000f
        )
        
        Spacer(Modifier.height(16.dp))
        
        Text("${uiState.products.size} productos")
        
        LazyColumn {
            items(uiState.products, key = { it.id }) { product ->
                Card(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Column {
                            Text(product.name, fontWeight = FontWeight.Bold)
                            Text(product.category, fontSize = 12.sp)
                        }
                        Text("${product.price}€")
                    }
                }
            }
        }
    }
}
```

---

## Ejercicio 5: Eventos con SharedFlow

```kotlin
sealed class UiEvent {
    data class ShowSnackbar(val message: String) : UiEvent()
    data class Navigate(val route: String) : UiEvent()
    object ShowDialog : UiEvent()
}

class EventViewModel : ViewModel() {
    
    private val _events = MutableSharedFlow<UiEvent>()
    val events: SharedFlow<UiEvent> = _events.asSharedFlow()
    
    fun saveItem() {
        viewModelScope.launch {
            // Simular guardado
            delay(500)
            _events.emit(UiEvent.ShowSnackbar("Item guardado correctamente"))
        }
    }
    
    fun deleteItem() {
        viewModelScope.launch {
            _events.emit(UiEvent.ShowDialog)
        }
    }
    
    fun confirmDelete() {
        viewModelScope.launch {
            delay(500)
            _events.emit(UiEvent.ShowSnackbar("Item eliminado"))
            _events.emit(UiEvent.Navigate("home"))
        }
    }
}

@Composable
fun EventScreen(
    viewModel: EventViewModel = viewModel(),
    onNavigate: (String) -> Unit
) {
    val snackbarHostState = remember { SnackbarHostState() }
    var showDialog by remember { mutableStateOf(false) }
    
    LaunchedEffect(Unit) {
        viewModel.events.collect { event ->
            when (event) {
                is UiEvent.ShowSnackbar -> {
                    snackbarHostState.showSnackbar(event.message)
                }
                is UiEvent.Navigate -> {
                    onNavigate(event.route)
                }
                UiEvent.ShowDialog -> {
                    showDialog = true
                }
            }
        }
    }
    
    if (showDialog) {
        AlertDialog(
            onDismissRequest = { showDialog = false },
            title = { Text("Confirmar") },
            text = { Text("¿Eliminar este item?") },
            confirmButton = {
                Button(onClick = {
                    showDialog = false
                    viewModel.confirmDelete()
                }) {
                    Text("Eliminar")
                }
            },
            dismissButton = {
                TextButton(onClick = { showDialog = false }) {
                    Text("Cancelar")
                }
            }
        )
    }
    
    Scaffold(snackbarHost = { SnackbarHost(snackbarHostState) }) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.Center
        ) {
            Button(
                onClick = { viewModel.saveItem() },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Guardar")
            }
            
            Spacer(Modifier.height(16.dp))
            
            OutlinedButton(
                onClick = { viewModel.deleteItem() },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Eliminar")
            }
        }
    }
}
```
