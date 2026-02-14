package com.example.postsapp.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.example.postsapp.domain.model.User

@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey
    val id: Int,
    val name: String,
    val username: String,
    val email: String,
    val phone: String,
    val website: String,
    val cachedAt: Long = System.currentTimeMillis()
) {
    fun toDomain(): User = User(
        id = id,
        name = name,
        username = username,
        email = email,
        phone = phone,
        website = website
    )
    
    companion object {
        fun fromDomain(user: User): UserEntity = UserEntity(
            id = user.id,
            name = user.name,
            username = user.username,
            email = user.email,
            phone = user.phone,
            website = user.website
        )
    }
}
