# Guía COMPLETA del Proyecto **Todo Compose** — Para el Profesor

Esta guía está diseñada para que **tú como profesor entiendas TODO** lo que hace el proyecto, línea por línea, y puedas explicarlo con confianza a tus alumnos.

> Proyecto base: `projects/todo-compose/starter`

---

## ÍNDICE DE LA GUÍA

1. [Visión General del Proyecto](#1-visión-general-del-proyecto)
2. [Arquitectura y Patrón MVVM](#2-arquitectura-y-patrón-mvvm)
3. [Estructura de Archivos Explicada](#3-estructura-de-archivos-explicada)
4. [CAPA DOMINIO: Los Modelos](#4-capa-dominio-los-modelos-domain)
5. [CAPA DATOS: Room y Repository](#5-capa-datos-room-y-repository-data)
6. [CAPA UI: Pantallas y Componentes](#6-capa-ui-pantallas-y-componentes-ui)
7. [Punto de Entrada: MainActivity y Application](#7-punto-de-entrada-mainactivity-y-application)
8. [Gradle: Configuración del Proyecto](#8-gradle-configuración-del-proyecto)
9. [Flujo Completo: De un Click a la Base de Datos](#9-flujo-completo-de-un-click-a-la-base-de-datos)
10. [Guion para la Clase (2 horas)](#10-guion-para-la-clase-2-horas)
11. [Ejercicio Práctico Guiado](#11-ejercicio-práctico-guiado)

---

## 1) Visión General del Proyecto

### ¿Qué es esta app?

Una aplicación de **lista de tareas (To-Do List)** que permite:
- ✅ Crear tareas con título, descripción, prioridad y fecha límite
- ✅ Ver todas las tareas, solo pendientes o solo completadas
- ✅ Marcar tareas como completadas/pendientes (checkbox)
- ✅ Editar tareas existentes
- ✅ Eliminar tareas deslizando (swipe)
- ✅ Eliminar todas las completadas desde el menú
- ✅ Los datos se guardan en base de datos local (Room)

### Tecnologías que usa

| Tecnología | Qué hace | Por qué se usa |
|------------|----------|----------------|
| **Kotlin** | Lenguaje de programación | Lenguaje oficial de Android, más moderno que Java |
| **Jetpack Compose** | Framework de UI | UI declarativa, más simple que XML |
| **Material 3** | Diseño visual | Estilo moderno de Google |
| **MVVM** | Arquitectura | Separa lógica de UI, facilita testing |
| **Room** | Base de datos | Abstracción sobre SQLite, más fácil de usar |
| **StateFlow** | Estado reactivo | La UI se actualiza automáticamente al cambiar datos |
| **Coroutines** | Asincronía | Operaciones de BD sin bloquear la UI |
| **Navigation Compose** | Navegación | Moverse entre pantallas |

### Al terminar la clase, el alumno debe saber:

1. Abrir y ejecutar un proyecto Android moderno en emulador
2. Entender la **estructura** de un proyecto Android y qué hace Gradle
3. Recorrer el flujo **UI → ViewModel → Repository → Room**
4. Implementar una mejora pequeña tocando todas las capas

---

## 2) Arquitectura y Patrón MVVM

### ¿Qué es MVVM?

**Model-View-ViewModel** es un patrón de arquitectura que separa la aplicación en tres capas:

```
┌─────────────────────────────────────────────────────────────────┐
│                         UI (View)                                │
│  HomeScreen.kt, EditScreen.kt, componentes Compose               │
│  → Solo dibuja la pantalla según el estado que recibe            │
│  → Envía eventos al ViewModel (clicks, texto, etc.)              │
└─────────────────────────┬───────────────────────────────────────┘
                          │ observa estado / envía eventos
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ViewModel                                   │
│  HomeViewModel.kt, EditViewModel.kt                              │
│  → Mantiene el estado de la UI (uiState)                         │
│  → Contiene la lógica de presentación                            │
│  → Transforma datos del Repository para la UI                    │
│  → Sobrevive a rotaciones de pantalla                            │
└─────────────────────────┬───────────────────────────────────────┘
                          │ llama métodos / observa flujos
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Repository                                  │
│  TodoRepository.kt                                               │
│  → Punto único de acceso a datos                                 │
│  → Puede combinar múltiples fuentes (BD local, API, etc.)        │
│  → Convierte Entity ↔ Domain model                               │
└─────────────────────────┬───────────────────────────────────────┘
                          │ queries SQL
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Room (DAO + Database)                       │
│  TodoDao.kt, TodoDatabase.kt, TodoEntity.kt                      │
│  → Persiste datos en SQLite                                      │
│  → Expone Flows reactivos (se actualizan automáticamente)        │
└─────────────────────────────────────────────────────────────────┘
```

### ¿Por qué esta arquitectura?

| Problema sin MVVM | Solución con MVVM |
|-------------------|-------------------|
| UI mezclada con lógica de negocio | Cada capa tiene una responsabilidad clara |
| Difícil de testear | ViewModel se puede testear sin UI |
| Bug en un sitio rompe todo | Cambios aislados en cada capa |
| Estado perdido al rotar | ViewModel sobrevive a cambios de configuración |

### Regla de oro para explicar a los alumnos:

> **"La UI NUNCA habla con la base de datos directamente. La UI habla con el ViewModel, el ViewModel con el Repository, y el Repository con Room."**

---

## 3) Estructura de Archivos Explicada

```
app/src/main/java/com/example/todocompose/
│
├── MainActivity.kt          ← Punto de entrada de la app
├── TodoApplication.kt       ← Configuración global (instancia la BD)
│
├── domain/                  ← CAPA DOMINIO: Modelos de negocio puros
│   └── model/
│       ├── Todo.kt          ← Modelo que usa toda la app
│       └── Priority.kt      ← Enum de prioridades (HIGH, MEDIUM, LOW)
│
├── data/                    ← CAPA DATOS: Acceso a base de datos
│   ├── local/
│   │   ├── entity/
│   │   │   └── TodoEntity.kt    ← Cómo se guarda en la BD (tabla)
│   │   ├── TodoDao.kt           ← Queries SQL (interfaz)
│   │   └── TodoDatabase.kt      ← Configuración de Room
│   └── repository/
│       └── TodoRepository.kt    ← Punto único de acceso a datos
│
└── ui/                      ← CAPA UI: Todo lo visual
    ├── theme/               ← Colores, tipografía, estilos
    │   ├── Color.kt
    │   ├── Theme.kt
    │   └── Type.kt
    ├── components/          ← Componentes reutilizables
    │   ├── TodoItem.kt      ← Tarjeta de una tarea
    │   └── PriorityDropdown.kt  ← Selector de prioridad
    ├── navigation/
    │   └── NavGraph.kt      ← Rutas y navegación entre pantallas
    └── screens/             ← Pantallas de la app
        ├── home/            ← Pantalla principal (lista)
        │   ├── HomeScreen.kt
        │   ├── HomeViewModel.kt
        │   └── HomeUiState.kt
        └── edit/            ← Pantalla crear/editar
            ├── EditScreen.kt
            ├── EditViewModel.kt
            └── EditUiState.kt
```

---

## 4) CAPA DOMINIO: Los Modelos (domain/)

Esta es la capa más simple pero MUY importante. Define **qué es una tarea** para toda la aplicación.

### 4.1) Priority.kt — El enum de prioridades

**Archivo:** `domain/model/Priority.kt`

```kotlin
package com.example.todocompose.domain.model

enum class Priority {
    HIGH,      // ordinal = 0
    MEDIUM,    // ordinal = 1
    LOW;       // ordinal = 2
    
    companion object {
        fun fromOrdinal(ordinal: Int): Priority {
            return entries.getOrElse(ordinal) { MEDIUM }
        }
    }
}
```

**Explicación línea por línea:**

| Línea | Qué hace | Para qué sirve |
|-------|----------|----------------|
| `enum class Priority` | Define un tipo con valores fijos | Solo puede ser HIGH, MEDIUM o LOW, nada más |
| `HIGH, MEDIUM, LOW` | Los tres valores posibles | Kotlin les asigna un número (ordinal): HIGH=0, MEDIUM=1, LOW=2 |
| `companion object` | Bloque de métodos estáticos | Se pueden llamar como `Priority.fromOrdinal(1)` sin crear instancia |
| `fun fromOrdinal(ordinal: Int)` | Convierte un número a Priority | Útil porque en la BD guardamos números, no objetos |
| `entries.getOrElse(ordinal) { MEDIUM }` | Busca el valor por posición | Si el número no existe, devuelve MEDIUM por defecto |

**¿Por qué usamos ordinal en la BD?**
- Room (SQLite) solo puede guardar tipos básicos: Int, String, Long, etc.
- No puede guardar objetos Kotlin directamente
- Solución: guardamos el número (0, 1, 2) y lo convertimos de vuelta al leer

### 4.2) Todo.kt — El modelo de tarea

**Archivo:** `domain/model/Todo.kt`

```kotlin
package com.example.todocompose.domain.model

import java.time.LocalDate

data class Todo(
    val id: Int = 0,
    val title: String,
    val description: String = "",
    val isCompleted: Boolean = false,
    val priority: Priority = Priority.MEDIUM,
    val dueDate: LocalDate? = null,
    val createdAt: LocalDate = LocalDate.now()
)
```

**Explicación de cada propiedad:**

| Propiedad | Tipo | Qué representa | Valor por defecto |
|-----------|------|----------------|-------------------|
| `id` | `Int` | Identificador único en BD | 0 (Room lo genera automáticamente si es 0) |
| `title` | `String` | Título de la tarea | — (obligatorio, sin valor por defecto) |
| `description` | `String` | Descripción opcional | "" (cadena vacía) |
| `isCompleted` | `Boolean` | ¿Está completada? | false (nueva tarea = no completada) |
| `priority` | `Priority` | Prioridad (enum) | MEDIUM (prioridad por defecto) |
| `dueDate` | `LocalDate?` | Fecha límite | null (sin fecha = sin presión) |
| `createdAt` | `LocalDate` | Cuándo se creó | Fecha actual (`LocalDate.now()`) |

**¿Por qué `data class`?**

Una `data class` en Kotlin genera automáticamente:
- `equals()`: compara todos los campos
- `hashCode()`: para usar en colecciones
- `toString()`: imprime los valores bonito
- `copy()`: crea una copia modificando solo algunos campos

Ejemplo de `copy()` que usamos mucho:
```kotlin
val tarea = Todo(id = 1, title = "Comprar leche")
val tareaCompletada = tarea.copy(isCompleted = true)  // Cambia solo isCompleted
```

**¿Por qué `LocalDate` y no `Date`?**
- `LocalDate` es la API moderna de Java 8+ (más limpia y sin problemas de zonas horarias)
- Solo fecha (día/mes/año), sin hora ni timezone
- `Date` de Java antiguo tiene muchos bugs y está deprecado

---

## 5) CAPA DATOS: Room y Repository (data/)

Esta capa maneja TODO lo relacionado con guardar y leer datos.

### 5.1) TodoEntity.kt — La tabla de la base de datos

**Archivo:** `data/local/entity/TodoEntity.kt`

```kotlin
package com.example.todocompose.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.example.todocompose.domain.model.Priority
import com.example.todocompose.domain.model.Todo
import java.time.LocalDate

@Entity(tableName = "todos")
data class TodoEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val title: String,
    val description: String = "",
    val isCompleted: Boolean = false,
    val priority: Int = Priority.MEDIUM.ordinal,  // ← Guardamos número, no enum
    val dueDate: Long? = null,                     // ← Guardamos milisegundos, no LocalDate
    val createdAt: Long = System.currentTimeMillis()
) {
    // Método para convertir de Entity (BD) a Domain (app)
    fun toDomain(): Todo = Todo(
        id = id,
        title = title,
        description = description,
        isCompleted = isCompleted,
        priority = Priority.fromOrdinal(priority),              // Int → Priority
        dueDate = dueDate?.let { LocalDate.ofEpochDay(it) },   // Long → LocalDate
        createdAt = LocalDate.ofEpochDay(createdAt / (24 * 60 * 60 * 1000))
    )
    
    companion object {
        // Método para convertir de Domain (app) a Entity (BD)
        fun fromDomain(todo: Todo): TodoEntity = TodoEntity(
            id = todo.id,
            title = todo.title,
            description = todo.description,
            isCompleted = todo.isCompleted,
            priority = todo.priority.ordinal,                   // Priority → Int
            dueDate = todo.dueDate?.toEpochDay(),              // LocalDate → Long
            createdAt = todo.createdAt.toEpochDay() * 24 * 60 * 60 * 1000
        )
    }
}
```

**Anotaciones de Room explicadas:**

| Anotación | Qué hace |
|-----------|----------|
| `@Entity(tableName = "todos")` | Esta clase = tabla "todos" en SQLite |
| `@PrimaryKey(autoGenerate = true)` | El campo `id` es la clave primaria, Room la genera automáticamente |

**¿Por qué Entity es diferente de Todo?**

| Aspecto | Entity (para BD) | Todo (para la app) |
|---------|------------------|-------------------|
| Prioridad | `Int` (número) | `Priority` (enum) |
| Fechas | `Long` (milisegundos/días) | `LocalDate` (objeto fecha) |
| Propósito | Solo lo que SQLite entiende | Lo que es cómodo para la app |

**Métodos de conversión (MUY IMPORTANTES):**

1. `toDomain()`: Convierte Entity → Todo (cuando LEEMOS de la BD)
   ```kotlin
   val entity = TodoEntity(id=1, title="Comprar", priority=0, ...)
   val todo = entity.toDomain()  // → Todo(id=1, title="Comprar", priority=HIGH, ...)
   ```

2. `fromDomain()`: Convierte Todo → Entity (cuando ESCRIBIMOS en la BD)
   ```kotlin
   val todo = Todo(id=1, title="Comprar", priority=Priority.HIGH, ...)
   val entity = TodoEntity.fromDomain(todo)  // → TodoEntity(id=1, title="Comprar", priority=0, ...)
   ```

**Cálculos de fechas explicados:**

```kotlin
// De Long (días desde 1970) a LocalDate
LocalDate.ofEpochDay(dueDate)  // ej: 19000 → 2022-01-15

// De LocalDate a Long (días desde 1970)
fecha.toEpochDay()  // ej: 2022-01-15 → 19000

// 24 * 60 * 60 * 1000 = 86400000 = milisegundos en un día
createdAt / (24 * 60 * 60 * 1000)  // convierte millis a días
```

### 5.2) TodoDao.kt — Las queries SQL

**Archivo:** `data/local/TodoDao.kt`

```kotlin
package com.example.todocompose.data.local

import androidx.room.*
import com.example.todocompose.data.local.entity.TodoEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface TodoDao {
    
    // ========== QUERIES DE LECTURA (retornan Flow) ==========
    
    @Query("SELECT * FROM todos ORDER BY isCompleted ASC, priority ASC, dueDate ASC")
    fun observeAll(): Flow<List<TodoEntity>>
    
    @Query("SELECT * FROM todos WHERE isCompleted = 0 ORDER BY priority ASC, dueDate ASC")
    fun observePending(): Flow<List<TodoEntity>>
    
    @Query("SELECT * FROM todos WHERE isCompleted = 1 ORDER BY priority ASC, dueDate ASC")
    fun observeCompleted(): Flow<List<TodoEntity>>
    
    @Query("SELECT * FROM todos WHERE id = :todoId")
    suspend fun getById(todoId: Int): TodoEntity?
    
    // ========== OPERACIONES DE ESCRITURA (suspend) ==========
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(todo: TodoEntity): Long
    
    @Update
    suspend fun update(todo: TodoEntity)
    
    @Delete
    suspend fun delete(todo: TodoEntity)
    
    @Query("DELETE FROM todos WHERE id = :todoId")
    suspend fun deleteById(todoId: Int)
    
    @Query("UPDATE todos SET isCompleted = :isCompleted WHERE id = :todoId")
    suspend fun updateCompleted(todoId: Int, isCompleted: Boolean)
    
    @Query("DELETE FROM todos WHERE isCompleted = 1")
    suspend fun deleteCompleted()
}
```

**Conceptos clave explicados:**

| Concepto | Explicación detallada |
|----------|----------------------|
| `@Dao` | Data Access Object: interfaz donde defines las operaciones de BD. Room genera la implementación |
| `@Query("SQL")` | Ejecuta la query SQL que pongas. Room valida la sintaxis EN TIEMPO DE COMPILACIÓN |
| `Flow<List<T>>` | Flujo reactivo: cada vez que cambian los datos en la tabla, emite una lista nueva automáticamente |
| `suspend` | Función que se ejecuta en coroutine (no bloquea el hilo principal) |
| `:todoId` | Parámetro de la query. Se reemplaza por el valor del argumento de la función |

**¿Por qué `Flow` en lectura y `suspend` en escritura?**

- **Lectura con Flow**: Queremos que la UI se actualice AUTOMÁTICAMENTE cuando cambian los datos
  ```kotlin
  // Esto se dispara cada vez que alguien añade/borra/modifica una tarea
  todoDao.observeAll().collect { listaDeTareas ->
      // actualizar UI
  }
  ```

- **Escritura con suspend**: Son operaciones puntuales que hacemos y ya está
  ```kotlin
  // Ejecuta, guarda, terminó
  todoDao.insert(nuevaTarea)
  ```

**Explicación de las queries SQL:**

```sql
-- Todas las tareas, ordenadas primero no completadas, luego por prioridad, luego por fecha
SELECT * FROM todos 
ORDER BY isCompleted ASC, priority ASC, dueDate ASC

-- isCompleted ASC: 0 (no completadas) antes que 1 (completadas)
-- priority ASC: 0 (HIGH) antes que 1 (MEDIUM) antes que 2 (LOW)
-- dueDate ASC: las que vencen antes, primero
```

```sql
-- Solo tareas pendientes (isCompleted = 0 significa false)
SELECT * FROM todos WHERE isCompleted = 0
```

```sql
-- Actualizar solo el campo isCompleted de una tarea específica
UPDATE todos SET isCompleted = :isCompleted WHERE id = :todoId
```

**Estrategia de conflicto en Insert:**

```kotlin
@Insert(onConflict = OnConflictStrategy.REPLACE)
suspend fun insert(todo: TodoEntity): Long
```

Si intentas insertar con un `id` que ya existe, REEMPLAZA el registro existente (actúa como update).

### 5.3) TodoDatabase.kt — Configuración de Room

**Archivo:** `data/local/TodoDatabase.kt`

```kotlin
package com.example.todocompose.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.example.todocompose.data.local.entity.TodoEntity

@Database(
    entities = [TodoEntity::class],    // Lista de tablas (solo una en este proyecto)
    version = 1,                        // Versión del esquema de BD
    exportSchema = false                // No exportar esquema a archivo JSON
)
abstract class TodoDatabase : RoomDatabase() {
    
    // Room implementa este método automáticamente
    abstract fun todoDao(): TodoDao
    
    companion object {
        @Volatile    // Asegura visibilidad inmediata entre hilos
        private var INSTANCE: TodoDatabase? = null
        
        // Patrón Singleton: solo UNA instancia de la BD en toda la app
        fun getDatabase(context: Context): TodoDatabase {
            // Si ya existe, la devolvemos
            return INSTANCE ?: synchronized(this) {
                // Si no existe, la creamos (solo un hilo puede entrar aquí)
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    TodoDatabase::class.java,
                    "todo_database"    // Nombre del archivo .db en el dispositivo
                )
                .fallbackToDestructiveMigration()  // Si cambias version, borra y recrea
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
```

**Conceptos explicados:**

| Concepto | Explicación |
|----------|-------------|
| `@Database(entities=[...], version=1)` | Configura la BD: qué tablas tiene y versión del esquema |
| `exportSchema = false` | No genera archivo JSON del esquema (lo ponemos false para simplificar) |
| `abstract fun todoDao()` | Room genera la implementación real del DAO |
| `@Volatile` | Cuando un hilo cambia INSTANCE, los demás lo ven inmediatamente |
| `synchronized(this)` | Solo un hilo puede ejecutar este bloque a la vez (evita crear 2 instancias) |
| `fallbackToDestructiveMigration()` | Si cambias la versión del esquema, Room BORRA la BD y la recrea (pierdes datos pero es simple) |

**¿Por qué Singleton?**

- Crear una BD es COSTOSO (abre conexiones, archivos, etc.)
- Queremos UNA ÚNICA instancia compartida en toda la app
- Room maneja las conexiones internas eficientemente si usamos singleton

### 5.4) TodoRepository.kt — El punto único de acceso

**Archivo:** `data/repository/TodoRepository.kt`

```kotlin
package com.example.todocompose.data.repository

import com.example.todocompose.data.local.TodoDao
import com.example.todocompose.data.local.entity.TodoEntity
import com.example.todocompose.domain.model.Todo
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class TodoRepository(private val todoDao: TodoDao) {
    
    // ========== OBSERVAR LISTAS (Flow que transforma Entity → Todo) ==========
    
    fun observeAllTodos(): Flow<List<Todo>> {
        return todoDao.observeAll().map { entities ->
            entities.map { it.toDomain() }    // Convierte CADA Entity a Todo
        }
    }
    
    fun observePendingTodos(): Flow<List<Todo>> {
        return todoDao.observePending().map { entities ->
            entities.map { it.toDomain() }
        }
    }
    
    fun observeCompletedTodos(): Flow<List<Todo>> {
        return todoDao.observeCompleted().map { entities ->
            entities.map { it.toDomain() }
        }
    }
    
    // ========== OPERACIONES PUNTUALES (suspend que convierte Todo → Entity) ==========
    
    suspend fun getTodoById(id: Int): Todo? {
        return todoDao.getById(id)?.toDomain()
    }
    
    suspend fun addTodo(todo: Todo): Long {
        return todoDao.insert(TodoEntity.fromDomain(todo))
    }
    
    suspend fun updateTodo(todo: Todo) {
        todoDao.update(TodoEntity.fromDomain(todo))
    }
    
    suspend fun deleteTodo(todo: Todo) {
        todoDao.delete(TodoEntity.fromDomain(todo))
    }
    
    suspend fun deleteTodoById(id: Int) {
        todoDao.deleteById(id)
    }
    
    suspend fun toggleTodoCompleted(id: Int, isCompleted: Boolean) {
        todoDao.updateCompleted(id, isCompleted)
    }
    
    suspend fun deleteCompletedTodos() {
        todoDao.deleteCompleted()
    }
}
```

**¿Por qué existe el Repository?**

1. **Abstracción**: El ViewModel NO SABE si los datos vienen de Room, de una API REST, de memoria, etc.
2. **Conversión centralizada**: Toda conversión Entity ↔ Todo pasa por aquí
3. **Punto único**: Si mañana cambias Room por otra BD, solo tocas el Repository
4. **Futuro**: Si añades sincronización con servidor, el Repository combina ambas fuentes

**El operador `.map { }` en Flow:**

```kotlin
todoDao.observeAll()           // Flow<List<TodoEntity>>
    .map { entities ->         // Transforma el Flow
        entities.map {         // Transforma la lista
            it.toDomain()      // Transforma cada elemento
        }
    }                          // Resultado: Flow<List<Todo>>
```

---

## 6) CAPA UI: Pantallas y Componentes (ui/)

### 6.1) HomeUiState.kt — El estado de la pantalla principal

**Archivo:** `ui/screens/home/HomeUiState.kt`

```kotlin
package com.example.todocompose.ui.screens.home

import com.example.todocompose.domain.model.Todo

data class HomeUiState(
    val todos: List<Todo> = emptyList(),   // Lista de tareas a mostrar
    val isLoading: Boolean = false,         // ¿Está cargando?
    val error: String? = null,              // Mensaje de error (null = sin error)
    val filter: TodoFilter = TodoFilter.ALL // Filtro actual
)

enum class TodoFilter {
    ALL,        // Todas las tareas
    PENDING,    // Solo no completadas
    COMPLETED   // Solo completadas
}
```

**¿Por qué un UiState?**

- **Una única fuente de verdad**: Todo lo que la pantalla necesita está aquí
- **Inmutable**: Usamos `data class` y nunca mutamos, solo creamos copias
- **Predecible**: Dado un UiState, la UI siempre se ve igual

### 6.2) HomeViewModel.kt — La lógica de la pantalla principal

**Archivo:** `ui/screens/home/HomeViewModel.kt`

```kotlin
package com.example.todocompose.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.todocompose.data.repository.TodoRepository
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class HomeViewModel(
    private val repository: TodoRepository
) : ViewModel() {
    
    // Estado interno del filtro (mutable, privado)
    private val _filter = MutableStateFlow(TodoFilter.ALL)
    
    // Estado de la UI (inmutable, público)
    val uiState: StateFlow<HomeUiState> = _filter.flatMapLatest { filter ->
        // Cuando cambia el filtro, observamos la lista correspondiente
        when (filter) {
            TodoFilter.ALL -> repository.observeAllTodos()
            TodoFilter.PENDING -> repository.observePendingTodos()
            TodoFilter.COMPLETED -> repository.observeCompletedTodos()
        }.map { todos ->
            // Transformamos la lista de tareas en un UiState completo
            HomeUiState(todos = todos, filter = filter)
        }
    }.stateIn(
        scope = viewModelScope,           // Vive mientras viva el ViewModel
        started = SharingStarted.WhileSubscribed(5000),  // Se para 5s después de que nadie observe
        initialValue = HomeUiState(isLoading = true)     // Valor inicial mientras carga
    )
    
    // ========== ACCIONES (la UI llama estos métodos) ==========
    
    fun setFilter(filter: TodoFilter) {
        _filter.value = filter
    }
    
    fun toggleTodoCompleted(todoId: Int, isCompleted: Boolean) {
        viewModelScope.launch {
            repository.toggleTodoCompleted(todoId, isCompleted)
        }
    }
    
    fun deleteTodo(todoId: Int) {
        viewModelScope.launch {
            repository.deleteTodoById(todoId)
        }
    }
    
    fun deleteCompletedTodos() {
        viewModelScope.launch {
            repository.deleteCompletedTodos()
        }
    }
}
```

**Conceptos clave explicados:**

| Concepto | Explicación detallada |
|----------|----------------------|
| `ViewModel` | Clase que sobrevive a rotaciones de pantalla. La UI puede destruirse y recrearse, pero el ViewModel sigue ahí |
| `viewModelScope` | Scope de coroutines que se cancela automáticamente cuando el ViewModel se destruye |
| `MutableStateFlow` | Flow que guarda un valor y emite cada vez que cambia. El `_filter` empieza con ALL |
| `StateFlow` | Versión de solo lectura de MutableStateFlow. Lo exponemos a la UI |
| `flatMapLatest` | Cuando el filtro cambia, CANCELA el flow anterior y empieza uno nuevo |
| `stateIn()` | Convierte un Flow frío en un StateFlow caliente con valor inicial |

**¿Qué hace `flatMapLatest`?**

```
Tiempo →

_filter:  ALL ─────────────── PENDING ────────── COMPLETED ──────
                    ↓               ↓                  ↓
observa:     observeAll()    observePending()   observeCompleted()
                    ↓               ↓                  ↓
emite:        [t1, t2, t3]      [t1, t3]           [t2]
```

Cuando el usuario cambia el filtro, `flatMapLatest`:
1. CANCELA la suscripción al flow anterior (ej: `observeAll`)
2. Se suscribe al nuevo flow (ej: `observePending`)
3. La UI recibe la nueva lista automáticamente

**¿Por qué `viewModelScope.launch {}` en las acciones?**

Las operaciones de BD son `suspend`, necesitan ejecutarse en una coroutine:

```kotlin
fun deleteTodo(todoId: Int) {
    viewModelScope.launch {           // Lanza coroutine
        repository.deleteTodoById(todoId)  // Ejecuta en segundo plano
    }                                 // No bloquea la UI
}
```

### 6.3) HomeScreen.kt — La pantalla principal (Compose)

**Archivo:** `ui/screens/home/HomeScreen.kt`

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    viewModel: HomeViewModel,
    onAddTodo: () -> Unit,        // Callback: ir a crear tarea
    onEditTodo: (Int) -> Unit     // Callback: ir a editar tarea (recibe id)
) {
    // Observamos el estado del ViewModel (se re-renderiza cuando cambia)
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    var showMenu by remember { mutableStateOf(false) }  // Estado local del menú
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Mis Tareas") },
                actions = {
                    IconButton(onClick = { showMenu = true }) {
                        Icon(Icons.Default.MoreVert, contentDescription = "Menú")
                    }
                    DropdownMenu(
                        expanded = showMenu,
                        onDismissRequest = { showMenu = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("Eliminar completadas") },
                            onClick = {
                                viewModel.deleteCompletedTodos()
                                showMenu = false
                            }
                        )
                    }
                }
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = onAddTodo) {
                Icon(Icons.Default.Add, contentDescription = "Añadir tarea")
            }
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            // Pestañas de filtro
            FilterTabs(
                currentFilter = uiState.filter,
                onFilterChange = viewModel::setFilter  // Referencia al método
            )
            
            // Contenido según estado
            if (uiState.isLoading) {
                // Estado: Cargando
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            } else if (uiState.todos.isEmpty()) {
                // Estado: Lista vacía
                EmptyState(filter = uiState.filter)
            } else {
                // Estado: Lista con tareas
                TodoList(
                    todos = uiState.todos,
                    onTodoClick = onEditTodo,
                    onToggleCompleted = viewModel::toggleTodoCompleted,
                    onDelete = viewModel::deleteTodo
                )
            }
        }
    }
}
```

**Conceptos de Compose explicados:**

| Concepto | Explicación |
|----------|-------------|
| `@Composable` | Función que puede usar el sistema de UI de Compose |
| `by viewModel.uiState.collectAsStateWithLifecycle()` | Observa el StateFlow y se recompone cuando cambia. "WithLifecycle" evita memory leaks |
| `remember { mutableStateOf() }` | Estado local que sobrevive a recomposiciones |
| `Scaffold` | Estructura básica de Material: TopAppBar + contenido + FAB |
| `modifier = Modifier.xxx()` | Encadena propiedades de estilo (padding, tamaño, etc.) |

**El flujo de datos en Compose:**

```
uiState cambia → Compose detecta el cambio → Re-ejecuta HomeScreen
                         ↓
              Solo redibuja lo que cambió (eficiente)
```

### 6.4) TodoList y SwipeToDismiss — Lista con gestos

```kotlin
@Composable
private fun TodoList(
    todos: List<Todo>,
    onTodoClick: (Int) -> Unit,
    onToggleCompleted: (Int, Boolean) -> Unit,
    onDelete: (Int) -> Unit
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(vertical = 8.dp)
    ) {
        items(
            items = todos,
            key = { it.id }  // Optimización: Compose identifica cada item por id
        ) { todo ->
            // Estado del gesto de deslizar
            val dismissState = rememberSwipeToDismissBoxState(
                confirmValueChange = { dismissValue ->
                    if (dismissValue == SwipeToDismissBoxValue.EndToStart) {
                        onDelete(todo.id)  // Deslizó hacia la izquierda → borrar
                        true               // Confirmar el dismiss
                    } else {
                        false              // No permitir otras direcciones
                    }
                }
            )
            
            SwipeToDismissBox(
                state = dismissState,
                backgroundContent = {
                    // Fondo rojo que aparece al deslizar
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .background(MaterialTheme.colorScheme.error),
                        contentAlignment = Alignment.CenterEnd
                    ) {
                        Icon(Icons.Default.Delete, tint = Color.White)
                    }
                },
                enableDismissFromStartToEnd = false  // Solo derecha a izquierda
            ) {
                TodoItem(
                    todo = todo,
                    onClick = { onTodoClick(todo.id) },
                    onCheckedChange = { onToggleCompleted(todo.id, it) }
                )
            }
        }
    }
}
```

**LazyColumn vs Column:**

| Column | LazyColumn |
|--------|------------|
| Crea TODOS los items al inicio | Crea solo los visibles |
| Malo para listas largas | Perfecto para listas largas |
| Equivalente a LinearLayout | Equivalente a RecyclerView |

**¿Por qué `key = { it.id }`?**

- Compose usa la key para identificar cada item
- Si reordenas la lista, Compose mueve los items en vez de recrearlos
- IMPORTANTE para animaciones y rendimiento

### 6.5) EditViewModel.kt — Lógica de crear/editar

**Archivo:** `ui/screens/edit/EditViewModel.kt`

```kotlin
class EditViewModel(
    private val repository: TodoRepository,
    private val todoId: Int?    // null = crear nuevo, número = editar existente
) : ViewModel() {
    
    private val _uiState = MutableStateFlow(EditUiState(todoId = todoId))
    val uiState: StateFlow<EditUiState> = _uiState.asStateFlow()
    
    init {
        // Si estamos editando, cargamos la tarea existente
        if (todoId != null) {
            loadTodo(todoId)
        }
    }
    
    private fun loadTodo(id: Int) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            try {
                val todo = repository.getTodoById(id)
                if (todo != null) {
                    _uiState.update {
                        it.copy(
                            title = todo.title,
                            description = todo.description,
                            priority = todo.priority,
                            dueDate = todo.dueDate,
                            isLoading = false
                        )
                    }
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }
    
    // Métodos para actualizar cada campo
    fun updateTitle(title: String) {
        _uiState.update { it.copy(title = title) }
    }
    
    fun updateDescription(description: String) {
        _uiState.update { it.copy(description = description) }
    }
    
    fun updatePriority(priority: Priority) {
        _uiState.update { it.copy(priority = priority) }
    }
    
    fun updateDueDate(date: LocalDate?) {
        _uiState.update { it.copy(dueDate = date) }
    }
    
    // Guardar (crear o actualizar)
    fun save() {
        val state = _uiState.value
        if (!state.isValid) return
        
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            try {
                val todo = Todo(
                    id = state.todoId ?: 0,  // 0 = Room genera id nuevo
                    title = state.title.trim(),
                    description = state.description.trim(),
                    priority = state.priority,
                    dueDate = state.dueDate
                )
                
                if (state.isEditing) {
                    repository.updateTodo(todo)
                } else {
                    repository.addTodo(todo)
                }
                
                _uiState.update { it.copy(isSaved = true) }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }
}
```

**Patrón `.update { it.copy(...) }`:**

```kotlin
_uiState.update { currentState ->
    currentState.copy(title = nuevoTitulo)  // Crea copia con title cambiado
}
```

- `update` es atómico (thread-safe)
- `copy` crea una nueva instancia, no muta la existente
- Perfecto para estado inmutable

### 6.6) NavGraph.kt — Navegación entre pantallas

**Archivo:** `ui/navigation/NavGraph.kt`

```kotlin
object Routes {
    const val HOME = "home"
    const val EDIT = "edit"
    const val EDIT_ARG = "todoId"
    const val EDIT_WITH_ARG = "edit?todoId={todoId}"
}

@Composable
fun TodoNavGraph() {
    val navController = rememberNavController()
    val context = LocalContext.current
    val application = context.applicationContext as TodoApplication
    val repository = TodoRepository(application.database.todoDao())
    
    NavHost(
        navController = navController,
        startDestination = Routes.HOME
    ) {
        // Pantalla Home
        composable(Routes.HOME) {
            val viewModel: HomeViewModel = viewModel {
                HomeViewModel(repository)
            }
            HomeScreen(
                viewModel = viewModel,
                onAddTodo = {
                    navController.navigate(Routes.EDIT)  // Sin id = crear nueva
                },
                onEditTodo = { todoId ->
                    navController.navigate("${Routes.EDIT}?todoId=$todoId")  // Con id = editar
                }
            )
        }
        
        // Pantalla Edit (crear o editar)
        composable(
            route = Routes.EDIT_WITH_ARG,
            arguments = listOf(
                navArgument(Routes.EDIT_ARG) {
                    type = NavType.IntType
                    defaultValue = -1    // -1 significa "crear nuevo"
                }
            )
        ) { backStackEntry ->
            val todoId = backStackEntry.arguments?.getInt(Routes.EDIT_ARG) ?: -1
            val viewModel: EditViewModel = viewModel {
                EditViewModel(repository, if (todoId == -1) null else todoId)
            }
            EditScreen(
                viewModel = viewModel,
                onNavigateBack = {
                    navController.popBackStack()  // Volver a la pantalla anterior
                }
            )
        }
    }
}
```

**Navegación explicada:**

| Acción | URL de navegación | todoId en EditViewModel |
|--------|-------------------|------------------------|
| Crear tarea nueva | `edit` | null |
| Editar tarea id=5 | `edit?todoId=5` | 5 |

**¿Por qué `defaultValue = -1`?**

- Navigation Compose necesita un valor por defecto para argumentos opcionales
- Usamos -1 como "no hay id"
- En EditViewModel: `-1` se convierte a `null` (crear nuevo)

### 6.7) TodoItem.kt — Componente de tarea individual

**Archivo:** `ui/components/TodoItem.kt`

```kotlin
@Composable
fun TodoItem(
    todo: Todo,
    onClick: () -> Unit,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp)
            .clickable(onClick = onClick),  // Click en toda la tarjeta
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Checkbox para marcar completada
            Checkbox(
                checked = todo.isCompleted,
                onCheckedChange = onCheckedChange
            )
            
            Spacer(modifier = Modifier.width(12.dp))
            
            // Contenido de la tarea
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = todo.title,
                    style = MaterialTheme.typography.titleMedium,
                    // Si está completada, tachamos el texto
                    textDecoration = if (todo.isCompleted) TextDecoration.LineThrough else null,
                    color = if (todo.isCompleted) {
                        MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
                    } else {
                        MaterialTheme.colorScheme.onSurface
                    }
                )
                
                // Descripción (solo si existe)
                if (todo.description.isNotBlank()) {
                    Text(
                        text = todo.description,
                        style = MaterialTheme.typography.bodyMedium,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                
                // Fecha límite (solo si existe)
                todo.dueDate?.let { date ->
                    Text(
                        text = date.format(DateTimeFormatter.ofPattern("dd/MM/yyyy")),
                        style = MaterialTheme.typography.labelSmall
                    )
                }
            }
            
            // Indicador de prioridad (círculo de color)
            PriorityIndicator(priority = todo.priority)
        }
    }
}
```

**Conceptos importantes:**

- `modifier.clickable(onClick)`: Hace que toda la Card sea clickeable
- `Modifier.weight(1f)`: El Column ocupa todo el espacio disponible
- `TextDecoration.LineThrough`: Tacha el texto de tareas completadas
- `.copy(alpha = 0.5f)`: Hace el color semi-transparente

### 6.8) Color.kt — Colores del tema

**Archivo:** `ui/theme/Color.kt`

```kotlin
package com.example.todocompose.ui.theme

import androidx.compose.ui.graphics.Color

// Colores Material 3
val Purple80 = Color(0xFFD0BCFF)
val PurpleGrey80 = Color(0xFFCCC2DC)
val Pink80 = Color(0xFFEFB8C8)

val Purple40 = Color(0xFF6650a4)
val PurpleGrey40 = Color(0xFF625b71)
val Pink40 = Color(0xFF7D5260)

// Colores de prioridad
val PriorityHigh = Color(0xFFE53935)   // Rojo
val PriorityMedium = Color(0xFFFFA726) // Naranja
val PriorityLow = Color(0xFF66BB6A)    // Verde
```

---

## 7) Punto de Entrada: MainActivity y Application

### 7.1) TodoApplication.kt — Configuración global

**Archivo:** `TodoApplication.kt`

```kotlin
package com.example.todocompose

import android.app.Application
import com.example.todocompose.data.local.TodoDatabase

class TodoApplication : Application() {
    
    // Lazy: la BD se crea la primera vez que se accede
    val database: TodoDatabase by lazy {
        TodoDatabase.getDatabase(this)
    }
}
```

**¿Qué es una Application?**
- Clase que Android crea ANTES que cualquier Activity
- Vive durante toda la vida de la app
- Perfecto para inicializar cosas globales como la BD

**`by lazy`:**
```kotlin
val database: TodoDatabase by lazy { ... }
```
- No ejecuta el bloque hasta que alguien acceda a `database`
- Después de la primera vez, devuelve el mismo valor (singleton)

**IMPORTANTE:** Debes registrar esta clase en `AndroidManifest.xml`:
```xml
<application
    android:name=".TodoApplication"
    ... >
```

### 7.2) MainActivity.kt — Punto de entrada de la UI

**Archivo:** `MainActivity.kt`

```kotlin
package com.example.todocompose

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import com.example.todocompose.ui.navigation.TodoNavGraph
import com.example.todocompose.ui.theme.TodoComposeTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()  // UI va hasta los bordes de la pantalla
        setContent {
            TodoComposeTheme {  // Aplica el tema (colores, tipografía)
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    TodoNavGraph()  // Arranca la navegación (empieza en Home)
                }
            }
        }
    }
}
```

**Flujo de arranque:**

```
1. Android crea TodoApplication
2. Android crea MainActivity
3. onCreate() llama a setContent { }
4. Compose renderiza TodoNavGraph
5. NavGraph inicia en Routes.HOME
6. HomeScreen se muestra
```

---

## 8) Gradle: Configuración del Proyecto

### 8.1) app/build.gradle.kts — Configuración del módulo

```kotlin
plugins {
    id("com.android.application")           // Es una app (no librería)
    id("org.jetbrains.kotlin.android")      // Kotlin para Android
    id("com.google.devtools.ksp")           // Procesador de anotaciones (para Room)
}

android {
    namespace = "com.example.todocompose"   // Paquete base
    compileSdk = 34                          // SDK para compilar (última estable)

    defaultConfig {
        applicationId = "com.example.todocompose"  // ID único en Play Store
        minSdk = 26         // Mínimo Android 8.0 (para LocalDate)
        targetSdk = 34      // Optimizado para Android 14
        versionCode = 1     // Número de versión (para Play Store)
        versionName = "1.0.0"  // Versión legible
    }

    buildFeatures {
        compose = true      // Habilita Jetpack Compose
    }
}

dependencies {
    // Compose (UI)
    implementation(platform("androidx.compose:compose-bom:2024.01.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.material3:material3")
    
    // Navigation
    implementation("androidx.navigation:navigation-compose:2.7.6")
    
    // ViewModel
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    
    // Room (BD)
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    ksp("androidx.room:room-compiler:2.6.1")   // KSP genera código de Room
    
    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
}
```

**¿Qué es KSP y por qué lo usa Room?**

- **KSP** = Kotlin Symbol Processing
- Room usa anotaciones (`@Entity`, `@Dao`, etc.)
- KSP lee esas anotaciones y GENERA código Kotlin automáticamente
- El código generado está en `build/generated/ksp/`

---

## 9) Flujo Completo: De un Click a la Base de Datos

### Ejemplo: El usuario marca una tarea como completada

```
1. USUARIO: Marca el checkbox de la tarea id=5

2. UI (TodoItem.kt):
   Checkbox(
       checked = todo.isCompleted,
       onCheckedChange = { onToggleCompleted(todo.id, it) }  // Llama callback
   )
   
3. UI (HomeScreen.kt):
   TodoList(
       onToggleCompleted = viewModel::toggleTodoCompleted  // Pasa al ViewModel
   )

4. VIEWMODEL (HomeViewModel.kt):
   fun toggleTodoCompleted(todoId: Int, isCompleted: Boolean) {
       viewModelScope.launch {
           repository.toggleTodoCompleted(todoId, isCompleted)
       }
   }

5. REPOSITORY (TodoRepository.kt):
   suspend fun toggleTodoCompleted(id: Int, isCompleted: Boolean) {
       todoDao.updateCompleted(id, isCompleted)
   }

6. DAO (TodoDao.kt):
   @Query("UPDATE todos SET isCompleted = :isCompleted WHERE id = :todoId")
   suspend fun updateCompleted(todoId: Int, isCompleted: Boolean)

7. ROOM ejecuta el SQL en la BD

8. AUTOMÁTICAMENTE (porque usamos Flow):
   - Room detecta que la tabla cambió
   - Emite una nueva lista por observeAll()
   - Repository transforma Entity → Todo
   - ViewModel actualiza uiState
   - Compose detecta el cambio
   - La UI se redibuja con el checkbox actualizado
```

---

## 10) Guion para la Clase (2 horas)

### Preparación antes de la clase (10 min antes)

- [ ] Android Studio abierto con `projects/todo-compose/starter`
- [ ] Gradle Sync completado
- [ ] Emulador arrancado (o móvil conectado)
- [ ] Zoom del editor al 125-150%
- [ ] Notificaciones desactivadas

### 0:00-0:10 — Introducción

**Qué decir:**
> "Hoy vamos a ver un proyecto Android completo con Compose. Vamos a ejecutarlo, entender su arquitectura MVVM, y hacer una pequeña mejora."

**Mostrar:**
- La app corriendo en emulador
- Crear una tarea, marcarla, deslizar para borrar

### 0:10-0:30 — Estructura del proyecto

**Recorrido:**
1. Abrir la carpeta en el explorador de Android Studio
2. Explicar la estructura de carpetas (domain, data, ui)
3. Abrir `build.gradle.kts` y explicar las dependencias

**Concepto clave:**
> "La UI no habla con la BD. La UI habla con el ViewModel, el ViewModel con el Repository, y el Repository con Room."

### 0:30-0:50 — Capa de datos (Room)

**Archivos a abrir:**
1. `Todo.kt` - El modelo que usamos en la app
2. `TodoEntity.kt` - Cómo se guarda en BD
3. `TodoDao.kt` - Las queries SQL
4. `TodoRepository.kt` - El puente

**Demo visual:**
- Crear una tarea y mostrar que aparece en la lista
- Explicar: "Room notifica al Repository, que notifica al ViewModel, que notifica a la UI"

### 0:50-1:10 — Capa UI (Compose)

**Archivos a abrir:**
1. `HomeUiState.kt` - Todo lo que la pantalla necesita
2. `HomeViewModel.kt` - La lógica
3. `HomeScreen.kt` - La UI

**Concepto clave:**
> "La UI es una función del estado. Si cambia el estado, Compose redibuja automáticamente."

### 1:10-1:30 — El flujo completo

**Hacer una demostración en vivo:**
1. Poner breakpoints en:
   - `HomeScreen` donde se llama a `onToggleCompleted`
   - `HomeViewModel.toggleTodoCompleted`
   - `TodoDao.updateCompleted`
2. Marcar un checkbox y seguir el flujo

### 1:30-1:50 — Ejercicio práctico (búsqueda)

Ver sección 11.

### 1:50-2:00 — Resumen y tarea para casa

**Resumen en 6 frases:**
1. Gradle configura el proyecto y dependencias
2. Compose pinta UI a partir de estado
3. ViewModel guarda estado y lógica de UI
4. Repository centraliza acceso a datos
5. Room persiste y expone flujos reactivos
6. Una feature real toca varias capas

**Tarea para casa (elegir 1):**
- Añadir confirmación antes de borrar
- Añadir Snackbar con "deshacer" al borrar
- Añadir filtro por prioridad

---

## 11) Ejercicio Práctico Guiado

### Objetivo: Añadir búsqueda por título

Tocaremos: **UI → ViewModel → Repository → DAO**

### Paso 1: Añadir campo de búsqueda en HomeScreen

**Archivo:** `ui/screens/home/HomeScreen.kt`

**Añadir antes de FilterTabs:**
```kotlin
// Campo de búsqueda
OutlinedTextField(
    value = uiState.searchQuery,
    onValueChange = viewModel::setSearchQuery,
    label = { Text("Buscar") },
    modifier = Modifier
        .fillMaxWidth()
        .padding(16.dp),
    singleLine = true
)
```

### Paso 2: Añadir searchQuery al UiState

**Archivo:** `ui/screens/home/HomeUiState.kt`

```kotlin
data class HomeUiState(
    val todos: List<Todo> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val filter: TodoFilter = TodoFilter.ALL,
    val searchQuery: String = ""  // ← AÑADIR ESTO
)
```

### Paso 3: Añadir lógica en ViewModel

**Archivo:** `ui/screens/home/HomeViewModel.kt`

**Añadir:**
```kotlin
private val _searchQuery = MutableStateFlow("")

fun setSearchQuery(query: String) {
    _searchQuery.value = query
}
```

**Modificar la construcción de uiState para combinar filter + query:**
```kotlin
val uiState: StateFlow<HomeUiState> = combine(_filter, _searchQuery) { filter, query ->
    Pair(filter, query)
}.flatMapLatest { (filter, query) ->
    when (filter) {
        TodoFilter.ALL -> repository.observeAllTodos(query)
        TodoFilter.PENDING -> repository.observePendingTodos(query)
        TodoFilter.COMPLETED -> repository.observeCompletedTodos(query)
    }.map { todos ->
        HomeUiState(todos = todos, filter = filter, searchQuery = query)
    }
}.stateIn(...)
```

### Paso 4: Añadir parámetro query en Repository

**Archivo:** `data/repository/TodoRepository.kt`

```kotlin
fun observeAllTodos(query: String = ""): Flow<List<Todo>> {
    return if (query.isBlank()) {
        todoDao.observeAll()
    } else {
        todoDao.searchAll("%$query%")  // % = wildcard en SQL
    }.map { entities ->
        entities.map { it.toDomain() }
    }
}
```

### Paso 5: Añadir query en DAO

**Archivo:** `data/local/TodoDao.kt`

```kotlin
@Query("SELECT * FROM todos WHERE title LIKE :query ORDER BY isCompleted ASC, priority ASC")
fun searchAll(query: String): Flow<List<TodoEntity>>

@Query("SELECT * FROM todos WHERE title LIKE :query AND isCompleted = 0 ORDER BY priority ASC")
fun searchPending(query: String): Flow<List<TodoEntity>>

@Query("SELECT * FROM todos WHERE title LIKE :query AND isCompleted = 1 ORDER BY priority ASC")
fun searchCompleted(query: String): Flow<List<TodoEntity>>
```

### Paso 6: Probar

1. Ejecutar la app
2. Crear tareas: "Comprar leche", "Comprar pan", "Llamar al médico"
3. Buscar "Comprar" → solo aparecen las dos primeras

---

## Rutas rápidas de archivos

| Qué es | Ruta |
|--------|------|
| Proyecto | `projects/todo-compose/starter` |
| Gradle módulo | `app/build.gradle.kts` |
| MainActivity | `app/src/main/java/.../MainActivity.kt` |
| Modelo Todo | `app/src/main/java/.../domain/model/Todo.kt` |
| Entity | `app/src/main/java/.../data/local/entity/TodoEntity.kt` |
| DAO | `app/src/main/java/.../data/local/TodoDao.kt` |
| Repository | `app/src/main/java/.../data/repository/TodoRepository.kt` |
| HomeScreen | `app/src/main/java/.../ui/screens/home/HomeScreen.kt` |
| HomeViewModel | `app/src/main/java/.../ui/screens/home/HomeViewModel.kt` |
| EditScreen | `app/src/main/java/.../ui/screens/edit/EditScreen.kt` |
| NavGraph | `app/src/main/java/.../ui/navigation/NavGraph.kt` |

