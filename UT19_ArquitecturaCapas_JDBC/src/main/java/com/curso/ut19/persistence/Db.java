package com.curso.ut19.persistence;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * //! GESTOR DE CONEXIÓN JDBC - SQLITE
 * ? Centraliza la gestión de la conexión a la base de datos
 *
 * * PATRÓN SINGLETON:
 *   - Una única instancia de Connection compartida
 *   - Adecuado para aplicaciones pequeñas/demos
 *   - NO recomendado para producción (usar pool de conexiones)
 *
 * ! RESPONSABILIDADES:
 *   ✓ Crear y mantener la conexión SQLite
 *   ✓ Configurar PRAGMA foreign_keys
 *   ✓ Crear el esquema de la base de datos
 *   ✓ Cerrar la conexión de forma segura
 *   ✓ Logging de eventos con SLF4J
 *
 * TODO (Mejoras):
 *   - Implementar pool de conexiones (HikariCP, C3P0)
 *   - Separar la creación del esquema a archivos SQL
 *   - Añadir configuración externa (properties, yml)
 */
public class Db {

    // ========================================
    // LOGGING
    // ========================================

    /**
     * * Logger de SLF4J para trazabilidad
     * ? Permite cambiar la implementación de logging sin modificar código
     */
    private static final Logger log = LoggerFactory.getLogger(Db.class);

    // ========================================
    // SINGLETON
    // ========================================

    /**
     * ! INSTANCIA ÚNICA DE CONEXIÓN
     * ? null hasta la primera llamada a getConnection()
     * * volatile asegura visibilidad en entornos multi-hilo (opcional para este caso)
     */
    private static Connection connection;

    // * Constructor privado para prevenir instanciación
    private Db() {}

    /**
     * ! OBTENER CONEXIÓN (SINGLETON + LAZY INITIALIZATION)
     * ? Crea la conexión solo si no existe (lazy initialization)
     *
     * * Flujo de inicialización:
     * 1. Verifica si ya existe una conexión
     * 2. Carga el driver JDBC de SQLite
     * 3. Conecta a la base de datos (archivo miBaseDatos.db)
     * 4. Activa claves foráneas (PRAGMA foreign_keys = ON)
     * 5. Crea la tabla usuarios si no existe
     * 6. Registra el evento en el log
     *
     * ! ESQUEMA DE LA TABLA USUARIOS:
     * - id: INTEGER PRIMARY KEY AUTOINCREMENT
     * - nombre: TEXT NOT NULL
     * - edad: INTEGER NOT NULL CHECK(edad >= 0)
     *
     * @return Conexión JDBC activa
     * @throws RuntimeException si falla la conexión
     */
    public static Connection getConnection() {
        if (connection == null) {
            try {
                // ========================================
                // 1. CARGAR DRIVER JDBC
                // ========================================
                // * org.sqlite.JDBC registra el driver en DriverManager
                Class.forName("org.sqlite.JDBC");

                // ========================================
                // 2. ESTABLECER CONEXIÓN
                // ========================================
                // * jdbc:sqlite:miBaseDatos.db crea el archivo si no existe
                // * El archivo se almacena en el directorio raíz del proyecto
                connection = DriverManager.getConnection("jdbc:sqlite:miBaseDatos.db");

                // ========================================
                // 3. CONFIGURAR SQLITE + CREAR ESQUEMA
                // ========================================
                try (Statement st = connection.createStatement()) {
                    // * Activa integridad referencial (claves foráneas)
                    st.execute("PRAGMA foreign_keys = ON");

                    // * Crea la tabla usuarios si no existe
                    // ! CREATE TABLE IF NOT EXISTS evita errores en ejecuciones posteriores
                    st.execute("CREATE TABLE IF NOT EXISTS usuarios (" +
                            "id INTEGER PRIMARY KEY AUTOINCREMENT, " +  // * Auto-incremento de ID
                            "nombre TEXT NOT NULL, " +                   // * Nombre obligatorio
                            "edad INTEGER NOT NULL CHECK(edad >= 0))");  // * Edad >= 0
                }

                // ========================================
                // 4. LOGGING
                // ========================================
                log.info("Conexión SQLite abierta en miBaseDatos.db");

            } catch (SQLException | ClassNotFoundException e) {
                // * Envuelve excepciones checked en RuntimeException
                // ! En producción, considera un manejo más sofisticado
                throw new RuntimeException("Error abriendo conexión SQLite", e);
            }
        }
        return connection;
    }

    /**
     * ! CERRAR CONEXIÓN
     * ? Cierra la conexión de forma segura y resetea la variable
     *
     * * Buenas prácticas:
     * - Verifica que la conexión no sea null
     * - Maneja SQLException
     * - Resetea la variable a null para permitir reconexión
     * - Registra el evento en el log
     *
     * ? Llamar este método al finalizar la aplicación
     */
    public static void close() {
        if (connection != null) {
            try {
                connection.close();
                log.info("Conexión SQLite cerrada");
            } catch (SQLException e) {
                // * Log del error pero no lanza excepción (método de limpieza)
                log.error("Error cerrando conexión", e);
            }
            // * Resetea la variable para permitir reconexión futura
            connection = null;
        }
    }
}
