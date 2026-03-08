package com.curso.proyectobasico.model;

import java.time.LocalDate;
import java.util.Objects;

/*
 * Cita asociada a un cliente. Mantiene solo datos de dominio basicos.
 */
public class Cita {
    private final String id;
    private final String clienteId;
    private LocalDate fecha;
    private EstadoCita estado;
    private String descripcion;

    public Cita(String id, String clienteId, LocalDate fecha, EstadoCita estado, String descripcion) {
        this.id = id;
        this.clienteId = clienteId;
        this.fecha = fecha;
        this.estado = estado;
        this.descripcion = descripcion;
    }

    public String getId() {
        return id;
    }

    public String getClienteId() {
        return clienteId;
    }

    public LocalDate getFecha() {
        return fecha;
    }

    public void setFecha(LocalDate fecha) {
        this.fecha = fecha;
    }

    public EstadoCita getEstado() {
        return estado;
    }

    public void setEstado(EstadoCita estado) {
        this.estado = estado;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    @Override
    public String toString() {
        return "Cita{id='" + id + '\'' +
                ", clienteId='" + clienteId + '\'' +
                ", fecha=" + fecha +
                ", estado=" + estado +
                (descripcion == null || descripcion.isBlank() ? "" : ", descripcion='" + descripcion + '\'') +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Cita cita = (Cita) o;
        return Objects.equals(id, cita.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}

