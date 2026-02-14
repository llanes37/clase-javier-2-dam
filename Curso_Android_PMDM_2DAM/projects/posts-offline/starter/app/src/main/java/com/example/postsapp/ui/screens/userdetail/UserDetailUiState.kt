package com.example.postsapp.ui.screens.userdetail

import com.example.postsapp.domain.model.Post
import com.example.postsapp.domain.model.User

data class UserDetailUiState(
    val user: User? = null,
    val posts: List<Post> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)
