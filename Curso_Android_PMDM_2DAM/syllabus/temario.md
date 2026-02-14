# Temario - Curso Android PMDM 2º DAM

## Información general

| Aspecto | Detalle |
|---------|---------|
| Módulo | Programación Multimedia y Dispositivos Móviles |
| Ciclo | 2º DAM |
| Duración | 12 semanas (~96 horas lectivas) |
| Tecnologías | Kotlin, Jetpack Compose, MVVM, Room, Retrofit |

---

## Unidad 1: Fundamentos del entorno Android

### Lección 01: Setup y Gradle

**Contenidos:**
- Instalación y configuración de Android Studio
- Estructura de un proyecto Android
- Sistema de build Gradle
- Dependencias y plugins
- Ejecución en emulador y dispositivo físico

**Objetivos:**
- Configurar el entorno de desarrollo completo
- Entender la estructura de carpetas de un proyecto
- Saber añadir dependencias al proyecto
- Ejecutar una app en el emulador

### Lección 02: Kotlin Essentials

**Contenidos:**
- Variables, tipos y null safety
- Funciones y lambdas
- Clases, data classes y objects
- Colecciones y operaciones funcionales
- Extension functions
- Scope functions (let, run, apply, also, with)

**Objetivos:**
- Dominar la sintaxis básica de Kotlin
- Entender y usar null safety correctamente
- Trabajar con colecciones de forma funcional
- Aplicar scope functions apropiadamente

---

## Unidad 2: UI con Jetpack Compose

### Lección 03: Compose Basics

**Contenidos:**
- Paradigma declarativo vs imperativo
- Composables y recomposición
- Modificadores (Modifier)
- Layouts: Column, Row, Box, LazyColumn
- Material 3 components
- Estado local con remember y mutableStateOf
- Preview de composables

**Objetivos:**
- Entender el paradigma declarativo de Compose
- Crear interfaces con composables básicos
- Aplicar modificadores para estilo y comportamiento
- Manejar estado local en composables

### Lección 04: MVVM y UI State

**Contenidos:**
- Patrón MVVM en Android
- ViewModel y su ciclo de vida
- StateFlow y collectAsState
- UiState sealed class (Loading, Success, Error, Empty)
- Separación de responsabilidades
- Inyección de dependencias básica (manual)

**Objetivos:**
- Implementar arquitectura MVVM correctamente
- Crear y usar ViewModel con Compose
- Modelar estados de UI con sealed class
- Separar lógica de negocio de la UI

---

## Unidad 3: Navegación y listas

### Lección 05: Navigation Compose

**Contenidos:**
- NavController y NavHost
- Definición de rutas
- Navegación entre pantallas
- Paso de argumentos
- Deep links
- Navegación con bottom bar

**Objetivos:**
- Configurar navegación en una app multi-pantalla
- Pasar datos entre pantallas
- Implementar patrones de navegación comunes

### Lección 06: Listas y rendimiento

**Contenidos:**
- LazyColumn y LazyRow
- Items y keys
- Optimización de recomposiciones
- Paginación básica
- Pull to refresh
- Manejo de listas vacías

**Objetivos:**
- Implementar listas eficientes
- Evitar problemas de rendimiento comunes
- Manejar estados de lista vacía y carga

---

## Unidad 4: Conexión con APIs

### Lección 07: API con Retrofit

**Contenidos:**
- Cliente HTTP con OkHttp
- Retrofit setup y configuración
- Definición de endpoints
- Serialización JSON con kotlinx.serialization
- Interceptores y logging
- Manejo de errores de red

**Objetivos:**
- Configurar Retrofit en un proyecto
- Definir y consumir endpoints REST
- Serializar/deserializar JSON correctamente
- Manejar errores de red de forma robusta

### Lección 08: Coroutines y Flow

**Contenidos:**
- Introducción a coroutines
- suspend functions
- Dispatchers (Main, IO, Default)
- viewModelScope y lifecycleScope
- Flow básico
- StateFlow y SharedFlow
- Operadores de Flow (map, filter, catch)

**Objetivos:**
- Usar coroutines para operaciones asíncronas
- Entender los diferentes dispatchers
- Trabajar con Flow para streams de datos
- Combinar Flow con ViewModel

---

## Unidad 5: Persistencia local

### Lección 09: Room Database

**Contenidos:**
- Arquitectura de Room
- Entities y anotaciones
- DAO (Data Access Object)
- Database y migrations
- Queries básicas y avanzadas
- Room con Flow

**Objetivos:**
- Configurar Room en un proyecto
- Definir entidades y relaciones
- Implementar operaciones CRUD con DAO
- Observar cambios en la base de datos con Flow

### Lección 10: Offline First

**Contenidos:**
- Patrón Repository
- Single source of truth
- Sincronización API → Room
- Estrategias de cache
- Manejo de conectividad
- Conflictos y resolución

**Objetivos:**
- Implementar patrón Repository
- Crear apps que funcionen offline
- Sincronizar datos locales con remotos
- Detectar y manejar cambios de conectividad

---

## Unidad 6: Testing y distribución

### Lección 11: Testing de ViewModel

**Contenidos:**
- Tipos de tests en Android
- JUnit básico
- Testing de ViewModel
- Mocking con MockK o Fake
- Testing de coroutines
- Test de estados de UI

**Objetivos:**
- Escribir tests unitarios de ViewModel
- Usar fakes o mocks para dependencias
- Testear coroutines correctamente
- Verificar estados de UI en tests

### Lección 12: Entrega y APK

**Contenidos:**
- Build variants (debug, release)
- Firmado de APK
- ProGuard/R8 básico
- Generación de APK y AAB
- Checklist de entrega
- CI/CD con GitHub Actions

**Objetivos:**
- Generar APK de release firmado
- Entender las diferencias entre APK y AAB
- Preparar una app para distribución
- Usar CI para automatizar builds

---

## Proyectos evaluables

### Proyecto 1: Todo Compose

**Semana de entrega:** 6

**Lecciones prerequisito:** 01-06

**Resumen:**
App de gestión de tareas con persistencia local usando Room. Mínimo 2 pantallas (lista y detalle/crear). CRUD completo con filtros y validaciones.

### Proyecto 2: App API + Offline

**Semana de entrega:** 12

**Lecciones prerequisito:** 01-12

**Resumen:**
App que consume una API REST, cachea datos en Room para funcionamiento offline, y maneja correctamente todos los estados (loading, error, vacío, sin conexión).

---

## Competencias profesionales

Al finalizar el curso, el alumno habrá desarrollado:

### Competencias técnicas

- Desarrollo de apps Android nativas
- Arquitectura de software (MVVM)
- Consumo de APIs REST
- Persistencia de datos
- Testing básico
- Control de versiones con Git

### Competencias transversales

- Resolución de problemas
- Trabajo autónomo
- Documentación de código
- Trabajo colaborativo (PRs, code review)

---

## Recursos

### Incluidos en el repositorio

- 12 lecciones con teoría y ejercicios
- 2 proyectos starter completos
- Soluciones explicadas
- Documentación de instalación y troubleshooting

### Externos (complementarios)

- [Android Developers](https://developer.android.com/)
- [Kotlin Docs](https://kotlinlang.org/docs/)
- [Jetpack Compose Docs](https://developer.android.com/jetpack/compose)
