package com.example.todocompose.ui.navigation

import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.example.todocompose.TodoApplication
import com.example.todocompose.data.repository.TodoRepository
import com.example.todocompose.ui.screens.edit.EditScreen
import com.example.todocompose.ui.screens.edit.EditViewModel
import com.example.todocompose.ui.screens.home.HomeScreen
import com.example.todocompose.ui.screens.home.HomeViewModel

object Routes {
    const val HOME = "home"
    const val EDIT = "edit"
    const val EDIT_ARG = "todoId"
    const val EDIT_WITH_ARG = "edit?todoId={todoId}"
}

@Composable
fun TodoNavGraph() {
    val navController = rememberNavController()
    val context = LocalContext.current
    val application = context.applicationContext as TodoApplication
    val repository = TodoRepository(application.database.todoDao())
    
    NavHost(
        navController = navController,
        startDestination = Routes.HOME
    ) {
        composable(Routes.HOME) {
            val viewModel: HomeViewModel = viewModel {
                HomeViewModel(repository)
            }
            HomeScreen(
                viewModel = viewModel,
                onAddTodo = {
                    navController.navigate(Routes.EDIT)
                },
                onEditTodo = { todoId ->
                    navController.navigate("${Routes.EDIT}?todoId=$todoId")
                }
            )
        }
        
        composable(
            route = Routes.EDIT_WITH_ARG,
            arguments = listOf(
                navArgument(Routes.EDIT_ARG) {
                    type = NavType.IntType
                    defaultValue = -1
                }
            )
        ) { backStackEntry ->
            val todoId = backStackEntry.arguments?.getInt(Routes.EDIT_ARG) ?: -1
            val viewModel: EditViewModel = viewModel {
                EditViewModel(repository, if (todoId == -1) null else todoId)
            }
            EditScreen(
                viewModel = viewModel,
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }
    }
}
