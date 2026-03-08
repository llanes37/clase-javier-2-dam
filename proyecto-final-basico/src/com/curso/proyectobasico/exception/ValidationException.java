package com.curso.proyectobasico.exception;

/*
 * Excepcion especifica para errores de negocio (validaciones).
 */
public class ValidationException extends RuntimeException {
    public ValidationException(String message) {
        super(message);
    }
}

