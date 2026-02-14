package com.example.postsapp.data.remote

import com.example.postsapp.data.remote.dto.CommentDto
import com.example.postsapp.data.remote.dto.PostDto
import com.example.postsapp.data.remote.dto.UserDto
import retrofit2.http.GET
import retrofit2.http.Path

interface ApiService {
    
    @GET("posts")
    suspend fun getPosts(): List<PostDto>
    
    @GET("posts/{id}")
    suspend fun getPost(@Path("id") postId: Int): PostDto
    
    @GET("posts/{id}/comments")
    suspend fun getPostComments(@Path("id") postId: Int): List<CommentDto>
    
    @GET("users")
    suspend fun getUsers(): List<UserDto>
    
    @GET("users/{id}")
    suspend fun getUser(@Path("id") userId: Int): UserDto
    
    @GET("users/{id}/posts")
    suspend fun getUserPosts(@Path("id") userId: Int): List<PostDto>
}
