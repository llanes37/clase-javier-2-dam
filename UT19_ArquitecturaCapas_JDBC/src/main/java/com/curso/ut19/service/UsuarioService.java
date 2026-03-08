package com.curso.ut19.service;

import com.curso.ut19.model.Usuario;
import com.curso.ut19.repository.UsuarioRepository;

import java.util.List;
import java.util.Optional;

/**
 * //! CAPA DE SERVICIO - LÓGICA DE NEGOCIO DE USUARIO
 * ? Contiene las reglas de negocio y validaciones antes de persistir datos
 *
 * * RESPONSABILIDADES DE LA CAPA DE SERVICIO:
 *   ✓ Validar datos de entrada (nombre no vacío, edad >= 0)
 *   ✓ Aplicar reglas de negocio de la aplicación
 *   ✓ Coordinar operaciones entre múltiples repositorios (transacciones)
 *   ✓ Transformar datos entre capas (DTOs → Entidades)
 *   ✓ Gestionar excepciones de negocio
 *
 * ! SEPARACIÓN DE RESPONSABILIDADES:
 *   - Repositorio: Solo acceso a datos (sin validaciones de negocio)
 *   - Servicio: Validaciones, reglas de negocio, coordinación
 *   - Controlador: Solo presentación y manejo de entrada/salida
 *
 * ? INYECCIÓN DE DEPENDENCIAS:
 *   - El servicio depende de la interfaz UsuarioRepository, no de la implementación
 *   - Permite cambiar la implementación (JDBC → JPA) sin modificar el servicio
 *   - Facilita el testing con mocks (UsuarioRepositoryMock)
 *
 * * EJEMPLO DE FLUJO:
 *   1. Controller solicita crear usuario
 *   2. Service valida los datos (nombre, edad)
 *   3. Service llama al repository.save()
 *   4. Repository inserta en BD y retorna Usuario con ID
 *   5. Service retorna el Usuario al Controller
 *   6. Controller muestra el ID generado al usuario
 *
 * TODO (Alumno):
 *   - Añade validaciones más sofisticadas:
 *     * Longitud mínima/máxima del nombre
 *     * Nombre sin caracteres especiales
 *     * Rango de edad válido (0-120)
 *   - Implementa transacciones para operaciones complejas
 *   - Añade métodos de negocio (activarUsuario, suspenderUsuario)
 *   - Implementa conversión de DTOs a Entidades
 */
public class UsuarioService {

    // ========================================
    // DEPENDENCIAS
    // ========================================

    /**
     * ! REPOSITORIO DE USUARIO
     * ? Interfaz que abstrae el acceso a datos
     * * final: La referencia no puede cambiar después de la construcción
     * * Inyectada por constructor (Dependency Injection)
     */
    private final UsuarioRepository repository;

    // ========================================
    // CONSTRUCTOR (Inyección de Dependencias)
    // ========================================

    /**
     * ! CONSTRUCTOR CON INYECCIÓN DE DEPENDENCIAS
     * ? Recibe la implementación del repositorio desde fuera
     *
     * * Ventajas de la inyección por constructor:
     * - Permite testing fácil con mocks
     * - Hace explícitas las dependencias
     * - Asegura que el servicio está completamente inicializado
     * - Es inmutable (final) una vez construido
     *
     * * En Spring, esto se hace automáticamente con @Autowired
     * * Aquí lo hacemos manualmente en Application.main()
     *
     * @param repository Implementación del repositorio de usuario
     */
    public UsuarioService(UsuarioRepository repository) {
        this.repository = repository;
    }

    // ========================================
    // OPERACIONES DE NEGOCIO (CRUD + Validaciones)
    // ========================================

    /**
     * ! CREAR USUARIO
     * ? Valida los datos y crea un nuevo usuario en la base de datos
     *
     * * Flujo de ejecución:
     * 1. Valida nombre (no vacío)
     * 2. Valida edad (>= 0)
     * 3. Crea objeto Usuario sin ID
     * 4. Delega en repository.save()
     * 5. Retorna Usuario con ID asignado
     *
     * ! VALIDACIONES APLICADAS:
     * - Nombre no puede ser null ni vacío (trim)
     * - Edad no puede ser negativa
     *
     * * Ejemplo de uso:
     * <pre>
     * try {
     *     Usuario u = service.crear("Juan Pérez", 25);
     *     System.out.println("Usuario creado con ID: " + u.getId());
     * } catch (IllegalArgumentException e) {
     *     System.out.println("Error: " + e.getMessage());
     * }
     * </pre>
     *
     * @param nombre Nombre del usuario (no vacío)
     * @param edad Edad del usuario (>= 0)
     * @return Usuario creado con ID asignado
     * @throws IllegalArgumentException si los datos no son válidos
     * @throws RuntimeException si falla la inserción en BD
     */
    public Usuario crear(String nombre, int edad) {
        // ========================================
        // 1. VALIDAR DATOS DE ENTRADA
        // ========================================
        validar(nombre, edad);

        // ========================================
        // 2. CREAR Y PERSISTIR USUARIO
        // ========================================
        // * Crea Usuario sin ID (será generado por la BD)
        // * Delega en el repositorio para la persistencia
        return repository.save(new Usuario(nombre, edad));
    }

    /**
     * ! OBTENER USUARIO POR ID
     * ? Busca un usuario por su identificador
     *
     * * Uso de Optional:
     * - Evita retornar null
     * - Obliga al código cliente a manejar la ausencia de datos
     * - Permite encadenar operaciones (map, flatMap, filter)
     *
     * * Ejemplo de uso:
     * <pre>
     * service.obtener(5)
     *     .ifPresent(u -> System.out.println("Encontrado: " + u.getNombre()));
     *
     * Usuario u = service.obtener(5)
     *     .orElseThrow(() -> new NotFoundException("Usuario no encontrado"));
     * </pre>
     *
     * @param id Identificador del usuario
     * @return Optional con el usuario si existe, Optional.empty() si no existe
     * @throws RuntimeException si falla la consulta a BD
     */
    public Optional<Usuario> obtener(int id) {
        // * Sin validaciones adicionales de negocio
        // * Delega directamente en el repositorio
        return repository.findById(id);
    }

    /**
     * ! LISTAR TODOS LOS USUARIOS
     * ? Recupera todos los usuarios de la base de datos
     *
     * * Comportamiento:
     * - Delega en repository.findAll()
     * - Retorna lista vacía si no hay usuarios
     * - Nunca retorna null
     *
     * ! ADVERTENCIA:
     * - Sin paginación, puede retornar miles de registros
     * - En producción, implementa paginación
     *
     * * Ejemplo de uso:
     * <pre>
     * List<Usuario> usuarios = service.listar();
     * usuarios.forEach(u -> System.out.println(u.getNombre()));
     * </pre>
     *
     * @return Lista con todos los usuarios (vacía si no hay datos)
     * @throws RuntimeException si falla la consulta a BD
     */
    public List<Usuario> listar() {
        // * Sin validaciones ni transformaciones
        // * Delega directamente en el repositorio
        return repository.findAll();
    }

    /**
     * ! ACTUALIZAR USUARIO
     * ? Valida los datos y actualiza un usuario existente
     *
     * * Flujo de ejecución:
     * 1. Valida nombre y edad (reglas de negocio)
     * 2. Crea objeto Usuario con el ID y nuevos datos
     * 3. Delega en repository.update()
     * 4. Retorna true si se actualizó, false si el ID no existe
     *
     * ! VALIDACIONES APLICADAS:
     * - Nombre no puede ser null ni vacío
     * - Edad no puede ser negativa
     *
     * * Ejemplo de uso:
     * <pre>
     * try {
     *     boolean ok = service.actualizar(5, "Juan Pérez", 30);
     *     if (ok) {
     *         System.out.println("Usuario actualizado");
     *     } else {
     *         System.out.println("ID no encontrado");
     *     }
     * } catch (IllegalArgumentException e) {
     *     System.out.println("Datos inválidos: " + e.getMessage());
     * }
     * </pre>
     *
     * @param id ID del usuario a actualizar
     * @param nombre Nuevo nombre (no vacío)
     * @param edad Nueva edad (>= 0)
     * @return true si se actualizó, false si el ID no existe
     * @throws IllegalArgumentException si los datos no son válidos
     * @throws RuntimeException si falla la actualización en BD
     */
    public boolean actualizar(int id, String nombre, int edad) {
        // ========================================
        // 1. VALIDAR DATOS DE ENTRADA
        // ========================================
        validar(nombre, edad);

        // ========================================
        // 2. ACTUALIZAR USUARIO
        // ========================================
        // * Crea Usuario con ID y nuevos datos
        // * Delega en el repositorio para la actualización
        return repository.update(new Usuario(id, nombre, edad));
    }

    /**
     * ! BORRAR USUARIO
     * ? Elimina un usuario de la base de datos por su ID
     *
     * * Comportamiento:
     * - Delega en repository.delete()
     * - Retorna true si se eliminó, false si el ID no existe
     * - La eliminación es permanente
     *
     * ! IMPORTANTE:
     * - No hay confirmación ni papelera de reciclaje
     * - Si hay claves foráneas, puede fallar
     * - Considera implementar "soft delete" (borrado lógico)
     *
     * * Ejemplo de uso:
     * <pre>
     * boolean ok = service.borrar(5);
     * if (ok) {
     *     System.out.println("Usuario eliminado");
     * } else {
     *     System.out.println("ID no encontrado");
     * }
     * </pre>
     *
     * @param id Identificador del usuario a eliminar
     * @return true si se eliminó, false si el ID no existe
     * @throws RuntimeException si falla la eliminación (ej: violación FK)
     */
    public boolean borrar(int id) {
        // * Sin validaciones adicionales de negocio
        // * Delega directamente en el repositorio
        return repository.delete(id);
    }

    // ========================================
    // VALIDACIONES PRIVADAS
    // ========================================

    /**
     * ! VALIDACIÓN DE DATOS DE USUARIO
     * ? Aplica las reglas de negocio para nombre y edad
     *
     * * Reglas aplicadas:
     * 1. Nombre no puede ser null
     * 2. Nombre no puede estar vacío (trim)
     * 3. Edad no puede ser negativa
     *
     * ! IMPORTANTE:
     * - Lanza IllegalArgumentException con mensaje descriptivo
     * - El código cliente debe capturar la excepción
     * - En frameworks, se usarían anotaciones (@NotBlank, @Min)
     *
     * ? MEJORAS POSIBLES:
     * - Validar longitud mínima/máxima del nombre
     * - Validar caracteres permitidos (solo letras y espacios)
     * - Validar rango de edad (0-120)
     * - Validar formato de email (si se añade)
     *
     * @param nombre Nombre a validar
     * @param edad Edad a validar
     * @throws IllegalArgumentException si alguna validación falla
     */
    private void validar(String nombre, int edad) {
        // ========================================
        // VALIDACIÓN 1: NOMBRE NO VACÍO
        // ========================================
        // * Verifica null, cadena vacía y solo espacios
        if (nombre == null || nombre.trim().isEmpty()) {
            throw new IllegalArgumentException("El nombre no puede estar vacío");
        }

        // ========================================
        // VALIDACIÓN 2: EDAD NO NEGATIVA
        // ========================================
        // * Verifica que la edad sea >= 0
        // ! TODO: Considera añadir un límite superior (ej: 120)
        if (edad < 0) {
            throw new IllegalArgumentException("La edad no puede ser negativa");
        }
    }
}
