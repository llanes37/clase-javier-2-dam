package com.curso.ut20.service;

import com.curso.ut20.model.Usuario;
import com.curso.ut20.repository.UsuarioRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

/**
 * // ! CAPA DE SERVICIO — UsuarioService
 * ? Intermediario entre el Controller y el Repository.
 * ? Aquí vive la LÓGICA DE NEGOCIO: validaciones extra, transformaciones y
 * coordinación.
 *
 * * ¿POR QUÉ NECESITAMOS @Service si el Controller ya funciona?
 *
 * Sin capa Service (arquitectura de 2 capas — esto es un anti-patrón):
 * ┌────────────────┐ ┌────────────────────┐
 * │ Controller │──────▶│ Repository (BD) │
 * └────────────────┘ └────────────────────┘
 *
 * Con capa Service (arquitectura de 3 capas — buena práctica):
 * ┌────────────────┐ ┌────────────────┐ ┌────────────────────┐
 * │ Controller │──────▶│ Service │──────▶│ Repository (BD) │
 * │ (HTTP/JSON) │ │ (Negocio) │ │ (SQL/JPA) │
 * └────────────────┘ └────────────────┘ └────────────────────┘
 *
 * * VENTAJAS DE SEPARAR EN @Service:
 * ✓ El Controller solo gestiona HTTP (request/response)
 * ✓ El Service tiene lógica de negocio reutilizable desde múltiples controllers
 * ✓ El Repository solo accede a datos (sin validaciones)
 * ✓ TESTING: podemos testear el Service sin servidor HTTP (más rápido)
 * ✓ Transacciones (@Transactional) viven aquí, no en el Controller
 *
 * ! ANOTACIÓN @Service:
 * - Es un @Component especializado para la capa de negocio
 * - Spring la detecta automáticamente y la gestiona como un bean singleton
 * - Es semánticamente equivalente a @Component pero más expresiva
 *
 * TODO (Alumno):
 * - Añadir @Transactional en métodos que modifiquen datos
 * - Implementar paginación: Page<Usuario> listarPaginado(Pageable pageable)
 * - Añadir búsqueda: List<Usuario> buscarPorNombre(String nombre)
 * - Implementar conversión DTO ↔ Entidad (para desacoplar API de BD)
 */
@Service // * Marca esta clase como bean de la capa de negocio para Spring
public class UsuarioService {

    // ========================================
    // INYECCIÓN DE DEPENDENCIAS
    // ========================================

    /**
     * ! REPOSITORIO INYECTADO VÍA CONSTRUCTOR
     * ? Spring detecta el único constructor y lo usa para inyectar dependencias.
     * * No necesitamos @Autowired si hay un solo constructor (convención Spring
     * Boot 3+).
     * * final garantiza inmutabilidad: el repositorio no cambia después de
     * inyectarse.
     */
    private final UsuarioRepository repo;

    /**
     * ? Constructor con inyección de dependencias
     * * Spring busca automáticamente un bean de tipo UsuarioRepository
     * * y lo pasa aquí al crear el UsuarioService.
     *
     * @param repo Repositorio JPA de Usuario (implementado automáticamente por
     *             Spring Data)
     */
    public UsuarioService(UsuarioRepository repo) {
        this.repo = repo;
    }

    // ========================================
    // OPERACIONES DE NEGOCIO
    // ========================================

    /**
     * ! LISTAR todos los usuarios
     * ? Recupera todos los usuarios de la base de datos H2.
     *
     * * En este caso simple solo delegamos en el repo.
     * * En un caso real, aquí podríamos: filtrar, transformar a DTO, ordenar, etc.
     *
     * ! ADVERTENCIA: Sin paginación puede retornar miles de registros.
     * TODO: Implementar List<Usuario> listarPaginado(int page, int size)
     *
     * @return Lista con todos los usuarios (vacía si no hay ninguno)
     */
    public List<Usuario> listar() {
        // * SELECT * FROM usuario ORDER BY id (generado por Hibernate)
        return repo.findAll();
    }

    /**
     * ! BUSCAR usuario por ID
     * ? Usa Optional para evitar retornar null (programación defensiva).
     *
     * * COMPARACIÓN con y sin Optional:
     * ┌──────────────────────────────────────────────────────────────────┐
     * │ SIN Optional (código frágil): │
     * │ Usuario u = service.buscar(5); // ¿qué pasa si no existe? │
     * │ System.out.println(u.getNombre()); // NullPointerException !!! │
     * │ │
     * │ CON Optional (código seguro): │
     * │ service.buscar(5) │
     * │ .ifPresent(u -> System.out.println(u.getNombre())); // Seguro│
     * └──────────────────────────────────────────────────────────────────┘
     *
     * @param id ID del usuario a buscar
     * @return Optional con el usuario si existe, Optional.empty() si no existe
     */
    public Optional<Usuario> buscar(Long id) {
        // * findById retorna Optional<Usuario> — no null
        return repo.findById(id);
    }

    /**
     * ! CREAR un nuevo usuario
     * ? Valida los datos y lo persiste en la BD.
     *
     * * FLUJO:
     * 1. Validar datos de negocio (nombre, edad) — reglas propias del dominio
     * 2. Persistir en BD via repositorio
     * 3. Retornar el usuario con el ID generado automáticamente
     *
     * ! NOTA sobre validaciones:
     * Las validaciones de @NotBlank y @Min están en la entidad Usuario y
     * se activan con @Valid en el Controller (antes de llegar aquí).
     * Las validaciones aquí son adicionales de negocio (ej: nombre único).
     *
     * TODO: Añadir validación de nombre único:
     * if (repo.findByNombre(u.getNombre()).isPresent()) {
     * throw new IllegalArgumentException("Ya existe un usuario con ese nombre");
     * }
     *
     * @param u Usuario a crear (ya validado por @Valid en el Controller)
     * @return Usuario creado con ID asignado por la BD
     */
    public Usuario crear(Usuario u) {
        // * INSERT INTO usuario (nombre, edad) VALUES (?, ?)
        // * Hibernate asigna el ID automáticamente (IDENTITY strategy)
        return repo.save(u);
    }

    /**
     * ! ACTUALIZAR un usuario existente
     * ? Busca el usuario por ID, copia los nuevos datos y persiste.
     *
     * * Por qué buscamos primero en lugar de guardar directamente:
     * - Garantizamos que el usuario existe antes de actualizar
     * - Si save() recibe un ID que no existe, JPA haría un INSERT (¡incorrecto!)
     * - Retornamos Optional para que el Controller pueda devolver 404 si no existe
     *
     * * FLUJO:
     * 1. Buscar usuario por ID
     * 2. Si no existe → retornar Optional.empty() (el Controller devolverá 404)
     * 3. Si existe → copiar datos del DTO, guardar y retornar
     *
     * @param id    ID del usuario a actualizar
     * @param datos Objeto con los nuevos datos (nombre, edad)
     * @return Optional con el usuario actualizado, o empty() si no existe
     */
    public Optional<Usuario> actualizar(Long id, Usuario datos) {
        // * Búsqueda segura con Optional — no lanzamos excepción aquí,
        // * dejamos que el Controller decida qué hacer (404, etc.)
        return repo.findById(id).map(u -> {
            // * Solo actualizamos los campos permitidos (nunca el ID)
            u.setNombre(datos.getNombre()); // * SET nombre = ?
            u.setEdad(datos.getEdad()); // * SET edad = ?
            // * UPDATE usuario SET nombre=?, edad=? WHERE id=?
            return repo.save(u);
        });
    }

    /**
     * ! VERIFICAR si un usuario existe por ID
     * ? Utilidad para el Controller: comprobar antes de borrar.
     *
     * * SELECT COUNT(1) FROM usuario WHERE id = ? — más eficiente que findById()
     * * porque no carga la entidad completa en memoria.
     *
     * @param id ID a verificar
     * @return true si existe, false si no existe
     */
    public boolean existe(Long id) {
        // * Más eficiente que findById() para verificaciones de existencia
        return repo.existsById(id);
    }

    /**
     * ! BORRAR un usuario por ID
     * ? Elimina el registro de la BD si existe.
     *
     * * El Controller llama primero a existe() para devolver 404 si no existe.
     * * Aquí simplemente ejecutamos el DELETE.
     *
     * @param id ID del usuario a eliminar
     */
    public void borrar(Long id) {
        // * DELETE FROM usuario WHERE id = ?
        repo.deleteById(id);
    }
}
