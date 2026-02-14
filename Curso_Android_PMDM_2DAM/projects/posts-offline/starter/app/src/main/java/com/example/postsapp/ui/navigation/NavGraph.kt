package com.example.postsapp.ui.navigation

import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.example.postsapp.PostsApplication
import com.example.postsapp.data.repository.PostRepository
import com.example.postsapp.data.repository.UserRepository
import com.example.postsapp.ui.screens.postdetail.PostDetailScreen
import com.example.postsapp.ui.screens.postdetail.PostDetailViewModel
import com.example.postsapp.ui.screens.posts.PostsScreen
import com.example.postsapp.ui.screens.posts.PostsViewModel
import com.example.postsapp.ui.screens.userdetail.UserDetailScreen
import com.example.postsapp.ui.screens.userdetail.UserDetailViewModel
import com.example.postsapp.ui.screens.users.UsersScreen
import com.example.postsapp.ui.screens.users.UsersViewModel
import com.example.postsapp.util.ConnectivityObserver

object Routes {
    const val POSTS = "posts"
    const val POST_DETAIL = "post/{postId}"
    const val USERS = "users"
    const val USER_DETAIL = "user/{userId}"
}

@Composable
fun PostsNavGraph() {
    val navController = rememberNavController()
    val context = LocalContext.current
    val application = context.applicationContext as PostsApplication
    
    val postRepository = PostRepository(
        postDao = application.database.postDao(),
        commentDao = application.database.commentDao(),
        apiService = application.apiService
    )
    
    val userRepository = UserRepository(
        userDao = application.database.userDao(),
        postDao = application.database.postDao(),
        apiService = application.apiService
    )
    
    val connectivityObserver = ConnectivityObserver(context)
    
    NavHost(
        navController = navController,
        startDestination = Routes.POSTS
    ) {
        composable(Routes.POSTS) {
            val viewModel: PostsViewModel = viewModel {
                PostsViewModel(postRepository, connectivityObserver)
            }
            PostsScreen(
                viewModel = viewModel,
                onPostClick = { postId ->
                    navController.navigate("post/$postId")
                },
                onNavigateToUsers = {
                    navController.navigate(Routes.USERS)
                }
            )
        }
        
        composable(
            route = Routes.POST_DETAIL,
            arguments = listOf(navArgument("postId") { type = NavType.IntType })
        ) { backStackEntry ->
            val postId = backStackEntry.arguments?.getInt("postId") ?: return@composable
            val viewModel: PostDetailViewModel = viewModel {
                PostDetailViewModel(postRepository, userRepository, postId)
            }
            PostDetailScreen(
                viewModel = viewModel,
                onNavigateBack = { navController.popBackStack() },
                onUserClick = { userId ->
                    navController.navigate("user/$userId")
                }
            )
        }
        
        composable(Routes.USERS) {
            val viewModel: UsersViewModel = viewModel {
                UsersViewModel(userRepository, connectivityObserver)
            }
            UsersScreen(
                viewModel = viewModel,
                onUserClick = { userId ->
                    navController.navigate("user/$userId")
                },
                onNavigateBack = { navController.popBackStack() }
            )
        }
        
        composable(
            route = Routes.USER_DETAIL,
            arguments = listOf(navArgument("userId") { type = NavType.IntType })
        ) { backStackEntry ->
            val userId = backStackEntry.arguments?.getInt("userId") ?: return@composable
            val viewModel: UserDetailViewModel = viewModel {
                UserDetailViewModel(userRepository, userId)
            }
            UserDetailScreen(
                viewModel = viewModel,
                onNavigateBack = { navController.popBackStack() },
                onPostClick = { postId ->
                    navController.navigate("post/$postId")
                }
            )
        }
    }
}
