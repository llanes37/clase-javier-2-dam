# Rúbrica — Proyecto 2: App API + Offline First (Posts)

> Puntuación orientativa (100 puntos). El profesor puede ajustar el peso si lo indica en clase.

## 1) Funcionalidad base (45 puntos)

| Criterio | Puntos | Qué se espera |
|---|---:|---|
| Posts (lista + detalle) | 20 | Navegación, carga y UI correctas |
| Usuarios (lista + detalle) | 10 | Datos coherentes y navegables |
| Comentarios | 5 | En detalle de post |
| Refresh + estados | 10 | Pull-to-refresh, loading/error visibles |

## 2) Offline-first real (30 puntos)

| Criterio | Puntos | Qué se espera |
|---|---:|---|
| Cache en Room | 15 | Persistencia y lectura local |
| Funciona sin conexión | 10 | Modo avión: UI sigue mostrando datos |
| Sincronización | 5 | Refresca al volver la conexión (o manual) |

## 3) Arquitectura y calidad (20 puntos)

| Criterio | Puntos | Qué se espera |
|---|---:|---|
| Repository bien planteado | 10 | Coordina red/local, evita duplicación |
| Modelado y mappers | 5 | DTO/Entity → Domain limpios |
| Código limpio | 5 | Paquetes, nombres, sin lógica en UI |

## 4) Testing (bonus hasta +5)

| Criterio | Bonus | Qué se espera |
|---|---:|---|
| Tests de repository/VM | +5 | Tests unitarios básicos (mock/fake) |

---

## Penalizaciones típicas

- (-15) “Offline” falso: sin Room o sin lectura local.
- (-10) Crash al navegar o al perder conexión.
- (-5) Lógica de red/DB directamente en Composables.

