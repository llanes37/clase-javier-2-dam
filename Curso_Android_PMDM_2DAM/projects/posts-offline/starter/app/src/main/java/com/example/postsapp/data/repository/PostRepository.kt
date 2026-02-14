package com.example.postsapp.data.repository

import com.example.postsapp.data.local.dao.CommentDao
import com.example.postsapp.data.local.dao.PostDao
import com.example.postsapp.data.remote.ApiService
import com.example.postsapp.domain.model.Comment
import com.example.postsapp.domain.model.Post
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class PostRepository(
    private val postDao: PostDao,
    private val commentDao: CommentDao,
    private val apiService: ApiService
) {
    
    /**
     * Observe posts from local database (offline-first)
     */
    fun observePosts(): Flow<List<Post>> {
        return postDao.observeAll().map { entities ->
            entities.map { it.toDomain() }
        }
    }
    
    /**
     * Observe a single post by ID
     */
    fun observePost(postId: Int): Flow<Post?> {
        return postDao.observeById(postId).map { it?.toDomain() }
    }
    
    /**
     * Observe comments for a post
     */
    fun observeComments(postId: Int): Flow<List<Comment>> {
        return commentDao.observeByPostId(postId).map { entities ->
            entities.map { it.toDomain() }
        }
    }
    
    /**
     * Refresh posts from API and cache locally
     */
    suspend fun refreshPosts(): Result<Unit> {
        return try {
            val remotePosts = apiService.getPosts()
            postDao.deleteAll()
            postDao.insertAll(remotePosts.map { it.toEntity() })
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    /**
     * Refresh comments for a post
     */
    suspend fun refreshComments(postId: Int): Result<Unit> {
        return try {
            val remoteComments = apiService.getPostComments(postId)
            commentDao.deleteByPostId(postId)
            commentDao.insertAll(remoteComments.map { it.toEntity() })
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    /**
     * Get a single post, fetching from API if not cached
     */
    suspend fun getPost(postId: Int): Result<Post> {
        return try {
            // Try local first
            val localPost = postDao.getById(postId)
            if (localPost != null) {
                return Result.success(localPost.toDomain())
            }
            
            // Fetch from API
            val remotePost = apiService.getPost(postId)
            postDao.insert(remotePost.toEntity())
            Result.success(remotePost.toDomain())
        } catch (e: Exception) {
            // Return cached if available, otherwise fail
            val cachedPost = postDao.getById(postId)
            if (cachedPost != null) {
                Result.success(cachedPost.toDomain())
            } else {
                Result.failure(e)
            }
        }
    }
}
