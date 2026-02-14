# Soluciones - Lección 02: Kotlin Essentials

## Ejercicio 1: Null Safety

```kotlin
// 1. Retorna la longitud del string, o 0 si es null
fun longitudSegura(texto: String?): Int {
    return texto?.length ?: 0
}

// 2. Retorna el email en mayúsculas, o "NO EMAIL" si es null
fun formatearEmail(email: String?): String {
    return email?.uppercase() ?: "NO EMAIL"
}

// 3. Retorna el primer elemento, o null si la lista está vacía o es null
fun <T> primerElemento(lista: List<T>?): T? {
    return lista?.firstOrNull()
}
```

### Explicación

- **`?.`** (safe call): Solo ejecuta si no es null
- **`?:`** (Elvis): Proporciona valor por defecto si es null
- **`firstOrNull()`**: Retorna el primer elemento o null si está vacía

---

## Ejercicio 2: Data Classes

```kotlin
data class Producto(
    val id: Int,
    val nombre: String,
    val precio: Double,
    val enStock: Boolean = true
)

data class Carrito(
    val productos: List<Producto>
) {
    fun total(): Double = productos.sumOf { it.precio }
}

fun main() {
    val producto1 = Producto(1, "Laptop", 999.99)
    val producto2 = Producto(2, "Mouse", 29.99)
    val producto3 = Producto(3, "Teclado", 79.99)

    val carrito = Carrito(listOf(producto1, producto2, producto3))

    println("Total: ${carrito.total()} €")  // 1109.97 €

    val productoRebajado = producto1.copy(precio = 799.99)
    println("Producto rebajado: $productoRebajado")
}
```

### Explicación

- **`data class`**: Genera automáticamente `equals`, `hashCode`, `toString`, `copy`
- **`sumOf`**: Suma aplicando una transformación a cada elemento
- **`copy()`**: Crea una copia con los campos especificados modificados

---

## Ejercicio 3: Colecciones

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

fun main() {
    // 1. Usuarios activos mayores de edad
    val activosMayores = usuarios.filter { it.activo && it.edad >= 18 }
    println("1. Activos mayores: ${activosMayores.map { it.nombre }}")
    // [Ana, Pedro, Carmen, Laura]

    // 2. Nombres de usuarios de Madrid
    val nombresMadrid = usuarios
        .filter { it.ciudad == "Madrid" }
        .map { it.nombre }
    println("2. De Madrid: $nombresMadrid")
    // [Ana, María, Carmen]

    // 3. Usuario más joven
    val masJoven = usuarios.minByOrNull { it.edad }
    println("3. Más joven: ${masJoven?.nombre}")
    // Luis

    // 4. ¿Hay algún usuario de Sevilla?
    val haySevilla = usuarios.any { it.ciudad == "Sevilla" }
    println("4. ¿Hay de Sevilla?: $haySevilla")
    // false

    // 5. Número de usuarios por ciudad
    val porCiudad = usuarios.groupingBy { it.ciudad }.eachCount()
    println("5. Por ciudad: $porCiudad")
    // {Madrid=3, Barcelona=2, Valencia=2}

    // 6. Ordenados por edad descendente
    val ordenadosPorEdad = usuarios.sortedByDescending { it.edad }
    println("6. Por edad desc: ${ordenadosPorEdad.map { "${it.nombre}(${it.edad})" }}")
    // [Juan(45), María(35), Laura(31), Ana(28), Pedro(22), Carmen(19), Luis(17)]

    // 7. Suma de edades de usuarios activos
    val sumaEdadesActivos = usuarios
        .filter { it.activo }
        .sumOf { it.edad }
    println("7. Suma edades activos: $sumaEdadesActivos")
    // 28 + 17 + 22 + 19 + 31 = 117
}
```

---

## Ejercicio 4: Scope Functions

```kotlin
// 1. Configuración de objeto - usar apply
val configuracion = Configuracion().apply {
    servidor = "api.example.com"
    puerto = 8080
    timeout = 30
    debug = true
}

// 2. Ejecución condicional - usar let
obtenerUsuario()?.let { usuario ->
    println("Usuario encontrado: ${usuario.nombre}")
    procesarUsuario(usuario)
}

// 3. Logging con retorno - usar also
return calcularResultado().also {
    println("Resultado calculado: $it")
}
```

### Explicación

- **`apply`**: Configura un objeto y lo retorna. Usa `this`.
- **`let`**: Ejecuta bloque si no es null. Usa `it`.
- **`also`**: Ejecuta efecto secundario y retorna el objeto. Usa `it`.

---

## Ejercicio 5: Sealed Classes

```kotlin
sealed class EstadoPedido {
    object Pendiente : EstadoPedido()
    data class Procesando(val progreso: Int) : EstadoPedido()
    data class Enviado(val codigoSeguimiento: String) : EstadoPedido()
    data class Entregado(val fechaEntrega: String) : EstadoPedido()
    data class Cancelado(val motivo: String) : EstadoPedido()
}

fun mostrarEstado(estado: EstadoPedido): String {
    return when (estado) {
        is EstadoPedido.Pendiente -> 
            "Tu pedido está pendiente de procesamiento"
        is EstadoPedido.Procesando -> 
            "Tu pedido se está procesando (${estado.progreso}%)"
        is EstadoPedido.Enviado -> 
            "Tu pedido ha sido enviado. Código: ${estado.codigoSeguimiento}"
        is EstadoPedido.Entregado -> 
            "Tu pedido fue entregado el ${estado.fechaEntrega}"
        is EstadoPedido.Cancelado -> 
            "Tu pedido fue cancelado. Motivo: ${estado.motivo}"
    }
}

fun main() {
    val estados = listOf(
        EstadoPedido.Pendiente,
        EstadoPedido.Procesando(45),
        EstadoPedido.Enviado("ES123456789"),
        EstadoPedido.Entregado("15/01/2026"),
        EstadoPedido.Cancelado("Stock agotado")
    )

    estados.forEach { println(mostrarEstado(it)) }
}
```

### Explicación

- **`sealed class`**: Restringe las subclases a las definidas en el mismo archivo
- **`when` exhaustivo**: El compilador verifica que cubrimos todos los casos
- **`object`**: Para estados sin datos (singleton)
- **`data class`**: Para estados con datos

---

## Ejercicio 6: Extension Functions

```kotlin
// 1. Capitalizar cada palabra
fun String.capitalizarPalabras(): String {
    return split(" ")
        .joinToString(" ") { palabra ->
            palabra.lowercase().replaceFirstChar { it.uppercase() }
        }
}

// 2. Números en rango
fun List<Int>.enRango(min: Int, max: Int): List<Int> {
    return filter { it in min..max }
}

// 3. Formato moneda
fun Int.formatoMoneda(simbolo: String): String {
    val formatted = toString()
        .reversed()
        .chunked(3)
        .joinToString(".")
        .reversed()
    return "$formatted $simbolo"
}

fun main() {
    println("hola mundo".capitalizarPalabras())  
    // Hola Mundo

    println(listOf(1, 5, 10, 15, 20).enRango(5, 15))  
    // [5, 10, 15]

    println(1234.formatoMoneda("€"))  
    // 1.234 €

    println(1234567.formatoMoneda("€"))  
    // 1.234.567 €
}
```

---

## Ejercicio 7 (Bonus): Función de orden superior

```kotlin
fun <T> reintentar(maxIntentos: Int, bloque: () -> T): T? {
    repeat(maxIntentos) { intento ->
        try {
            return bloque()
        } catch (e: Exception) {
            println("Intento ${intento + 1} fallido: ${e.message}")
        }
    }
    return null
}

// Ejemplo de uso
fun main() {
    var contador = 0

    val resultado = reintentar(3) {
        contador++
        if (contador < 3) {
            throw Exception("Fallo intencional")
        }
        "¡Éxito!"
    }

    println("Resultado: $resultado")  // Resultado: ¡Éxito!
}
```

### Explicación

- **`repeat(n)`**: Ejecuta el bloque n veces
- **`try-catch`**: Captura excepciones para reintentar
- **`return bloque()`**: Sale de la función con el resultado si tiene éxito
- **`return null`**: Retorna null si se agotan los intentos

---

## Errores comunes

### Error: Smart cast imposible

```kotlin
var nombre: String? = "Juan"

if (nombre != null) {
    println(nombre.length)  // ❌ Error si nombre es var
}
```

**Causa:** `var` puede cambiar entre el check y el uso.

**Solución:**
```kotlin
val nombreLocal = nombre
if (nombreLocal != null) {
    println(nombreLocal.length)
}

// O mejor:
nombre?.let { println(it.length) }
```

### Error: when no exhaustivo

```kotlin
sealed class Estado { ... }

fun procesar(estado: Estado) = when (estado) {
    is Estado.Exito -> "ok"
    // ❌ Error: falta cubrir otros casos
}
```

**Solución:** Cubre todos los casos o añade `else`.

### Error: ConcurrentModificationException

```kotlin
val lista = mutableListOf(1, 2, 3)
for (item in lista) {
    if (item == 2) lista.remove(item)  // ❌ Error
}
```

**Solución:**
```kotlin
val lista = mutableListOf(1, 2, 3)
lista.removeAll { it == 2 }

// O:
val nuevaLista = lista.filter { it != 2 }
```
