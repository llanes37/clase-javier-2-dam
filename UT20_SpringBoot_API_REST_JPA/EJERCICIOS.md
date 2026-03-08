# 🏋️ EJERCICIOS PRÁCTICOS — UT20 Spring Boot API REST JPA

> **Autor:** Joaquín Rodríguez Llanes  
> **Nivel:** Spring Boot Intermedio  
> **Tiempo total estimado:** 6–8 horas  
> **Prerrequisitos:** Haber completado UT19 (Arquitectura en Capas con JDBC).

> 💡 **Cómo usar estos ejercicios:**  
> Cada ejercicio incluye un **análisis técnico** que explica QUÉ hay que hacer, POR QUÉ y EN QUÉ ARCHIVOS.  
> Al final de cada uno hay una **📋 Cajita de Prompt** lista para copiar y enviar a una IA  
> (Gemini, ChatGPT, etc.) si quieres que lo implemente automáticamente.  
> **Recomendación:** intenta hacerlo tú primero. Si te atascas, usa el prompt.

---

## 📋 Índice de Ejercicios

| # | Ejercicio | Nivel | Tiempo | Capas que toca |
|---|-----------|-------|--------|----------------|
| 1 | Explorar Swagger UI y la consola H2 | ⭐ Básico | 15 min | Todas (lectura) |
| 2 | Probar la API con curl o Postman | ⭐ Básico | 30 min | Controller (uso) |
| 3 | Añadir campo `email` a Usuario | ⭐⭐ Intermedio | 45 min | Entity → Repository → Service → Controller |
| 4 | Crear endpoint de búsqueda por nombre | ⭐⭐ Intermedio | 45 min | Repository → Service → Controller |
| 5 | Crear entidad y CRUD completo de `Categoria` | ⭐⭐ Intermedio | 60 min | Entity → Repository → Service → Controller |
| 6 | Relación ManyToOne: Producto ↔ Categoria | ⭐⭐⭐ Avanzado | 90 min | Entity → Repository → Controller |
| 7 | Paginación con `Pageable` | ⭐⭐ Intermedio | 45 min | Service → Controller |
| 8 | Tests unitarios del Service con Mockito | ⭐⭐⭐ Avanzado | 90 min | Test |

---

## ⭐ EJERCICIO 1 — Explorar Swagger UI y H2 Console (básico)

### 🎯 Objetivo
Familiarizarse con la **documentación automática** de la API y la **consola de BD en memoria**.

### ✅ Pasos
1. Arranca la app: `mvn spring-boot:run`
2. Abre Swagger: `http://localhost:8080/swagger-ui/index.html`
3. Expande `GET /api/usuarios` → **Try it out** → **Execute**.
4. Observa: petición curl, código de respuesta (`200`), body JSON.
5. Abre H2 Console: `http://localhost:8080/h2-console`
   - JDBC URL: `jdbc:h2:mem:testdb` — Usuario: `sa` — Password: (vacío)
6. Ejecuta: `SELECT * FROM USUARIO;`

### 🧠 Preguntas para responder
1. ¿Qué diferencia hay entre `200`, `201` y `204`?
2. ¿Qué pasa si haces `GET /api/usuarios/999`? ¿Qué código retorna?
3. ¿De dónde saca Swagger la información para generar la documentación?
4. ¿Qué pasa con los datos de H2 si reinicias la app?

---

## ⭐ EJERCICIO 2 — Probar la API con curl o Postman (básico)

### 🎯 Objetivo
Practicar el **ciclo CRUD completo** vía HTTP y entender los códigos de respuesta.

### 📖 Análisis técnico
Cada operación HTTP tiene un significado y un código de respuesta:

| Operación | Método | Código éxito | Código error |
|---|---|---|---|
| Listar todos | GET | 200 OK | — |
| Obtener uno | GET /{id} | 200 OK | 404 Not Found |
| Crear | POST | 201 Created | 400 Bad Request |
| Actualizar | PUT /{id} | 200 OK | 404 Not Found |
| Eliminar | DELETE /{id} | 204 No Content | 404 Not Found |

### ✅ Comandos curl a probar
```bash
# Crear usuario
curl -X POST http://localhost:8080/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Ana García", "edad": 28}'

# Listar todos
curl http://localhost:8080/api/usuarios

# Crear con nombre vacío → 400 Bad Request
curl -X POST http://localhost:8080/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre": "", "edad": 25}'
```

### 📋 Prompt para la IA
> ```
> Muéstrame una colección completa de comandos curl para probar el CRUD
> de mi API REST Spring Boot con endpoints:
> - GET /api/usuarios (listar)
> - GET /api/usuarios/{id} (obtener)
> - POST /api/usuarios (crear con JSON)
> - PUT /api/usuarios/{id} (actualizar)
> - DELETE /api/usuarios/{id} (borrar)
>
> Incluye casos de éxito y de error (nombre vacío, edad negativa, ID inexistente).
> Explica qué código HTTP se espera en cada caso.
> ```

---

## ⭐⭐ EJERCICIO 3 — Añadir campo `email` a Usuario (intermedio)

### 🎯 Objetivo
Practicar el ciclo completo de un cambio en Spring Boot: entidad → repo → service → controller.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Entity** | `Usuario.java` | Añadir campo `email` con `@Column(unique=true)`, `@NotBlank`, `@Email` |
| **Repository** | `UsuarioRepository.java` | Añadir `findByEmail(String email)` (query derivada) |
| **Service** | `UsuarioService.java` | Validar unicidad de email antes de guardar |
| **Controller** | (no cambia) | Spring deserializa el email del JSON automáticamente |

### 🧠 Decisiones de diseño
- `@Column(unique = true)` → restricción en BD (segunda barrera).
- `@Email` → Bean Validation verifica formato ANTES de llegar al Service.
- `findByEmail()` → Spring Data genera el SQL automáticamente (sin escribir SQL manual).
- `ddl-auto=update` → Hibernate añade la columna al reiniciar (sin borrar datos en H2).
- La unicidad se valida en el **Service** (mensaje claro) Y en la **BD** (integridad).

### 📋 Prompt para la IA
> ```
> En mi proyecto Spring Boot "UT20_SpringBoot_API_REST_JPA", necesito
> añadir un campo "email" (String, único, obligatorio) a la entidad Usuario.
>
> Archivos a modificar:
> - src/main/java/com/curso/ut20/model/Usuario.java
>   → añadir campo email con @Column(unique=true), @NotBlank, @Email
>   → getter y setter
> - src/main/java/com/curso/ut20/repository/UsuarioRepository.java
>   → añadir Optional<Usuario> findByEmail(String email) (query derivada)
> - src/main/java/com/curso/ut20/service/UsuarioService.java
>   → en crear(): verificar que no exista otro usuario con el mismo email
>   → si existe: lanzar IllegalArgumentException con mensaje claro
>
> El Controller NO necesita cambios (Spring deserializa email del JSON).
> Hibernate con ddl-auto=update añade la columna automáticamente.
> Usa estilo Better Comments.
> ```

---

## ⭐⭐ EJERCICIO 4 — Endpoint de búsqueda por nombre (intermedio)

### 🎯 Objetivo
Añadir un endpoint de **búsqueda parcial** por nombre usando `@RequestParam`.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Repository** | `UsuarioRepository.java` | Añadir `findByNombreContainingIgnoreCase(String nombre)` |
| **Service** | `UsuarioService.java` | Crear `buscarPorNombre(String nombre)` |
| **Controller** | `UsuarioController.java` | Nuevo endpoint `GET /api/usuarios/buscar?nombre=Ana` |

### 🧠 Decisiones de diseño
- `findByNombreContainingIgnoreCase()` → Spring genera SQL con `LIKE '%nombre%'` automáticamente.
- `@RequestParam(defaultValue = "")` → si no se envía el parámetro, retorna todos.
- El endpoint se mapea en una **URL diferente** (`/buscar`) para no colisionar con `/api/usuarios`.

### 📋 Prompt para la IA
> ```
> En mi proyecto Spring Boot "UT20_SpringBoot_API_REST_JPA", necesito un
> endpoint de búsqueda parcial de usuarios por nombre.
>
> Archivos a modificar:
> - src/main/java/com/curso/ut20/repository/UsuarioRepository.java
>   → añadir: List<Usuario> findByNombreContainingIgnoreCase(String nombre)
> - src/main/java/com/curso/ut20/service/UsuarioService.java
>   → crear buscarPorNombre(String nombre) que delega en el repo
> - src/main/java/com/curso/ut20/controller/UsuarioController.java
>   → nuevo endpoint: @GetMapping("/buscar")
>   → recibe @RequestParam(defaultValue="") String nombre
>   → si nombre está vacío: retorna todos; si no: busca por nombre
>
> Usa estilo Better Comments. Documentar con Javadoc para Swagger.
> ```

---

## ⭐⭐ EJERCICIO 5 — Crear entidad y CRUD completo de Categoria (intermedio)

### 🎯 Objetivo
Reproducir el **patrón completo** (Entity → Repo → Service → Controller) para una nueva entidad.

### 📖 Análisis técnico

| Capa | Archivo (nuevo) | Qué hacer |
|------|-----------------|-----------|
| **Entity** | `Categoria.java` | `@Entity` con id, nombre, descripcion |
| **Repository** | `CategoriaRepository.java` | `extends JpaRepository<Categoria, Long>` |
| **Service** | `CategoriaService.java` | CRUD + validación nombre obligatorio |
| **Controller** | `CategoriaController.java` | `@RestController` con CRUD completo en `/api/categorias` |

### 🧠 Decisiones de diseño
- Se sigue el mismo patrón exacto que Usuario y Producto (copy-adapt).
- `descripcion` es opcional (sin `@NotBlank`).
- `@GeneratedValue(strategy = IDENTITY)` para auto-incremento del ID.
- Swagger lo documenta automáticamente sin configuración extra.

### 📋 Prompt para la IA
> ```
> En mi proyecto Spring Boot "UT20_SpringBoot_API_REST_JPA", necesito crear
> una entidad Categoria con CRUD completo siguiendo el patrón existente.
>
> Archivos a crear:
> - src/main/java/com/curso/ut20/model/Categoria.java
>   → @Entity con id (Long, @GeneratedValue IDENTITY), nombre (@NotBlank), descripcion (opcional)
>   → getters/setters
> - src/main/java/com/curso/ut20/repository/CategoriaRepository.java
>   → extends JpaRepository<Categoria, Long>
> - src/main/java/com/curso/ut20/service/CategoriaService.java
>   → @Service con listar, buscar(id), crear, actualizar(id), borrar(id)
>   → validación: nombre obligatorio
> - src/main/java/com/curso/ut20/controller/CategoriaController.java
>   → @RestController @RequestMapping("/api/categorias")
>   → GET (listar), GET/{id}, POST (201), PUT/{id}, DELETE/{id} (204)
>   → ResponseEntity con códigos HTTP correctos
>
> Usa el mismo patrón que UsuarioController/UsuarioService. Estilo Better Comments.
> ```

---

## ⭐⭐⭐ EJERCICIO 6 — Relación ManyToOne: Producto ↔ Categoria (avanzado)

### 🎯 Objetivo
Implementar una **relación entre entidades** con `@ManyToOne` y un endpoint para consultar productos por categoría.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Entity** | `Producto.java` | Añadir `@ManyToOne` con `Categoria` |
| **Repository** | `ProductoRepository.java` | Añadir `findByCategoriaId(Long id)` |
| **Service** | `ProductoService.java` | Crear `listarPorCategoria(Long categoriaId)` |
| **Controller** | `ProductoController.java` | Nuevo endpoint `GET /api/productos/categoria/{id}` |

### 🧠 Decisiones de diseño
- `@ManyToOne(fetch = FetchType.LAZY)` → no carga la categoría salvo que se acceda.
- `@JoinColumn(name = "categoria_id")` → nombre de la FK en la tabla producto.
- `findByCategoriaId()` → Spring genera `WHERE categoria_id = ?` automáticamente.
- Al crear un producto vía API, se envía `categoriaId` y se busca la categoría.

### ⚠️ Errores comunes
- Serialización circular (Producto → Categoria → List<Producto> → ...) → usar `@JsonIgnore` o DTO.
- `LazyInitializationException` → usar `FetchType.EAGER` o `@EntityGraph`.

### 📋 Prompt para la IA
> ```
> En mi proyecto Spring Boot "UT20_SpringBoot_API_REST_JPA", necesito relacionar
> Producto con Categoria usando @ManyToOne.
>
> Archivos a modificar:
> - src/main/java/com/curso/ut20/model/Producto.java
>   → añadir @ManyToOne(fetch=LAZY) @JoinColumn(name="categoria_id") Categoria categoria
>   → getter/setter
> - src/main/java/com/curso/ut20/repository/ProductoRepository.java
>   → añadir List<Producto> findByCategoriaId(Long categoriaId)
> - src/main/java/com/curso/ut20/service/ProductoService.java
>   → crear listarPorCategoria(Long categoriaId)
> - src/main/java/com/curso/ut20/controller/ProductoController.java
>   → nuevo endpoint @GetMapping("/categoria/{categoriaId}")
>
> OJO: evitar serialización circular con @JsonIgnore en la lista inversa
> o usando @JsonBackReference/@JsonManagedReference.
> Usa estilo Better Comments.
> ```

---

## ⭐⭐ EJERCICIO 7 — Paginación con Pageable (intermedio)

### 🎯 Objetivo
Implementar **paginación** para no cargar todos los registros de golpe.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Service** | `UsuarioService.java` | Crear `listarPaginado(Pageable pageable)` |
| **Controller** | `UsuarioController.java` | Nuevo endpoint `GET /api/usuarios/paginado` |

### 🧠 Decisiones de diseño
- `JpaRepository` ya hereda `findAll(Pageable)` → no necesitas añadir nada al repo.
- `Page<Usuario>` contiene: `.getContent()` (lista), `.getTotalPages()`, `.getTotalElements()`, `.getNumber()`.
- Parámetros en URL: `?page=0&size=5&sort=nombre,asc`.
- Spring inyecta `Pageable` automáticamente si lo declaras como parámetro del controller.
- El JSON de respuesta incluye metadatos de paginación automáticamente.

### 📋 Prompt para la IA
> ```
> En mi proyecto Spring Boot "UT20_SpringBoot_API_REST_JPA", necesito
> implementar paginación en el listado de usuarios.
>
> Archivos a modificar:
> - src/main/java/com/curso/ut20/service/UsuarioService.java
>   → crear listarPaginado(Pageable pageable) que delega en repo.findAll(pageable)
> - src/main/java/com/curso/ut20/controller/UsuarioController.java
>   → nuevo endpoint @GetMapping("/paginado")
>   → recibe Pageable como parámetro (Spring lo inyecta automáticamente)
>   → retorna Page<Usuario>
>
> Ejemplo de uso: GET /api/usuarios/paginado?page=0&size=3&sort=nombre,asc
> JpaRepository ya tiene findAll(Pageable) heredado.
> Usa estilo Better Comments y documenta con Javadoc para Swagger.
> ```

---

## ⭐⭐⭐ EJERCICIO 8 — Tests unitarios del Service con Mockito (avanzado)

### 🎯 Objetivo
Verificar el `UsuarioService` **sin arrancar Spring ni la BD** usando mocks.

### 📖 Análisis técnico

| Qué probar | Resultado esperado |
|---|---|
| `listar()` sin datos | Retorna lista vacía, llama a `repo.findAll()` |
| `buscar(id)` cuando existe | Retorna Optional con el usuario |
| `buscar(id)` cuando no existe | Retorna Optional vacío |
| `crear(usuario)` | Llama a `repo.save()` y retorna el usuario con ID |

### 🧠 Decisiones de diseño
- `@Mock` → crea un falso Repository (no arranca BD).
- `@InjectMocks` → crea el Service inyectando el mock automáticamente.
- `when(...).thenReturn(...)` → configura qué devuelve el mock.
- `verify(repo).save(...)` → comprueba que el Service llamó al repo correctamente.
- **Patrón AAA:** Arrange (preparar) → Act (ejecutar) → Assert (verificar).

### 📋 Prompt para la IA
> ```
> En mi proyecto Spring Boot "UT20_SpringBoot_API_REST_JPA", necesito crear
> tests unitarios para UsuarioService con JUnit 5 y Mockito.
>
> Archivo a crear:
> - src/test/java/com/curso/ut20/service/UsuarioServiceTest.java
>
> Tests a implementar:
> 1. listar() sin datos → retorna lista vacía, verify repo.findAll() called
> 2. buscar(id) cuando existe → retorna Optional con usuario
> 3. buscar(id) cuando no existe → retorna Optional.empty()
> 4. crear(usuario) → llama repo.save() y retorna el usuario
>
> Usa:
> - @Mock para UsuarioRepository
> - @InjectMocks para UsuarioService
> - @BeforeEach con MockitoAnnotations.openMocks(this)
> - AssertJ: assertThat, assertThatThrownBy
> - @DisplayName descriptivo
> - Comentarios // * Arrange / Act / Assert
>
> Dependencias en pom.xml: spring-boot-starter-test (incluye JUnit 5, Mockito, AssertJ).
> ```

---

## 📚 Tabla resumen: Conceptos clave del proyecto

| Concepto | Dónde verlo en el código |
|----------|--------------------------|
| **@RestController** | `UsuarioController`, `ProductoController` |
| **ResponseEntity\<T\>** | Controllers — control de código HTTP + body |
| **@RequestBody** | POST/PUT — JSON → Objeto Java |
| **@PathVariable** | GET/{id}, PUT/{id}, DELETE/{id} |
| **@RequestParam** | GET/buscar?nombre=Ana |
| **@Service** | `UsuarioService`, `ProductoService` |
| **JpaRepository** | Repos heredan CRUD sin escribir SQL |
| **Bean Validation** | `@NotBlank`, `@Email`, `@Min` en entidades |
| **Swagger / OpenAPI** | `/swagger-ui/index.html` — doc automática |
| **H2 en memoria** | `/h2-console` — BD que se reinicia con la app |
| **Optional\<T\>** | `findById()` → evita null |
| **Query derivadas** | `findByNombreContainingIgnoreCase()` |

---

## 🏁 Rúbrica de evaluación

| Criterio | Peso |
|---|---|
| **Correctitud:** endpoints funcionan, códigos HTTP correctos | 40% |
| **Diseño por capas:** Controller → Service → Repository | 25% |
| **Robustez:** validaciones, errores controlados, códigos HTTP | 20% |
| **Claridad:** nombres RESTful, Swagger documentado | 15% |

---

## 🚀 ¿Quieres ir más allá?

| Idea | Dificultad | Qué aprenderías |
|------|-----------|-----------------|
| DTOs (no exponer la entidad) | ⭐⭐ | Separar modelo de API, MapStruct |
| Spring Security (JWT) | ⭐⭐⭐⭐ | Autenticación, roles, tokens |
| Tests de Controller con MockMvc | ⭐⭐⭐ | `@WebMvcTest`, simular HTTP |
| Docker para despliegue | ⭐⭐ | Dockerfile, docker-compose |
| Cambiar H2 por PostgreSQL | ⭐⭐ | Perfiles Spring, datasource |
| Frontend React/Vue consumiendo la API | ⭐⭐⭐ | fetch/axios, CORS, fullstack |
