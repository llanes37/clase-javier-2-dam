package com.example.postsapp.data.repository

import com.example.postsapp.data.local.dao.PostDao
import com.example.postsapp.data.local.dao.UserDao
import com.example.postsapp.data.remote.ApiService
import com.example.postsapp.domain.model.Post
import com.example.postsapp.domain.model.User
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class UserRepository(
    private val userDao: UserDao,
    private val postDao: PostDao,
    private val apiService: ApiService
) {
    
    /**
     * Observe users from local database (offline-first)
     */
    fun observeUsers(): Flow<List<User>> {
        return userDao.observeAll().map { entities ->
            entities.map { it.toDomain() }
        }
    }
    
    /**
     * Observe a single user by ID
     */
    fun observeUser(userId: Int): Flow<User?> {
        return userDao.observeById(userId).map { it?.toDomain() }
    }
    
    /**
     * Observe posts by a user
     */
    fun observeUserPosts(userId: Int): Flow<List<Post>> {
        return postDao.observeByUserId(userId).map { entities ->
            entities.map { it.toDomain() }
        }
    }
    
    /**
     * Refresh users from API and cache locally
     */
    suspend fun refreshUsers(): Result<Unit> {
        return try {
            val remoteUsers = apiService.getUsers()
            userDao.deleteAll()
            userDao.insertAll(remoteUsers.map { it.toEntity() })
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    /**
     * Get a single user, fetching from API if not cached
     */
    suspend fun getUser(userId: Int): Result<User> {
        return try {
            // Try local first
            val localUser = userDao.getById(userId)
            if (localUser != null) {
                return Result.success(localUser.toDomain())
            }
            
            // Fetch from API
            val remoteUser = apiService.getUser(userId)
            userDao.insert(remoteUser.toEntity())
            Result.success(remoteUser.toDomain())
        } catch (e: Exception) {
            val cachedUser = userDao.getById(userId)
            if (cachedUser != null) {
                Result.success(cachedUser.toDomain())
            } else {
                Result.failure(e)
            }
        }
    }
    
    /**
     * Refresh posts for a specific user
     */
    suspend fun refreshUserPosts(userId: Int): Result<Unit> {
        return try {
            val remotePosts = apiService.getUserPosts(userId)
            postDao.insertAll(remotePosts.map { it.toEntity() })
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
