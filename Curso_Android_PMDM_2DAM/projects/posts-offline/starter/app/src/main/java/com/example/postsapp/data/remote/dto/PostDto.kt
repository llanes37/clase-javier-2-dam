package com.example.postsapp.data.remote.dto

import com.example.postsapp.data.local.entity.PostEntity
import com.example.postsapp.domain.model.Post
import com.squareup.moshi.JsonClass

@JsonClass(generateAdapter = true)
data class PostDto(
    val id: Int,
    val userId: Int,
    val title: String,
    val body: String
) {
    fun toDomain(): Post = Post(
        id = id,
        userId = userId,
        title = title,
        body = body
    )
    
    fun toEntity(): PostEntity = PostEntity(
        id = id,
        userId = userId,
        title = title,
        body = body
    )
}
