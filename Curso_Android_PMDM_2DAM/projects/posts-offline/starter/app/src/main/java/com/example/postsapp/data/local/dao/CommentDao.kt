package com.example.postsapp.data.local.dao

import androidx.room.*
import com.example.postsapp.data.local.entity.CommentEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface CommentDao {
    
    @Query("SELECT * FROM comments WHERE postId = :postId ORDER BY id ASC")
    fun observeByPostId(postId: Int): Flow<List<CommentEntity>>
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(comments: List<CommentEntity>)
    
    @Query("DELETE FROM comments WHERE postId = :postId")
    suspend fun deleteByPostId(postId: Int)
}
