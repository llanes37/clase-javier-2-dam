# Ejercicios - Lección 09: Room Database

## Ejercicio 1: App de notas básica

### Instrucciones

Crea una app de notas con Room.

### Requisitos

**Entidad `NoteEntity`:**
- id (Int, autoGenerate)
- title (String)
- content (String)
- createdAt (Long)
- updatedAt (Long)

**DAO con operaciones:**
- Observar todas las notas
- Obtener nota por ID
- Insertar nota
- Actualizar nota
- Eliminar nota

**UI:**
- Lista de notas
- FAB para crear nueva
- Click para ver/editar
- Swipe para eliminar

### Criterios de aceptación

- [ ] Entidad configurada correctamente
- [ ] DAO con todas las operaciones
- [ ] Las notas persisten al cerrar la app
- [ ] UI funcional con CRUD completo

---

## Ejercicio 2: Filtros y búsqueda

### Instrucciones

Añade búsqueda y ordenación a la app de notas.

### Requisitos

- Barra de búsqueda que filtra por título o contenido
- Ordenar por: fecha creación, fecha modificación, título
- Chip para orden ascendente/descendente

### Queries necesarias

```kotlin
@Query("SELECT * FROM notes WHERE title LIKE '%' || :query || '%' OR content LIKE '%' || :query || '%'")
fun search(query: String): Flow<List<NoteEntity>>

@Query("SELECT * FROM notes ORDER BY CASE WHEN :ascending THEN created_at END ASC, CASE WHEN NOT :ascending THEN created_at END DESC")
fun getAllSorted(ascending: Boolean): Flow<List<NoteEntity>>
```

### Criterios de aceptación

- [ ] Búsqueda funciona en tiempo real
- [ ] Ordenación funciona
- [ ] Combinar búsqueda + ordenación

---

## Ejercicio 3: Categorías con relación

### Instrucciones

Añade categorías a las notas (relación 1:N).

### Requisitos

**Nueva entidad `CategoryEntity`:**
- id
- name
- color (String hex)

**Modificar `NoteEntity`:**
- Añadir categoryId (nullable)
- Configurar ForeignKey

**UI:**
- Selector de categoría al crear/editar nota
- Filtrar por categoría
- Mostrar color de categoría en la lista

### Criterios de aceptación

- [ ] ForeignKey configurada
- [ ] Relación funciona
- [ ] Filtro por categoría
- [ ] ON DELETE comportamiento correcto

---

## Ejercicio 4: Favoritos y contador

### Instrucciones

Añade sistema de favoritos con estadísticas.

### Requisitos

**Modificar `NoteEntity`:**
- Añadir campo `isFavorite` (Boolean)

**Nuevas queries:**
- Observar solo favoritos
- Contar total de notas
- Contar favoritos

**UI:**
- Icono de corazón para marcar favorito
- Mostrar contadores en header
- Tab o filtro para ver solo favoritos

### Criterios de aceptación

- [ ] Toggle favorito funciona
- [ ] Contadores se actualizan reactivamente
- [ ] Filtro de favoritos funciona

---

## Ejercicio 5: Migración de base de datos

### Instrucciones

Implementa una migración para añadir un campo nuevo.

### Requisitos

**Migración 1 → 2:**
- Añadir campo `pinned` (Boolean, default false)
- Las notas pinneadas aparecen primero

**Código de migración:**
```kotlin
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(database: SupportSQLiteDatabase) {
        // Tu código aquí
    }
}
```

### Criterios de aceptación

- [ ] Migración SQL correcta
- [ ] La app no pierde datos al actualizar
- [ ] El campo nuevo funciona
- [ ] Las notas existentes tienen pinned = false

---

## Ejercicio 6: Papelera de reciclaje

### Instrucciones

Implementa soft delete con papelera.

### Requisitos

**Modificar `NoteEntity`:**
- Añadir `isDeleted` (Boolean)
- Añadir `deletedAt` (Long?)

**Comportamiento:**
- "Eliminar" marca isDeleted = true
- Papelera muestra notas eliminadas
- "Restaurar" vuelve isDeleted = false
- "Eliminar permanentemente" borra de verdad
- Auto-eliminar notas en papelera > 30 días

### Criterios de aceptación

- [ ] Soft delete funciona
- [ ] Papelera muestra notas eliminadas
- [ ] Restaurar funciona
- [ ] Eliminar permanente funciona

---

## Ejercicio 7 (Bonus): Etiquetas Many-to-Many

### Instrucciones

Añade sistema de etiquetas (tags) a las notas.

### Requisitos

**Nueva entidad `TagEntity`:**
- id
- name

**Tabla intermedia `NoteTagCrossRef`:**
- noteId
- tagId

**Clase `NoteWithTags`:**
- Embedded note
- Relation tags

**UI:**
- Añadir múltiples tags a una nota
- Filtrar por tag
- Mostrar tags en la lista

### Criterios de aceptación

- [ ] Relación M:N configurada
- [ ] @Transaction para queries con relación
- [ ] Añadir/quitar tags funciona
- [ ] Filtrar por tag funciona

---

## Entrega

1. Estructura de carpetas:
   ```
   data/
     local/
       entity/
       dao/
       AppDatabase.kt
     repository/
   ui/
     notes/
   ```
2. Tests para DAO (al menos 3 tests)
3. Crea rama y PR
