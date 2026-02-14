package com.example.todocompose.ui.screens.edit

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.todocompose.data.repository.TodoRepository
import com.example.todocompose.domain.model.Priority
import com.example.todocompose.domain.model.Todo
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.time.LocalDate

class EditViewModel(
    private val repository: TodoRepository,
    private val todoId: Int?
) : ViewModel() {
    
    private val _uiState = MutableStateFlow(EditUiState(todoId = todoId))
    val uiState: StateFlow<EditUiState> = _uiState.asStateFlow()
    
    init {
        if (todoId != null) {
            loadTodo(todoId)
        }
    }
    
    private fun loadTodo(id: Int) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            try {
                val todo = repository.getTodoById(id)
                if (todo != null) {
                    _uiState.update {
                        it.copy(
                            title = todo.title,
                            description = todo.description,
                            priority = todo.priority,
                            dueDate = todo.dueDate,
                            isLoading = false
                        )
                    }
                } else {
                    _uiState.update { it.copy(error = "Tarea no encontrada", isLoading = false) }
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }
    
    fun updateTitle(title: String) {
        _uiState.update { it.copy(title = title) }
    }
    
    fun updateDescription(description: String) {
        _uiState.update { it.copy(description = description) }
    }
    
    fun updatePriority(priority: Priority) {
        _uiState.update { it.copy(priority = priority) }
    }
    
    fun updateDueDate(date: LocalDate?) {
        _uiState.update { it.copy(dueDate = date) }
    }
    
    fun save() {
        val state = _uiState.value
        if (!state.isValid) return
        
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            try {
                val todo = Todo(
                    id = state.todoId ?: 0,
                    title = state.title.trim(),
                    description = state.description.trim(),
                    priority = state.priority,
                    dueDate = state.dueDate
                )
                
                if (state.isEditing) {
                    repository.updateTodo(todo)
                } else {
                    repository.addTodo(todo)
                }
                
                _uiState.update { it.copy(isSaved = true, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }
    
    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }
}
