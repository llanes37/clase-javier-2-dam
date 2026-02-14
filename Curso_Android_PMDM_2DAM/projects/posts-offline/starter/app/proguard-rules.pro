# ProGuard rules for Posts App

# Room
-keep class * extends androidx.room.RoomDatabase
-keep @androidx.room.Entity class *

# Models
-keep class com.example.postsapp.data.local.entity.** { *; }
-keep class com.example.postsapp.data.remote.dto.** { *; }
-keep class com.example.postsapp.domain.model.** { *; }

# Retrofit
-keepattributes Signature
-keepattributes Exceptions
-keep class retrofit2.** { *; }
-keepclasseswithmembers class * {
    @retrofit2.http.* <methods>;
}

# Moshi
-keep class com.squareup.moshi.** { *; }
-keepclassmembers class * {
    @com.squareup.moshi.FromJson <methods>;
    @com.squareup.moshi.ToJson <methods>;
}
-keep @com.squareup.moshi.JsonClass class * { *; }

# OkHttp
-dontwarn okhttp3.**
-dontwarn okio.**
