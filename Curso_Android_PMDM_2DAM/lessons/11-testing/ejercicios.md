# Ejercicios - Lección 11: Testing

## Ejercicio 1: Tests unitarios básicos

### Instrucciones

Crea una clase `StringUtils` y testéala.

### Métodos a implementar

```kotlin
object StringUtils {
    fun reverseString(input: String): String
    fun isPalindrome(input: String): Boolean
    fun countWords(input: String): Int
    fun capitalizeWords(input: String): String
}
```

### Tests requeridos

- reverseString con string normal, vacío, un carácter
- isPalindrome con palíndromo, no palíndromo, case insensitive
- countWords con texto normal, múltiples espacios, vacío
- capitalizeWords casos varios

### Criterios de aceptación

- [ ] Mínimo 12 tests
- [ ] Todos pasan
- [ ] Nombres descriptivos
- [ ] Cubrir edge cases

---

## Ejercicio 2: Tests de ViewModel simple

### Instrucciones

Testea el siguiente ViewModel:

```kotlin
data class TodoItem(val id: Int, val text: String, val isDone: Boolean)

class TodoViewModel : ViewModel() {
    private val _todos = MutableStateFlow<List<TodoItem>>(emptyList())
    val todos: StateFlow<List<TodoItem>> = _todos.asStateFlow()
    
    fun addTodo(text: String)
    fun toggleTodo(id: Int)
    fun deleteTodo(id: Int)
    fun clearCompleted()
}
```

### Tests requeridos

- addTodo añade item correctamente
- toggleTodo cambia isDone
- deleteTodo elimina item
- clearCompleted elimina solo completados
- Estado inicial vacío

### Criterios de aceptación

- [ ] Mínimo 8 tests
- [ ] Usa MainDispatcherRule
- [ ] Tests independientes

---

## Ejercicio 3: Tests con Fake Repository

### Instrucciones

Implementa y testea con un FakeRepository.

### Repository interface

```kotlin
interface ProductRepository {
    fun observeProducts(): Flow<List<Product>>
    suspend fun getProduct(id: Int): Product?
    suspend fun addProduct(product: Product)
    suspend fun deleteProduct(id: Int)
}
```

### Crear FakeProductRepository

```kotlin
class FakeProductRepository : ProductRepository {
    // Implementar con lista en memoria
}
```

### ViewModel a testear

```kotlin
class ProductViewModel(repository: ProductRepository) : ViewModel() {
    val products: StateFlow<List<Product>>
    val isLoading: StateFlow<Boolean>
    
    fun loadProducts()
    fun deleteProduct(id: Int)
}
```

### Criterios de aceptación

- [ ] FakeRepository implementado
- [ ] Mínimo 6 tests de ViewModel
- [ ] Usa Turbine para flows

---

## Ejercicio 4: Tests de UI con Compose

### Instrucciones

Testea el siguiente composable:

```kotlin
@Composable
fun LoginScreen(
    email: String,
    password: String,
    isLoading: Boolean,
    error: String?,
    onEmailChange: (String) -> Unit,
    onPasswordChange: (String) -> Unit,
    onLoginClick: () -> Unit
)
```

### Tests requeridos

- Campos de email y password visibles
- Botón login deshabilitado si campos vacíos
- Loading indicator visible cuando isLoading = true
- Error message visible cuando error != null
- Click en login trigger callback
- Input text funciona

### Criterios de aceptación

- [ ] Mínimo 6 tests de UI
- [ ] Usa testTag donde sea útil
- [ ] Tests claros y legibles

---

## Ejercicio 5: Tests de Room DAO

### Instrucciones

Testea el siguiente DAO:

```kotlin
@Dao
interface NoteDao {
    @Query("SELECT * FROM notes ORDER BY created_at DESC")
    fun observeAll(): Flow<List<NoteEntity>>
    
    @Query("SELECT * FROM notes WHERE id = :noteId")
    suspend fun getById(noteId: Int): NoteEntity?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(note: NoteEntity): Long
    
    @Update
    suspend fun update(note: NoteEntity)
    
    @Query("DELETE FROM notes WHERE id = :noteId")
    suspend fun deleteById(noteId: Int)
    
    @Query("SELECT * FROM notes WHERE title LIKE '%' || :query || '%'")
    fun search(query: String): Flow<List<NoteEntity>>
}
```

### Tests requeridos

- Insert y retrieve
- Update modifica correctamente
- Delete elimina
- Search encuentra por título
- observeAll emite actualizaciones
- getById devuelve null si no existe

### Criterios de aceptación

- [ ] Base de datos in-memory
- [ ] Mínimo 8 tests
- [ ] Cleanup después de cada test

---

## Ejercicio 6: Tests de error handling

### Instrucciones

Testea manejo de errores en ViewModel.

### Escenarios

```kotlin
class UserViewModel(private val repository: UserRepository) {
    val uiState: StateFlow<UserUiState>
    
    fun loadUsers()  // Puede fallar
    fun retry()
}

data class UserUiState(
    val users: List<User> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)
```

### Tests requeridos

- loadUsers error → muestra mensaje error
- loadUsers error → isLoading = false
- retry después de error → intenta de nuevo
- Error específico (IOException) → mensaje "Sin conexión"
- Error genérico → mensaje del error

### Criterios de aceptación

- [ ] FakeRepository que puede simular errores
- [ ] Mínimo 5 tests de error
- [ ] Verificar estados intermedios

---

## Ejercicio 7 (Bonus): Test integración completo

### Instrucciones

Test de integración que verifica flujo completo.

### Flujo a testear

1. Usuario abre lista (vacía)
2. Usuario crea item
3. Item aparece en lista
4. Usuario marca como completado
5. Usuario filtra por completados
6. Item aparece en filtro
7. Usuario elimina item
8. Lista vacía de nuevo

### Criterios de aceptación

- [ ] Un test que cubre todo el flujo
- [ ] Usa ViewModel real con FakeRepository
- [ ] Verifica cada paso del flujo

---

## Entrega

1. Estructura:
   ```
   app/src/test/
     ├── StringUtilsTest.kt
     ├── TodoViewModelTest.kt
     ├── ProductViewModelTest.kt
     └── fakes/
         └── FakeProductRepository.kt
   
   app/src/androidTest/
     ├── LoginScreenTest.kt
     └── NoteDaoTest.kt
   ```
2. Todos los tests pasan
3. Reporte de cobertura (opcional)
4. Crea rama y PR
