# Migración a Angular — Análisis completo del proyecto

> Proyecto base: `proyecto-final-sqlite-thymeleaf-jpa`  
> Stack actual: Spring Boot 3.3.5 · Thymeleaf · SQLite · JPA · Spring Security · Flyway  
> Stack objetivo: Spring Boot (API REST) + Angular SPA

---

## Índice

1. [Estado actual — qué hace cada capa](#1-estado-actual)
2. [Qué se reutiliza y qué se reemplaza](#2-qué-se-reutiliza-y-qué-se-reemplaza)
3. [Cambios en el backend Spring Boot](#3-cambios-en-el-backend-spring-boot)
4. [Estructura del frontend Angular](#4-estructura-del-frontend-angular)
5. [Fases de migración paso a paso](#5-fases-de-migración-paso-a-paso)
6. [Código de referencia — Spring Boot](#6-código-de-referencia--spring-boot)
7. [Código de referencia — Angular](#7-código-de-referencia--angular)
8. [Puntos de atención y riesgos](#8-puntos-de-atención-y-riesgos)

---

## 1. Estado actual

### Arquitectura del proyecto Thymeleaf

```
Navegador
   │  HTML renderizado en servidor
   ▼
@Controller (capa web MVC)
   │  devuelve nombre de vista
   ▼
Thymeleaf (motor de plantillas)
   │  rellena templates/*.html con datos del Model
   ▼
@Service (lógica de negocio)
   │  valida y transforma
   ▼
@Repository (JPA)
   │  consultas SQL
   ▼
SQLite (./data/app.db)
```

### Flujo de una petición actual (ejemplo: GET /alumnos)

```
GET /alumnos
  → AlumnoController.listar(Model model)
      alumnoService.listar()            → SELECT * FROM alumnos
      model.addAttribute("alumnos", …)
      return "alumnos/lista"            → Thymeleaf resuelve templates/alumnos/lista.html
  ← 200 HTML completo (página entera)
```

### Qué hace cada clase

| Clase | Capa | Responsabilidad actual |
|---|---|---|
| `HomeController` | Web | Sirve la página de inicio (`index.html`) |
| `AlumnoController` | Web | CRUD alumnos → retorna vistas Thymeleaf |
| `CursoController` | Web | CRUD cursos → retorna vistas Thymeleaf |
| `MatriculaController` | Web | CRUD matrículas → retorna vistas Thymeleaf |
| `AuthController` | Web | Login/registro → modal en `auth/login.html` |
| `GlobalExceptionHandler` | Web | Captura errores → retorna vista `error.html` |
| `AlumnoForm`, `CursoForm`, `MatriculaForm` | Web | DTOs ligados al formulario HTML con Thymeleaf |
| `AlumnoService` | Service | Valida email (regex + unicidad), borrado protegido |
| `CursoService` | Service | Valida fechas (`fin >= inicio`), borrado protegido |
| `MatriculaService` | Service | Valida existencia alumno/curso, rango fechas, unicidad ACTIVA |
| `UsuarioService` | Service | Implementa `UserDetailsService`, crea usuarios con BCrypt |
| `SecurityConfig` | Config | `formLogin`, `logout`, reglas de autorización por rol |
| `Alumno`, `Curso`, `Matricula`, `Usuario` | Domain | Entidades JPA (no cambian) |
| Repositorios | Repository | Consultas JPA (no cambian) |

### Seguridad actual

- Sesión HTTP gestionada por Spring Security.
- Login con formulario HTML (`POST /login`).
- Roles: `ROLE_USER` (solo lectura) y `ROLE_ADMIN` (escritura).
- CSRF habilitado por defecto (Thymeleaf lo gestiona automáticamente con `th:action`).
- No hay `@RestController` en el proyecto.

---

## 2. Qué se reutiliza y qué se reemplaza

### Se reutiliza completo (no tocar)

| Qué | Por qué |
|---|---|
| Entidades JPA: `Alumno`, `Curso`, `Matricula`, `Usuario` | No dependen de la capa web |
| Repositorios JPA | No dependen de la capa web |
| `AlumnoService`, `CursoService`, `MatriculaService` | Lógica de negocio pura, independiente de Thymeleaf |
| `UsuarioService` (implementa `UserDetailsService`) | Compatible con JWT y sesión |
| `BusinessException`, `NotFoundException` | Se siguen usando en la API REST |
| Migraciones Flyway (`V1__init.sql`, etc.) | El esquema no cambia |
| `SecurityConfig` (BCrypt, `DaoAuthenticationProvider`) | Se adapta, no se reescribe |

### Se reemplaza

| Qué se reemplaza | Por qué | Por qué lo sustituye |
|---|---|---|
| `@Controller` con vistas Thymeleaf | Angular gestiona la UI | `@RestController` con JSON |
| `Model`, `RedirectAttributes` | Solo tienen sentido con vistas servidor | `ResponseEntity<T>` |
| Clases `*Form` (ligadas a `th:object`) | Thymeleaf las vincula al HTML | DTOs de entrada/salida JSON |
| `GlobalExceptionHandler` devuelve vista | Angular no puede mostrar HTML como error | `@RestControllerAdvice` devuelve JSON |
| `formLogin` / `logout` de sesión | SPA no usa páginas de login servidor | Autenticación basada en sesión con cookie **o** JWT |
| Templates Thymeleaf (`templates/`) | Angular renderiza en el cliente | Componentes Angular (`.component.ts` + `.html`) |
| `thymeleaf-extras-springsecurity6` | No tiene sentido sin Thymeleaf | Interceptores HTTP en Angular |

### Cambios en `pom.xml`

**Eliminar:**
```xml
<artifactId>spring-boot-starter-thymeleaf</artifactId>
<artifactId>thymeleaf-extras-springsecurity6</artifactId>
```

**Añadir (si se usa JWT):**
```xml
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-api</artifactId>
    <version>0.12.6</version>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-impl</artifactId>
    <version>0.12.6</version>
    <scope>runtime</scope>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-jackson</artifactId>
    <version>0.12.6</version>
    <scope>runtime</scope>
</dependency>
```

---

## 3. Cambios en el backend Spring Boot

### 3.1. Nuevos DTOs JSON (sustituyen a los `*Form`)

Los `*Form` actuales están acoplados a Thymeleaf y `BindingResult`. Con Angular, los DTOs sirven para:
- Recibir datos del cliente (DTOs de entrada).
- Responder con datos al cliente (DTOs de salida) sin exponer entidades JPA directamente.

> Por qué no exponer las entidades JPA: tienen relaciones `LAZY` (`@ManyToOne(fetch = LAZY)`
> en `Matricula`) que fuera de transacción provocan `LazyInitializationException`.
> Además, `spring.jpa.open-in-view=false` ya está configurado en este proyecto,
> por lo que la sesión de Hibernate cierra al salir del servicio.

**Ejemplo: DTO de respuesta para Alumno**
```java
// src/main/java/com/curso/pfsqlite/web/dto/AlumnoResponseDto.java
public record AlumnoResponseDto(Integer id, String nombre, String email, LocalDate fechaNacimiento) {
    public static AlumnoResponseDto from(Alumno a) {
        return new AlumnoResponseDto(a.getId(), a.getNombre(), a.getEmail(), a.getFechaNacimiento());
    }
}
```

**Ejemplo: DTO de entrada para Alumno (sustituye a `AlumnoForm`)**
```java
// src/main/java/com/curso/pfsqlite/web/dto/AlumnoRequestDto.java
public record AlumnoRequestDto(
    @NotBlank(message = "El nombre es obligatorio") String nombre,
    @NotBlank @Email String email,
    LocalDate fechaNacimiento
) {}
```

### 3.2. Nuevos `@RestController`

Cada `@Controller` actual tiene un `@RestController` equivalente bajo `/api/`.

| Controlador Thymeleaf | RestController Angular | Prefijo |
|---|---|---|
| `AlumnoController` | `AlumnoApiController` | `/api/alumnos` |
| `CursoController` | `CursoApiController` | `/api/cursos` |
| `MatriculaController` | `MatriculaApiController` | `/api/matriculas` |
| `AuthController` | `AuthApiController` | `/api/auth` |

**Mapa de endpoints REST:**

```
GET    /api/alumnos           → lista todos los alumnos (ROLE_USER, ROLE_ADMIN)
GET    /api/alumnos/{id}      → devuelve un alumno por id
POST   /api/alumnos           → crea alumno (ROLE_ADMIN)
PUT    /api/alumnos/{id}      → actualiza alumno (ROLE_ADMIN)
DELETE /api/alumnos/{id}      → elimina alumno (ROLE_ADMIN)

GET    /api/cursos
GET    /api/cursos/{id}
POST   /api/cursos
PUT    /api/cursos/{id}
DELETE /api/cursos/{id}

GET    /api/matriculas
GET    /api/matriculas/{id}
POST   /api/matriculas
PATCH  /api/matriculas/{id}/anular   → borrado lógico (estado → ANULADA)
DELETE /api/matriculas/{id}

POST   /api/auth/login        → devuelve token o establece cookie de sesión
POST   /api/auth/register     → registra nuevo usuario
GET    /api/auth/me           → devuelve el usuario autenticado actual
POST   /api/auth/logout
```

> **Nota sobre DELETE con Angular:** A diferencia de los formularios HTML que solo soportan GET y POST
> (por eso el proyecto usa `POST /alumnos/{id}/eliminar`), Angular puede enviar
> DELETE y PUT nativamente con `HttpClient`.

### 3.3. Manejo de errores en API REST

El `GlobalExceptionHandler` actual devuelve la vista `error.html`. Necesita convertirse en
`@RestControllerAdvice` para devolver JSON:

```java
// Antes (Thymeleaf)
@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(NotFoundException.class)
    public String handleNotFound(NotFoundException ex, Model model) {
        model.addAttribute("mensaje", ex.getMessage());
        return "error";   // ← vista HTML
    }
}

// Después (API REST)
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(NotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public Map<String, String> handleNotFound(NotFoundException ex) {
        return Map.of("error", ex.getMessage());   // ← JSON
    }

    @ExceptionHandler(BusinessException.class)
    @ResponseStatus(HttpStatus.UNPROCESSABLE_ENTITY)
    public Map<String, String> handleBusiness(BusinessException ex) {
        return Map.of("error", ex.getMessage());
    }
}
```

### 3.4. Seguridad — Dos opciones

#### Opción A: Sesión con cookie (más sencilla, recomendada para empezar)

Mantiene el `DaoAuthenticationProvider` y BCrypt que ya existen. Solo cambia cómo se gestiona
el login y el CSRF.

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http, ...) throws Exception {
    http
        .authenticationProvider(authProvider)
        // ── CORS necesario para que Angular (localhost:4200) pueda llamar ──
        .cors(cors -> cors.configurationSource(corsConfigSource()))
        // ── CSRF: desactivar para API REST sin estado (si usas JWT)
        //    o usar CookieCsrfTokenRepository si quieres mantener CSRF con sesión ──
        .csrf(csrf -> csrf
            .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
        )
        .authorizeHttpRequests(auth -> auth
            .requestMatchers(HttpMethod.POST, "/api/auth/login", "/api/auth/register").permitAll()
            .requestMatchers(HttpMethod.GET, "/api/alumnos", "/api/cursos", "/api/matriculas").hasAnyRole("USER", "ADMIN")
            .requestMatchers("/api/**").hasRole("ADMIN")
            .anyRequest().authenticated()
        )
        // ── Responder 401 JSON en vez de redirigir a /login ──
        .exceptionHandling(ex -> ex
            .authenticationEntryPoint((req, res, e) ->
                res.sendError(HttpServletResponse.SC_UNAUTHORIZED, "No autenticado"))
        )
        // ── Sin formLogin ni logout HTML ──
        .sessionManagement(session -> session
            .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)
        );
    return http.build();
}
```

#### Opción B: JWT (sin estado, estándar en SPA en producción)

JWT elimina la necesidad de gestionar sesiones en servidor. Angular guarda el token en memoria
(o `localStorage`) y lo envía en cada petición en la cabecera `Authorization: Bearer <token>`.

```
Login:
  POST /api/auth/login  { username, password }
  ← 200 { token: "eyJhbGci..." }

Peticiones autenticadas:
  GET /api/alumnos
  Authorization: Bearer eyJhbGci...
```

Requiere añadir:
- Dependencia `jjwt` en `pom.xml`.
- Clase `JwtTokenProvider` (genera y valida tokens).
- Filtro `JwtAuthenticationFilter extends OncePerRequestFilter`.
- Registrar el filtro en `SecurityFilterChain` antes del `UsernamePasswordAuthenticationFilter`.

### 3.5. CORS

Angular en desarrollo corre en `localhost:4200`, Spring en `localhost:8080`. Sin CORS,
el navegador bloquea las peticiones.

```java
@Bean
public CorsConfigurationSource corsConfigSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(List.of("http://localhost:4200"));
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"));
    config.setAllowedHeaders(List.of("*"));
    config.setAllowCredentials(true);   // obligatorio si usas sesión con cookie
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/api/**", config);
    return source;
}
```

### 3.6. Problema de serialización JSON con relaciones LAZY

`Matricula` tiene `@ManyToOne(fetch = FetchType.LAZY)` para `alumno` y `curso`. Jackson
intentaría serializar las relaciones y provocaría `LazyInitializationException`.

**Solución: DTOs de respuesta que mapean manualmente los datos necesarios:**

```java
// No devolver Matricula directamente, sino un DTO:
public record MatriculaResponseDto(
    Integer id,
    String alumnoNombre,
    String cursoNombre,
    LocalDate fechaMatricula,
    EstadoMatricula estado
) {
    public static MatriculaResponseDto from(Matricula m) {
        return new MatriculaResponseDto(
            m.getId(),
            m.getAlumno().getNombre(),   // seguro dentro de @Transactional
            m.getCurso().getNombre(),
            m.getFechaMatricula(),
            m.getEstado()
        );
    }
}
```

---

## 4. Estructura del frontend Angular

### Requisitos previos

```bash
node --version     # v20+ recomendado
npm --version      # v10+
npm install -g @angular/cli
ng version         # Angular CLI 17+
```

### Crear el proyecto Angular

```bash
# Dentro de la carpeta raíz del proyecto
ng new frontend --routing --style=scss --no-standalone
cd frontend
```

### Estructura de carpetas Angular

```
frontend/src/app/
│
├── core/                          ← Servicios singleton, guards, interceptores
│   ├── auth/
│   │   ├── auth.service.ts        ← login(), logout(), getMe(), isLoggedIn()
│   │   ├── auth.guard.ts          ← protege rutas que requieren login
│   │   └── role.guard.ts          ← protege rutas que requieren ADMIN
│   ├── interceptors/
│   │   ├── auth.interceptor.ts    ← añade Authorization header (si JWT)
│   │   └── error.interceptor.ts   ← captura 401/403/500 globalmente
│   └── models/                    ← Interfaces TypeScript = DTOs del backend
│       ├── alumno.model.ts
│       ├── curso.model.ts
│       ├── matricula.model.ts
│       └── usuario.model.ts
│
├── features/                      ← Módulos de funcionalidad por dominio
│   ├── alumnos/
│   │   ├── alumnos.module.ts
│   │   ├── alumnos-routing.module.ts
│   │   ├── alumnos-lista/         ← equivalente a templates/alumnos/lista.html
│   │   │   ├── alumnos-lista.component.ts
│   │   │   └── alumnos-lista.component.html
│   │   ├── alumno-form/           ← equivalente a templates/alumnos/nuevo.html + editar.html
│   │   │   ├── alumno-form.component.ts
│   │   │   └── alumno-form.component.html
│   │   └── alumnos.service.ts     ← llama a GET/POST/PUT/DELETE /api/alumnos
│   │
│   ├── cursos/                    ← mismo patrón que alumnos/
│   │   ├── cursos.module.ts
│   │   ├── cursos-lista/
│   │   ├── curso-form/
│   │   └── cursos.service.ts
│   │
│   └── matriculas/                ← mismo patrón
│       ├── matriculas.module.ts
│       ├── matriculas-lista/
│       ├── matricula-form/
│       └── matriculas.service.ts
│
├── shared/                        ← Componentes reutilizables en toda la app
│   ├── navbar/
│   │   └── navbar.component.ts    ← equivalente a templates/fragments/nav.html
│   ├── alert/
│   │   └── alert.component.ts     ← mensajes ok/error (como los flash de Spring)
│   └── shared.module.ts
│
├── auth/                          ← Módulo de autenticación
│   ├── login/
│   │   ├── login.component.ts     ← equivalente a templates/auth/login.html
│   │   └── login.component.html
│   └── auth.module.ts
│
├── app-routing.module.ts          ← Rutas principales con lazy loading
└── app.component.ts               ← Shell principal con <router-outlet>
```

### Interfaces TypeScript (equivalentes a las entidades Java)

```typescript
// core/models/alumno.model.ts
export interface Alumno {
  id: number;
  nombre: string;
  email: string;
  fechaNacimiento?: string;   // ISO date string (yyyy-MM-dd)
}

// core/models/curso.model.ts
export interface Curso {
  id: number;
  nombre: string;
  tipo: 'ONLINE' | 'PRESENCIAL';
  fechaInicio: string;
  fechaFin: string;
  precio: number;
}

// core/models/matricula.model.ts
export interface Matricula {
  id: number;
  alumnoNombre: string;
  cursoNombre: string;
  fechaMatricula: string;
  estado: 'ACTIVA' | 'ANULADA' | 'FINALIZADA';
}
```

### Rutas Angular (equivalentes a las URLs de Spring MVC)

| URL Spring MVC (actual) | Ruta Angular (nueva) | Componente |
|---|---|---|
| `GET /` | `/` | `HomeComponent` |
| `GET /alumnos` | `/alumnos` | `AlumnosListaComponent` |
| `GET /alumnos/nuevo` | `/alumnos/nuevo` | `AlumnoFormComponent` |
| `GET /alumnos/{id}/editar` | `/alumnos/:id/editar` | `AlumnoFormComponent` |
| `GET /cursos` | `/cursos` | `CursosListaComponent` |
| `GET /cursos/nuevo` | `/cursos/nuevo` | `CursoFormComponent` |
| `GET /matriculas` | `/matriculas` | `MatriculasListaComponent` |
| `GET /matriculas/nueva` | `/matriculas/nueva` | `MatriculaFormComponent` |
| `GET /login` | `/login` | `LoginComponent` |

---

## 5. Fases de migración paso a paso

### Fase 1 — Crear la API REST en Spring Boot (sin tocar nada existente)

**Objetivo:** el backend puede responder tanto a los `@Controller` Thymeleaf como a los nuevos `@RestController`. Ambos coexisten.

**Pasos:**

1. Crear paquete `web/api/` para los nuevos `@RestController`.
2. Crear paquete `web/dto/` para los DTOs de entrada/salida JSON.
3. Cambiar `GlobalExceptionHandler` de `@ControllerAdvice` a `@RestControllerAdvice`
   (o crear uno nuevo solo para el prefijo `/api/**`).
4. Añadir configuración CORS en `SecurityConfig`.
5. Añadir el endpoint `POST /api/auth/login` que responda JSON.
6. Verificar todos los endpoints con Postman o curl antes de tocar Angular.

**Resultado al final de Fase 1:** el backend sirve HTML (Thymeleaf) Y JSON (REST) simultáneamente.

---

### Fase 2 — Crear el proyecto Angular mínimo

**Objetivo:** Angular arranca, puede hacer login y ver la lista de alumnos.

**Pasos:**

1. Crear el proyecto Angular con `ng new frontend --routing`.
2. Crear `AuthService` con `login()` y `logout()`.
3. Crear `AuthGuard` que redirige a `/login` si no hay sesión.
4. Crear `AlumnosService` con `getAll()`: `GET /api/alumnos`.
5. Crear componente `LoginComponent` con formulario reactivo.
6. Crear componente `AlumnosListaComponent` que llame al servicio y muestre la tabla.
7. Configurar rutas con `AuthGuard`.

---

### Fase 3 — Completar los CRUD en Angular

**Objetivo:** todos los formularios y acciones de alumnos, cursos y matrículas funcionan.

**Pasos:**

1. Completar `AlumnoFormComponent` para crear y editar (reutiliza el mismo componente,
   distinto comportamiento según si hay `:id` en la URL).
2. Implementar confirmación de borrado (reemplaza el `onclick="return confirm()"` de Thymeleaf).
3. Repetir para `CursosModule` y `MatriculasModule`.
4. Crear el `NavbarComponent` con lógica de roles (mostrar/ocultar botones según rol).
5. Crear `AlertComponent` para mensajes de éxito/error (reemplaza los flash attributes de Spring).
6. Crear `ErrorInterceptor` que captura `401` y redirige a login, y `500` que muestra un toast.

---

### Fase 4 — Eliminar Thymeleaf del backend

**Objetivo:** el backend es una API REST pura, Angular es el único frontend.

**Pasos:**

1. Eliminar todas las clases `@Controller` (NO los `@RestController`).
2. Eliminar todas las plantillas HTML del directorio `resources/templates/`.
3. Eliminar `spring-boot-starter-thymeleaf` y `thymeleaf-extras-springsecurity6` del `pom.xml`.
4. Ajustar `SecurityConfig` para eliminar `formLogin` y `logout` HTML.
5. Borrar la carpeta `web/form/` (los `AlumnoForm`, `CursoForm`, etc. ya no se usan).
6. Mover el CSS existente o reemplazarlo por estilos Angular.

---

### Fase 5 — Despliegue conjunto (opcional)

Para un entorno de producción donde solo hay un servidor, Angular puede compilarse dentro del JAR:

```xml
<!-- pom.xml: plugin para compilar Angular antes de empaquetar Spring Boot -->
<plugin>
    <groupId>com.github.eirslett</groupId>
    <artifactId>frontend-maven-plugin</artifactId>
    <version>1.15.0</version>
    <configuration>
        <workingDirectory>frontend</workingDirectory>
        <installDirectory>target</installDirectory>
    </configuration>
    <executions>
        <execution>
            <id>install node and npm</id>
            <goals><goal>install-node-and-npm</goal></goals>
            <configuration><nodeVersion>v20.17.0</nodeVersion></configuration>
        </execution>
        <execution>
            <id>npm install</id>
            <goals><goal>npm</goal></goals>
        </execution>
        <execution>
            <id>npm build</id>
            <goals><goal>npm</goal></goals>
            <configuration><arguments>run build</arguments></configuration>
        </execution>
    </executions>
</plugin>
```

El resultado de `ng build` se copia a `resources/static/` y Spring sirve Angular como estático.

---

## 6. Código de referencia — Spring Boot

### AlumnoApiController (reemplaza a AlumnoController)

```java
@RestController
@RequestMapping("/api/alumnos")
public class AlumnoApiController {

    private final AlumnoService alumnoService;

    public AlumnoApiController(AlumnoService alumnoService) {
        this.alumnoService = alumnoService;
    }

    // GET /api/alumnos → lista todos
    @GetMapping
    public List<AlumnoResponseDto> listar() {
        return alumnoService.listar()
                .stream()
                .map(AlumnoResponseDto::from)
                .toList();
    }

    // GET /api/alumnos/{id} → uno por id
    @GetMapping("/{id}")
    public AlumnoResponseDto buscar(@PathVariable Integer id) {
        return AlumnoResponseDto.from(alumnoService.buscarPorId(id));
    }

    // POST /api/alumnos → crear
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public AlumnoResponseDto crear(@Valid @RequestBody AlumnoRequestDto dto) {
        return AlumnoResponseDto.from(alumnoService.crear(dto));
    }

    // PUT /api/alumnos/{id} → actualizar
    @PutMapping("/{id}")
    public AlumnoResponseDto actualizar(@PathVariable Integer id,
                                        @Valid @RequestBody AlumnoRequestDto dto) {
        return AlumnoResponseDto.from(alumnoService.actualizar(id, dto));
    }

    // DELETE /api/alumnos/{id} → eliminar
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void eliminar(@PathVariable Integer id) {
        alumnoService.borrar(id);
    }
}
```

### AuthApiController

```java
@RestController
@RequestMapping("/api/auth")
public class AuthApiController {

    private final UsuarioService usuarioService;
    private final AuthenticationManager authenticationManager;

    // POST /api/auth/login
    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequestDto dto,
                                   HttpServletRequest request) {
        Authentication auth = authenticationManager.authenticate(
            new UsernamePasswordAuthenticationToken(dto.username(), dto.password())
        );
        SecurityContextHolder.getContext().setAuthentication(auth);
        // La sesión se crea automáticamente con sesión+cookie.
        // Con JWT aquí se generaría el token y se devolvería en el body.
        return ResponseEntity.ok(Map.of("username", auth.getName(),
                                        "rol", auth.getAuthorities()));
    }

    // GET /api/auth/me → usuario actual
    @GetMapping("/me")
    public ResponseEntity<?> me(@AuthenticationPrincipal UserDetails user) {
        if (user == null) return ResponseEntity.status(401).build();
        return ResponseEntity.ok(Map.of("username", user.getUsername(),
                                        "roles", user.getAuthorities()));
    }

    // POST /api/auth/logout
    @PostMapping("/logout")
    public ResponseEntity<?> logout(HttpServletRequest request) {
        request.getSession().invalidate();
        SecurityContextHolder.clearContext();
        return ResponseEntity.ok(Map.of("mensaje", "Sesión cerrada"));
    }

    // POST /api/auth/register
    @PostMapping("/register")
    @ResponseStatus(HttpStatus.CREATED)
    public ResponseEntity<?> register(@Valid @RequestBody RegisterRequestDto dto) {
        usuarioService.registrar(dto);
        return ResponseEntity.status(HttpStatus.CREATED)
                             .body(Map.of("mensaje", "Usuario registrado"));
    }
}
```

---

## 7. Código de referencia — Angular

### AlumnosService (llama a la API)

```typescript
// features/alumnos/alumnos.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Alumno } from '../../core/models/alumno.model';

@Injectable({ providedIn: 'root' })
export class AlumnosService {
  private readonly API = 'http://localhost:8080/api/alumnos';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Alumno[]> {
    return this.http.get<Alumno[]>(this.API);
  }

  getById(id: number): Observable<Alumno> {
    return this.http.get<Alumno>(`${this.API}/${id}`);
  }

  create(alumno: Partial<Alumno>): Observable<Alumno> {
    return this.http.post<Alumno>(this.API, alumno);
  }

  update(id: number, alumno: Partial<Alumno>): Observable<Alumno> {
    return this.http.put<Alumno>(`${this.API}/${id}`, alumno);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API}/${id}`);
  }
}
```

### AlumnosListaComponent (equivalente a lista.html)

```typescript
// features/alumnos/alumnos-lista/alumnos-lista.component.ts
import { Component, OnInit } from '@angular/core';
import { AlumnosService } from '../alumnos.service';
import { AuthService } from '../../../core/auth/auth.service';
import { Alumno } from '../../../core/models/alumno.model';

@Component({
  selector: 'app-alumnos-lista',
  templateUrl: './alumnos-lista.component.html'
})
export class AlumnosListaComponent implements OnInit {
  alumnos: Alumno[] = [];
  mensaje: string | null = null;
  error: string | null = null;

  constructor(
    private alumnosService: AlumnosService,
    public auth: AuthService   // para controlar visibilidad de botones por rol
  ) {}

  ngOnInit(): void {
    this.alumnosService.getAll().subscribe({
      next: data => this.alumnos = data,
      error: () => this.error = 'Error cargando alumnos'
    });
  }

  eliminar(id: number): void {
    if (!confirm('¿Eliminar este alumno?')) return;
    this.alumnosService.delete(id).subscribe({
      next: () => {
        this.alumnos = this.alumnos.filter(a => a.id !== id);
        this.mensaje = 'Alumno eliminado correctamente';
      },
      error: err => this.error = err.error?.error ?? 'Error al eliminar'
    });
  }
}
```

```html
<!-- features/alumnos/alumnos-lista/alumnos-lista.component.html -->
<div class="container mt-4">
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1>Alumnos</h1>
    <a *ngIf="auth.isAdmin()" routerLink="/alumnos/nuevo" class="btn btn-primary">
      Nuevo alumno
    </a>
  </div>

  <div *ngIf="mensaje" class="alert alert-success">{{ mensaje }}</div>
  <div *ngIf="error" class="alert alert-danger">{{ error }}</div>

  <table class="table table-hover">
    <thead>
      <tr>
        <th>#</th>
        <th>Nombre</th>
        <th>Email</th>
        <th>Fecha nacimiento</th>
        <th *ngIf="auth.isAdmin()">Acciones</th>
      </tr>
    </thead>
    <tbody>
      <tr *ngFor="let alumno of alumnos">
        <td>{{ alumno.id }}</td>
        <td>{{ alumno.nombre }}</td>
        <td>{{ alumno.email }}</td>
        <td>{{ alumno.fechaNacimiento | date:'dd/MM/yyyy' }}</td>
        <td *ngIf="auth.isAdmin()">
          <a [routerLink]="['/alumnos', alumno.id, 'editar']" class="btn btn-sm btn-warning me-2">
            Editar
          </a>
          <button (click)="eliminar(alumno.id)" class="btn btn-sm btn-danger">
            Eliminar
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</div>
```

### AuthGuard (protege rutas privadas)

```typescript
// core/auth/auth.guard.ts
import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from './auth.service';

@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
  constructor(private auth: AuthService, private router: Router) {}

  canActivate(): boolean {
    if (this.auth.isLoggedIn()) return true;
    this.router.navigate(['/login']);
    return false;
  }
}
```

### Configuración de rutas principales

```typescript
// app-routing.module.ts
const routes: Routes = [
  { path: '', redirectTo: '/alumnos', pathMatch: 'full' },
  { path: 'login', loadChildren: () => import('./auth/auth.module').then(m => m.AuthModule) },
  {
    path: 'alumnos',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/alumnos/alumnos.module').then(m => m.AlumnosModule)
  },
  {
    path: 'cursos',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/cursos/cursos.module').then(m => m.CursosModule)
  },
  {
    path: 'matriculas',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/matriculas/matriculas.module').then(m => m.MatriculasModule)
  },
];
```

---

## 8. Puntos de atención y riesgos

### Problema N+1 en matrículas

El `MatriculaController` actual delega en `MatriculaService.listar()` que usa `@EntityGraph` en el
repositorio para cargar `alumno` y `curso` en una sola consulta. Esto debe mantenerse en el
`MatriculaApiController` — usar el DTO `MatriculaResponseDto.from(m)` dentro de una transacción
activa del servicio, no en el controlador.

### Serialización de fechas Java ↔ JSON

`LocalDate` y `BigDecimal` de las entidades Java se serializan bien a JSON, pero hay que asegurarse
de que Jackson los trata correctamente. En `application.properties`:
```properties
spring.jackson.serialization.write-dates-as-timestamps=false
```
Esto devuelve fechas como `"2025-03-15"` (ISO-8601), compatible con el tipo `string` de TypeScript.

### CSRF con Angular y sesión cookie

Si se elige Opción A (sesión + cookie), Angular debe leer el token CSRF de la cookie
`XSRF-TOKEN` y enviarlo en la cabecera `X-XSRF-TOKEN`. Angular tiene soporte nativo para esto
con `HttpClientXsrfModule`:

```typescript
// app.module.ts
imports: [
  HttpClientModule,
  HttpClientXsrfModule.withOptions({
    cookieName: 'XSRF-TOKEN',
    headerName: 'X-XSRF-TOKEN'
  })
]
```

### Navegación directa a rutas Angular en producción

Si Angular se sirve desde Spring Boot y el usuario navega directamente a
`http://localhost:8080/alumnos`, Spring busca un mapeo para `/alumnos` y no lo encuentra
(404). Solución: añadir un `SpaController` en Spring que devuelve `index.html` para cualquier
ruta no-API:

```java
@Controller
public class SpaController {
    @GetMapping(value = "/{path:[^\\.]*}")
    public String forwardToAngular() {
        return "forward:/index.html";
    }
}
```

### Roles en Angular — no es seguridad real

Ocultar botones en Angular según el rol (`auth.isAdmin()`) es solo UX. La seguridad real está
siempre en el backend (`SecurityConfig`). Un usuario malicioso puede manipular el estado del
cliente. Por eso los endpoints `POST`, `PUT`, `DELETE` deben seguir protegidos con
`.hasRole("ADMIN")` en el `SecurityFilterChain`.

---

## Resumen visual de la migración

```
ANTES (Thymeleaf MVC)              DESPUÉS (Angular SPA + API REST)
─────────────────────────          ──────────────────────────────────

Navegador                          Angular (localhost:4200)
  │                                  │  HttpClient → JSON
  │  HTML completo                    │  
  ▼                                  ▼
@Controller                        @RestController
  │  Model + RedirectAttributes       │  ResponseEntity<DTO>
  ▼                                  ▼
Thymeleaf (templates/)             ── ELIMINADO ──
  │  renderiza HTML                    
  ▼                                  
@Service  ←─────────────────────→  @Service  (sin cambios)
@Repository ◄──────────────────►   @Repository  (sin cambios)
SQLite ◄────────────────────────►  SQLite  (sin cambios)
```

La clave de la migración es que **el 60% del código backend no cambia**: entidades, repositorios,
servicios y la lógica de negocio permanecen exactamente igual. Solo cambia la capa web.
