package com.curso.pfsqlite.web;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: HomeController  |  CAPA: Web (Controlador MVC)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: Controlador de navegación inicial
// ? Mapea la ruta raíz "/" a la página de bienvenida de la aplicación.
// ? Es el primer controlador que un alumno debería estudiar porque es el más simple.
// ? Mantenerlo separado evita mezclar el concepto de routing con la complejidad del CRUD.

// * 🧠 TEORÍA: Flujo de una petición GET sencilla
// ? 1) Usuario accede a http://localhost:8080/
// ? 2) Spring busca un @GetMapping("/") que coincida
// ? 3) Ejecuta home() → devuelve el nombre lógico "index"
// ? 4) Thymeleaf resuelve "index" → templates/index.html y renderiza la página

@Controller
public class HomeController {

    // * @GetMapping("/") → mapea el método a la ruta raíz de la aplicación
    @GetMapping("/")
    public String home() {
        // * String "index" → nombre lógico que Thymeleaf resuelve a
        // templates/index.html
        return "index";
    }
}
