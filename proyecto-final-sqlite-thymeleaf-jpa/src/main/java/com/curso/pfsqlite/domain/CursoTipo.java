package com.curso.pfsqlite.domain;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 ENUM: CursoTipo  |  CAPA: Domain (Modelo)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: ¿Qué es un enum en Java?
// ? Un enum es un tipo especial que define un conjunto fijo de constantes con nombre.
// ? Aquí define la modalidad de impartición de un curso: solo puede ser ONLINE o PRESENCIAL.

// * 🧠 TEORÍA: ¿Por qué usar enum en lugar de un String?
// ? Con String, nadie impide que alguien escriba "online", "En Línea" o "presencal" (con typo).
// ? Con enum, el compilador garantiza que el valor siempre será ONLINE o PRESENCIAL.
// ? Además, JPA lo persiste como texto legible en la BD gracias a @Enumerated(EnumType.STRING).

// TODO: añadir tipo HIBRIDO si el temario lo requiere en el futuro

public enum CursoTipo {
    ONLINE,
    PRESENCIAL
}
