package com.curso.proyectobasico.model;

import java.util.Objects;

/*
 * Cliente de la agenda: nombre, email y telefono basicos.
 * Mantener esta clase sin dependencias de consola ni de CSV (solo dominio).
 */
public class Cliente {
    private final String id;
    private String nombre;
    private String email;
    private String telefono;

    public Cliente(String id, String nombre, String email, String telefono) {
        this.id = id;
        this.nombre = nombre;
        this.email = email;
        this.telefono = telefono;
    }

    public String getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getTelefono() {
        return telefono;
    }

    public void setTelefono(String telefono) {
        this.telefono = telefono;
    }

    @Override
    public String toString() {
        return "Cliente{id='" + id + '\'' +
                ", nombre='" + nombre + '\'' +
                (email == null || email.isBlank() ? "" : ", email='" + email + '\'') +
                (telefono == null || telefono.isBlank() ? "" : ", telefono='" + telefono + '\'') +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Cliente cliente = (Cliente) o;
        return Objects.equals(id, cliente.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}

