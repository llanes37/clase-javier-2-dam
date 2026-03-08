package com.curso.pfsqlite.web.form;

import com.curso.pfsqlite.domain.CursoTipo;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.springframework.format.annotation.DateTimeFormat;

import java.math.BigDecimal;
import java.time.LocalDate;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: CursoForm  |  CAPA: Web (DTO de Formulario)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: DTO de formulario para alta de cursos con validaciones declarativas
// ? Estas anotaciones cubren FORMATO de los campos (no vacío, tipo correcto, etc.).
// ! ⚠️ Las reglas de NEGOCIO (fechas coherentes) se validan en CursoService, no aquí.
// ? Separar formato vs negocio permite mostrar errores de campo individuales en Thymeleaf
// ? sin código extra, y mantener la lógica de negocio en una única capa.

public class CursoForm {

    // * @NotBlank → obligatorio, no vacío ni solo espacios
    @NotBlank(message = "El nombre es obligatorio")
    private String nombre;

    // * @NotNull → para enums se usa @NotNull (no @NotBlank, que es solo para
    // Strings)
    // ? El <select> en HTML enviará "ONLINE" o "PRESENCIAL", Spring lo convierte al
    // enum
    @NotNull(message = "El tipo es obligatorio")
    private CursoTipo tipo;

    // * @NotNull + @DateTimeFormat → fecha obligatoria en formato ISO (yyyy-MM-dd)
    @NotNull(message = "La fecha de inicio es obligatoria")
    @DateTimeFormat(iso = DateTimeFormat.ISO.DATE)
    private LocalDate fechaInicio;

    @NotNull(message = "La fecha de fin es obligatoria")
    @DateTimeFormat(iso = DateTimeFormat.ISO.DATE)
    private LocalDate fechaFin;

    // * @DecimalMin → el precio debe ser >= 0.0 (no se permiten precios negativos)
    // ? inclusive=true → 0.0 es un valor válido (un curso gratuito es posible)
    @NotNull(message = "El precio es obligatorio")
    @DecimalMin(value = "0.0", inclusive = true, message = "El precio debe ser mayor o igual a 0")
    private BigDecimal precio;

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GETTERS Y SETTERS
    // ─────────────────────────────────────────────────────────────────────────

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
}
