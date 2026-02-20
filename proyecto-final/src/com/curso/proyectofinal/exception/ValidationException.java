package com.curso.proyectofinal.exception;

/*
 * ******************************************************************************************
 * 📘 ValidationException — Excepción de validación de negocio
 * Usada para reglas de dominio (duplicados, fechas inválidas, etc.).
 *
 * TODO Alumno
 * - [ ] Añadir códigos de error (enum) si quieres tipificar casos.
 * ******************************************************************************************
 */
/** Excepción de validación específica para la capa de negocio. */
public class ValidationException extends RuntimeException {
    // * Usada por controladores para indicar contravalidaciones de negocio (no errores técnicos).
    // ? Podríamos ampliar con códigos o datos estructurados si hace falta.
    public ValidationException(String message) { super(message); }
}
