package com.curso.pfsqlite.repository;

import com.curso.pfsqlite.domain.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 INTERFAZ: UsuarioRepository  |  CAPA: Repository (Acceso a Datos)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: Spring Data JPA genera la implementación SQL automáticamente.
// ? findByUsernameIgnoreCase → SELECT * FROM usuarios WHERE LOWER(username) = LOWER(?)
// ? existsByUsernameIgnoreCase → SELECT COUNT(*) > 0 (más eficiente que cargar la entidad)
public interface UsuarioRepository extends JpaRepository<Usuario, Integer> {

    // * Usado por UserDetailsService para cargar el usuario en el login
    Optional<Usuario> findByUsernameIgnoreCase(String username);

    // * Usado en el registro para evitar duplicados de username
    boolean existsByUsernameIgnoreCase(String username);
}
