# Lección 02: Kotlin Essentials

## Objetivos

- Dominar la sintaxis básica de Kotlin
- Entender y aplicar null safety
- Trabajar con colecciones de forma funcional
- Usar data classes correctamente
- Aplicar scope functions (let, run, apply, also, with)

---

## 1. Variables y tipos

### val vs var

```kotlin
val nombre = "Juan"       // Inmutable (recomendado)
var contador = 0          // Mutable

nombre = "Pedro"          // ❌ Error: val no se puede reasignar
contador = 1              // ✅ OK
```

**Regla:** Usa `val` por defecto. Solo usa `var` cuando necesites reasignar.

### Tipos básicos

```kotlin
val entero: Int = 42
val decimal: Double = 3.14
val texto: String = "Hola"
val booleano: Boolean = true
val caracter: Char = 'A'
val largo: Long = 1_000_000L
val flotante: Float = 3.14f
```

### Inferencia de tipos

```kotlin
val nombre = "Juan"       // Kotlin infiere String
val edad = 25             // Kotlin infiere Int
val precio = 19.99        // Kotlin infiere Double
```

---

## 2. Null Safety

Kotlin diferencia entre tipos nullables y no-nullables.

### Tipos nullable

```kotlin
var nombre: String = "Juan"    // No puede ser null
var apellido: String? = null   // Puede ser null

nombre = null    // ❌ Error de compilación
apellido = null  // ✅ OK
```

### Operador safe call (?.)

```kotlin
val longitud = apellido?.length  // Si apellido es null, longitud = null
```

### Operador Elvis (?:)

```kotlin
val longitud = apellido?.length ?: 0  // Si es null, usa 0
```

### Operador not-null assertion (!!)

```kotlin
val longitud = apellido!!.length  // ⚠️ Lanza excepción si es null
```

**Regla:** Evita `!!`. Indica que no has manejado bien el null.

### Smart casts

```kotlin
fun procesar(texto: String?) {
    if (texto != null) {
        // Aquí texto es String (no nullable)
        println(texto.length)
    }
}
```

---

## 3. Funciones

### Declaración básica

```kotlin
fun sumar(a: Int, b: Int): Int {
    return a + b
}
```

### Función de una expresión

```kotlin
fun sumar(a: Int, b: Int): Int = a + b

// El tipo de retorno se puede inferir
fun sumar(a: Int, b: Int) = a + b
```

### Parámetros por defecto

```kotlin
fun saludar(nombre: String, saludo: String = "Hola") {
    println("$saludo, $nombre!")
}

saludar("Juan")              // "Hola, Juan!"
saludar("Juan", "Buenos días") // "Buenos días, Juan!"
```

### Parámetros nombrados

```kotlin
fun crearUsuario(nombre: String, edad: Int, email: String) { ... }

// Puedes cambiar el orden usando nombres
crearUsuario(
    email = "juan@mail.com",
    nombre = "Juan",
    edad = 25
)
```

---

## 4. Lambdas

### Sintaxis básica

```kotlin
val sumar: (Int, Int) -> Int = { a, b -> a + b }

val resultado = sumar(2, 3)  // 5
```

### Lambda como último parámetro

```kotlin
fun ejecutar(veces: Int, accion: () -> Unit) {
    repeat(veces) { accion() }
}

// Se puede sacar fuera de los paréntesis
ejecutar(3) {
    println("Hola")
}
```

### it implícito

```kotlin
val numeros = listOf(1, 2, 3)
val dobles = numeros.map { it * 2 }  // it = cada elemento
```

---

## 5. Clases

### Clase básica

```kotlin
class Persona(val nombre: String, var edad: Int) {
    fun cumpleanos() {
        edad++
    }
}

val persona = Persona("Juan", 25)
println(persona.nombre)  // Juan
persona.cumpleanos()
println(persona.edad)    // 26
```

### Data class

```kotlin
data class Usuario(
    val id: Int,
    val nombre: String,
    val email: String
)

val user1 = Usuario(1, "Juan", "juan@mail.com")
val user2 = user1.copy(nombre = "Pedro")  // Copia con cambios

// equals, hashCode, toString generados automáticamente
println(user1)  // Usuario(id=1, nombre=Juan, email=juan@mail.com)
```

**Usa data class cuando:**
- La clase solo guarda datos
- Necesitas equals/hashCode/toString
- Necesitas copy()

### Object (Singleton)

```kotlin
object ConfiguracionApp {
    val apiUrl = "https://api.example.com"
    var debugMode = false
}

println(ConfiguracionApp.apiUrl)
```

### Companion object

```kotlin
class Usuario(val nombre: String) {
    companion object {
        fun crear(json: String): Usuario {
            // parsear JSON
            return Usuario("parsed")
        }
    }
}

val user = Usuario.crear("{...}")
```

---

## 6. Colecciones

### Tipos de colecciones

```kotlin
// Lista inmutable
val lista = listOf(1, 2, 3)

// Lista mutable
val listaMutable = mutableListOf(1, 2, 3)
listaMutable.add(4)

// Set (sin duplicados)
val set = setOf(1, 2, 2, 3)  // {1, 2, 3}

// Map
val mapa = mapOf("a" to 1, "b" to 2)
println(mapa["a"])  // 1
```

### Operaciones funcionales

```kotlin
val numeros = listOf(1, 2, 3, 4, 5)

// filter - filtra elementos
val pares = numeros.filter { it % 2 == 0 }  // [2, 4]

// map - transforma elementos
val dobles = numeros.map { it * 2 }  // [2, 4, 6, 8, 10]

// find - encuentra el primero que cumple
val primeroMayor3 = numeros.find { it > 3 }  // 4

// firstOrNull - como find pero más explícito
val primero = numeros.firstOrNull { it > 10 }  // null

// any - ¿alguno cumple?
val hayPares = numeros.any { it % 2 == 0 }  // true

// all - ¿todos cumplen?
val todosPositivos = numeros.all { it > 0 }  // true

// none - ¿ninguno cumple?
val ningunoNegativo = numeros.none { it < 0 }  // true

// sumOf - suma con transformación
val suma = numeros.sumOf { it * 2 }  // 30

// groupBy - agrupa por clave
val porParidad = numeros.groupBy { if (it % 2 == 0) "par" else "impar" }
// {impar=[1, 3, 5], par=[2, 4]}

// sortedBy - ordena
val ordenados = numeros.sortedByDescending { it }  // [5, 4, 3, 2, 1]
```

### Encadenamiento

```kotlin
val resultado = usuarios
    .filter { it.edad >= 18 }
    .sortedBy { it.nombre }
    .map { it.email }
    .take(10)
```

---

## 7. Scope Functions

### let

```kotlin
// Ejecuta bloque si no es null
val longitud = nombre?.let {
    println("Procesando: $it")
    it.length
}

// Transformación con null safety
val resultado = obtenerUsuario()?.let { user ->
    "Usuario: ${user.nombre}"
}
```

### run

```kotlin
// Ejecuta bloque y retorna resultado
val resultado = servicio.run {
    configurar()
    ejecutar()
    obtenerResultado()
}
```

### apply

```kotlin
// Configura objeto y lo retorna
val usuario = Usuario().apply {
    nombre = "Juan"
    edad = 25
    email = "juan@mail.com"
}
```

### also

```kotlin
// Ejecuta efecto secundario y retorna el objeto
val numeros = mutableListOf(1, 2, 3).also {
    println("Lista creada con ${it.size} elementos")
}
```

### with

```kotlin
// Opera sobre objeto sin repetir el nombre
with(usuario) {
    println(nombre)
    println(edad)
    println(email)
}
```

### Resumen

| Función | Referencia al objeto | Retorna |
|---------|---------------------|---------|
| `let` | `it` | Resultado del lambda |
| `run` | `this` | Resultado del lambda |
| `apply` | `this` | El objeto |
| `also` | `it` | El objeto |
| `with` | `this` | Resultado del lambda |

---

## 8. Extension Functions

```kotlin
// Añade función a una clase existente
fun String.quitarEspacios(): String {
    return this.replace(" ", "")
}

val texto = "Hola Mundo".quitarEspacios()  // "HolaMundo"

// Extension con nullable
fun String?.orEmpty(): String = this ?: ""

val nombre: String? = null
println(nombre.orEmpty())  // ""
```

---

## 9. Sealed Classes

```kotlin
sealed class Resultado {
    data class Exito(val datos: String) : Resultado()
    data class Error(val mensaje: String) : Resultado()
    object Cargando : Resultado()
}

fun procesar(resultado: Resultado) {
    when (resultado) {
        is Resultado.Exito -> println(resultado.datos)
        is Resultado.Error -> println(resultado.mensaje)
        Resultado.Cargando -> println("Cargando...")
        // No necesita else - el when es exhaustivo
    }
}
```

**Uso principal:** Modelar estados finitos (muy útil para UI state).

---

## Resumen

| Concepto | Cuándo usar |
|----------|-------------|
| `val` vs `var` | `val` por defecto, `var` solo si necesitas mutar |
| `?` nullable | Cuando el valor puede ser null |
| `?.` safe call | Acceder a miembros de nullable |
| `?:` Elvis | Valor por defecto si es null |
| `data class` | Clases que solo guardan datos |
| `sealed class` | Estados finitos, tipos cerrados |
| `let` | Transformar nullable, ejecutar si no es null |
| `apply` | Configurar objeto (builder pattern) |
| `filter/map` | Transformar colecciones |

---

## Siguiente paso

→ [ejercicios.md](ejercicios.md)
