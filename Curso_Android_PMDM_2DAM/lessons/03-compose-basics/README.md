# Lección 03: Compose Basics

## Objetivos

- Entender el paradigma declarativo vs imperativo
- Crear interfaces con composables básicos
- Aplicar Modifier para estilo y comportamiento
- Manejar estado local con `remember` y `mutableStateOf`
- Usar layouts: Column, Row, Box, LazyColumn
- Implementar previews

---

## 1. Paradigma declarativo

### Imperativo (XML tradicional)

```kotlin
// Buscas la vista
val textView = findViewById<TextView>(R.id.miTexto)
// Le dices QUÉ HACER
textView.text = "Hola"
textView.setTextColor(Color.RED)
```

### Declarativo (Compose)

```kotlin
// Describes QUÉ QUIERES VER
@Composable
fun MiTexto() {
    Text(
        text = "Hola",
        color = Color.Red
    )
}
```

**Diferencia clave:**
- Imperativo: manipulas objetos existentes
- Declarativo: describes el estado final, Compose se encarga del resto

---

## 2. Composables

Un composable es una función que define UI.

```kotlin
@Composable
fun Saludo(nombre: String) {
    Text(text = "Hola, $nombre!")
}
```

**Reglas:**
- Anotada con `@Composable`
- Nombre en PascalCase
- Puede llamar a otros composables
- No retorna nada (Unit)

### Recomposición

Cuando el estado cambia, Compose "recompone" (redibuja) solo lo necesario.

```kotlin
@Composable
fun Contador() {
    var count by remember { mutableStateOf(0) }

    Button(onClick = { count++ }) {
        Text("Clicks: $count")  // Se recompone cuando count cambia
    }
}
```

---

## 3. Composables básicos

### Text

```kotlin
Text(
    text = "Hola Mundo",
    fontSize = 24.sp,
    fontWeight = FontWeight.Bold,
    color = Color.Blue,
    textAlign = TextAlign.Center,
    maxLines = 2,
    overflow = TextOverflow.Ellipsis
)
```

### Button

```kotlin
Button(
    onClick = { /* acción */ },
    enabled = true,
    colors = ButtonDefaults.buttonColors(
        containerColor = Color.Blue
    )
) {
    Text("Pulsar")
}

// Variantes
OutlinedButton(onClick = { }) { Text("Outlined") }
TextButton(onClick = { }) { Text("Text") }
```

### TextField

```kotlin
var texto by remember { mutableStateOf("") }

TextField(
    value = texto,
    onValueChange = { texto = it },
    label = { Text("Nombre") },
    placeholder = { Text("Escribe tu nombre") },
    singleLine = true
)

// Variante outlined
OutlinedTextField(
    value = texto,
    onValueChange = { texto = it },
    label = { Text("Email") }
)
```

### Image

```kotlin
// Desde recursos
Image(
    painter = painterResource(id = R.drawable.mi_imagen),
    contentDescription = "Descripción",
    contentScale = ContentScale.Crop
)

// Icono de Material
Icon(
    imageVector = Icons.Default.Favorite,
    contentDescription = "Favorito",
    tint = Color.Red
)
```

### Card

```kotlin
Card(
    modifier = Modifier.fillMaxWidth(),
    elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("Título", fontWeight = FontWeight.Bold)
        Text("Contenido de la tarjeta")
    }
}
```

---

## 4. Layouts

### Column

Apila elementos verticalmente.

```kotlin
Column(
    modifier = Modifier.fillMaxSize(),
    verticalArrangement = Arrangement.Center,
    horizontalAlignment = Alignment.CenterHorizontally
) {
    Text("Primero")
    Text("Segundo")
    Text("Tercero")
}
```

### Row

Apila elementos horizontalmente.

```kotlin
Row(
    modifier = Modifier.fillMaxWidth(),
    horizontalArrangement = Arrangement.SpaceBetween,
    verticalAlignment = Alignment.CenterVertically
) {
    Text("Izquierda")
    Text("Derecha")
}
```

### Box

Apila elementos uno encima de otro (z-index).

```kotlin
Box(
    modifier = Modifier.size(200.dp),
    contentAlignment = Alignment.Center
) {
    Image(painter = painterResource(R.drawable.fondo), ...)
    Text("Texto encima")  // Se dibuja encima de la imagen
}
```

### Spacer

Espacio vacío.

```kotlin
Column {
    Text("Arriba")
    Spacer(modifier = Modifier.height(16.dp))
    Text("Abajo")
}
```

---

## 5. Modifier

Los Modifier configuran apariencia y comportamiento.

```kotlin
Text(
    text = "Hola",
    modifier = Modifier
        .fillMaxWidth()           // Ancho máximo
        .padding(16.dp)           // Padding interno
        .background(Color.Gray)   // Fondo
        .clickable { }            // Hace clickable
)
```

### Modificadores comunes

```kotlin
Modifier
    // Tamaño
    .size(100.dp)
    .fillMaxWidth()
    .fillMaxHeight()
    .fillMaxSize()
    .width(200.dp)
    .height(100.dp)
    .wrapContentSize()
    
    // Espaciado
    .padding(16.dp)
    .padding(horizontal = 16.dp, vertical = 8.dp)
    .padding(start = 8.dp, top = 4.dp)
    
    // Apariencia
    .background(Color.Red)
    .background(Color.Red, RoundedCornerShape(8.dp))
    .border(1.dp, Color.Black)
    .clip(RoundedCornerShape(8.dp))
    .shadow(4.dp)
    
    // Interacción
    .clickable { }
    .scrollable(...)
    
    // Peso (en Row/Column)
    .weight(1f)
```

### Orden importa

```kotlin
// Padding FUERA del background
Modifier
    .padding(16.dp)
    .background(Color.Red)

// Padding DENTRO del background
Modifier
    .background(Color.Red)
    .padding(16.dp)
```

---

## 6. Estado local

### remember + mutableStateOf

```kotlin
@Composable
fun Contador() {
    // remember: sobrevive a recomposiciones
    // mutableStateOf: trigger de recomposición cuando cambia
    var count by remember { mutableStateOf(0) }

    Column {
        Text("Contador: $count")
        Button(onClick = { count++ }) {
            Text("Incrementar")
        }
    }
}
```

### Delegación con by

```kotlin
// Sin delegación
val countState = remember { mutableStateOf(0) }
Text("Valor: ${countState.value}")
countState.value = 5

// Con delegación (más limpio)
var count by remember { mutableStateOf(0) }
Text("Valor: $count")
count = 5
```

Necesitas importar:
```kotlin
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
```

### Estado para TextField

```kotlin
@Composable
fun FormularioNombre() {
    var nombre by remember { mutableStateOf("") }

    Column {
        OutlinedTextField(
            value = nombre,
            onValueChange = { nombre = it },
            label = { Text("Nombre") }
        )
        
        if (nombre.isNotEmpty()) {
            Text("Hola, $nombre!")
        }
    }
}
```

---

## 7. Listas con LazyColumn

Para listas grandes, usa `LazyColumn` (equivalente a RecyclerView).

```kotlin
@Composable
fun ListaProductos(productos: List<Producto>) {
    LazyColumn {
        items(productos) { producto ->
            ProductoItem(producto)
        }
    }
}

@Composable
fun ProductoItem(producto: Producto) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(producto.nombre, fontWeight = FontWeight.Bold)
            Text("${producto.precio} €")
        }
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

### Con key (importante para rendimiento)

```kotlin
LazyColumn {
    items(
        items = productos,
        key = { it.id }  // Identifica cada item únicamente
    ) { producto ->
        ProductoItem(producto)
    }
}
```

---

## 8. Preview

Las previews muestran la UI sin ejecutar la app.

```kotlin
@Preview(showBackground = true)
@Composable
fun SaludoPreview() {
    MiAppTheme {
        Saludo("Android")
    }
}

// Preview con configuración
@Preview(
    name = "Dark Mode",
    showBackground = true,
    uiMode = Configuration.UI_MODE_NIGHT_YES
)
@Composable
fun SaludoDarkPreview() {
    MiAppTheme {
        Saludo("Android")
    }
}

// Preview de grupo
@Preview(showBackground = true, widthDp = 320)
@Preview(showBackground = true, widthDp = 480)
@Composable
fun SaludoMultiPreview() {
    Saludo("Android")
}
```

**Reglas para Preview:**
- Función sin parámetros
- O parámetros con valores por defecto
- Anotada con `@Preview`

---

## 9. Material 3

### Scaffold

Estructura básica con TopBar, BottomBar, FAB.

```kotlin
@Composable
fun PantallaConScaffold() {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Mi App") },
                navigationIcon = {
                    IconButton(onClick = { }) {
                        Icon(Icons.Default.Menu, "Menú")
                    }
                }
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = { }) {
                Icon(Icons.Default.Add, "Añadir")
            }
        }
    ) { paddingValues ->
        // Contenido principal
        Column(modifier = Modifier.padding(paddingValues)) {
            Text("Contenido")
        }
    }
}
```

### Colores del tema

```kotlin
Text(
    text = "Título",
    color = MaterialTheme.colorScheme.primary
)

Surface(
    color = MaterialTheme.colorScheme.surfaceVariant
) {
    // contenido
}
```

### Tipografía del tema

```kotlin
Text(
    text = "Título",
    style = MaterialTheme.typography.headlineMedium
)

Text(
    text = "Cuerpo",
    style = MaterialTheme.typography.bodyLarge
)
```

---

## Resumen

| Concepto | Descripción |
|----------|-------------|
| `@Composable` | Marca funciones que definen UI |
| `Modifier` | Configura apariencia y comportamiento |
| `remember` | Mantiene estado entre recomposiciones |
| `mutableStateOf` | Estado observable que dispara recomposición |
| `Column/Row/Box` | Layouts básicos |
| `LazyColumn` | Lista eficiente (como RecyclerView) |
| `@Preview` | Previsualiza UI sin ejecutar |
| `Scaffold` | Estructura de pantalla Material |

---

## Siguiente paso

→ [ejercicios.md](ejercicios.md)
