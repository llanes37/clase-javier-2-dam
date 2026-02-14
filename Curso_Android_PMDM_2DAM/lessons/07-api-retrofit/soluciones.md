# Soluciones - Lección 07: APIs con Retrofit

## Ejercicio 1: Lista de usuarios

```kotlin
// data/model/User.kt
@JsonClass(generateAdapter = true)
data class User(
    val id: Int,
    val name: String,
    val email: String,
    val phone: String? = null,
    val website: String? = null
)

// data/api/JsonPlaceholderApi.kt
interface JsonPlaceholderApi {
    @GET("users")
    suspend fun getUsers(): List<User>
}

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
        .build()

    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(MoshiConverterFactory.create(moshi))
        .build()

    val api: JsonPlaceholderApi = retrofit.create(JsonPlaceholderApi::class.java)
}

// data/repository/UserRepository.kt
class UserRepository(
    private val api: JsonPlaceholderApi = RetrofitInstance.api
) {
    suspend fun getUsers(): Result<List<User>> {
        return try {
            Result.success(api.getUsers())
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

// ui/users/UserListUiState.kt
data class UserListUiState(
    val users: List<User> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)

// ui/users/UserViewModel.kt
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
                    _uiState.update { it.copy(users = users, isLoading = false) }
                }
                .onFailure { e ->
                    _uiState.update { 
                        it.copy(error = e.message ?: "Error", isLoading = false) 
                    }
                }
        }
    }
}

// ui/users/UserListScreen.kt
@Composable
fun UserListScreen(viewModel: UserViewModel = viewModel()) {
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
                Button(onClick = { viewModel.loadUsers() }) {
                    Text("Reintentar")
                }
            }
        }
        else -> {
            LazyColumn {
                items(uiState.users, key = { it.id }) { user ->
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(8.dp)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(user.name, fontWeight = FontWeight.Bold)
                            Text(user.email)
                        }
                    }
                }
            }
        }
    }
}
```

---

## Ejercicio 2: Detalle de usuario

```kotlin
// data/model/Post.kt
@JsonClass(generateAdapter = true)
data class Post(
    val id: Int,
    val userId: Int,
    val title: String,
    val body: String
)

// data/api/JsonPlaceholderApi.kt (añadir)
@GET("users/{id}")
suspend fun getUser(@Path("id") userId: Int): User

@GET("posts")
suspend fun getPostsByUser(@Query("userId") userId: Int): List<Post>

// data/repository/UserRepository.kt (añadir)
suspend fun getUser(id: Int): Result<User> {
    return try {
        Result.success(api.getUser(id))
    } catch (e: Exception) {
        Result.failure(e)
    }
}

suspend fun getPostsByUser(userId: Int): Result<List<Post>> {
    return try {
        Result.success(api.getPostsByUser(userId))
    } catch (e: Exception) {
        Result.failure(e)
    }
}

// ui/users/UserDetailViewModel.kt
data class UserDetailUiState(
    val user: User? = null,
    val posts: List<Post> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)

class UserDetailViewModel(
    private val userId: Int,
    private val repository: UserRepository = UserRepository()
) : ViewModel() {

    private val _uiState = MutableStateFlow(UserDetailUiState())
    val uiState: StateFlow<UserDetailUiState> = _uiState.asStateFlow()

    init {
        loadUserAndPosts()
    }

    private fun loadUserAndPosts() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            
            // Cargar en paralelo
            val userResult = async { repository.getUser(userId) }
            val postsResult = async { repository.getPostsByUser(userId) }
            
            val user = userResult.await()
            val posts = postsResult.await()
            
            if (user.isSuccess && posts.isSuccess) {
                _uiState.update {
                    it.copy(
                        user = user.getOrNull(),
                        posts = posts.getOrNull() ?: emptyList(),
                        isLoading = false
                    )
                }
            } else {
                _uiState.update {
                    it.copy(
                        error = "Error al cargar datos",
                        isLoading = false
                    )
                }
            }
        }
    }
}

// ui/users/UserDetailScreen.kt
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UserDetailScreen(
    userId: Int,
    onBack: () -> Unit
) {
    val viewModel: UserDetailViewModel = viewModel(
        factory = object : ViewModelProvider.Factory {
            override fun <T : ViewModel> create(modelClass: Class<T>): T {
                @Suppress("UNCHECKED_CAST")
                return UserDetailViewModel(userId) as T
            }
        }
    )
    val uiState by viewModel.uiState.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(uiState.user?.name ?: "Usuario") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Volver")
                    }
                }
            )
        }
    ) { padding ->
        when {
            uiState.isLoading -> {
                Box(
                    Modifier.fillMaxSize().padding(padding),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }
            uiState.error != null -> {
                Text(uiState.error!!, modifier = Modifier.padding(padding))
            }
            else -> {
                LazyColumn(modifier = Modifier.padding(padding)) {
                    item {
                        uiState.user?.let { user ->
                            Card(modifier = Modifier.padding(16.dp).fillMaxWidth()) {
                                Column(modifier = Modifier.padding(16.dp)) {
                                    Text(user.name, style = MaterialTheme.typography.headlineSmall)
                                    Text(user.email)
                                    user.phone?.let { Text(it) }
                                    user.website?.let { Text(it) }
                                }
                            }
                        }
                    }

                    item {
                        Text(
                            "Posts",
                            style = MaterialTheme.typography.titleMedium,
                            modifier = Modifier.padding(16.dp)
                        )
                    }

                    items(uiState.posts, key = { it.id }) { post ->
                        Card(modifier = Modifier.padding(horizontal = 16.dp, vertical = 4.dp)) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Text(post.title, fontWeight = FontWeight.Bold)
                                Spacer(Modifier.height(4.dp))
                                Text(post.body, maxLines = 2, overflow = TextOverflow.Ellipsis)
                            }
                        }
                    }
                }
            }
        }
    }
}
```

---

## Ejercicio 3: Crear post

```kotlin
// data/api/JsonPlaceholderApi.kt (añadir)
@POST("posts")
suspend fun createPost(@Body post: Post): Post

// ui/posts/CreatePostViewModel.kt
data class CreatePostUiState(
    val title: String = "",
    val body: String = "",
    val isSubmitting: Boolean = false,
    val isSuccess: Boolean = false,
    val error: String? = null
) {
    val isValid: Boolean get() = title.isNotBlank() && body.isNotBlank()
}

class CreatePostViewModel(
    private val userId: Int,
    private val repository: UserRepository = UserRepository()
) : ViewModel() {

    private val _uiState = MutableStateFlow(CreatePostUiState())
    val uiState: StateFlow<CreatePostUiState> = _uiState.asStateFlow()

    fun onTitleChange(title: String) {
        _uiState.update { it.copy(title = title) }
    }

    fun onBodyChange(body: String) {
        _uiState.update { it.copy(body = body) }
    }

    fun submit() {
        if (!_uiState.value.isValid) return

        viewModelScope.launch {
            _uiState.update { it.copy(isSubmitting = true, error = null) }

            val post = Post(
                id = 0,
                userId = userId,
                title = _uiState.value.title,
                body = _uiState.value.body
            )

            try {
                RetrofitInstance.api.createPost(post)
                _uiState.update { it.copy(isSuccess = true, isSubmitting = false) }
            } catch (e: Exception) {
                _uiState.update { 
                    it.copy(error = e.message, isSubmitting = false) 
                }
            }
        }
    }
}

// ui/posts/CreatePostScreen.kt
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CreatePostScreen(
    userId: Int,
    onBack: () -> Unit
) {
    val viewModel: CreatePostViewModel = viewModel(
        factory = object : ViewModelProvider.Factory {
            override fun <T : ViewModel> create(modelClass: Class<T>): T {
                @Suppress("UNCHECKED_CAST")
                return CreatePostViewModel(userId) as T
            }
        }
    )
    val uiState by viewModel.uiState.collectAsState()

    LaunchedEffect(uiState.isSuccess) {
        if (uiState.isSuccess) {
            onBack()
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Nuevo Post") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Volver")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
        ) {
            OutlinedTextField(
                value = uiState.title,
                onValueChange = viewModel::onTitleChange,
                label = { Text("Título") },
                modifier = Modifier.fillMaxWidth(),
                enabled = !uiState.isSubmitting
            )

            Spacer(Modifier.height(16.dp))

            OutlinedTextField(
                value = uiState.body,
                onValueChange = viewModel::onBodyChange,
                label = { Text("Contenido") },
                modifier = Modifier.fillMaxWidth().height(200.dp),
                enabled = !uiState.isSubmitting
            )

            Spacer(Modifier.height(16.dp))

            uiState.error?.let {
                Text(it, color = MaterialTheme.colorScheme.error)
                Spacer(Modifier.height(8.dp))
            }

            Button(
                onClick = viewModel::submit,
                enabled = uiState.isValid && !uiState.isSubmitting,
                modifier = Modifier.fillMaxWidth()
            ) {
                if (uiState.isSubmitting) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(20.dp),
                        strokeWidth = 2.dp
                    )
                } else {
                    Text("Publicar")
                }
            }
        }
    }
}
```

---

## Ejercicio 4: Manejo de errores completo

```kotlin
// data/network/NetworkResult.kt
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
    } catch (e: UnknownHostException) {
        NetworkResult.Exception(e)
    } catch (e: SocketTimeoutException) {
        NetworkResult.Exception(e)
    } catch (e: IOException) {
        NetworkResult.Exception(e)
    } catch (e: Exception) {
        NetworkResult.Exception(e)
    }
}

fun NetworkResult.Exception.toUserMessage(): String {
    return when (e) {
        is UnknownHostException -> "No hay conexión a internet"
        is SocketTimeoutException -> "El servidor no responde"
        else -> e.message ?: "Error desconocido"
    }
}

fun NetworkResult.Error.toUserMessage(): String {
    return when (code) {
        404 -> "Recurso no encontrado"
        500, 501, 502, 503 -> "Error del servidor"
        else -> "Error $code: $message"
    }
}

// ViewModel actualizado
fun loadUsers() {
    viewModelScope.launch {
        _uiState.update { it.copy(isLoading = true) }
        
        when (val result = safeApiCall { api.getUsers() }) {
            is NetworkResult.Success -> {
                _uiState.update { it.copy(users = result.data, isLoading = false) }
            }
            is NetworkResult.Error -> {
                _uiState.update { 
                    it.copy(error = result.toUserMessage(), isLoading = false) 
                }
            }
            is NetworkResult.Exception -> {
                _uiState.update { 
                    it.copy(error = result.toUserMessage(), isLoading = false) 
                }
            }
        }
    }
}
```

---

## Ejercicio 5: Interceptor de autenticación

```kotlin
// data/api/AuthInterceptor.kt
class AuthInterceptor(private val tokenProvider: () -> String) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()
        
        val newRequest = originalRequest.newBuilder()
            .addHeader("Authorization", "Bearer ${tokenProvider()}")
            .addHeader("Content-Type", "application/json")
            .build()
            
        return chain.proceed(newRequest)
    }
}

// RetrofitInstance actualizado
object RetrofitInstance {
    private const val BASE_URL = "https://jsonplaceholder.typicode.com/"
    
    // En producción, esto vendría de SharedPreferences o DataStore
    private val token = "mi_token_de_prueba_12345"

    private val authInterceptor = AuthInterceptor { token }
    
    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.HEADERS  // Ver headers
    }

    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(authInterceptor)
        .addInterceptor(loggingInterceptor)
        .build()

    // resto igual...
}
```

---

## Ejercicio 6: Búsqueda con debounce

```kotlin
class SearchPostsViewModel(
    private val api: JsonPlaceholderApi = RetrofitInstance.api
) : ViewModel() {

    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()

    private val _uiState = MutableStateFlow(SearchUiState())
    val uiState: StateFlow<SearchUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            _searchQuery
                .debounce(500)  // Esperar 500ms
                .distinctUntilChanged()
                .collect { query ->
                    searchPosts(query)
                }
        }
    }

    fun onSearchQueryChange(query: String) {
        _searchQuery.value = query
    }

    private suspend fun searchPosts(query: String) {
        _uiState.update { it.copy(isLoading = true) }
        
        try {
            val allPosts = api.getPosts()
            val filtered = if (query.isBlank()) {
                allPosts
            } else {
                allPosts.filter { 
                    it.title.contains(query, ignoreCase = true) 
                }
            }
            _uiState.update { it.copy(posts = filtered, isLoading = false) }
        } catch (e: Exception) {
            _uiState.update { it.copy(error = e.message, isLoading = false) }
        }
    }
}

data class SearchUiState(
    val posts: List<Post> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SearchPostsScreen(viewModel: SearchPostsViewModel = viewModel()) {
    val query by viewModel.searchQuery.collectAsState()
    val uiState by viewModel.uiState.collectAsState()

    Column(modifier = Modifier.fillMaxSize()) {
        OutlinedTextField(
            value = query,
            onValueChange = viewModel::onSearchQueryChange,
            label = { Text("Buscar posts") },
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            leadingIcon = { Icon(Icons.Default.Search, null) }
        )

        when {
            uiState.isLoading -> {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            }
            else -> {
                LazyColumn {
                    items(uiState.posts, key = { it.id }) { post ->
                        Card(modifier = Modifier.padding(8.dp).fillMaxWidth()) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Text(post.title, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }
        }
    }
}
```
