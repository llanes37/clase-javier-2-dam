package com.example.postsapp.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.example.postsapp.data.local.dao.CommentDao
import com.example.postsapp.data.local.dao.PostDao
import com.example.postsapp.data.local.dao.UserDao
import com.example.postsapp.data.local.entity.CommentEntity
import com.example.postsapp.data.local.entity.PostEntity
import com.example.postsapp.data.local.entity.UserEntity

@Database(
    entities = [
        PostEntity::class,
        UserEntity::class,
        CommentEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    
    abstract fun postDao(): PostDao
    abstract fun userDao(): UserDao
    abstract fun commentDao(): CommentDao
    
    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null
        
        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "posts_database"
                )
                .fallbackToDestructiveMigration()
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
