package com.example.postsapp.ui.screens.userdetail

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.postsapp.data.repository.UserRepository
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class UserDetailViewModel(
    private val repository: UserRepository,
    private val userId: Int
) : ViewModel() {
    
    private val _uiState = MutableStateFlow(UserDetailUiState(isLoading = true))
    val uiState: StateFlow<UserDetailUiState> = _uiState.asStateFlow()
    
    init {
        observeUser()
        observePosts()
        loadData()
    }
    
    private fun observeUser() {
        viewModelScope.launch {
            repository.observeUser(userId).collect { user ->
                _uiState.update { it.copy(user = user, isLoading = false) }
            }
        }
    }
    
    private fun observePosts() {
        viewModelScope.launch {
            repository.observeUserPosts(userId).collect { posts ->
                _uiState.update { it.copy(posts = posts) }
            }
        }
    }
    
    private fun loadData() {
        viewModelScope.launch {
            repository.getUser(userId)
            repository.refreshUserPosts(userId)
        }
    }
}
