package com.example.todocompose.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.example.todocompose.domain.model.Priority
import com.example.todocompose.domain.model.Todo
import java.time.LocalDate

@Entity(tableName = "todos")
data class TodoEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val title: String,
    val description: String = "",
    val isCompleted: Boolean = false,
    val priority: Int = Priority.MEDIUM.ordinal,
    val dueDate: Long? = null,
    val createdAt: Long = System.currentTimeMillis()
) {
    fun toDomain(): Todo = Todo(
        id = id,
        title = title,
        description = description,
        isCompleted = isCompleted,
        priority = Priority.fromOrdinal(priority),
        dueDate = dueDate?.let { LocalDate.ofEpochDay(it) },
        createdAt = LocalDate.ofEpochDay(createdAt / (24 * 60 * 60 * 1000))
    )
    
    companion object {
        fun fromDomain(todo: Todo): TodoEntity = TodoEntity(
            id = todo.id,
            title = todo.title,
            description = todo.description,
            isCompleted = todo.isCompleted,
            priority = todo.priority.ordinal,
            dueDate = todo.dueDate?.toEpochDay(),
            createdAt = todo.createdAt.toEpochDay() * 24 * 60 * 60 * 1000
        )
    }
}
