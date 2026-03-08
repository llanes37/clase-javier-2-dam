package com.curso.ut19;

import com.curso.ut19.repository.UsuarioRepository;
import com.curso.ut19.repository.jdbc.UsuarioRepositoryJdbc;
import com.curso.ut19.service.UsuarioService;
import com.curso.ut19.persistence.Db;

import java.util.Scanner;

/**
 * //! UT19 — ARQUITECTURA EN CAPAS CON JDBC + JUnit + Maven + Logging
 * ? Proyecto educativo que demuestra la arquitectura en capas profesional con JDBC
 *
 * * ARQUITECTURA DEL PROYECTO:
 *   - model/         → Entidades de dominio (Usuario)
 *   - persistence/   → Gestor de conexión JDBC (Db)
 *   - repository/    → Interfaces de acceso a datos (Repository Pattern)
 *   - service/       → Lógica de negocio y validaciones
 *   - Application    → Capa de presentación (CLI)
 *
 * ! PATRONES DE DISEÑO APLICADOS:
 *   ✓ Repository Pattern     - Abstracción de persistencia
 *   ✓ Service Layer          - Lógica de negocio separada
 *   ✓ Dependency Injection   - Inyección manual por constructor
 *   ✓ Singleton              - Conexión única de BD
 *
 * ? OBJETIVO:
 *   - Refactorizar prácticas UT17/UT18 hacia un diseño profesional y mantenible
 *   - Preparar el camino para frameworks como Spring Boot
 *
 * TODO (Alumno):
 *   - Extiende la arquitectura para entidades Producto y Categoría
 *   - Implementa relaciones entre entidades (1:N, N:M)
 */
public class Application {

    // * Scanner global para toda la aplicación
    private static final Scanner sc = new Scanner(System.in);

    /**
     * ! MÉTODO MAIN - PUNTO DE ENTRADA
     * ? Configura las capas y ejecuta el menú principal
     *
     * * Flujo de inicialización:
     * 1. Crea el repositorio JDBC (capa de datos)
     * 2. Inyecta el repositorio en el servicio (capa de negocio)
     * 3. Ejecuta el menú interactivo (capa de presentación)
     * 4. Cierra recursos al salir
     */
    public static void main(String[] args) {
        // ========================================
        // WIRING MANUAL (Dependency Injection)
        // ========================================
        // * En frameworks como Spring, esto se hace automáticamente
        // * Aquí lo hacemos manualmente para entender el concepto

        UsuarioRepository repo = new UsuarioRepositoryJdbc(); // * Implementación concreta JDBC
        UsuarioService service = new UsuarioService(repo);     // * Inyección por constructor

        // ========================================
        // BUCLE PRINCIPAL DEL MENÚ
        // ========================================
        int opcion;
        do {
            // ================================
            // 📋 MENÚ PRINCIPAL — UT19
            // ================================
            System.out.println("\n==================================");
            System.out.println("  MENÚ DE PRÁCTICAS - UT19 (Capas)");
            System.out.println("==================================");
            System.out.println(" 1. Insertar usuario");
            System.out.println(" 2. Listar usuarios");
            System.out.println(" 3. Actualizar usuario por ID");
            System.out.println(" 4. Eliminar usuario por ID");
            System.out.println(" 5. Salir (cerrar BD)");
            System.out.print("👉 Selecciona opción: ");
            opcion = readInt();

            // * Switch con sintaxis moderna de Java (arrow functions)
            switch (opcion) {
                case 1 -> insertar(service);
                case 2 -> listar(service);
                case 3 -> actualizar(service);
                case 4 -> eliminar(service);
                case 5 -> Db.close(); // * Cierra la conexión SQLite
                default -> System.out.println("❌ Opción inválida.");
            }
        } while (opcion != 5);

        // ========================================
        // CIERRE DE RECURSOS
        // ========================================
        sc.close();
        System.out.println("👋 Programa finalizado. ¡Hasta luego!");
    }

    // ========================================
    // UTILIDADES DE ENTRADA - LECTURA SEGURA
    // ========================================

    /**
     * ! LECTURA SEGURA DE ENTEROS
     * ? Repite hasta recibir un número válido
     * * Limpia el buffer con nextLine() para evitar bucles infinitos
     *
     * @return Entero válido ingresado por el usuario
     */
    private static int readInt() {
        while (!sc.hasNextInt()) {
            System.out.print("❌ Número inválido: ");
            sc.next(); // * Descarta entrada inválida
        }
        int val = sc.nextInt();
        sc.nextLine(); // * Limpia el salto de línea pendiente
        return val;
    }

    /**
     * ! LECTURA SEGURA DE CADENAS NO VACÍAS
     * ? Repite hasta recibir una cadena con contenido
     * * Aplica trim() para eliminar espacios en blanco
     *
     * @param prompt Mensaje a mostrar al usuario
     * @return Cadena no vacía ingresada por el usuario
     */
    private static String readNonEmpty(String prompt) {
        while (true) {
            System.out.print(prompt);
            String s = sc.nextLine().trim();
            if (!s.isEmpty()) return s;
            System.out.println("❌ No puede estar vacío.");
        }
    }

    // ========================================
    // CASOS DE USO (CRUD)
    // ========================================
    // * Estos métodos delegan en la capa de servicio
    // * No contienen lógica de negocio, solo presentación

    /**
     * ! CASO DE USO: CREAR USUARIO
     * ? Solicita datos al usuario y los envía al servicio
     *
     * Flujo:
     * 1. Solicita nombre (validado no vacío en UI)
     * 2. Solicita edad
     * 3. Llama a service.crear() que aplica validaciones de negocio
     * 4. Muestra ID generado o error
     *
     * @param service Servicio de usuario
     */
    private static void insertar(UsuarioService service) {
        String nombre = readNonEmpty("Nombre: ");
        System.out.print("Edad: ");
        int edad = readInt();

        try {
            var u = service.crear(nombre, edad); // * var = inferencia de tipos (Java 10+)
            System.out.println("✅ Insertado con ID: " + u.getId());
        } catch (Exception e) {
            // * El servicio lanza IllegalArgumentException si la validación falla
            System.out.println("❌ " + e.getMessage());
        }
    }

    /**
     * ! CASO DE USO: LISTAR USUARIOS
     * ? Muestra todos los usuarios en formato tabular
     *
     * * Formato de salida:
     * ID | Nombre           | Edad
     * ---+------------------+-----
     *  1 | Juan Pérez       |  25
     *
     * @param service Servicio de usuario
     */
    private static void listar(UsuarioService service) {
        System.out.println("ID | Nombre           | Edad");
        System.out.println("---+------------------+-----");

        // * forEach con lambda para iterar sobre la lista
        // * printf permite formateo alineado: %2d = entero con 2 caracteres
        service.listar().forEach(u ->
                System.out.printf("%2d | %-16s | %3d%n",
                        u.getId(),
                        u.getNombre(),
                        u.getEdad())
        );
    }

    /**
     * ! CASO DE USO: ACTUALIZAR USUARIO
     * ? Solicita ID y nuevos datos, luego actualiza el usuario
     *
     * Flujo:
     * 1. Solicita ID del usuario a actualizar
     * 2. Solicita nuevos datos (nombre y edad)
     * 3. Llama a service.actualizar() que aplica validaciones
     * 4. Informa si se actualizó o si el ID no existe
     *
     * @param service Servicio de usuario
     */
    private static void actualizar(UsuarioService service) {
        System.out.print("ID a actualizar: ");
        int id = readInt();

        String nombre = readNonEmpty("Nuevo nombre: ");
        System.out.print("Nueva edad: ");
        int edad = readInt();

        try {
            boolean ok = service.actualizar(id, nombre, edad);
            // * Operador ternario para mensaje condicional
            System.out.println(ok ? "✅ Actualizado." : "⚠️ ID no encontrado.");
        } catch (Exception e) {
            System.out.println("❌ " + e.getMessage());
        }
    }

    /**
     * ! CASO DE USO: ELIMINAR USUARIO
     * ? Solicita ID y elimina el usuario de la base de datos
     *
     * Flujo:
     * 1. Solicita ID del usuario a eliminar
     * 2. Llama a service.borrar()
     * 3. Informa si se eliminó o si el ID no existe
     *
     * @param service Servicio de usuario
     */
    private static void eliminar(UsuarioService service) {
        System.out.print("ID a eliminar: ");
        int id = readInt();

        boolean ok = service.borrar(id);
        System.out.println(ok ? "✅ Eliminado." : "⚠️ ID no encontrado.");
    }
}
