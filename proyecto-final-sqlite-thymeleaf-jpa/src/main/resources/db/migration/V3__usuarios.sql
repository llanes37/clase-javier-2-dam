-- * Tabla de usuarios para autenticación con Spring Security.
-- ? Cada usuario tiene un rol: ROLE_USER (solo lectura) o ROLE_ADMIN (lectura + escritura).
-- ! La contraseña se almacena SIEMPRE como hash BCrypt, nunca en texto plano.
CREATE TABLE IF NOT EXISTS usuarios (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80)  NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol      VARCHAR(20)  NOT NULL,
    CONSTRAINT uk_usuarios_username UNIQUE (username),
    CONSTRAINT ck_usuarios_rol CHECK (rol IN ('ROLE_USER', 'ROLE_ADMIN'))
);

-- * Los usuarios por defecto (admin/admin123 y user/user123) los inserta
-- * DataInitializer.java al arrancar, usando BCryptPasswordEncoder para el hash.
-- ? Así evitamos tener hashes BCrypt hardcodeados en SQL y la lógica queda en Java.
