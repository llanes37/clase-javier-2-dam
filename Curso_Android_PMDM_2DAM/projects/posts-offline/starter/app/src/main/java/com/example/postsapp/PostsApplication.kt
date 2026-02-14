package com.example.postsapp

import android.app.Application
import com.example.postsapp.data.local.AppDatabase
import com.example.postsapp.data.remote.RetrofitClient

class PostsApplication : Application() {
    
    val database: AppDatabase by lazy {
        AppDatabase.getDatabase(this)
    }
    
    val apiService by lazy {
        RetrofitClient.apiService
    }
}
