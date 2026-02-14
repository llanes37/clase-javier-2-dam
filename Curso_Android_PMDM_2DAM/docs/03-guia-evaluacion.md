# Guía de evaluación

## Distribución de la nota final

| Componente | Peso | Descripción |
|------------|------|-------------|
| Proyecto 1: Todo Compose | 30% | App de tareas con Room |
| Proyecto 2: API + Offline | 40% | App con API y cache |
| Ejercicios y participación | 30% | Trabajo continuo |

---

## Proyecto 1: Todo Compose (30%)

### Requisitos mínimos para aprobar (5/10)

- [ ] App compila sin errores
- [ ] CI pasa (tests, lint, build)
- [ ] Pantalla de lista de tareas funcional
- [ ] Crear nueva tarea funciona
- [ ] Marcar tarea como completada funciona
- [ ] Datos persisten con Room

### Requisitos para nota máxima (10/10)

- [ ] Todo lo anterior
- [ ] Editar tarea existente
- [ ] Eliminar tarea
- [ ] Filtro pendientes/completadas
- [ ] Validaciones de formulario
- [ ] Mínimo 3 tests de ViewModel
- [ ] Código limpio y bien estructurado
- [ ] UI cuidada (Material 3)

### Penalizaciones

| Motivo | Penalización |
|--------|--------------|
| Entrega tardía (≤3 días) | -1 punto |
| Entrega tardía (>3 días) | -2 puntos |
| CI no pasa | -1 punto |
| Código copiado sin entender | -50% a -100% |
| No seguir arquitectura MVVM | -1 punto |

### Rúbrica detallada

Ver [todo-compose/rubric.md](../projects/todo-compose/rubric.md)

---

## Proyecto 2: API + Offline (40%)

### Requisitos mínimos para aprobar (5/10)

- [ ] App compila sin errores
- [ ] CI pasa (tests, lint, build)
- [ ] Lista desde API funcional
- [ ] Pantalla de detalle funcional
- [ ] Manejo básico de errores (Loading/Error)
- [ ] Cache con Room funciona

### Requisitos para nota máxima (10/10)

- [ ] Todo lo anterior
- [ ] Búsqueda o filtrado
- [ ] Modo offline completo
- [ ] Estados: Loading, Success, Error, Empty
- [ ] Mínimo 5 tests de ViewModel
- [ ] Arquitectura data/domain/ui clara
- [ ] Manejo de timeout y sin conexión
- [ ] Pull-to-refresh
- [ ] UI cuidada (Material 3)

### Penalizaciones

| Motivo | Penalización |
|--------|--------------|
| Entrega tardía (≤3 días) | -1 punto |
| Entrega tardía (>3 días) | -2 puntos |
| CI no pasa | -1 punto |
| Código copiado sin entender | -50% a -100% |
| API hardcodeada sin manejo errores | -1 punto |
| No hay cache offline | -2 puntos |

### Rúbrica detallada

Ver [posts-offline/rubric.md](../projects/posts-offline/rubric.md)

---

## Ejercicios y participación (30%)

### Componentes

| Elemento | Peso dentro del 30% |
|----------|---------------------|
| Ejercicios de lecciones | 60% |
| Participación en clase | 20% |
| Calidad de PRs y commits | 20% |

### Ejercicios de lecciones

Cada lección tiene ejercicios en `ejercicios.md`.

**Criterios:**
- Entregados a tiempo
- Funcionan correctamente
- Código limpio
- No es copia literal de soluciones

### Participación

- Preguntas relevantes en clase
- Ayudar a compañeros (sin dar soluciones directas)
- Reportar errores en el material
- Proponer mejoras

### Calidad de PRs y commits

- Commits con mensajes claros
- PRs bien documentadas
- Respuesta rápida a feedback

---

## Criterios generales de código

### Obligatorio

| Criterio | Descripción |
|----------|-------------|
| Compila | Sin errores de compilación |
| Funciona | La funcionalidad pedida existe |
| Tests pasan | `./gradlew test` sin fallos |
| Lint limpio | Sin errores de lint (warnings ok) |
| MVVM | Arquitectura respetada |
| Kotlin idiomático | Uso correcto del lenguaje |

### Valorado positivamente

| Criterio | Bonus |
|----------|-------|
| Tests adicionales | +0.5 |
| UI excepcional | +0.5 |
| Documentación extra | +0.25 |
| Manejo errores exhaustivo | +0.5 |
| Código especialmente limpio | +0.25 |

### Penalizado

| Problema | Penalización |
|----------|--------------|
| Warnings de lint ignorados | -0.25 |
| TODO comments sin resolver | -0.25 |
| Código comentado (dead code) | -0.25 |
| Nombres de variables pobres | -0.5 |
| God classes/functions | -0.5 |
| Copiar soluciones sin entender | -50% a -100% |

---

## Política de integridad académica

### Permitido

- Consultar documentación oficial
- Usar las soluciones del curso (después de intentarlo)
- Discutir conceptos con compañeros
- Buscar errores específicos en Stack Overflow

### No permitido

- Copiar código de compañeros
- Usar código de internet sin entenderlo
- Usar IA para generar el proyecto completo
- Compartir tu código con compañeros

### Consecuencias

| Infracción | Consecuencia |
|------------|--------------|
| Primera vez (menor) | Advertencia + rehacer entrega |
| Primera vez (grave) | 0 en la entrega |
| Reincidencia | Suspenso en la asignatura |

---

## Fechas importantes

| Entrega | Fecha límite | Peso |
|---------|--------------|------|
| Proyecto 1 | Semana 6 (viernes 23:59) | 30% |
| Proyecto 2 | Semana 12 (viernes 23:59) | 40% |
| Ejercicios | Cada semana (domingo 23:59) | 30% |

Las fechas exactas se comunicarán al inicio del curso.

---

## Proceso de revisión

### 1. Entrega

Alumno abre PR antes de la fecha límite.

### 2. CI automático

GitHub Actions ejecuta tests, lint y build.

### 3. Revisión del profesor

- Revisa código
- Prueba funcionalidad (descarga APK del artifact)
- Deja comentarios

### 4. Feedback

- Comentarios en la PR
- Posibles cambios requeridos

### 5. Calificación

- Se publica nota en el sistema de la escuela
- Feedback detallado en la PR

---

## Recuperación

### Proyectos

Si suspendes un proyecto:
- Tienes una convocatoria de recuperación
- Fecha: después de la evaluación ordinaria
- Requisitos: mismos que la entrega original
- Nota máxima en recuperación: 7/10

### Asignatura

Para aprobar la asignatura necesitas:
- Nota final ≥ 5
- Al menos 4/10 en cada proyecto
- Al menos 40% de ejercicios entregados

---

## Siguiente paso

→ [04-solucion-problemas.md](04-solucion-problemas.md)
