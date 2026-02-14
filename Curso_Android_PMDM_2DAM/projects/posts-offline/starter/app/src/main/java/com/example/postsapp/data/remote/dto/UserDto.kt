package com.example.postsapp.data.remote.dto

import com.example.postsapp.data.local.entity.UserEntity
import com.example.postsapp.domain.model.User
import com.squareup.moshi.JsonClass

@JsonClass(generateAdapter = true)
data class UserDto(
    val id: Int,
    val name: String,
    val username: String,
    val email: String,
    val phone: String,
    val website: String
) {
    fun toDomain(): User = User(
        id = id,
        name = name,
        username = username,
        email = email,
        phone = phone,
        website = website
    )
    
    fun toEntity(): UserEntity = UserEntity(
        id = id,
        name = name,
        username = username,
        email = email,
        phone = phone,
        website = website
    )
}
