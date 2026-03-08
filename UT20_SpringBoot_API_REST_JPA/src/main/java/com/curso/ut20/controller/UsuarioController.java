package com.curso.ut20.controller;

import com.curso.ut20.model.Usuario;
import com.curso.ut20.service.UsuarioService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.List;

/**
 * // ! CONTROLADOR REST — UsuarioController
 * ? Gestiona las peticiones HTTP para el recurso Usuario (CRUD completo).
 *
 * * CAPAS QUE INTERVIENEN EN CADA PETICIÓN:
 * Cliente HTTP
 * │ (JSON)
 * ▼
 * UsuarioController ← Esta clase: solo HTTP (recibe, responde, delega)
 * │ (objetos Java)
 * ▼
 * UsuarioService ← Lógica de negocio y validaciones adicionales
 * │ (objetos Java)
 * ▼
 * UsuarioRepository ← Acceso a BD (SQL generado por Spring Data JPA)
 * │ (SQL)
 * ▼
 * H2 Database ← Base de datos en memoria
 *
 * ! RESPONSABILIDADES DEL CONTROLLER:
 * ✓ Mapear URLs a métodos Java (@GetMapping, @PostMapping, etc.)
 * ✓ Deserializar JSON a objetos Java (@RequestBody)
 * ✓ Serializar objetos Java a JSON (automático con @RestController)
 * ✓ Activar validaciones con @Valid
 * ✓ Devolver el código HTTP correcto (200, 201, 204, 404)
 * ✗ NO contiene lógica de negocio → eso es responsabilidad del Service
 *
 * * ENDPOINTS DISPONIBLES:
 * GET /api/usuarios → Listar todos los usuarios (200 OK)
 * GET /api/usuarios/{id} → Obtener uno por ID (200 OK / 404 Not Found)
 * POST /api/usuarios → Crear nuevo usuario (201 Created)
 * PUT /api/usuarios/{id} → Actualizar usuario (200 OK / 404 Not Found)
 * DELETE /api/usuarios/{id} → Eliminar usuario (204 No Content / 404 Not Found)
 *
 * TODO:
 * - Añadir paginación: @GetMapping con @RequestParam int page, int size
 * - Añadir búsqueda: GET /api/usuarios?nombre=Juan
 */
@RestController // * Combina @Controller + @ResponseBody → todas las respuestas son JSON
@RequestMapping("/api/usuarios") // * Prefijo para todos los endpoints de este controller
public class UsuarioController {

    // ========================================
    // INYECCIÓN DE DEPENDENCIAS
    // ========================================

    /**
     * ! SERVICE inyectado vía constructor
     * ? Ahora dependemos del SERVICE, no del REPOSITORY directamente.
     * * Esto respeta la arquitectura de 3 capas: Controller → Service → Repository.
     * * final: la referencia es inmutable tras la inyección.
     */
    private final UsuarioService service;

    /**
     * ? Constructor — Spring detecta el único constructor e inyecta el Service
     * automáticamente.
     * * No hace falta @Autowired (convención desde Spring 4.3+).
     *
     * @param service Servicio de negocio para la entidad Usuario
     */
    public UsuarioController(UsuarioService service) {
        this.service = service;
    }

    // ========================================
    // ENDPOINTS CRUD
    // ========================================

    /**
     * ! GET /api/usuarios — LISTAR TODOS LOS USUARIOS
     * ? Retorna todos los usuarios de la BD en formato JSON.
     *
     * * HTTP 200 OK → siempre (puede ser lista vacía [])
     *
     * ? Ejemplo de respuesta:
     * [
     * { "id": 1, "nombre": "Juan Pérez", "edad": 25 },
     * { "id": 2, "nombre": "María García", "edad": 30 }
     * ]
     *
     * @return Lista de usuarios (puede estar vacía)
     */
    @GetMapping // * Mapea GET /api/usuarios
    public List<Usuario> listar() {
        return service.listar(); // * Delega en el Service (que delega en el Repository)
    }

    /**
     * ! GET /api/usuarios/{id} — OBTENER UN USUARIO POR ID
     * ? Busca un usuario específico. Si no existe, devuelve 404.
     *
     * * HTTP 200 OK → usuario encontrado
     * * HTTP 404 Not Found → usuario no existe
     *
     * ? Encadenamiento funcional con Optional:
     * service.buscar(id) → Optional<Usuario>
     * .map(ResponseEntity::ok) → Optional<ResponseEntity<200, usuario>>
     * .orElse(404) → ResponseEntity<404>
     *
     * @param id ID del usuario (extraído de la URL, ej: /api/usuarios/5)
     * @return 200 con el usuario, o 404 si no existe
     */
    @GetMapping("/{id}") // * {id} es una variable de ruta (PathVariable)
    public ResponseEntity<Usuario> uno(@PathVariable Long id) {
        // * Optional evita NullPointerException — patrón funcional en lugar de if/null
        return service.buscar(id)
                .map(ResponseEntity::ok) // * Si existe → 200 OK con el usuario
                .orElse(ResponseEntity.notFound().build()); // * Si no → 404 Not Found (sin body)
    }

    /**
     * ! POST /api/usuarios — CREAR NUEVO USUARIO
     * ? Recibe JSON, lo valida, lo persiste y retorna 201 Created.
     *
     * * @Valid activa las validaciones de la entidad Usuario:
     * - @NotBlank en nombre → 400 si está vacío
     * - @Min(0) en edad → 400 si es negativa
     * Si falla → GlobalExceptionHandler intercepta y retorna 400 con detalles del
     * error.
     *
     * * El header "Location" indica la URL del nuevo recurso:
     * Location: /api/usuarios/7
     * (Permite al cliente hacer GET a esa URL para obtener el recurso creado)
     *
     * ? Ejemplo de petición:
     * POST /api/usuarios
     * Content-Type: application/json
     * { "nombre": "Carlos López", "edad": 28 }
     *
     * ? Ejemplo de respuesta:
     * HTTP 201 Created
     * Location: /api/usuarios/7
     * { "id": 7, "nombre": "Carlos López", "edad": 28 }
     *
     * @param u Usuario recibido del body JSON (ya validado)
     * @return 201 Created con el usuario y header Location
     */
    @PostMapping // * Mapea POST /api/usuarios
    public ResponseEntity<Usuario> crear(@Valid @RequestBody Usuario u) {
        // * @RequestBody: Spring deserializa JSON → objeto Usuario
        // * @Valid: activa las validaciones de Bean Validation antes de entrar al
        // método
        Usuario guardado = service.crear(u);

        // * 201 Created con header Location: /api/usuarios/{id}
        return ResponseEntity
                .created(URI.create("/api/usuarios/" + guardado.getId()))
                .body(guardado); // * Incluir el usuario creado (con ID) en el body
    }

    /**
     * ! PUT /api/usuarios/{id} — ACTUALIZAR USUARIO EXISTENTE
     * ? Reemplaza los datos del usuario indicado por ID.
     *
     * * HTTP 200 OK → usuario actualizado (body con los nuevos datos)
     * * HTTP 404 Not Found → usuario no existe (no se actualiza nada)
     *
     * ! Diferencia PUT vs PATCH:
     * PUT → Reemplaza el recurso completo (todos los campos)
     * PATCH → Solo actualiza los campos enviados (parcial)
     * Aquí implementamos PUT: se deben enviar todos los campos.
     *
     * @param id    ID del usuario a actualizar (de la URL)
     * @param datos Nuevos datos del usuario (del body JSON, validados)
     * @return 200 con el usuario actualizado, o 404 si no existe
     */
    @PutMapping("/{id}") // * Mapea PUT /api/usuarios/{id}
    public ResponseEntity<Usuario> actualizar(@PathVariable Long id,
            @Valid @RequestBody Usuario datos) {
        // * El Service se encarga de buscar, modificar y guardar.
        // * Si no existe, map() no se ejecuta y .orElse() devuelve 404.
        return service.actualizar(id, datos)
                .map(ResponseEntity::ok) // * 200 OK con el usuario actualizado
                .orElse(ResponseEntity.notFound().build()); // * 404 Not Found
    }

    /**
     * ! DELETE /api/usuarios/{id} — ELIMINAR USUARIO
     * ? Elimina el usuario si existe. Retorna 204 (sin body) o 404.
     *
     * * HTTP 204 No Content → eliminado con éxito (no hay body en la respuesta)
     * * HTTP 404 Not Found → usuario no existe
     *
     * ! ¿Por qué 204 y no 200?
     * 204 = "procesado correctamente, sin contenido que devolver"
     * 200 = "procesado correctamente, con contenido en el body"
     * Un DELETE exitoso no devuelve el recurso borrado → 204 es el estándar REST.
     *
     * @param id ID del usuario a eliminar
     * @return 204 si se eliminó, 404 si no existía
     */
    @DeleteMapping("/{id}") // * Mapea DELETE /api/usuarios/{id}
    public ResponseEntity<Void> borrar(@PathVariable Long id) {
        // * Verificar existencia primero para distinguir 204 de 404
        if (!service.existe(id)) {
            return ResponseEntity.notFound().build(); // * 404 Not Found
        }
        service.borrar(id); // * Eliminar — delega en el Service
        return ResponseEntity.noContent().build(); // * 204 No Content (eliminación exitosa)
    }
}
