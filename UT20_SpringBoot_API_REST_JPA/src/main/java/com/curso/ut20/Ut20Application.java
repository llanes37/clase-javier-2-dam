package com.curso.ut20;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * //! UT20 — SPRING BOOT API REST CON JPA, VALIDACIÓN Y SWAGGER
 * ? Proyecto educativo que demuestra las mejores prácticas de Spring Boot
 *
 * * ARQUITECTURA DEL PROYECTO:
 *   - model/        → Entidades JPA (Usuario, Producto)
 *   - repository/   → Interfaces de acceso a datos (Spring Data JPA)
 *   - controller/   → Endpoints REST (@RestController)
 *   - exception/    → Manejo global de errores (@ControllerAdvice)
 *
 * ! TECNOLOGÍAS UTILIZADAS:
 *   ✓ Spring Boot 3.3.4      - Framework principal
 *   ✓ Spring Data JPA        - Persistencia de datos
 *   ✓ Hibernate              - ORM (Object-Relational Mapping)
 *   ✓ H2 Database            - Base de datos en memoria
 *   ✓ Bean Validation        - Validaciones (@Valid, @NotBlank, @Min)
 *   ✓ Swagger/OpenAPI        - Documentación automática de API
 *
 * ? ENDPOINTS DISPONIBLES:
 *   - GET/POST/PUT/DELETE /api/usuarios   → CRUD de usuarios
 *   - GET/POST/PUT/DELETE /api/productos  → CRUD de productos
 *
 * ? RECURSOS ÚTILES:
 *   - API: http://localhost:8080/api/usuarios
 *   - Swagger UI: http://localhost:8080/swagger-ui/index.html
 *   - H2 Console: http://localhost:8080/h2-console
 *
 * TODO: Mejoras sugeridas:
 *   - Añadir Spring Security (autenticación y autorización)
 *   - Implementar capa de servicios (@Service)
 *   - Añadir DTOs para separar modelo de datos de modelo de negocio
 *   - Implementar paginación (Pageable)
 *   - Añadir tests unitarios y de integración
 *   - Configurar perfiles (dev, prod)
 */
@SpringBootApplication
// * @SpringBootApplication combina 3 anotaciones:
// * 1. @Configuration    - Indica que esta clase define configuración
// * 2. @EnableAutoConfiguration - Activa la configuración automática de Spring Boot
// * 3. @ComponentScan    - Escanea el paquete y subpaquetes buscando componentes (@RestController, @Repository, etc.)
public class Ut20Application {

    /**
     * ! MÉTODO MAIN - PUNTO DE ENTRADA DE LA APLICACIÓN
     * ? Arranca el servidor embebido de Tomcat y configura el contexto de Spring
     *
     * * Proceso de arranque:
     * 1. SpringApplication.run() crea el contexto de Spring
     * 2. Escanea componentes (@RestController, @Repository, @ControllerAdvice)
     * 3. Configura la base de datos H2 según application.properties
     * 4. Crea las tablas automáticamente (hibernate.ddl-auto=update)
     * 5. Levanta el servidor Tomcat en el puerto 8080
     * 6. Expone los endpoints REST definidos en los controladores
     *
     * @param args Argumentos de línea de comandos (opcional)
     */
    public static void main(String[] args) {
        // * Arranca la aplicación Spring Boot
        SpringApplication.run(Ut20Application.class, args);

        // * Mensaje informativo en consola
        System.out.println("\n" +
                "╔════════════════════════════════════════════════════════════════╗\n" +
                "║  🚀 APLICACIÓN SPRING BOOT INICIADA CORRECTAMENTE             ║\n" +
                "╠════════════════════════════════════════════════════════════════╣\n" +
                "║  📍 API REST:       http://localhost:8080/api/usuarios        ║\n" +
                "║  📍 API REST:       http://localhost:8080/api/productos       ║\n" +
                "║  📚 Swagger UI:     http://localhost:8080/swagger-ui/index.html║\n" +
                "║  🗄️  H2 Console:     http://localhost:8080/h2-console         ║\n" +
                "╠════════════════════════════════════════════════════════════════╣\n" +
                "║  💡 Tip: Usa Swagger UI para probar los endpoints             ║\n" +
                "║  🔑 H2 JDBC URL: jdbc:h2:mem:ut20db                           ║\n" +
                "║  👤 Usuario H2: sa (sin contraseña)                           ║\n" +
                "╚════════════════════════════════════════════════════════════════╝\n");
    }
}
