/*
 * ******************************************************************************************
 * 📘 Alumno — Entidad del dominio
 * Campos: id (UUID), nombre, email, fechaNacimiento (opcional).
 *
 * Notas:
 * - Las validaciones fuertes se realizan en controladores (email único, formato, etc.).
 * - equals/hashCode por id (identidad).
 *
 * TODO Alumno
 * - [ ] Añadir validación ligera en setNombre (no null/blank) si no rompe otras capas.
 * - [ ] Añadir método helper getEdad() opcional (requiere fechaNacimiento no null).
 * ******************************************************************************************
 */
package com.curso.proyectofinal.model;

import java.time.LocalDate;
import java.util.Objects;

/**
 * Alumno del sistema. Entidad simple con validaciones en controladores.
 */
public class Alumno {
    private String id;              // UUID
    private String nombre;
    private String email;
    private LocalDate fechaNacimiento;

    public Alumno() {}

    public Alumno(String id, String nombre, String email, LocalDate fechaNacimiento) {
        this.id = id;
        this.nombre = nombre;
        this.email = email;
        this.fechaNacimiento = fechaNacimiento;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { 
        // * Setter simple. Evita validaciones fuertes aquí para mantener la lógica en controladores.
        this.nombre = nombre; 
    }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public LocalDate getFechaNacimiento() { return fechaNacimiento; }
    public void setFechaNacimiento(LocalDate fechaNacimiento) { this.fechaNacimiento = fechaNacimiento; }

    @Override
    public String toString() {
        return "Alumno{" +
                "id='" + id + '\'' +
                ", nombre='" + nombre + '\'' +
                ", email='" + email + '\'' +
                ", fechaNacimiento=" + fechaNacimiento +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Alumno alumno = (Alumno) o;
        return Objects.equals(id, alumno.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
