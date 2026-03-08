# 📚 Proyecto Final — Spring Boot + SQLite + JPA + Thymeleaf

> **Proyecto didáctico** que simula una aplicación real de gestión de alumnos, cursos y matrículas.  
> Construido con arquitectura por capas, reglas de negocio en `service`, migraciones Flyway,  
> comentarios Better Comments y tests con Mockito + JUnit 5.  
> **Autor:** Joaquín Rodríguez Llanes | Uso educativo exclusivo.

---

## 🚀 Arranque rápido

```bash
# Windows (1 clic)
run-dev.bat

# Cualquier sistema operativo
./mvnw spring-boot:run          # Linux / Mac
mvnw.cmd spring-boot:run        # Windows
```

Abre **http://localhost:8080** cuando veas `Started Application`.

> 💡 Si quieres una demo limpia, borra `data/app.db` antes de arrancar.  
> Flyway lo recrea automáticamente con tablas y datos de ejemplo.

---

## 🛠️ Stack tecnológico

| Tecnología | Versión | Para qué se usa |
|---|---|---|
| Java | 17+ | Lenguaje base |
| Spring Boot | 3.3.5 | Framework web y de configuración |
| Thymeleaf | (via Spring Boot) | Motor de plantillas HTML |
| Spring Data JPA / Hibernate | (via Spring Boot) | ORM y acceso a datos |
| SQLite | 3.46 | Base de datos en fichero local (`data/app.db`) |
| Flyway | 10.x | Migraciones de esquema versionadas |
| Bean Validation | (via Spring Boot) | Validación de formularios con anotaciones |
| JUnit 5 + Mockito | (via Spring Boot) | Tests unitarios e integración |
| SLF4J | (via Spring Boot) | Logging profesional en servicios |

---

## 🏗️ Arquitectura por capas

```
Petición HTTP del navegador
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│  📁 web/  (Capa WEB)                                    │
│  *Controller.java     → valida formulario (@Valid)       │
│  GlobalExceptionHandler → captura errores globales       │
│  web/form/*.java      → DTOs de entrada (formularios)    │
└────────────────────────┬────────────────────────────────┘
                         │ delega lógica
                         ▼
┌─────────────────────────────────────────────────────────┐
│  📁 service/  (Capa de NEGOCIO)  ← AQUÍ van las reglas  │
│  AlumnoService, CursoService, MatriculaService           │
│  BusinessException, NotFoundException                    │
└────────────────────────┬────────────────────────────────┘
                         │ acceso a datos
                         ▼
┌─────────────────────────────────────────────────────────┐
│  📁 repository/  (Capa de DATOS)                         │
│  Spring Data JPA genera SQL automáticamente              │
│  @EntityGraph para evitar el problema N+1                │
└────────────────────────┬────────────────────────────────┘
                         │ JPA / Hibernate
                         ▼
┌─────────────────────────────────────────────────────────┐
│  📁 domain/  (Entidades JPA)                             │
│  Alumno, Curso, Matricula, CursoTipo, EstadoMatricula    │
└────────────────────────┬────────────────────────────────┘
                         │ SQL
                         ▼
              data/app.db  (SQLite)
              db/migration/V1__init.sql  (Flyway)
```

**🔑 Regla de oro:** si no sabes dónde va una regla, la respuesta es **`service`**.

---

## 📏 Reglas de negocio implementadas

| # | Regla | Dónde vive | Doble barrera |
|---|---|---|---|
| 1 | Email de alumno con formato válido (regex) | `AlumnoService` | — |
| 2 | Email de alumno único (sin importar mayúsculas) | `AlumnoService` | ✅ UNIQUE en BD |
| 3 | `fechaFin >= fechaInicio` en el curso | `CursoService` | ✅ CHECK en BD |
| 4 | Precio de curso >= 0 | — | ✅ CHECK en BD |
| 5 | Fecha de matrícula dentro del rango del curso | `MatriculaService` | — |
| 6 | No duplicado ACTIVA para mismo alumno+curso | `MatriculaService` | ✅ Índice parcial BD |
| 7 | No borrar alumno con matrículas ACTIVAS | `AlumnoService` | ✅ FK RESTRICT BD |
| 8 | No borrar curso con matrículas ACTIVAS | `CursoService` | ✅ FK RESTRICT BD |

> **Doble barrera** = validación en service (mensaje claro para el usuario) + restricción en BD (protección ante bugs o inserciones directas).

---

## 🌐 Rutas disponibles

| Método | URL | Qué hace |
|---|---|---|
| GET | `/` | Página de inicio |
| GET | `/alumnos` | Lista de alumnos |
| GET | `/alumnos/nuevo` | Formulario de alta |
| POST | `/alumnos` | Crear alumno |
| POST | `/alumnos/{id}/eliminar` | Borrar alumno (protegido) |
| GET | `/cursos` | Lista de cursos |
| GET | `/cursos/nuevo` | Formulario de alta |
| POST | `/cursos` | Crear curso |
| POST | `/cursos/{id}/eliminar` | Borrar curso (protegido) |
| GET | `/matriculas` | Lista de matrículas |
| GET | `/matriculas/nueva` | Formulario de alta |
| POST | `/matriculas` | Crear matrícula |
| POST | `/matriculas/{id}/anular` | Cambiar estado a ANULADA |
| POST | `/matriculas/{id}/eliminar` | Borrar matrícula físicamente |

---

## 🗄️ Base de datos y migraciones

- **Fichero:** `data/app.db` (SQLite, creado automáticamente al arrancar).
- **Migraciones** en `src/main/resources/db/migration`:

| Fichero | Contenido |
|---|---|
| `V1__init.sql` | Tablas, constraints CHECK, índices, índice parcial anti-duplicado ACTIVA |
| `V2__seed.sql` | Datos de ejemplo para clase |

> ⚠️ **Para cambiar el esquema**, crea siempre un fichero `V3__mi_cambio.sql`.  
> **Nunca** modifiques `V1` o `V2` después de haberlos ejecutado.  
> **Nunca** uses `ddl-auto=create` para cambios de esquema.

---

## 🧪 Tests incluidos

```
test/
  service/
    AlumnoServiceTest.java     → email único, email inválido, borrado protegido
    CursoServiceTest.java      → fechas inválidas, borrado protegido
    MatriculaServiceTest.java  → ventana temporal, duplicado ACTIVA, caso válido
  repository/
    MatriculaRepositoryTest.java → existsByAlumnoIdAndCursoIdAndEstado (BD real)
```

```bash
# Ejecutar todos los tests
mvnw.cmd test          # Windows
./mvnw test            # Linux / Mac
```

---

## 📂 Estructura de carpetas

```
proyecto-final-sqlite-thymeleaf-jpa/
├── data/                          ← app.db se crea aquí al arrancar
├── docs/                          ← documentación docente
├── src/
│   ├── main/
│   │   ├── java/com/curso/pfsqlite/
│   │   │   ├── Application.java   ← punto de entrada
│   │   │   ├── config/            ← configuración de arranque
│   │   │   ├── domain/            ← entidades JPA + enums
│   │   │   ├── repository/        ← Spring Data JPA (interfaces)
│   │   │   ├── service/           ← reglas de negocio + excepciones
│   │   │   └── web/               ← controllers + forms (DTOs)
│   │   └── resources/
│   │       ├── application.properties ← configuración Spring
│   │       ├── db/migration/      ← V1, V2... SQL versionado (Flyway)
│   │       ├── static/css/        ← estilos CSS
│   │       └── templates/         ← HTML Thymeleaf
│   └── test/
│       └── java/com/curso/pfsqlite/
│           ├── repository/        ← tests integración (@DataJpaTest)
│           └── service/           ← tests unitarios (Mockito)
├── EJERCICIOS.md                  ← 10 ejercicios con prompts para IA
├── README.md                      ← este archivo
├── pom.xml                        ← dependencias Maven
└── run-dev.bat                    ← arranque 1-clic Windows
```

---

## 🎨 Better Comments (colores en VS Code)

Instala la extensión **`aaron-bond.better-comments`** en VS Code para ver los colores:

| Prefijo | Color | Significado | Ejemplo |
|---|---|---|---|
| `// *` | 🟢 Verde | Explicación de flujo o teoría | `// * 🧠 TEORÍA: @Transactional...` |
| `// ?` | 🔵 Azul | Justificación técnica, pregunta didáctica | `// ? ¿Por qué BigDecimal y no double?` |
| `// !` | 🔴 Rojo | Regla crítica, advertencia, error a evitar | `// ! ⚠️ NUNCA exponer stack trace` |
| `// TODO` | 🟠 Naranja | Mejora futura o ejercicio pendiente | `// TODO: añadir campo teléfono` |

---

## 📖 Cómo estudiar este proyecto en clase

**Ruta de lectura recomendada (de menor a mayor complejidad):**

| Orden | Archivo | Qué aprendes |
|---|---|---|
| 1️⃣ | `Application.java` | Qué es `@SpringBootApplication` y cómo arranca Spring |
| 2️⃣ | `HomeController.java` | Routing MVC básico (GET → vista) |
| 3️⃣ | `AlumnoController.java` | CRUD completo con validación y redirect |
| 4️⃣ | `AlumnoService.java` | Reglas de negocio, Logger, @Transactional |
| 5️⃣ | `AlumnoRepository.java` | Consultas derivadas de Spring Data |
| 6️⃣ | `Alumno.java` | Entidad JPA, equals/hashCode, @Entity |
| 7️⃣ | `MatriculaService.java` | Servicio complejo con múltiples reglas |
| 8️⃣ | `GlobalExceptionHandler.java` | Manejo global de errores |
| 9️⃣ | `V1__init.sql` | Constraints, CHECK, índices en BD |
| 🔟 | `AlumnoServiceTest.java` | Tests unitarios con Mockito |

---

## ❓ Problemas frecuentes

| Problema | Solución |
|---|---|
| `mvnw.cmd` da error de `JAVA_HOME` | Configura `JAVA_HOME` apuntando a tu JDK 17+ |
| Puerto 8080 ocupado | Cambia `server.port=8081` en `application.properties` |
| Error de SQLite al arrancar | Borra `data/app.db` y reinicia (Flyway lo recrea) |
| Quiero cambiar el esquema BD | Crea `V3__mi_cambio.sql` en `db/migration/`, NO modifiques V1/V2 |
| Los tests fallan | Verifica que `target/test-repository.db` no esté bloqueado |
| `mvn` no reconocido | Usa `mvnw.cmd` (Maven Wrapper incluido en el proyecto) |
