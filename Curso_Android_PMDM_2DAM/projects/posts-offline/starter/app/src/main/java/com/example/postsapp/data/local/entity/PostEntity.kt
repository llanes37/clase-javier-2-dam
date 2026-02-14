package com.example.postsapp.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.example.postsapp.domain.model.Post

@Entity(tableName = "posts")
data class PostEntity(
    @PrimaryKey
    val id: Int,
    val userId: Int,
    val title: String,
    val body: String,
    val cachedAt: Long = System.currentTimeMillis()
) {
    fun toDomain(): Post = Post(
        id = id,
        userId = userId,
        title = title,
        body = body
    )
    
    companion object {
        fun fromDomain(post: Post): PostEntity = PostEntity(
            id = post.id,
            userId = post.userId,
            title = post.title,
            body = post.body
        )
    }
}
