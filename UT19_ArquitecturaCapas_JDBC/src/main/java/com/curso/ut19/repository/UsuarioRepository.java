package com.curso.ut19.repository;

import com.curso.ut19.model.Usuario;
import java.util.List;
import java.util.Optional;

/**
 * //! REPOSITORY PATTERN - INTERFAZ DE REPOSITORIO DE USUARIO
 * ? Define el contrato para el acceso a datos de Usuario (abstracción de persistencia)
 *
 * * PATRÓN REPOSITORY:
 *   - Abstrae la capa de persistencia del resto de la aplicación
 *   - Permite cambiar la implementación sin modificar el servicio
 *   - Facilita el testing con implementaciones mock
 *   - Centraliza las consultas a la base de datos
 *
 * ! IMPLEMENTACIONES POSIBLES:
 *   ✓ UsuarioRepositoryJdbc    - Implementación con JDBC manual
 *   ✓ UsuarioRepositoryJpa     - Implementación con JPA/Hibernate
 *   ✓ UsuarioRepositoryMock    - Implementación en memoria para tests
 *   ✓ UsuarioRepositoryFile    - Implementación con archivos
 *
 * ? VENTAJAS:
 *   - Inversión de dependencias (el servicio depende de la interfaz, no de la implementación)
 *   - Código más testeable y mantenible
 *   - Facilita la migración de tecnologías (de JDBC a JPA, por ejemplo)
 *
 * TODO (Alumno):
 *   - Añade métodos de consulta personalizados (findByNombre, findByEdadMayorQue)
 *   - Implementa paginación (findAll con Pageable)
 *   - Añade métodos de búsqueda con criterios (findByExample)
 */
public interface UsuarioRepository {

    /**
     * ! CREAR/GUARDAR USUARIO
     * ? Inserta un nuevo usuario en la base de datos
     *
     * * Comportamiento:
     * - Recibe un Usuario sin ID (o con ID null)
     * - Inserta el usuario en la base de datos
     * - Asigna el ID generado automáticamente (AUTOINCREMENT)
     * - Retorna el mismo objeto con el ID asignado
     *
     * @param u Usuario a guardar (sin ID o con ID null)
     * @return Usuario guardado con ID asignado por la base de datos
     *
     * @throws RuntimeException si falla la inserción en la base de datos
     */
    Usuario save(Usuario u);

    /**
     * ! BUSCAR USUARIO POR ID
     * ? Busca un usuario en la base de datos por su identificador único
     *
     * * Uso de Optional:
     * - Optional<Usuario> evita retornar null
     * - Obliga al código cliente a manejar explícitamente la ausencia de datos
     * - Métodos útiles: isPresent(), ifPresent(), orElse(), orElseThrow()
     *
     * * Ejemplo de uso:
     * <pre>
     * Optional<Usuario> opt = repository.findById(5);
     * if (opt.isPresent()) {
     *     Usuario u = opt.get();
     *     System.out.println(u.getNombre());
     * } else {
     *     System.out.println("Usuario no encontrado");
     * }
     * </pre>
     *
     * @param id Identificador del usuario a buscar
     * @return Optional con el usuario si existe, Optional.empty() si no existe
     *
     * @throws RuntimeException si falla la consulta a la base de datos
     */
    Optional<Usuario> findById(int id);

    /**
     * ! LISTAR TODOS LOS USUARIOS
     * ? Recupera todos los usuarios almacenados en la base de datos
     *
     * * Comportamiento:
     * - Ejecuta SELECT * FROM usuarios ORDER BY id
     * - Mapea cada fila del ResultSet a un objeto Usuario
     * - Retorna lista vacía si no hay usuarios (nunca retorna null)
     *
     * ! ADVERTENCIA:
     * - Sin paginación, puede retornar miles de registros
     * - En producción, considera implementar findAll(Pageable)
     * - Para tablas grandes, usa consultas con LIMIT/OFFSET
     *
     * @return Lista con todos los usuarios (lista vacía si no hay datos)
     *
     * @throws RuntimeException si falla la consulta a la base de datos
     */
    List<Usuario> findAll();

    /**
     * ! ACTUALIZAR USUARIO
     * ? Actualiza los datos de un usuario existente en la base de datos
     *
     * * Comportamiento:
     * - Requiere un Usuario con ID válido
     * - Ejecuta UPDATE usuarios SET nombre=?, edad=? WHERE id=?
     * - Retorna true si se actualizó al menos 1 fila (ID existe)
     * - Retorna false si no se actualizó ninguna fila (ID no existe)
     *
     * * Ejemplo de uso:
     * <pre>
     * Usuario u = new Usuario(5, "Juan Pérez", 30);
     * boolean actualizado = repository.update(u);
     * if (actualizado) {
     *     System.out.println("Usuario actualizado");
     * } else {
     *     System.out.println("ID no encontrado");
     * }
     * </pre>
     *
     * @param u Usuario con ID y datos a actualizar
     * @return true si se actualizó el usuario, false si el ID no existe
     *
     * @throws RuntimeException si falla la actualización en la base de datos
     */
    boolean update(Usuario u);

    /**
     * ! ELIMINAR USUARIO POR ID
     * ? Elimina un usuario de la base de datos por su identificador
     *
     * * Comportamiento:
     * - Ejecuta DELETE FROM usuarios WHERE id=?
     * - Retorna true si se eliminó al menos 1 fila (ID existe)
     * - Retorna false si no se eliminó ninguna fila (ID no existe)
     *
     * ! IMPORTANTE:
     * - La eliminación es permanente (no hay papelera de reciclaje)
     * - Si hay claves foráneas, podría fallar (integridad referencial)
     * - Considera implementar "soft delete" (borrado lógico con flag)
     *
     * @param id Identificador del usuario a eliminar
     * @return true si se eliminó el usuario, false si el ID no existe
     *
     * @throws RuntimeException si falla la eliminación (ej: violación de FK)
     */
    boolean delete(int id);
}
