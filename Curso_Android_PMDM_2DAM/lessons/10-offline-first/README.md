# Lección 10: Arquitectura Offline-First

## Objetivos

- Entender el patrón Offline-First
- Combinar Room con Retrofit
- Implementar caché inteligente
- Manejar sincronización
- Resolver conflictos de datos

---

## 1. ¿Qué es Offline-First?

La app funciona sin conexión usando datos locales, y sincroniza cuando hay red.

### Beneficios

- Funciona sin internet
- Respuesta instantánea (datos locales)
- Menor consumo de datos
- Mejor UX

### Flujo de datos

```
UI ← ViewModel ← Repository ← Room (caché)
                           ← Retrofit (red)
```

**Regla de oro:** La UI siempre lee de Room. La red solo actualiza Room.

---

## 2. Arquitectura

```kotlin
// Single Source of Truth: Room
class UserRepository(
    private val userDao: UserDao,
    private val userApi: UserApi
) {
    // La UI observa Room
    fun observeUsers(): Flow<List<User>> {
        return userDao.observeAll().map { entities ->
            entities.map { it.toDomain() }
        }
    }
    
    // Refresh desde la red
    suspend fun refreshUsers(): Result<Unit> {
        return try {
            val remoteUsers = userApi.getUsers()
            userDao.insertAll(remoteUsers.map { it.toEntity() })
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

---

## 3. Implementación completa

### Entidad y DTO

```kotlin
// Entidad local (Room)
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey
    val id: Int,
    val name: String,
    val email: String,
    @ColumnInfo(name = "last_updated")
    val lastUpdated: Long = System.currentTimeMillis()
)

// DTO de red (Retrofit)
@JsonClass(generateAdapter = true)
data class UserDto(
    val id: Int,
    val name: String,
    val email: String
)

// Modelo de dominio
data class User(
    val id: Int,
    val name: String,
    val email: String
)

// Mappers
fun UserDto.toEntity() = UserEntity(id = id, name = name, email = email)
fun UserEntity.toDomain() = User(id = id, name = name, email = email)
```

### DAO

```kotlin
@Dao
interface UserDao {
    @Query("SELECT * FROM users ORDER BY name")
    fun observeAll(): Flow<List<UserEntity>>
    
    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getById(userId: Int): UserEntity?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(users: List<UserEntity>)
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(user: UserEntity)
    
    @Query("DELETE FROM users")
    suspend fun deleteAll()
    
    @Query("SELECT MAX(last_updated) FROM users")
    suspend fun getLastUpdateTime(): Long?
}
```

### API

```kotlin
interface UserApi {
    @GET("users")
    suspend fun getUsers(): List<UserDto>
    
    @GET("users/{id}")
    suspend fun getUser(@Path("id") userId: Int): UserDto
    
    @POST("users")
    suspend fun createUser(@Body user: UserDto): UserDto
    
    @PUT("users/{id}")
    suspend fun updateUser(@Path("id") userId: Int, @Body user: UserDto): UserDto
}
```

### Repository

```kotlin
class UserRepository(
    private val userDao: UserDao,
    private val userApi: UserApi
) {
    // Observar datos locales (UI siempre lee de aquí)
    fun observeUsers(): Flow<List<User>> {
        return userDao.observeAll().map { entities ->
            entities.map { it.toDomain() }
        }
    }
    
    // Refresh: obtener de red y guardar en local
    suspend fun refreshUsers(): Result<Unit> {
        return try {
            val remoteUsers = userApi.getUsers()
            userDao.deleteAll()  // Limpiar caché
            userDao.insertAll(remoteUsers.map { it.toEntity() })
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Refresh inteligente (solo si datos viejos)
    suspend fun refreshIfNeeded(maxAgeMs: Long = 5 * 60 * 1000): Result<Unit> {
        val lastUpdate = userDao.getLastUpdateTime() ?: 0
        val age = System.currentTimeMillis() - lastUpdate
        
        return if (age > maxAgeMs) {
            refreshUsers()
        } else {
            Result.success(Unit)  // Datos frescos
        }
    }
    
    // Obtener usuario (local + red si necesario)
    suspend fun getUser(userId: Int): Result<User> {
        // Primero buscar en local
        val local = userDao.getById(userId)
        if (local != null) {
            return Result.success(local.toDomain())
        }
        
        // Si no existe, buscar en red
        return try {
            val remote = userApi.getUser(userId)
            userDao.insert(remote.toEntity())
            Result.success(remote.toEntity().toDomain())
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

---

## 4. ViewModel con estados

```kotlin
data class UserListUiState(
    val users: List<User> = emptyList(),
    val isLoading: Boolean = false,
    val isRefreshing: Boolean = false,
    val error: String? = null,
    val isOffline: Boolean = false
)

class UserListViewModel(
    private val repository: UserRepository,
    private val connectivityObserver: ConnectivityObserver
) : ViewModel() {
    
    private val _isRefreshing = MutableStateFlow(false)
    private val _error = MutableStateFlow<String?>(null)
    
    val uiState: StateFlow<UserListUiState> = combine(
        repository.observeUsers(),
        _isRefreshing,
        _error,
        connectivityObserver.observe()
    ) { users, isRefreshing, error, connectivity ->
        UserListUiState(
            users = users,
            isLoading = users.isEmpty() && isRefreshing,
            isRefreshing = isRefreshing,
            error = error,
            isOffline = connectivity == ConnectivityStatus.OFFLINE
        )
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = UserListUiState(isLoading = true)
    )
    
    init {
        refresh()
    }
    
    fun refresh() {
        viewModelScope.launch {
            _isRefreshing.value = true
            _error.value = null
            
            repository.refreshUsers()
                .onFailure { e ->
                    _error.value = when (e) {
                        is UnknownHostException -> "Sin conexión. Mostrando datos guardados."
                        else -> e.message
                    }
                }
            
            _isRefreshing.value = false
        }
    }
    
    fun clearError() {
        _error.value = null
    }
}
```

---

## 5. Observador de conectividad

```kotlin
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
        val isConnected = connectivityManager.activeNetwork != null
        trySend(if (isConnected) ConnectivityStatus.ONLINE else ConnectivityStatus.OFFLINE)
        
        awaitClose {
            connectivityManager.unregisterNetworkCallback(callback)
        }
    }
}
```

---

## 6. UI con indicadores

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UserListScreen(viewModel: UserListViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    val snackbarHostState = remember { SnackbarHostState() }
    
    // Mostrar error como snackbar
    LaunchedEffect(uiState.error) {
        uiState.error?.let { error ->
            snackbarHostState.showSnackbar(error)
            viewModel.clearError()
        }
    }
    
    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) },
        topBar = {
            TopAppBar(
                title = { Text("Usuarios") },
                actions = {
                    // Indicador offline
                    if (uiState.isOffline) {
                        Icon(
                            Icons.Default.CloudOff,
                            contentDescription = "Sin conexión",
                            tint = MaterialTheme.colorScheme.error
                        )
                    }
                }
            )
        }
    ) { padding ->
        PullToRefreshBox(
            isRefreshing = uiState.isRefreshing,
            onRefresh = { viewModel.refresh() },
            modifier = Modifier.padding(padding)
        ) {
            when {
                uiState.isLoading -> {
                    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        CircularProgressIndicator()
                    }
                }
                uiState.users.isEmpty() -> {
                    EmptyState(
                        message = if (uiState.isOffline) 
                            "Sin conexión y sin datos guardados" 
                        else 
                            "No hay usuarios"
                    )
                }
                else -> {
                    LazyColumn {
                        // Banner offline
                        if (uiState.isOffline) {
                            item {
                                Surface(
                                    color = MaterialTheme.colorScheme.errorContainer,
                                    modifier = Modifier.fillMaxWidth()
                                ) {
                                    Text(
                                        "Modo sin conexión - Mostrando datos guardados",
                                        modifier = Modifier.padding(8.dp),
                                        textAlign = TextAlign.Center
                                    )
                                }
                            }
                        }
                        
                        items(uiState.users, key = { it.id }) { user ->
                            UserItem(user)
                        }
                    }
                }
            }
        }
    }
}
```

---

## 7. Operaciones Create/Update offline

### Patrón: guardar local + sincronizar

```kotlin
@Entity(tableName = "pending_operations")
data class PendingOperation(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val type: String,  // "CREATE", "UPDATE", "DELETE"
    val entityType: String,
    val entityId: Int?,
    val payload: String,  // JSON del objeto
    val createdAt: Long = System.currentTimeMillis()
)

class UserRepository(
    private val userDao: UserDao,
    private val userApi: UserApi,
    private val pendingDao: PendingOperationDao
) {
    suspend fun createUser(name: String, email: String): Result<User> {
        // Crear localmente con ID temporal negativo
        val tempId = -(System.currentTimeMillis().toInt())
        val localUser = UserEntity(
            id = tempId,
            name = name,
            email = email
        )
        userDao.insert(localUser)
        
        // Intentar sincronizar
        return try {
            val remoteUser = userApi.createUser(UserDto(0, name, email))
            // Reemplazar temporal con real
            userDao.delete(tempId)
            userDao.insert(remoteUser.toEntity())
            Result.success(remoteUser.toEntity().toDomain())
        } catch (e: Exception) {
            // Guardar operación pendiente
            pendingDao.insert(PendingOperation(
                type = "CREATE",
                entityType = "user",
                entityId = tempId,
                payload = Json.encodeToString(localUser)
            ))
            Result.success(localUser.toDomain())  // Devolver local
        }
    }
    
    // Sincronizar pendientes cuando haya conexión
    suspend fun syncPending() {
        val pending = pendingDao.getAll()
        
        for (op in pending) {
            try {
                when (op.type) {
                    "CREATE" -> {
                        val user = Json.decodeFromString<UserEntity>(op.payload)
                        val remote = userApi.createUser(UserDto(0, user.name, user.email))
                        userDao.delete(user.id)
                        userDao.insert(remote.toEntity())
                    }
                    // UPDATE, DELETE...
                }
                pendingDao.delete(op)
            } catch (e: Exception) {
                // Mantener pendiente para próximo intento
            }
        }
    }
}
```

---

## 8. WorkManager para sincronización

```kotlin
class SyncWorker(
    context: Context,
    params: WorkerParameters,
    private val repository: UserRepository
) : CoroutineWorker(context, params) {
    
    override suspend fun doWork(): Result {
        return try {
            repository.syncPending()
            repository.refreshUsers()
            Result.success()
        } catch (e: Exception) {
            Result.retry()
        }
    }
}

// Programar sincronización
fun scheduleSyncWork(context: Context) {
    val constraints = Constraints.Builder()
        .setRequiredNetworkType(NetworkType.CONNECTED)
        .build()
    
    val syncRequest = PeriodicWorkRequestBuilder<SyncWorker>(
        15, TimeUnit.MINUTES
    )
        .setConstraints(constraints)
        .build()
    
    WorkManager.getInstance(context).enqueueUniquePeriodicWork(
        "sync_work",
        ExistingPeriodicWorkPolicy.KEEP,
        syncRequest
    )
}
```

---

## Resumen

| Concepto | Descripción |
|----------|-------------|
| Offline-First | Datos locales como fuente principal |
| Single Source of Truth | UI solo lee de Room |
| Refresh | Red actualiza Room |
| Operaciones pendientes | Guardar para sincronizar después |
| ConnectivityObserver | Detectar estado de red |
| WorkManager | Sincronización en background |

### Flujo típico

1. App inicia → Mostrar datos de Room
2. Si hay red → Refresh desde API → Guardar en Room
3. Crear/Editar → Guardar en Room + Intentar sincronizar
4. Sin red → Guardar operación pendiente
5. Red disponible → Sincronizar pendientes

---

## Siguiente paso

→ [ejercicios.md](ejercicios.md)
