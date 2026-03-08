package com.curso.ut20.repository;

import com.curso.ut20.model.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * //! REPOSITORIO JPA - USUARIO
 * ? Interfaz de acceso a datos para la entidad Usuario
 *
 * * Spring Data JPA genera automáticamente la implementación de esta interfaz en tiempo de ejecución
 * * No es necesario escribir código SQL ni implementar métodos CRUD
 *
 * ! MÉTODOS HEREDADOS DE JpaRepository (los más importantes):
 *
 * ? Búsqueda:
 *   - findAll() → List<Usuario> - Obtiene todos los usuarios
 *   - findById(Long id) → Optional<Usuario> - Busca por ID
 *   - findAllById(Iterable<Long> ids) → List<Usuario> - Busca múltiples IDs
 *
 * ? Inserción/Actualización:
 *   - save(Usuario u) → Usuario - Guarda o actualiza (si tiene ID)
 *   - saveAll(Iterable<Usuario> us) → List<Usuario> - Guarda múltiples
 *
 * ? Eliminación:
 *   - deleteById(Long id) - Elimina por ID
 *   - delete(Usuario u) - Elimina la entidad
 *   - deleteAll() - Elimina todos los registros
 *
 * ? Utilidades:
 *   - existsById(Long id) → boolean - Verifica si existe
 *   - count() → long - Cuenta total de registros
 *
 * * CONSULTAS PERSONALIZADAS:
 * TODO: Puedes añadir consultas personalizadas siguiendo la convención de nombres:
 *   - List<Usuario> findByNombre(String nombre);
 *   - List<Usuario> findByEdadGreaterThan(int edad);
 *   - List<Usuario> findByNombreContaining(String keyword);
 *   - @Query("SELECT u FROM Usuario u WHERE u.edad BETWEEN :min AND :max")
 *     List<Usuario> buscarPorRangoEdad(@Param("min") int min, @Param("max") int max);
 *
 * @see org.springframework.data.jpa.repository.JpaRepository
 */
public interface UsuarioRepository extends JpaRepository<Usuario, Long> {
    // * No es necesario definir métodos aquí
    // * Spring Data JPA genera automáticamente toda la implementación CRUD
    // * La magia sucede en tiempo de ejecución mediante proxies dinámicos

    // TODO: Añade métodos de consulta personalizados si los necesitas
    // Ejemplos:
    // List<Usuario> findByNombre(String nombre);
    // List<Usuario> findByEdadBetween(int min, int max);
}
