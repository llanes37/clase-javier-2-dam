package com.curso.pfsqlite;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: Application  |  PUNTO DE ENTRADA DE LA APLICACIÓN
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: @SpringBootApplication equivale a TRES anotaciones combinadas
// ? 1) @Configuration      → permite definir beans con @Bean en esta clase.
// ? 2) @EnableAutoConfiguration → Spring configura automáticamente los módulos detectados
// ?    (JPA, Thymeleaf, servidor web Tomcat embebido, etc.) según las dependencias del pom.xml.
// ? 3) @ComponentScan      → escanea este paquete y TODOS sus subpaquetes buscando clases
// ?    anotadas con @Service, @Repository, @Controller, @Component, etc.

// * 🧠 TEORÍA: Estructura de paquetes detectados automáticamente
// ? com.curso.pfsqlite           ← este paquete (Application.java)
// ? com.curso.pfsqlite.config    ← configuraciones (@Configuration)
// ? com.curso.pfsqlite.domain    ← entidades JPA (@Entity)
// ? com.curso.pfsqlite.repository ← repositorios (extienden JpaRepository)
// ? com.curso.pfsqlite.service   ← servicios de negocio (@Service)
// ? com.curso.pfsqlite.web       ← controladores MVC (@Controller)
// ? com.curso.pfsqlite.web.form  ← DTOs de formulario (sin anotación Spring)

@SpringBootApplication
public class Application {

    // * main() es el punto de entrada estándar de Java
    // ? SpringApplication.run() arranca el servidor Tomcat embebido y todo el
    // contexto Spring
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
