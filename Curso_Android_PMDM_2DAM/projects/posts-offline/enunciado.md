# Enunciado — Proyecto 2: App API + Offline First (Posts)

## Descripción

Vas a desarrollar una app que consume una API REST y funciona con enfoque **offline-first**:

- La app muestra contenido desde red cuando hay conexión.
- Cachea datos en **Room**.
- Si no hay conexión, sigue funcionando con los datos locales.

Carpeta de trabajo:

- `projects/posts-offline/starter` (abre esta carpeta en Android Studio)

---

## API

Usaremos **JSONPlaceholder**:

- Base URL: `https://jsonplaceholder.typicode.com`

Endpoints principales:

| Endpoint | Método | Descripción |
|---|---|---|
| `/posts` | GET | Lista de posts |
| `/posts/{id}` | GET | Post por id |
| `/posts/{id}/comments` | GET | Comentarios del post |
| `/users` | GET | Lista de usuarios |
| `/users/{id}` | GET | Usuario por id |
| `/users/{id}/posts` | GET | Posts de un usuario |

---

## Requisitos funcionales (RF)

### RF1 — Listado de Posts

- Mostrar lista de posts
- Mostrar título + extracto del body
- Pull-to-refresh (o botón equivalente) para refrescar
- Indicar si estás online/offline (icono/texto)

### RF2 — Detalle de Post

- Ver post completo
- Mostrar autor (User)
- Mostrar comentarios del post

### RF3 — Usuarios

- Lista de usuarios
- Detalle de usuario con información completa
- Posibilidad de ver posts del usuario

### RF4 — Offline-first

- Cachear posts/usuarios/comentarios en Room
- La app debe seguir mostrando datos sin conexión
- Al volver la conexión, sincronizar (refrescar) y actualizar UI
- Mostrar estado del dato (por ejemplo: “datos locales” / “sincronizado”)

### RF5 (Bonus) — Crear post

- Formulario de creación
- Si no hay conexión: guardar localmente como “pendiente”
- Sincronizar cuando vuelva la conexión

---

## Requisitos técnicos (RT)

- UI con **Compose** + estado reactivo.
- Capa de red con **Retrofit** (+ converter).
- Capa local con **Room**.
- Arquitectura recomendada:
  - DTOs (red) → mappers → domain models
  - Entities (Room) → mappers → domain models
  - Repository como fuente de verdad (coordina red y local)
- Manejo de errores:
  - estados de carga
  - errores de red
  - no bloquear la UI

---

## Entrega

1. Trabajar desde `starter/`.
2. Subir cambios a Git (commits frecuentes).
3. Entregar mediante Pull Request según `docs/02-flujo-trabajo-git-y-entregas.md`.

---

## Criterios de aceptación (checklist)

- [ ] La app compila y ejecuta.
- [ ] Lista de posts + detalle funcionan.
- [ ] Usuarios funcionan.
- [ ] Con el dispositivo sin conexión, la app sigue mostrando datos cacheados.
- [ ] La UI refleja estados (cargando / error / offline).

