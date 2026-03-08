package com.curso.pfsqlite.domain;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 ENUM: EstadoMatricula  |  CAPA: Domain (Modelo)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: Estados del ciclo de vida de una matrícula
// ? Una matrícula nace siempre en estado ACTIVA (creada por el usuario).
// ? Puede pasar a ANULADA si se cancela (borrado lógico, el registro permanece en BD).
// ? Puede pasar a FINALIZADA cuando el curso termina (operación futura / ejercicio avanzado).

// * 🧠 TEORÍA: ¿Por qué persistir como texto y no como número (ordinal)?
// ? Si lo guardamos como ORDINAL (0, 1, 2) y cambiamos el orden del enum,
// ? todos los datos existentes en la BD quedarían con significados incorrectos.
// ? Guardando como STRING ("ACTIVA", "ANULADA", "FINALIZADA") el dato es siempre legible
// ? y no se rompe si se reordena o amplía el enum en el futuro.

// TODO: modelar las transiciones válidas (ACTIVA → ANULADA/FINALIZADA) como ejercicio avanzado

public enum EstadoMatricula {
    ACTIVA,
    ANULADA,
    FINALIZADA
}
