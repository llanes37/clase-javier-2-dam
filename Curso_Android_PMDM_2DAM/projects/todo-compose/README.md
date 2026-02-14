# Proyecto 1: Todo Compose

## 📱 Descripción

Aplicación de gestión de tareas (Todo List) desarrollada con Jetpack Compose, Material 3 y arquitectura MVVM.

**Valor:** 30% de la nota final

---

## 🎯 Objetivos de aprendizaje

- Implementar UI declarativa con Jetpack Compose
- Aplicar arquitectura MVVM correctamente
- Usar Room para persistencia local
- Manejar estados con StateFlow y UiState
- Navegación con Navigation Compose
- Diseño Material 3

---

## 📋 Requisitos funcionales

### RF1: Pantalla principal
- Lista de tareas con LazyColumn
- Mostrar título, fecha y estado (completado/pendiente)
- Checkbox para marcar como completado
- Swipe to delete
- FAB para añadir nueva tarea

### RF2: Crear/Editar tarea
- Campo de título (obligatorio)
- Campo de descripción (opcional)
- Selector de fecha límite (opcional)
- Selector de prioridad (alta/media/baja)
- Botón guardar/actualizar

### RF3: Filtros
- Ver todas las tareas
- Ver solo pendientes
- Ver solo completadas
- Ordenar por fecha o prioridad

### RF4: Persistencia
- Guardar tareas en Room
- Cargar al iniciar la app
- Sincronización automática

---

## 🏗️ Estructura del proyecto

```
app/src/main/java/com/example/todocompose/
├── MainActivity.kt
├── TodoApplication.kt
├── data/
│   ├── local/
│   │   ├── TodoDatabase.kt
│   │   ├── TodoDao.kt
│   │   └── entity/
│   │       └── TodoEntity.kt
│   └── repository/
│       └── TodoRepository.kt
├── domain/
│   └── model/
│       ├── Todo.kt
│       └── Priority.kt
├── ui/
│   ├── navigation/
│   │   └── NavGraph.kt
│   ├── screens/
│   │   ├── home/
│   │   │   ├── HomeScreen.kt
│   │   │   ├── HomeViewModel.kt
│   │   │   └── HomeUiState.kt
│   │   └── edit/
│   │       ├── EditScreen.kt
│   │       ├── EditViewModel.kt
│   │       └── EditUiState.kt
│   ├── components/
│   │   ├── TodoItem.kt
│   │   ├── PriorityDropdown.kt
│   │   └── DatePickerDialog.kt
│   └── theme/
│       ├── Theme.kt
│       ├── Color.kt
│       └── Type.kt
└── di/
    └── AppModule.kt (opcional, sin Hilt)
```

---

## 🚀 Cómo empezar

### 1. Clonar el starter
```bash
cd starter
```

### 2. Abrir en Android Studio

### 3. Sincronizar Gradle

### 4. Ejecutar en emulador

---

## ✅ Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| UI Compose correcta | 20% |
| MVVM bien implementado | 25% |
| Room funcionando | 20% |
| Navegación correcta | 15% |
| Código limpio y organizado | 10% |
| Tests (bonus) | 10% |

---

## 📅 Entrega

1. Fork del repositorio
2. Implementar funcionalidad
3. Crear Pull Request
4. El CI debe pasar (build + lint + test)
5. Fecha límite: según calendario

---

## 💡 Consejos

- Empieza por la estructura de datos (Entity, Model)
- Luego implementa el Repository
- Después los ViewModels
- Finalmente las pantallas
- Testea cada parte antes de continuar
