# Soluciones - Lección 03: Compose Basics

## Ejercicio 1: Tarjeta de perfil

```kotlin
@Composable
fun ProfileCard(
    nombre: String,
    email: String,
    modifier: Modifier = Modifier
) {
    var isFollowing by remember { mutableStateOf(false) }

    Card(
        modifier = modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth()
            ) {
                // Avatar circular con inicial
                Box(
                    modifier = Modifier
                        .size(60.dp)
                        .clip(CircleShape)
                        .background(MaterialTheme.colorScheme.primary),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = nombre.first().uppercase(),
                        color = Color.White,
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Bold
                    )
                }

                Spacer(modifier = Modifier.width(16.dp))

                Column {
                    Text(
                        text = nombre,
                        fontWeight = FontWeight.Bold,
                        fontSize = 18.sp
                    )
                    Text(
                        text = email,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = 14.sp
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            Button(
                onClick = { isFollowing = !isFollowing },
                modifier = Modifier.fillMaxWidth(),
                colors = if (isFollowing) {
                    ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.surfaceVariant,
                        contentColor = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                } else {
                    ButtonDefaults.buttonColors()
                }
            ) {
                Text(if (isFollowing) "Siguiendo" else "Seguir")
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun ProfileCardPreview() {
    MaterialTheme {
        ProfileCard(
            nombre = "Juan García",
            email = "juan@email.com",
            modifier = Modifier.padding(16.dp)
        )
    }
}
```

---

## Ejercicio 2: Contador con límites

```kotlin
@Composable
fun BoundedCounter(
    min: Int = 0,
    max: Int = 10,
    initial: Int = 5,
    modifier: Modifier = Modifier
) {
    var count by remember { mutableStateOf(initial.coerceIn(min, max)) }

    Row(
        modifier = modifier,
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.Center
    ) {
        IconButton(
            onClick = { count-- },
            enabled = count > min
        ) {
            Icon(
                imageVector = Icons.Default.Remove,
                contentDescription = "Decrementar"
            )
        }

        Card(
            modifier = Modifier.padding(horizontal = 16.dp)
        ) {
            Text(
                text = count.toString(),
                modifier = Modifier.padding(horizontal = 24.dp, vertical = 12.dp),
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold
            )
        }

        IconButton(
            onClick = { count++ },
            enabled = count < max
        ) {
            Icon(
                imageVector = Icons.Default.Add,
                contentDescription = "Incrementar"
            )
        }
    }
}

@Preview(showBackground = true)
@Composable
fun BoundedCounterPreview() {
    MaterialTheme {
        Column {
            BoundedCounter(min = 0, max = 10, initial = 5)
            Spacer(modifier = Modifier.height(16.dp))
            BoundedCounter(min = 0, max = 3, initial = 0)  // - deshabilitado
            Spacer(modifier = Modifier.height(16.dp))
            BoundedCounter(min = 0, max = 5, initial = 5)  // + deshabilitado
        }
    }
}
```

---

## Ejercicio 3: Lista de tareas simple

```kotlin
data class Task(
    val id: Int,
    val title: String,
    val completed: Boolean
)

@Composable
fun SimpleTaskList(
    initialTasks: List<Task>,
    modifier: Modifier = Modifier
) {
    var tasks by remember { mutableStateOf(initialTasks) }

    LazyColumn(modifier = modifier) {
        items(
            items = tasks,
            key = { it.id }
        ) { task ->
            TaskItem(
                task = task,
                onToggle = { taskId ->
                    tasks = tasks.map {
                        if (it.id == taskId) it.copy(completed = !it.completed)
                        else it
                    }
                },
                onDelete = { taskId ->
                    tasks = tasks.filter { it.id != taskId }
                }
            )
        }
    }
}

@Composable
fun TaskItem(
    task: Task,
    onToggle: (Int) -> Unit,
    onDelete: (Int) -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Checkbox(
                checked = task.completed,
                onCheckedChange = { onToggle(task.id) }
            )

            Text(
                text = task.title,
                modifier = Modifier.weight(1f),
                textDecoration = if (task.completed) {
                    TextDecoration.LineThrough
                } else {
                    TextDecoration.None
                },
                color = if (task.completed) {
                    MaterialTheme.colorScheme.onSurfaceVariant
                } else {
                    MaterialTheme.colorScheme.onSurface
                }
            )

            IconButton(onClick = { onDelete(task.id) }) {
                Icon(
                    imageVector = Icons.Default.Delete,
                    contentDescription = "Eliminar",
                    tint = MaterialTheme.colorScheme.error
                )
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun SimpleTaskListPreview() {
    val sampleTasks = listOf(
        Task(1, "Comprar leche", false),
        Task(2, "Llamar al médico", true),
        Task(3, "Estudiar Compose", false),
        Task(4, "Hacer ejercicio", false)
    )

    MaterialTheme {
        SimpleTaskList(initialTasks = sampleTasks)
    }
}
```

---

## Ejercicio 4: Formulario con validación visual

```kotlin
@Composable
fun RegistrationForm(modifier: Modifier = Modifier) {
    var nombre by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var showSuccess by remember { mutableStateOf(false) }

    val nombreValido = nombre.length >= 3
    val emailValido = email.contains("@")
    val passwordValido = password.length >= 6
    val formularioValido = nombreValido && emailValido && passwordValido

    Column(
        modifier = modifier
            .fillMaxWidth()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        // Campo Nombre
        OutlinedTextField(
            value = nombre,
            onValueChange = { nombre = it },
            label = { Text("Nombre") },
            isError = nombre.isNotEmpty() && !nombreValido,
            supportingText = {
                if (nombre.isNotEmpty() && !nombreValido) {
                    Text("Mínimo 3 caracteres")
                }
            },
            modifier = Modifier.fillMaxWidth()
        )

        // Campo Email
        OutlinedTextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email") },
            isError = email.isNotEmpty() && !emailValido,
            supportingText = {
                if (email.isNotEmpty() && !emailValido) {
                    Text("Debe contener @")
                }
            },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
            modifier = Modifier.fillMaxWidth()
        )

        // Campo Contraseña
        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Contraseña") },
            isError = password.isNotEmpty() && !passwordValido,
            supportingText = {
                if (password.isNotEmpty() && !passwordValido) {
                    Text("Mínimo 6 caracteres")
                }
            },
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(8.dp))

        // Botón
        Button(
            onClick = { showSuccess = true },
            enabled = formularioValido,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Registrar")
        }

        // Mensaje de éxito
        if (showSuccess) {
            Card(
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer
                ),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = "¡Registro exitoso!",
                    modifier = Modifier.padding(16.dp),
                    color = MaterialTheme.colorScheme.onPrimaryContainer
                )
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun RegistrationFormPreview() {
    MaterialTheme {
        RegistrationForm()
    }
}
```

---

## Ejercicio 5: Galería de imágenes

```kotlin
@OptIn(ExperimentalFoundationApi::class)
@Composable
fun ImageGallery(modifier: Modifier = Modifier) {
    val colors = listOf(
        Color.Red, Color.Green, Color.Blue,
        Color.Yellow, Color.Cyan, Color.Magenta,
        Color.Gray, Color.DarkGray, Color(0xFFFF9800)
    )

    var expandedIndex by remember { mutableStateOf<Int?>(null) }

    Box(modifier = modifier.fillMaxSize()) {
        // Grid de colores
        LazyVerticalGrid(
            columns = GridCells.Fixed(3),
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
                        .clickable { expandedIndex = index }
                )
            }
        }

        // Vista expandida
        expandedIndex?.let { index ->
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Black.copy(alpha = 0.8f))
                    .clickable { expandedIndex = null },
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Box(
                        modifier = Modifier
                            .size(250.dp)
                            .clip(RoundedCornerShape(16.dp))
                            .background(colors[index])
                    )

                    Spacer(modifier = Modifier.height(24.dp))

                    IconButton(
                        onClick = { expandedIndex = null },
                        modifier = Modifier
                            .size(48.dp)
                            .background(Color.White, CircleShape)
                    ) {
                        Icon(
                            imageVector = Icons.Default.Close,
                            contentDescription = "Cerrar",
                            tint = Color.Black
                        )
                    }
                }
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun ImageGalleryPreview() {
    MaterialTheme {
        ImageGallery()
    }
}
```

---

## Ejercicio 6: Scaffold completo

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(modifier: Modifier = Modifier) {
    var selectedTab by remember { mutableStateOf(0) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Mi App") },
                navigationIcon = {
                    IconButton(onClick = { /* abrir drawer */ }) {
                        Icon(Icons.Default.Menu, contentDescription = "Menú")
                    }
                }
            )
        },
        bottomBar = {
            NavigationBar {
                NavigationBarItem(
                    selected = selectedTab == 0,
                    onClick = { selectedTab = 0 },
                    icon = { Icon(Icons.Default.Home, contentDescription = null) },
                    label = { Text("Home") }
                )
                NavigationBarItem(
                    selected = selectedTab == 1,
                    onClick = { selectedTab = 1 },
                    icon = { Icon(Icons.Default.Search, contentDescription = null) },
                    label = { Text("Buscar") }
                )
                NavigationBarItem(
                    selected = selectedTab == 2,
                    onClick = { selectedTab = 2 },
                    icon = { Icon(Icons.Default.Person, contentDescription = null) },
                    label = { Text("Perfil") }
                )
            }
        },
        floatingActionButton = {
            FloatingActionButton(onClick = { /* acción */ }) {
                Icon(Icons.Default.Add, contentDescription = "Añadir")
            }
        },
        modifier = modifier
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues),
            contentAlignment = Alignment.Center
        ) {
            when (selectedTab) {
                0 -> Text("Pantalla Home", style = MaterialTheme.typography.headlineMedium)
                1 -> Text("Pantalla Buscar", style = MaterialTheme.typography.headlineMedium)
                2 -> Text("Pantalla Perfil", style = MaterialTheme.typography.headlineMedium)
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun MainScreenPreview() {
    MaterialTheme {
        MainScreen()
    }
}
```

---

## Ejercicio 7 (Bonus): Animación básica

```kotlin
@Composable
fun AnimatedHeart(modifier: Modifier = Modifier) {
    var liked by remember { mutableStateOf(false) }

    val size by animateDpAsState(
        targetValue = if (liked) 64.dp else 32.dp,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioMediumBouncy,
            stiffness = Spring.StiffnessLow
        ),
        label = "size"
    )

    val color by animateColorAsState(
        targetValue = if (liked) Color.Red else Color.Gray,
        animationSpec = tween(durationMillis = 300),
        label = "color"
    )

    Box(
        modifier = modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = if (liked) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
            contentDescription = "Corazón",
            tint = color,
            modifier = Modifier
                .size(size)
                .clickable { liked = !liked }
        )
    }
}

@Preview(showBackground = true)
@Composable
fun AnimatedHeartPreview() {
    MaterialTheme {
        AnimatedHeart()
    }
}
```

### Imports necesarios para animación

```kotlin
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
```
