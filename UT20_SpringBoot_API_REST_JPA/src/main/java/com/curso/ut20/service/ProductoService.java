package com.curso.ut20.service;

import com.curso.ut20.model.Producto;
import com.curso.ut20.repository.ProductoRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

/**
 * // ! CAPA DE SERVICIO — ProductoService
 * ? Intermediario entre ProductoController y ProductoRepository.
 *
 * * ARQUITECTURA DE 3 CAPAS (patrón profesional):
 * ┌─────────────────────┐ ┌──────────────────┐ ┌───────────────────┐
 * │ ProductoController │──────▶│ ProductoService │──────▶│ ProductoRepository │
 * │ (HTTP/JSON) │ │ (@Service) │ │ (JPA/H2) │
 * │ @RestController │◀──────│ Lógica negocio │◀──────│ SQL generado │
 * └─────────────────────┘ └──────────────────┘ └───────────────────┘
 *
 * ! @Service VS @Component VS @Repository:
 * 
 * @Component → Bean genérico (cualquier capa)
 * @Service → Bean de la capa de negocio (semántico + interceptable con AOP)
 * @Repository → Bean de acceso a datos (manejo especial de excepciones JPA)
 *             Todos son @Components. Los nombres son para expresar intención y
 *             habilitar AOP.
 *
 *             TODO (Alumno):
 *             - Añadir validación de precio: si precio=0, avisar (pero
 *             permitirlo)
 *             - Implementar buscarPorNombre(String nombre) usando el
 *             repositorio
 *             - Implementar buscarBaratos(double precioMax) usando @Query en el
 *             repo
 *             - Añadir @Transactional en métodos de escritura (crear,
 *             actualizar, borrar)
 */
@Service // * Spring crea e inyecta automáticamente esta clase donde se necesite
public class ProductoService {

    // ========================================
    // INYECCIÓN DE DEPENDENCIAS
    // ========================================

    /**
     * ! REPOSITORIO inyectado por constructor (inyección recomendada en Spring Boot
     * 3+)
     * * No hace falta @Autowired — Spring detecta el único constructor
     * automáticamente.
     * * final: inmutable tras la construcción (buena práctica con DI).
     */
    private final ProductoRepository repo;

    public ProductoService(ProductoRepository repo) {
        this.repo = repo;
    }

    // ========================================
    // OPERACIONES DE NEGOCIO
    // ========================================

    /**
     * ! LISTAR todos los productos
     * * SELECT * FROM producto
     * TODO: Añadir paginación → Page<Producto> listar(Pageable pageable)
     *
     * @return Lista con todos los productos (vacía si no hay ninguno)
     */
    public List<Producto> listar() {
        return repo.findAll();
    }

    /**
     * ! BUSCAR producto por ID
     * ? Retorna Optional para gestionar de forma segura la ausencia del producto.
     *
     * * El Controller puede hacer:
     * service.buscar(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build())
     *
     * @param id ID del producto
     * @return Optional con el producto si existe, empty() si no
     */
    public Optional<Producto> buscar(Long id) {
        return repo.findById(id);
    }

    /**
     * ! CREAR un nuevo producto
     * ? Persiste el producto en H2 y retorna la entidad con el ID asignado.
     *
     * * Las validaciones de @NotBlank y @Min ya se aplicaron en el Controller
     * * con @Valid antes de llegar aquí. Aquí podemos añadir reglas extra.
     *
     * Ejemplo de regla de negocio que podrías añadir:
     * if (p.getPrecio() == 0) { log.warn("Producto '{}' con precio 0",
     * p.getNombre()); }
     *
     * @param p Producto a crear (ya validado por @Valid)
     * @return Producto creado con ID asignado por H2
     */
    public Producto crear(Producto p) {
        // * INSERT INTO producto (nombre, precio) VALUES (?, ?)
        return repo.save(p);
    }

    /**
     * ! ACTUALIZAR un producto existente
     * ? Busca, modifica campos y persiste.
     *
     * * Por qué no usamos repo.save(datos) directamente:
     * - datos tiene el ID del path (URL), pero si fuera 0 o null, JPA haría INSERT.
     * - Al buscar primero, garantizamos que el ID existe y hacemos UPDATE.
     *
     * @param id    ID del producto a actualizar
     * @param datos Producto con nuevos valores (nombre, precio)
     * @return Optional con el producto actualizado, o empty() si no existe (el
     *         Controller devolverá 404)
     */
    public Optional<Producto> actualizar(Long id, Producto datos) {
        return repo.findById(id).map(p -> {
            p.setNombre(datos.getNombre()); // * Actualizar campos editables
            p.setPrecio(datos.getPrecio()); // * El ID nunca se modifica
            // * UPDATE producto SET nombre=?, precio=? WHERE id=?
            return repo.save(p);
        });
    }

    /**
     * ! VERIFICAR existencia por ID
     * ? SELECT COUNT(1) — más eficiente que cargar la entidad completa.
     *
     * @param id ID a verificar
     * @return true si el producto existe
     */
    public boolean existe(Long id) {
        return repo.existsById(id);
    }

    /**
     * ! BORRAR un producto por ID
     * * DELETE FROM producto WHERE id=?
     * ? El Controller verifica con existe() antes de llamar a este método
     * ? para poder devolver 404 si no existe.
     *
     * @param id ID del producto a eliminar
     */
    public void borrar(Long id) {
        repo.deleteById(id);
    }
}
