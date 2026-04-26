package com.curso.pfsqlite.web.form;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: RegisterForm  |  CAPA: Web (DTO de formulario)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: DTO (Data Transfer Object) de registro.
// ? Desacopla el formulario HTML de la entidad JPA Usuario.
// ? Las anotaciones Bean Validation actúan en el controlador antes de llegar al service.
public class RegisterForm {

    @NotBlank(message = "El nombre de usuario es obligatorio")
    @Size(min = 3, max = 40, message = "El usuario debe tener entre 3 y 40 caracteres")
    @Pattern(regexp = "^[a-zA-Z0-9_.-]+$", message = "Solo letras, números, guiones y puntos")
    private String username;

    @NotBlank(message = "La contraseña es obligatoria")
    @Size(min = 6, message = "La contraseña debe tener al menos 6 caracteres")
    private String password;

    // * Solo se permiten los dos roles válidos del sistema
    @NotBlank(message = "Debes seleccionar un rol")
    @Pattern(regexp = "ROLE_USER|ROLE_ADMIN", message = "Rol no válido")
    private String rol;

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }

    public String getRol() { return rol; }
    public void setRol(String rol) { this.rol = rol; }
}
