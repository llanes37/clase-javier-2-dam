# Soluciones - Lección 05: Navigation Compose

## Ejercicio 1: Navegación básica

```kotlin
// Screen.kt
sealed class Screen(val route: String) {
    object Home : Screen("home")
    object About : Screen("about")
    object Contact : Screen("contact")
}

// AppNavigation.kt
@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Screen.Home.route
    ) {
        composable(Screen.Home.route) {
            HomeScreen(
                onNavigateToAbout = { navController.navigate(Screen.About.route) }
            )
        }

        composable(Screen.About.route) {
            AboutScreen(
                onNavigateToContact = { navController.navigate(Screen.Contact.route) }
            )
        }

        composable(Screen.Contact.route) {
            ContactScreen(
                onNavigateToHome = {
                    navController.navigate(Screen.Home.route) {
                        popUpTo(Screen.Home.route) { inclusive = true }
                    }
                }
            )
        }
    }
}

// Screens
@Composable
fun HomeScreen(onNavigateToAbout: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text("Pantalla Home", fontSize = 24.sp)
        Spacer(Modifier.height(16.dp))
        Button(onClick = onNavigateToAbout) {
            Text("Ir a About")
        }
    }
}

@Composable
fun AboutScreen(onNavigateToContact: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text("Pantalla About", fontSize = 24.sp)
        Spacer(Modifier.height(8.dp))
        Text("Información sobre la app")
        Spacer(Modifier.height(16.dp))
        Button(onClick = onNavigateToContact) {
            Text("Ir a Contact")
        }
    }
}

@Composable
fun ContactScreen(onNavigateToHome: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text("Pantalla Contact", fontSize = 24.sp)
        Spacer(Modifier.height(8.dp))
        Text("Email: contacto@app.com")
        Spacer(Modifier.height(16.dp))
        Button(onClick = onNavigateToHome) {
            Text("Volver al inicio")
        }
    }
}
```

---

## Ejercicio 2: Navegación con argumentos

```kotlin
// Models
data class Product(
    val id: Int,
    val name: String,
    val price: Double,
    val description: String
)

object ProductRepository {
    val products = listOf(
        Product(1, "Laptop", 999.99, "Potente laptop para trabajo"),
        Product(2, "Mouse", 29.99, "Mouse ergonómico"),
        Product(3, "Teclado", 79.99, "Teclado mecánico RGB")
    )

    fun getById(id: Int) = products.find { it.id == id }
}

// Screen.kt
sealed class Screen(val route: String) {
    object ProductList : Screen("products")

    data class ProductDetail(val productId: Int) : Screen("product/$productId") {
        companion object {
            const val routeWithArgs = "product/{productId}"
            val arguments = listOf(
                navArgument("productId") { type = NavType.IntType }
            )
        }
    }
}

// AppNavigation.kt
@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Screen.ProductList.route
    ) {
        composable(Screen.ProductList.route) {
            ProductListScreen(
                products = ProductRepository.products,
                onProductClick = { productId ->
                    navController.navigate(Screen.ProductDetail(productId).route)
                }
            )
        }

        composable(
            route = Screen.ProductDetail.routeWithArgs,
            arguments = Screen.ProductDetail.arguments
        ) { backStackEntry ->
            val productId = backStackEntry.arguments?.getInt("productId") ?: 0
            val product = ProductRepository.getById(productId)

            if (product != null) {
                ProductDetailScreen(
                    product = product,
                    onBack = { navController.popBackStack() }
                )
            }
        }
    }
}

// Screens
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProductListScreen(
    products: List<Product>,
    onProductClick: (Int) -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Productos") })
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.padding(padding)
        ) {
            items(products, key = { it.id }) { product ->
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(8.dp)
                        .clickable { onProductClick(product.id) }
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(product.name, fontWeight = FontWeight.Bold)
                            Text(product.description, fontSize = 12.sp)
                        }
                        Text(
                            "${product.price} €",
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary
                        )
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProductDetailScreen(
    product: Product,
    onBack: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(product.name) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Volver")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
        ) {
            Text(
                text = product.name,
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold
            )

            Spacer(Modifier.height(8.dp))

            Text(
                text = "${product.price} €",
                fontSize = 20.sp,
                color = MaterialTheme.colorScheme.primary
            )

            Spacer(Modifier.height(16.dp))

            Text(
                text = product.description,
                fontSize = 16.sp
            )
        }
    }
}
```

---

## Ejercicio 3: Bottom Navigation

```kotlin
sealed class Screen(val route: String) {
    object Home : Screen("home")
    object Search : Screen("search")
    object Profile : Screen("profile")
}

data class BottomNavItem(
    val screen: Screen,
    val icon: ImageVector,
    val label: String
)

@Composable
fun MainScreen() {
    val navController = rememberNavController()

    val items = listOf(
        BottomNavItem(Screen.Home, Icons.Default.Home, "Inicio"),
        BottomNavItem(Screen.Search, Icons.Default.Search, "Buscar"),
        BottomNavItem(Screen.Profile, Icons.Default.Person, "Perfil")
    )

    Scaffold(
        bottomBar = {
            NavigationBar {
                val navBackStackEntry by navController.currentBackStackEntryAsState()
                val currentRoute = navBackStackEntry?.destination?.route

                items.forEach { item ->
                    NavigationBarItem(
                        icon = { Icon(item.icon, contentDescription = item.label) },
                        label = { Text(item.label) },
                        selected = currentRoute == item.screen.route,
                        onClick = {
                            if (currentRoute != item.screen.route) {
                                navController.navigate(item.screen.route) {
                                    popUpTo(navController.graph.findStartDestination().id) {
                                        saveState = true
                                    }
                                    launchSingleTop = true
                                    restoreState = true
                                }
                            }
                        }
                    )
                }
            }
        }
    ) { padding ->
        NavHost(
            navController = navController,
            startDestination = Screen.Home.route,
            modifier = Modifier.padding(padding)
        ) {
            composable(Screen.Home.route) {
                HomeTab()
            }
            composable(Screen.Search.route) {
                SearchTab()
            }
            composable(Screen.Profile.route) {
                ProfileTab()
            }
        }
    }
}

@Composable
fun HomeTab() {
    var items by remember { mutableStateOf(listOf("Item 1", "Item 2", "Item 3")) }

    Column(modifier = Modifier.fillMaxSize()) {
        Text(
            "Home",
            fontSize = 24.sp,
            modifier = Modifier.padding(16.dp)
        )
        LazyColumn {
            items(items) { item ->
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(8.dp)
                ) {
                    Text(item, modifier = Modifier.padding(16.dp))
                }
            }
        }
    }
}

@Composable
fun SearchTab() {
    var query by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text("Buscar", fontSize = 24.sp)
        Spacer(Modifier.height(16.dp))
        OutlinedTextField(
            value = query,
            onValueChange = { query = it },
            label = { Text("Buscar...") },
            modifier = Modifier.fillMaxWidth()
        )
    }
}

@Composable
fun ProfileTab() {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(
            Icons.Default.Person,
            contentDescription = null,
            modifier = Modifier.size(100.dp)
        )
        Spacer(Modifier.height(16.dp))
        Text("Usuario", fontSize = 24.sp)
        Text("usuario@email.com")
    }
}
```

---

## Ejercicio 4: Argumentos opcionales

```kotlin
sealed class Screen(val route: String) {
    object Home : Screen("home")

    data class Search(
        val query: String = "",
        val category: String = "all"
    ) : Screen("search?query=$query&category=$category") {
        companion object {
            const val routeWithArgs = "search?query={query}&category={category}"
            val arguments = listOf(
                navArgument("query") {
                    type = NavType.StringType
                    defaultValue = ""
                },
                navArgument("category") {
                    type = NavType.StringType
                    defaultValue = "all"
                }
            )
        }
    }
}

@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Screen.Home.route
    ) {
        composable(Screen.Home.route) {
            HomeScreen(
                onSearchEmpty = {
                    navController.navigate(Screen.Search().route)
                },
                onSearchWithQuery = {
                    navController.navigate(Screen.Search(query = "kotlin").route)
                },
                onSearchWithAll = {
                    navController.navigate(Screen.Search(query = "android", category = "books").route)
                }
            )
        }

        composable(
            route = Screen.Search.routeWithArgs,
            arguments = Screen.Search.arguments
        ) { backStackEntry ->
            val query = backStackEntry.arguments?.getString("query") ?: ""
            val category = backStackEntry.arguments?.getString("category") ?: "all"
            
            SearchScreen(
                initialQuery = query,
                initialCategory = category,
                onBack = { navController.popBackStack() }
            )
        }
    }
}

@Composable
fun HomeScreen(
    onSearchEmpty: () -> Unit,
    onSearchWithQuery: () -> Unit,
    onSearchWithAll: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.Center
    ) {
        Button(
            onClick = onSearchEmpty,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Buscar (sin argumentos)")
        }

        Spacer(Modifier.height(8.dp))

        Button(
            onClick = onSearchWithQuery,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Buscar 'kotlin'")
        }

        Spacer(Modifier.height(8.dp))

        Button(
            onClick = onSearchWithAll,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Buscar 'android' en 'books'")
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SearchScreen(
    initialQuery: String,
    initialCategory: String,
    onBack: () -> Unit
) {
    var query by remember { mutableStateOf(initialQuery) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Buscar") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Volver")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
        ) {
            OutlinedTextField(
                value = query,
                onValueChange = { query = it },
                label = { Text("Buscar") },
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(Modifier.height(8.dp))

            Text("Categoría: $initialCategory")
        }
    }
}
```

---

## Ejercicio 5: Resultado de navegación

```kotlin
sealed class Screen(val route: String) {
    object Main : Screen("main")
    object Picker : Screen("picker")
}

@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Screen.Main.route
    ) {
        composable(Screen.Main.route) {
            MainScreen(navController = navController)
        }

        composable(Screen.Picker.route) {
            PickerScreen(navController = navController)
        }
    }
}

@Composable
fun MainScreen(navController: NavController) {
    val selectedItem by navController.currentBackStackEntry
        ?.savedStateHandle
        ?.getStateFlow<String?>("selected_item", null)
        ?.collectAsState() ?: remember { mutableStateOf(null) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text("Item seleccionado:", fontSize = 18.sp)
        Spacer(Modifier.height(8.dp))
        Text(
            text = selectedItem ?: "Ninguno",
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold
        )
        Spacer(Modifier.height(24.dp))
        Button(onClick = { navController.navigate(Screen.Picker.route) }) {
            Text("Seleccionar item")
        }
    }
}

@Composable
fun PickerScreen(navController: NavController) {
    val items = listOf(
        "Opción A",
        "Opción B",
        "Opción C",
        "Opción D"
    )

    Column(modifier = Modifier.fillMaxSize()) {
        Text(
            "Selecciona una opción",
            fontSize = 24.sp,
            modifier = Modifier.padding(16.dp)
        )

        LazyColumn {
            items(items) { item ->
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(8.dp)
                        .clickable {
                            navController.previousBackStackEntry
                                ?.savedStateHandle
                                ?.set("selected_item", item)
                            navController.popBackStack()
                        }
                ) {
                    Text(
                        text = item,
                        modifier = Modifier.padding(16.dp),
                        fontSize = 18.sp
                    )
                }
            }
        }
    }
}
```
