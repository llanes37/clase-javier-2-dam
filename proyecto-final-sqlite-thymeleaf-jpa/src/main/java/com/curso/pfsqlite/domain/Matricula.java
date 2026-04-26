package com.curso.pfsqlite.domain;

import jakarta.persistence.*;

import java.time.LocalDate;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: Matricula  |  CAPA: Domain (Entidad JPA)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: ¿Qué relación modela esta entidad?
// ? Matricula actúa como tabla de unión (many-to-many con atributos propios)
// ? entre Alumno y Curso. Tiene su propio ciclo de vida: ACTIVA → ANULADA / FINALIZADA.

// * 🧠 TEORÍA: FetchType.LAZY vs FetchType.EAGER
// ? LAZY  → Hibernate NO carga alumno/curso hasta que se accede al campo.
// ?          Evita consultas innecesarias cuando solo necesitamos el ID de la matrícula.
// ? EAGER → Hibernate carga siempre alumno y curso en el mismo SELECT, aunque no los necesitemos.
// ! ⚠️ Si accedes a alumno.getNombre() fuera de una transacción activa con LAZY, obtienes
// ! LazyInitializationException. La solución es usar @EntityGraph en el repositorio.

// * 🧠 TEORÍA: Unicidad de matrícula ACTIVA
// ? Un alumno NO puede tener dos matrículas ACTIVAS en el mismo curso.
// ? Reforzado en BD con índice parcial (uk_matricula_activa) Y en MatriculaService.
// ? Una matrícula ANULADA no bloquea: se puede volver a matricular (decisión de negocio).

@Entity
@Table(name = "matriculas")
public class Matricula {

    // * Clave primaria generada automáticamente por SQLite
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    // * 🧠 TEORÍA: @ManyToOne → muchas matrículas pertenecen a UN alumno
    // ? optional=false le indica a Hibernate que NUNCA será null.
    // ? Hibernate puede optimizar el JOIN: usa INNER JOIN en vez de LEFT OUTER
    // JOIN.
    // ? @JoinColumn(name="alumno_id") → nombre de la columna de clave foránea en la
    // tabla matriculas
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "alumno_id", nullable = false)
    private Alumno alumno;

    // * @ManyToOne → muchas matrículas pertenecen a UN curso (mismo patrón que
    // alumno)
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "curso_id", nullable = false)
    private Curso curso;

    // * Fecha en que se realiza la matriculación → debe estar dentro del rango del
    // curso
    @Column(name = "fecha_matricula", nullable = false)
    private LocalDate fechaMatricula;

    // * 🧠 TEORÍA: @Enumerated(EnumType.STRING) → guarda "ACTIVA", "ANULADA" o
    // "FINALIZADA"
    // ? Más legible que ORDINAL (0, 1, 2) y no se rompe si se reordena el enum
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private EstadoMatricula estado;

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GETTERS Y SETTERS
    // ─────────────────────────────────────────────────────────────────────────

    public Integer getId() {
        return id;
    }

    public Alumno getAlumno() {
        return alumno;
    }

    public void setAlumno(Alumno alumno) {
        this.alumno = alumno;
    }

    public Curso getCurso() {
        return curso;
    }

    public void setCurso(Curso curso) {
        this.curso = curso;
    }

    public LocalDate getFechaMatricula() {
        return fechaMatricula;
    }

    public void setFechaMatricula(LocalDate fechaMatricula) {
        this.fechaMatricula = fechaMatricula;
    }

    public EstadoMatricula getEstado() {
        return estado;
    }

    public void setEstado(EstadoMatricula estado) {
        this.estado = estado;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 equals(), hashCode() y toString()
    // ─────────────────────────────────────────────────────────────────────────

    // * Igualdad por ID → ver justificación detallada en Alumno.java
    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (!(o instanceof Matricula other))
            return false;
        return id != null && id.equals(other.id);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }

    // ! ⚠️ No incluimos alumno.toString() ni curso.toString() aquí para evitar
    // ! LazyInitializationException si toString() se llama fuera de contexto
    // transaccional.
    // * Mostramos solo los IDs de las relaciones, que siempre están disponibles
    @Override
    public String toString() {
        return "Matricula{" +
                "id=" + id +
                ", alumnoId=" + (alumno != null ? alumno.getId() : null) +
                ", cursoId=" + (curso != null ? curso.getId() : null) +
                ", fechaMatricula=" + fechaMatricula +
                ", estado=" + estado +
                '}';
    }
}
