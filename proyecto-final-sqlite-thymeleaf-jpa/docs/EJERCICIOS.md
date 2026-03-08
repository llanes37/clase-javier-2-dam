# Ejercicios del Proyecto

> **Instrucciones para el alumno:**
> 1. Lee el enunciado completo antes de empezar.
> 2. Identifica los archivos a tocar en la tabla de cambios.
> 3. Implementa en pasos pequenos, ejecuta los tests entre cada paso.
> 4. Verifica la prueba manual antes de dar el ejercicio por terminado.
>
> **Para pedir ayuda a la IA**, usa este prompt base:
> ```
> Quiero resolver el ejercicio [E_NUMERO] de este proyecto Spring Boot.
> Dame los pasos de implementacion, los casos borde y un test de ejemplo.
> No rompas ningun test existente ni la arquitectura por capas.
> ```

---

## Nivel Basico â€” Fundamentos de cada capa

### E1 â€” Validacion de nombre minimo 3 caracteres

**Que aprendes:** Bean Validation con `@Size`, diferencia entre validacion de formulario y regla de negocio.

| Capa | Archivo | Cambio |
|---|---|---|
| Formulario | `AlumnoForm.java` | `@Size(min = 3, message = "El nombre debe tener al menos 3 caracteres")` en `nombre` |
| Vista | `alumnos/nuevo.html` | Mostrar el mensaje de error con `th:errors` |

**Casos borde:**
- Nombre de 2 caracteres â†’ debe mostrar error en formulario.
- Nombre de exactamente 3 caracteres â†’ debe guardarse correctamente.
- Nombre con espacios al inicio: " Jo" â†’ Â¿cuenta el trim? Decide y justifica.

**Para probar:** intenta crear un alumno con nombre "Jo" â†’ el formulario debe rechazarlo con mensaje.

---

### E2 â€” Columna de edad calculada en el listado

**Que aprendes:** logica de presentacion vs logica de negocio, calculo de fechas con `LocalDate`.

| Capa | Archivo | Cambio |
|---|---|---|
| Service | `AlumnoService.java` | AÃ±adir metodo `calcularEdad(Alumno a)` que devuelva `Optional<Integer>` |
| Controller | `AlumnoController.java` | Pasar el mapa de edades al modelo |
| Vista | `alumnos/lista.html` | AÃ±adir columna "Edad" con valor calculado o "â€”" si no hay fecha |

**Casos borde:** alumno sin fecha de nacimiento (campo nullable) â†’ mostrar "â€”" sin errores.

**Para probar:** crea un alumno nacido en 2000 â†’ debe aparecer la edad correcta en el listado.

---

### E3 â€” Filtrar cursos por tipo ONLINE / PRESENCIAL

**Que aprendes:** `@RequestParam`, query derivada en repositorio, como Thymeleaf genera URLs con parametros.

| Capa | Archivo | Cambio |
|---|---|---|
| Repository | `CursoRepository.java` | `findAllByTipoOrderByIdAsc(CursoTipo tipo)` |
| Service | `CursoService.java` | `listarPorTipo(CursoTipo tipo)` |
| Controller | `CursoController.java` | `@RequestParam(required = false) CursoTipo tipo` en `listar()` |
| Vista | `cursos/lista.html` | Botones de filtro que aÃ±adan `?tipo=ONLINE` a la URL |

**Para probar:** navega a `/cursos?tipo=ONLINE` â†’ solo aparecen cursos ONLINE.

---

### E4 â€” Confirmacion visual antes de anular matricula

**Que aprendes:** UX defensivo, JavaScript basico integrado en Thymeleaf.

| Capa | Archivo | Cambio |
|---|---|---|
| Vista | `matriculas/lista.html` | `onclick="return confirm('Â¿Seguro que quieres anular esta matricula?')"`  en el boton |

**Para probar:** haz clic en "Anular" â†’ aparece el dialogo â†’ pulsa Cancelar â†’ la matricula continua ACTIVA.

---

## Nivel Intermedio â€” Flujos completos y relaciones

### E5 â€” Edicion de alumno (GET cargar + POST guardar)

**Que aprendes:** flujo GETâ†’POST para edicion, reutilizacion de formularios, regla de unicidad excluyendo el propio registro.

| Capa | Archivo | Cambio |
|---|---|---|
| Service | `AlumnoService.java` | `actualizar(Long id, AlumnoForm form)` â€” al verificar unicidad de email, excluir el propio alumno |
| Controller | `AlumnoController.java` | `GET /alumnos/{id}/editar` (carga datos) + `POST /alumnos/{id}/editar` (guarda) |
| Vista | Crear `alumnos/editar.html` | Formulario precargado con `th:value` y `th:field` |

**Casos borde:**
- Editar email al mismo valor â†’ no debe lanzar "ya existe".
- Editar email a un valor ya usado por otro alumno â†’ debe rechazarlo.

---

### E6 â€” Edicion de curso con reglas de negocio

**Que aprendes:** mismo patron que E5 con validacion de fechas. Restriccion extra por matriculas.

| Capa | Archivo | Cambio |
|---|---|---|
| Service | `CursoService.java` | `actualizar(Long id, CursoForm form)` â€” si hay matriculas ACTIVAS, no permitir cambiar `fechaInicio` |
| Controller | `CursoController.java` | `GET /cursos/{id}/editar` + `POST /cursos/{id}/editar` |
| Vista | Crear `cursos/editar.html` | |

**Caso borde importante:** un curso con matriculas activas puede cambiar nombre y precio, pero no las fechas.

---

### E7 â€” Busqueda de alumnos por email

**Que aprendes:** `@RequestParam`, query derivada con `LIKE`, mantener el filtro activo en la vista.

| Capa | Archivo | Cambio |
|---|---|---|
| Repository | `AlumnoRepository.java` | `findByEmailContainingIgnoreCaseOrderByIdAsc(String fragmento)` |
| Service | `AlumnoService.java` | `buscarPorEmail(String fragmento)` |
| Controller | `AlumnoController.java` | Parametro opcional `@RequestParam` en `listar()` |
| Vista | `alumnos/lista.html` | Input de busqueda con formulario GET que preserva el valor escrito |

**Para probar:** busca "gmail" â†’ aparecen solo alumnos con gmail en su email.

---

### E8 â€” Vista de matriculas de un alumno concreto

**Que aprendes:** navegacion entre entidades relacionadas, nuevo endpoint con parametro de ruta.

| Capa | Archivo | Cambio |
|---|---|---|
| Repository | `MatriculaRepository.java` | `findAllByAlumnoIdOrderByFechaMatriculaDesc(Long alumnoId)` con `@EntityGraph` |
| Service | `MatriculaService.java` | `listarPorAlumno(Long alumnoId)` |
| Controller | `AlumnoController.java` | `GET /alumnos/{id}/matriculas` |
| Vista | Crear `alumnos/matriculas.html` | Lista de matriculas del alumno con link de vuelta |

**Para probar:** navega a `/alumnos/{id}/matriculas` â†’ aparecen solo las matriculas de ese alumno.

---

## Nivel Avanzado â€” Mejoras de calidad y nuevas funcionalidades

### E9 â€” Paginacion en listados

**Que aprendes:** `Pageable`, `Page<T>`, como Thymeleaf genera la navegacion entre paginas.

| Capa | Archivo | Cambio |
|---|---|---|
| Repository | `MatriculaRepository.java` | Metodo con `Pageable` |
| Service | `MatriculaService.java` | `listar(int pagina)` |
| Controller | `MatriculaController.java` | `@RequestParam(defaultValue = "0") int pagina` |
| Vista | `matriculas/lista.html` | Botones anterior/siguiente |

**Pista:**
```java
// Repository
Page<Matricula> findAll(Pageable pageable);

// Service
public Page<Matricula> listar(int pagina) {
    return matriculaRepository.findAll(
        PageRequest.of(pagina, 10, Sort.by("fechaMatricula").descending()));
}
```

---

### E10 â€” Tests que faltan (TDD inverso)

**Que aprendes:** identificar huecos en la cobertura, patron Arrange/Act/Assert, `@DisplayName`.

Escribe estos tests uno a uno. Para cada uno: copia la clase de test correspondiente, aÃ±ade el metodo y ejecuta solo ese test con `mvnw -Dtest=NombreTest#nombreMetodo test`.

| Test | Clase | Que verifica |
|---|---|---|
| 1 | `AlumnoServiceTest` | Email con formato invalido (sin @) lanza `BusinessException` |
| 2 | `AlumnoServiceTest` | `borrar()` sin matriculas activas elimina el alumno correctamente |
| 3 | `CursoServiceTest` | Curso con fechaFin igual a fechaInicio (mismo dia) se crea ok |
| 4 | `MatriculaServiceTest` | `anular()` cambia el estado a ANULADA |
| 5 | `MatriculaRepositoryTest` | `existsByAlumnoIdAndCursoIdAndEstado` devuelve `false` para estado ANULADA |

**Patron obligatorio para cada test:**
```java
@Test
@DisplayName("Descripcion legible: que regla y que caso borde verifica")
void nombreDelTest() {
    // Arrange: preparar datos de entrada y configurar mocks

    // Act: llamar al metodo que estamos probando

    // Assert: verificar el resultado esperado
}
```

---

### E11 â€” Exportacion a CSV de matriculas

**Que aprendes:** `HttpServletResponse`, escritura de datos en streaming, cabeceras HTTP de descarga.

| Capa | Archivo | Cambio |
|---|---|---|
| Controller | `MatriculaController.java` | `GET /matriculas/exportar.csv` |
| Vista | `matriculas/lista.html` | Boton de descarga que apunte a ese endpoint |

**Pista de implementacion:**
```java
@GetMapping("/exportar.csv")
public void exportarCsv(HttpServletResponse response) throws IOException {
    response.setContentType("text/csv; charset=UTF-8");
    response.setHeader("Content-Disposition", "attachment; filename=\"matriculas.csv\"");
    // TODO: usar matriculaService.listar() y escribir cabecera + filas
    // cabecera: "ID,Alumno,Curso,Fecha,Estado"
    // fila: id + "," + alumno.getNombre() + "," + ...
}
```

**Para probar:** haz clic en el boton â†’ el navegador descarga `matriculas.csv`.

---

### E12 â€” Endpoint REST paralelo a Thymeleaf

**Que aprendes:** `@RestController`, serializacion JSON, coexistencia de MVC y REST en el mismo proyecto, problema de ciclos en serializar entidades con relaciones LAZY.

| Capa | Archivo | Cambio |
|---|---|---|
| Web | Crear `web/CursoRestController.java` | `GET /api/cursos` devuelve `List<Curso>` como JSON |

**Pista:**
```java
@RestController
@RequestMapping("/api")
public class CursoRestController {
    private final CursoService cursoService;
    public CursoRestController(CursoService cursoService) {
        this.cursoService = cursoService;
    }
    // TODO: GET /api/cursos â†’ return cursoService.listar()
    // ? Â¿Por que puede fallar si Curso tiene relaciones LAZY?
    // ! AÃ±adir @JsonIgnoreProperties en las relaciones si hay ciclos de serializacion
}
```

**Para probar:** abre `http://localhost:8080/api/cursos` en el navegador â†’ debe devolver JSON.

---

### E13 â€” Auditoria: fechas de creacion y modificacion

**Que aprendes:** `@CreationTimestamp`, `@UpdateTimestamp` de Hibernate, migraciones con columnas nuevas.

| Capa | Archivo | Cambio |
|---|---|---|
| Migracion | Crear `V3__auditoria_alumnos.sql` | AÃ±adir columnas `creado_en DATETIME` y `modificado_en DATETIME` |
| Entidad | `Alumno.java` | Campos con `@CreationTimestamp` y `@UpdateTimestamp` |
| Vista | `alumnos/lista.html` | Columna "Alta" con la fecha de creacion |

**Pista SQL (SQLite):**
```sql
-- V3__auditoria_alumnos.sql
ALTER TABLE alumnos ADD COLUMN creado_en DATETIME;
ALTER TABLE alumnos ADD COLUMN modificado_en DATETIME;
```

**Para probar:** crea un alumno â†’ la columna "Alta" muestra la fecha. Edita el alumno â†’ `modificado_en` cambia.

---

### E14 â€” Estadisticas en el home

**Que aprendes:** consultas de agregacion (`count`), pasar multiples datos al modelo, presentacion de KPIs.

| Capa | Archivo | Cambio |
|---|---|---|
| Repository | Los 3 repositorios | `count()` ya existe en `JpaRepository` |
| Controller | `HomeController.java` | Pasar contadores al modelo |
| Vista | `index.html` | Tarjetas con N alumnos, N cursos, N matriculas ACTIVAS |

**Pista:**
```java
// En HomeController:
model.addAttribute("totalAlumnos", alumnoRepository.count());
model.addAttribute("totalCursos", cursoRepository.count());
// Para contar ACTIVAS necesitas un metodo en MatriculaRepository:
long countByEstado(EstadoMatricula estado);
```

---

## Extension profesional

### E15 â€” Perfiles dev / prod con PostgreSQL

**Que aprendes:** `@Profile`, ficheros `application-{perfil}.properties`, separacion de entornos.

**Pasos:**
1. Crea `src/main/resources/application-dev.properties` con la configuracion actual de SQLite.
2. Crea `src/main/resources/application-prod.properties` con PostgreSQL.
3. En `application.properties`, deja solo `spring.profiles.active=dev`.
4. AÃ±ade la dependencia de PostgreSQL en `pom.xml`.
5. Comprueba que las migraciones Flyway son compatibles con PostgreSQL.

```bash
# Arrancar con perfil prod:
./mvnw spring-boot:run -Dspring-boot.run.arguments=--spring.profiles.active=prod
```

---

### E16 â€” Seguridad con Spring Security y roles

**Que aprendes:** autenticacion, autorizacion, formulario de login, restriccion de rutas por rol.

Dependencia a aÃ±adir en `pom.xml`:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
<dependency>
    <groupId>org.thymeleaf.extras</groupId>
    <artifactId>thymeleaf-extras-springsecurity6</artifactId>
</dependency>
```

**Roles a implementar:**
- `ADMIN` â†’ acceso total (crear, editar, borrar).
- `VIEWER` â†’ solo puede ver listados, no puede crear ni borrar.

**Pista de configuracion:**
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/", "/css/**").permitAll()
                .requestMatchers(HttpMethod.POST, "/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .formLogin(Customizer.withDefaults())
            .build();
    }
    // TODO: definir usuarios en memoria o en base de datos
}
```

