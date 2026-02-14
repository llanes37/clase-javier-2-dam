# Ejercicios - Lección 07: APIs con Retrofit

## Ejercicio 1: Lista de usuarios

### Instrucciones

Crea una app que muestre usuarios de JSONPlaceholder API.

**Endpoint:** `https://jsonplaceholder.typicode.com/users`

### Requisitos

- Modelo `User` con: id, name, email, phone, website
- Interface de Retrofit con método `getUsers()`
- Repository con manejo de errores
- ViewModel con UiState (loading, success, error)
- UI con lista y estados

### Criterios de aceptación

- [ ] La lista se carga al iniciar
- [ ] Muestra loading mientras carga
- [ ] Muestra error con botón retry si falla
- [ ] Cada usuario muestra name y email

---

## Ejercicio 2: Detalle de usuario

### Instrucciones

Añade pantalla de detalle con los posts del usuario.

**Endpoints:**
- Usuario: `GET /users/{id}`
- Posts: `GET /posts?userId={userId}`

### Requisitos

- Navegar desde lista a detalle pasando userId
- Mostrar info del usuario arriba
- Lista de posts debajo
- Modelo `Post` con: id, userId, title, body

### Criterios de aceptación

- [ ] Navegación funciona
- [ ] Muestra datos del usuario
- [ ] Lista posts del usuario
- [ ] Maneja errores

---

## Ejercicio 3: Crear post

### Instrucciones

Añade formulario para crear un nuevo post.

**Endpoint:** `POST /posts`

```json
{
  "title": "string",
  "body": "string",
  "userId": 1
}
```

### Requisitos

- Pantalla con campos: título, contenido
- Botón enviar (deshabilitado si campos vacíos)
- Loading durante envío
- Mensaje de éxito/error
- Volver a la pantalla anterior al crear

### Criterios de aceptación

- [ ] Formulario valida campos
- [ ] Envía POST correctamente
- [ ] Muestra feedback al usuario
- [ ] Navega después de crear

---

## Ejercicio 4: Manejo de errores completo

### Instrucciones

Implementa manejo de errores robusto.

### Requisitos

Crea `NetworkResult` sealed class:
```kotlin
sealed class NetworkResult<out T> {
    data class Success<T>(val data: T) : NetworkResult<T>()
    data class Error(val code: Int, val message: String) : NetworkResult<Nothing>()
    data class Exception(val e: Throwable) : NetworkResult<Nothing>()
}
```

Muestra mensajes específicos:
- Sin conexión → "No hay conexión a internet"
- Timeout → "El servidor no responde"
- 404 → "Recurso no encontrado"
- 500 → "Error del servidor"

### Criterios de aceptación

- [ ] `safeApiCall` implementado
- [ ] Mensajes específicos por tipo de error
- [ ] UI muestra mensajes claros

---

## Ejercicio 5: Interceptor de autenticación

### Instrucciones

Simula autenticación con un token.

### Requisitos

- Crear `AuthInterceptor` que añade header `Authorization: Bearer <token>`
- El token puede ser hardcodeado para el ejercicio
- Verificar en logs que el header se envía

### Criterios de aceptación

- [ ] Interceptor creado e integrado
- [ ] El header aparece en los logs
- [ ] Las peticiones siguen funcionando

---

## Ejercicio 6: Búsqueda de posts

### Instrucciones

Implementa búsqueda con debounce.

### Requisitos

- Campo de búsqueda que filtra posts
- Debounce de 500ms antes de buscar
- Mostrar todos los posts si búsqueda vacía
- Loading mientras busca

**Tip:** Usa `Flow.debounce()` con coroutines.

### Criterios de aceptación

- [ ] Búsqueda filtra por título
- [ ] Debounce funciona (no busca en cada tecla)
- [ ] UI responde correctamente

---

## Ejercicio 7 (Bonus): Álbumes y fotos

### Instrucciones

Crea una galería de fotos usando:

**Endpoints:**
- Álbumes: `GET /albums`
- Fotos: `GET /photos?albumId={albumId}`

### Requisitos

- Lista de álbumes
- Al pulsar, mostrar grid de fotos (thumbnailUrl)
- Usar Coil para cargar imágenes

```kotlin
// Dependencia Coil
implementation("io.coil-kt:coil-compose:2.5.0")

// Uso
AsyncImage(
    model = photo.thumbnailUrl,
    contentDescription = null
)
```

### Criterios de aceptación

- [ ] Lista de álbumes
- [ ] Grid de fotos con Coil
- [ ] Navegación entre pantallas
- [ ] Manejo de errores

---

## Entrega

1. Estructura de carpetas:
   ```
   data/
     api/
     model/
     repository/
   ui/
     users/
     posts/
   ```
2. Crea rama y PR
3. Incluye capturas de pantalla
