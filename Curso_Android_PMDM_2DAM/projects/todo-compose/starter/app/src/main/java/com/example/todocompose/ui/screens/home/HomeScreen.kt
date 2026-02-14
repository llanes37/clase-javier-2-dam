package com.example.todocompose.ui.screens.home

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.todocompose.domain.model.Priority
import com.example.todocompose.domain.model.Todo
import com.example.todocompose.ui.components.TodoItem
import com.example.todocompose.ui.theme.PriorityHigh
import com.example.todocompose.ui.theme.PriorityLow
import com.example.todocompose.ui.theme.PriorityMedium

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    viewModel: HomeViewModel,
    onAddTodo: () -> Unit,
    onEditTodo: (Int) -> Unit
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    var showMenu by remember { mutableStateOf(false) }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Mis Tareas") },
                actions = {
                    IconButton(onClick = { showMenu = true }) {
                        Icon(Icons.Default.MoreVert, contentDescription = "Menú")
                    }
                    DropdownMenu(
                        expanded = showMenu,
                        onDismissRequest = { showMenu = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("Eliminar completadas") },
                            onClick = {
                                viewModel.deleteCompletedTodos()
                                showMenu = false
                            }
                        )
                    }
                }
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = onAddTodo) {
                Icon(Icons.Default.Add, contentDescription = "Añadir tarea")
            }
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            // Filter tabs
            FilterTabs(
                currentFilter = uiState.filter,
                onFilterChange = viewModel::setFilter
            )
            
            // Content
            if (uiState.isLoading) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            } else if (uiState.todos.isEmpty()) {
                EmptyState(filter = uiState.filter)
            } else {
                TodoList(
                    todos = uiState.todos,
                    onTodoClick = onEditTodo,
                    onToggleCompleted = viewModel::toggleTodoCompleted,
                    onDelete = viewModel::deleteTodo
                )
            }
        }
    }
}

@Composable
private fun FilterTabs(
    currentFilter: TodoFilter,
    onFilterChange: (TodoFilter) -> Unit
) {
    TabRow(
        selectedTabIndex = currentFilter.ordinal
    ) {
        TodoFilter.entries.forEach { filter ->
            Tab(
                selected = currentFilter == filter,
                onClick = { onFilterChange(filter) },
                text = {
                    Text(
                        when (filter) {
                            TodoFilter.ALL -> "Todas"
                            TodoFilter.PENDING -> "Pendientes"
                            TodoFilter.COMPLETED -> "Completadas"
                        }
                    )
                }
            )
        }
    }
}

@Composable
private fun EmptyState(filter: TodoFilter) {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = when (filter) {
                TodoFilter.ALL -> "No hay tareas.\n¡Añade una nueva!"
                TodoFilter.PENDING -> "No hay tareas pendientes.\n¡Buen trabajo!"
                TodoFilter.COMPLETED -> "No hay tareas completadas."
            },
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun TodoList(
    todos: List<Todo>,
    onTodoClick: (Int) -> Unit,
    onToggleCompleted: (Int, Boolean) -> Unit,
    onDelete: (Int) -> Unit
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(vertical = 8.dp)
    ) {
        items(
            items = todos,
            key = { it.id }
        ) { todo ->
            val dismissState = rememberSwipeToDismissBoxState(
                confirmValueChange = { dismissValue ->
                    if (dismissValue == SwipeToDismissBoxValue.EndToStart) {
                        onDelete(todo.id)
                        true
                    } else {
                        false
                    }
                }
            )
            
            SwipeToDismissBox(
                state = dismissState,
                backgroundContent = {
                    val color by animateColorAsState(
                        when (dismissState.targetValue) {
                            SwipeToDismissBoxValue.EndToStart -> MaterialTheme.colorScheme.error
                            else -> Color.Transparent
                        },
                        label = "swipe_color"
                    )
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .background(color)
                            .padding(horizontal = 20.dp),
                        contentAlignment = Alignment.CenterEnd
                    ) {
                        Icon(
                            Icons.Default.Delete,
                            contentDescription = "Eliminar",
                            tint = Color.White
                        )
                    }
                },
                enableDismissFromStartToEnd = false
            ) {
                TodoItem(
                    todo = todo,
                    onClick = { onTodoClick(todo.id) },
                    onCheckedChange = { onToggleCompleted(todo.id, it) }
                )
            }
        }
    }
}
