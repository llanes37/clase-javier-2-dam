package com.example.todocompose.ui.screens.edit

import com.example.todocompose.domain.model.Priority
import java.time.LocalDate

data class EditUiState(
    val todoId: Int? = null,
    val title: String = "",
    val description: String = "",
    val priority: Priority = Priority.MEDIUM,
    val dueDate: LocalDate? = null,
    val isLoading: Boolean = false,
    val isSaved: Boolean = false,
    val error: String? = null
) {
    val isEditing: Boolean get() = todoId != null
    val isValid: Boolean get() = title.isNotBlank()
}
