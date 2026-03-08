# 📚 Guía de Proyectos — Curso Java Completo

> **Para el profesor:** Esta guía resume todos los proyectos del curso,  
> qué enseña cada uno, en qué orden presentarlos y su estado actual.  
> **Autor:** Joaquín Rodríguez Llanes | Última actualización: Febrero 2026

---

## 🗺️ Ruta de Aprendizaje (de menos a más)

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  1️⃣  proyecto-final-basico          ← Java puro, sin BD, consola   │
│         ↓  (+entidades, +relaciones, +validaciones avanzadas)       │
│  2️⃣  proyecto-final                 ← Java puro, sin BD, consola   │
│         ↓  (+JDBC, +Maven, +Testing, +arquitectura de capas)       │
│  3️⃣  UT19_ArquitecturaCapas_JDBC    ← Java + Maven + SQLite + JDBC  │
│         ↓  (+Spring Boot, +JPA, +Web, +Flyway, +Thymeleaf)         │
│  4️⃣  proyecto-final-sqlite-thymeleaf-jpa  ← App Web completa       │
│         ↓  (+API REST, +JSON, +Swagger, +H2)                       │
│  5️⃣  UT20_SpringBoot_API_REST_JPA   ← API REST profesional         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Tabla Comparativa

| Aspecto                  | basico | proyecto-final | UT19_JDBC | SpringBoot+Thymeleaf | UT20_API_REST |
|--------------------------|:------:|:--------------:|:---------:|:--------------------:|:-------------:|
| Nivel                    | ⭐      | ⭐⭐             | ⭐⭐⭐       | ⭐⭐⭐⭐                 | ⭐⭐⭐⭐          |
| Base de datos real       | ❌ CSV  | ❌ CSV          | ✅ SQLite  | ✅ SQLite             | ✅ H2 (mem.)  |
| Maven                    | ❌      | ❌              | ✅         | ✅                   | ✅            |
| Tests automáticos        | ❌      | ❌              | ✅ JUnit+Mockito | ✅ JUnit+Mockito | ❌ (ejercicio)|
| Spring Boot              | ❌      | ❌              | ❌         | ✅                   | ✅            |
| Interfaz de usuario      | Consola | Consola        | Consola   | Web HTML             | JSON/API REST |
| Thymeleaf                | ❌      | ❌              | ❌         | ✅                   | ❌            |
| Swagger/OpenAPI          | ❌      | ❌              | ❌         | ❌                   | ✅            |
| Logging profesional      | ❌      | ❌              | ✅ SLF4J   | ✅ SLF4J             | ✅ SLF4J      |
| Flyway (migraciones BD)  | ❌      | ❌              | ❌         | ✅                   | ❌            |
| DTOs / Forms             | ❌      | ❌              | ❌         | ✅ Forms              | ❌ (ejercicio)|
| Inyección dependencias   | Manual  | Manual         | Manual    | Automática Spring    | Automática Spring |
| Capa @Service            | ❌      | ❌              | ✅         | ✅                   | ✅            |
| Better Comments          | ✅      | ✅              | ✅         | ✅                   | ✅            |
| **EJERCICIOS.md con 📋 Prompts** | ✅ 10 | ✅ 12    | ✅ 8      | ✅ 10                | ✅ 8          |

---

## 1️⃣ `proyecto-final-basico` — Agenda de Citas

> **Cuándo usarlo:** Primera semana de proyectos. El alumno ya sabe POO básica
> pero nunca ha construido una aplicación completa.

### 🎯 Qué enseña

| Concepto | Cómo lo ve el alumno |
|----------|----------------------|
| **POO aplicada** | `Cliente`, `Cita` como clases reales |
| **Enums** | `EstadoCita`: PENDIENTE / REALIZADA / CANCELADA |
| **Colecciones** | `List<Cliente>`, `List<Cita>` en repositorios |
| **Fechas** | `LocalDate`, parseo `yyyy-MM-dd` con `DateUtils` |
| **Patrón MVC sencillo** | model → repository → controller → view |
| **Persistencia CSV** | `FileStorage` lee/escribe ficheros de texto |
| **Validaciones básicas** | Email, campos obligatorios en `Validator` |
| **Better Comments** | `// !` riesgo, `// *` flujo, `// ?` decisión, `// TODO` mejora |

### ✅ Estado: COMPLETO
- README con diagrama MVC, ruta de estudio y troubleshooting.
- EJERCICIOS.md: **10 ejercicios** con análisis técnico y **📋 cajita de prompt** en cada uno.
- Better Comments en todo el código.
- Menú completo: Clientes (listar/crear/borrar) + Citas (listar/crear/marcar/borrar).

---

## 2️⃣ `proyecto-final` — Gestor de Cursos

> **Cuándo usarlo:** Como proyecto integrador de los fundamentos Java.
> Consolida todo antes de entrar a Maven y bases de datos.

### 🎯 Qué enseña (cosas nuevas respecto al básico)

| Concepto | Cómo lo ve el alumno |
|----------|----------------------|
| **Dominio más complejo** | 3 entidades: Alumno, Curso, Matrícula |
| **Relaciones entre objetos** | Alumno 1:N Matrícula, Curso 1:N Matrícula |
| **UUIDs** | `UUID.randomUUID()` para IDs únicos |
| **Reglas de negocio** | Email único, fecha matrícula en rango del curso |
| **Validaciones con regex** | Formato email con `matches()` |
| **Enum con más estados** | `EstadoMatricula`: ACTIVA, ANULADA, FINALIZADA |
| **Tipo de curso** | `CursoTipo`: ONLINE, PRESENCIAL |
| **Precio y coherencia de fechas** | precio ≥ 0, fechaFin ≥ fechaInicio |

### ✅ Estado: COMPLETO
- README con diagrama MVC, tabla de reglas y ruta de estudio.
- EJERCICIOS.md: **12 ejercicios** con análisis técnico y **📋 cajita de prompt** en cada uno.
- Better Comments en todos los controllers.
- GUIA_Codex_Ensenanza.md integrada y eliminada (contenido en EJERCICIOS.md).

---

## 3️⃣ `UT19_ArquitecturaCapas_JDBC` — Arquitectura profesional con JDBC

> **Cuándo usarlo:** Unidad de transición. El alumno ya sabe Java puro
> y va a aprender Maven, bases de datos reales y testing.

### 🎯 Qué enseña (cosas nuevas respecto al proyecto-final)

| Concepto | Cómo lo ve el alumno |
|----------|----------------------|
| **Maven** | `pom.xml`, `mvn compile`, `mvn test` |
| **Base de datos real** | SQLite, fichero `.db`, tabla `usuarios` |
| **JDBC puro** | `DriverManager`, `PreparedStatement`, `ResultSet` |
| **SQL seguro** | `PreparedStatement` vs concatenación (SQL injection) |
| **Repository Pattern** | `UsuarioRepository` (interface) → `UsuarioRepositoryJdbc` (impl.) |
| **Service Layer** | `UsuarioService` con validaciones sin conocer JDBC |
| **Singleton** | `Db.java` con lazy initialization |
| **Testing** | JUnit 5 + Mockito |
| **Logging** | SLF4J + Logback |

### ✅ Estado: COMPLETO
- README con diagramas ASCII de capas.
- EJERCICIOS.md: **8 ejercicios** con análisis técnico y **📋 cajita de prompt** en cada uno.
- Better Comments en todas las clases.

---

## 4️⃣ `proyecto-final-sqlite-thymeleaf-jpa` — App Web completa

> **Cuándo usarlo:** Proyecto integrador de Spring Boot. El alumno ya
> entiende capas y JDBC. Ahora ve cómo Spring lo automatiza todo.

### 🎯 Qué enseña (cosas nuevas respecto a UT19)

| Concepto | Cómo lo ve el alumno |
|----------|----------------------|
| **Spring Boot** | Autoconfiguración, `@SpringBootApplication`, IoC |
| **Spring MVC (web)** | `@Controller`, rutas GET/POST, formularios HTML |
| **Thymeleaf** | Motor de plantillas: `th:each`, `th:text`, `th:action` |
| **Spring Data JPA** | Repositorios sin SQL, `JpaRepository<T, ID>` |
| **Bean Validation** | `@Valid`, `@NotBlank`, `@Email`, `BindingResult` |
| **Flyway** | `V1__init.sql`, `V2__seed.sql` — esquema versionado |
| **DTOs / Forms** | `AlumnoForm`, `CursoForm` vs entidades |
| **@ControllerAdvice** | Errores centralizados |
| **Doble barrera** | Reglas en Service Y en constraints SQL |
| **@EntityGraph** | Optimización de consultas N+1 |

### 📋 Reglas de negocio (doble barrera)

| # | Regla | Service | Constraint SQL |
|---|-------|---------|----------------|
| 1 | Email válido | `AlumnoService` | — |
| 2 | Email único | `AlumnoService` | `UNIQUE` |
| 3 | fechaFin ≥ fechaInicio | `CursoService` | `CHECK` |
| 4 | Precio ≥ 0 | Bean Validation | `CHECK` |
| 5 | Fecha matrícula en rango | `MatriculaService` | — |
| 6 | No duplicar ACTIVA | `MatriculaService` | Índice parcial |
| 7 | Borrado protegido | Services | FK RESTRICT |

### ✅ Estado: COMPLETO
- README completo con diagrama de arquitectura y troubleshooting.
- EJERCICIOS.md: **10 ejercicios** con análisis técnico y **📋 cajita de prompt** en cada uno.
- **23 archivos Java** con Better Comments aplicados (estilo UT7_CadenasTexto.java).
- Bugs corregidos: pom.xml (Flyway), GlobalExceptionHandler (código duplicado).
- Docs completos: guía docente, rúbrica, checklist, lectura guiada.

---

## 5️⃣ `UT20_SpringBoot_API_REST_JPA` — API REST profesional

> **Cuándo usarlo:** Después del proyecto Thymeleaf. El alumno ya conoce
> Spring Boot con vistas HTML. Ahora aprende APIs JSON.

### 🎯 Qué enseña (cosas nuevas respecto al proyecto Thymeleaf)

| Concepto | Cómo lo ve el alumno |
|----------|----------------------|
| **API REST** | HTTP verbs, códigos de estado, JSON |
| **@RestController** | `@Controller` + `@ResponseBody` automático |
| **ResponseEntity\<T\>** | Control total de la respuesta |
| **@RequestBody** | JSON → Objeto Java |
| **@PathVariable / @RequestParam** | Variables en URL y parámetros de consulta |
| **Swagger / OpenAPI** | Documentación automática e interactiva |
| **H2 en memoria** | BD que se reinicia con la app |
| **CRUD completo** | GET / POST / PUT / DELETE |

### ✅ Estado: COMPLETO
- README con endpoints y arquitectura.
- EJERCICIOS.md: **8 ejercicios** con análisis técnico y **📋 cajita de prompt** en cada uno.
- `@Service` creados (UsuarioService, ProductoService).
- Better Comments en todos los ficheros.
- `application.properties` comentado exhaustivamente.

---

## 💡 Consejos para usar estos proyectos en clase

### Orden de presentación recomendado

1. **Muestra primero** el proyecto más complejo (UT20 o Thymeleaf) para crear motivación.
2. **Construye desde abajo** empezando por `proyecto-final-basico`.
3. **Compara en paralelo**: cuando llegues a UT19, muestra cómo el Service hace lo mismo con diferente tecnología.
4. **Usa Swagger** (UT20) para que el alumno inspeccione APIs externas reales.

### Preguntas didácticas clave para el aula

- ¿Qué cambiaría si en el proyecto básico el CSV se corrompiera? ¿Y con una BD real?
- ¿Por qué en UT19 el `UsuarioService` no importa nada de `java.sql`?
- ¿Qué tiene que cambiar si en Thymeleaf queremos SQLite → PostgreSQL?
- ¿Por qué Swagger genera la documentación **automáticamente**?

### Extensiones de VS Code recomendadas

```
VS Code:
  - aaron-bond.better-comments   → colores en comentarios // ! // * // ? // TODO
  - vscjava.vscode-java-pack     → soporte Java completo
  - humao.rest-client            → probar APIs REST desde VS Code
```

---

## 📁 Estructura del curso

```
Curso java completo/
│
├── proyecto-final-basico/              ← 1️⃣ Java puro, consola, CSV
│   ├── src/com/curso/proyectobasico/
│   ├── EJERCICIOS.md                   ← ✅ 10 ejercicios con 📋 prompts
│   └── README.md                       ← ✅ Diagrama MVC, ruta de estudio
│
├── proyecto-final/                     ← 2️⃣ Java puro, consola, CSV (avanzado)
│   ├── src/com/curso/proyectofinal/
│   ├── EJERCICIOS.md                   ← ✅ 12 ejercicios con 📋 prompts
│   └── README.md                       ← ✅ Diagrama MVC, reglas de negocio
│
├── UT19_ArquitecturaCapas_JDBC/        ← 3️⃣ Maven + JDBC + SQLite + Tests
│   ├── src/main/java/com/curso/ut19/
│   ├── EJERCICIOS.md                   ← ✅ 8 ejercicios con 📋 prompts
│   └── README.md
│
├── proyecto-final-sqlite-thymeleaf-jpa/ ← 4️⃣ Spring Boot + Web + JPA + Flyway
│   ├── src/main/java/com/curso/pfsqlite/
│   ├── EJERCICIOS.md                   ← ✅ 10 ejercicios con 📋 prompts
│   └── README.md                       ← ✅ Completo con troubleshooting
│
├── UT20_SpringBoot_API_REST_JPA/       ← 5️⃣ Spring Boot + API REST + Swagger
│   ├── src/main/java/com/curso/ut20/
│   ├── EJERCICIOS.md                   ← ✅ 8 ejercicios con 📋 prompts
│   └── README.md
│
└── 📘_GUIA_PROYECTOS_JAVA.md           ← 📖 Este fichero
```

---

## ✅ Todo completado

| Proyecto | README | EJERCICIOS | 📋 Prompts | Better Comments | Bugs |
|---|---|---|---|---|---|
| proyecto-final-basico | ✅ | ✅ 10 | ✅ | ✅ | — |
| proyecto-final | ✅ | ✅ 12 | ✅ | ✅ | — |
| UT19_JDBC | ✅ | ✅ 8 | ✅ | ✅ | — |
| pf-sqlite-thymeleaf | ✅ | ✅ 10 | ✅ | ✅ 23 archivos | ✅ Corregidos |
| UT20_API_REST | ✅ | ✅ 8 | ✅ | ✅ | — |

**Total: 48 ejercicios con cajita de prompt** repartidos en 5 proyectos progresivos.

---

*Última actualización: Febrero 2026 — Curso Java Completo*
