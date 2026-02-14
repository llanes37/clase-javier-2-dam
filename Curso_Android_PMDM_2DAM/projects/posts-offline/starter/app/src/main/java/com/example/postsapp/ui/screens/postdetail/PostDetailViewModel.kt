package com.example.postsapp.ui.screens.postdetail

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.postsapp.data.repository.PostRepository
import com.example.postsapp.data.repository.UserRepository
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class PostDetailViewModel(
    private val postRepository: PostRepository,
    private val userRepository: UserRepository,
    private val postId: Int
) : ViewModel() {
    
    private val _uiState = MutableStateFlow(PostDetailUiState(isLoading = true))
    val uiState: StateFlow<PostDetailUiState> = _uiState.asStateFlow()
    
    init {
        loadPost()
        observeComments()
    }
    
    private fun loadPost() {
        viewModelScope.launch {
            postRepository.observePost(postId).collect { post ->
                _uiState.update { it.copy(post = post, isLoading = false) }
                
                post?.let {
                    loadAuthor(it.userId)
                }
            }
        }
        
        // Also try to refresh from API
        viewModelScope.launch {
            postRepository.getPost(postId)
            postRepository.refreshComments(postId)
        }
    }
    
    private fun loadAuthor(userId: Int) {
        viewModelScope.launch {
            userRepository.getUser(userId)
                .onSuccess { user ->
                    _uiState.update { it.copy(author = user) }
                }
        }
    }
    
    private fun observeComments() {
        viewModelScope.launch {
            postRepository.observeComments(postId).collect { comments ->
                _uiState.update { it.copy(comments = comments) }
            }
        }
    }
}
