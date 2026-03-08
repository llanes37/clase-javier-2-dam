package com.curso.ut19.repository.jdbc;

import com.curso.ut19.model.Usuario;
import com.curso.ut19.persistence.Db;
import com.curso.ut19.repository.UsuarioRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * //! IMPLEMENTACIÓN JDBC DEL REPOSITORIO DE USUARIO
 * ? Implementa UsuarioRepository usando JDBC y SQL nativo
 *
 * * RESPONSABILIDADES:
 *   ✓ Traducir operaciones Java a consultas SQL
 *   ✓ Mapear ResultSet (filas de BD) a objetos Usuario
 *   ✓ Gestionar PreparedStatements y recursos JDBC
 *   ✓ Manejar excepciones SQLException
 *   ✓ Logging de operaciones y errores
 *
 * ! CARACTERÍSTICAS DE ESTA IMPLEMENTACIÓN:
 *   - Usa PreparedStatement para prevenir SQL Injection
 *   - Try-with-resources para cerrar recursos automáticamente
 *   - Mapeo manual de ResultSet a Usuario (método map)
 *   - Logging con SLF4J para trazabilidad
 *   - Obtención de claves generadas (RETURN_GENERATED_KEYS)
 *
 * ? COMPARACIÓN CON JPA:
 *   | Aspecto           | JDBC Manual           | JPA/Hibernate       |
 *   |-------------------|-----------------------|---------------------|
 *   | SQL               | Escrito a mano        | Generado automático |
 *   | Mapeo             | Manual (map method)   | Automático (@Entity)|
 *   | Boilerplate       | Alto                  | Mínimo              |
 *   | Control           | Total                 | Limitado            |
 *   | Curva aprendizaje | Media                 | Alta                |
 *
 * TODO (Mejoras):
 *   - Implementar transacciones (commit/rollback)
 *   - Añadir métodos de búsqueda personalizados (findByNombre)
 *   - Separar SQL a archivos .sql externos
 *   - Implementar paginación con LIMIT/OFFSET
 *   - Añadir manejo de errores más específico
 */
public class UsuarioRepositoryJdbc implements UsuarioRepository {

    // ========================================
    // LOGGING
    // ========================================

    /**
     * * Logger de SLF4J para trazabilidad de operaciones CRUD
     * ? Registra éxitos, errores y eventos importantes
     */
    private static final Logger log = LoggerFactory.getLogger(UsuarioRepositoryJdbc.class);

    // ========================================
    // OPERACIONES CRUD
    // ========================================

    /**
     * ! CREAR/GUARDAR USUARIO (INSERT)
     * ? Inserta un nuevo usuario en la tabla usuarios
     *
     * * Flujo de ejecución:
     * 1. Prepara SQL con parámetros (?, ?)
     * 2. Asigna valores a los parámetros (nombre, edad)
     * 3. Ejecuta el INSERT
     * 4. Recupera el ID generado automáticamente (AUTOINCREMENT)
     * 5. Asigna el ID al objeto Usuario
     * 6. Retorna el Usuario con el ID asignado
     *
     * ! SEGURIDAD:
     * - PreparedStatement previene SQL Injection
     * - Nunca concatenes valores directamente en el SQL
     *
     * * EJEMPLO DE SQL GENERADO:
     * INSERT INTO usuarios(nombre, edad) VALUES('Juan Pérez', 25)
     *
     * @param u Usuario a guardar (sin ID o con ID null)
     * @return Usuario guardado con ID asignado
     * @throws RuntimeException si falla la inserción
     */
    @Override
    public Usuario save(Usuario u) {
        // * SQL con placeholders (?) para parámetros
        String sql = "INSERT INTO usuarios(nombre, edad) VALUES(?,?)";

        // * Try-with-resources cierra automáticamente el PreparedStatement
        // * RETURN_GENERATED_KEYS permite recuperar el ID auto-generado
        try (PreparedStatement ps = Db.getConnection().prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {

            // ========================================
            // 1. ASIGNAR PARÁMETROS
            // ========================================
            ps.setString(1, u.getNombre()); // * Asigna el primer ? (nombre)
            ps.setInt(2, u.getEdad());      // * Asigna el segundo ? (edad)

            // ========================================
            // 2. EJECUTAR INSERT
            // ========================================
            ps.executeUpdate(); // * Ejecuta el INSERT y retorna filas afectadas

            // ========================================
            // 3. RECUPERAR ID GENERADO
            // ========================================
            try (ResultSet keys = ps.getGeneratedKeys()) {
                if (keys.next()) {
                    // * Asigna el ID generado al objeto Usuario
                    u.setId(keys.getInt(1)); // * Primera columna = ID
                }
            }

            return u;

        } catch (SQLException e) {
            // * Registra el error en el log
            log.error("Error guardando usuario", e);
            // * Envuelve SQLException en RuntimeException
            // ! En producción, considera crear excepciones personalizadas
            throw new RuntimeException(e);
        }
    }

    /**
     * ! BUSCAR USUARIO POR ID (SELECT con WHERE)
     * ? Busca un usuario por su identificador único
     *
     * * Flujo de ejecución:
     * 1. Prepara SQL con parámetro (id)
     * 2. Ejecuta SELECT
     * 3. Si existe resultado, mapea ResultSet a Usuario
     * 4. Retorna Optional<Usuario> (presente o vacío)
     *
     * * EJEMPLO DE SQL GENERADO:
     * SELECT * FROM usuarios WHERE id=5
     *
     * @param id Identificador del usuario
     * @return Optional con el usuario si existe, Optional.empty() si no existe
     * @throws RuntimeException si falla la consulta
     */
    @Override
    public Optional<Usuario> findById(int id) {
        String sql = "SELECT * FROM usuarios WHERE id=?";

        try (PreparedStatement ps = Db.getConnection().prepareStatement(sql)) {
            // ========================================
            // 1. ASIGNAR PARÁMETRO
            // ========================================
            ps.setInt(1, id); // * Asigna el ID al placeholder

            // ========================================
            // 2. EJECUTAR CONSULTA
            // ========================================
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    // * Si hay resultados, mapea la fila a Usuario
                    return Optional.of(map(rs));
                }
            }

            // * Si no hay resultados, retorna Optional vacío
            return Optional.empty();

        } catch (SQLException e) {
            log.error("Error buscando usuario por id", e);
            throw new RuntimeException(e);
        }
    }

    /**
     * ! LISTAR TODOS LOS USUARIOS (SELECT sin WHERE)
     * ? Recupera todos los usuarios ordenados por ID
     *
     * * Flujo de ejecución:
     * 1. Ejecuta SELECT * FROM usuarios ORDER BY id
     * 2. Itera sobre todas las filas del ResultSet
     * 3. Mapea cada fila a un objeto Usuario
     * 4. Añade cada Usuario a la lista
     * 5. Retorna la lista completa
     *
     * ! ADVERTENCIA:
     * - Sin paginación, puede retornar miles de registros
     * - Consume memoria proporcional al número de usuarios
     * - En producción, implementa paginación (LIMIT/OFFSET)
     *
     * @return Lista con todos los usuarios (vacía si no hay datos)
     * @throws RuntimeException si falla la consulta
     */
    @Override
    public List<Usuario> findAll() {
        String sql = "SELECT * FROM usuarios ORDER BY id";
        List<Usuario> lista = new ArrayList<>();

        // * Statement (no PreparedStatement) porque no hay parámetros
        try (Statement st = Db.getConnection().createStatement();
             ResultSet rs = st.executeQuery(sql)) {

            // ========================================
            // ITERAR SOBRE RESULTADOS
            // ========================================
            // * rs.next() avanza a la siguiente fila y retorna true si existe
            while (rs.next()) {
                lista.add(map(rs)); // * Mapea la fila actual a Usuario
            }

            return lista;

        } catch (SQLException e) {
            log.error("Error listando usuarios", e);
            throw new RuntimeException(e);
        }
    }

    /**
     * ! ACTUALIZAR USUARIO (UPDATE)
     * ? Actualiza los datos de un usuario existente
     *
     * * Flujo de ejecución:
     * 1. Prepara SQL con parámetros (nombre, edad, id)
     * 2. Ejecuta UPDATE
     * 3. Verifica filas afectadas (0 = ID no existe, >0 = actualizado)
     * 4. Retorna true/false según el resultado
     *
     * * EJEMPLO DE SQL GENERADO:
     * UPDATE usuarios SET nombre='Juan Pérez', edad=30 WHERE id=5
     *
     * @param u Usuario con ID y datos a actualizar
     * @return true si se actualizó, false si el ID no existe
     * @throws RuntimeException si falla la actualización
     */
    @Override
    public boolean update(Usuario u) {
        String sql = "UPDATE usuarios SET nombre=?, edad=? WHERE id=?";

        try (PreparedStatement ps = Db.getConnection().prepareStatement(sql)) {
            // ========================================
            // ASIGNAR PARÁMETROS
            // ========================================
            ps.setString(1, u.getNombre()); // * SET nombre = ?
            ps.setInt(2, u.getEdad());      // * SET edad = ?
            ps.setInt(3, u.getId());        // * WHERE id = ?

            // ========================================
            // EJECUTAR UPDATE Y VERIFICAR RESULTADO
            // ========================================
            // * executeUpdate() retorna el número de filas afectadas
            // * 0 filas = ID no existe, >0 filas = actualizado con éxito
            return ps.executeUpdate() > 0;

        } catch (SQLException e) {
            log.error("Error actualizando usuario", e);
            throw new RuntimeException(e);
        }
    }

    /**
     * ! ELIMINAR USUARIO POR ID (DELETE)
     * ? Elimina un usuario de la base de datos
     *
     * * Flujo de ejecución:
     * 1. Prepara SQL con parámetro (id)
     * 2. Ejecuta DELETE
     * 3. Verifica filas afectadas (0 = ID no existe, >0 = eliminado)
     * 4. Retorna true/false según el resultado
     *
     * * EJEMPLO DE SQL GENERADO:
     * DELETE FROM usuarios WHERE id=5
     *
     * ! IMPORTANTE:
     * - La eliminación es permanente
     * - Si hay claves foráneas, puede fallar por integridad referencial
     * - Considera implementar "soft delete" (borrado lógico)
     *
     * @param id Identificador del usuario a eliminar
     * @return true si se eliminó, false si el ID no existe
     * @throws RuntimeException si falla la eliminación
     */
    @Override
    public boolean delete(int id) {
        String sql = "DELETE FROM usuarios WHERE id=?";

        try (PreparedStatement ps = Db.getConnection().prepareStatement(sql)) {
            ps.setInt(1, id); // * WHERE id = ?
            return ps.executeUpdate() > 0; // * Retorna true si eliminó al menos 1 fila

        } catch (SQLException e) {
            log.error("Error eliminando usuario", e);
            throw new RuntimeException(e);
        }
    }

    // ========================================
    // MAPEO ResultSet → Usuario
    // ========================================

    /**
     * ! MAPEO DE ResultSet A Usuario
     * ? Convierte una fila de la base de datos a un objeto Usuario
     *
     * * Mapeo columna → atributo:
     * - id     → Usuario.id
     * - nombre → Usuario.nombre
     * - edad   → Usuario.edad
     *
     * ! IMPORTANTE:
     * - Los nombres de las columnas deben coincidir con el esquema de la BD
     * - Si cambias el nombre de una columna, actualiza este método
     * - En JPA/Hibernate esto se hace automáticamente con anotaciones
     *
     * ? ALTERNATIVA:
     * - Podrías usar rs.getInt(1), rs.getString(2), rs.getInt(3)
     * - Pero usar nombres de columnas es más legible y menos frágil
     *
     * @param rs ResultSet posicionado en una fila válida
     * @return Usuario mapeado desde la fila actual del ResultSet
     * @throws SQLException si falta una columna o hay error de tipo
     */
    private Usuario map(ResultSet rs) throws SQLException {
        return new Usuario(
                rs.getInt("id"),        // * Columna "id" → Integer id
                rs.getString("nombre"), // * Columna "nombre" → String nombre
                rs.getInt("edad")       // * Columna "edad" → int edad
        );
    }
}
