# Proyecto 2: App API + Offline First

## 📱 Descripción

Aplicación que consume la API JSONPlaceholder con arquitectura offline-first. Los datos se cachean en Room y se sincronizan con la API.

**Valor:** 40% de la nota final

---

## 🎯 Objetivos de aprendizaje

- Consumir API REST con Retrofit
- Implementar patrón offline-first
- Sincronizar datos locales con remotos
- Manejar estados de conectividad
- UI reactiva con StateFlow

---

## 📋 Requisitos funcionales

### RF1: Listado de Posts
- Lista de posts desde JSONPlaceholder
- Mostrar título y extracto del body
- Pull-to-refresh para actualizar
- Indicador de conectividad

### RF2: Detalle de Post
- Ver post completo
- Ver autor (User)
- Ver comentarios del post

### RF3: Usuarios
- Lista de usuarios
- Detalle con info completa
- Ver posts del usuario

### RF4: Offline-first
- Cachear datos en Room
- Funcionar sin conexión
- Sincronizar al recuperar conexión
- Mostrar estado de datos (sincronizado/offline)

### RF5: Crear Post (Bonus)
- Formulario para crear post
- Guardar localmente si no hay conexión
- Sincronizar cuando haya conexión

---

## 🌐 API: JSONPlaceholder

Base URL: `https://jsonplaceholder.typicode.com`

### Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/posts` | GET | Lista de posts |
| `/posts/{id}` | GET | Post por ID |
| `/posts/{id}/comments` | GET | Comentarios de un post |
| `/users` | GET | Lista de usuarios |
| `/users/{id}` | GET | Usuario por ID |
| `/users/{id}/posts` | GET | Posts de un usuario |

### Modelos de respuesta

```kotlin
// Post
{
  "userId": 1,
  "id": 1,
  "title": "...",
  "body": "..."
}

// User
{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz",
  "address": { ... },
  "phone": "1-770-736-8031 x56442",
  "website": "hildegard.org",
  "company": { ... }
}

// Comment
{
  "postId": 1,
  "id": 1,
  "name": "...",
  "email": "...",
  "body": "..."
}
```

---

## 🏗️ Estructura del proyecto

```
app/src/main/java/com/example/postsapp/
├── MainActivity.kt
├── PostsApplication.kt
├── data/
│   ├── local/
│   │   ├── AppDatabase.kt
│   │   ├── dao/
│   │   │   ├── PostDao.kt
│   │   │   ├── UserDao.kt
│   │   │   └── CommentDao.kt
│   │   └── entity/
│   │       ├── PostEntity.kt
│   │       ├── UserEntity.kt
│   │       └── CommentEntity.kt
│   ├── remote/
│   │   ├── ApiService.kt
│   │   ├── RetrofitClient.kt
│   │   └── dto/
│   │       ├── PostDto.kt
│   │       ├── UserDto.kt
│   │       └── CommentDto.kt
│   └── repository/
│       ├── PostRepository.kt
│       └── UserRepository.kt
├── domain/
│   └── model/
│       ├── Post.kt
│       ├── User.kt
│       └── Comment.kt
├── ui/
│   ├── navigation/
│   │   └── NavGraph.kt
│   ├── screens/
│   │   ├── posts/
│   │   ├── postdetail/
│   │   ├── users/
│   │   └── userdetail/
│   ├── components/
│   └── theme/
└── util/
    └── ConnectivityObserver.kt
```

---

## 🚀 Cómo empezar

### 1. Abrir el proyecto starter

### 2. Completar:
   - DTOs y mappers
   - ApiService con Retrofit
   - Entities de Room
   - DAOs
   - Repositories con offline-first
   - ViewModels
   - Pantallas

---

## ✅ Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| API Retrofit correcta | 20% |
| Room implementado | 20% |
| Offline-first funcionando | 25% |
| UI Compose | 15% |
| Manejo de errores | 10% |
| Tests (bonus) | 10% |

---

## 📅 Entrega

1. Fork del repositorio
2. Implementar funcionalidad
3. Crear Pull Request
4. El CI debe pasar
5. Demo funcional sin conexión

---

## 💡 Consejos

- Empieza por la capa de datos (API + Room)
- Implementa un repository a la vez
- Testea el offline desconectando wifi/datos
- Usa NetworkBoundResource pattern
