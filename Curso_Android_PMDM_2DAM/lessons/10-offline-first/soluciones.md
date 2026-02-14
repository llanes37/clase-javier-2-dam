# Soluciones - Lección 10: Offline-First

## Ejercicio 1: Lista de posts offline

```kotlin
// data/local/entity/PostEntity.kt
@Entity(tableName = "posts")
data class PostEntity(
    @PrimaryKey
    val id: Int,
    val userId: Int,
    val title: String,
    val body: String,
    @ColumnInfo(name = "last_updated")
    val lastUpdated: Long = System.currentTimeMillis()
)

// data/remote/dto/PostDto.kt
@JsonClass(generateAdapter = true)
data class PostDto(
    val id: Int,
    val userId: Int,
    val title: String,
    val body: String
)

// Mappers
fun PostDto.toEntity() = PostEntity(
    id = id, userId = userId, title = title, body = body
)
fun PostEntity.toDomain() = Post(
    id = id, userId = userId, title = title, body = body
)

// data/local/dao/PostDao.kt
@Dao
interface PostDao {
    @Query("SELECT * FROM posts ORDER BY id DESC")
    fun observeAll(): Flow<List<PostEntity>>
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(posts: List<PostEntity>)
    
    @Query("DELETE FROM posts")
    suspend fun deleteAll()
}

// data/remote/api/PostApi.kt
interface PostApi {
    @GET("posts")
    suspend fun getPosts(): List<PostDto>
}

// data/repository/PostRepository.kt
class PostRepository(
    private val postDao: PostDao,
    private val postApi: PostApi
) {
    fun observePosts(): Flow<List<Post>> {
        return postDao.observeAll().map { entities ->
            entities.map { it.toDomain() }
        }
    }
    
    suspend fun refresh(): Result<Unit> {
        return try {
            val remotePosts = postApi.getPosts()
            postDao.deleteAll()
            postDao.insertAll(remotePosts.map { it.toEntity() })
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

// ui/posts/PostListViewModel.kt
data class PostListUiState(
    val posts: List<Post> = emptyList(),
    val isLoading: Boolean = true,
    val isRefreshing: Boolean = false,
    val error: String? = null,
    val isOffline: Boolean = false
)

class PostListViewModel(
    private val repository: PostRepository,
    private val connectivityObserver: ConnectivityObserver
) : ViewModel() {
    
    private val _isRefreshing = MutableStateFlow(false)
    private val _error = MutableStateFlow<String?>(null)
    
    val uiState: StateFlow<PostListUiState> = combine(
        repository.observePosts(),
        _isRefreshing,
        _error,
        connectivityObserver.observe()
    ) { posts, refreshing, error, connectivity ->
        PostListUiState(
            posts = posts,
            isLoading = posts.isEmpty() && refreshing,
            isRefreshing = refreshing,
            error = error,
            isOffline = connectivity == ConnectivityStatus.OFFLINE
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), PostListUiState())
    
    init { refresh() }
    
    fun refresh() {
        viewModelScope.launch {
            _isRefreshing.value = true
            _error.value = null
            
            repository.refresh().onFailure { e ->
                _error.value = if (e is UnknownHostException) {
                    "Sin conexión. Mostrando datos guardados."
                } else {
                    e.message
                }
            }
            
            _isRefreshing.value = false
        }
    }
}
```

---

## Ejercicio 2: Caché inteligente

```kotlin
// PostDao.kt (añadir)
@Query("SELECT MAX(last_updated) FROM posts")
suspend fun getLastUpdateTime(): Long?

// PostRepository.kt actualizado
class PostRepository(
    private val postDao: PostDao,
    private val postApi: PostApi
) {
    private val cacheMaxAge = 5 * 60 * 1000L  // 5 minutos
    
    fun observePosts(): Flow<List<Post>> =
        postDao.observeAll().map { it.map { e -> e.toDomain() } }
    
    fun observeLastUpdateTime(): Flow<Long?> = flow {
        emit(postDao.getLastUpdateTime())
    }
    
    suspend fun refreshIfNeeded(): Result<Unit> {
        val lastUpdate = postDao.getLastUpdateTime() ?: 0
        val age = System.currentTimeMillis() - lastUpdate
        
        return if (age > cacheMaxAge) {
            refresh()
        } else {
            Result.success(Unit)
        }
    }
    
    suspend fun refresh(): Result<Unit> {
        return try {
            val remotePosts = postApi.getPosts()
            postDao.deleteAll()
            postDao.insertAll(remotePosts.map { it.toEntity() })
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

// ViewModel
class PostListViewModel(private val repository: PostRepository) : ViewModel() {
    
    val lastUpdateTime: StateFlow<String> = repository.observeLastUpdateTime()
        .map { timestamp ->
            if (timestamp == null) return@map "Nunca"
            val minutes = (System.currentTimeMillis() - timestamp) / 60000
            when {
                minutes < 1 -> "Hace un momento"
                minutes < 60 -> "Hace $minutes minutos"
                else -> "Hace ${minutes / 60} horas"
            }
        }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "")
    
    init {
        viewModelScope.launch {
            repository.refreshIfNeeded()
        }
    }
    
    fun forceRefresh() {
        viewModelScope.launch {
            repository.refresh()
        }
    }
}
```

---

## Ejercicio 3: Crear posts offline

```kotlin
// PostEntity.kt (modificar)
@Entity(tableName = "posts")
data class PostEntity(
    @PrimaryKey
    val id: Int,
    val userId: Int,
    val title: String,
    val body: String,
    @ColumnInfo(name = "is_synced")
    val isSynced: Boolean = true,
    @ColumnInfo(name = "last_updated")
    val lastUpdated: Long = System.currentTimeMillis()
)

// PostDao.kt (añadir)
@Insert(onConflict = OnConflictStrategy.REPLACE)
suspend fun insert(post: PostEntity): Long

@Query("SELECT * FROM posts WHERE is_synced = 0")
suspend fun getPendingSync(): List<PostEntity>

@Query("UPDATE posts SET is_synced = 1 WHERE id = :postId")
suspend fun markAsSynced(postId: Int)

@Query("UPDATE posts SET id = :newId, is_synced = 1 WHERE id = :oldId")
suspend fun updateIdAndMarkSynced(oldId: Int, newId: Int)

// PostApi.kt (añadir)
@POST("posts")
suspend fun createPost(@Body post: PostDto): PostDto

// PostRepository.kt
class PostRepository(
    private val postDao: PostDao,
    private val postApi: PostApi
) {
    private var tempIdCounter = -1
    
    suspend fun createPost(title: String, body: String, userId: Int = 1): Result<Post> {
        // Guardar localmente primero
        val tempId = tempIdCounter--
        val localPost = PostEntity(
            id = tempId,
            userId = userId,
            title = title,
            body = body,
            isSynced = false
        )
        postDao.insert(localPost)
        
        // Intentar sincronizar
        return try {
            val remotePost = postApi.createPost(PostDto(0, userId, title, body))
            postDao.updateIdAndMarkSynced(tempId, remotePost.id)
            Result.success(remotePost.toEntity().toDomain())
        } catch (e: Exception) {
            // Mantener como pendiente
            Result.success(localPost.toDomain())
        }
    }
    
    suspend fun syncPendingPosts() {
        val pending = postDao.getPendingSync()
        for (post in pending) {
            try {
                val remote = postApi.createPost(
                    PostDto(0, post.userId, post.title, post.body)
                )
                postDao.updateIdAndMarkSynced(post.id, remote.id)
            } catch (e: Exception) {
                // Mantener pendiente
            }
        }
    }
}

// UI para mostrar pendientes
@Composable
fun PostItem(post: Post, isPending: Boolean) {
    Card(
        modifier = Modifier.fillMaxWidth().padding(8.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (isPending) 
                MaterialTheme.colorScheme.surfaceVariant 
            else 
                MaterialTheme.colorScheme.surface
        )
    ) {
        Row(modifier = Modifier.padding(16.dp)) {
            Column(modifier = Modifier.weight(1f)) {
                Text(post.title, fontWeight = FontWeight.Bold)
                Text(post.body, maxLines = 2)
            }
            if (isPending) {
                Icon(
                    Icons.Default.CloudUpload,
                    contentDescription = "Pendiente de sincronizar",
                    tint = MaterialTheme.colorScheme.primary
                )
            }
        }
    }
}
```

---

## Ejercicio 4: Observador de conectividad

```kotlin
// ConnectivityObserver.kt
sealed class ConnectivityStatus {
    object ONLINE : ConnectivityStatus()
    object OFFLINE : ConnectivityStatus()
}

class ConnectivityObserver(context: Context) {
    private val connectivityManager = 
        context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
    
    fun observe(): Flow<ConnectivityStatus> = callbackFlow {
        val callback = object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: Network) {
                trySend(ConnectivityStatus.ONLINE)
            }
            
            override fun onLost(network: Network) {
                trySend(ConnectivityStatus.OFFLINE)
            }
        }
        
        val request = NetworkRequest.Builder()
            .addCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
            .build()
        
        connectivityManager.registerNetworkCallback(request, callback)
        
        // Estado inicial
        val activeNetwork = connectivityManager.activeNetworkInfo
        val isConnected = activeNetwork?.isConnectedOrConnecting == true
        trySend(if (isConnected) ConnectivityStatus.ONLINE else ConnectivityStatus.OFFLINE)
        
        awaitClose { connectivityManager.unregisterNetworkCallback(callback) }
    }
    
    fun isOnline(): Boolean {
        val activeNetwork = connectivityManager.activeNetworkInfo
        return activeNetwork?.isConnectedOrConnecting == true
    }
}

// ViewModel con auto-refresh
class PostListViewModel(
    private val repository: PostRepository,
    private val connectivityObserver: ConnectivityObserver
) : ViewModel() {
    
    init {
        // Auto-refresh cuando vuelve la conexión
        viewModelScope.launch {
            connectivityObserver.observe()
                .distinctUntilChanged()
                .filter { it == ConnectivityStatus.ONLINE }
                .collect {
                    repository.syncPendingPosts()
                    repository.refresh()
                }
        }
    }
}

// Banner de offline
@Composable
fun OfflineBanner(isOffline: Boolean) {
    AnimatedVisibility(visible = isOffline) {
        Surface(
            color = MaterialTheme.colorScheme.errorContainer,
            modifier = Modifier.fillMaxWidth()
        ) {
            Row(
                modifier = Modifier.padding(12.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.Center
            ) {
                Icon(Icons.Default.CloudOff, null, modifier = Modifier.size(16.dp))
                Spacer(Modifier.width(8.dp))
                Text("Sin conexión - Modo offline")
            }
        }
    }
}
```

---

## Ejercicio 5: Detalle con caché

```kotlin
// PostDao.kt (añadir)
@Query("SELECT * FROM posts WHERE id = :postId")
suspend fun getById(postId: Int): PostEntity?

// PostApi.kt (añadir)
@GET("posts/{id}")
suspend fun getPost(@Path("id") postId: Int): PostDto

// PostRepository.kt
class PostRepository(...) {
    
    suspend fun getPost(postId: Int): Result<Post> {
        // Buscar en caché primero
        val cached = postDao.getById(postId)
        
        if (cached != null) {
            val age = System.currentTimeMillis() - cached.lastUpdated
            if (age < cacheMaxAge) {
                return Result.success(cached.toDomain())
            }
        }
        
        // Obtener de red si no hay caché o está viejo
        return try {
            val remote = postApi.getPost(postId)
            postDao.insert(remote.toEntity())
            Result.success(remote.toEntity().toDomain())
        } catch (e: Exception) {
            // Si hay caché aunque esté viejo, usarlo
            if (cached != null) {
                Result.success(cached.toDomain())
            } else {
                Result.failure(e)
            }
        }
    }
}

// PostDetailViewModel.kt
sealed class PostDetailUiState {
    object Loading : PostDetailUiState()
    data class Success(val post: Post, val isFromCache: Boolean) : PostDetailUiState()
    data class Error(val message: String) : PostDetailUiState()
}

class PostDetailViewModel(
    private val postId: Int,
    private val repository: PostRepository
) : ViewModel() {
    
    private val _uiState = MutableStateFlow<PostDetailUiState>(PostDetailUiState.Loading)
    val uiState: StateFlow<PostDetailUiState> = _uiState.asStateFlow()
    
    init { loadPost() }
    
    fun loadPost() {
        viewModelScope.launch {
            _uiState.value = PostDetailUiState.Loading
            
            repository.getPost(postId)
                .onSuccess { post ->
                    _uiState.value = PostDetailUiState.Success(post, isFromCache = false)
                }
                .onFailure { e ->
                    _uiState.value = PostDetailUiState.Error(
                        if (e is UnknownHostException) "Sin conexión y sin datos guardados"
                        else e.message ?: "Error"
                    )
                }
        }
    }
}
```

---

## Ejercicio 6: Eliminar offline

```kotlin
// PendingOperationEntity.kt
@Entity(tableName = "pending_operations")
data class PendingOperationEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val type: String,  // "DELETE"
    val entityId: Int,
    val createdAt: Long = System.currentTimeMillis()
)

// PendingOperationDao.kt
@Dao
interface PendingOperationDao {
    @Insert
    suspend fun insert(operation: PendingOperationEntity)
    
    @Query("SELECT * FROM pending_operations WHERE type = 'DELETE'")
    suspend fun getDeleteOperations(): List<PendingOperationEntity>
    
    @Delete
    suspend fun delete(operation: PendingOperationEntity)
}

// PostApi.kt (añadir)
@DELETE("posts/{id}")
suspend fun deletePost(@Path("id") postId: Int)

// PostRepository.kt
class PostRepository(
    private val postDao: PostDao,
    private val postApi: PostApi,
    private val pendingDao: PendingOperationDao
) {
    suspend fun deletePost(postId: Int): Result<Unit> {
        // Eliminar localmente inmediatamente
        postDao.deleteById(postId)
        
        // Intentar eliminar en servidor
        return try {
            postApi.deletePost(postId)
            Result.success(Unit)
        } catch (e: Exception) {
            // Guardar operación pendiente
            pendingDao.insert(PendingOperationEntity(
                type = "DELETE",
                entityId = postId
            ))
            Result.success(Unit)  // Éxito local
        }
    }
    
    suspend fun syncPendingDeletes() {
        val pending = pendingDao.getDeleteOperations()
        for (op in pending) {
            try {
                postApi.deletePost(op.entityId)
                pendingDao.delete(op)
            } catch (e: Exception) {
                // Mantener pendiente
            }
        }
    }
}
```
