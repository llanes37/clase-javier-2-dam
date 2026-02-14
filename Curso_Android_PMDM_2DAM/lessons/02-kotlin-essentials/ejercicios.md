# Ejercicios - Lección 02: Kotlin Essentials

## Ejercicio 1: Null Safety

### Instrucciones

Implementa las siguientes funciones manejando nulls correctamente:

```kotlin
// 1. Retorna la longitud del string, o 0 si es null
fun longitudSegura(texto: String?): Int {
    // Tu código
}

// 2. Retorna el email en mayúsculas, o "NO EMAIL" si es null
fun formatearEmail(email: String?): String {
    // Tu código
}

// 3. Retorna el primer elemento, o null si la lista está vacía o es null
fun <T> primerElemento(lista: List<T>?): T? {
    // Tu código
}
```

### Criterios de aceptación

- [ ] No usas `!!` en ninguna función
- [ ] `longitudSegura(null)` retorna `0`
- [ ] `longitudSegura("hola")` retorna `4`
- [ ] `formatearEmail(null)` retorna `"NO EMAIL"`
- [ ] `formatearEmail("test@mail.com")` retorna `"TEST@MAIL.COM"`
- [ ] `primerElemento(null)` retorna `null`
- [ ] `primerElemento(emptyList())` retorna `null`
- [ ] `primerElemento(listOf(1, 2, 3))` retorna `1`

---

## Ejercicio 2: Data Classes

### Instrucciones

1. Crea una data class `Producto` con:
   - `id: Int`
   - `nombre: String`
   - `precio: Double`
   - `enStock: Boolean` (por defecto `true`)

2. Crea una data class `Carrito` con:
   - `productos: List<Producto>`
   - Una función `total()` que calcule el precio total

3. Escribe código que:
   - Cree 3 productos
   - Cree un carrito con esos productos
   - Imprima el total
   - Cree una copia del primer producto con precio rebajado

### Criterios de aceptación

- [ ] `Producto` es una data class
- [ ] `Carrito` tiene función `total()`
- [ ] El total se calcula correctamente
- [ ] Usas `copy()` para crear el producto rebajado

---

## Ejercicio 3: Colecciones

### Instrucciones

Dada la siguiente lista de usuarios:

```kotlin
data class Usuario(
    val id: Int,
    val nombre: String,
    val edad: Int,
    val ciudad: String,
    val activo: Boolean
)

val usuarios = listOf(
    Usuario(1, "Ana", 28, "Madrid", true),
    Usuario(2, "Luis", 17, "Barcelona", true),
    Usuario(3, "María", 35, "Madrid", false),
    Usuario(4, "Pedro", 22, "Valencia", true),
    Usuario(5, "Carmen", 19, "Madrid", true),
    Usuario(6, "Juan", 45, "Barcelona", false),
    Usuario(7, "Laura", 31, "Valencia", true)
)
```

Escribe expresiones que obtengan:

1. Lista de usuarios activos mayores de edad (≥18)
2. Lista de nombres de usuarios de Madrid
3. Usuario más joven
4. ¿Hay algún usuario de Sevilla?
5. Número de usuarios por ciudad (Map<String, Int>)
6. Lista de usuarios ordenada por edad descendente
7. Suma de edades de usuarios activos

### Criterios de aceptación

- [ ] Usas operaciones funcionales (filter, map, etc.)
- [ ] No usas bucles for
- [ ] Los resultados son correctos

---

## Ejercicio 4: Scope Functions

### Instrucciones

Refactoriza el siguiente código usando scope functions apropiadas:

```kotlin
// Código a refactorizar

// 1. Configuración de objeto
val configuracion = Configuracion()
configuracion.servidor = "api.example.com"
configuracion.puerto = 8080
configuracion.timeout = 30
configuracion.debug = true

// 2. Ejecución condicional
val usuario: Usuario? = obtenerUsuario()
if (usuario != null) {
    println("Usuario encontrado: ${usuario.nombre}")
    procesarUsuario(usuario)
}

// 3. Logging con retorno
val resultado = calcularResultado()
println("Resultado calculado: $resultado")
return resultado
```

### Criterios de aceptación

- [ ] El código 1 usa `apply`
- [ ] El código 2 usa `let`
- [ ] El código 3 usa `also`
- [ ] El comportamiento es el mismo que el original

---

## Ejercicio 5: Sealed Classes

### Instrucciones

1. Crea una sealed class `EstadoPedido` con los siguientes estados:
   - `Pendiente` (sin datos adicionales)
   - `Procesando` (con `progreso: Int` de 0 a 100)
   - `Enviado` (con `codigoSeguimiento: String`)
   - `Entregado` (con `fechaEntrega: String`)
   - `Cancelado` (con `motivo: String`)

2. Implementa una función `mostrarEstado(estado: EstadoPedido): String` que retorne un mensaje descriptivo para cada estado.

3. Crea ejemplos de cada estado y prueba la función.

### Criterios de aceptación

- [ ] `EstadoPedido` es una sealed class
- [ ] Cada estado tiene los datos indicados
- [ ] `mostrarEstado` usa `when` exhaustivo (sin `else`)
- [ ] Los mensajes son descriptivos

---

## Ejercicio 6: Extension Functions

### Instrucciones

Crea las siguientes extension functions:

```kotlin
// 1. Para String: capitaliza cada palabra
// "hola mundo" -> "Hola Mundo"
fun String.capitalizarPalabras(): String

// 2. Para List<Int>: retorna solo los números en un rango
// listOf(1, 5, 10, 15, 20).enRango(5, 15) -> [5, 10, 15]
fun List<Int>.enRango(min: Int, max: Int): List<Int>

// 3. Para Int: formatea como moneda
// 1234.formatoMoneda("€") -> "1.234 €"
fun Int.formatoMoneda(simbolo: String): String
```

### Criterios de aceptación

- [ ] Las 3 funciones están implementadas
- [ ] `"hola mundo".capitalizarPalabras()` retorna `"Hola Mundo"`
- [ ] `listOf(1, 5, 10, 15, 20).enRango(5, 15)` retorna `[5, 10, 15]`
- [ ] `1234.formatoMoneda("€")` retorna `"1.234 €"` (o formato similar)

---

## Ejercicio 7 (Bonus): Función de orden superior

### Instrucciones

Implementa una función `reintentar` que:
- Recibe un número máximo de intentos
- Recibe un bloque de código que puede fallar (lanzar excepción)
- Ejecuta el bloque hasta que tenga éxito o se agoten los intentos
- Retorna el resultado si tiene éxito, o null si falla todos los intentos

```kotlin
fun <T> reintentar(maxIntentos: Int, bloque: () -> T): T? {
    // Tu código
}

// Uso:
val resultado = reintentar(3) {
    llamadaQuePodriaFallar()
}
```

### Criterios de aceptación

- [ ] La función es genérica (`<T>`)
- [ ] Reintenta el número correcto de veces
- [ ] Retorna el resultado si tiene éxito
- [ ] Retorna null si falla todos los intentos
- [ ] No lanza excepciones al exterior

---

## Entrega

1. Crea un archivo Kotlin con todas las soluciones
2. Incluye una función `main` que pruebe cada ejercicio
3. Crea una rama y abre PR como se indica en el flujo de trabajo
