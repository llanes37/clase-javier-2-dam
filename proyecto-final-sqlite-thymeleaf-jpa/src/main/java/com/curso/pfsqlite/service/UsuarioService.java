package com.curso.pfsqlite.service;

import com.curso.pfsqlite.domain.Usuario;
import com.curso.pfsqlite.repository.UsuarioRepository;
import com.curso.pfsqlite.web.form.RegisterForm;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: UsuarioService  |  CAPA: Service (Seguridad + Negocio)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: UserDetailsService es la interfaz que Spring Security llama en cada login.
// ? Spring Security invoca loadUserByUsername(username) automáticamente al procesar
// ? el formulario de login. Nosotros solo tenemos que devolver un UserDetails con
// ? el hash de contraseña y los roles; Spring Security hace la comparación BCrypt.

// ! ⚠️ REGLA DE SEGURIDAD: nunca lanzar mensajes distintos para "usuario no existe"
// ! vs "contraseña incorrecta". Ambos casos deben dar el mismo error genérico al usuario
// ! para evitar que un atacante descubra qué usernames están registrados.

@Service
public class UsuarioService implements UserDetailsService {

    private static final Logger log = LoggerFactory.getLogger(UsuarioService.class);

    private final UsuarioRepository usuarioRepository;
    private final PasswordEncoder passwordEncoder;

    public UsuarioService(UsuarioRepository usuarioRepository, PasswordEncoder passwordEncoder) {
        this.usuarioRepository = usuarioRepository;
        this.passwordEncoder = passwordEncoder;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 loadUserByUsername() → llamado automáticamente por Spring Security en login
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: UserDetails es la representación interna de Spring Security.
    // ? Contiene: username, password (hash), y lista de GrantedAuthority (roles).
    // ? Spring Security comparará el hash almacenado con la contraseña introducida.
    @Override
    @Transactional(readOnly = true)
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        Usuario usuario = usuarioRepository.findByUsernameIgnoreCase(username)
                .orElseThrow(() -> {
                    // ! Mensaje genérico intencionado: no revelamos si el usuario existe o no
                    log.warn("Intento de login con username no registrado: {}", username);
                    return new UsernameNotFoundException("Credenciales incorrectas");
                });

        log.debug("Usuario cargado para login: {} con rol: {}", usuario.getUsername(), usuario.getRol());

        // * SimpleGrantedAuthority envuelve el string del rol (ej: "ROLE_ADMIN")
        return new User(
                usuario.getUsername(),
                usuario.getPassword(),
                List.of(new SimpleGrantedAuthority(usuario.getRol()))
        );
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 registrar() → crea un nuevo usuario con contraseña encriptada
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: passwordEncoder.encode() genera un hash BCrypt único para cada llamada.
    // ? BCrypt incluye un "salt" aleatorio en el hash → dos llamadas con la misma
    // ? contraseña producen hashes distintos, lo que protege contra ataques de tabla arcoíris.
    @Transactional
    public void registrar(RegisterForm form) {
        if (usuarioRepository.existsByUsernameIgnoreCase(form.getUsername())) {
            throw new BusinessException("Ya existe un usuario con ese nombre de usuario");
        }

        Usuario nuevo = new Usuario();
        nuevo.setUsername(form.getUsername().trim().toLowerCase());
        // ! ⚠️ encode() → hash BCrypt, nunca texto plano
        nuevo.setPassword(passwordEncoder.encode(form.getPassword()));
        nuevo.setRol(form.getRol());

        usuarioRepository.save(nuevo);
        log.info("Nuevo usuario registrado: {} con rol: {}", nuevo.getUsername(), nuevo.getRol());
    }
}
