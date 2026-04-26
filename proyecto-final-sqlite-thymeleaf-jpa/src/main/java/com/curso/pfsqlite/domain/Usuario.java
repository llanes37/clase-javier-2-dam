package com.curso.pfsqlite.domain;

import jakarta.persistence.*;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: Usuario  |  CAPA: Domain (Entidad JPA)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: Esta entidad representa la tabla `usuarios` gestionada por Spring Security.
// ? Spring Security necesita un mecanismo para cargar usuarios desde la BD.
// ? UsuarioService implementará UserDetailsService y usará esta entidad.

// ! ⚠️ La contraseña NUNCA se almacena en texto plano.
// ! BCryptPasswordEncoder genera un hash seguro que Spring Security compara en login.

@Entity
@Table(name = "usuarios")
public class Usuario {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    // * username único (constraint en BD + comprobación en service antes de guardar)
    @Column(nullable = false, unique = true, length = 80)
    private String username;

    // ! ⚠️ Este campo almacena el HASH BCrypt, nunca la contraseña en claro
    @Column(nullable = false, length = 255)
    private String password;

    // * Valores válidos: "ROLE_USER" (solo lectura) o "ROLE_ADMIN" (lectura + escritura)
    // ? Spring Security espera que los roles tengan el prefijo "ROLE_" por convenio.
    @Column(nullable = false, length = 20)
    private String rol;

    // * Constructor vacío requerido por JPA/Hibernate
    public Usuario() {}

    public Integer getId() { return id; }

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }

    public String getRol() { return rol; }
    public void setRol(String rol) { this.rol = rol; }
}
