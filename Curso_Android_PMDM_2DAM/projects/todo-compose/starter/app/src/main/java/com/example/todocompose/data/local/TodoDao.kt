package com.example.todocompose.data.local

import androidx.room.*
import com.example.todocompose.data.local.entity.TodoEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface TodoDao {
    
    @Query("SELECT * FROM todos ORDER BY isCompleted ASC, priority ASC, dueDate ASC")
    fun observeAll(): Flow<List<TodoEntity>>
    
    @Query("SELECT * FROM todos WHERE isCompleted = 0 ORDER BY priority ASC, dueDate ASC")
    fun observePending(): Flow<List<TodoEntity>>
    
    @Query("SELECT * FROM todos WHERE isCompleted = 1 ORDER BY priority ASC, dueDate ASC")
    fun observeCompleted(): Flow<List<TodoEntity>>
    
    @Query("SELECT * FROM todos WHERE id = :todoId")
    suspend fun getById(todoId: Int): TodoEntity?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(todo: TodoEntity): Long
    
    @Update
    suspend fun update(todo: TodoEntity)
    
    @Delete
    suspend fun delete(todo: TodoEntity)
    
    @Query("DELETE FROM todos WHERE id = :todoId")
    suspend fun deleteById(todoId: Int)
    
    @Query("UPDATE todos SET isCompleted = :isCompleted WHERE id = :todoId")
    suspend fun updateCompleted(todoId: Int, isCompleted: Boolean)
    
    @Query("DELETE FROM todos WHERE isCompleted = 1")
    suspend fun deleteCompleted()
}
