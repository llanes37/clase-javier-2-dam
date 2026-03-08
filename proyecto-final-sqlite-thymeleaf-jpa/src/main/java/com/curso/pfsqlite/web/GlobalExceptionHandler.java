package com.curso.pfsqlite.web;

import com.curso.pfsqlite.service.BusinessException;
import com.curso.pfsqlite.service.NotFoundException;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: GlobalExceptionHandler  |  CAPA: Web (Manejo de Errores)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: ¿Qué es @ControllerAdvice?
// ? Es una anotación que convierte esta clase en un manejador global de excepciones.
// ? Intercepta CUALQUIER excepción lanzada en CUALQUIER @Controller de la aplicación.
// ? Sin esta clase, una excepción no capturada mostraría la página de error blanca
// ? de Spring (Whitelabel Error Page) con el stack trace completo al usuario.

// * 🧠 TEORÍA: ¿Por qué separar NotFoundException de BusinessException?
// ? Tienen significado distinto en el dominio:
// ?   - NotFoundException  → el recurso no existe (típicamente HTTP 404).
// ?   - BusinessException  → la operación violó una regla de negocio (HTTP 422/400).
// ? Separarlos permite dar títulos diferentes y,  en el futuro, devolver códigos
// ? HTTP correctos si se añade una API REST al proyecto.

@ControllerAdvice
public class GlobalExceptionHandler {

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 HANDLER 1: NotFoundException → el recurso solicitado no existe en BD
    // ─────────────────────────────────────────────────────────────────────────

    // ? @ExceptionHandler indica a Spring qué tipo de excepción captura este
    // método.
    // ? Spring elige SIEMPRE el handler más específico que encuentre.
    @ExceptionHandler(NotFoundException.class)
    public String handleNotFound(NotFoundException ex, Model model) {
        // * Título específico para que el usuario entienda que el recurso no se
        // encontró
        model.addAttribute("titulo", "Recurso no encontrado");
        // * Mensaje descriptivo que viene del service (ej: "Alumno no encontrado")
        model.addAttribute("mensaje", ex.getMessage());
        // * Devuelve el nombre lógico de la vista → Thymeleaf lo resuelve a
        // templates/error.html
        return "error";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 HANDLER 2: BusinessException → la operación violó una regla de negocio
    // ─────────────────────────────────────────────────────────────────────────

    // ! ⚠️ NOTA: NotFoundException extiende BusinessException.
    // ! Spring elige el handler más específico primero, por lo que handleNotFound()
    // ! siempre tiene prioridad sobre este método para excepciones
    // NotFoundException.
    @ExceptionHandler(BusinessException.class)
    public String handleBusiness(BusinessException ex, Model model) {
        model.addAttribute("titulo", "Regla de negocio");
        model.addAttribute("mensaje", ex.getMessage());
        return "error";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 HANDLER 3: Exception genérica → red de seguridad para errores
    // inesperados
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: ¿Por qué necesitamos este handler genérico?
    // ? Captura cualquier excepción no prevista (NullPointerException, error de BD,
    // etc.)
    // ? Sin él, el usuario vería el stack trace completo en pantalla.
    // ! ⚠️ En producción NUNCA debemos exponer información técnica interna al
    // usuario.
    // ! ⚠️ Aquí NO mostramos ex.getMessage() porque podría contener datos
    // sensibles.
    @ExceptionHandler(Exception.class)
    public String handleAny(Exception ex, Model model) {
        // TODO: añadir Logger SLF4J aquí para registrar el error completo en los logs
        // del servidor
        // * Mensaje genérico controlado → nunca revelamos detalles técnicos al usuario
        // final
        model.addAttribute("titulo", "Error inesperado");
        model.addAttribute("mensaje", "Ha ocurrido un error interno. Por favor, informa al administrador.");
        return "error";
    }
}
