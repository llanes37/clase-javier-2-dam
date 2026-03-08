/*
 * ******************************************************************************************
 * 📘 Curso — Entidad del dominio
 * Campos: id, nombre, tipo (ONLINE/PRESENCIAL), fechas (inicio/fin), precio.
 *
 * Notas:
 * - Reglas de negocio en controlador (precio >= 0, fin >= inicio).
 * - equals/hashCode por id.
 *
 * TODO Alumno
 * - [ ] Añadir helper getDuracionDias().
 * - [ ] Validar en setPrecio que no sea negativo (si no rompe lógica existente).
 * ******************************************************************************************
 */
package com.curso.proyectofinal.model;

import java.time.LocalDate;
import java.util.Objects;

/**
 * Curso con tipo, fechas y precio.
 */
public class Curso {
    private String id;          // UUID
    private String nombre;
    private CursoTipo tipo;
    private LocalDate fechaInicio;
    private LocalDate fechaFin;
    private double precio;

    public Curso() {}

    public Curso(String id, String nombre, CursoTipo tipo, LocalDate fechaInicio, LocalDate fechaFin, double precio) {
        this.id = id;
        this.nombre = nombre;
        this.tipo = tipo;
        this.fechaInicio = fechaInicio;
        this.fechaFin = fechaFin;
        this.precio = precio;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public CursoTipo getTipo() { return tipo; }
    public void setTipo(CursoTipo tipo) { this.tipo = tipo; }

    public LocalDate getFechaInicio() { return fechaInicio; }
    public void setFechaInicio(LocalDate fechaInicio) { this.fechaInicio = fechaInicio; }

    public LocalDate getFechaFin() { return fechaFin; }
    public void setFechaFin(LocalDate fechaFin) { this.fechaFin = fechaFin; }

    public double getPrecio() { return precio; }
    public void setPrecio(double precio) { 
        // * Setter simple; la regla precio >= 0 se aplica en el controlador al crear/actualizar.
        this.precio = precio; 
    }

    @Override
    public String toString() {
        return "Curso{" +
                "id='" + id + '\'' +
                ", nombre='" + nombre + '\'' +
                ", tipo=" + tipo +
                ", fechaInicio=" + fechaInicio +
                ", fechaFin=" + fechaFin +
                ", precio=" + precio +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Curso curso = (Curso) o;
        return Objects.equals(id, curso.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
