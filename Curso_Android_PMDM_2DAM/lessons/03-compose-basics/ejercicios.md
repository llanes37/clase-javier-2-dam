# Ejercicios - Lección 03: Compose Basics

## Ejercicio 1: Tarjeta de perfil

### Instrucciones

Crea un composable `ProfileCard` que muestre:
- Avatar (puedes usar un `Box` con color de fondo como placeholder)
- Nombre
- Email
- Botón "Seguir"

La tarjeta debe:
- Tener bordes redondeados
- Tener sombra
- El avatar debe ser circular
- El botón debe cambiar su texto a "Siguiendo" cuando se pulse

### Mockup

```
┌─────────────────────────────┐
│  ┌───┐                      │
│  │ A │  Juan García         │
│  └───┘  juan@email.com      │
│                             │
│         [ Seguir ]          │
└─────────────────────────────┘
```

### Criterios de aceptación

- [ ] El composable recibe nombre y email como parámetros
- [ ] El avatar es un círculo con la inicial del nombre
- [ ] El botón cambia entre "Seguir" y "Siguiendo"
- [ ] Usa `Card` de Material 3
- [ ] Tiene una Preview funcional

---

## Ejercicio 2: Contador con límites

### Instrucciones

Crea un composable `BoundedCounter` que:
- Muestre un número
- Tenga botones + y -
- El número nunca baje de un mínimo ni suba de un máximo
- Los botones se deshabiliten cuando se alcanza el límite

### Parámetros

```kotlin
@Composable
fun BoundedCounter(
    min: Int = 0,
    max: Int = 10,
    initial: Int = 5
)
```

### Mockup

```
       ┌───────┐
  [-]  │   5   │  [+]
       └───────┘
```

### Criterios de aceptación

- [ ] El contador respeta los límites min/max
- [ ] El botón - se deshabilita cuando count == min
- [ ] El botón + se deshabilita cuando count == max
- [ ] El valor inicial se puede configurar
- [ ] Preview con diferentes configuraciones

---

## Ejercicio 3: Lista de tareas simple

### Instrucciones

Crea un composable `SimpleTaskList` que muestre una lista de tareas con:
- Checkbox para marcar completada
- Texto de la tarea (tachado si completada)
- Botón para eliminar

Usa estos datos de ejemplo:

```kotlin
data class Task(
    val id: Int,
    val title: String,
    val completed: Boolean
)

val sampleTasks = listOf(
    Task(1, "Comprar leche", false),
    Task(2, "Llamar al médico", true),
    Task(3, "Estudiar Compose", false),
    Task(4, "Hacer ejercicio", false)
)
```

### Criterios de aceptación

- [ ] Usa `LazyColumn`
- [ ] Cada item tiene checkbox, texto y botón eliminar
- [ ] El checkbox funciona (cambia el estado)
- [ ] El texto se tacha cuando está completado
- [ ] El botón eliminar quita el item de la lista
- [ ] Usa `key` en los items

---

## Ejercicio 4: Formulario con validación visual

### Instrucciones

Crea un formulario de registro con:
- Campo nombre (mínimo 3 caracteres)
- Campo email (debe contener @)
- Campo contraseña (mínimo 6 caracteres)
- Botón "Registrar"

Validación visual:
- Mostrar mensaje de error bajo el campo si no es válido
- El borde del campo debe ser rojo si hay error
- El botón solo se habilita si todo es válido

### Criterios de aceptación

- [ ] Los 3 campos validan correctamente
- [ ] Los mensajes de error se muestran/ocultan
- [ ] Los campos inválidos tienen indicación visual
- [ ] El botón se habilita/deshabilita según validez
- [ ] Al pulsar "Registrar" (si válido), muestra un mensaje de éxito

---

## Ejercicio 5: Galería de imágenes

### Instrucciones

Crea una galería que muestre imágenes en grid:
- 3 columnas
- Al pulsar una imagen, se expande a pantalla completa
- Botón para cerrar la imagen expandida

Usa colores como placeholder de imágenes:

```kotlin
val colors = listOf(
    Color.Red, Color.Green, Color.Blue,
    Color.Yellow, Color.Cyan, Color.Magenta,
    Color.Gray, Color.DarkGray, Color.LightGray
)
```

### Pistas

- Usa `LazyVerticalGrid` con `GridCells.Fixed(3)`
- Para la imagen expandida, usa un `Box` que ocupe toda la pantalla
- Controla qué imagen está expandida con estado

### Criterios de aceptación

- [ ] Se muestra un grid de 3 columnas
- [ ] Al pulsar un color, se expande
- [ ] La vista expandida ocupa toda la pantalla
- [ ] Hay un botón/icono para cerrar
- [ ] Al cerrar, vuelve al grid

---

## Ejercicio 6: Scaffold completo

### Instrucciones

Crea una pantalla con `Scaffold` que incluya:
- TopAppBar con título y menú hamburguesa
- BottomNavigationBar con 3 opciones (Home, Search, Profile)
- FloatingActionButton
- Contenido que cambia según la opción seleccionada en el BottomNav

### Criterios de aceptación

- [ ] Usa `Scaffold` correctamente
- [ ] La TopAppBar tiene navegación icon
- [ ] El BottomNav tiene 3 items con iconos
- [ ] El contenido cambia al pulsar cada opción del BottomNav
- [ ] El FAB está posicionado correctamente
- [ ] El padding del Scaffold se aplica al contenido

---

## Ejercicio 7 (Bonus): Animación básica

### Instrucciones

Crea un composable que:
- Muestre un corazón (❤️ o Icon)
- Al pulsarlo, crezca de tamaño con animación
- Cambie de color (gris a rojo) con animación

### Pistas

```kotlin
val size by animateDpAsState(
    targetValue = if (liked) 48.dp else 24.dp,
    animationSpec = spring(dampingRatio = Spring.DampingRatioMediumBouncy)
)

val color by animateColorAsState(
    targetValue = if (liked) Color.Red else Color.Gray
)
```

### Criterios de aceptación

- [ ] El corazón anima su tamaño
- [ ] El corazón anima su color
- [ ] La animación es suave (no instantánea)
- [ ] Funciona como toggle (pulsar de nuevo lo reduce)

---

## Entrega

1. Crea los composables en archivos separados dentro de tu proyecto
2. Cada composable debe tener al menos una `@Preview`
3. Verifica que compila y las previews se renderizan
4. Crea rama y PR siguiendo el flujo establecido
