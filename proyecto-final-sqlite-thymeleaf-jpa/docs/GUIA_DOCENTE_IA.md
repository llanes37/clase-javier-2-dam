# GUIA DOCENTE â€” Spring Boot + SQLite + JPA + Thymeleaf

> **Este es el unico archivo que necesitas como profesor.**
> Contiene el plan de 3 sesiones, como leer el codigo con los alumnos,
> la rubrica de evaluacion y una biblioteca completa de prompts de IA
> para expandir el proyecto en clase o como trabajo autonomo.
>
> Los ejercicios con sus tablas de archivos y casos borde estan en `EJERCICIOS.md`.

---

## 0. Antes de clase (5 min)

```bash
./mvnw spring-boot:run     # arranca la app
# Abre http://localhost:8080 y verifica que carga
# Para demo limpia: borra data/app.db antes de arrancar (Flyway lo recrea)
```

**Mapa mental rapido â€” di esto en voz alta al abrir el proyecto:**

```
web/         â†’ recibe peticiones HTTP, valida formularios, devuelve vistas
service/     â†’ AQUI viven las reglas de negocio (nunca en el controller)
repository/  â†’ Spring genera el SQL, nosotros declaramos el metodo
domain/      â†’ entidades JPA: solo estado, sin logica
db/migration â†’ esquema SQL versionado; nunca usar ddl-auto=create
test/        â†’ cada regla de negocio tiene al menos un test
```

---

## 1. Plan de 3 sesiones

### Sesion 1 (90 min) â€” Arquitectura por capas y reglas de negocio

**Objetivo:** el alumno sabe donde va cada cosa y por que el service existe.

| Tiempo | Actividad |
|---|---|
| 15 min | Dibuja el diagrama de capas en pizarra. Pregunta: "Â¿donde irias a buscar la regla de email unico?" |
| 20 min | Lee `AlumnoService` en voz alta. Explica `// *`, `// !`, `// ?`. Por que `Logger` y no `System.out`. |
| 30 min | Demo en vivo: crea alumno â†’ email duplicado â†’ email invalido â†’ borrado protegido. Lee el log en consola. |
| 25 min | Ejercicio E1 o E2 de `EJERCICIOS.md`. |

**Preguntas que forzaran la reflexion:**
- "Â¿Que pasaria si la validacion de email estuviera en el controller?"
- "Â¿Por que `@Transactional(readOnly=true)` y no solo `@Transactional`?"
- "Â¿Que diferencia hay entre `BusinessException` y `NotFoundException`?"
- "Â¿Por que la regla de email unico esta en el service Y en la base de datos?"

**Checklist de salida sesion 1:**
- [ ] El alumno sabe donde viven las reglas de negocio y puede justificarlo.
- [ ] El alumno provoco un error de email duplicado y leyo el mensaje en consola (SLF4J).
- [ ] El alumno diferencia validacion de formulario (Bean Validation) de regla de negocio (service).

---

### Sesion 2 (90 min) â€” Persistencia, Flyway y el problema N+1

**Objetivo:** el alumno entiende el ciclo de vida de los datos y por que el esquema importa.

| Tiempo | Actividad |
|---|---|
| 20 min | Lee `V1__init.sql` juntos, constraint a constraint: "Â¿que regla de negocio protege esto?" |
| 20 min | Activa `show-sql=true`. Navega a `/matriculas`. Cuenta las queries en consola. |
| 20 min | Quita `@EntityGraph` de `MatriculaRepository`. Recarga. 11 queries â†’ explica N+1. Pon de nuevo `@EntityGraph`. |
| 15 min | Crea juntos una migracion `V3__agregar_telefono.sql` desde cero. |
| 15 min | Ejercicio E3 o parte de E13 de `EJERCICIOS.md`. |

**Truco demostracion N+1 (copiar y pegar en `application.properties`):**
```properties
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
```
Con 5 matriculas y sin `@EntityGraph`: ves `1 + 5 + 5 = 11` queries.
Con `@EntityGraph`: 1 sola query con JOIN. El alumno ve la diferencia en tiempo real.

**Checklist de salida sesion 2:**
- [ ] El alumno explica que hace cada constraint de `V1__init.sql`.
- [ ] El alumno vio el problema N+1 en vivo y sabe como lo soluciona `@EntityGraph`.
- [ ] El alumno creo o modifico una migracion Flyway sin romper las existentes.

---

### Sesion 3 (90 min) â€” Tests, calidad y codigo como contrato

**Objetivo:** el alumno conecta cada regla de negocio con su test y entiende que los tests son documentacion ejecutable.

| Tiempo | Actividad |
|---|---|
| 20 min | Lee `AlumnoServiceTest` en voz alta. Por cada test: "Â¿que regla verifica?" |
| 15 min | Lee `MatriculaRepositoryTest`. Explica la diferencia: Mockito (unitario) vs `@DataJpaTest` (integracion). |
| 35 min | El alumno escribe un test que falta (ejercicio E10). El profe solo orienta, no escribe. |
| 20 min | Code review colectivo del test escrito. Evalua con la rubrica. |

**Preguntas que forzaran la reflexion:**
- "Â¿Que es un mock y por que no usamos la base de datos real en tests unitarios?"
- "Â¿Que diferencia hay entre `@Mock` y `@InjectMocks`?"
- "Si borramos la validacion de duplicado ACTIVA del service, Â¿que test falla primero?"
- "Â¿Que caso borde no esta cubierto por los tests actuales?"

**Checklist de salida sesion 3:**
- [ ] El alumno escribe un test con `@ExtendWith(MockitoExtension.class)` desde cero.
- [ ] El alumno diferencia test unitario (Mockito) de test de integracion (`@DataJpaTest`).
- [ ] El alumno identifico al menos un caso borde sin test en el proyecto.

---

## 2. Como leer el codigo con los alumnos

**Orden recomendado** (del exterior al interior, de lo visible a lo oculto):

```
1. Application.java              â†’ Â¿Donde arranca Spring Boot?
2. web/*Controller.java          â†’ Â¿Que URLs existen? Â¿Que hace cada one?
3. web/form/*.java               â†’ Â¿Que datos recibe cada formulario?
4. service/*Service.java         â†’ Â¿Donde viven las reglas? (el nucleo)
5. repository/*.java             â†’ Â¿Como genera Spring el SQL?
6. domain/*.java                 â†’ Â¿Como estan estructuradas las entidades?
7. db/migration/V1__init.sql     â†’ Â¿Que protege la base de datos?
8. test/**/*Test.java            â†’ Â¿Como se verifica que todo funciona?
```

**Preguntas guiadas por archivo:**

| Archivo | Pregunta clave |
|---|---|
| `AlumnoController` | Â¿Que metodos responden a GET y cuales a POST? Â¿Por que no hay logica de negocio aqui? |
| `AlumnoService` | Â¿En que linea exacta se detecta el email duplicado? Â¿Que lanza y por que? |
| `CursoService` | Â¿Por que el mismo mensaje de error para fechas esta TAMBIEN en la DB? |
| `MatriculaService` | Â¿Por que validamos la fecha ANTES de comprobar el duplicado? Â¿Importa el orden? |
| `MatriculaRepository` | Â¿Como infiere Spring el SQL de `existsByAlumnoIdAndCursoIdAndEstado`? |
| `V1__init.sql` | Â¿Que hace el indice parcial `uk_matricula_activa`? Â¿Que ocurre si lo borramos? |
| `AlumnoServiceTest` | Â¿Por que `verify(repo, never()).save(any())` es mejor que solo `assertThrows`? |

---

## 3. Sistema de comentarios Better Comments

Instala `aaron-bond.better-comments` en VS Code para activar los colores.

| Marcador | Color | Cuando usarlo | Ejemplo real del proyecto |
|---|---|---|---|
| `// *` | Verde | Explicar flujo, que hace un bloque, teoria | `// * readOnly=true â†’ Hibernate no rastrea cambios â†’ menos memoria` |
| `// ?` | Azul | Justificar decisiones tecnicas, "Â¿por que esto?" | `// ? Â¿Por que SLF4J y no System.out? â†’ niveles configurables` |
| `// !` | Rojo | Reglas criticas, errores frecuentes, advertencias | `// ! NUNCA uses == para comparar Strings â†’ usa .equals()` |
| `// TODO` | Naranja | Mejoras futuras, ejercicios pendientes | `// TODO: aÃ±adir cupos maximos por curso` |

**Regla de oro al comentar: comenta DECISIONES, no obviedades.**
```java
// MAL (obvio): suma los dos numeros
int total = a + b;

// BIEN (decision): separamos precio base e IVA para poder cambiar el tipo impositivo
BigDecimal totalConIva = precioBase.multiply(new BigDecimal("1.21"));
```

**Actividad rapida para clase (10 min):**
1. Abre `AlumnoService`, `MatriculaService`.
2. Localiza todos los `// !` â†’ explica que riesgo protege cada uno.
3. Localiza todos los `// TODO` â†’ convierte uno en una historia de usuario.
4. AÃ±ade un `// ?` nuevo justificando una decision que no estaba comentada.

---

## 4. Rubrica de evaluacion

| Criterio | Peso | Indicadores |
|---|---|---|
| **Correctitud funcional** | 40% | Las reglas de negocio se cumplen. No se rompen flujos existentes. |
| **Arquitectura por capas** | 25% | La logica de negocio esta en `service`. Los controllers estan limpios. Los repositories solo acceden a datos. |
| **Robustez y validacion** | 20% | Errores bien manejados con mensajes claros. Validaciones en formulario Y en service. |
| **Calidad de codigo** | 15% | Nombres claros. `// *`, `// ?`, `// !` usados con significado real. Tests coherentes con `@DisplayName`. |

| Nota | Descripcion |
|---|---|
| **Sobresaliente** | Cumple todo, aporta tests adicionales, mejora el diseno y lo justifica. |
| **Notable** | Cumple casi todo, con pequeÃ±os huecos en pruebas o en UX. |
| **Aprobado** | Funciona, pero con deuda tecnica visible o capas mezcladas puntualmente. |
| **Insuficiente** | Rompe reglas de negocio existentes o mezcla logica entre capas de forma sistematica. |

---

## 5. Biblioteca de prompts de IA

> Usa estos prompts en GitHub Copilot, ChatGPT o cualquier asistente de IA.
> Sustituye los textos entre `[CORCHETES]` por el valor concreto.
> Cuanto mas contexto des, mejor sera la respuesta.

---

### 5.1 Prompts para ENTENDER el proyecto

**Explicar una clase completa:**
```
Eres un profesor de Java senior. Explica la clase [NOMBRE_CLASE] de este proyecto
a un alumno que sabe Java basico pero no conoce Spring Boot.
Usa analogias del mundo real. Explica cada metodo en no mas de 3 lineas.
Al final, plantea 3 preguntas de reflexion para el alumno.
```

**Entender una anotacion de Spring:**
```
Explica la anotacion [ANOTACION] (ej: @Transactional, @EntityGraph, @Service)
en el contexto de este proyecto.
Indica: que hace, que pasaria si la quitaramos, y donde mas se usa en este proyecto.
```

**Trazar el flujo de una peticion:**
```
Sigue el flujo completo de la peticion POST /matriculas en este proyecto.
Indica archivo por archivo, metodo por metodo, que ocurre desde que
el usuario pulsa "Guardar" hasta que ve el resultado en pantalla.
Si hay una regla de negocio que puede fallar, explicala.
```

---

### 5.2 Prompts para IMPLEMENTAR ejercicios

**Implementar un ejercicio paso a paso:**
```
Quiero resolver el ejercicio [E_NUMERO - NOMBRE] de EJERCICIOS.md en este proyecto.
Dame:
1) Diseno por capas: que cambia exactamente en cada archivo.
2) Pasos pequenos de implementacion (no mas de 5 pasos).
3) Casos borde que debo tener en cuenta.
4) Como probarlo manualmente en 2 minutos.
5) Un test unitario de ejemplo para la regla mas importante.
No hagas cambios fuera de la carpeta del proyecto actual.
No rompas ningun test existente.
```

**AÃ±adir una nueva regla de negocio:**
```
Quiero aÃ±adir esta regla de negocio al proyecto: [DESCRIPCION_REGLA].
Indica:
1) En que capa debe vivir la validacion (service, repository, DB o varias).
2) Que archivos hay que modificar.
3) Que excepcion debe lanzar si se viola la regla.
4) Como reforzarlo tambien en la base de datos (si aplica).
5) Que test unitario cubre esta regla (dame el codigo completo).
```

**AÃ±adir un campo nuevo a una entidad:**
```
Quiero aÃ±adir el campo [NOMBRE_CAMPO] de tipo [TIPO_JAVA] a la entidad [ENTIDAD].
Indica los cambios necesarios en:
1) La entidad JPA (campo, getter, setter, toString).
2) La migracion Flyway (V[N]__agregar_[campo].sql, compatible con SQLite).
3) El formulario web (AlumnoForm / CursoForm / MatriculaForm).
4) La vista Thymeleaf correspondiente.
5) Los tests que hay que actualizar.
No uses ddl-auto para el cambio de esquema.
```

---

### 5.3 Prompts para MEJORAR la calidad

**Code review de un archivo:**
```
Haz un code review estricto del archivo [NOMBRE_ARCHIVO] de este proyecto.
Prioriza los hallazgos por severidad:
1) Bugs funcionales (rompen algo).
2) Regresiones potenciales (podrian romper algo en el futuro).
3) Validaciones faltantes.
4) Deuda tecnica.
Referencia numeros de linea concretos. No cambies el codigo, solo reporta.
```

**Mejorar los comentarios Better Comments:**
```
Reviset el archivo [NOMBRE_ARCHIVO] y mejora los comentarios Better Comments.
Usa el convenio del proyecto:
- // * para explicar flujo y responsabilidades
- // ? para justificar decisiones tecnicas
- // ! para reglas criticas o errores frecuentes
- // TODO para mejoras futuras
No cambies el codigo, solo los comentarios. Comenta decisiones, no obviedades.
```

**Generar tests que faltan:**
```
Analiza la clase [NOMBRE_SERVICE] y lista todos los casos de prueba que faltan.
Para cada caso indica: nombre del test, que regla verifica, arrange/act/assert.
Luego genera el codigo completo de los 3 tests mas importantes usando
JUnit 5, Mockito y @DisplayName. Sigue el patron de los tests existentes en el proyecto.
```

---

### 5.4 Prompts para EXPANDIR el proyecto

**AÃ±adir una migracion Flyway:**
```
Necesito crear la migracion Flyway V[N]__[nombre_descriptivo].sql.
Lo que debe hacer: [descripcion].
Requisitos:
- Compatible con SQLite (sin tipos exclusivos de otros SGBD como SERIAL o UUID).
- No romper los datos de V2__seed.sql.
- Incluir comentarios SQL con -- * y -- ! segun la convencion del proyecto.
Muestra tambien como verificar que la migracion se aplico correctamente.
```

**AÃ±adir un endpoint REST:**
```
Quiero aÃ±adir un endpoint REST GET /api/[recurso] a este proyecto Spring Boot
sin eliminar los controllers Thymeleaf existentes.
Indica:
1) Que clase crear (@RestController) y donde colocarla.
2) Como reutilizar el service existente sin duplicar logica.
3) Como serializa Spring Boot la entidad a JSON (y posibles problemas con LAZY).
4) Un test de ejemplo con @WebMvcTest para este endpoint.
```

**Sustituir SQLite por PostgreSQL:**
```
Quiero crear un perfil 'prod' en este proyecto que use PostgreSQL en lugar de SQLite.
El perfil 'dev' debe seguir usando SQLite.
Indica:
1) Dependencias a aÃ±adir en pom.xml.
2) Contenido de application-dev.properties y application-prod.properties.
3) Si hay algun SQL en las migraciones Flyway incompatible con PostgreSQL.
4) Como activar cada perfil desde la linea de comandos.
```

**AÃ±adir Spring Security:**
```
Quiero proteger este proyecto con Spring Security.
Debe haber dos roles: ADMIN (puede todo) y ALUMNO (solo lectura).
Indica:
1) Dependencia a aÃ±adir en pom.xml.
2) Clase de configuracion SecurityConfig minima.
3) Como crear usuarios en memoria para pruebas.
4) Que rutas debe proteger cada rol.
5) Como aÃ±adir el formulario de login de Thymeleaf.
```

**Generar un CRUD completo para una nueva entidad:**
```
Quiero aÃ±adir la entidad [NOMBRE] con los campos [LISTA_CAMPOS] a este proyecto.
Sigue exactamente el mismo patron que Alumno:
- Entidad JPA con equals/hashCode/toString y Javadoc.
- Migracion Flyway V[N]__crear_[tabla].sql.
- Repository con los metodos necesarios para las reglas de negocio.
- Service con validaciones, Logger SLF4J y comentarios Better Comments.
- Controller MVC con GET lista, GET formulario, POST crear, POST eliminar.
- Formulario con Bean Validation.
- Vistas Thymeleaf: lista.html y nuevo.html.
- Al menos 3 tests unitarios del service.
```

---

### 5.5 Prompts de diagnostico y depuracion

**Diagnosticar un error de arranque:**
```
Al arrancar este proyecto Spring Boot obtengo el siguiente error:
[PEGA EL STACK TRACE AQUI]
Analiza el stack trace, identifica la causa raiz y proporciona
los pasos concretos para solucionarlo en este proyecto.
```

**Diagnosticar un test que falla:**
```
Este test esta fallando:
[PEGA EL CODIGO DEL TEST]
El mensaje de error es:
[PEGA EL ERROR]
Explica por que falla y como corregirlo sin cambiar la logica de negocio.
```

**Entender una LazyInitializationException:**
```
Obtuve LazyInitializationException al acceder a [CAMPO] de [ENTIDAD].
Explica por que ocurre en este proyecto (con open-in-view=false)
y proporciona 3 soluciones posibles ordenadas de mejor a peor practica.
```

---

## 6. Ideas para expandir el proyecto en clase

Estas ideas van de menos a mas complejidad. Cada una puede ser una sesion adicional o trabajo autonomo.

| # | Idea | Nuevo concepto que enseÃ±a |
|---|---|---|
| A | AÃ±adir campo `telefono` opcional a Alumno | Migracion + campo nullable + vista |
| B | Mostrar estadisticas en el home (N alumnos, N cursos, N matriculas activas) | Consultas `count()` en repository |
| C | Paginar el listado de matriculas | `Pageable`, `Page<T>`, navegacion |
| D | Exportar matriculas a CSV | `HttpServletResponse`, streams, descarga |
| E | Endpoint REST `/api/cursos` | `@RestController`, JSON, coexistencia MVC+REST |
| F | Auditoria: `creadoEn`, `modificadoEn` | `@CreationTimestamp`, `@UpdateTimestamp` |
| G | Perfiles dev/prod con PostgreSQL | `@Profile`, `application-{perfil}.properties` |
| H | Spring Security con roles ADMIN/ALUMNO | Autenticacion, autorizacion, formulario login |
| I | Soft delete en alumnos/cursos | Estado en vez de borrado fisico, filtro en queries |
| J | Internacionalizacion (i18n) | `messages.properties`, `MessageSource` |

> Para cada idea, usa el prompt correspondiente de la seccion 5.4.
