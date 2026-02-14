# Lección 07: APIs con Retrofit

## Objetivos

- Configurar Retrofit para llamadas HTTP
- Usar Moshi/Gson para serialización JSON
- Implementar interceptores
- Manejar errores de red
- Integrar con ViewModel y UiState

---

## 1. Dependencias

```kotlin
// build.gradle.kts (app)
dependencies {
    // Retrofit
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-moshi:2.9.0")
    
    // Moshi (serialización JSON)
    implementation("com.squareup.moshi:moshi-kotlin:1.15.0")
    ksp("com.squareup.moshi:moshi-kotlin-codegen:1.15.0")
    
    // OkHttp (logging)
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
}
```

### Permisos

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.INTERNET" />
```

---

## 2. Modelo de datos

```kotlin
// data/model/User.kt
@JsonClass(generateAdapter = true)
data class User(
    val id: Int,
    val name: String,
    val email: String,
    val phone: String? = null
)

@JsonClass(generateAdapter = true)
data class Post(
    val id: Int,
    val userId: Int,
    val title: String,
    val body: String
)
```

---

## 3. API Interface

```kotlin
// data/api/JsonPlaceholderApi.kt
interface JsonPlaceholderApi {

    @GET("users")
    suspend fun getUsers(): List<User>

    @GET("users/{id}")
    suspend fun getUser(@Path("id") userId: Int): User

    @GET("posts")
    suspend fun getPosts(): List<Post>

    @GET("posts")
    suspend fun getPostsByUser(@Query("userId") userId: Int): List<Post>

    @POST("posts")
    suspend fun createPost(@Body post: Post): Post

    @PUT("posts/{id}")
    suspend fun updatePost(
        @Path("id") postId: Int,
        @Body post: Post
    ): Post

    @DELETE("posts/{id}")
    suspend fun deletePost(@Path("id") postId: Int)
}
```

### Anotaciones HTTP

| Anotación | Uso |
|-----------|-----|
| `@GET` | Petición GET |
| `@POST` | Petición POST |
| `@PUT` | Petición PUT |
| `@DELETE` | Petición DELETE |
| `@Path` | Parámetro en la URL |
| `@Query` | Query parameter (?key=value) |
| `@Body` | Cuerpo de la petición |
| `@Header` | Header personalizado |

---

## 4. Configurar Retrofit

```kotlin
// data/api/RetrofitInstance.kt
object RetrofitInstance {

    private const val BASE_URL = "https://jsonplaceholder.typicode.com/"

    private val moshi = Moshi.Builder()
        .add(KotlinJsonAdapterFactory())
        .build()

    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }

    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()

    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(MoshiConverterFactory.create(moshi))
        .build()

    val api: JsonPlaceholderApi = retrofit.create(JsonPlaceholderApi::class.java)
}
```

---

## 5. Repository

```kotlin
// data/repository/UserRepository.kt
class UserRepository(
    private val api: JsonPlaceholderApi = RetrofitInstance.api
) {

    suspend fun getUsers(): Result<List<User>> {
        return try {
            val users = api.getUsers()
            Result.success(users)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getUser(id: Int): Result<User> {
        return try {
            val user = api.getUser(id)
            Result.success(user)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getPostsByUser(userId: Int): Result<List<Post>> {
        return try {
            val posts = api.getPostsByUser(userId)
            Result.success(posts)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

---

## 6. ViewModel con API

```kotlin
// ui/users/UserViewModel.kt
data class UserListUiState(
    val users: List<User> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)

class UserViewModel(
    private val repository: UserRepository = UserRepository()
) : ViewModel() {

    private val _uiState = MutableStateFlow(UserListUiState())
    val uiState: StateFlow<UserListUiState> = _uiState.asStateFlow()

    init {
        loadUsers()
    }

    fun loadUsers() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            
            repository.getUsers()
                .onSuccess { users ->
                    _uiState.update { 
                        it.copy(users = users, isLoading = false) 
                    }
                }
                .onFailure { exception ->
                    _uiState.update { 
                        it.copy(
                            error = exception.message ?: "Error desconocido",
                            isLoading = false
                        ) 
                    }
                }
        }
    }

    fun retry() {
        loadUsers()
    }
}
```

---

## 7. UI

```kotlin
@Composable
fun UserListScreen(
    viewModel: UserViewModel = viewModel(),
    onUserClick: (Int) -> Unit
) {
    val uiState by viewModel.uiState.collectAsState()

    when {
        uiState.isLoading -> {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        }
        uiState.error != null -> {
            Column(
                Modifier.fillMaxSize(),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Text(uiState.error!!, color = MaterialTheme.colorScheme.error)
                Spacer(Modifier.height(16.dp))
                Button(onClick = { viewModel.retry() }) {
                    Text("Reintentar")
                }
            }
        }
        else -> {
            LazyColumn {
                items(uiState.users, key = { it.id }) { user ->
                    UserItem(user = user, onClick = { onUserClick(user.id) })
                }
            }
        }
    }
}

@Composable
fun UserItem(user: User, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
            .clickable(onClick = onClick)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(user.name, fontWeight = FontWeight.Bold)
            Text(user.email, fontSize = 14.sp)
            user.phone?.let {
                Text(it, fontSize = 12.sp, color = Color.Gray)
            }
        }
    }
}
```

---

## 8. Manejo de errores avanzado

### Wrapper de respuesta

```kotlin
sealed class NetworkResult<out T> {
    data class Success<T>(val data: T) : NetworkResult<T>()
    data class Error(val code: Int, val message: String) : NetworkResult<Nothing>()
    data class Exception(val e: Throwable) : NetworkResult<Nothing>()
}

suspend fun <T> safeApiCall(apiCall: suspend () -> T): NetworkResult<T> {
    return try {
        NetworkResult.Success(apiCall())
    } catch (e: HttpException) {
        NetworkResult.Error(e.code(), e.message())
    } catch (e: IOException) {
        NetworkResult.Exception(e)
    } catch (e: Exception) {
        NetworkResult.Exception(e)
    }
}
```

### Uso en Repository

```kotlin
class UserRepository(private val api: JsonPlaceholderApi) {

    suspend fun getUsers(): NetworkResult<List<User>> {
        return safeApiCall { api.getUsers() }
    }
}
```

### En ViewModel

```kotlin
fun loadUsers() {
    viewModelScope.launch {
        _uiState.update { it.copy(isLoading = true) }
        
        when (val result = repository.getUsers()) {
            is NetworkResult.Success -> {
                _uiState.update { 
                    it.copy(users = result.data, isLoading = false) 
                }
            }
            is NetworkResult.Error -> {
                _uiState.update { 
                    it.copy(
                        error = "Error ${result.code}: ${result.message}",
                        isLoading = false
                    ) 
                }
            }
            is NetworkResult.Exception -> {
                val message = when (result.e) {
                    is UnknownHostException -> "Sin conexión a internet"
                    is SocketTimeoutException -> "Tiempo de espera agotado"
                    else -> result.e.message ?: "Error desconocido"
                }
                _uiState.update { it.copy(error = message, isLoading = false) }
            }
        }
    }
}
```

---

## 9. Interceptores personalizados

### Auth interceptor

```kotlin
class AuthInterceptor(private val tokenProvider: () -> String) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request().newBuilder()
            .addHeader("Authorization", "Bearer ${tokenProvider()}")
            .build()
        return chain.proceed(request)
    }
}

// Uso
val okHttpClient = OkHttpClient.Builder()
    .addInterceptor(AuthInterceptor { "mi_token_aqui" })
    .build()
```

### Retry interceptor

```kotlin
class RetryInterceptor(private val maxRetries: Int = 3) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        var attempt = 0
        var response: Response? = null
        
        while (attempt < maxRetries) {
            try {
                response = chain.proceed(chain.request())
                if (response.isSuccessful) return response
            } catch (e: IOException) {
                if (attempt == maxRetries - 1) throw e
            }
            attempt++
        }
        
        return response ?: throw IOException("Max retries exceeded")
    }
}
```

---

## 10. Testing

### Fake API para tests

```kotlin
class FakeJsonPlaceholderApi : JsonPlaceholderApi {
    
    var usersToReturn = listOf<User>()
    var shouldThrowError = false
    
    override suspend fun getUsers(): List<User> {
        if (shouldThrowError) throw IOException("Test error")
        return usersToReturn
    }
    
    // Implementar otros métodos...
}
```

### Test del ViewModel

```kotlin
class UserViewModelTest {
    
    @Test
    fun `loadUsers success updates state`() = runTest {
        val fakeApi = FakeJsonPlaceholderApi().apply {
            usersToReturn = listOf(
                User(1, "John", "john@test.com")
            )
        }
        val repository = UserRepository(fakeApi)
        val viewModel = UserViewModel(repository)
        
        advanceUntilIdle()
        
        val state = viewModel.uiState.value
        assertEquals(1, state.users.size)
        assertEquals("John", state.users[0].name)
        assertFalse(state.isLoading)
        assertNull(state.error)
    }
}
```

---

## Resumen

| Concepto | Descripción |
|----------|-------------|
| `Retrofit` | Cliente HTTP type-safe |
| `@GET/@POST` | Métodos HTTP |
| `@Path/@Query` | Parámetros URL |
| `Moshi` | Serialización JSON |
| `Interceptor` | Modificar requests/responses |
| `Result/NetworkResult` | Wrapper para errores |

---

## Siguiente paso

→ [ejercicios.md](ejercicios.md)
