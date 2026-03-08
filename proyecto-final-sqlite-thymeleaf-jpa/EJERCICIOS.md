# 🏋️ EJERCICIOS PRÁCTICOS — Proyecto Final SQLite + Thymeleaf + JPA

> **Autor:** Joaquín Rodríguez Llanes  
> **Nivel:** Spring Boot Intermedio-Avanzado  
> **Tiempo total estimado:** 8–12 horas  
> **Prerrequisitos:** UT19 y UT20 completados. Conocimientos de SQL, JPA, HTML básico.

> 💡 **Cómo usar estos ejercicios:**  
> Cada ejercicio incluye un **análisis técnico completo** que explica QUÉ hay que hacer y POR QUÉ.  
> Al final de cada uno hay una **📋 Cajita de Prompt** lista para copiar y enviar a una IA  
> (Gemini, ChatGPT, etc.) si quieres que lo implemente automáticamente.  
> **Recomendación:** intenta hacerlo tú primero. Si te atascas, usa el prompt.

---

## 📋 Índice de Ejercicios

| # | Ejercicio | Nivel | Tiempo | Capas que toca |
|---|-----------|-------|--------|----------------|
| 1 | Explorar el proyecto y responder preguntas | ⭐ Básico | 20 min | Todas (lectura) |
| 2 | Entender las migraciones Flyway | ⭐ Básico | 30 min | BD / Config |
| 3 | Añadir campo `telefono` al Alumno | ⭐⭐ Intermedio | 60 min | BD → Domain → Form → Service → Vista |
| 4 | Filtro de cursos por tipo (ONLINE/PRESENCIAL) | ⭐⭐ Intermedio | 45 min | Repository → Service → Controller → Vista |
| 5 | Dashboard con estadísticas en el Home | ⭐⭐ Intermedio | 45 min | Repository → Controller → Vista |
| 6 | Editar un alumno existente | ⭐⭐⭐ Avanzado | 90 min | Repository → Service → Controller → Vista |
| 7 | Validar transiciones de estado en matrículas | ⭐⭐⭐ Avanzado | 45 min | Service |
| 8 | Paginación en el listado de matrículas | ⭐⭐⭐ Avanzado | 60 min | Repository → Service → Controller → Vista |
| 9 | Exportar listado de alumnos a CSV | ⭐⭐⭐ Avanzado | 60 min | Service → Controller |
| 10 | Tests de integración con @SpringBootTest | ⭐⭐⭐ Avanzado | 60 min | Test |

---

## ⭐ EJERCICIO 1 — Explorar el proyecto (básico)

### 🎯 Objetivo
Comprender la relación entre capas: **Controller → Service → Repository → BD**.

### 📖 Análisis
Este ejercicio no requiere escribir código. El objetivo es **navegar y entender** cómo está conectado todo antes de modificar nada.

### ✅ Pasos
1. Arranca la aplicación con `run-dev.bat` o `mvnw.cmd spring-boot:run`.
2. Abre `http://localhost:8080` en el navegador.
3. Navega por todas las secciones: **Alumnos**, **Cursos**, **Matrículas**.
4. Crea **2 alumnos**, **1 curso** y **1 matrícula**.
5. Intenta borrar un alumno que tenga una matrícula activa → observa el mensaje de error.
6. Anula la matrícula → ahora intenta borrar el alumno otra vez → debería funcionar.

### 🧠 Preguntas para responder
1. ¿En qué archivo se genera la tabla HTML de alumnos? *(pista: busca `th:each` en los `.html`)*
2. ¿Qué hace `@Transactional(readOnly = true)` en el servicio?
3. ¿Cuál es la diferencia entre **Anular** y **Eliminar** una matrícula?
4. ¿En qué fichero SQL se define la estructura de las tablas? *(pista: `resources/db/migration/`)*
5. ¿Por qué `AlumnoController` NO comprueba si el email ya existe? ¿Quién lo hace?
6. ¿Qué pasaría si borramos el `GlobalExceptionHandler`? ¿Qué vería el usuario?

---

## ⭐ EJERCICIO 2 — Entender las migraciones Flyway (básico)

### 🎯 Objetivo
Comprender cómo **Flyway gestiona el esquema de BD** de forma versionada y segura.

### 📖 Análisis
En proyectos reales, la base de datos evoluciona con el tiempo (nuevos campos, nuevas tablas). Si cada desarrollador modifica la BD manualmente, se producen inconsistencias. **Flyway** resuelve esto: cada cambio de esquema es un fichero SQL con versión (`V1__`, `V2__`, etc.) que se ejecuta automáticamente y EN ORDEN.

### ✅ Pasos
1. Abre `src/main/resources/db/migration/` y lee los ficheros `V1__init.sql` y `V2__seed.sql`.
2. Arranca la app y abre la base de datos `data/app.db` con cualquier visor SQLite.
3. Ejecuta: `SELECT * FROM flyway_schema_history;` → verás el registro de migraciones.
4. **Mini-ejercicio:** Crea un fichero `V3__añadir_observaciones_curso.sql` con este contenido:
   ```sql
   ALTER TABLE cursos ADD COLUMN observaciones TEXT;
   ```
5. Reinicia la app. Verifica que la columna se ha creado en la tabla `cursos`.

### 🧠 Preguntas para responder
1. ¿Qué pasa si cambias el contenido de una migración ya aplicada (ej: V1)?
2. ¿Por qué los ficheros se llaman `V1__` con **doble guion bajo**?
3. ¿Qué ventaja tiene Flyway sobre `ddl-auto=update` de Hibernate?
4. ¿Qué ocurre si creas `V3__` sin que exista `V2__`?

---

## ⭐⭐ EJERCICIO 3 — Añadir campo `telefono` al Alumno (intermedio)

### 🎯 Objetivo
Practicar el **ciclo completo** de un cambio: migración → entidad → form → servicio → vista.

### 📖 Análisis técnico

| Capa | Archivo a modificar | Qué hacer |
|------|---------------------|-----------|
| **BD** | `V4__añadir_telefono.sql` | Crear migración con `ALTER TABLE` |
| **Domain** | `Alumno.java` | Añadir campo `telefono` + getter/setter |
| **Form** | `AlumnoForm.java` | Añadir campo con `@Size(max=20)` |
| **Service** | `AlumnoService.java` | Pasar `form.getTelefono()` a la entidad en el método `crear()` |
| **Vista** | `alumnos/nuevo.html` | Añadir input de texto para teléfono |
| **Vista** | `alumnos/lista.html` | Añadir columna "Teléfono" en la tabla |

### 🧠 Decisiones de diseño a tener en cuenta
- El teléfono es **opcional** (puede ser null) → NO ponemos `@NotBlank`.
- Limitamos a 20 caracteres con `@Size` → suficiente para "+34 612 345 678".
- En el service hacemos `trim()` para limpiar espacios.
- No necesitamos regla de unicidad (dos alumnos pueden compartir teléfono).

### 📋 Prompt para la IA
> ```
> En mi proyecto Spring Boot "proyecto-final-sqlite-thymeleaf-jpa", necesito añadir
> un campo opcional "telefono" (String, máximo 20 caracteres) al Alumno.
>
> Archivos existentes que debes modificar:
> - Crear nueva migración Flyway: src/main/resources/db/migration/V4__añadir_telefono.sql
> - Entidad: src/main/java/com/curso/pfsqlite/domain/Alumno.java (añadir campo + getter/setter)
> - Form DTO: src/main/java/com/curso/pfsqlite/web/form/AlumnoForm.java (añadir campo con @Size(max=20))
> - Service: src/main/java/com/curso/pfsqlite/service/AlumnoService.java (pasar telefono al crear)
> - Vista formulario: src/main/resources/templates/alumnos/nuevo.html (añadir input)
> - Vista listado: src/main/resources/templates/alumnos/lista.html (añadir columna)
>
> El teléfono es opcional (null permitido), se debe hacer trim() en el service.
> Usa el mismo estilo de comentarios Better Comments del proyecto (// *, // ?, // !, // TODO).
> ```

---

## ⭐⭐ EJERCICIO 4 — Filtro de cursos por tipo (intermedio)

### 🎯 Objetivo
Añadir un **filtro en la vista de cursos** para mostrar solo ONLINE, solo PRESENCIAL, o todos.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Repository** | `CursoRepository.java` | Añadir método `findByTipoOrderByIdAsc(CursoTipo tipo)` |
| **Service** | `CursoService.java` | Nuevo método `listarPorTipo(CursoTipo tipo)` → if null → listar todos |
| **Controller** | `CursoController.java` | Modificar `listar()` para aceptar `@RequestParam(required=false) CursoTipo tipo` |
| **Vista** | `cursos/lista.html` | Añadir botones de filtro con `th:href` y clase `active` dinámica |

### 🧠 Decisiones de diseño
- El parámetro `tipo` es **opcional** (`required=false`) → si no llega, mostramos todos.
- Spring convierte automáticamente el String "ONLINE" al enum `CursoTipo.ONLINE`.
- El botón activo se resalta con `th:classappend="${filtroActual == t} ? 'active'"`.
- No necesitamos nueva migración Flyway porque no cambiamos la BD.

### 📋 Prompt para la IA
> ```
> En mi proyecto Spring Boot "proyecto-final-sqlite-thymeleaf-jpa", necesito añadir
> un filtro por tipo (ONLINE/PRESENCIAL/Todos) en la vista de listado de cursos.
>
> Archivos a modificar:
> - CursoRepository.java → añadir findByTipoOrderByIdAsc(CursoTipo tipo)
> - CursoService.java → nuevo método listarPorTipo(CursoTipo tipo) que si es null lista todos
> - CursoController.java → modificar listar() para aceptar @RequestParam(required=false) CursoTipo tipo
> - templates/cursos/lista.html → añadir grupo de botones Bootstrap (Todos / ONLINE / PRESENCIAL)
>   con clase 'active' dinámica según el filtro seleccionado
>
> El enum CursoTipo ya existe con valores ONLINE y PRESENCIAL.
> Usa el mismo estilo de comentarios Better Comments del proyecto.
> ```

---

## ⭐⭐ EJERCICIO 5 — Dashboard con estadísticas en el Home (intermedio)

### 🎯 Objetivo
Convertir la página de inicio en un **dashboard** con contadores y últimas matrículas.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Repository** | `MatriculaRepository.java` | Añadir `long countByEstado(EstadoMatricula estado)` |
| **Controller** | `HomeController.java` | Inyectar repos/services, pasar contadores y lista al modelo |
| **Vista** | `templates/index.html` | Crear 3 tarjetas Bootstrap + tabla de últimas matrículas |

### 🧠 Decisiones de diseño
- `count()` ya existe heredado de JpaRepository → lo usamos para total de alumnos y cursos.
- `countByEstado()` es una query derivada: Spring genera el SQL automáticamente.
- Limitamos las últimas matrículas a 5 con `.stream().limit(5).toList()`.
- HomeController necesitará inyectar `AlumnoRepository`, `CursoRepository` y `MatriculaService`.

### 📋 Prompt para la IA
> ```
> En mi proyecto Spring Boot "proyecto-final-sqlite-thymeleaf-jpa", quiero que la
> página de inicio (/) muestre un dashboard con:
> - 3 tarjetas Bootstrap con contadores: Total Alumnos, Total Cursos, Matrículas Activas
> - Una tabla con las 5 últimas matrículas (fecha, alumno, curso, estado)
> - Enlaces rápidos a cada sección
>
> Archivos a modificar:
> - MatriculaRepository.java → añadir countByEstado(EstadoMatricula estado)
> - HomeController.java → inyectar repositorios y service, pasar datos al modelo
> - templates/index.html → rediseñar con tarjetas y tabla
>
> Usa Bootstrap 5 para el diseño y el estilo Better Comments del proyecto.
> ```

---

## ⭐⭐⭐ EJERCICIO 6 — Editar un alumno existente (avanzado)

### 🎯 Objetivo
Implementar el **flujo completo de edición**: GET formulario pre-rellenado + POST para guardar.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Repository** | `AlumnoRepository.java` | Añadir `existsByEmailIgnoreCaseAndIdNot(String email, Long id)` |
| **Service** | `AlumnoService.java` | Nuevo método `buscar(Long id)` + `actualizar(Long id, AlumnoForm form)` |
| **Controller** | `AlumnoController.java` | Dos endpoints: `GET /{id}/editar` y `POST /{id}/editar` |
| **Vista** | `alumnos/editar.html` | Formulario igual a `nuevo.html` pero con `th:action` distinto |
| **Vista** | `alumnos/lista.html` | Añadir botón "Editar" en cada fila que enlace a `/{id}/editar` |

### 🧠 Decisiones de diseño
- **Email único excluyendo al propio alumno:** al editar, el alumno puede mantener su mismo email. Por eso usamos `existsByEmailIgnoreCaseAndIdNot(email, id)` en vez de `existsByEmailIgnoreCase(email)`.
- El formulario de edición es casi idéntico al de nuevo, pero el `th:action` apunta a `/alumnos/{id}/editar`.
- Se pasa `alumnoId` al modelo para que Thymeleaf construya la URL del formulario.
- Se reutiliza el mismo `AlumnoForm` (no hace falta crear otro DTO).

### ⚠️ Errores comunes
- Olvidar la validación de email único excluyente → permite que otro alumno robe el email.
- No pasar `alumnoId` al modelo cuando hay errores de validación → el formulario no sabe a dónde enviar.
- Olvidar pasar los datos existentes al form en el GET → el formulario aparece vacío.

### 📋 Prompt para la IA
> ```
> En mi proyecto Spring Boot "proyecto-final-sqlite-thymeleaf-jpa", necesito
> implementar la funcionalidad de EDITAR un alumno existente.
>
> Requisitos:
> - GET /alumnos/{id}/editar → muestra formulario pre-rellenado con los datos actuales
> - POST /alumnos/{id}/editar → guarda los cambios validando email único (excluyendo al propio alumno)
> - Botón "Editar" en cada fila de la lista de alumnos
>
> Archivos a modificar:
> - AlumnoRepository.java → añadir existsByEmailIgnoreCaseAndIdNot(String email, Long id)
> - AlumnoService.java → añadir buscar(Long id) y actualizar(Long id, AlumnoForm form)
> - AlumnoController.java → añadir GET /{id}/editar y POST /{id}/editar
> - Crear templates/alumnos/editar.html (formulario similar a nuevo.html)
> - templates/alumnos/lista.html → añadir botón "Editar" en cada fila
>
> Usa Better Comments, validación con @Valid, y manejo de BusinessException.
> ```

---

## ⭐⭐⭐ EJERCICIO 7 — Validar transiciones de estado en matrículas (avanzado)

### 🎯 Objetivo
Implementar una **máquina de estados** que solo permita transiciones válidas.

### 📖 Análisis técnico
Actualmente, `anular()` cambia el estado sin comprobar el estado previo. Queremos que:
- Solo se pueda anular una matrícula **ACTIVA** (no una ya ANULADA o FINALIZADA).
- Solo se pueda finalizar una matrícula **ACTIVA**.
- Una matrícula ANULADA o FINALIZADA no puede volver a ACTIVA.

| Transición | ¿Válida? |
|---|---|
| ACTIVA → ANULADA | ✅ Sí |
| ACTIVA → FINALIZADA | ✅ Sí |
| ANULADA → ACTIVA | ❌ No |
| ANULADA → FINALIZADA | ❌ No |
| FINALIZADA → cualquiera | ❌ No |

### 🧠 Decisiones de diseño
- La validación va en **MatriculaService** (es regla de negocio, no de formato).
- Se lanza `BusinessException` con mensaje claro si la transición no es válida.
- Se puede añadir un método `finalizar(Long id)` similar a `anular()`.

### 📋 Prompt para la IA
> ```
> En mi proyecto Spring Boot "proyecto-final-sqlite-thymeleaf-jpa", necesito
> validar las transiciones de estado en MatriculaService:
>
> Transiciones válidas:
> - ACTIVA → ANULADA (método anular)
> - ACTIVA → FINALIZADA (nuevo método finalizar)
> - Cualquier otra transición lanza BusinessException
>
> Archivos a modificar:
> - MatriculaService.java → validar estado actual antes de cambiar + nuevo método finalizar()
> - MatriculaController.java → nuevo endpoint POST /matriculas/{id}/finalizar
> - templates/matriculas/lista.html → añadir botón "Finalizar" (solo visible si ACTIVA)
>
> Usa Better Comments y manejo de BusinessException con mensajes claros.
> ```

---

## ⭐⭐⭐ EJERCICIO 8 — Paginación en matrículas (avanzado)

### 🎯 Objetivo
Evitar cargar TODAS las matrículas a la vez usando **paginación de Spring Data**.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Repository** | `MatriculaRepository.java` | Nuevo método con `Pageable` que devuelve `Page<Matricula>` |
| **Service** | `MatriculaService.java` | Nuevo método `listarPaginado(int page, int size)` |
| **Controller** | `MatriculaController.java` | Aceptar `@RequestParam(defaultValue="0") int page` |
| **Vista** | `matriculas/lista.html` | Añadir navegación de páginas (anterior/siguiente) |

### 🧠 Decisiones de diseño
- `Page<Matricula>` contiene `.getContent()` (la lista), `.getTotalPages()`, `.getNumber()` (página actual).
- Tamaño de página: **10 matrículas** por página (configurable).
- Los botones de navegación usan `th:href="@{/matriculas(page=${paginaActual - 1})}"`.
- El botón "Anterior" se oculta si estamos en página 0.
- El botón "Siguiente" se oculta si estamos en la última página.

### 📋 Prompt para la IA
> ```
> En mi proyecto Spring Boot "proyecto-final-sqlite-thymeleaf-jpa", necesito
> implementar paginación en el listado de matrículas (10 por página).
>
> Archivos a modificar:
> - MatriculaRepository.java → método con Pageable que devuelve Page<Matricula> con @EntityGraph
> - MatriculaService.java → listarPaginado(int page, int size) con PageRequest.of()
> - MatriculaController.java → aceptar parámetro page, pasar datos de paginación al modelo
> - templates/matriculas/lista.html → botones Anterior/Siguiente con th:href dinámico
>
> Usa Spring Data Page, PageRequest y Bootstrap para los botones de navegación.
> ```

---

## ⭐⭐⭐ EJERCICIO 9 — Exportar alumnos a CSV (avanzado)

### 🎯 Objetivo
Crear un endpoint que genere un **archivo CSV descargable** con la lista de alumnos.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Controller** | `AlumnoController.java` | Nuevo endpoint `GET /alumnos/exportar` que devuelve `ResponseEntity<byte[]>` |
| **Vista** | `alumnos/lista.html` | Añadir botón "📥 Exportar CSV" que enlace a `/alumnos/exportar` |

### 🧠 Decisiones de diseño
- El endpoint devuelve `ResponseEntity<byte[]>` con header `Content-Disposition: attachment; filename=alumnos.csv`.
- El content type es `text/csv; charset=UTF-8`.
- Se genera el CSV directamente con `StringBuilder` (sin librería externa).
- Cabeceras del CSV: `ID,Nombre,Email,Fecha Nacimiento`.
- Se incluye BOM UTF-8 (`\uFEFF`) para que Excel interprete correctamente los acentos.

### 📋 Prompt para la IA
> ```
> En mi proyecto Spring Boot "proyecto-final-sqlite-thymeleaf-jpa", necesito un
> endpoint GET /alumnos/exportar que descargue un archivo CSV con todos los alumnos.
>
> Requisitos:
> - Cabeceras: ID, Nombre, Email, Fecha Nacimiento
> - Content-Type: text/csv; charset=UTF-8
> - Header Content-Disposition: attachment; filename=alumnos.csv
> - Incluir BOM UTF-8 para compatibilidad con Excel
> - ResponseEntity<byte[]> como tipo de retorno
>
> Archivos a modificar:
> - AlumnoController.java → nuevo endpoint GET /alumnos/exportar
> - templates/alumnos/lista.html → añadir botón "Exportar CSV" que enlace al endpoint
>
> Usa Better Comments para documentar el nuevo endpoint.
> ```

---

## ⭐⭐⭐ EJERCICIO 10 — Tests de integración con @SpringBootTest (avanzado)

### 🎯 Objetivo
Verificar que las **reglas de negocio funcionan con la BD real** (SQLite en modo test).

### 📖 Análisis técnico
Los tests unitarios que ya tiene el proyecto usan **Mockito** (simulan el repositorio). Los tests de integración arrancan Spring completo y usan la BD real para verificar que todo funciona de extremo a extremo.

| Qué probar | Resultado esperado |
|---|---|
| Crear alumno con email duplicado | Lanza `BusinessException` |
| Crear curso con `fechaFin < fechaInicio` | Lanza `BusinessException` |
| Borrar alumno con matrícula ACTIVA | Lanza `BusinessException` |
| Crear matrícula ACTIVA duplicada | Lanza `BusinessException` |
| Crear alumno válido y verificar que existe en BD | Funciona correctamente |

### 🧠 Decisiones de diseño
- `@SpringBootTest` → arranca TODO el contexto de Spring (lento pero completo).
- `@Transactional` en la clase de test → cada test hace **rollback automático** al terminar.
- Se usa `assertThatThrownBy()` de AssertJ para verificar excepciones.

### 📋 Prompt para la IA
> ```
> En mi proyecto Spring Boot "proyecto-final-sqlite-thymeleaf-jpa", necesito
> crear tests de integración con @SpringBootTest y @Transactional.
>
> Crear archivo: src/test/java/com/curso/pfsqlite/service/AlumnoServiceIntegrationTest.java
>
> Tests a implementar:
> 1. Crear alumno válido → verificar que existe en BD con el ID asignado
> 2. Crear alumno con email duplicado → debe lanzar BusinessException
> 3. Crear alumno con email inválido → debe lanzar BusinessException
> 4. Borrar alumno sin matrículas → funciona correctamente
> 5. Borrar alumno con matrícula ACTIVA → debe lanzar BusinessException
>
> Usa @Autowired para inyectar AlumnoService y los repositorios.
> Cada test debe ser @Transactional para rollback automático.
> Usa AssertJ (assertThat, assertThatThrownBy) para las assertions.
> Añade @DisplayName descriptivo en cada test.
> ```

---

## 📚 Tabla resumen: Conceptos clave del proyecto

| Concepto | Dónde verlo en el código |
|----------|--------------------------|
| **@Transactional** | Todos los métodos del Service (`readOnly` para lectura) |
| **@Transactional(readOnly=true)** | Métodos `listar()` en todos los services |
| **Flyway Migrations** | `resources/db/migration/V*.sql` |
| **Thymeleaf `th:each`** | Vistas HTML para iterar listas |
| **RedirectAttributes (flash)** | Controllers → mensajes de éxito/error tras redirect |
| **Bean Validation (`@Valid`)** | AlumnoForm, CursoForm, MatriculaForm |
| **Borrado protegido** | Service verifica matrículas ACTIVAS antes de borrar |
| **Borrado lógico vs físico** | `anular()` vs `borrar()` en MatriculaService |
| **SLF4J Logger** | Logging profesional en todos los services |
| **Inyección por constructor** | Todos los controllers y services (patrón `final`) |
| **@EntityGraph** | MatriculaRepository → evita problema N+1 |
| **Query derivadas** | `existsByEmailIgnoreCase`, `findAllByOrderByIdAsc`, etc. |
| **BigDecimal** | Precio del curso → precisión exacta para dinero |
| **EnumType.STRING** | CursoTipo y EstadoMatricula → texto legible en BD |
| **@ControllerAdvice** | GlobalExceptionHandler → errores globales |

---

## 🚀 ¿Quieres ir más allá? Ideas avanzadas

Estas ideas no tienen ejercicio detallado pero son excelentes proyectos de ampliación:

| Idea | Dificultad | Qué aprenderías |
|------|-----------|-----------------|
| API REST (JSON) además de las vistas HTML | ⭐⭐⭐ | `@RestController`, `ResponseEntity`, códigos HTTP |
| Autenticación con Spring Security | ⭐⭐⭐⭐ | Login, roles (ADMIN/USER), protección de rutas |
| Subir foto de perfil del alumno | ⭐⭐⭐ | `MultipartFile`, almacenamiento de archivos |
| Enviar email al crear matrícula | ⭐⭐⭐ | Spring Mail, plantillas Thymeleaf para email |
| Docker para despliegue | ⭐⭐ | `Dockerfile`, `docker-compose`, variables de entorno |
| Cambiar SQLite por PostgreSQL | ⭐⭐ | Perfil de Spring, configuración de datasource |
