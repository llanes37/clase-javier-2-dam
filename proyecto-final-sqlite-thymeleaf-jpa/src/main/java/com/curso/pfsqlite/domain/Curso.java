package com.curso.pfsqlite.domain;

import jakarta.persistence.*;

import java.math.BigDecimal;
import java.time.LocalDate;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: Curso  |  CAPA: Domain (Entidad JPA)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: Entidad JPA → cada instancia = una fila en la tabla `cursos` de la BD
// ? Contiene los datos esenciales del curso: nombre, tipo (ONLINE/PRESENCIAL), fechas y precio.

// * 🧠 TEORÍA: Reglas de negocio que aplican a esta entidad (validadas en CursoService)
// ? 1) fechaFin >= fechaInicio     → validada en service Y con CHECK en BD.
// ? 2) precio >= 0                 → validada con CHECK en BD (ck_cursos_precio).
// ? 3) No se puede borrar con matrículas ACTIVAS → validada en CursoService.

// * 🧠 TEORÍA: Doble barrera para la regla de fechas
// ? Service → lanza BusinessException con mensaje claro ("La fecha de fin no puede ser anterior...").
// ? CHECK en BD → barrera de seguridad ante inserciones directas o scripts de migración.

@Entity
@Table(name = "cursos")
public class Curso {

    // * @Id + @GeneratedValue → clave primaria generada automáticamente por SQLite
    // (AUTOINCREMENT)
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // * nullable=false → NOT NULL en BD | length=150 → VARCHAR(150)
    @Column(nullable = false, length = 150)
    private String nombre;

    // * 🧠 TEORÍA: @Enumerated(EnumType.STRING) vs EnumType.ORDINAL
    // ? EnumType.STRING → guarda "ONLINE" o "PRESENCIAL" como texto → legible en
    // BD.
    // ? EnumType.ORDINAL → guarda 0 o 1 como número → si el orden del enum cambia,
    // los datos se corrompen.
    // ! ⚠️ Usar SIEMPRE EnumType.STRING para evitar corrupción de datos al
    // refactorizar el enum.
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private CursoTipo tipo;

    // * fechaInicio y fechaFin forman la ventana temporal del curso
    // ? La fecha de matrícula de un alumno DEBE estar dentro de este rango
    // (validado en MatriculaService)
    @Column(name = "fecha_inicio", nullable = false)
    private LocalDate fechaInicio;

    @Column(name = "fecha_fin", nullable = false)
    private LocalDate fechaFin;

    // * 🧠 TEORÍA: ¿Por qué BigDecimal para precio y NO double o float?
    // ? double tiene errores de precisión en coma flotante: 0.1 + 0.2 =
    // 0.30000000000000004 (incorrecto).
    // ? BigDecimal es exacto: 0.1 + 0.2 = 0.3 (correcto). Esencial para datos
    // financieros.
    // ? En BD: DECIMAL(10,2) → máximo 10 dígitos con 2 decimales (ej: 9999999.99)
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal precio;

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GETTERS Y SETTERS
    // ─────────────────────────────────────────────────────────────────────────

    public Long getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public CursoTipo getTipo() {
        return tipo;
    }

    public void setTipo(CursoTipo tipo) {
        this.tipo = tipo;
    }

    public LocalDate getFechaInicio() {
        return fechaInicio;
    }

    public void setFechaInicio(LocalDate fechaInicio) {
        this.fechaInicio = fechaInicio;
    }

    public LocalDate getFechaFin() {
        return fechaFin;
    }

    public void setFechaFin(LocalDate fechaFin) {
        this.fechaFin = fechaFin;
    }

    public BigDecimal getPrecio() {
        return precio;
    }

    public void setPrecio(BigDecimal precio) {
        this.precio = precio;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 equals(), hashCode() y toString()
    // ─────────────────────────────────────────────────────────────────────────

    // * Igualdad por ID de base de datos → ver justificación detallada en
    // Alumno.java
    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (!(o instanceof Curso other))
            return false;
        return id != null && id.equals(other.id);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }

    // * toString() → permite ver "Curso{id=3, nombre='Java', tipo=ONLINE}" en los
    // logs
    // ? Sin sobrescribir toString(), verías "Curso@1f2b3c" (inútil para depurar)
    @Override
    public String toString() {
        return "Curso{" +
                "id=" + id +
                ", nombre='" + nombre + '\'' +
                ", tipo=" + tipo +
                ", fechaInicio=" + fechaInicio +
                ", fechaFin=" + fechaFin +
                ", precio=" + precio +
                '}';
    }
}
