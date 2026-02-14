# Lección 05: Navigation Compose

## Objetivos

- Configurar navegación en una app multi-pantalla
- Definir rutas y NavHost
- Pasar datos entre pantallas
- Implementar navegación con argumentos
- Crear bottom navigation

---

## 1. Dependencias

```kotlin
// build.gradle.kts (app)
implementation("androidx.navigation:navigation-compose:2.7.6")
```

---

## 2. Conceptos básicos

### Componentes principales

| Componente | Descripción |
|------------|-------------|
| `NavController` | Controla la navegación (back stack) |
| `NavHost` | Contenedor que muestra las pantallas |
| `NavGraph` | Define las rutas disponibles |
| `composable()` | Define una pantalla y su ruta |

---

## 3. Setup básico

### Definir rutas

```kotlin
// Routes.kt
object Routes {
    const val HOME = "home"
    const val DETAIL = "detail/{itemId}"
    const val PROFILE = "profile"
    
    fun detailRoute(itemId: Int) = "detail/$itemId"
}
```

### NavHost

```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Routes.HOME
    ) {
        composable(Routes.HOME) {
            HomeScreen(
                onItemClick = { itemId ->
                    navController.navigate(Routes.detailRoute(itemId))
                }
            )
        }

        composable(
            route = Routes.DETAIL,
            arguments = listOf(
                navArgument("itemId") { type = NavType.IntType }
            )
        ) { backStackEntry ->
            val itemId = backStackEntry.arguments?.getInt("itemId") ?: 0
            DetailScreen(
                itemId = itemId,
                onBack = { navController.popBackStack() }
            )
        }

        composable(Routes.PROFILE) {
            ProfileScreen()
        }
    }
}
```

---

## 4. Navegación básica

### Navegar a otra pantalla

```kotlin
// Navegación simple
navController.navigate("profile")

// Con argumento en la ruta
navController.navigate("detail/123")
```

### Volver atrás

```kotlin
// Volver a la pantalla anterior
navController.popBackStack()

// Volver a una pantalla específica
navController.popBackStack(
    route = "home",
    inclusive = false  // No incluir "home" en el pop
)
```

### Reemplazar pantalla (sin añadir al back stack)

```kotlin
navController.navigate("profile") {
    popUpTo("home") { inclusive = true }
}
```

### Single top (evitar duplicados)

```kotlin
navController.navigate("home") {
    launchSingleTop = true
}
```

---

## 5. Argumentos de navegación

### Argumentos obligatorios

```kotlin
// Ruta con argumento
composable(
    route = "detail/{productId}",
    arguments = listOf(
        navArgument("productId") { type = NavType.IntType }
    )
) { backStackEntry ->
    val productId = backStackEntry.arguments?.getInt("productId") ?: 0
    DetailScreen(productId = productId)
}

// Navegar
navController.navigate("detail/42")
```

### Argumentos opcionales

```kotlin
composable(
    route = "search?query={query}",
    arguments = listOf(
        navArgument("query") {
            type = NavType.StringType
            defaultValue = ""
            nullable = true
        }
    )
) { backStackEntry ->
    val query = backStackEntry.arguments?.getString("query") ?: ""
    SearchScreen(initialQuery = query)
}

// Navegar
navController.navigate("search?query=kotlin")
navController.navigate("search")  // Sin query, usa default
```

### Múltiples argumentos

```kotlin
composable(
    route = "filter/{category}/{minPrice}/{maxPrice}",
    arguments = listOf(
        navArgument("category") { type = NavType.StringType },
        navArgument("minPrice") { type = NavType.FloatType },
        navArgument("maxPrice") { type = NavType.FloatType }
    )
) { backStackEntry ->
    val category = backStackEntry.arguments?.getString("category") ?: ""
    val minPrice = backStackEntry.arguments?.getFloat("minPrice") ?: 0f
    val maxPrice = backStackEntry.arguments?.getFloat("maxPrice") ?: 100f
    
    FilterScreen(category, minPrice, maxPrice)
}
```

---

## 6. Patrón recomendado: Sealed class para rutas

```kotlin
sealed class Screen(val route: String) {
    object Home : Screen("home")
    object Profile : Screen("profile")
    
    data class Detail(val productId: Int) : Screen("detail/$productId") {
        companion object {
            const val routeWithArgs = "detail/{productId}"
            val arguments = listOf(
                navArgument("productId") { type = NavType.IntType }
            )
        }
    }
    
    data class Search(val query: String = "") : Screen("search?query=$query") {
        companion object {
            const val routeWithArgs = "search?query={query}"
            val arguments = listOf(
                navArgument("query") {
                    type = NavType.StringType
                    defaultValue = ""
                }
            )
        }
    }
}
```

### Uso con sealed class

```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Screen.Home.route
    ) {
        composable(Screen.Home.route) {
            HomeScreen(
                onProductClick = { productId ->
                    navController.navigate(Screen.Detail(productId).route)
                }
            )
        }

        composable(
            route = Screen.Detail.routeWithArgs,
            arguments = Screen.Detail.arguments
        ) { backStackEntry ->
            val productId = backStackEntry.arguments?.getInt("productId") ?: 0
            DetailScreen(productId = productId)
        }
    }
}
```

---

## 7. Bottom Navigation

```kotlin
@Composable
fun MainScreen() {
    val navController = rememberNavController()

    Scaffold(
        bottomBar = {
            BottomNavBar(navController = navController)
        }
    ) { padding ->
        NavHost(
            navController = navController,
            startDestination = Screen.Home.route,
            modifier = Modifier.padding(padding)
        ) {
            composable(Screen.Home.route) { HomeScreen() }
            composable(Screen.Search.routeWithArgs) { SearchScreen() }
            composable(Screen.Profile.route) { ProfileScreen() }
        }
    }
}

@Composable
fun BottomNavBar(navController: NavController) {
    val items = listOf(
        BottomNavItem(Screen.Home.route, Icons.Default.Home, "Inicio"),
        BottomNavItem(Screen.Search.routeWithArgs, Icons.Default.Search, "Buscar"),
        BottomNavItem(Screen.Profile.route, Icons.Default.Person, "Perfil")
    )

    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    NavigationBar {
        items.forEach { item ->
            NavigationBarItem(
                icon = { Icon(item.icon, contentDescription = item.label) },
                label = { Text(item.label) },
                selected = currentRoute == item.route,
                onClick = {
                    navController.navigate(item.route) {
                        // Evita múltiples copias en el back stack
                        popUpTo(navController.graph.findStartDestination().id) {
                            saveState = true
                        }
                        launchSingleTop = true
                        restoreState = true
                    }
                }
            )
        }
    }
}

data class BottomNavItem(
    val route: String,
    val icon: ImageVector,
    val label: String
)
```

---

## 8. Navegación desde ViewModel

El ViewModel no debe tener referencia al NavController. Usa eventos:

```kotlin
// ViewModel
class ProductViewModel : ViewModel() {
    private val _navigationEvent = MutableSharedFlow<NavigationEvent>()
    val navigationEvent: SharedFlow<NavigationEvent> = _navigationEvent.asSharedFlow()

    fun onProductClick(productId: Int) {
        viewModelScope.launch {
            _navigationEvent.emit(NavigationEvent.ToDetail(productId))
        }
    }
}

sealed class NavigationEvent {
    data class ToDetail(val productId: Int) : NavigationEvent()
    object Back : NavigationEvent()
}

// Screen
@Composable
fun ProductListScreen(
    navController: NavController,
    viewModel: ProductViewModel = viewModel()
) {
    LaunchedEffect(Unit) {
        viewModel.navigationEvent.collect { event ->
            when (event) {
                is NavigationEvent.ToDetail -> {
                    navController.navigate(Screen.Detail(event.productId).route)
                }
                NavigationEvent.Back -> {
                    navController.popBackStack()
                }
            }
        }
    }
    
    // UI...
}
```

---

## 9. Resultado de navegación

Pasar datos de vuelta a la pantalla anterior:

```kotlin
// Pantalla que recibe resultado
@Composable
fun HomeScreen(navController: NavController) {
    // Observar resultado
    val result = navController.currentBackStackEntry
        ?.savedStateHandle
        ?.getStateFlow<String?>("selected_item", null)
        ?.collectAsState()

    result?.value?.let { selectedItem ->
        Text("Seleccionado: $selectedItem")
    }

    Button(onClick = { navController.navigate("picker") }) {
        Text("Seleccionar item")
    }
}

// Pantalla que envía resultado
@Composable
fun PickerScreen(navController: NavController) {
    val items = listOf("Opción A", "Opción B", "Opción C")

    LazyColumn {
        items(items) { item ->
            TextButton(
                onClick = {
                    navController.previousBackStackEntry
                        ?.savedStateHandle
                        ?.set("selected_item", item)
                    navController.popBackStack()
                }
            ) {
                Text(item)
            }
        }
    }
}
```

---

## 10. Deep links

```kotlin
composable(
    route = "product/{productId}",
    arguments = listOf(navArgument("productId") { type = NavType.IntType }),
    deepLinks = listOf(
        navDeepLink { uriPattern = "https://miapp.com/product/{productId}" }
    )
) { backStackEntry ->
    val productId = backStackEntry.arguments?.getInt("productId") ?: 0
    ProductScreen(productId)
}
```

Configurar en AndroidManifest:

```xml
<activity ...>
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data
            android:scheme="https"
            android:host="miapp.com"
            android:pathPattern="/product/.*" />
    </intent-filter>
</activity>
```

---

## Resumen

| Concepto | Uso |
|----------|-----|
| `NavController` | Controla la navegación |
| `NavHost` | Contiene las pantallas |
| `composable()` | Define una ruta |
| `navigate()` | Navega a una pantalla |
| `popBackStack()` | Vuelve atrás |
| `navArgument` | Define argumentos |
| `launchSingleTop` | Evita duplicados |
| `popUpTo` | Limpia el back stack |

---

## Siguiente paso

→ [ejercicios.md](ejercicios.md)
