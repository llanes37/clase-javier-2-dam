package com.curso.pfsqlite.web.form;

import jakarta.validation.constraints.NotNull;
import org.springframework.format.annotation.DateTimeFormat;

import java.time.LocalDate;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: MatriculaForm  |  CAPA: Web (DTO de Formulario)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: DTO para matricular un alumno en un curso
// ? Solo contiene los campos que el formulario envía: alumnoId, cursoId, fecha.
// ? El service se encarga de buscar las entidades reales en BD con esos IDs.

// * 🧠 TEORÍA: ¿Por qué la fecha es opcional?
// ? Si el usuario no selecciona fecha, el service usa LocalDate.now() como valor por defecto.
// ? Esto simplifica el formulario para el caso más habitual (matricularse "hoy").

// TODO: agregar campo de observaciones para casos administrativos (ejercicio intermedio)

public class MatriculaForm {

    // * @NotNull → el usuario DEBE seleccionar un alumno del <select>
    @NotNull(message = "Debes seleccionar un alumno")
    private Long alumnoId;

    // * @NotNull → el usuario DEBE seleccionar un curso del <select>
    @NotNull(message = "Debes seleccionar un curso")
    private Long cursoId;

    // * Campo opcional → si es null, el service usa LocalDate.now() como fecha por
    // defecto
    // ? @DateTimeFormat indica a Spring cómo parsear el input HTML de tipo date
    // (yyyy-MM-dd)
    @DateTimeFormat(iso = DateTimeFormat.ISO.DATE)
    private LocalDate fechaMatricula;

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GETTERS Y SETTERS
    // ─────────────────────────────────────────────────────────────────────────

    public Long getAlumnoId() {
        return alumnoId;
    }

    public void setAlumnoId(Long alumnoId) {
        this.alumnoId = alumnoId;
    }

    public Long getCursoId() {
        return cursoId;
    }

    public void setCursoId(Long cursoId) {
        this.cursoId = cursoId;
    }

    public LocalDate getFechaMatricula() {
        return fechaMatricula;
    }

    public void setFechaMatricula(LocalDate fechaMatricula) {
        this.fechaMatricula = fechaMatricula;
    }
}
