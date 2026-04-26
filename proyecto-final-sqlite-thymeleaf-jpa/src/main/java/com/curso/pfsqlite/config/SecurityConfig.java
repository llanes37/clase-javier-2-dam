package com.curso.pfsqlite.config;

import com.curso.pfsqlite.service.UsuarioService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: SecurityConfig  |  CAPA: Config (Seguridad)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: @EnableWebSecurity activa el sistema completo de Spring Security.
// ? Sin esta anotación, la configuración personalizada no se aplicaría.

// * 🧠 TEORÍA: En Spring Boot 3.x ya no se usa WebSecurityConfigurerAdapter.
// ? Ahora se definen beans: SecurityFilterChain (reglas HTTP) + PasswordEncoder (hash).
// ? Este estilo funcional es más flexible y fácil de testear.

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    // * PasswordEncoder como bean para poder inyectarlo en UsuarioService y DataInitializer
    // ! ⚠️ BCrypt es el algoritmo recomendado: lento por diseño, resistente a fuerza bruta
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    // * DaoAuthenticationProvider conecta Spring Security con nuestra BD a través de UsuarioService
    // ? Spring Security llama a loadUserByUsername() → compara el hash BCrypt → decide si autentica
    @Bean
    public DaoAuthenticationProvider authProvider(UsuarioService usuarioService, PasswordEncoder encoder) {
        DaoAuthenticationProvider provider = new DaoAuthenticationProvider();
        provider.setUserDetailsService(usuarioService);
        provider.setPasswordEncoder(encoder);
        return provider;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 SecurityFilterChain → define qué rutas necesitan qué rol
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: Las reglas se evalúan EN ORDEN, la primera que coincide gana.
    // ? Por eso las rutas más específicas van antes que las generales.

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http,
                                           DaoAuthenticationProvider authProvider) throws Exception {
        http
            .authenticationProvider(authProvider)
            .authorizeHttpRequests(auth -> auth

                // * Recursos públicos: CSS, páginas de login/registro, gestión de errores
                .requestMatchers("/login", "/register", "/css/**", "/error").permitAll()

                // * Página principal y listados: accesibles para cualquier usuario autenticado
                .requestMatchers(HttpMethod.GET, "/").hasAnyRole("USER", "ADMIN")
                .requestMatchers(HttpMethod.GET, "/alumnos", "/cursos", "/matriculas").hasAnyRole("USER", "ADMIN")

                // * Formularios de alta (GET) y todas las acciones de escritura (POST) → solo ADMIN
                // ? hasRole("ADMIN") comprueba la autoridad "ROLE_ADMIN" automáticamente
                .requestMatchers("/alumnos/**", "/cursos/**", "/matriculas/**").hasRole("ADMIN")

                // * Cualquier ruta no contemplada requiere estar autenticado
                .anyRequest().authenticated()
            )

            // * Configuración del formulario de login propio (sustituye el de Spring por defecto)
            .formLogin(form -> form
                .loginPage("/login")                     // GET /login → nuestro login.html
                .loginProcessingUrl("/login")            // POST /login → procesado por Spring Security
                .defaultSuccessUrl("/", true)            // tras login OK → redirige a /
                .failureUrl("/login?error")              // tras login KO → muestra mensaje
                .permitAll()
            )

            // * Configuración del logout
            .logout(logout -> logout
                .logoutUrl("/logout")                    // POST /logout → cierra sesión
                .logoutSuccessUrl("/login?logout")       // después de logout → redirige a login
                .permitAll()
            );

        return http.build();
    }
}
