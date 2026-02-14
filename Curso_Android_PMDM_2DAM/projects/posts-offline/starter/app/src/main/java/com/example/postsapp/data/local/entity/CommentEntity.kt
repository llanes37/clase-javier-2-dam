package com.example.postsapp.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.example.postsapp.domain.model.Comment

@Entity(tableName = "comments")
data class CommentEntity(
    @PrimaryKey
    val id: Int,
    val postId: Int,
    val name: String,
    val email: String,
    val body: String,
    val cachedAt: Long = System.currentTimeMillis()
) {
    fun toDomain(): Comment = Comment(
        id = id,
        postId = postId,
        name = name,
        email = email,
        body = body
    )
    
    companion object {
        fun fromDomain(comment: Comment): CommentEntity = CommentEntity(
            id = comment.id,
            postId = comment.postId,
            name = comment.name,
            email = comment.email,
            body = comment.body
        )
    }
}
