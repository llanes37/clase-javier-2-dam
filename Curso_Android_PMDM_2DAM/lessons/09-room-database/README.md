# Lección 09: Room - Base de datos local

## Objetivos

- Configurar Room para persistencia local
- Definir entidades y DAOs
- Implementar operaciones CRUD
- Usar Flow para datos reactivos
- Relaciones entre tablas
- Migraciones de base de datos

---

## 1. Dependencias

```kotlin
// build.gradle.kts (app)
plugins {
    id("com.google.devtools.ksp")
}

dependencies {
    val roomVersion = "2.6.1"
    
    implementation("androidx.room:room-runtime:$roomVersion")
    implementation("androidx.room:room-ktx:$roomVersion")
    ksp("androidx.room:room-compiler:$roomVersion")
}
```

---

## 2. Entidad (Tabla)

```kotlin
// data/local/entity/TaskEntity.kt
@Entity(tableName = "tasks")
data class TaskEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    
    @ColumnInfo(name = "title")
    val title: String,
    
    @ColumnInfo(name = "description")
    val description: String? = null,
    
    @ColumnInfo(name = "is_completed")
    val isCompleted: Boolean = false,
    
    @ColumnInfo(name = "created_at")
    val createdAt: Long = System.currentTimeMillis()
)
```

### Anotaciones principales

| Anotación | Uso |
|-----------|-----|
| `@Entity` | Marca la clase como tabla |
| `@PrimaryKey` | Clave primaria |
| `@ColumnInfo` | Personalizar nombre de columna |
| `@Ignore` | Ignorar campo en la tabla |
| `@Index` | Crear índice para búsquedas |

---

## 3. DAO (Data Access Object)

```kotlin
// data/local/dao/TaskDao.kt
@Dao
interface TaskDao {
    
    // Obtener todas las tareas (reactivo)
    @Query("SELECT * FROM tasks ORDER BY created_at DESC")
    fun observeAll(): Flow<List<TaskEntity>>
    
    // Obtener una tarea por ID
    @Query("SELECT * FROM tasks WHERE id = :taskId")
    suspend fun getById(taskId: Int): TaskEntity?
    
    // Obtener tareas completadas
    @Query("SELECT * FROM tasks WHERE is_completed = :completed")
    fun observeByCompleted(completed: Boolean): Flow<List<TaskEntity>>
    
    // Buscar tareas
    @Query("SELECT * FROM tasks WHERE title LIKE '%' || :query || '%'")
    fun search(query: String): Flow<List<TaskEntity>>
    
    // Insertar una tarea
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(task: TaskEntity): Long
    
    // Insertar múltiples tareas
    @Insert
    suspend fun insertAll(tasks: List<TaskEntity>)
    
    // Actualizar tarea
    @Update
    suspend fun update(task: TaskEntity)
    
    // Eliminar tarea
    @Delete
    suspend fun delete(task: TaskEntity)
    
    // Eliminar por ID
    @Query("DELETE FROM tasks WHERE id = :taskId")
    suspend fun deleteById(taskId: Int)
    
    // Eliminar todas
    @Query("DELETE FROM tasks")
    suspend fun deleteAll()
    
    // Marcar como completada
    @Query("UPDATE tasks SET is_completed = :completed WHERE id = :taskId")
    suspend fun setCompleted(taskId: Int, completed: Boolean)
    
    // Contar tareas
    @Query("SELECT COUNT(*) FROM tasks WHERE is_completed = 0")
    fun countPending(): Flow<Int>
}
```

### Estrategias de conflicto

| Estrategia | Comportamiento |
|------------|----------------|
| `REPLACE` | Reemplaza si existe |
| `IGNORE` | Ignora si existe |
| `ABORT` | Cancela operación (default) |

---

## 4. Database

```kotlin
// data/local/AppDatabase.kt
@Database(
    entities = [TaskEntity::class],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    
    abstract fun taskDao(): TaskDao
    
    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null
        
        fun getInstance(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "app_database"
                )
                .fallbackToDestructiveMigration()  // Solo en desarrollo
                .build()
                
                INSTANCE = instance
                instance
            }
        }
    }
}
```

---

## 5. Repository

```kotlin
// data/repository/TaskRepository.kt
class TaskRepository(private val taskDao: TaskDao) {
    
    fun observeAllTasks(): Flow<List<Task>> {
        return taskDao.observeAll().map { entities ->
            entities.map { it.toDomain() }
        }
    }
    
    fun observePendingTasks(): Flow<List<Task>> {
        return taskDao.observeByCompleted(false).map { entities ->
            entities.map { it.toDomain() }
        }
    }
    
    suspend fun getTask(id: Int): Task? {
        return taskDao.getById(id)?.toDomain()
    }
    
    suspend fun addTask(title: String, description: String?): Long {
        val entity = TaskEntity(
            title = title,
            description = description
        )
        return taskDao.insert(entity)
    }
    
    suspend fun updateTask(task: Task) {
        taskDao.update(task.toEntity())
    }
    
    suspend fun toggleCompleted(taskId: Int, completed: Boolean) {
        taskDao.setCompleted(taskId, completed)
    }
    
    suspend fun deleteTask(taskId: Int) {
        taskDao.deleteById(taskId)
    }
    
    fun countPending(): Flow<Int> {
        return taskDao.countPending()
    }
}

// Mappers
fun TaskEntity.toDomain() = Task(
    id = id,
    title = title,
    description = description,
    isCompleted = isCompleted,
    createdAt = createdAt
)

fun Task.toEntity() = TaskEntity(
    id = id,
    title = title,
    description = description,
    isCompleted = isCompleted,
    createdAt = createdAt
)
```

---

## 6. ViewModel

```kotlin
data class TaskListUiState(
    val tasks: List<Task> = emptyList(),
    val pendingCount: Int = 0,
    val filter: TaskFilter = TaskFilter.ALL
)

enum class TaskFilter { ALL, PENDING, COMPLETED }

class TaskViewModel(
    private val repository: TaskRepository
) : ViewModel() {
    
    private val _filter = MutableStateFlow(TaskFilter.ALL)
    
    val uiState: StateFlow<TaskListUiState> = combine(
        _filter,
        repository.observeAllTasks(),
        repository.countPending()
    ) { filter, allTasks, pendingCount ->
        val filteredTasks = when (filter) {
            TaskFilter.ALL -> allTasks
            TaskFilter.PENDING -> allTasks.filter { !it.isCompleted }
            TaskFilter.COMPLETED -> allTasks.filter { it.isCompleted }
        }
        
        TaskListUiState(
            tasks = filteredTasks,
            pendingCount = pendingCount,
            filter = filter
        )
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = TaskListUiState()
    )
    
    fun setFilter(filter: TaskFilter) {
        _filter.value = filter
    }
    
    fun addTask(title: String, description: String?) {
        viewModelScope.launch {
            repository.addTask(title, description)
        }
    }
    
    fun toggleCompleted(taskId: Int, completed: Boolean) {
        viewModelScope.launch {
            repository.toggleCompleted(taskId, completed)
        }
    }
    
    fun deleteTask(taskId: Int) {
        viewModelScope.launch {
            repository.deleteTask(taskId)
        }
    }
}
```

---

## 7. Relaciones entre tablas

### One-to-Many

```kotlin
@Entity(tableName = "categories")
data class CategoryEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val name: String
)

@Entity(
    tableName = "tasks",
    foreignKeys = [
        ForeignKey(
            entity = CategoryEntity::class,
            parentColumns = ["id"],
            childColumns = ["category_id"],
            onDelete = ForeignKey.CASCADE
        )
    ],
    indices = [Index("category_id")]
)
data class TaskEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val title: String,
    @ColumnInfo(name = "category_id")
    val categoryId: Int? = null
)

// Clase para relación
data class CategoryWithTasks(
    @Embedded
    val category: CategoryEntity,
    
    @Relation(
        parentColumn = "id",
        entityColumn = "category_id"
    )
    val tasks: List<TaskEntity>
)

// En DAO
@Transaction
@Query("SELECT * FROM categories")
fun getCategoriesWithTasks(): Flow<List<CategoryWithTasks>>
```

### Many-to-Many

```kotlin
@Entity(tableName = "tags")
data class TagEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val name: String
)

// Tabla intermedia
@Entity(
    tableName = "task_tag_cross_ref",
    primaryKeys = ["taskId", "tagId"]
)
data class TaskTagCrossRef(
    val taskId: Int,
    val tagId: Int
)

data class TaskWithTags(
    @Embedded
    val task: TaskEntity,
    
    @Relation(
        parentColumn = "id",
        entityColumn = "id",
        associateBy = Junction(
            TaskTagCrossRef::class,
            parentColumn = "taskId",
            entityColumn = "tagId"
        )
    )
    val tags: List<TagEntity>
)
```

---

## 8. Migraciones

```kotlin
@Database(
    entities = [TaskEntity::class],
    version = 2  // Incrementar versión
)
abstract class AppDatabase : RoomDatabase() {
    // ...
    
    companion object {
        // Migración de versión 1 a 2
        private val MIGRATION_1_2 = object : Migration(1, 2) {
            override fun migrate(database: SupportSQLiteDatabase) {
                database.execSQL(
                    "ALTER TABLE tasks ADD COLUMN priority INTEGER NOT NULL DEFAULT 0"
                )
            }
        }
        
        fun getInstance(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "app_database"
                )
                .addMigrations(MIGRATION_1_2)
                .build()
            }
        }
    }
}
```

---

## 9. Type Converters

Para tipos no soportados:

```kotlin
class Converters {
    @TypeConverter
    fun fromTimestamp(value: Long?): Date? {
        return value?.let { Date(it) }
    }
    
    @TypeConverter
    fun dateToTimestamp(date: Date?): Long? {
        return date?.time
    }
    
    @TypeConverter
    fun fromStringList(value: String?): List<String>? {
        return value?.split(",")
    }
    
    @TypeConverter
    fun toStringList(list: List<String>?): String? {
        return list?.joinToString(",")
    }
}

@Database(...)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase()
```

---

## 10. Testing

```kotlin
@RunWith(AndroidJUnit4::class)
class TaskDaoTest {
    
    private lateinit var database: AppDatabase
    private lateinit var taskDao: TaskDao
    
    @Before
    fun setup() {
        database = Room.inMemoryDatabaseBuilder(
            ApplicationProvider.getApplicationContext(),
            AppDatabase::class.java
        )
        .allowMainThreadQueries()  // Solo en tests
        .build()
        
        taskDao = database.taskDao()
    }
    
    @After
    fun tearDown() {
        database.close()
    }
    
    @Test
    fun insertAndGetTask() = runTest {
        val task = TaskEntity(title = "Test Task")
        val id = taskDao.insert(task)
        
        val retrieved = taskDao.getById(id.toInt())
        
        assertNotNull(retrieved)
        assertEquals("Test Task", retrieved?.title)
    }
    
    @Test
    fun observeTasksFlow() = runTest {
        val task1 = TaskEntity(title = "Task 1")
        val task2 = TaskEntity(title = "Task 2")
        
        taskDao.insert(task1)
        taskDao.insert(task2)
        
        val tasks = taskDao.observeAll().first()
        
        assertEquals(2, tasks.size)
    }
}
```

---

## Resumen

| Componente | Función |
|------------|---------|
| `@Entity` | Define tabla |
| `@Dao` | Define operaciones |
| `@Database` | Configura base de datos |
| `Flow<List<T>>` | Observación reactiva |
| `suspend fun` | Operaciones one-shot |
| `@Transaction` | Operaciones atómicas |
| `Migration` | Actualizar esquema |

---

## Siguiente paso

→ [ejercicios.md](ejercicios.md)
