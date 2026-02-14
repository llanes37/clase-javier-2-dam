package com.example.postsapp.ui.screens.posts

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.postsapp.data.repository.PostRepository
import com.example.postsapp.util.ConnectivityObserver
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class PostsViewModel(
    private val repository: PostRepository,
    connectivityObserver: ConnectivityObserver
) : ViewModel() {
    
    private val _isRefreshing = MutableStateFlow(false)
    private val _error = MutableStateFlow<String?>(null)
    
    val uiState: StateFlow<PostsUiState> = combine(
        repository.observePosts(),
        connectivityObserver.isOnline,
        _isRefreshing,
        _error
    ) { posts, isOnline, isRefreshing, error ->
        PostsUiState(
            posts = posts,
            isLoading = posts.isEmpty() && isRefreshing,
            isRefreshing = isRefreshing,
            isOnline = isOnline,
            error = error
        )
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = PostsUiState(isLoading = true)
    )
    
    init {
        refresh()
    }
    
    fun refresh() {
        viewModelScope.launch {
            _isRefreshing.value = true
            _error.value = null
            
            repository.refreshPosts()
                .onFailure { e ->
                    _error.value = e.message ?: "Error al cargar posts"
                }
            
            _isRefreshing.value = false
        }
    }
    
    fun clearError() {
        _error.value = null
    }
}
