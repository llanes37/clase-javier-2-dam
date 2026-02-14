package com.example.postsapp.ui.screens.users

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.postsapp.data.repository.UserRepository
import com.example.postsapp.util.ConnectivityObserver
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class UsersViewModel(
    private val repository: UserRepository,
    connectivityObserver: ConnectivityObserver
) : ViewModel() {
    
    private val _isRefreshing = MutableStateFlow(false)
    private val _error = MutableStateFlow<String?>(null)
    
    val uiState: StateFlow<UsersUiState> = combine(
        repository.observeUsers(),
        connectivityObserver.isOnline,
        _isRefreshing,
        _error
    ) { users, isOnline, isRefreshing, error ->
        UsersUiState(
            users = users,
            isLoading = users.isEmpty() && isRefreshing,
            isRefreshing = isRefreshing,
            isOnline = isOnline,
            error = error
        )
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = UsersUiState(isLoading = true)
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
                    _error.value = e.message ?: "Error al cargar usuarios"
                }
            
            _isRefreshing.value = false
        }
    }
    
    fun clearError() {
        _error.value = null
    }
}
