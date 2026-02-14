# Enunciado — Proyecto 1: Todo Compose

## Descripción

Vas a desarrollar una aplicación de gestión de tareas (**Todo List**) con **Kotlin + Jetpack Compose + Material 3**, siguiendo arquitectura **MVVM** y persistencia local con **Room**.

Carpeta de trabajo:

- `projects/todo-compose/starter` (abre esta carpeta en Android Studio)

---

## Objetivos de aprendizaje

- UI declarativa con **Jetpack Compose**
- Gestión de estado con **StateFlow** y `UiState`
- Arquitectura **MVVM** (separación de responsabilidades)
- Persistencia local con **Room**
- Navegación con **Navigation Compose**
- Código limpio (capas y paquetes coherentes)

---

## Requisitos funcionales (RF)

### RF1 — Pantalla principal (Home)

- Lista de tareas (recomendado: `LazyColumn`)
- Mostrar:
  - título
  - prioridad (alta/media/baja)
  - fecha límite (si existe)
  - estado (completado/pendiente)
- Marcar como completada con `Checkbox`
- Borrado por gesto (recomendado: swipe)
- Botón flotante (FAB) para añadir una tarea nueva

### RF2 — Crear/Editar tarea

- Campo **título** (obligatorio)
- Campo **descripción** (opcional)
- Selector de **fecha límite** (opcional)
- Selector de **prioridad** (alta/media/baja)
- Botón “Guardar” / “Actualizar”

### RF3 — Filtros

- Ver **todas**
- Ver solo **pendientes**
- Ver solo **completadas**
- Orden recomendado: pendientes primero

### RF4 — Persistencia

- Guardar tareas con **Room**
- Cargar tareas al iniciar la app
- Las operaciones CRUD deben reflejarse en UI automáticamente (UI reactiva)

---

## Requisitos técnicos (RT)

- UI con **Compose** (sin pantallas XML).
- Arquitectura recomendada:
  - `ui/` (pantallas, componentes, navegación)
  - `domain/` (modelos de negocio)
  - `data/` (Room + repository)
- No acceder a Room directamente desde Composables:
  - UI → ViewModel → Repository → DAO
- Manejo de estados:
  - `UiState` claro (loading, datos, vacío, error si aplica)
- Validaciones:
  - No permitir guardar una tarea con título vacío

---

## Entrega

1. Trabajar desde `starter/`.
2. Subir cambios a Git (commits frecuentes y con mensaje claro).
3. Entregar mediante **Pull Request** según el flujo de `docs/02-flujo-trabajo-git-y-entregas.md`.

---

## Criterios de aceptación (checklist)

- [ ] La app compila y ejecuta en emulador (API 34 recomendado).
- [ ] Puedo crear, editar, completar y borrar tareas.
- [ ] Los filtros funcionan y la lista se actualiza sin reiniciar la app.
- [ ] Los datos persisten al cerrar y reabrir la app.
- [ ] El código está organizado por capas (sin lógica de datos en UI).

