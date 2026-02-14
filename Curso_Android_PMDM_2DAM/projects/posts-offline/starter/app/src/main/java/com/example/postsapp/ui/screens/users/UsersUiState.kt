package com.example.postsapp.ui.screens.users

import com.example.postsapp.domain.model.User

data class UsersUiState(
    val users: List<User> = emptyList(),
    val isLoading: Boolean = false,
    val isRefreshing: Boolean = false,
    val isOnline: Boolean = true,
    val error: String? = null
)
