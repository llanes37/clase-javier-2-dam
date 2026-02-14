package com.example.todocompose.domain.model

import java.time.LocalDate

data class Todo(
    val id: Int = 0,
    val title: String,
    val description: String = "",
    val isCompleted: Boolean = false,
    val priority: Priority = Priority.MEDIUM,
    val dueDate: LocalDate? = null,
    val createdAt: LocalDate = LocalDate.now()
)
