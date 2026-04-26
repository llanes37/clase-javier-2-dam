package com.curso.pfsqlite.config;

import com.curso.pfsqlite.domain.Usuario;
import com.curso.pfsqlite.repository.UsuarioRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.password.PasswordEncoder;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: DataInitializer  |  CAPA: Config (Infraestructura)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: ¿Por qué aquí y no en Flyway SQL?
// ? BCrypt genera un hash diferente cada vez que se llama.
// ? En un script SQL tendríamos que hardcodear el hash, que es frágil y confuso.
// ? Aquí usamos el mismo PasswordEncoder que usa el resto de la app → coherencia garantizada.

// * 🧠 TEORÍA: ApplicationRunner se ejecuta UNA VEZ al arrancar, después de que el
// ? contexto de Spring (JPA, Flyway, Security) esté 100% inicializado.
// ? El `if (!exists)` hace la operación idempotente: seguro de ejecutar múltiples veces.

@Configuration
public class DataInitializer {

    private static final Logger log = LoggerFactory.getLogger(DataInitializer.class);

    // * Credenciales por defecto para el entorno didáctico/local.
    // ! ⚠️ En producción real, estos valores se leerían de variables de entorno o un vault.
    private static final String ADMIN_USERNAME = "admin";
    private static final String ADMIN_PASSWORD = "admin123";
    private static final String USER_USERNAME  = "user";
    private static final String USER_PASSWORD  = "user123";

    @Bean
    ApplicationRunner inicializarUsuarios(UsuarioRepository repo, PasswordEncoder encoder) {
        return args -> {
            if (!repo.existsByUsernameIgnoreCase(ADMIN_USERNAME)) {
                Usuario admin = new Usuario();
                admin.setUsername(ADMIN_USERNAME);
                // ! encode() genera el hash BCrypt con salt aleatorio → contraseña segura
                admin.setPassword(encoder.encode(ADMIN_PASSWORD));
                admin.setRol("ROLE_ADMIN");
                repo.save(admin);
                log.info("Usuario por defecto creado → username: '{}', rol: ROLE_ADMIN", ADMIN_USERNAME);
            }

            if (!repo.existsByUsernameIgnoreCase(USER_USERNAME)) {
                Usuario user = new Usuario();
                user.setUsername(USER_USERNAME);
                user.setPassword(encoder.encode(USER_PASSWORD));
                user.setRol("ROLE_USER");
                repo.save(user);
                log.info("Usuario por defecto creado → username: '{}', rol: ROLE_USER", USER_USERNAME);
            }
        };
    }
}
