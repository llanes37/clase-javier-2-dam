package com.example.todocompose.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.todocompose.data.repository.TodoRepository
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class HomeViewModel(
    private val repository: TodoRepository
) : ViewModel() {
    
    private val _filter = MutableStateFlow(TodoFilter.ALL)
    
    val uiState: StateFlow<HomeUiState> = _filter.flatMapLatest { filter ->
        when (filter) {
            TodoFilter.ALL -> repository.observeAllTodos()
            TodoFilter.PENDING -> repository.observePendingTodos()
            TodoFilter.COMPLETED -> repository.observeCompletedTodos()
        }.map { todos ->
            HomeUiState(todos = todos, filter = filter)
        }
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = HomeUiState(isLoading = true)
    )
    
    fun setFilter(filter: TodoFilter) {
        _filter.value = filter
    }
    
    fun toggleTodoCompleted(todoId: Int, isCompleted: Boolean) {
        viewModelScope.launch {
            repository.toggleTodoCompleted(todoId, isCompleted)
        }
    }
    
    fun deleteTodo(todoId: Int) {
        viewModelScope.launch {
            repository.deleteTodoById(todoId)
        }
    }
    
    fun deleteCompletedTodos() {
        viewModelScope.launch {
            repository.deleteCompletedTodos()
        }
    }
}
