package com.example.todocompose.ui.screens.home

import com.example.todocompose.domain.model.Todo

data class HomeUiState(
    val todos: List<Todo> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val filter: TodoFilter = TodoFilter.ALL
)

enum class TodoFilter {
    ALL,
    PENDING,
    COMPLETED
}
