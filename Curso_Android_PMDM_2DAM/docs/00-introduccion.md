# Introducción al Curso

## Sobre este curso

Este curso de **Programación Multimedia y Dispositivos Móviles (PMDM)** está diseñado para estudiantes de 2º de DAM que quieren aprender desarrollo Android moderno.

## Objetivos generales

Al finalizar el curso serás capaz de:

- Crear aplicaciones Android nativas con Kotlin
- Diseñar interfaces declarativas con Jetpack Compose
- Implementar arquitectura MVVM correctamente
- Conectar apps con APIs REST
- Persistir datos localmente con Room
- Gestionar estados y errores de forma profesional
- Escribir tests unitarios básicos
- Generar APKs para distribución

## Filosofía del curso

### Aprender haciendo

No hay largas sesiones teóricas. Cada lección tiene:
- Teoría mínima necesaria (15-20 min lectura)
- Pasos guiados para implementar
- Ejercicios prácticos inmediatos

### Código real

Todos los ejemplos son código funcional que puedes ejecutar. No hay pseudocódigo ni fragmentos incompletos.

### Arquitectura moderna

Seguimos las recomendaciones oficiales de Google:
- Compose para UI (no XML)
- MVVM con ViewModel
- Coroutines para asincronía
- Room para persistencia

### Sin dependencias externas críticas

Todo lo que necesitas está en el repositorio. Los enlaces externos son complementarios, no obligatorios.

## Conocimientos previos necesarios

| Tema | Nivel |
|------|-------|
| Programación orientada a objetos | Medio |
| Git básico (clone, commit, push, branch) | Básico |
| Kotlin o Java | Básico |
| SQL básico | Básico |

Si no dominas Kotlin, la lección 02 cubre lo esencial.

## Herramientas que usaremos

| Herramienta | Propósito |
|-------------|-----------|
| Android Studio | IDE principal |
| Git + GitHub | Control de versiones y entregas |
| Emulador Android | Pruebas sin dispositivo físico |
| GitHub Actions | CI/CD automático |

## Metodología de trabajo

### Semana típica

1. **Día 1-2:** Leer lección y seguir pasos guiados
2. **Día 3-4:** Resolver ejercicios
3. **Día 5:** Revisar soluciones, corregir errores
4. **Continuo:** Trabajo en proyecto evaluable

### Entregas

- Las entregas se hacen via **Pull Request** en GitHub
- El CI verifica automáticamente que el código compila y pasa tests
- El profesor revisa y da feedback en el PR

## Evaluación resumida

| Componente | Peso |
|------------|------|
| Proyecto 1: Todo App | 30% |
| Proyecto 2: API + Offline | 40% |
| Ejercicios y participación | 30% |

Ver detalles completos en [03-guia-evaluacion.md](03-guia-evaluacion.md).

## Consejos para tener éxito

1. **No copies código sin entenderlo** - Si copias de las soluciones sin entender, fallarás en los proyectos
2. **Haz commits frecuentes** - Pequeños commits con mensajes claros
3. **Pregunta pronto** - No pierdas horas atascado, abre un Issue
4. **Lee los errores** - Android Studio da mensajes útiles, léelos
5. **Usa el emulador** - No dependas solo de dispositivo físico

## Siguiente paso

→ [01-instalacion-android-studio.md](01-instalacion-android-studio.md)
