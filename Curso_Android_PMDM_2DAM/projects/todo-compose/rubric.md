# Rúbrica — Proyecto 1: Todo Compose

> Puntuación orientativa (100 puntos). El profesor puede ajustar el peso si lo indica en clase.

## 1) Funcionalidad (40 puntos)

| Criterio | Puntos | Qué se espera |
|---|---:|---|
| CRUD completo | 20 | Crear, editar, completar y borrar tareas sin errores |
| Filtros | 10 | Todas / Pendientes / Completadas funcionando |
| Persistencia real | 10 | Room guarda y recupera al reiniciar |

## 2) UI/UX (20 puntos)

| Criterio | Puntos | Qué se espera |
|---|---:|---|
| Compose + Material 3 | 10 | Uso correcto de `Scaffold`, `TopAppBar`, etc. |
| Lista eficiente | 5 | `LazyColumn`, estados vacío/carga |
| Interacciones | 5 | Checkbox, FAB, swipe (o alternativa equivalente) |

## 3) Arquitectura y estado (25 puntos)

| Criterio | Puntos | Qué se espera |
|---|---:|---|
| MVVM | 10 | UI sin lógica de negocio; ViewModel orquesta |
| Estado y flujos | 10 | `StateFlow`/`UiState` bien definido y estable |
| Separación por capas | 5 | `ui/`, `domain/`, `data/` coherentes |

## 4) Calidad de código (10 puntos)

| Criterio | Puntos | Qué se espera |
|---|---:|---|
| Nombres y estructura | 5 | Paquetes/clases claros, sin duplicaciones |
| Manejo de errores/validaciones | 5 | Validar título, evitar crashes |

## 5) Testing (bonus hasta +5)

| Criterio | Bonus | Qué se espera |
|---|---:|---|
| Tests de ViewModel/Repository | +5 | Tests unitarios básicos (turbine/coroutines-test si aplica) |

---

## Penalizaciones típicas

- (-10) App no ejecuta / crash al iniciar.
- (-5) Lógica de DB directamente en Composables.
- (-5) Sin persistencia real (datos “en memoria”).

