# Soluciones - Lección 09: Room Database

## Ejercicio 1: App de notas básica

```kotlin
// data/local/entity/NoteEntity.kt
@Entity(tableName = "notes")
data class NoteEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val title: String,
    val content: String,
    @ColumnInfo(name = "created_at")
    val createdAt: Long = System.currentTimeMillis(),
    @ColumnInfo(name = "updated_at")
    val updatedAt: Long = System.currentTimeMillis()
)

// data/local/dao/NoteDao.kt
@Dao
interface NoteDao {
    @Query("SELECT * FROM notes ORDER BY updated_at DESC")
    fun observeAll(): Flow<List<NoteEntity>>
    
    @Query("SELECT * FROM notes WHERE id = :noteId")
    suspend fun getById(noteId: Int): NoteEntity?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(note: NoteEntity): Long
    
    @Update
    suspend fun update(note: NoteEntity)
    
    @Delete
    suspend fun delete(note: NoteEntity)
    
    @Query("DELETE FROM notes WHERE id = :noteId")
    suspend fun deleteById(noteId: Int)
}

// data/local/AppDatabase.kt
@Database(entities = [NoteEntity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun noteDao(): NoteDao
    
    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null
        
        fun getInstance(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "notes_database"
                ).build().also { INSTANCE = it }
            }
        }
    }
}

// data/repository/NoteRepository.kt
class NoteRepository(private val noteDao: NoteDao) {
    fun observeAllNotes(): Flow<List<Note>> =
        noteDao.observeAll().map { entities -> entities.map { it.toDomain() } }
    
    suspend fun getNote(id: Int): Note? = noteDao.getById(id)?.toDomain()
    
    suspend fun saveNote(title: String, content: String, existingId: Int? = null): Long {
        val entity = NoteEntity(
            id = existingId ?: 0,
            title = title,
            content = content,
            updatedAt = System.currentTimeMillis()
        )
        return noteDao.insert(entity)
    }
    
    suspend fun deleteNote(noteId: Int) = noteDao.deleteById(noteId)
}

// ui/notes/NoteListViewModel.kt
class NoteListViewModel(
    private val repository: NoteRepository
) : ViewModel() {
    
    val notes: StateFlow<List<Note>> = repository.observeAllNotes()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    
    fun deleteNote(noteId: Int) {
        viewModelScope.launch {
            repository.deleteNote(noteId)
        }
    }
}

// ui/notes/NoteListScreen.kt
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NoteListScreen(
    viewModel: NoteListViewModel,
    onNoteClick: (Int) -> Unit,
    onCreateClick: () -> Unit
) {
    val notes by viewModel.notes.collectAsState()
    
    Scaffold(
        floatingActionButton = {
            FloatingActionButton(onClick = onCreateClick) {
                Icon(Icons.Default.Add, "Crear nota")
            }
        }
    ) { padding ->
        if (notes.isEmpty()) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Text("No hay notas")
            }
        } else {
            LazyColumn(modifier = Modifier.padding(padding)) {
                items(notes, key = { it.id }) { note ->
                    val dismissState = rememberSwipeToDismissBoxState(
                        confirmValueChange = {
                            if (it == SwipeToDismissBoxValue.EndToStart) {
                                viewModel.deleteNote(note.id)
                                true
                            } else false
                        }
                    )
                    
                    SwipeToDismissBox(
                        state = dismissState,
                        backgroundContent = {
                            Box(
                                Modifier.fillMaxSize().background(Color.Red).padding(16.dp),
                                contentAlignment = Alignment.CenterEnd
                            ) {
                                Icon(Icons.Default.Delete, null, tint = Color.White)
                            }
                        }
                    ) {
                        NoteItem(note = note, onClick = { onNoteClick(note.id) })
                    }
                }
            }
        }
    }
}

@Composable
fun NoteItem(note: Note, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
            .clickable(onClick = onClick)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(note.title, fontWeight = FontWeight.Bold)
            Text(
                note.content,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
                fontSize = 14.sp
            )
        }
    }
}
```

---

## Ejercicio 2: Filtros y búsqueda

```kotlin
// NoteDao.kt (añadir)
@Query("""
    SELECT * FROM notes 
    WHERE title LIKE '%' || :query || '%' 
    OR content LIKE '%' || :query || '%'
    ORDER BY updated_at DESC
""")
fun search(query: String): Flow<List<NoteEntity>>

@Query("SELECT * FROM notes ORDER BY created_at ASC")
fun getAllByCreatedAtAsc(): Flow<List<NoteEntity>>

@Query("SELECT * FROM notes ORDER BY created_at DESC")
fun getAllByCreatedAtDesc(): Flow<List<NoteEntity>>

@Query("SELECT * FROM notes ORDER BY title ASC")
fun getAllByTitleAsc(): Flow<List<NoteEntity>>

// ViewModel actualizado
enum class SortOrder { CREATED_ASC, CREATED_DESC, TITLE_ASC, UPDATED_DESC }

class NoteListViewModel(private val repository: NoteRepository) : ViewModel() {
    
    private val _searchQuery = MutableStateFlow("")
    private val _sortOrder = MutableStateFlow(SortOrder.UPDATED_DESC)
    
    val uiState: StateFlow<NoteListUiState> = combine(
        _searchQuery,
        _sortOrder,
        repository.observeAllNotes()
    ) { query, sort, allNotes ->
        val filtered = if (query.isBlank()) allNotes else {
            allNotes.filter { 
                it.title.contains(query, ignoreCase = true) ||
                it.content.contains(query, ignoreCase = true)
            }
        }
        
        val sorted = when (sort) {
            SortOrder.CREATED_ASC -> filtered.sortedBy { it.createdAt }
            SortOrder.CREATED_DESC -> filtered.sortedByDescending { it.createdAt }
            SortOrder.TITLE_ASC -> filtered.sortedBy { it.title.lowercase() }
            SortOrder.UPDATED_DESC -> filtered.sortedByDescending { it.updatedAt }
        }
        
        NoteListUiState(notes = sorted, query = query, sortOrder = sort)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), NoteListUiState())
    
    fun onSearchQueryChange(query: String) { _searchQuery.value = query }
    fun onSortOrderChange(order: SortOrder) { _sortOrder.value = order }
}

data class NoteListUiState(
    val notes: List<Note> = emptyList(),
    val query: String = "",
    val sortOrder: SortOrder = SortOrder.UPDATED_DESC
)
```

---

## Ejercicio 3: Categorías con relación

```kotlin
// CategoryEntity.kt
@Entity(tableName = "categories")
data class CategoryEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val name: String,
    val color: String = "#2196F3"
)

// NoteEntity.kt actualizado
@Entity(
    tableName = "notes",
    foreignKeys = [
        ForeignKey(
            entity = CategoryEntity::class,
            parentColumns = ["id"],
            childColumns = ["category_id"],
            onDelete = ForeignKey.SET_NULL
        )
    ],
    indices = [Index("category_id")]
)
data class NoteEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val title: String,
    val content: String,
    @ColumnInfo(name = "category_id")
    val categoryId: Int? = null,
    @ColumnInfo(name = "created_at")
    val createdAt: Long = System.currentTimeMillis(),
    @ColumnInfo(name = "updated_at")
    val updatedAt: Long = System.currentTimeMillis()
)

// NoteWithCategory.kt
data class NoteWithCategory(
    @Embedded
    val note: NoteEntity,
    
    @Relation(
        parentColumn = "category_id",
        entityColumn = "id"
    )
    val category: CategoryEntity?
)

// CategoryDao.kt
@Dao
interface CategoryDao {
    @Query("SELECT * FROM categories ORDER BY name")
    fun observeAll(): Flow<List<CategoryEntity>>
    
    @Insert
    suspend fun insert(category: CategoryEntity): Long
    
    @Delete
    suspend fun delete(category: CategoryEntity)
}

// NoteDao.kt (añadir)
@Transaction
@Query("SELECT * FROM notes ORDER BY updated_at DESC")
fun observeAllWithCategory(): Flow<List<NoteWithCategory>>

@Query("SELECT * FROM notes WHERE category_id = :categoryId")
fun observeByCategory(categoryId: Int): Flow<List<NoteEntity>>
```

---

## Ejercicio 4: Favoritos y contador

```kotlin
// NoteEntity.kt (añadir campo)
@ColumnInfo(name = "is_favorite")
val isFavorite: Boolean = false

// NoteDao.kt (añadir)
@Query("SELECT * FROM notes WHERE is_favorite = 1 ORDER BY updated_at DESC")
fun observeFavorites(): Flow<List<NoteEntity>>

@Query("UPDATE notes SET is_favorite = :isFavorite WHERE id = :noteId")
suspend fun setFavorite(noteId: Int, isFavorite: Boolean)

@Query("SELECT COUNT(*) FROM notes")
fun countAll(): Flow<Int>

@Query("SELECT COUNT(*) FROM notes WHERE is_favorite = 1")
fun countFavorites(): Flow<Int>

// ViewModel
class NoteListViewModel(private val repository: NoteRepository) : ViewModel() {
    
    private val _showFavoritesOnly = MutableStateFlow(false)
    
    val uiState: StateFlow<NoteListUiState> = combine(
        _showFavoritesOnly,
        repository.observeAllNotes(),
        repository.countAll(),
        repository.countFavorites()
    ) { favoritesOnly, notes, totalCount, favCount ->
        val filtered = if (favoritesOnly) notes.filter { it.isFavorite } else notes
        
        NoteListUiState(
            notes = filtered,
            showFavoritesOnly = favoritesOnly,
            totalCount = totalCount,
            favoritesCount = favCount
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), NoteListUiState())
    
    fun toggleFavorite(noteId: Int, currentState: Boolean) {
        viewModelScope.launch {
            repository.setFavorite(noteId, !currentState)
        }
    }
    
    fun toggleShowFavorites() {
        _showFavoritesOnly.value = !_showFavoritesOnly.value
    }
}

// UI
@Composable
fun NoteItem(note: Note, onClick: () -> Unit, onFavoriteClick: () -> Unit) {
    Card(modifier = Modifier.fillMaxWidth().padding(8.dp).clickable(onClick = onClick)) {
        Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Column(modifier = Modifier.weight(1f)) {
                Text(note.title, fontWeight = FontWeight.Bold)
                Text(note.content, maxLines = 2, overflow = TextOverflow.Ellipsis)
            }
            IconButton(onClick = onFavoriteClick) {
                Icon(
                    if (note.isFavorite) Icons.Default.Favorite else Icons.Default.FavoriteBorder,
                    contentDescription = "Favorito",
                    tint = if (note.isFavorite) Color.Red else Color.Gray
                )
            }
        }
    }
}
```

---

## Ejercicio 5: Migración

```kotlin
// AppDatabase.kt
@Database(entities = [NoteEntity::class], version = 2)
abstract class AppDatabase : RoomDatabase() {
    
    companion object {
        private val MIGRATION_1_2 = object : Migration(1, 2) {
            override fun migrate(database: SupportSQLiteDatabase) {
                database.execSQL(
                    "ALTER TABLE notes ADD COLUMN pinned INTEGER NOT NULL DEFAULT 0"
                )
            }
        }
        
        fun getInstance(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "notes_database"
                )
                .addMigrations(MIGRATION_1_2)
                .build()
                .also { INSTANCE = it }
            }
        }
    }
}

// NoteEntity.kt (añadir)
val pinned: Boolean = false

// NoteDao.kt (modificar query)
@Query("""
    SELECT * FROM notes 
    ORDER BY pinned DESC, updated_at DESC
""")
fun observeAll(): Flow<List<NoteEntity>>

@Query("UPDATE notes SET pinned = :pinned WHERE id = :noteId")
suspend fun setPinned(noteId: Int, pinned: Boolean)
```

---

## Ejercicio 6: Papelera

```kotlin
// NoteEntity.kt (añadir campos)
@ColumnInfo(name = "is_deleted")
val isDeleted: Boolean = false,

@ColumnInfo(name = "deleted_at")
val deletedAt: Long? = null

// NoteDao.kt
@Query("SELECT * FROM notes WHERE is_deleted = 0 ORDER BY updated_at DESC")
fun observeActive(): Flow<List<NoteEntity>>

@Query("SELECT * FROM notes WHERE is_deleted = 1 ORDER BY deleted_at DESC")
fun observeDeleted(): Flow<List<NoteEntity>>

@Query("UPDATE notes SET is_deleted = 1, deleted_at = :timestamp WHERE id = :noteId")
suspend fun softDelete(noteId: Int, timestamp: Long = System.currentTimeMillis())

@Query("UPDATE notes SET is_deleted = 0, deleted_at = NULL WHERE id = :noteId")
suspend fun restore(noteId: Int)

@Query("DELETE FROM notes WHERE id = :noteId")
suspend fun permanentDelete(noteId: Int)

@Query("DELETE FROM notes WHERE is_deleted = 1 AND deleted_at < :threshold")
suspend fun deleteOldTrash(threshold: Long)

// Repository
class NoteRepository(private val noteDao: NoteDao) {
    // Ejecutar limpieza de papelera
    suspend fun cleanOldTrash() {
        val thirtyDaysAgo = System.currentTimeMillis() - (30 * 24 * 60 * 60 * 1000L)
        noteDao.deleteOldTrash(thirtyDaysAgo)
    }
}

// TrashScreen.kt
@Composable
fun TrashScreen(viewModel: TrashViewModel) {
    val deletedNotes by viewModel.deletedNotes.collectAsState()
    
    LazyColumn {
        items(deletedNotes, key = { it.id }) { note ->
            Card(modifier = Modifier.fillMaxWidth().padding(8.dp)) {
                Row(modifier = Modifier.padding(16.dp)) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(note.title)
                        Text("Eliminado: ${formatDate(note.deletedAt)}", fontSize = 12.sp)
                    }
                    IconButton(onClick = { viewModel.restore(note.id) }) {
                        Icon(Icons.Default.Restore, "Restaurar")
                    }
                    IconButton(onClick = { viewModel.permanentDelete(note.id) }) {
                        Icon(Icons.Default.DeleteForever, "Eliminar permanentemente")
                    }
                }
            }
        }
    }
}
```
