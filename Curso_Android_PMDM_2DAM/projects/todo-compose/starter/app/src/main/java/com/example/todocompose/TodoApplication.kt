package com.example.todocompose

import android.app.Application
import com.example.todocompose.data.local.TodoDatabase

class TodoApplication : Application() {
    
    // Lazy initialization of database
    val database: TodoDatabase by lazy {
        TodoDatabase.getDatabase(this)
    }
}
