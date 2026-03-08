package com.curso.pfsqlite.web.form;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import org.springframework.format.annotation.DateTimeFormat;

import java.time.LocalDate;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: AlumnoForm  |  CAPA: Web (DTO de Formulario)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: ¿Qué es un DTO (Data Transfer Object)?
// ? Es una clase que transporta datos entre la vista (formulario HTML) y el controlador.
// ? Separa los datos del formulario de la entidad JPA para no acoplar
// ? detalles de persistencia (@Entity, @Id, @Column) con la capa web.

// * 🧠 TEORÍA: Bean Validation (anotaciones @NotBlank, @Email, etc.)
// ? Cuando el controlador recibe el formulario con @Valid, Spring activa automáticamente
// ? la validación de estas anotaciones ANTES de ejecutar el método del controller.
// ? Si alguna falla, BindingResult contiene los errores y Thymeleaf los muestra en la vista.

// TODO: incluir validación de longitud mínima de nombre (@Size(min=2)) como ejercicio básico

public class AlumnoForm {

    // * @NotBlank → no puede ser null, ni vacío, ni solo espacios en blanco
    @NotBlank(message = "El nombre es obligatorio")
    private String nombre;

    // * @NotBlank + @Email → campo obligatorio con formato de email válido
    // ? @Email comprueba el formato básico (que contenga @ y dominio)
    // ? El service hace una validación más estricta con regex
    @NotBlank(message = "El email es obligatorio")
    @Email(message = "El email no es válido")
    private String email;

    // * Campo opcional → puede ser null (no tiene @NotNull)
    // ? @DateTimeFormat indica a Spring cómo parsear la fecha del input HTML
    // (formato ISO: yyyy-MM-dd)
    @DateTimeFormat(iso = DateTimeFormat.ISO.DATE)
    private LocalDate fechaNacimiento;

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GETTERS Y SETTERS (necesarios para que Spring y Thymeleaf lean/escriban
    // los campos)
    // ─────────────────────────────────────────────────────────────────────────

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
}
