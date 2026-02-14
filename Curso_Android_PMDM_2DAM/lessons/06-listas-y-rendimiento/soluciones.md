# Soluciones - Lección 06: Listas y rendimiento

## Ejercicio 1: Lista básica con estados

```kotlin
data class Contact(
    val id: Int,
    val name: String,
    val phone: String
)

sealed class ContactUiState {
    object Loading : ContactUiState()
    data class Success(val contacts: List<Contact>) : ContactUiState()
    data class Error(val message: String) : ContactUiState()
    object Empty : ContactUiState()
}

class ContactViewModel : ViewModel() {
    private val _uiState = MutableStateFlow<ContactUiState>(ContactUiState.Loading)
    val uiState: StateFlow<ContactUiState> = _uiState.asStateFlow()

    private val sampleContacts = listOf(
        Contact(1, "Ana García", "612345678"),
        Contact(2, "Luis Martín", "623456789"),
        Contact(3, "María López", "634567890")
    )

    init {
        loadContacts()
    }

    fun loadContacts() {
        viewModelScope.launch {
            _uiState.value = ContactUiState.Loading
            delay(1500)
            
            // Simular diferentes estados
            _uiState.value = ContactUiState.Success(sampleContacts)
        }
    }
}

@Composable
fun ContactListScreen(viewModel: ContactViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()

    when (val state = uiState) {
        is ContactUiState.Loading -> {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        }
        is ContactUiState.Success -> {
            LazyColumn {
                items(state.contacts, key = { it.id }) { contact ->
                    ContactItem(contact)
                }
            }
        }
        is ContactUiState.Error -> {
            Column(
                Modifier.fillMaxSize(),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Text(state.message, color = MaterialTheme.colorScheme.error)
                Spacer(Modifier.height(16.dp))
                Button(onClick = { viewModel.loadContacts() }) {
                    Text("Reintentar")
                }
            }
        }
        is ContactUiState.Empty -> {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text("No hay contactos")
            }
        }
    }
}

@Composable
fun ContactItem(contact: Contact) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Avatar con inicial
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.primary),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = contact.name.first().uppercase(),
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                    fontSize = 20.sp
                )
            }

            Spacer(Modifier.width(16.dp))

            Column {
                Text(contact.name, fontWeight = FontWeight.Bold)
                Text(contact.phone, fontSize = 14.sp, color = Color.Gray)
            }
        }
    }
}
```

---

## Ejercicio 2: Lista con headers sticky

```kotlin
data class Product(
    val id: Int,
    val name: String,
    val price: Double,
    val inStock: Boolean
)

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun CategorizedProductList() {
    val productosPorCategoria = remember {
        mapOf(
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
    }

    LazyColumn(modifier = Modifier.fillMaxSize()) {
        productosPorCategoria.forEach { (categoria, productos) ->
            stickyHeader {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = MaterialTheme.colorScheme.primaryContainer
                ) {
                    Text(
                        text = categoria,
                        modifier = Modifier.padding(16.dp),
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                }
            }

            items(productos, key = { it.id }) { producto ->
                ProductItem(producto)
            }
        }
    }
}

@Composable
fun ProductItem(product: Product) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (product.inStock) 
                MaterialTheme.colorScheme.surface 
            else 
                MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column {
                Text(
                    text = product.name,
                    fontWeight = FontWeight.Medium,
                    textDecoration = if (!product.inStock) TextDecoration.LineThrough else null
                )
                if (!product.inStock) {
                    Text(
                        "Agotado",
                        fontSize = 12.sp,
                        color = MaterialTheme.colorScheme.error
                    )
                }
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

## Ejercicio 3: Grid de imágenes

```kotlin
@Composable
fun ImageGalleryGrid() {
    val colors = remember {
        listOf(
            Color.Red, Color.Green, Color.Blue,
            Color.Yellow, Color.Cyan, Color.Magenta,
            Color.Gray, Color(0xFFFFA500), Color(0xFF800080),
            Color(0xFF008080), Color(0xFFFFD700), Color(0xFF4B0082)
        )
    }

    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()

    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) { padding ->
        LazyVerticalGrid(
            columns = GridCells.Fixed(3),
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(8.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            itemsIndexed(colors) { index, color ->
                Box(
                    modifier = Modifier
                        .aspectRatio(1f)
                        .clip(RoundedCornerShape(8.dp))
                        .background(color)
                        .clickable {
                            scope.launch {
                                snackbarHostState.showSnackbar("Imagen ${index + 1}")
                            }
                        }
                )
            }
        }
    }
}
```

---

## Ejercicio 4: Pull to Refresh

```kotlin
data class News(
    val id: Int,
    val title: String,
    val date: String,
    val summary: String
)

data class NewsUiState(
    val news: List<News> = emptyList(),
    val isRefreshing: Boolean = false
)

class NewsViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(NewsUiState())
    val uiState: StateFlow<NewsUiState> = _uiState.asStateFlow()

    private var nextId = 1

    init {
        loadNews()
    }

    private fun loadNews() {
        viewModelScope.launch {
            _uiState.update { it.copy(isRefreshing = true) }
            delay(1000)
            
            val initialNews = (1..5).map { id ->
                News(
                    id = nextId++,
                    title = "Noticia $id",
                    date = "01/02/2026",
                    summary = "Resumen de la noticia $id"
                )
            }
            _uiState.update { it.copy(news = initialNews, isRefreshing = false) }
        }
    }

    fun refresh() {
        viewModelScope.launch {
            _uiState.update { it.copy(isRefreshing = true) }
            delay(2000)
            
            val newNews = News(
                id = nextId++,
                title = "Nueva noticia ${nextId - 1}",
                date = "01/02/2026",
                summary = "Contenido actualizado"
            )
            
            _uiState.update { state ->
                state.copy(
                    news = listOf(newNews) + state.news,
                    isRefreshing = false
                )
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NewsListScreen(viewModel: NewsViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()

    PullToRefreshBox(
        isRefreshing = uiState.isRefreshing,
        onRefresh = { viewModel.refresh() }
    ) {
        LazyColumn(modifier = Modifier.fillMaxSize()) {
            items(uiState.news, key = { it.id }) { news ->
                NewsItem(news)
            }
        }
    }
}

@Composable
fun NewsItem(news: News) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(news.title, fontWeight = FontWeight.Bold)
            Text(news.date, fontSize = 12.sp, color = Color.Gray)
            Spacer(Modifier.height(8.dp))
            Text(news.summary)
        }
    }
}
```

---

## Ejercicio 5: Scroll y FAB

```kotlin
@Composable
fun ScrollableListWithFab() {
    val items = remember { (1..100).map { "Item $it" } }
    val listState = rememberLazyListState()
    val coroutineScope = rememberCoroutineScope()

    val showScrollToTop by remember {
        derivedStateOf { listState.firstVisibleItemIndex > 5 }
    }

    Box(modifier = Modifier.fillMaxSize()) {
        LazyColumn(
            state = listState,
            modifier = Modifier.fillMaxSize()
        ) {
            items(items.size) { index ->
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(8.dp)
                ) {
                    Text(
                        text = items[index],
                        modifier = Modifier.padding(16.dp)
                    )
                }
            }
        }

        AnimatedVisibility(
            visible = showScrollToTop,
            enter = slideInVertically(initialOffsetY = { it }) + fadeIn(),
            exit = slideOutVertically(targetOffsetY = { it }) + fadeOut(),
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(16.dp)
        ) {
            FloatingActionButton(
                onClick = {
                    coroutineScope.launch {
                        listState.animateScrollToItem(0)
                    }
                }
            ) {
                Icon(Icons.Default.KeyboardArrowUp, "Ir arriba")
            }
        }
    }
}
```

---

## Ejercicio 6: Paginación infinita

```kotlin
data class PaginatedItem(val id: Int, val title: String)

data class PaginatedUiState(
    val items: List<PaginatedItem> = emptyList(),
    val isLoading: Boolean = false,
    val isLoadingMore: Boolean = false,
    val hasMore: Boolean = true
)

class PaginatedViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(PaginatedUiState())
    val uiState: StateFlow<PaginatedUiState> = _uiState.asStateFlow()

    private var nextId = 1
    private val maxItems = 100
    private val pageSize = 10

    init {
        loadInitial()
    }

    private fun loadInitial() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            delay(1000)
            
            val initialItems = (1..20).map {
                PaginatedItem(nextId++, "Item ${nextId - 1}")
            }
            
            _uiState.update {
                it.copy(
                    items = initialItems,
                    isLoading = false,
                    hasMore = initialItems.size < maxItems
                )
            }
        }
    }

    fun loadMore() {
        val currentState = _uiState.value
        if (currentState.isLoadingMore || !currentState.hasMore) return

        viewModelScope.launch {
            _uiState.update { it.copy(isLoadingMore = true) }
            delay(1500)
            
            val newItems = (1..pageSize).map {
                PaginatedItem(nextId++, "Item ${nextId - 1}")
            }
            
            val allItems = currentState.items + newItems
            
            _uiState.update {
                it.copy(
                    items = allItems,
                    isLoadingMore = false,
                    hasMore = allItems.size < maxItems
                )
            }
        }
    }
}

@Composable
fun PaginatedListScreen(viewModel: PaginatedViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    val listState = rememberLazyListState()

    val shouldLoadMore by remember {
        derivedStateOf {
            val lastVisibleItem = listState.layoutInfo.visibleItemsInfo.lastOrNull()
            lastVisibleItem != null &&
            lastVisibleItem.index >= listState.layoutInfo.totalItemsCount - 5 &&
            !uiState.isLoadingMore &&
            uiState.hasMore
        }
    }

    LaunchedEffect(shouldLoadMore) {
        if (shouldLoadMore) {
            viewModel.loadMore()
        }
    }

    if (uiState.isLoading) {
        Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator()
        }
    } else {
        LazyColumn(
            state = listState,
            modifier = Modifier.fillMaxSize()
        ) {
            items(uiState.items, key = { it.id }) { item ->
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(8.dp)
                ) {
                    Text(item.title, modifier = Modifier.padding(16.dp))
                }
            }

            if (uiState.isLoadingMore) {
                item {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        CircularProgressIndicator()
                    }
                }
            }

            if (!uiState.hasMore) {
                item {
                    Text(
                        "No hay más elementos",
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        textAlign = TextAlign.Center,
                        color = Color.Gray
                    )
                }
            }
        }
    }
}
```
