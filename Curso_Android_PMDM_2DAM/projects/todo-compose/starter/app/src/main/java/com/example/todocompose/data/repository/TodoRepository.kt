package com.example.todocompose.data.repository

import com.example.todocompose.data.local.TodoDao
import com.example.todocompose.data.local.entity.TodoEntity
import com.example.todocompose.domain.model.Todo
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class TodoRepository(private val todoDao: TodoDao) {
    
    fun observeAllTodos(): Flow<List<Todo>> {
        return todoDao.observeAll().map { entities ->
            entities.map { it.toDomain() }
        }
    }
    
    fun observePendingTodos(): Flow<List<Todo>> {
        return todoDao.observePending().map { entities ->
            entities.map { it.toDomain() }
        }
    }
    
    fun observeCompletedTodos(): Flow<List<Todo>> {
        return todoDao.observeCompleted().map { entities ->
            entities.map { it.toDomain() }
        }
    }
    
    suspend fun getTodoById(id: Int): Todo? {
        return todoDao.getById(id)?.toDomain()
    }
    
    suspend fun addTodo(todo: Todo): Long {
        return todoDao.insert(TodoEntity.fromDomain(todo))
    }
    
    suspend fun updateTodo(todo: Todo) {
        todoDao.update(TodoEntity.fromDomain(todo))
    }
    
    suspend fun deleteTodo(todo: Todo) {
        todoDao.delete(TodoEntity.fromDomain(todo))
    }
    
    suspend fun deleteTodoById(id: Int) {
        todoDao.deleteById(id)
    }
    
    suspend fun toggleTodoCompleted(id: Int, isCompleted: Boolean) {
        todoDao.updateCompleted(id, isCompleted)
    }
    
    suspend fun deleteCompletedTodos() {
        todoDao.deleteCompleted()
    }
}
