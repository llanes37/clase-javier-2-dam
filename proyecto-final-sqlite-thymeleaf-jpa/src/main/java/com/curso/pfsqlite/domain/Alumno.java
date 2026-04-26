package com.curso.pfsqlite.domain;

import jakarta.persistence.*;

import java.time.LocalDate;
import java.util.Objects;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: Alumno  |  CAPA: Domain (Entidad JPA)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: ¿Qué es una entidad JPA?
// ? Una clase anotada con @Entity representa una tabla en la base de datos.
// ? Cada instancia de la clase = una fila de la tabla.
// ? JPA (a través de Hibernate) se encarga de traducir operaciones Java ↔ SQL automáticamente.

// * 🧠 TEORÍA: Principio de responsabilidad única aplicado a la entidad
// ? La entidad SOLO almacena estado (datos de la tabla).
// ? Las validaciones y reglas de negocio (email único, borrado protegido) viven en AlumnoService.

// * 🧠 TEORÍA: Doble barrera para el email único
// ? 1) Service → comprueba existsByEmailIgnoreCase() antes de insertar → mensaje claro al usuario.
// ? 2) UNIQUE constraint en BD (uk_alumnos_email) → protección ante inserciones directas o bugs.

// TODO: añadir campos de auditoría (createdAt, updatedAt) como ejercicio avanzado

@Entity
@Table(name = "alumnos", uniqueConstraints = {
        // * La constraint UNIQUE en BD protege la integridad aunque alguien inserte
        // datos directamente
        @UniqueConstraint(name = "uk_alumnos_email", columnNames = "email")
})
public class Alumno {

    // * 🧠 TEORÍA: @Id + @GeneratedValue
    // ? @Id marca el campo como clave primaria de la tabla.
    // ? GenerationType.IDENTITY delega la generación al AUTOINCREMENT de SQLite.
    // ? Hibernate asigna el valor automáticamente al hacer
    // alumnoRepository.save(alumno).
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    // * nullable=false → genera NOT NULL en el esquema SQL de la tabla
    // * length=120 → VARCHAR(120) en la columna de la BD
    @Column(nullable = false, length = 120)
    private String nombre;

    // ! ⚠️ El email debe ser único: la constraint UNIQUE está en BD Y se comprueba
    // en el service
    @Column(nullable = false, length = 160)
    private String email;

    // * Campo opcional (puede ser null) → útil para calcular edad o segmentar
    // alumnos por edad
    // ? Si el campo es null, JPA lo guarda como NULL en la BD sin error
    @Column(name = "fecha_nacimiento")
    private LocalDate fechaNacimiento;

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GETTERS Y SETTERS
    // ─────────────────────────────────────────────────────────────────────────

    // ? Hibernate necesita getters/setters públicos para leer y escribir los
    // campos.
    // ? El setter de id no existe: el ID lo asigna la BD, nunca el código de
    // negocio.

    public Integer getId() {
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

    public LocalDate getFechaNacimiento() {
        return fechaNacimiento;
    }

    public void setFechaNacimiento(LocalDate fechaNacimiento) {
        this.fechaNacimiento = fechaNacimiento;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 equals(), hashCode() y toString()
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: ¿Por qué sobrescribir equals() en una entidad JPA?
    // ? Hibernate puede crear múltiples instancias Java para la misma fila de BD.
    // ? Comparar solo el ID garantiza que dos instancias de la misma fila sean
    // "iguales".
    // ! ⚠️ Si el ID es null (entidad aún no persistida), dos instancias distintas
    // NUNCA
    // ! serán iguales, que es el comportamiento correcto antes del save().
    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (!(o instanceof Alumno other))
            return false;
        // * Solo son iguales si ambos tienen ID asignado y coincide
        return id != null && id.equals(other.id);
    }

    // * 🧠 TEORÍA: ¿Por qué hashCode() devuelve getClass().hashCode() y no
    // Objects.hashCode(id)?
    // ? Si usáramos el ID como hashCode, una entidad con id=null al insertarse en
    // un HashSet
    // ? cambiaría de "bucket", corrompiendo la colección.
    // ? Devolver siempre el mismo valor por clase es seguro (aunque algo menos
    // eficiente).
    @Override
    public int hashCode() {
        return getClass().hashCode();
    }

    // * 🧠 TEORÍA: toString() es esencial para depuración
    // ? Sin sobrescribir toString(), verías "Alumno@3a5d28" en los logs en lugar de
    // datos reales.
    @Override
    public String toString() {
        return "Alumno{" +
                "id=" + id +
                ", nombre='" + nombre + '\'' +
                ", email='" + email + '\'' +
                ", fechaNacimiento=" + fechaNacimiento +
                '}';
    }
}
