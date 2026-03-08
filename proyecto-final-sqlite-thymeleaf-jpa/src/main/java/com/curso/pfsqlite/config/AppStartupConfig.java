package com.curso.pfsqlite.config;

import org.springframework.boot.ApplicationRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.nio.file.Files;
import java.nio.file.Path;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: AppStartupConfig  |  CAPA: Config (Infraestructura)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: ¿Qué es @Configuration?
// ? Indica a Spring que esta clase contiene definiciones de beans (@Bean).
// ? Spring la procesa durante el arranque y registra los beans que define.

// * 🧠 TEORÍA: ¿Qué es ApplicationRunner?
// ? Es un bean funcional que se ejecuta UNA SOLA VEZ al arrancar la aplicación,
// ? después de que el contexto de Spring esté completamente cargado.
// ? Perfecto para tareas de inicialización: crear directorios, verificar conexiones, etc.

// ! ⚠️ SQLite usa un fichero local (data/app.db) para almacenar la base de datos.
// ! Si la carpeta `data/` no existe al arrancar, SQLite puede fallar al crear el fichero.
// ! Este bean se asegura de que la carpeta exista ANTES de que JPA abra la conexión.

@Configuration
public class AppStartupConfig {

    // * @Bean registra el resultado del método como un componente gestionado por
    // Spring
    @Bean
    ApplicationRunner ensureDataDirectory() {
        return args -> {
            // * Ruta relativa a la raíz del proyecto → crea la carpeta `data/` si no existe
            Path dataDir = Path.of("data");
            if (!Files.exists(dataDir)) {
                // * createDirectories() crea el directorio y todos los padres necesarios
                Files.createDirectories(dataDir);
            }
        };
    }
}
