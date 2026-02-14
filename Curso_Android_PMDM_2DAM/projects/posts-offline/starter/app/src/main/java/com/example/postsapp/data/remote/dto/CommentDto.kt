package com.example.postsapp.data.remote.dto

import com.example.postsapp.data.local.entity.CommentEntity
import com.example.postsapp.domain.model.Comment
import com.squareup.moshi.JsonClass

@JsonClass(generateAdapter = true)
data class CommentDto(
    val id: Int,
    val postId: Int,
    val name: String,
    val email: String,
    val body: String
) {
    fun toDomain(): Comment = Comment(
        id = id,
        postId = postId,
        name = name,
        email = email,
        body = body
    )
    
    fun toEntity(): CommentEntity = CommentEntity(
        id = id,
        postId = postId,
        name = name,
        email = email,
        body = body
    )
}
