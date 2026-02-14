# Lección 11: Testing en Android

## Objetivos

- Escribir tests unitarios con JUnit
- Testear ViewModels y Repositories
- Usar Fakes y Mocks
- Tests de UI con Compose
- Ejecutar tests en CI

---

## 1. Tipos de tests

| Tipo | Ubicación | Velocidad | Qué testea |
|------|-----------|-----------|------------|
| Unit | `test/` | Rápido | Lógica pura |
| Integration | `test/` o `androidTest/` | Medio | Componentes juntos |
| UI | `androidTest/` | Lento | Interfaz de usuario |

**Pirámide de tests:** Muchos unit, algunos integration, pocos UI.

---

## 2. Dependencias

```kotlin
// build.gradle.kts (app)
dependencies {
    // Unit tests
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
    testImplementation("app.cash.turbine:turbine:1.0.0")  // Testing flows
    testImplementation("io.mockk:mockk:1.13.8")
    
    // Android tests
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
```

---

## 3. Tests unitarios básicos

### Estructura de un test

```kotlin
class CalculatorTest {
    
    @Test
    fun `sum of two positive numbers returns correct result`() {
        // Arrange (Given)
        val calculator = Calculator()
        
        // Act (When)
        val result = calculator.sum(2, 3)
        
        // Assert (Then)
        assertEquals(5, result)
    }
    
    @Test
    fun `division by zero throws exception`() {
        val calculator = Calculator()
        
        assertThrows(ArithmeticException::class.java) {
            calculator.divide(10, 0)
        }
    }
}
```

### Assertions comunes

```kotlin
assertEquals(expected, actual)
assertNotEquals(unexpected, actual)
assertTrue(condition)
assertFalse(condition)
assertNull(value)
assertNotNull(value)
assertThrows(Exception::class.java) { ... }
```

---

## 4. Testear ViewModels

### ViewModel ejemplo

```kotlin
class CounterViewModel : ViewModel() {
    private val _count = MutableStateFlow(0)
    val count: StateFlow<Int> = _count.asStateFlow()
    
    fun increment() {
        _count.value++
    }
    
    fun decrement() {
        if (_count.value > 0) {
            _count.value--
        }
    }
}
```

### Test del ViewModel

```kotlin
class CounterViewModelTest {
    
    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()
    
    private lateinit var viewModel: CounterViewModel
    
    @Before
    fun setup() {
        viewModel = CounterViewModel()
    }
    
    @Test
    fun `initial count is zero`() {
        assertEquals(0, viewModel.count.value)
    }
    
    @Test
    fun `increment increases count by one`() {
        viewModel.increment()
        assertEquals(1, viewModel.count.value)
    }
    
    @Test
    fun `decrement does not go below zero`() {
        viewModel.decrement()
        assertEquals(0, viewModel.count.value)
    }
    
    @Test
    fun `multiple increments work correctly`() {
        repeat(5) { viewModel.increment() }
        assertEquals(5, viewModel.count.value)
    }
}
```

### MainDispatcherRule

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class MainDispatcherRule(
    private val dispatcher: TestDispatcher = UnconfinedTestDispatcher()
) : TestWatcher() {
    
    override fun starting(description: Description) {
        Dispatchers.setMain(dispatcher)
    }
    
    override fun finished(description: Description) {
        Dispatchers.resetMain()
    }
}
```

---

## 5. Fakes vs Mocks

### Fake (implementación simplificada)

```kotlin
// Interface
interface UserRepository {
    fun observeUsers(): Flow<List<User>>
    suspend fun getUser(id: Int): User?
    suspend fun saveUser(user: User)
}

// Fake para tests
class FakeUserRepository : UserRepository {
    private val users = mutableListOf<User>()
    private val _usersFlow = MutableStateFlow<List<User>>(emptyList())
    
    override fun observeUsers(): Flow<List<User>> = _usersFlow.asStateFlow()
    
    override suspend fun getUser(id: Int): User? = users.find { it.id == id }
    
    override suspend fun saveUser(user: User) {
        users.add(user)
        _usersFlow.value = users.toList()
    }
    
    // Helpers para tests
    fun addUser(user: User) {
        users.add(user)
        _usersFlow.value = users.toList()
    }
    
    fun clear() {
        users.clear()
        _usersFlow.value = emptyList()
    }
}
```

### Mock (con MockK)

```kotlin
@Test
fun `loadUsers calls repository`() = runTest {
    // Crear mock
    val mockRepository = mockk<UserRepository>()
    
    // Configurar comportamiento
    coEvery { mockRepository.getUsers() } returns listOf(
        User(1, "Test User")
    )
    
    val viewModel = UserViewModel(mockRepository)
    viewModel.loadUsers()
    
    // Verificar que se llamó
    coVerify { mockRepository.getUsers() }
}
```

**Recomendación:** Prefiere Fakes sobre Mocks para tests más mantenibles.

---

## 6. Testing Flows

### Con Turbine

```kotlin
@Test
fun `users flow emits updates`() = runTest {
    val repository = FakeUserRepository()
    val viewModel = UserViewModel(repository)
    
    viewModel.users.test {
        // Estado inicial
        assertEquals(emptyList<User>(), awaitItem())
        
        // Añadir usuario
        repository.addUser(User(1, "Alice"))
        assertEquals(listOf(User(1, "Alice")), awaitItem())
        
        // Añadir otro
        repository.addUser(User(2, "Bob"))
        val users = awaitItem()
        assertEquals(2, users.size)
        
        cancelAndIgnoreRemainingEvents()
    }
}
```

### Sin Turbine

```kotlin
@Test
fun `state updates correctly`() = runTest {
    val viewModel = UserViewModel(FakeUserRepository())
    
    viewModel.loadUsers()
    advanceUntilIdle()  // Esperar coroutines
    
    val state = viewModel.uiState.value
    assertFalse(state.isLoading)
    assertTrue(state.users.isNotEmpty())
}
```

---

## 7. Testing con coroutines

```kotlin
class UserViewModelTest {
    
    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()
    
    @Test
    fun `loadUsers shows loading then success`() = runTest {
        val fakeRepository = FakeUserRepository().apply {
            addUser(User(1, "Test"))
        }
        val viewModel = UserViewModel(fakeRepository)
        
        viewModel.uiState.test {
            // Estado inicial
            val initial = awaitItem()
            assertTrue(initial.isLoading)
            
            // Después de cargar
            val loaded = awaitItem()
            assertFalse(loaded.isLoading)
            assertEquals(1, loaded.users.size)
            
            cancelAndIgnoreRemainingEvents()
        }
    }
    
    @Test
    fun `loadUsers handles error`() = runTest {
        val fakeRepository = object : UserRepository {
            override suspend fun getUsers() = throw IOException("Network error")
            override fun observeUsers() = flowOf<List<User>>()
        }
        
        val viewModel = UserViewModel(fakeRepository)
        viewModel.loadUsers()
        advanceUntilIdle()
        
        assertNotNull(viewModel.uiState.value.error)
    }
}
```

---

## 8. Tests de Compose UI

### Configuración

```kotlin
class UserListScreenTest {
    
    @get:Rule
    val composeTestRule = createComposeRule()
    
    @Test
    fun `displays user list`() {
        val users = listOf(
            User(1, "Alice", "alice@test.com"),
            User(2, "Bob", "bob@test.com")
        )
        
        composeTestRule.setContent {
            UserListScreen(users = users)
        }
        
        // Verificar que se muestran
        composeTestRule.onNodeWithText("Alice").assertIsDisplayed()
        composeTestRule.onNodeWithText("Bob").assertIsDisplayed()
    }
    
    @Test
    fun `shows loading indicator`() {
        composeTestRule.setContent {
            UserListScreen(isLoading = true, users = emptyList())
        }
        
        composeTestRule
            .onNode(hasProgressBarRangeInfo(ProgressBarRangeInfo.Indeterminate))
            .assertIsDisplayed()
    }
    
    @Test
    fun `clicking user triggers callback`() {
        var clickedId: Int? = null
        
        composeTestRule.setContent {
            UserListScreen(
                users = listOf(User(1, "Alice", "alice@test.com")),
                onUserClick = { clickedId = it }
            )
        }
        
        composeTestRule.onNodeWithText("Alice").performClick()
        
        assertEquals(1, clickedId)
    }
}
```

### Matchers comunes

```kotlin
// Buscar nodos
onNodeWithText("texto")
onNodeWithContentDescription("descripción")
onNodeWithTag("testTag")
onAllNodesWithText("texto")

// Acciones
performClick()
performTextInput("texto")
performScrollTo()

// Assertions
assertIsDisplayed()
assertIsNotDisplayed()
assertIsEnabled()
assertIsSelected()
assertTextEquals("texto")
```

### Test tags

```kotlin
// En el código
Text(
    text = "Hello",
    modifier = Modifier.testTag("greeting")
)

// En el test
composeTestRule.onNodeWithTag("greeting").assertIsDisplayed()
```

---

## 9. Testing Room

```kotlin
@RunWith(AndroidJUnit4::class)
class UserDaoTest {
    
    private lateinit var database: AppDatabase
    private lateinit var userDao: UserDao
    
    @Before
    fun setup() {
        database = Room.inMemoryDatabaseBuilder(
            ApplicationProvider.getApplicationContext(),
            AppDatabase::class.java
        ).allowMainThreadQueries().build()
        
        userDao = database.userDao()
    }
    
    @After
    fun tearDown() {
        database.close()
    }
    
    @Test
    fun insertAndRetrieveUser() = runTest {
        val user = UserEntity(1, "Test User", "test@email.com")
        
        userDao.insert(user)
        val retrieved = userDao.getById(1)
        
        assertEquals(user, retrieved)
    }
    
    @Test
    fun observeUsersEmitsUpdates() = runTest {
        userDao.observeAll().test {
            assertEquals(emptyList<UserEntity>(), awaitItem())
            
            userDao.insert(UserEntity(1, "Alice", "alice@test.com"))
            assertEquals(1, awaitItem().size)
            
            cancelAndIgnoreRemainingEvents()
        }
    }
}
```

---

## 10. Ejecutar tests

### Desde terminal

```bash
# Unit tests
./gradlew test

# Tests de un módulo
./gradlew :app:test

# Android tests (requiere emulador/device)
./gradlew connectedAndroidTest

# Con reporte
./gradlew test --continue
```

### En CI (GitHub Actions)

```yaml
- name: Run unit tests
  run: ./gradlew test

- name: Upload test results
  uses: actions/upload-artifact@v3
  if: failure()
  with:
    name: test-results
    path: app/build/reports/tests/
```

---

## Resumen

| Tipo | Herramienta | Uso |
|------|-------------|-----|
| Unit | JUnit + kotlinx-coroutines-test | Lógica, ViewModels |
| Flow | Turbine | StateFlow, SharedFlow |
| Mocks | MockK | Dependencias externas |
| UI | Compose Testing | Pantallas |
| Database | Room in-memory | DAOs |

### Buenas prácticas

1. **Nombres descriptivos:** `methodName_condition_expectedResult`
2. **Arrange-Act-Assert:** Estructura clara
3. **Un assert por test** (preferiblemente)
4. **Fakes sobre Mocks** cuando sea posible
5. **Tests independientes:** No depender de orden

---

## Siguiente paso

→ [ejercicios.md](ejercicios.md)
