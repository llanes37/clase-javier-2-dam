# 🚀 UT20 - Spring Boot API REST con JPA

> **Proyecto educativo completo** que demuestra las mejores prácticas de desarrollo de APIs REST con Spring Boot 3, JPA/Hibernate, validaciones y documentación automática.

---

## 📋 Tabla de Contenidos

1. [Introducción](#-introducción)
2. [Tecnologías Utilizadas](#-tecnologías-utilizadas)
3. [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
4. [Configuración y Ejecución](#-configuración-y-ejecución)
5. [Endpoints de la API](#-endpoints-de-la-api)
6. [Explicación Detallada por Capas](#-explicación-detallada-por-capas)
7. [Ejercicios Prácticos](#-ejercicios-prácticos)
8. [Testing con Swagger](#-testing-con-swagger)
9. [Base de Datos H2](#-base-de-datos-h2)
10. [Mejoras Sugeridas](#-mejoras-sugeridas)

---

## 🎯 Introducción

Este proyecto es una **API REST completa** que implementa operaciones CRUD (Create, Read, Update, Delete) para dos entidades:
- **Usuarios** (nombre, edad)
- **Productos** (nombre, precio)

### ¿Qué aprenderás?

✅ Crear una API REST profesional con Spring Boot
✅ Implementar persistencia de datos con JPA/Hibernate
✅ Aplicar validaciones automáticas
✅ Manejar errores de forma centralizada
✅ Documentar APIs automáticamente con Swagger
✅ Trabajar con bases de datos en memoria (H2)
✅ Aplicar inyección de dependencias
✅ Usar programación funcional con Optional

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Java** | 17 | Lenguaje de programación |
| **Spring Boot** | 3.3.4 | Framework principal |
| **Spring Data JPA** | - | Persistencia de datos |
| **Hibernate** | - | ORM (Object-Relational Mapping) |
| **H2 Database** | - | Base de datos en memoria |
| **Bean Validation** | - | Validaciones (@Valid, @NotBlank, @Min) |
| **Swagger/OpenAPI** | 2.5.0 | Documentación automática |
| **Maven** | - | Gestión de dependencias |

---

## 🏗️ Arquitectura del Proyecto

El proyecto sigue el patrón de **arquitectura por capas**:

```
UT20_SpringBoot_API_REST_JPA/
├── src/main/java/com/curso/ut20/
│   ├── Ut20Application.java          # 🚀 Clase principal
│   │
│   ├── model/                         # 📦 CAPA DE MODELO (Entidades JPA)
│   │   ├── Usuario.java              # Entidad Usuario
│   │   └── Producto.java             # Entidad Producto
│   │
│   ├── repository/                    # 💾 CAPA DE DATOS (Repositorios)
│   │   ├── UsuarioRepository.java    # Acceso a datos de Usuario
│   │   └── ProductoRepository.java   # Acceso a datos de Producto
│   │
│   ├── controller/                    # 🌐 CAPA DE CONTROLADORES (API REST)
│   │   ├── UsuarioController.java    # Endpoints de Usuario
│   │   └── ProductoController.java   # Endpoints de Producto
│   │
│   └── exception/                     # ⚠️ MANEJO DE ERRORES
│       └── GlobalExceptionHandler.java
│
├── src/main/resources/
│   └── application.properties         # ⚙️ Configuración
│
└── pom.xml                            # 📦 Dependencias Maven
```

### Flujo de una Petición HTTP

```
Cliente (Postman/Navegador)
    ↓
[HTTP Request] GET /api/usuarios
    ↓
@RestController (UsuarioController)
    ↓
@Valid - Validaciones
    ↓
Repository (UsuarioRepository)
    ↓
Spring Data JPA
    ↓
Hibernate (ORM)
    ↓
H2 Database
    ↓
[HTTP Response] JSON
    ↓
Cliente recibe datos
```

---

## ⚙️ Configuración y Ejecución

### Prerrequisitos

- Java 17 o superior
- Maven 3.6+
- IDE (IntelliJ IDEA, Eclipse, VSCode)

### Pasos para ejecutar

1. **Clonar o descargar el proyecto**

2. **Compilar el proyecto**
   ```bash
   mvn clean install
   ```

3. **Ejecutar la aplicación**
   ```bash
   mvn spring-boot:run
   ```

   O desde tu IDE: ejecutar `Ut20Application.java`

4. **Verificar que está funcionando**
   - Deberías ver en consola un banner ASCII con las URLs
   - La aplicación arranca en `http://localhost:8080`

### URLs Importantes

| Recurso | URL |
|---------|-----|
| **API Usuarios** | http://localhost:8080/api/usuarios |
| **API Productos** | http://localhost:8080/api/productos |
| **Swagger UI** | http://localhost:8080/swagger-ui/index.html |
| **H2 Console** | http://localhost:8080/h2-console |

---

## 🌐 Endpoints de la API

### 👤 Usuarios (`/api/usuarios`)

| Método | Endpoint | Descripción | Código HTTP |
|--------|----------|-------------|-------------|
| **GET** | `/api/usuarios` | Listar todos los usuarios | 200 OK |
| **GET** | `/api/usuarios/{id}` | Obtener un usuario por ID | 200 OK / 404 Not Found |
| **POST** | `/api/usuarios` | Crear nuevo usuario | 201 Created |
| **PUT** | `/api/usuarios/{id}` | Actualizar usuario existente | 200 OK / 404 Not Found |
| **DELETE** | `/api/usuarios/{id}` | Eliminar usuario | 204 No Content / 404 Not Found |

#### Ejemplo de JSON para Usuario

```json
{
  "nombre": "Juan Pérez",
  "edad": 25
}
```

### 📦 Productos (`/api/productos`)

| Método | Endpoint | Descripción | Código HTTP |
|--------|----------|-------------|-------------|
| **GET** | `/api/productos` | Listar todos los productos | 200 OK |
| **GET** | `/api/productos/{id}` | Obtener un producto por ID | 200 OK / 404 Not Found |
| **POST** | `/api/productos` | Crear nuevo producto | 201 Created |
| **PUT** | `/api/productos/{id}` | Actualizar producto existente | 200 OK / 404 Not Found |
| **DELETE** | `/api/productos/{id}` | Eliminar producto | 204 No Content / 404 Not Found |

#### Ejemplo de JSON para Producto

```json
{
  "nombre": "Laptop Dell",
  "precio": 999.99
}
```

---

## 📚 Explicación Detallada por Capas

### 1️⃣ Capa de Modelo (Entidades JPA)

#### `Usuario.java` y `Producto.java`

**Propósito:** Representan las tablas de la base de datos como clases Java.

**Anotaciones clave:**

- `@Entity` - Marca la clase como entidad JPA (tabla en BD)
- `@Id` - Define la clave primaria
- `@GeneratedValue(strategy = GenerationType.IDENTITY)` - Auto-incremento del ID
- `@NotBlank` - El campo no puede estar vacío
- `@Min(0)` - El valor debe ser >= 0

**¿Cómo funciona?**

Cuando arranca la aplicación, Hibernate lee estas clases y **crea automáticamente** las tablas en H2:

```sql
CREATE TABLE usuario (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    edad INT
);

CREATE TABLE producto (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    precio DOUBLE
);
```

---

### 2️⃣ Capa de Repositorios (Spring Data JPA)

#### `UsuarioRepository.java` y `ProductoRepository.java`

**Propósito:** Interfaces que proporcionan acceso a la base de datos **sin escribir SQL**.

```java
public interface UsuarioRepository extends JpaRepository<Usuario, Long> {
    // ¡No necesitas implementar nada!
    // Spring Data JPA genera el código automáticamente
}
```

**Métodos heredados automáticamente:**

| Método | Descripción | SQL Equivalente |
|--------|-------------|-----------------|
| `findAll()` | Obtiene todos los registros | `SELECT * FROM usuario` |
| `findById(Long id)` | Busca por ID | `SELECT * FROM usuario WHERE id = ?` |
| `save(Usuario u)` | Guarda o actualiza | `INSERT` o `UPDATE` |
| `deleteById(Long id)` | Elimina por ID | `DELETE FROM usuario WHERE id = ?` |
| `existsById(Long id)` | Verifica si existe | `SELECT COUNT(*) FROM usuario WHERE id = ?` |
| `count()` | Cuenta registros | `SELECT COUNT(*) FROM usuario` |

**Magia de Spring Data JPA:**

Spring genera dinámicamente una implementación en tiempo de ejecución usando **proxies dinámicos**. ¡No necesitas escribir la clase de implementación!

---

### 3️⃣ Capa de Controladores (API REST)

#### `UsuarioController.java` y `ProductoController.java`

**Propósito:** Exponen endpoints HTTP para que los clientes interactúen con la API.

**Anotaciones clave:**

- `@RestController` - Combina `@Controller` + `@ResponseBody` (respuestas JSON automáticas)
- `@RequestMapping("/api/usuarios")` - Prefijo de ruta
- `@GetMapping` - Endpoint GET
- `@PostMapping` - Endpoint POST
- `@PutMapping("/{id}")` - Endpoint PUT con variable de ruta
- `@DeleteMapping("/{id}")` - Endpoint DELETE
- `@PathVariable` - Extrae variable de la URL
- `@RequestBody` - Deserializa JSON del body
- `@Valid` - Activa validaciones

**Ejemplo detallado:**

```java
@PostMapping
public ResponseEntity<Usuario> crear(@Valid @RequestBody Usuario u) {
    Usuario saved = repo.save(u);
    return ResponseEntity
        .created(URI.create("/api/usuarios/" + saved.getId()))
        .body(saved);
}
```

**¿Qué sucede aquí?**

1. Cliente envía POST con JSON: `{"nombre": "Ana", "edad": 30}`
2. `@RequestBody` convierte JSON → Objeto Usuario
3. `@Valid` verifica que nombre no esté vacío y edad >= 0
4. Si validación falla → 400 Bad Request (manejado por GlobalExceptionHandler)
5. Si validación pasa → `repo.save()` inserta en BD
6. Retorna 201 Created con header `Location: /api/usuarios/1`

---

### 4️⃣ Manejo de Excepciones

#### `GlobalExceptionHandler.java`

**Propósito:** Captura errores de validación y retorna respuestas JSON estructuradas.

**Flujo:**

1. Cliente envía: `{"nombre": "", "edad": -5}`
2. `@Valid` detecta errores
3. Spring lanza `MethodArgumentNotValidException`
4. `GlobalExceptionHandler` captura la excepción
5. Extrae los errores de cada campo
6. Retorna 400 Bad Request con:

```json
{
  "nombre": "El nombre del usuario es obligatorio",
  "edad": "La edad debe ser mayor o igual a 0"
}
```

---

### 5️⃣ Configuración (application.properties)

```properties
# Base de datos H2 en memoria
spring.datasource.url=jdbc:h2:mem:ut20db
spring.datasource.username=sa
spring.datasource.password=

# Hibernate: Actualiza el esquema automáticamente
spring.jpa.hibernate.ddl-auto=update

# Consola H2 habilitada
spring.h2.console.enabled=true
```

**¿Qué significa `ddl-auto=update`?**

- `create` - Elimina y recrea las tablas al arrancar (PIERDE DATOS)
- `create-drop` - Crea al arrancar, elimina al cerrar
- **`update`** - Crea las tablas si no existen, actualiza si cambian (CONSERVA DATOS)
- `validate` - Solo valida que el esquema coincida
- `none` - No hace nada

---

## 🎓 Ejercicios Prácticos

### 📝 Nivel 1: Básico (Familiarización)

#### Ejercicio 1.1: Probar los endpoints con Swagger

1. Arranca la aplicación
2. Abre http://localhost:8080/swagger-ui/index.html
3. Crea 3 usuarios usando el endpoint POST `/api/usuarios`
4. Lista todos los usuarios con GET `/api/usuarios`
5. Obtén un usuario específico con GET `/api/usuarios/{id}`
6. Actualiza un usuario con PUT `/api/usuarios/{id}`
7. Elimina un usuario con DELETE `/api/usuarios/{id}`

**Objetivo:** Entender cómo funciona cada endpoint.

---

#### Ejercicio 1.2: Validaciones

1. Intenta crear un usuario sin nombre:
   ```json
   {
     "nombre": "",
     "edad": 25
   }
   ```
   **¿Qué código HTTP recibes? ¿Qué mensaje?**

2. Intenta crear un usuario con edad negativa:
   ```json
   {
     "nombre": "Pedro",
     "edad": -10
   }
   ```
   **¿Qué sucede?**

3. Envía múltiples errores a la vez:
   ```json
   {
     "nombre": "",
     "edad": -5
   }
   ```
   **¿Cuántos errores retorna?**

**Objetivo:** Comprender el sistema de validaciones.

---

#### Ejercicio 1.3: Explorar la base de datos H2

1. Abre http://localhost:8080/h2-console
2. Configura la conexión:
   - **JDBC URL:** `jdbc:h2:mem:ut20db`
   - **Usuario:** `sa`
   - **Contraseña:** *(dejar vacío)*
3. Conéctate y ejecuta:
   ```sql
   SELECT * FROM usuario;
   SELECT * FROM producto;
   ```
4. Inserta un usuario directamente con SQL:
   ```sql
   INSERT INTO usuario (nombre, edad) VALUES ('Admin', 99);
   ```
5. Verifica con GET `/api/usuarios` que el usuario aparece

**Objetivo:** Entender que Spring Data JPA trabaja sobre SQL.

---

### 📝 Nivel 2: Intermedio (Extensión de Funcionalidades)

#### Ejercicio 2.1: Añadir campo "descripción" a Producto

**Tarea:** Añade un nuevo campo `descripcion` a la entidad Producto.

**Pasos:**

1. Abre `Producto.java`
2. Añade el campo:
   ```java
   @NotBlank(message = "La descripción es obligatoria")
   private String descripcion;
   ```
3. Genera getters y setters
4. Actualiza el controlador para incluir descripción en actualizaciones
5. Reinicia la aplicación (Hibernate actualizará la tabla automáticamente)
6. Prueba crear un producto con descripción

**Validación:**
- Verifica en H2 Console que la columna `descripcion` existe
- Prueba validaciones (descripción vacía debe fallar)

---

#### Ejercicio 2.2: Consulta personalizada - Buscar usuarios por nombre

**Tarea:** Implementa un endpoint para buscar usuarios por nombre.

**Pasos:**

1. En `UsuarioRepository.java`, añade:
   ```java
   List<Usuario> findByNombre(String nombre);
   ```

2. En `UsuarioController.java`, añade:
   ```java
   @GetMapping("/buscar")
   public List<Usuario> buscarPorNombre(@RequestParam String nombre) {
       return repo.findByNombre(nombre);
   }
   ```

3. Prueba con: `GET /api/usuarios/buscar?nombre=Juan`

**Bonus:** Añade búsqueda parcial (que contenga):
```java
List<Usuario> findByNombreContaining(String keyword);
```

---

#### Ejercicio 2.3: Endpoint para contar productos

**Tarea:** Crea un endpoint que retorne el número total de productos.

**Pasos:**

1. En `ProductoController.java`, añade:
   ```java
   @GetMapping("/count")
   public long contarProductos() {
       return repo.count();
   }
   ```

2. Prueba con `GET /api/productos/count`

**Bonus:** Añade conteo de productos por rango de precio:
```java
@GetMapping("/count-por-precio")
public long contarPorPrecio(@RequestParam double min, @RequestParam double max) {
    return repo.countByPrecioBetween(min, max);
}
```
(Deberás crear el método en el repositorio)

---

#### Ejercicio 2.4: Añadir validación @Email

**Tarea:** Añade un campo `email` a Usuario con validación de email.

**Pasos:**

1. En `Usuario.java`, añade:
   ```java
   @Email(message = "Email inválido")
   @NotBlank(message = "El email es obligatorio")
   private String email;
   ```

2. No olvides añadir getters y setters

3. Importa: `import jakarta.validation.constraints.Email;`

4. Prueba enviar emails inválidos:
   - `"test"` → Debe fallar
   - `"test@"` → Debe fallar
   - `"test@example.com"` → Debe pasar

---

### 📝 Nivel 3: Avanzado (Arquitectura y Mejoras)

#### Ejercicio 3.1: Implementar capa de servicios

**Tarea:** Añade una capa `@Service` entre controladores y repositorios.

**Estructura:**

```
controller/ → service/ → repository/
```

**Pasos:**

1. Crea el paquete `com.curso.ut20.service`

2. Crea `UsuarioService.java`:
   ```java
   package com.curso.ut20.service;

   import com.curso.ut20.model.Usuario;
   import com.curso.ut20.repository.UsuarioRepository;
   import org.springframework.stereotype.Service;
   import java.util.List;
   import java.util.Optional;

   @Service
   public class UsuarioService {
       private final UsuarioRepository repo;

       public UsuarioService(UsuarioRepository repo) {
           this.repo = repo;
       }

       public List<Usuario> listarTodos() {
           return repo.findAll();
       }

       public Optional<Usuario> buscarPorId(Long id) {
           return repo.findById(id);
       }

       public Usuario guardar(Usuario usuario) {
           return repo.save(usuario);
       }

       public void eliminar(Long id) {
           repo.deleteById(id);
       }

       public boolean existe(Long id) {
           return repo.existsById(id);
       }
   }
   ```

3. Modifica `UsuarioController.java` para usar el servicio:
   ```java
   @RestController
   @RequestMapping("/api/usuarios")
   public class UsuarioController {
       private final UsuarioService service; // Cambiado de repo a service

       public UsuarioController(UsuarioService service) {
           this.service = service;
       }

       @GetMapping
       public List<Usuario> listar() {
           return service.listarTodos();
       }
       // ... actualizar todos los métodos
   }
   ```

**Beneficios:**
- Separación de responsabilidades
- Lógica de negocio centralizada
- Facilita testing con mocks

---

#### Ejercicio 3.2: DTOs (Data Transfer Objects)

**Tarea:** Crea DTOs para no exponer las entidades directamente.

**¿Por qué?**
- Las entidades contienen anotaciones JPA
- No queremos exponer todos los campos (ej: contraseñas)
- Permite diferentes representaciones del mismo objeto

**Pasos:**

1. Crea el paquete `com.curso.ut20.dto`

2. Crea `UsuarioDTO.java`:
   ```java
   package com.curso.ut20.dto;

   import jakarta.validation.constraints.Min;
   import jakarta.validation.constraints.NotBlank;

   public class UsuarioDTO {
       private Long id;

       @NotBlank
       private String nombre;

       @Min(0)
       private int edad;

       // Constructor vacío
       public UsuarioDTO() {}

       // Constructor desde entidad
       public UsuarioDTO(Usuario usuario) {
           this.id = usuario.getId();
           this.nombre = usuario.getNombre();
           this.edad = usuario.getEdad();
       }

       // Getters y setters...
   }
   ```

3. Crea un mapper:
   ```java
   public Usuario toEntity() {
       Usuario usuario = new Usuario();
       usuario.setId(this.id);
       usuario.setNombre(this.nombre);
       usuario.setEdad(this.edad);
       return usuario;
   }
   ```

4. Modifica el controlador para usar DTOs:
   ```java
   @PostMapping
   public ResponseEntity<UsuarioDTO> crear(@Valid @RequestBody UsuarioDTO dto) {
       Usuario usuario = dto.toEntity();
       Usuario saved = service.guardar(usuario);
       return ResponseEntity.created(/*...*/).body(new UsuarioDTO(saved));
   }
   ```

---

#### Ejercicio 3.3: Paginación y ordenación

**Tarea:** Añade paginación a los endpoints de listado.

**Pasos:**

1. Modifica el método listar:
   ```java
   @GetMapping
   public Page<Usuario> listar(
       @RequestParam(defaultValue = "0") int page,
       @RequestParam(defaultValue = "10") int size,
       @RequestParam(defaultValue = "id") String sort
   ) {
       Pageable pageable = PageRequest.of(page, size, Sort.by(sort));
       return repo.findAll(pageable);
   }
   ```

2. Prueba:
   - `GET /api/usuarios?page=0&size=5` - Primera página, 5 elementos
   - `GET /api/usuarios?page=1&size=5` - Segunda página
   - `GET /api/usuarios?sort=nombre` - Ordenado por nombre

**Respuesta esperada:**
```json
{
  "content": [...],
  "totalElements": 50,
  "totalPages": 10,
  "size": 5,
  "number": 0
}
```

---

#### Ejercicio 3.4: Manejo de excepciones personalizadas

**Tarea:** Crea excepciones personalizadas para errores de negocio.

**Pasos:**

1. Crea `ResourceNotFoundException.java`:
   ```java
   package com.curso.ut20.exception;

   public class ResourceNotFoundException extends RuntimeException {
       public ResourceNotFoundException(String message) {
           super(message);
       }
   }
   ```

2. En el servicio, lanza la excepción:
   ```java
   public Usuario buscarPorIdOFallar(Long id) {
       return repo.findById(id)
           .orElseThrow(() -> new ResourceNotFoundException(
               "Usuario no encontrado con ID: " + id
           ));
   }
   ```

3. En `GlobalExceptionHandler.java`, captura la excepción:
   ```java
   @ExceptionHandler(ResourceNotFoundException.class)
   public ResponseEntity<String> handleNotFound(ResourceNotFoundException ex) {
       return ResponseEntity.status(HttpStatus.NOT_FOUND).body(ex.getMessage());
   }
   ```

---

#### Ejercicio 3.5: Relación entre entidades (Avanzado)

**Tarea:** Crea una relación One-to-Many entre Usuario y Producto.

**Escenario:** Un usuario puede tener múltiples productos.

**Pasos:**

1. En `Usuario.java`, añade:
   ```java
   @OneToMany(mappedBy = "usuario", cascade = CascadeType.ALL)
   private List<Producto> productos = new ArrayList<>();
   ```

2. En `Producto.java`, añade:
   ```java
   @ManyToOne
   @JoinColumn(name = "usuario_id")
   private Usuario usuario;
   ```

3. Crea endpoint para obtener productos de un usuario:
   ```java
   @GetMapping("/{id}/productos")
   public List<Producto> obtenerProductosDeUsuario(@PathVariable Long id) {
       Usuario usuario = service.buscarPorIdOFallar(id);
       return usuario.getProductos();
   }
   ```

**Prueba:**
1. Crea un usuario
2. Crea productos asignándolos al usuario
3. Obtén los productos del usuario

---

### 📝 Nivel 4: Experto (Características Empresariales)

#### Ejercicio 4.1: Spring Security (Autenticación Básica)

**Tarea:** Añade seguridad básica a la API.

**Pasos:**

1. Añade dependencia en `pom.xml`:
   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-security</artifactId>
   </dependency>
   ```

2. Crea `SecurityConfig.java`:
   ```java
   @Configuration
   @EnableWebSecurity
   public class SecurityConfig {
       @Bean
       public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
           http
               .csrf().disable()
               .authorizeHttpRequests(auth -> auth
                   .requestMatchers("/api/productos/**").permitAll()
                   .anyRequest().authenticated()
               )
               .httpBasic();
           return http.build();
       }

       @Bean
       public UserDetailsService userDetailsService() {
           UserDetails user = User.builder()
               .username("admin")
               .password("{noop}admin123")
               .roles("ADMIN")
               .build();
           return new InMemoryUserDetailsManager(user);
       }
   }
   ```

3. Prueba:
   - `/api/productos` - Sin autenticación (permitAll)
   - `/api/usuarios` - Requiere autenticación (usuario: admin, contraseña: admin123)

---

#### Ejercicio 4.2: Tests Unitarios con JUnit y Mockito

**Tarea:** Crea tests para el servicio de usuarios.

**Pasos:**

1. Crea `UsuarioServiceTest.java` en `src/test/java`:
   ```java
   @ExtendWith(MockitoExtension.class)
   class UsuarioServiceTest {
       @Mock
       private UsuarioRepository repo;

       @InjectMocks
       private UsuarioService service;

       @Test
       void testListarTodos() {
           // Arrange
           List<Usuario> usuarios = Arrays.asList(
               new Usuario("Juan", 25),
               new Usuario("Ana", 30)
           );
           when(repo.findAll()).thenReturn(usuarios);

           // Act
           List<Usuario> resultado = service.listarTodos();

           // Assert
           assertEquals(2, resultado.size());
           verify(repo, times(1)).findAll();
       }

       @Test
       void testBuscarPorId() {
           Usuario usuario = new Usuario("Pedro", 28);
           when(repo.findById(1L)).thenReturn(Optional.of(usuario));

           Optional<Usuario> resultado = service.buscarPorId(1L);

           assertTrue(resultado.isPresent());
           assertEquals("Pedro", resultado.get().getNombre());
       }
   }
   ```

2. Ejecuta: `mvn test`

---

#### Ejercicio 4.3: Tests de Integración

**Tarea:** Crea tests que prueban toda la pila (controlador → servicio → repositorio → BD).

**Pasos:**

1. Crea `UsuarioControllerIntegrationTest.java`:
   ```java
   @SpringBootTest
   @AutoConfigureMockMvc
   class UsuarioControllerIntegrationTest {
       @Autowired
       private MockMvc mockMvc;

       @Autowired
       private ObjectMapper objectMapper;

       @Test
       void testCrearUsuario() throws Exception {
           Usuario usuario = new Usuario("Test", 25);

           mockMvc.perform(post("/api/usuarios")
                   .contentType(MediaType.APPLICATION_JSON)
                   .content(objectMapper.writeValueAsString(usuario)))
               .andExpect(status().isCreated())
               .andExpect(jsonPath("$.nombre").value("Test"))
               .andExpect(jsonPath("$.edad").value(25));
       }

       @Test
       void testValidacionNombreVacio() throws Exception {
           Usuario usuario = new Usuario("", 25);

           mockMvc.perform(post("/api/usuarios")
                   .contentType(MediaType.APPLICATION_JSON)
                   .content(objectMapper.writeValueAsString(usuario)))
               .andExpect(status().isBadRequest());
       }
   }
   ```

---

#### Ejercicio 4.4: Auditoría con JPA Auditing

**Tarea:** Añade campos de auditoría (createdAt, updatedAt).

**Pasos:**

1. Crea clase base `Auditable.java`:
   ```java
   @MappedSuperclass
   @EntityListeners(AuditingEntityListener.class)
   public abstract class Auditable {
       @CreatedDate
       private LocalDateTime createdAt;

       @LastModifiedDate
       private LocalDateTime updatedAt;

       // Getters...
   }
   ```

2. Haz que Usuario extienda Auditable:
   ```java
   @Entity
   public class Usuario extends Auditable {
       // ... campos existentes
   }
   ```

3. Activa auditoría en la clase principal:
   ```java
   @SpringBootApplication
   @EnableJpaAuditing
   public class Ut20Application {
       // ...
   }
   ```

4. Ahora cada entidad tendrá `createdAt` y `updatedAt` automáticamente.

---

#### Ejercicio 4.5: Caché con Spring Cache

**Tarea:** Mejora el rendimiento con caché.

**Pasos:**

1. Añade dependencia:
   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-cache</artifactId>
   </dependency>
   ```

2. Activa caché:
   ```java
   @SpringBootApplication
   @EnableCaching
   public class Ut20Application {
       // ...
   }
   ```

3. Añade anotaciones en el servicio:
   ```java
   @Cacheable("usuarios")
   public List<Usuario> listarTodos() {
       return repo.findAll();
   }

   @CacheEvict(value = "usuarios", allEntries = true)
   public Usuario guardar(Usuario usuario) {
       return repo.save(usuario);
   }
   ```

4. Prueba:
   - Primera llamada a `GET /api/usuarios` → Consulta BD
   - Segunda llamada → Retorna desde caché (más rápido)
   - Crear/actualizar usuario → Invalida caché

---

## 🧪 Testing con Swagger

### Paso a paso para probar la API

1. **Abre Swagger UI:** http://localhost:8080/swagger-ui/index.html

2. **Crear un Usuario:**
   - Expande `POST /api/usuarios`
   - Click en "Try it out"
   - Pega este JSON:
     ```json
     {
       "nombre": "María García",
       "edad": 28
     }
     ```
   - Click "Execute"
   - **Resultado esperado:** 201 Created

3. **Listar Usuarios:**
   - Expande `GET /api/usuarios`
   - Click "Execute"
   - **Resultado esperado:** Array con todos los usuarios

4. **Obtener un Usuario:**
   - Expande `GET /api/usuarios/{id}`
   - Introduce `id = 1`
   - Click "Execute"
   - **Resultado esperado:** 200 OK con el usuario

5. **Actualizar Usuario:**
   - Expande `PUT /api/usuarios/{id}`
   - Introduce `id = 1`
   - Cambia el JSON:
     ```json
     {
       "nombre": "María García López",
       "edad": 29
     }
     ```
   - Click "Execute"
   - **Resultado esperado:** 200 OK con datos actualizados

6. **Eliminar Usuario:**
   - Expande `DELETE /api/usuarios/{id}`
   - Introduce `id = 1`
   - Click "Execute"
   - **Resultado esperado:** 204 No Content

### Probar Validaciones

**Nombre vacío:**
```json
{
  "nombre": "",
  "edad": 25
}
```
**Resultado:** 400 Bad Request
```json
{
  "nombre": "El nombre del usuario es obligatorio"
}
```

**Edad negativa:**
```json
{
  "nombre": "Pedro",
  "edad": -5
}
```
**Resultado:** 400 Bad Request
```json
{
  "edad": "La edad debe ser mayor o igual a 0"
}
```

---

## 🗄️ Base de Datos H2

### Acceder a la Consola H2

1. URL: http://localhost:8080/h2-console
2. Configuración:
   - **JDBC URL:** `jdbc:h2:mem:ut20db`
   - **Usuario:** `sa`
   - **Contraseña:** *(vacío)*
3. Click "Connect"

### Consultas SQL Útiles

```sql
-- Ver todos los usuarios
SELECT * FROM usuario;

-- Ver todos los productos
SELECT * FROM producto;

-- Buscar usuarios mayores de 25 años
SELECT * FROM usuario WHERE edad > 25;

-- Contar usuarios
SELECT COUNT(*) FROM usuario;

-- Insertar usuario manualmente
INSERT INTO usuario (nombre, edad) VALUES ('Admin', 99);

-- Actualizar un usuario
UPDATE usuario SET edad = 30 WHERE id = 1;

-- Eliminar un usuario
DELETE FROM usuario WHERE id = 1;

-- Ver estructura de la tabla
SHOW COLUMNS FROM usuario;
```

### Ver logs de Hibernate (SQL generado)

Añade en `application.properties`:
```properties
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
```

Verás en consola cada operación SQL que ejecuta Hibernate.

---

## 🚀 Mejoras Sugeridas

### 🔒 Seguridad
- [ ] Implementar Spring Security con JWT
- [ ] Añadir roles (ADMIN, USER)
- [ ] Proteger endpoints sensibles
- [ ] Implementar rate limiting

### 📊 Base de Datos
- [ ] Migrar a PostgreSQL/MySQL
- [ ] Implementar Flyway/Liquibase para migraciones
- [ ] Añadir índices en campos buscados frecuentemente
- [ ] Configurar pool de conexiones

### 🧪 Testing
- [ ] Alcanzar 80%+ de cobertura de tests
- [ ] Tests de integración con Testcontainers
- [ ] Tests de carga con JMeter/Gatling

### 📈 Monitoreo
- [ ] Añadir Spring Boot Actuator
- [ ] Integrar Prometheus + Grafana
- [ ] Logs estructurados con Logback
- [ ] Añadir métricas personalizadas

### 🎨 Frontend
- [ ] Crear frontend con React/Angular/Vue
- [ ] Implementar CORS correctamente
- [ ] Añadir WebSockets para actualizaciones en tiempo real

### 🐳 DevOps
- [ ] Dockerizar la aplicación
- [ ] Crear pipeline CI/CD (GitHub Actions, Jenkins)
- [ ] Desplegar en AWS/Azure/Heroku
- [ ] Configurar perfiles (dev, staging, prod)

### 📚 Documentación
- [ ] Añadir OpenAPI annotations detalladas
- [ ] Crear Postman Collection
- [ ] Generar documentación con Spring REST Docs

---

## 📖 Recursos Adicionales

### Documentación Oficial
- [Spring Boot](https://spring.io/projects/spring-boot)
- [Spring Data JPA](https://spring.io/projects/spring-data-jpa)
- [Hibernate](https://hibernate.org/orm/documentation/)
- [Bean Validation](https://beanvalidation.org/)
- [OpenAPI/Swagger](https://swagger.io/specification/)

### Tutoriales Recomendados
- [Baeldung - Spring Boot](https://www.baeldung.com/spring-boot)
- [Spring Guides](https://spring.io/guides)
- [JPA Buddy](https://www.jpa-buddy.com/blog/)

---

## 🤝 Contribuir

¿Tienes ideas para mejorar este proyecto? ¡Contribuye!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📜 Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

---

## ✨ Créditos

**Proyecto educativo creado para enseñar Spring Boot de forma práctica y completa.**

Desarrollado con ❤️ para estudiantes de programación.

---

## 📞 Soporte

¿Tienes dudas o problemas?

- 📧 Email: tu-email@example.com
- 💬 Discord: [Tu servidor]
- 🐛 Issues: [GitHub Issues](https://github.com/tu-usuario/tu-repo/issues)

---

**¡Feliz aprendizaje! 🚀**
