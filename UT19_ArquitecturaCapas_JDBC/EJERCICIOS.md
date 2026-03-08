# 🏋️ EJERCICIOS PRÁCTICOS — UT19 Arquitectura en Capas con JDBC

> **Autor:** Joaquín Rodríguez Llanes  
> **Nivel:** Java Intermedio (antes de Spring Boot)  
> **Tiempo total estimado:** 6–8 horas  
> **Prerrequisitos:** Java 17, Maven, conocimientos básicos de SQL.

> 💡 **Cómo usar estos ejercicios:**  
> Cada ejercicio incluye un **análisis técnico** que explica QUÉ hay que hacer, POR QUÉ y EN QUÉ ARCHIVOS.  
> Al final de cada uno hay una **📋 Cajita de Prompt** lista para copiar y enviar a una IA  
> (Gemini, ChatGPT, etc.) si quieres que lo implemente automáticamente.  
> **Recomendación:** intenta hacerlo tú primero. Si te atascas, usa el prompt.

---

## 📋 Índice de Ejercicios

| # | Ejercicio | Nivel | Tiempo | Capas que toca |
|---|-----------|-------|--------|----------------|
| 1 | Ejecutar y explorar el proyecto | ⭐ Básico | 20 min | Todas (lectura) |
| 2 | Añadir búsqueda por ID desde menú | ⭐ Básico | 20 min | Application |
| 3 | Añadir campo `email` a Usuario | ⭐⭐ Intermedio | 45 min | Model → BD → Repository → Service → Application |
| 4 | Implementar `count()` en el repositorio | ⭐ Básico | 20 min | Repository → Service → Application |
| 5 | Crear entidad y repositorio `Producto` | ⭐⭐ Intermedio | 60 min | Model → BD → Repository |
| 6 | Implementar `ProductoService` con validaciones | ⭐⭐ Intermedio | 45 min | Service → Application |
| 7 | Implementación en memoria del repositorio | ⭐⭐⭐ Avanzado | 60 min | Repository (nueva impl.) |
| 8 | Tests unitarios con JUnit 5 + Mockito | ⭐⭐⭐ Avanzado | 60 min | Test |

---

## ⭐ EJERCICIO 1 — Ejecutar y explorar el proyecto (básico)

### 🎯 Objetivo
Entender la arquitectura de capas **antes** de modificar nada.

### ✅ Pasos
1. Ejecuta: `mvn exec:java -Dexec.mainClass="com.curso.ut19.Application"`
2. Prueba el menú completo: inserta 3 usuarios, lístalos, actualiza uno, elimínalo.
3. Mira el fichero `miBaseDatos.db` generado en la raíz del proyecto.
4. Busca en el código dónde se ejecuta cada consulta SQL.

### 🧠 Preguntas para responder
1. ¿Cuántas capas tiene la aplicación? ¿Cuál es la responsabilidad de cada una?
2. ¿Qué pasaría si cambiáramos SQLite por MySQL? ¿Qué ficheros habría que modificar?
3. ¿Qué es un `PreparedStatement` y por qué es más seguro que concatenar Strings en el SQL?
4. ¿Qué hace `Db.java`? ¿Por qué es un Singleton?
5. ¿Dónde están las reglas de negocio: en el Repository o en el Service?

---

## ⭐ EJERCICIO 2 — Búsqueda por ID desde el menú (básico)

### 🎯 Objetivo
Explicar el flujo completo de una operación añadiendo una opción nueva al menú.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Application** | `Application.java` | Añadir opción "5) Buscar por ID" al menú y método `buscarPorId()` |

### 🧠 Decisiones de diseño
- `findById()` ya existe en la interfaz `UsuarioRepository` → solo hay que usarlo desde el menú.
- Se usa `Optional.ifPresentOrElse()` para mostrar el usuario o un mensaje de aviso.
- NO se modifica ni el Repository ni el Service → el flujo ya existe, solo falta exponerlo.

### 📋 Prompt para la IA
> ```
> En mi proyecto Java Maven "UT19_ArquitecturaCapas_JDBC", necesito añadir
> una opción de búsqueda por ID al menú de la consola.
>
> Archivo a modificar:
> - src/main/java/com/curso/ut19/Application.java
>   → añadir opción "5. Buscar usuario por ID" al menú
>   → crear método buscarPorId(UsuarioService service) que:
>     1) Pide ID al usuario
>     2) Llama a service.obtener(id)
>     3) Usa ifPresentOrElse() para mostrar datos o "No encontrado"
>   → renumerar "Salir" a opción 6
>
> El método service.obtener(id) ya existe y devuelve Optional<Usuario>.
> Usa estilo Better Comments (// *, // ?, // !).
> ```

---

## ⭐⭐ EJERCICIO 3 — Añadir campo `email` a Usuario (intermedio)

### 🎯 Objetivo
Practicar el **ciclo completo** de un cambio en JDBC: modelo → BD → repositorio → servicio → menú.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Model** | `Usuario.java` | Añadir campo `email` + constructor + getter/setter |
| **BD** | `Db.java` | Añadir columna `email TEXT` al CREATE TABLE |
| **Repository** | `UsuarioRepositoryJdbc.java` | Actualizar SQL de INSERT, SELECT y el método `map()` |
| **Service** | `UsuarioService.java` | Actualizar `crear()` para recibir email |
| **Application** | `Application.java` | Pedir email al usuario en el menú |

### 🧠 Decisiones de diseño
- El email es opcional → `TEXT` sin `NOT NULL` en SQL.
- `CREATE TABLE IF NOT EXISTS` NO añade columnas nuevas → **hay que borrar `miBaseDatos.db`** y recrear.
- En el `map(ResultSet rs)` se lee con `rs.getString("email")`.
- En el `save()` se añade un 3er parámetro al PreparedStatement.

### ⚠️ Errores comunes
- Olvidar borrar `miBaseDatos.db` → la tabla no tiene la columna email → `SQLException`.
- No actualizar el método `map()` → el email nunca se lee de la BD.
- No actualizar `update()` → al editar un usuario se pierde el email.

### 📋 Prompt para la IA
> ```
> En mi proyecto Java Maven "UT19_ArquitecturaCapas_JDBC", necesito añadir
> un campo "email" (String, opcional) a la entidad Usuario.
>
> Archivos a modificar:
> - src/main/java/com/curso/ut19/model/Usuario.java
>   → añadir campo email, actualizar constructor, getter/setter, toString
> - src/main/java/com/curso/ut19/db/Db.java
>   → añadir columna "email TEXT" al CREATE TABLE
> - src/main/java/com/curso/ut19/repository/jdbc/UsuarioRepositoryJdbc.java
>   → actualizar save() para incluir email en INSERT
>   → actualizar update() para incluir email en UPDATE
>   → actualizar map(ResultSet) para leer email
> - src/main/java/com/curso/ut19/service/UsuarioService.java
>   → actualizar crear() para recibir email
> - src/main/java/com/curso/ut19/Application.java
>   → pedir email al usuario en el menú de crear
>
> IMPORTANTE: Hay que borrar miBaseDatos.db para que se recree con la nueva columna.
> Usa estilo Better Comments.
> ```

---

## ⭐ EJERCICIO 4 — Implementar `count()` en el repositorio (básico)

### 🎯 Objetivo
Añadir un método SQL personalizado y exponerlo por las 3 capas.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Repository (interfaz)** | `UsuarioRepository.java` | Añadir firma `long count()` |
| **Repository (impl.)** | `UsuarioRepositoryJdbc.java` | Implementar con `SELECT COUNT(*)` |
| **Service** | `UsuarioService.java` | Crear `contarUsuarios()` |
| **Application** | `Application.java` | Mostrar total antes de listar |

### 🧠 Decisiones de diseño
- `SELECT COUNT(*)` devuelve una sola fila con una sola columna → `rs.getLong(1)`.
- Se expone en el Service aunque sea un simple "pass-through" → mantiene la separación de capas.
- Se muestra al inicio del listado: "Total de usuarios: X".

### 📋 Prompt para la IA
> ```
> En mi proyecto Java Maven "UT19_ArquitecturaCapas_JDBC", necesito implementar
> un método count() que cuente los usuarios en BD.
>
> Archivos a modificar:
> - src/main/java/com/curso/ut19/repository/UsuarioRepository.java
>   → añadir firma: long count()
> - src/main/java/com/curso/ut19/repository/jdbc/UsuarioRepositoryJdbc.java
>   → implementar con SELECT COUNT(*) FROM usuarios, usando try-with-resources
>   → leer rs.getLong(1), retornar 0 si no hay resultados
> - src/main/java/com/curso/ut19/service/UsuarioService.java
>   → crear contarUsuarios() que delegue en repository.count()
> - src/main/java/com/curso/ut19/Application.java
>   → mostrar "Total de usuarios: X" antes del listado
>
> Usa SLF4J para logging de errores. Estilo Better Comments.
> ```

---

## ⭐⭐ EJERCICIO 5 — Crear entidad y repositorio `Producto` (intermedio)

### 🎯 Objetivo
Reproducir la arquitectura existente para una nueva entidad, demostrando que el patrón es **replicable**.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Model** | `Producto.java` (nuevo) | Clase con id, nombre, precio |
| **BD** | `Db.java` | Añadir CREATE TABLE productos |
| **Repository (interfaz)** | `ProductoRepository.java` (nuevo) | Misma interfaz que UsuarioRepository |
| **Repository (impl.)** | `ProductoRepositoryJdbc.java` (nuevo) | CRUD JDBC completo |

### 🧠 Decisiones de diseño
- `precio` es `double` → `REAL` en SQLite, `ps.setDouble()`, `rs.getDouble()`.
- `CHECK(precio >= 0)` en SQL para impedir precios negativos en la BD.
- Se sigue el mismo patrón exacto que `UsuarioRepositoryJdbc` (copy-adapt).
- La interfaz `ProductoRepository` es igual a `UsuarioRepository` pero con tipo `Producto`.

### 📋 Prompt para la IA
> ```
> En mi proyecto Java Maven "UT19_ArquitecturaCapas_JDBC", necesito crear
> una nueva entidad Producto con su repositorio JDBC completo.
>
> Archivos a crear:
> - src/main/java/com/curso/ut19/model/Producto.java
>   → campos: int id, String nombre, double precio
>   → constructor sin id, constructor completo, getters/setters, toString
> - src/main/java/com/curso/ut19/repository/ProductoRepository.java
>   → interfaz con save, findById, findAll, update, delete (mismo patrón que UsuarioRepository)
> - src/main/java/com/curso/ut19/repository/jdbc/ProductoRepositoryJdbc.java
>   → implementación JDBC completa con PreparedStatement y try-with-resources
>   → precio: ps.setDouble() / rs.getDouble()
>
> Archivo a modificar:
> - src/main/java/com/curso/ut19/db/Db.java
>   → añadir CREATE TABLE IF NOT EXISTS productos (id, nombre, precio REAL CHECK >= 0)
>
> Usa SLF4J para logging. Estilo Better Comments.
> ```

---

## ⭐⭐ EJERCICIO 6 — ProductoService con validaciones (intermedio)

### 🎯 Objetivo
Añadir **lógica de negocio** específica para productos en la capa Service.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Service** | `ProductoService.java` (nuevo) | Validaciones de negocio + delegación al repo |
| **Application** | `Application.java` | Añadir submenú de productos |

### 🧠 Decisiones de diseño
- Reglas: nombre obligatorio, precio >= 0, aviso si precio es 0 (gratuito).
- Se inyecta `ProductoRepository` por constructor (mismo patrón que `UsuarioService`).
- Si precio < 0 → `IllegalArgumentException` (la regla vive en el Service, no en la BD).
- La BD tiene `CHECK(precio >= 0)` como **segunda barrera** de seguridad.

### 📋 Prompt para la IA
> ```
> En mi proyecto Java Maven "UT19_ArquitecturaCapas_JDBC", necesito crear
> ProductoService con validaciones y añadir un menú de productos.
>
> Archivos a crear:
> - src/main/java/com/curso/ut19/service/ProductoService.java
>   → constructor con ProductoRepository inyectado
>   → crear(nombre, precio): valida nombre no vacío, precio >= 0, aviso si precio == 0
>   → listar(): delega en repo.findAll()
>   → borrar(id): delega en repo.delete()
>
> Archivo a modificar:
> - src/main/java/com/curso/ut19/Application.java
>   → añadir opción "Gestión de Productos" en el menú principal
>   → crear submenú con: listar, crear, borrar productos
>   → instanciar ProductoRepositoryJdbc y ProductoService al inicio
>
> Usa estilo Better Comments e IllegalArgumentException para errores.
> ```

---

## ⭐⭐⭐ EJERCICIO 7 — Implementación en memoria del repositorio (avanzado)

### 🎯 Objetivo
Demostrar el poder del **patrón Repository**: cambiar la implementación sin tocar el resto del código.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Repository (nueva impl.)** | `UsuarioRepositoryInMemory.java` (nuevo) | Implementar con `HashMap` en vez de JDBC |
| **Application** | `Application.java` | Cambiar 1 línea para usar la nueva implementación |

### 🧠 Decisiones de diseño
- Se simula la tabla con `Map<Integer, Usuario>` y el AUTOINCREMENT con `AtomicInteger`.
- Implementa **exactamente la misma interfaz** `UsuarioRepository`.
- Al cambiar `new UsuarioRepositoryJdbc()` por `new UsuarioRepositoryInMemory()`, **todo el resto del código sigue funcionando** sin cambios.
- **Esto demuestra por qué usamos interfaces**: la capa de negocio no sabe si los datos están en BD, en memoria, en un fichero o en la nube.

### ⚠️ Concept clave
```
UsuarioService  →  UsuarioRepository (interfaz)
                       ↓                    ↓
              UsuarioRepositoryJdbc   UsuarioRepositoryInMemory
              (SQLite real)           (HashMap en memoria)
```
El Service NO cambia. Los tests NO cambian. **Solo cambia 1 línea en Application.**

### 📋 Prompt para la IA
> ```
> En mi proyecto Java Maven "UT19_ArquitecturaCapas_JDBC", necesito crear
> una implementación en memoria del UsuarioRepository para demostrar
> el patrón Repository (interfaz + múltiples implementaciones).
>
> Archivo a crear:
> - src/main/java/com/curso/ut19/repository/memory/UsuarioRepositoryInMemory.java
>   → implementa UsuarioRepository
>   → usa Map<Integer, Usuario> como almacén
>   → usa AtomicInteger para simular AUTOINCREMENT
>   → los 5 métodos: save, findById, findAll, update, delete
>
> Archivo a modificar (solo 1 línea):
> - src/main/java/com/curso/ut19/Application.java
>   → cambiar new UsuarioRepositoryJdbc() por new UsuarioRepositoryInMemory()
>   → comentar con // ? para explicar el cambio
>
> Usa estilo Better Comments. Explica en comentarios por qué esto demuestra
> el poder de las interfaces.
> ```

---

## ⭐⭐⭐ EJERCICIO 8 — Tests unitarios con JUnit 5 + Mockito (avanzado)

### 🎯 Objetivo
Testear `UsuarioService` de forma **aislada** usando mocks (sin BD real).

### 📖 Análisis técnico

| Qué probar | Resultado esperado |
|---|---|
| `crear()` con nombre vacío | Lanza `IllegalArgumentException` |
| `crear()` con edad negativa | Lanza `IllegalArgumentException` |
| `crear()` con datos válidos | Llama a `repo.save()` y retorna el usuario |
| `borrar()` delega correctamente | Llama a `repo.delete()` con el ID correcto |

### 🧠 Decisiones de diseño
- `@Mock` crea un falso Repository que NO toca la BD.
- `when(repo.save(...)).thenReturn(...)` configura qué devuelve el mock.
- `verify(repo).save(...)` comprueba que el Service llamó al repo correctamente.
- Patrón AAA: **Arrange** (preparar) → **Act** (ejecutar) → **Assert** (verificar).

### 📋 Prompt para la IA
> ```
> En mi proyecto Java Maven "UT19_ArquitecturaCapas_JDBC", necesito crear
> tests unitarios para UsuarioService usando JUnit 5 y Mockito.
>
> Archivo a crear:
> - src/test/java/com/curso/ut19/service/UsuarioServiceTest.java
>
> Tests a implementar:
> 1. crear() con nombre vacío → lanza IllegalArgumentException con "vacío"
> 2. crear() con edad negativa → lanza IllegalArgumentException con "negativa"
> 3. crear() con datos válidos → llama repo.save() y retorna el usuario
> 4. borrar() → delega en repo.delete() con el ID correcto
>
> Usa:
> - @Mock para UsuarioRepository
> - @BeforeEach con MockitoAnnotations.openMocks(this)
> - AssertJ: assertThat, assertThatThrownBy
> - @DisplayName descriptivo en cada test
> - Patrón AAA con comentarios // * Arrange / Act / Assert
>
> Dependencias ya están en pom.xml: junit-jupiter 5, mockito-core, assertj-core.
> ```

---

## 📚 Tabla resumen: Conceptos clave del proyecto

| Concepto | Dónde verlo en el código |
|----------|--------------------------|
| **Repository Pattern** | `UsuarioRepository` (interfaz) + `UsuarioRepositoryJdbc` (impl.) |
| **Service Layer** | `UsuarioService` — reglas de negocio aisladas del SQL |
| **Dependency Injection** | `new UsuarioService(repo)` en `Application.java` |
| **PreparedStatement** | `UsuarioRepositoryJdbc` — previene SQL Injection |
| **Optional\<T\>** | `findById()` — evita NullPointerException |
| **Try-with-resources** | `try (PreparedStatement ps = ...)` — cierre automático |
| **Singleton** | `Db.getConnection()` — conexión única a SQLite |
| **SLF4J + Logback** | Logging profesional con niveles (info, error, debug) |
| **Maven** | `pom.xml`, `mvn compile`, `mvn test`, `mvn exec:java` |
| **JUnit 5 + Mockito** | Tests aislados sin BD real |

---

## 🏁 Rúbrica de evaluación

| Criterio | Peso |
|---|---|
| **Correctitud:** funciona bien y los tests pasan | 40% |
| **Diseño por capas:** cada responsabilidad en su capa | 25% |
| **Robustez:** SQL seguro, errores controlados, logging | 20% |
| **Claridad:** nombres descriptivos, código legible | 15% |

---

## 🚀 ¿Quieres ir más allá?

| Idea | Dificultad | Qué aprenderías |
|------|-----------|-----------------|
| Buscar usuarios por nombre parcial (LIKE) | ⭐⭐ | SQL LIKE, PreparedStatement con wildcards |
| Transacciones (commit/rollback) | ⭐⭐⭐ | `Connection.setAutoCommit(false)`, atomicidad |
| Pool de conexiones (HikariCP) | ⭐⭐⭐ | DataSource vs DriverManager, rendimiento |
| Migrar a Spring Boot | ⭐⭐⭐⭐ | Comparar JDBC manual vs Spring Data JPA |
