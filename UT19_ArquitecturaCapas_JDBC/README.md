# 🏗️ UT19 - Arquitectura en Capas con JDBC

> **Proyecto educativo** que demuestra una arquitectura profesional en capas con JDBC, aplicando patrones de diseño y mejores prácticas para aplicaciones empresariales.

---

## 📋 Tabla de Contenidos

1. [Introducción](#-introducción)
2. [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
3. [Tecnologías Utilizadas](#-tecnologías-utilizadas)
4. [Patrones de Diseño](#-patrones-de-diseño)
5. [Configuración y Ejecución](#-configuración-y-ejecución)
6. [Estructura Detallada](#-estructura-detallada)
7. [Flujo de Datos](#-flujo-de-datos)
8. [Ejercicios Prácticos](#-ejercicios-prácticos)
9. [Testing](#-testing)
10. [Comparación con Spring Boot](#-comparación-con-spring-boot)
11. [Mejoras Sugeridas](#-mejoras-sugeridas)

---

## 🎯 Introducción

Este proyecto **refactoriza las prácticas UT17/UT18** aplicando una arquitectura profesional por capas. Es el puente perfecto entre JDBC básico y frameworks como Spring Boot.

### ¿Qué aprenderás?

✅ Arquitectura en capas (Layered Architecture)
✅ Repository Pattern para abstracción de datos
✅ Service Layer para lógica de negocio
✅ Dependency Injection manual
✅ Testing con JUnit 5 y Mockito
✅ Logging con SLF4J/Logback
✅ Gestión de proyectos con Maven
✅ Preparación para Spring Framework

---

## 🏗️ Arquitectura del Proyecto

```
┌─────────────────────────────────────────────────────────────┐
│                  CAPA DE PRESENTACIÓN (CLI)                  │
│                     Application.java                         │
│  - Menú interactivo                                          │
│  - Validación de entrada                                     │
│  - Formateo de salida                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE SERVICIO                           │
│                   UsuarioService.java                        │
│  - Validaciones de negocio                                   │
│  - Coordinación de operaciones                               │
│  - NO conoce detalles de persistencia                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                 CAPA DE REPOSITORIO                          │
│          UsuarioRepository (Interface/Puerto)                │
│  - Define el contrato de persistencia                        │
│  - Permite cambiar la implementación                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              IMPLEMENTACIÓN JDBC                             │
│            UsuarioRepositoryJdbc.java                        │
│  - PreparedStatements (seguridad SQL)                        │
│  - Mapeo ResultSet → Usuario                                 │
│  - Try-with-resources                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                 CAPA DE PERSISTENCIA                         │
│                       Db.java                                │
│  - Gestión de conexión (Singleton)                           │
│  - Creación de esquema                                       │
│  - Configuración SQLite                                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    BASE DE DATOS                             │
│                 SQLite (miBaseDatos.db)                      │
│  - Tabla: usuarios (id, nombre, edad)                        │
└─────────────────────────────────────────────────────────────┘
```

### Ventajas de esta arquitectura:

1. **Separación de responsabilidades** - Cada capa tiene un propósito claro
2. **Testabilidad** - Puedes mockear cualquier capa
3. **Mantenibilidad** - Cambios en una capa no afectan a las demás
4. **Escalabilidad** - Fácil añadir nuevas entidades
5. **Reutilización** - El servicio puede usarse desde Web, API REST, etc.

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Java** | 17 | Lenguaje de programación |
| **Maven** | 3.6+ | Gestión de dependencias y build |
| **JDBC** | - | API de acceso a bases de datos |
| **SQLite** | 3.45.3 | Base de datos embebida |
| **SLF4J** | 2.0.13 | Facade de logging |
| **Logback** | 1.5.6 | Implementación de logging |
| **JUnit 5** | 5.10.2 | Framework de testing |
| **Mockito** | 5.12.0 | Framework de mocking |

---

## 🎨 Patrones de Diseño

### 1. Repository Pattern

```java
// Interface (Puerto) - Define el contrato
public interface UsuarioRepository {
    Usuario save(Usuario u);
    Optional<Usuario> findById(int id);
    List<Usuario> findAll();
    boolean update(Usuario u);
    boolean delete(int id);
}

// Implementación JDBC (Adaptador)
public class UsuarioRepositoryJdbc implements UsuarioRepository {
    // Implementación con PreparedStatements
}
```

**Beneficios:**
- Abstrae el mecanismo de persistencia
- Permite cambiar de JDBC a JPA sin modificar el servicio
- Facilita el testing con mocks

---

### 2. Service Layer

```java
public class UsuarioService {
    private final UsuarioRepository repository;

    // Inyección de dependencias por constructor
    public UsuarioService(UsuarioRepository repository) {
        this.repository = repository;
    }

    public Usuario crear(String nombre, int edad) {
        validar(nombre, edad); // Lógica de negocio
        return repository.save(new Usuario(nombre, edad));
    }
}
```

**Beneficios:**
- Centraliza la lógica de negocio
- Aplica validaciones antes de persistir
- Coordina operaciones entre repositorios

---

### 3. Dependency Injection (Manual)

```java
// Wiring manual en Application.java
UsuarioRepository repo = new UsuarioRepositoryJdbc();
UsuarioService service = new UsuarioService(repo);
```

**Beneficios:**
- Bajo acoplamiento
- Facilita el testing
- Prepara para frameworks IoC (Spring)

---

### 4. Singleton (Conexión BD)

```java
public class Db {
    private static Connection connection;

    public static Connection getConnection() {
        if (connection == null) {
            // Lazy initialization
            connection = DriverManager.getConnection("...");
        }
        return connection;
    }
}
```

**Beneficios:**
- Una única conexión compartida
- Lazy initialization (se crea solo cuando se necesita)

---

## ⚙️ Configuración y Ejecución

### Prerrequisitos

- Java 17 o superior
- Maven 3.6+
- IDE (IntelliJ IDEA, Eclipse, VSCode)

### Pasos para ejecutar

1. **Clonar o descargar el proyecto**

2. **Compilar**
   ```bash
   mvn clean compile
   ```

3. **Ejecutar**
   ```bash
   mvn exec:java -Dexec.mainClass="com.curso.ut19.Application"
   ```

   O desde tu IDE: ejecutar `Application.java`

4. **Ejecutar tests**
   ```bash
   mvn test
   ```

### Archivo generado

Al ejecutar, se crea `miBaseDatos.db` en la raíz del proyecto (base de datos SQLite).

---

## 📁 Estructura Detallada

### Estructura de Carpetas

```
UT19_ArquitecturaCapas_JDBC/
├── pom.xml                           # Configuración Maven
├── miBaseDatos.db                    # Base de datos SQLite (generado)
│
├── src/main/java/com/curso/ut19/
│   ├── Application.java              # CLI - Capa de presentación
│   │
│   ├── model/                        # Entidades de dominio
│   │   └── Usuario.java             # POJO Usuario
│   │
│   ├── persistence/                  # Gestión de conexión
│   │   └── Db.java                  # Singleton de Connection
│   │
│   ├── repository/                   # Abstracción de persistencia
│   │   ├── UsuarioRepository.java   # Interface (Puerto)
│   │   └── jdbc/
│   │       └── UsuarioRepositoryJdbc.java # Implementación JDBC
│   │
│   ├── service/                      # Lógica de negocio
│   │   └── UsuarioService.java      # Servicio con validaciones
│   │
│   └── util/                         # Utilidades
│       └── Validator.java           # Validaciones reutilizables
│
├── src/main/resources/
│   └── logback.xml                   # Configuración de logging
│
└── src/test/java/com/curso/ut19/
    └── service/
        └── UsuarioServiceTest.java  # Tests con JUnit + Mockito
```

---

## 🔄 Flujo de Datos

### Ejemplo: Crear un Usuario

```
1. Usuario escribe: "Juan", 25
   ↓
2. Application.insertar()
   - Valida que el nombre no esté vacío (UI)
   - Llama a service.crear("Juan", 25)
   ↓
3. UsuarioService.crear()
   - Valida reglas de negocio (nombre no vacío, edad >= 0)
   - Crea: new Usuario("Juan", 25)
   - Llama a repository.save(usuario)
   ↓
4. UsuarioRepositoryJdbc.save()
   - Crea PreparedStatement: INSERT INTO usuarios...
   - Ejecuta INSERT
   - Obtiene ID generado
   - Asigna ID al objeto Usuario
   - Retorna Usuario con ID
   ↓
5. UsuarioService retorna Usuario
   ↓
6. Application muestra: "✅ Insertado con ID: 1"
```

### SQL Generado

```sql
INSERT INTO usuarios(nombre, edad) VALUES('Juan', 25)
-- Retorna ID autogenerado: 1
```

---

## 🎓 Ejercicios Prácticos

### 📝 Nivel 1: Básico (Familiarización)

#### Ejercicio 1.1: Ejecutar y Probar

1. Ejecuta la aplicación
2. Inserta 3 usuarios
3. Lista todos los usuarios
4. Actualiza uno por ID
5. Elimina uno
6. Cierra la aplicación

**Objetivo:** Familiarizarte con el flujo CRUD completo.

---

#### Ejercicio 1.2: Explorar la Base de Datos

1. Instala [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Abre `miBaseDatos.db`
3. Explora la tabla `usuarios`
4. Ejecuta consultas SQL:
   ```sql
   SELECT * FROM usuarios;
   SELECT * FROM usuarios WHERE edad > 25;
   INSERT INTO usuarios (nombre, edad) VALUES ('Test', 30);
   ```
5. Verifica desde la aplicación

**Objetivo:** Entender que JDBC trabaja sobre SQL real.

---

#### Ejercicio 1.3: Provocar Errores de Validación

1. Intenta crear usuario con nombre vacío
2. Intenta crear usuario con edad negativa
3. Analiza los mensajes de error

**¿Qué capa lanza la excepción?** UsuarioService

**Objetivo:** Comprender el flujo de validaciones.

---

### 📝 Nivel 2: Intermedio (Extensión)

#### Ejercicio 2.1: Añadir campo `email` a Usuario

**Tarea:** Extiende la entidad Usuario con un campo email.

**Pasos:**

1. Modifica `Usuario.java`:
   ```java
   private String email;
   // Añadir getter y setter
   ```

2. Modifica `Db.java` (esquema):
   ```sql
   CREATE TABLE IF NOT EXISTS usuarios (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       nombre TEXT NOT NULL,
       edad INTEGER NOT NULL CHECK(edad >= 0),
       email TEXT UNIQUE  -- NUEVO CAMPO
   )
   ```

3. Modifica `UsuarioRepositoryJdbc.java`:
   - `save()`: añadir email al INSERT
   - `update()`: añadir email al UPDATE
   - `map()`: leer email del ResultSet

4. Modifica `UsuarioService.java`:
   - `crear()`: añadir parámetro email
   - `actualizar()`: añadir parámetro email
   - `validar()`: validar formato de email

5. Modifica `Application.java`:
   - Solicitar email en `insertar()` y `actualizar()`

6. Elimina `miBaseDatos.db` y reinicia la aplicación

**Validación extra:**
```java
if (!email.matches("^[A-Za-z0-9+_.-]+@(.+)$")) {
    throw new IllegalArgumentException("Email inválido");
}
```

---

#### Ejercicio 2.2: Implementar búsqueda por nombre

**Tarea:** Añade funcionalidad para buscar usuarios por nombre (búsqueda exacta).

**Pasos:**

1. En `UsuarioRepository.java`, añade:
   ```java
   List<Usuario> findByNombre(String nombre);
   ```

2. En `UsuarioRepositoryJdbc.java`, implementa:
   ```java
   @Override
   public List<Usuario> findByNombre(String nombre) {
       String sql = "SELECT * FROM usuarios WHERE nombre = ?";
       List<Usuario> lista = new ArrayList<>();
       try (PreparedStatement ps = Db.getConnection().prepareStatement(sql)) {
           ps.setString(1, nombre);
           try (ResultSet rs = ps.executeQuery()) {
               while (rs.next()) lista.add(map(rs));
           }
           return lista;
       } catch (SQLException e) {
           log.error("Error buscando por nombre", e);
           throw new RuntimeException(e);
       }
   }
   ```

3. En `UsuarioService.java`:
   ```java
   public List<Usuario> buscarPorNombre(String nombre) {
       return repository.findByNombre(nombre);
   }
   ```

4. En `Application.java`, añade opción al menú (opción 6):
   ```java
   case 6 -> buscarPorNombre(service);
   ```

   Y el método:
   ```java
   private static void buscarPorNombre(UsuarioService service) {
       String nombre = readNonEmpty("Nombre a buscar: ");
       List<Usuario> usuarios = service.buscarPorNombre(nombre);
       if (usuarios.isEmpty()) {
           System.out.println("No se encontraron usuarios");
       } else {
           listarUsuarios(usuarios); // Reutilizar lógica de listar
       }
   }
   ```

**Bonus:** Implementa búsqueda parcial con `LIKE`:
```sql
SELECT * FROM usuarios WHERE nombre LIKE ?
```
```java
ps.setString(1, "%" + nombre + "%");
```

---

#### Ejercicio 2.3: Añadir entidad Producto

**Tarea:** Replica toda la arquitectura para una nueva entidad Producto.

**Entidad Producto:**
- id: Integer (PRIMARY KEY AUTOINCREMENT)
- nombre: String (NOT NULL)
- precio: double (CHECK precio >= 0)
- stock: int (CHECK stock >= 0)

**Pasos:**

1. Crea `Producto.java` en `model/`
2. Crea `ProductoRepository.java` en `repository/`
3. Crea `ProductoRepositoryJdbc.java` en `repository/jdbc/`
4. Crea `ProductoService.java` en `service/`
5. Modifica `Db.java` para crear tabla productos
6. Añade opciones al menú de `Application.java`

**Validaciones de negocio:**
- Nombre no vacío
- Precio >= 0
- Stock >= 0

---

### 📝 Nivel 3: Avanzado (Optimización)

#### Ejercicio 3.1: Implementar Pool de Conexiones

**Tarea:** Cambia de Singleton a HikariCP (pool de conexiones).

**¿Por qué?**
- Singleton mantiene 1 conexión abierta (no escalable)
- Pool mantiene múltiples conexiones reutilizables
- HikariCP es el pool más rápido y usado

**Pasos:**

1. Añade dependencia en `pom.xml`:
   ```xml
   <dependency>
       <groupId>com.zaxxer</groupId>
       <artifactId>HikariCP</artifactId>
       <version>5.1.0</version>
   </dependency>
   ```

2. Modifica `Db.java`:
   ```java
   import com.zaxxer.hikari.HikariConfig;
   import com.zaxxer.hikari.HikariDataSource;

   public class Db {
       private static HikariDataSource dataSource;

       public static Connection getConnection() throws SQLException {
           if (dataSource == null) {
               HikariConfig config = new HikariConfig();
               config.setJdbcUrl("jdbc:sqlite:miBaseDatos.db");
               config.setMaximumPoolSize(10);
               dataSource = new HikariDataSource(config);
           }
           return dataSource.getConnection();
       }

       public static void close() {
           if (dataSource != null) {
               dataSource.close();
           }
       }
   }
   ```

---

#### Ejercicio 3.2: Implementar Transacciones

**Tarea:** Añade soporte para transacciones en operaciones complejas.

**Escenario:** Transferir stock de un producto a otro (operación atómica).

**Pasos:**

1. Crea método en `ProductoService.java`:
   ```java
   public void transferirStock(int idOrigen, int idDestino, int cantidad) {
       Connection conn = null;
       try {
           conn = Db.getConnection();
           conn.setAutoCommit(false); // Iniciar transacción

           // 1. Restar stock del origen
           Producto origen = repository.findById(idOrigen)
               .orElseThrow(() -> new IllegalArgumentException("Origen no encontrado"));
           if (origen.getStock() < cantidad) {
               throw new IllegalArgumentException("Stock insuficiente");
           }
           origen.setStock(origen.getStock() - cantidad);
           repository.update(origen);

           // 2. Sumar stock al destino
           Producto destino = repository.findById(idDestino)
               .orElseThrow(() -> new IllegalArgumentException("Destino no encontrado"));
           destino.setStock(destino.getStock() + cantidad);
           repository.update(destino);

           conn.commit(); // Confirmar transacción
       } catch (Exception e) {
           if (conn != null) {
               try {
                   conn.rollback(); // Revertir cambios
               } catch (SQLException ex) {
                   log.error("Error en rollback", ex);
               }
           }
           throw new RuntimeException("Error en transferencia", e);
       } finally {
           if (conn != null) {
               try {
                   conn.setAutoCommit(true);
               } catch (SQLException e) {
                   log.error("Error restaurando autoCommit", e);
               }
           }
       }
   }
   ```

---

#### Ejercicio 3.3: Añadir Relaciones 1:N

**Tarea:** Implementa relación Usuario 1:N Producto (un usuario tiene muchos productos).

**Cambios necesarios:**

1. Añade campo `usuario_id` a la tabla productos:
   ```sql
   CREATE TABLE productos (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       nombre TEXT NOT NULL,
       precio REAL NOT NULL CHECK(precio >= 0),
       stock INTEGER NOT NULL CHECK(stock >= 0),
       usuario_id INTEGER,
       FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
   )
   ```

2. Añade campo en `Producto.java`:
   ```java
   private Integer usuarioId;
   ```

3. Añade método en `ProductoRepository`:
   ```java
   List<Producto> findByUsuarioId(int usuarioId);
   ```

4. Implementa en `ProductoRepositoryJdbc`:
   ```java
   public List<Producto> findByUsuarioId(int usuarioId) {
       String sql = "SELECT * FROM productos WHERE usuario_id = ?";
       // ... implementación similar a findAll()
   }
   ```

5. Añade método en `Application.java`:
   ```java
   private static void listarProductosDeUsuario(ProductoService productoService) {
       System.out.print("ID del usuario: ");
       int usuarioId = readInt();
       List<Producto> productos = productoService.buscarPorUsuarioId(usuarioId);
       // Mostrar productos
   }
   ```

---

### 📝 Nivel 4: Experto (Arquitectura Avanzada)

#### Ejercicio 4.1: Migrar a PostgreSQL

**Tarea:** Cambia de SQLite a PostgreSQL.

**Pasos:**

1. Instala PostgreSQL
2. Añade dependencia en `pom.xml`:
   ```xml
   <dependency>
       <groupId>org.postgresql</groupId>
       <artifactId>postgresql</artifactId>
       <version>42.7.2</version>
   </dependency>
   ```

3. Modifica `Db.java`:
   ```java
   Class.forName("org.postgresql.Driver");
   connection = DriverManager.getConnection(
       "jdbc:postgresql://localhost:5432/ut19db",
       "postgres",
       "password"
   );
   ```

4. Ajusta el esquema SQL (PostgreSQL usa SERIAL en lugar de AUTOINCREMENT)

**Beneficio:** Sin cambios en el código de negocio (gracias al Repository Pattern).

---

#### Ejercicio 4.2: Implementar DAO Genérico

**Tarea:** Crea un DAO base reutilizable para todas las entidades.

**Pasos:**

1. Crea interface genérica:
   ```java
   public interface GenericRepository<T, ID> {
       T save(T entity);
       Optional<T> findById(ID id);
       List<T> findAll();
       boolean update(T entity);
       boolean delete(ID id);
   }
   ```

2. Implementación base:
   ```java
   public abstract class JdbcRepository<T, ID> implements GenericRepository<T, ID> {
       protected abstract String getTableName();
       protected abstract T map(ResultSet rs) throws SQLException;
       protected abstract void setInsertParams(PreparedStatement ps, T entity) throws SQLException;

       @Override
       public List<T> findAll() {
           String sql = "SELECT * FROM " + getTableName();
           // Implementación genérica
       }
   }
   ```

3. Extiende en `UsuarioRepositoryJdbc`:
   ```java
   public class UsuarioRepositoryJdbc extends JdbcRepository<Usuario, Integer> {
       @Override
       protected String getTableName() { return "usuarios"; }

       @Override
       protected Usuario map(ResultSet rs) throws SQLException {
           // Mapeo específico
       }
   }
   ```

---

#### Ejercicio 4.3: Tests de Integración con H2

**Tarea:** Crea tests de integración que usan H2 en memoria.

**¿Por qué H2?**
- Base de datos en memoria (rápida)
- Compatible con JDBC
- No requiere instalación

**Pasos:**

1. Añade dependencia:
   ```xml
   <dependency>
       <groupId>com.h2database</groupId>
       <artifactId>h2</artifactId>
       <version>2.2.224</version>
       <scope>test</scope>
   </dependency>
   ```

2. Crea `UsuarioRepositoryIntegrationTest.java`:
   ```java
   @BeforeEach
   void setUp() throws SQLException {
       // Configurar H2
       connection = DriverManager.getConnection("jdbc:h2:mem:test");
       // Crear esquema
       connection.createStatement().execute(
           "CREATE TABLE usuarios (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255), edad INT)"
       );
   }

   @Test
   void testSaveAndFindById() {
       UsuarioRepositoryJdbc repo = new UsuarioRepositoryJdbc();
       Usuario u = repo.save(new Usuario("Test", 25));

       assertNotNull(u.getId());
       Optional<Usuario> found = repo.findById(u.getId());
       assertTrue(found.isPresent());
       assertEquals("Test", found.get().getNombre());
   }
   ```

---

## 🧪 Testing

### Estructura de Tests

```
src/test/java/com/curso/ut19/
└── service/
    └── UsuarioServiceTest.java
```

### Ejemplo de Test con Mockito

```java
@Test
void crearDebeValidarNombreYEdad() {
    // Arrange - Preparar
    UsuarioRepository repo = Mockito.mock(UsuarioRepository.class);
    UsuarioService service = new UsuarioService(repo);

    // Act & Assert - Actuar y Verificar
    assertThrows(IllegalArgumentException.class,
        () -> service.crear("", 10)); // Nombre vacío

    assertThrows(IllegalArgumentException.class,
        () -> service.crear("Ana", -1)); // Edad negativa
}
```

### Ejecutar Tests

```bash
mvn test
```

**Salida esperada:**
```
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0
```

---

## 🆚 Comparación con Spring Boot

| Concepto | UT19 (Manual) | Spring Boot |
|----------|---------------|-------------|
| **Inyección de dependencias** | Manual en Application | @Autowired automático |
| **Repositorios** | Interface + Implementación JDBC | @Repository + Spring Data JPA |
| **Servicios** | Clase con constructor injection | @Service con @Autowired |
| **Transacciones** | Manual con Connection | @Transactional |
| **Configuración BD** | Hardcoded en Db.java | application.properties |
| **Logging** | SLF4J + Logback manual | Autoconfigured |
| **Testing** | JUnit + Mockito manual | @SpringBootTest |

### Evolución natural:

```
UT19 (JDBC + Manual DI)
    ↓
Spring Core (IoC Container)
    ↓
Spring Boot + Spring Data JPA
```

---

## 🚀 Mejoras Sugeridas

### 🔒 Seguridad
- [ ] Validación de SQL Injection (ya implementado con PreparedStatements)
- [ ] Escapado de entrada de usuario
- [ ] Hasheo de contraseñas (si añades campo password)

### 📊 Base de Datos
- [ ] Migrar a PostgreSQL/MySQL
- [ ] Implementar pool de conexiones (HikariCP)
- [ ] Añadir índices en campos buscados frecuentemente
- [ ] Implementar migraciones (Flyway/Liquibase)

### 🧪 Testing
- [ ] Tests de integración con H2
- [ ] Aumentar cobertura de tests
- [ ] Tests de rendimiento

### 📈 Funcionalidades
- [ ] Paginación en listados
- [ ] Ordenación configurable
- [ ] Búsqueda avanzada (múltiples criterios)
- [ ] Exportar datos a CSV/JSON

### 🎨 Arquitectura
- [ ] Implementar DTOs separados del modelo
- [ ] Añadir capa de Mappers (ModelMapper, MapStruct)
- [ ] Implementar eventos de dominio
- [ ] Añadir caché (Caffeine, Redis)

### 📚 Documentación
- [ ] JavaDoc completo en todos los métodos públicos
- [ ] Diagramas UML de clases y secuencia
- [ ] Manual de usuario

---

## 📖 Recursos Adicionales

### Conceptos Clave

- **[Layered Architecture](https://www.baeldung.com/cs/layered-architecture)** - Arquitectura en capas
- **[Repository Pattern](https://www.baeldung.com/java-repository-pattern)** - Patrón repositorio
- **[Dependency Injection](https://www.baeldung.com/inversion-control-and-dependency-injection-in-spring)** - Inyección de dependencias
- **[JDBC Best Practices](https://www.baeldung.com/java-jdbc)** - Mejores prácticas JDBC

### Herramientas

- **[DB Browser for SQLite](https://sqlitebrowser.org/)** - Explorador de bases de datos SQLite
- **[Maven](https://maven.apache.org/)** - Gestión de proyectos
- **[Logback](https://logback.qos.ch/)** - Logging
- **[JUnit 5](https://junit.org/junit5/)** - Testing
- **[Mockito](https://site.mockito.org/)** - Mocking

---

## 🤝 Contribuir

¿Tienes ideas para mejorar este proyecto? ¡Contribuye!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Añade mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

---

## 📜 Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

---

## ✨ Créditos

**Proyecto educativo creado para enseñar arquitectura en capas y preparar para Spring Framework.**

Desarrollado con ❤️ para estudiantes de programación.

---

**¡Feliz aprendizaje! 🚀**

*Este proyecto es el puente perfecto entre JDBC básico y Spring Boot profesional.*
