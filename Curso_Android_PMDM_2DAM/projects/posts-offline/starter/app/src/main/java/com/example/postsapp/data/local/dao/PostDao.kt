package com.example.postsapp.data.local.dao

import androidx.room.*
import com.example.postsapp.data.local.entity.PostEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface PostDao {
    
    @Query("SELECT * FROM posts ORDER BY id ASC")
    fun observeAll(): Flow<List<PostEntity>>
    
    @Query("SELECT * FROM posts WHERE id = :postId")
    fun observeById(postId: Int): Flow<PostEntity?>
    
    @Query("SELECT * FROM posts WHERE userId = :userId ORDER BY id ASC")
    fun observeByUserId(userId: Int): Flow<List<PostEntity>>
    
    @Query("SELECT * FROM posts WHERE id = :postId")
    suspend fun getById(postId: Int): PostEntity?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(posts: List<PostEntity>)
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(post: PostEntity)
    
    @Query("DELETE FROM posts")
    suspend fun deleteAll()
    
    @Query("DELETE FROM posts WHERE id = :postId")
    suspend fun deleteById(postId: Int)
}
