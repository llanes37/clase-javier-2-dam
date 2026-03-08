package com.curso.pfsqlite.service;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: NotFoundException  |  CAPA: Service (Excepciones de Dominio)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: NotFoundException es una variante específica de BusinessException
// ? Se lanza cuando se solicita un recurso que NO existe en la base de datos.
// ? Ejemplo: intentar borrar un alumno con id=999 que ya no existe.

// * 🧠 TEORÍA: ¿Por qué extiende BusinessException en vez de RuntimeException directamente?
// ? Hereda todos los handlers de BusinessException.
// ? Como GlobalExceptionHandler tiene un handler más específico para NotFoundException,
// ? Spring lo usa con prioridad y muestra el título "Recurso no encontrado".

// ! ⚠️ Usar esta excepción evita devolver null y empujar los errores a capas superiores.
// ! El patrón correcto es: orElseThrow(() -> new NotFoundException("Alumno no encontrado"))

public class NotFoundException extends BusinessException {
    public NotFoundException(String message) {
        super(message);
    }
}
