package com.curso.ut20.repository;

import com.curso.ut20.model.Producto;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * //! REPOSITORIO JPA - PRODUCTO
 * ? Interfaz de acceso a datos para la entidad Producto
 *
 * * Spring Data JPA genera automáticamente la implementación de esta interfaz en tiempo de ejecución
 * * No es necesario escribir código SQL ni implementar métodos CRUD
 *
 * ! MÉTODOS HEREDADOS DE JpaRepository (los más importantes):
 *
 * ? Búsqueda:
 *   - findAll() → List<Producto> - Obtiene todos los productos
 *   - findById(Long id) → Optional<Producto> - Busca por ID
 *   - findAllById(Iterable<Long> ids) → List<Producto> - Busca múltiples IDs
 *
 * ? Inserción/Actualización:
 *   - save(Producto p) → Producto - Guarda o actualiza (si tiene ID)
 *   - saveAll(Iterable<Producto> ps) → List<Producto> - Guarda múltiples
 *
 * ? Eliminación:
 *   - deleteById(Long id) - Elimina por ID
 *   - delete(Producto p) - Elimina la entidad
 *   - deleteAll() - Elimina todos los registros
 *
 * ? Utilidades:
 *   - existsById(Long id) → boolean - Verifica si existe
 *   - count() → long - Cuenta total de registros
 *
 * * CONSULTAS PERSONALIZADAS:
 * TODO: Puedes añadir consultas personalizadas siguiendo la convención de nombres:
 *   - List<Producto> findByNombre(String nombre);
 *   - List<Producto> findByPrecioLessThan(double precio);
 *   - List<Producto> findByNombreContaining(String keyword);
 *   - @Query("SELECT p FROM Producto p WHERE p.precio > :precio")
 *     List<Producto> buscarCaros(@Param("precio") double precio);
 *
 * @see org.springframework.data.jpa.repository.JpaRepository
 */
public interface ProductoRepository extends JpaRepository<Producto, Long> {
    // * No es necesario definir métodos aquí
    // * Spring Data JPA genera automáticamente toda la implementación CRUD
    // * La magia sucede en tiempo de ejecución mediante proxies dinámicos

    // TODO: Añade métodos de consulta personalizados si los necesitas
    // Ejemplos:
    // List<Producto> findByNombre(String nombre);
    // List<Producto> findByPrecioBetween(double min, double max);
}
