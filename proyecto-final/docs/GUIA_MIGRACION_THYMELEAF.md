# Guia Completa: Migrar este proyecto a Spring Boot + Thymeleaf

## 1. Objetivo
Este documento te guia para transformar `proyecto-final` (Java consola + CSV) en una aplicacion web MVC con `Spring Boot` y `Thymeleaf`, manteniendo la logica didactica que ya tienes.

Objetivo final:
- Backend web con Spring Boot.
- Vistas HTML con Thymeleaf.
- Mismos casos de uso: alumnos, cursos, matriculas.
- Sin romper tu modelo de dominio actual.

Tambien incluye prompts listos para usar con Codex (GPT-5.3).

---

## 2. Estado actual del proyecto (resumen)
Actualmente tienes:
- Entrada por consola en `src/com/curso/proyectofinal/Application.java`.
- Capas separadas: `model`, `controller` (negocio), `repository` (CSV), `view` (consola).
- Build sin Maven/Gradle (`build.bat`, `run.bat`).

Esto esta bien para didactica. Para pasar a web, hay que cambiar el arranque, la capa de presentacion y el empaquetado.

---

## 3. Estrategia recomendada (sin romper todo)
Haz la migracion en 2 fases:

1. Fase Web MVC:
- Crear proyecto Spring Boot (Maven).
- Reusar `model` y reglas de negocio.
- Crear controladores web y plantillas Thymeleaf.
- Mantener CSV temporalmente para no mezclar demasiados cambios.

2. Fase Datos (opcional ahora, recomendada despues):
- Cambiar repositorios CSV por SQLite (ver la otra guia).

Ventaja: reduces riesgo y entiendes cada cambio.

---

## 4. Estructura destino recomendada

```text
proyecto-final/
  pom.xml
  src/main/java/com/curso/proyectofinal/
    ProyectoFinalApplication.java
    model/
    service/
    repository/
    web/
      controller/
      dto/
  src/main/resources/
    templates/
      alumnos/
      cursos/
      matriculas/
    static/
      css/
    application.properties
```

Notas:
- Mueve tu logica de negocio de `controller` actual a `service` (mas limpio).
- `web/controller` solo gestiona peticiones HTTP y modelos para vista.

---

## 5. Dependencias Spring Boot minimas
En `pom.xml`:
- `spring-boot-starter-web`
- `spring-boot-starter-thymeleaf`
- `spring-boot-starter-validation`
- `spring-boot-devtools` (opcional)

Si todavia sigues con CSV en esta fase, no necesitas DB aun.

---

## 6. Paso a paso detallado

### Paso 1: Crear rama de migracion

```powershell
cd "c:\Users\MediaMarktVillaverde\Desktop\clase javier 2 dam\proyecto-final"
git checkout -b feature/spring-thymeleaf
```

### Paso 2: Inicializar Spring Boot (Maven)
Opciones:
- Desde start.spring.io y copiar base.
- O crear `pom.xml` y estructura manualmente.

Parametros recomendados:
- Group: `com.curso`
- Artifact: `proyecto-final`
- Java: `17`
- Packaging: `jar`

### Paso 3: Crear clase principal Spring Boot
Crear:
- `src/main/java/com/curso/proyectofinal/ProyectoFinalApplication.java`

Con:
- `@SpringBootApplication`
- metodo `main` con `SpringApplication.run(...)`

### Paso 4: Reubicar codigo existente
- Mover clases del dominio a `src/main/java/.../model`.
- Mover utilidades (`Validator`, `DateUtils`, excepciones).
- Extraer la logica de negocio de controladores actuales a `service`.

Patron simple:
- `AlumnoService` usa `AlumnoRepository`.
- `CursoService` usa `CursoRepository`.
- `MatriculaService` usa `MatriculaRepository` + otros repos.

### Paso 5: Crear controladores web
Crear:
- `web/controller/AlumnoWebController`
- `web/controller/CursoWebController`
- `web/controller/MatriculaWebController`

Endpoints minimos:
- `GET /` home.
- `GET /alumnos` listar.
- `GET /alumnos/nuevo` formulario.
- `POST /alumnos` crear.
- Igual para cursos y matriculas.

### Paso 6: Plantillas Thymeleaf
En `src/main/resources/templates`:
- `layout.html` (opcional)
- `home.html`
- `alumnos/lista.html`
- `alumnos/form.html`
- `cursos/lista.html`
- `cursos/form.html`
- `matriculas/lista.html`
- `matriculas/form.html`

### Paso 7: Validacion en formularios
Usa DTOs para formularios:
- `AlumnoForm`
- `CursoForm`
- `MatriculaForm`

Con anotaciones:
- `@NotBlank`, `@Email`, `@DecimalMin`, etc.

En controller web:
- `@Valid` + `BindingResult`.
- Si hay errores, volver al `form.html`.

### Paso 8: Manejo global de errores
Crear `GlobalExceptionHandler` con `@ControllerAdvice` para:
- `ValidationException`
- errores de parseo
- fallback general

### Paso 9: Recursos estaticos
- `src/main/resources/static/css/app.css`
- Estilo simple y claro para tablas/formularios.

### Paso 10: Probar flujo completo
Pruebas manuales:
- Crear/listar/borrar alumno.
- Crear/listar/borrar curso.
- Matricular y anular.
- Casos invalidos: fechas, precio, email.

---

## 7. Prompt maestro para Codex (GPT-5.3)
Copia este prompt tal cual cuando quieras que Codex haga la migracion completa por pasos:

```text
Quiero migrar este proyecto Java de consola a Spring Boot + Thymeleaf sin perder la logica actual.

Contexto del proyecto:
- Proyecto actual en: proyecto-final
- Arquitectura actual: model + controller (negocio) + repository CSV + view consola.
- Java 17.
- No uso Maven ahora.

Objetivo:
1) Convertirlo a Spring Boot Maven.
2) Mantener modelos y reglas de negocio.
3) Crear capa web con Thymeleaf para alumnos, cursos y matriculas.
4) Mantener temporalmente persistencia CSV si hace falta.
5) Dejar todo compilando y arrancando con `mvn spring-boot:run`.

Instrucciones de ejecucion:
- Haz cambios reales en archivos, no solo explicaciones.
- Muestra un plan breve y luego implementa.
- Crea/actualiza pom.xml.
- Crea clase principal @SpringBootApplication.
- Separa negocio en servicios.
- Crea controladores web MVC y templates Thymeleaf.
- Añade validacion de formularios con DTO + @Valid + BindingResult.
- Añade manejo global de errores con @ControllerAdvice.
- Incluye CSS simple.
- Al final ejecuta una verificacion (compilacion/tests si existen).
- Resume archivos tocados y comandos usados.

Restricciones:
- No borrar reglas de negocio actuales.
- No meter frontend SPA (React/Vue).
- Mantener codigo claro didactico.
```

---

## 8. Prompts cortos por etapa

### Prompt etapa 1: bootstrap Spring
```text
Convierte `proyecto-final` a estructura Spring Boot Maven con Java 17.
Crea `pom.xml`, `src/main/java`, `src/main/resources`, y clase principal `ProyectoFinalApplication`.
No hagas aun controladores web funcionales; solo deja el proyecto arrancando.
```

### Prompt etapa 2: servicios
```text
Refactoriza la logica de negocio actual para moverla de `controller` legacy a `service`.
Mantener mismas validaciones y contratos.
Actualiza imports y dependencias internas.
```

### Prompt etapa 3: Thymeleaf CRUD
```text
Crea controladores web MVC + templates Thymeleaf para alumnos, cursos y matriculas.
Rutas: listar, nuevo (form), crear, borrar/anular.
Usa DTOs con validacion y muestra errores en formulario.
```

### Prompt etapa 4: errores y calidad
```text
Implementa `@ControllerAdvice` para errores de validacion y negocio.
Mejora mensajes de error en vistas.
Revisa que toda la app compila y arranca con `mvn spring-boot:run`.
```

---

## 9. Checklist de aceptacion
Marca todo antes de cerrar:

- [ ] `mvn spring-boot:run` arranca sin errores.
- [ ] Existe pagina home en `/`.
- [ ] Alumnos: listar y crear funcional.
- [ ] Cursos: listar y crear funcional.
- [ ] Matriculas: listar y crear/anular funcional.
- [ ] Validaciones muestran error en formulario.
- [ ] No hay logica de negocio metida en controladores web.
- [ ] Codigo compila limpio.

---

## 10. Errores comunes y solucion

1. Error de codificacion de caracteres:
- Usa UTF-8 en editor y compilador.

2. Thymeleaf no encuentra templates:
- Verifica ruta exacta: `src/main/resources/templates/...`.

3. `Enum.valueOf(...)` falla con minusculas:
- Normaliza con `.toUpperCase()` antes de convertir.

4. Rutas POST sin CSRF (si luego activas Spring Security):
- De momento sin security no aplica.

5. Mezcla de capas:
- Regla: controller web no valida negocio complejo, solo delega a service.

---

## 11. Recomendacion de trabajo realista
Orden recomendado para ti:

1. Hacer Spring + Thymeleaf con CSV funcionando.
2. Entregar esa version estable.
3. En segunda rama, migrar datos a SQLite.

Asi tienes una entrega segura y luego una mejora tecnica clara.

---

## 12. Comandos utiles (Windows)

```powershell
# En la raiz de proyecto-final
mvn -v
mvn clean compile
mvn spring-boot:run
mvn test
```

Si no tienes Maven global, instala Maven o usa wrapper (`mvnw`) cuando lo tengas en proyecto.

---

## 13. Resultado esperado al final
Debes poder abrir en navegador:
- `http://localhost:8080/`
- `http://localhost:8080/alumnos`
- `http://localhost:8080/cursos`
- `http://localhost:8080/matriculas`

Con formularios funcionales, validacion visible y reglas de negocio respetadas.
