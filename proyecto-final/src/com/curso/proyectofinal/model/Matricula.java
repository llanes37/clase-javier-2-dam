/*
 * ******************************************************************************************
 * 📘 Matricula — Entidad del dominio
 * Une Alumno y Curso, con fecha y estado.
 *
 * Notas:
 * - Controlador aplica reglas de ventana temporal y estados.
 * - equals/hashCode por id.
 *
 * TODO Alumno
 * - [ ] Añadir helper isActiva().
 * - [ ] Añadir invariantes simples en setters (ej.: estado no null).
 * ******************************************************************************************
 */
package com.curso.proyectofinal.model;

import java.time.LocalDate;
import java.util.Objects;

/**
 * Matrícula que une Alumno y Curso.
 */
public class Matricula {
    private String id;          // UUID
    private String alumnoId;
    private String cursoId;
    private LocalDate fechaMatricula;
    private EstadoMatricula estado;

    public Matricula() {}

    public Matricula(String id, String alumnoId, String cursoId, LocalDate fechaMatricula, EstadoMatricula estado) {
        this.id = id;
        this.alumnoId = alumnoId;
        this.cursoId = cursoId;
        this.fechaMatricula = fechaMatricula;
        this.estado = estado;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getAlumnoId() { return alumnoId; }
    public void setAlumnoId(String alumnoId) { this.alumnoId = alumnoId; }

    public String getCursoId() { return cursoId; }
    public void setCursoId(String cursoId) { this.cursoId = cursoId; }

    public LocalDate getFechaMatricula() { return fechaMatricula; }
    public void setFechaMatricula(LocalDate fechaMatricula) { this.fechaMatricula = fechaMatricula; }

    public EstadoMatricula getEstado() { return estado; }
    public void setEstado(EstadoMatricula estado) { 
        // * Cambio de estado simple; las reglas para transiciones deben estar en el controlador.
        this.estado = estado; 
    }

    @Override
    public String toString() {
        return "Matricula{" +
                "id='" + id + '\'' +
                ", alumnoId='" + alumnoId + '\'' +
                ", cursoId='" + cursoId + '\'' +
                ", fechaMatricula=" + fechaMatricula +
                ", estado=" + estado +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Matricula that = (Matricula) o;
        return Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
