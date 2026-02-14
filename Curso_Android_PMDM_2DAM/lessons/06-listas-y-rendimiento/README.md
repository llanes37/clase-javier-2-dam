# Lección 06: Listas y rendimiento

## Objetivos

- Implementar listas eficientes con LazyColumn
- Entender y usar keys correctamente
- Optimizar recomposiciones
- Implementar pull-to-refresh
- Manejar estados de lista vacía y carga

---

## 1. LazyColumn vs Column

### Column (para pocas items)

```kotlin
// ❌ Malo para listas grandes - renderiza todo
Column {
    items.forEach { item ->
        ItemCard(item)
    }
}
```

### LazyColumn (para listas)

```kotlin
// ✅ Bueno - solo renderiza lo visible
LazyColumn {
    items(items) { item ->
        ItemCard(item)
    }
}
```

**LazyColumn:**
- Solo compone items visibles
- Recicla composables al hacer scroll
- Equivalente a RecyclerView

---

## 2. Sintaxis de LazyColumn

### items básico

```kotlin
LazyColumn {
    items(productos) { producto ->
        ProductoCard(producto)
    }
}
```

### Con índice

```kotlin
LazyColumn {
    itemsIndexed(productos) { index, producto ->
        Text("$index: ${producto.nombre}")
    }
}
```

### Items individuales

```kotlin
LazyColumn {
    item {
        Text("Header", style = MaterialTheme.typography.headlineMedium)
    }

    items(productos) { producto ->
        ProductoCard(producto)
    }

    item {
        Text("Footer")
    }
}
```

### Secciones con headers

```kotlin
LazyColumn {
    productosPorCategoria.forEach { (categoria, productos) ->
        stickyHeader {
            Text(
                categoria,
                modifier = Modifier
                    .fillMaxWidth()
                    .background(MaterialTheme.colorScheme.surface)
                    .padding(16.dp)
            )
        }

        items(productos) { producto ->
            ProductoCard(producto)
        }
    }
}
```

---

## 3. Keys: Por qué son importantes

### Sin key (problema)

```kotlin
LazyColumn {
    items(items) { item ->  // ❌ Sin key
        ItemCard(item)
    }
}
```

Cuando la lista cambia, Compose no sabe qué items son los mismos.

### Con key (correcto)

```kotlin
LazyColumn {
    items(
        items = items,
        key = { it.id }  // ✅ Identifica cada item
    ) { item ->
        ItemCard(item)
    }
}
```

**Beneficios de usar key:**
- Compose sabe qué items añadir/eliminar/mover
- El estado de cada item se preserva
- Animaciones funcionan correctamente
- Mejor rendimiento

### Regla: siempre usa key con un ID único

```kotlin
// Con data class que tiene id
items(users, key = { it.id }) { user -> ... }

// Con índice como fallback (menos ideal)
itemsIndexed(items) { index, item ->
    key(item.hashCode()) {
        ItemCard(item)
    }
}
```

---

## 4. LazyRow

Para listas horizontales:

```kotlin
LazyRow(
    contentPadding = PaddingValues(horizontal = 16.dp),
    horizontalArrangement = Arrangement.spacedBy(8.dp)
) {
    items(categorias, key = { it.id }) { categoria ->
        CategoriaChip(categoria)
    }
}
```

---

## 5. LazyVerticalGrid

Para grids:

```kotlin
LazyVerticalGrid(
    columns = GridCells.Fixed(2),  // 2 columnas
    contentPadding = PaddingValues(16.dp),
    horizontalArrangement = Arrangement.spacedBy(8.dp),
    verticalArrangement = Arrangement.spacedBy(8.dp)
) {
    items(productos, key = { it.id }) { producto ->
        ProductoGridItem(producto)
    }
}

// Columnas adaptativas (mínimo 150dp por columna)
LazyVerticalGrid(
    columns = GridCells.Adaptive(minSize = 150.dp)
) {
    // ...
}
```

---

## 6. Optimizar recomposiciones

### Problema: recomposiciones innecesarias

```kotlin
@Composable
fun ProductList(products: List<Product>) {
    LazyColumn {
        items(products, key = { it.id }) { product ->
            // Se recompone TODA la lista cuando cambia algo
            ProductCard(
                product = product,
                onClick = { /* ... */ }
            )
        }
    }
}
```

### Solución 1: Pasar datos primitivos

```kotlin
@Composable
fun ProductCard(
    name: String,
    price: Double,
    onClick: () -> Unit
) {
    // Solo se recompone si name o price cambian
    Card(onClick = onClick) {
        Text(name)
        Text("$price €")
    }
}

// Uso
items(products, key = { it.id }) { product ->
    ProductCard(
        name = product.name,
        price = product.price,
        onClick = { onProductClick(product.id) }
    )
}
```

### Solución 2: Clases estables

```kotlin
// ✅ Data class es estable por defecto
data class Product(
    val id: Int,
    val name: String,
    val price: Double
)

// ❌ List no es estable - considera usar ImmutableList de kotlinx
data class CartState(
    val items: List<CartItem>  // Causa recomposiciones
)

// ✅ Mejor con wrapper estable
@Immutable
data class CartState(
    val items: ImmutableList<CartItem>
)
```

### Solución 3: remember con keys

```kotlin
@Composable
fun ProductCard(product: Product, onClick: () -> Unit) {
    // Memoriza el callback para evitar recomposición
    val memoizedOnClick = remember(product.id) {
        { onClick() }
    }

    Card(onClick = memoizedOnClick) {
        // ...
    }
}
```

---

## 7. Pull to Refresh

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProductListScreen(
    viewModel: ProductViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    val pullRefreshState = rememberPullToRefreshState()

    PullToRefreshBox(
        isRefreshing = uiState.isRefreshing,
        onRefresh = { viewModel.refresh() },
        state = pullRefreshState
    ) {
        LazyColumn(modifier = Modifier.fillMaxSize()) {
            items(uiState.products, key = { it.id }) { product ->
                ProductCard(product)
            }
        }
    }
}
```

### ViewModel para Pull to Refresh

```kotlin
class ProductViewModel : ViewModel() {

    private val _uiState = MutableStateFlow(ProductUiState())
    val uiState: StateFlow<ProductUiState> = _uiState.asStateFlow()

    fun refresh() {
        viewModelScope.launch {
            _uiState.update { it.copy(isRefreshing = true) }
            
            try {
                val products = repository.getProducts()
                _uiState.update { 
                    it.copy(products = products, isRefreshing = false) 
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isRefreshing = false) }
            }
        }
    }
}

data class ProductUiState(
    val products: List<Product> = emptyList(),
    val isRefreshing: Boolean = false
)
```

---

## 8. Estados de lista

### Componente reutilizable

```kotlin
@Composable
fun <T> StatefulList(
    items: List<T>,
    isLoading: Boolean,
    error: String?,
    emptyMessage: String = "No hay elementos",
    onRetry: () -> Unit,
    itemContent: @Composable (T) -> Unit
) {
    when {
        isLoading && items.isEmpty() -> {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        }
        error != null && items.isEmpty() -> {
            Column(
                Modifier.fillMaxSize(),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Text(error, color = MaterialTheme.colorScheme.error)
                Spacer(Modifier.height(16.dp))
                Button(onClick = onRetry) {
                    Text("Reintentar")
                }
            }
        }
        items.isEmpty() -> {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(emptyMessage)
            }
        }
        else -> {
            LazyColumn {
                items(items) { item ->
                    itemContent(item)
                }
            }
        }
    }
}
```

### Uso

```kotlin
@Composable
fun ProductScreen(viewModel: ProductViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()

    StatefulList(
        items = uiState.products,
        isLoading = uiState.isLoading,
        error = uiState.error,
        emptyMessage = "No hay productos disponibles",
        onRetry = { viewModel.loadProducts() }
    ) { product ->
        ProductCard(product)
    }
}
```

---

## 9. Scroll state y posición

### Detectar scroll

```kotlin
@Composable
fun ProductList(products: List<Product>) {
    val listState = rememberLazyListState()

    // ¿El usuario ha hecho scroll?
    val showScrollToTop by remember {
        derivedStateOf { listState.firstVisibleItemIndex > 0 }
    }

    Box {
        LazyColumn(state = listState) {
            items(products, key = { it.id }) { product ->
                ProductCard(product)
            }
        }

        // Botón "volver arriba"
        AnimatedVisibility(
            visible = showScrollToTop,
            modifier = Modifier.align(Alignment.BottomEnd).padding(16.dp)
        ) {
            FloatingActionButton(
                onClick = {
                    // Scroll al inicio
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

### Guardar posición del scroll

```kotlin
@Composable
fun ProductList(
    products: List<Product>,
    listState: LazyListState = rememberLazyListState()
) {
    LazyColumn(state = listState) {
        items(products, key = { it.id }) { product ->
            ProductCard(product)
        }
    }
}

// En el padre, mantener el estado
@Composable
fun ProductScreen() {
    val listState = rememberLazyListState()
    
    // listState sobrevive a recomposiciones
    ProductList(products = products, listState = listState)
}
```

---

## 10. Paginación básica

```kotlin
@Composable
fun PaginatedList(
    viewModel: ProductViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    val listState = rememberLazyListState()

    // Detectar cuando llegamos al final
    val shouldLoadMore by remember {
        derivedStateOf {
            val lastVisibleItem = listState.layoutInfo.visibleItemsInfo.lastOrNull()
            lastVisibleItem != null && 
            lastVisibleItem.index >= listState.layoutInfo.totalItemsCount - 5
        }
    }

    LaunchedEffect(shouldLoadMore) {
        if (shouldLoadMore && !uiState.isLoadingMore) {
            viewModel.loadMore()
        }
    }

    LazyColumn(state = listState) {
        items(uiState.products, key = { it.id }) { product ->
            ProductCard(product)
        }

        // Indicador de carga al final
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
    }
}
```

---

## Resumen

| Concepto | Descripción |
|----------|-------------|
| `LazyColumn` | Lista eficiente vertical |
| `LazyRow` | Lista eficiente horizontal |
| `LazyVerticalGrid` | Grid eficiente |
| `key` | Identifica items para optimizar |
| `rememberLazyListState` | Controla scroll |
| `derivedStateOf` | Deriva estado sin recomposiciones extra |
| Pull-to-refresh | Actualizar deslizando hacia abajo |

### Reglas de rendimiento

1. **Siempre usa `key`** con ID único
2. **Evita objetos inestables** en parámetros
3. **Usa `remember`** para callbacks
4. **Muestra estados** (loading, error, empty)
5. **No anides LazyColumns** (problemas de altura)

---

## Siguiente paso

→ [ejercicios.md](ejercicios.md)
