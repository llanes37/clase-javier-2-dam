# Soluciones - Lección 11: Testing

## Ejercicio 1: Tests unitarios básicos

```kotlin
// StringUtils.kt
object StringUtils {
    fun reverseString(input: String): String = input.reversed()
    
    fun isPalindrome(input: String): Boolean {
        val cleaned = input.lowercase().filter { it.isLetterOrDigit() }
        return cleaned == cleaned.reversed()
    }
    
    fun countWords(input: String): Int {
        return input.trim().split("\\s+".toRegex()).filter { it.isNotEmpty() }.size
    }
    
    fun capitalizeWords(input: String): String {
        return input.split(" ").joinToString(" ") { word ->
            word.replaceFirstChar { it.uppercaseChar() }
        }
    }
}

// StringUtilsTest.kt
class StringUtilsTest {
    
    // reverseString tests
    @Test
    fun `reverseString with normal string returns reversed`() {
        assertEquals("olleh", StringUtils.reverseString("hello"))
    }
    
    @Test
    fun `reverseString with empty string returns empty`() {
        assertEquals("", StringUtils.reverseString(""))
    }
    
    @Test
    fun `reverseString with single char returns same`() {
        assertEquals("a", StringUtils.reverseString("a"))
    }
    
    // isPalindrome tests
    @Test
    fun `isPalindrome with palindrome returns true`() {
        assertTrue(StringUtils.isPalindrome("radar"))
    }
    
    @Test
    fun `isPalindrome with non-palindrome returns false`() {
        assertFalse(StringUtils.isPalindrome("hello"))
    }
    
    @Test
    fun `isPalindrome is case insensitive`() {
        assertTrue(StringUtils.isPalindrome("Radar"))
    }
    
    @Test
    fun `isPalindrome ignores spaces and punctuation`() {
        assertTrue(StringUtils.isPalindrome("A man a plan a canal Panama"))
    }
    
    // countWords tests
    @Test
    fun `countWords with normal text returns correct count`() {
        assertEquals(3, StringUtils.countWords("hello world test"))
    }
    
    @Test
    fun `countWords with multiple spaces works correctly`() {
        assertEquals(2, StringUtils.countWords("hello    world"))
    }
    
    @Test
    fun `countWords with empty string returns zero`() {
        assertEquals(0, StringUtils.countWords(""))
    }
    
    @Test
    fun `countWords with only spaces returns zero`() {
        assertEquals(0, StringUtils.countWords("   "))
    }
    
    // capitalizeWords tests
    @Test
    fun `capitalizeWords capitalizes first letter of each word`() {
        assertEquals("Hello World", StringUtils.capitalizeWords("hello world"))
    }
    
    @Test
    fun `capitalizeWords with already capitalized stays same`() {
        assertEquals("Hello", StringUtils.capitalizeWords("Hello"))
    }
}
```

---

## Ejercicio 2: Tests de ViewModel simple

```kotlin
// TodoViewModel.kt
data class TodoItem(val id: Int, val text: String, val isDone: Boolean = false)

class TodoViewModel : ViewModel() {
    private val _todos = MutableStateFlow<List<TodoItem>>(emptyList())
    val todos: StateFlow<List<TodoItem>> = _todos.asStateFlow()
    
    private var nextId = 1
    
    fun addTodo(text: String) {
        if (text.isNotBlank()) {
            _todos.value = _todos.value + TodoItem(nextId++, text, false)
        }
    }
    
    fun toggleTodo(id: Int) {
        _todos.value = _todos.value.map { todo ->
            if (todo.id == id) todo.copy(isDone = !todo.isDone) else todo
        }
    }
    
    fun deleteTodo(id: Int) {
        _todos.value = _todos.value.filter { it.id != id }
    }
    
    fun clearCompleted() {
        _todos.value = _todos.value.filter { !it.isDone }
    }
}

// TodoViewModelTest.kt
class TodoViewModelTest {
    
    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()
    
    private lateinit var viewModel: TodoViewModel
    
    @Before
    fun setup() {
        viewModel = TodoViewModel()
    }
    
    @Test
    fun `initial state is empty list`() {
        assertTrue(viewModel.todos.value.isEmpty())
    }
    
    @Test
    fun `addTodo adds item to list`() {
        viewModel.addTodo("Test todo")
        
        assertEquals(1, viewModel.todos.value.size)
        assertEquals("Test todo", viewModel.todos.value[0].text)
    }
    
    @Test
    fun `addTodo with blank text does not add item`() {
        viewModel.addTodo("   ")
        
        assertTrue(viewModel.todos.value.isEmpty())
    }
    
    @Test
    fun `toggleTodo changes isDone to true`() {
        viewModel.addTodo("Test")
        val id = viewModel.todos.value[0].id
        
        viewModel.toggleTodo(id)
        
        assertTrue(viewModel.todos.value[0].isDone)
    }
    
    @Test
    fun `toggleTodo changes isDone back to false`() {
        viewModel.addTodo("Test")
        val id = viewModel.todos.value[0].id
        
        viewModel.toggleTodo(id)
        viewModel.toggleTodo(id)
        
        assertFalse(viewModel.todos.value[0].isDone)
    }
    
    @Test
    fun `deleteTodo removes item from list`() {
        viewModel.addTodo("Test")
        val id = viewModel.todos.value[0].id
        
        viewModel.deleteTodo(id)
        
        assertTrue(viewModel.todos.value.isEmpty())
    }
    
    @Test
    fun `clearCompleted removes only completed items`() {
        viewModel.addTodo("Todo 1")
        viewModel.addTodo("Todo 2")
        viewModel.addTodo("Todo 3")
        
        viewModel.toggleTodo(viewModel.todos.value[1].id)  // Complete Todo 2
        viewModel.clearCompleted()
        
        assertEquals(2, viewModel.todos.value.size)
        assertTrue(viewModel.todos.value.none { it.isDone })
    }
    
    @Test
    fun `multiple todos have unique ids`() {
        viewModel.addTodo("Todo 1")
        viewModel.addTodo("Todo 2")
        
        val ids = viewModel.todos.value.map { it.id }
        assertEquals(ids.distinct().size, ids.size)
    }
}
```

---

## Ejercicio 3: Tests con Fake Repository

```kotlin
// FakeProductRepository.kt
class FakeProductRepository : ProductRepository {
    private val products = mutableListOf<Product>()
    private val _productsFlow = MutableStateFlow<List<Product>>(emptyList())
    
    var shouldThrowError = false
    var errorToThrow: Exception = IOException("Network error")
    
    override fun observeProducts(): Flow<List<Product>> = _productsFlow.asStateFlow()
    
    override suspend fun getProduct(id: Int): Product? {
        if (shouldThrowError) throw errorToThrow
        return products.find { it.id == id }
    }
    
    override suspend fun addProduct(product: Product) {
        if (shouldThrowError) throw errorToThrow
        products.add(product)
        _productsFlow.value = products.toList()
    }
    
    override suspend fun deleteProduct(id: Int) {
        if (shouldThrowError) throw errorToThrow
        products.removeIf { it.id == id }
        _productsFlow.value = products.toList()
    }
    
    // Test helpers
    fun setProducts(productList: List<Product>) {
        products.clear()
        products.addAll(productList)
        _productsFlow.value = products.toList()
    }
}

// ProductViewModelTest.kt
class ProductViewModelTest {
    
    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()
    
    private lateinit var repository: FakeProductRepository
    private lateinit var viewModel: ProductViewModel
    
    @Before
    fun setup() {
        repository = FakeProductRepository()
        viewModel = ProductViewModel(repository)
    }
    
    @Test
    fun `products flow emits repository data`() = runTest {
        val testProducts = listOf(
            Product(1, "Product 1", 10.0),
            Product(2, "Product 2", 20.0)
        )
        repository.setProducts(testProducts)
        
        viewModel.products.test {
            assertEquals(testProducts, awaitItem())
            cancelAndIgnoreRemainingEvents()
        }
    }
    
    @Test
    fun `deleteProduct removes product from list`() = runTest {
        repository.setProducts(listOf(
            Product(1, "Product 1", 10.0),
            Product(2, "Product 2", 20.0)
        ))
        
        viewModel.deleteProduct(1)
        advanceUntilIdle()
        
        viewModel.products.test {
            val products = awaitItem()
            assertEquals(1, products.size)
            assertEquals(2, products[0].id)
            cancelAndIgnoreRemainingEvents()
        }
    }
    
    @Test
    fun `loadProducts sets isLoading true then false`() = runTest {
        viewModel.isLoading.test {
            assertFalse(awaitItem())  // Initial
            
            viewModel.loadProducts()
            assertTrue(awaitItem())   // Loading
            assertFalse(awaitItem())  // Done
            
            cancelAndIgnoreRemainingEvents()
        }
    }
    
    @Test
    fun `error sets error state`() = runTest {
        repository.shouldThrowError = true
        
        viewModel.loadProducts()
        advanceUntilIdle()
        
        assertNotNull(viewModel.uiState.value.error)
    }
}
```

---

## Ejercicio 4: Tests de UI con Compose

```kotlin
class LoginScreenTest {
    
    @get:Rule
    val composeTestRule = createComposeRule()
    
    @Test
    fun `email and password fields are displayed`() {
        composeTestRule.setContent {
            LoginScreen(
                email = "",
                password = "",
                isLoading = false,
                error = null,
                onEmailChange = {},
                onPasswordChange = {},
                onLoginClick = {}
            )
        }
        
        composeTestRule.onNodeWithText("Email").assertIsDisplayed()
        composeTestRule.onNodeWithText("Contraseña").assertIsDisplayed()
    }
    
    @Test
    fun `login button is disabled when fields are empty`() {
        composeTestRule.setContent {
            LoginScreen(
                email = "",
                password = "",
                isLoading = false,
                error = null,
                onEmailChange = {},
                onPasswordChange = {},
                onLoginClick = {}
            )
        }
        
        composeTestRule.onNodeWithText("Iniciar sesión").assertIsNotEnabled()
    }
    
    @Test
    fun `login button is enabled when fields have text`() {
        composeTestRule.setContent {
            LoginScreen(
                email = "test@email.com",
                password = "password123",
                isLoading = false,
                error = null,
                onEmailChange = {},
                onPasswordChange = {},
                onLoginClick = {}
            )
        }
        
        composeTestRule.onNodeWithText("Iniciar sesión").assertIsEnabled()
    }
    
    @Test
    fun `loading indicator is shown when isLoading is true`() {
        composeTestRule.setContent {
            LoginScreen(
                email = "test@email.com",
                password = "password123",
                isLoading = true,
                error = null,
                onEmailChange = {},
                onPasswordChange = {},
                onLoginClick = {}
            )
        }
        
        composeTestRule
            .onNode(hasProgressBarRangeInfo(ProgressBarRangeInfo.Indeterminate))
            .assertIsDisplayed()
    }
    
    @Test
    fun `error message is displayed when error is not null`() {
        composeTestRule.setContent {
            LoginScreen(
                email = "",
                password = "",
                isLoading = false,
                error = "Credenciales inválidas",
                onEmailChange = {},
                onPasswordChange = {},
                onLoginClick = {}
            )
        }
        
        composeTestRule.onNodeWithText("Credenciales inválidas").assertIsDisplayed()
    }
    
    @Test
    fun `clicking login button triggers callback`() {
        var wasClicked = false
        
        composeTestRule.setContent {
            LoginScreen(
                email = "test@email.com",
                password = "password123",
                isLoading = false,
                error = null,
                onEmailChange = {},
                onPasswordChange = {},
                onLoginClick = { wasClicked = true }
            )
        }
        
        composeTestRule.onNodeWithText("Iniciar sesión").performClick()
        
        assertTrue(wasClicked)
    }
    
    @Test
    fun `typing in email field triggers callback`() {
        var typedEmail = ""
        
        composeTestRule.setContent {
            LoginScreen(
                email = "",
                password = "",
                isLoading = false,
                error = null,
                onEmailChange = { typedEmail = it },
                onPasswordChange = {},
                onLoginClick = {}
            )
        }
        
        composeTestRule.onNodeWithTag("email_field").performTextInput("test@email.com")
        
        assertEquals("test@email.com", typedEmail)
    }
}
```

---

## Ejercicio 5: Tests de Room DAO

```kotlin
@RunWith(AndroidJUnit4::class)
class NoteDaoTest {
    
    private lateinit var database: AppDatabase
    private lateinit var noteDao: NoteDao
    
    @Before
    fun setup() {
        database = Room.inMemoryDatabaseBuilder(
            ApplicationProvider.getApplicationContext(),
            AppDatabase::class.java
        ).allowMainThreadQueries().build()
        
        noteDao = database.noteDao()
    }
    
    @After
    fun tearDown() {
        database.close()
    }
    
    @Test
    fun insertAndRetrieveNote() = runTest {
        val note = NoteEntity(id = 1, title = "Test", content = "Content")
        
        noteDao.insert(note)
        val retrieved = noteDao.getById(1)
        
        assertEquals(note.title, retrieved?.title)
    }
    
    @Test
    fun updateModifiesNote() = runTest {
        val note = NoteEntity(id = 1, title = "Original", content = "Content")
        noteDao.insert(note)
        
        val updated = note.copy(title = "Updated")
        noteDao.update(updated)
        
        val retrieved = noteDao.getById(1)
        assertEquals("Updated", retrieved?.title)
    }
    
    @Test
    fun deleteRemovesNote() = runTest {
        val note = NoteEntity(id = 1, title = "Test", content = "Content")
        noteDao.insert(note)
        
        noteDao.deleteById(1)
        
        assertNull(noteDao.getById(1))
    }
    
    @Test
    fun searchFindsByTitle() = runTest {
        noteDao.insert(NoteEntity(1, "Kotlin basics", "Content"))
        noteDao.insert(NoteEntity(2, "Java basics", "Content"))
        noteDao.insert(NoteEntity(3, "Python basics", "Content"))
        
        noteDao.search("Kotlin").test {
            val results = awaitItem()
            assertEquals(1, results.size)
            assertEquals("Kotlin basics", results[0].title)
            cancelAndIgnoreRemainingEvents()
        }
    }
    
    @Test
    fun observeAllEmitsUpdates() = runTest {
        noteDao.observeAll().test {
            assertEquals(emptyList<NoteEntity>(), awaitItem())
            
            noteDao.insert(NoteEntity(1, "Note 1", "Content"))
            assertEquals(1, awaitItem().size)
            
            noteDao.insert(NoteEntity(2, "Note 2", "Content"))
            assertEquals(2, awaitItem().size)
            
            cancelAndIgnoreRemainingEvents()
        }
    }
    
    @Test
    fun getByIdReturnsNullForNonExistent() = runTest {
        val result = noteDao.getById(999)
        assertNull(result)
    }
    
    @Test
    fun insertWithSameIdReplaces() = runTest {
        noteDao.insert(NoteEntity(1, "Original", "Content"))
        noteDao.insert(NoteEntity(1, "Replaced", "New Content"))
        
        val retrieved = noteDao.getById(1)
        assertEquals("Replaced", retrieved?.title)
    }
    
    @Test
    fun searchIsCaseInsensitive() = runTest {
        noteDao.insert(NoteEntity(1, "KOTLIN", "Content"))
        
        noteDao.search("kotlin").test {
            val results = awaitItem()
            assertEquals(1, results.size)
            cancelAndIgnoreRemainingEvents()
        }
    }
}
```
