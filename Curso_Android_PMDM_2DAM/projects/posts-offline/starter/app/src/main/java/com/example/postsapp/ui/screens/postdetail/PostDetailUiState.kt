package com.example.postsapp.ui.screens.postdetail

import com.example.postsapp.domain.model.Comment
import com.example.postsapp.domain.model.Post
import com.example.postsapp.domain.model.User

data class PostDetailUiState(
    val post: Post? = null,
    val author: User? = null,
    val comments: List<Comment> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)
