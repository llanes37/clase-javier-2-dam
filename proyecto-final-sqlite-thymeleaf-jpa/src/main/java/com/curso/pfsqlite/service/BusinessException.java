package com.curso.pfsqlite.service;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: BusinessException  |  CAPA: Service (Excepciones de Dominio)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: Excepción de dominio para reglas de negocio incumplidas
// ? Se lanza en el service cuando una operación viola una regla de negocio:
// ?   - Email duplicado al crear un alumno.
// ?   - Fecha de fin anterior a la de inicio al crear un curso.
// ?   - Matrícula ACTIVA duplicada para el mismo alumno y curso.

// * 🧠 TEORÍA: ¿Por qué extends RuntimeException?
// ? RuntimeException es una excepción no comprobada (unchecked).
// ? El compilador NO obliga a capturarla con try-catch en cada capa.
// ? Esto permite que suba limpiamente hasta el GlobalExceptionHandler sin código extra.

// ! ⚠️ No usar para errores técnicos (IOException, NullPointerException, etc.)
// ! Para esos casos se usa el handler genérico de Exception en GlobalExceptionHandler.

public class BusinessException extends RuntimeException {
    public BusinessException(String message) {
        super(message);
    }
}
