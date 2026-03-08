package com.curso.ut20.controller;

import com.curso.ut20.model.Producto;
import com.curso.ut20.service.ProductoService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.List;

/**
 * // ! CONTROLADOR REST — ProductoController
 * ? Gestiona las peticiones HTTP para el recurso Producto (CRUD completo).
 *
 * * CAPAS QUE INTERVIENEN EN CADA PETICIÓN:
 * Cliente HTTP → ProductoController → ProductoService → ProductoRepository → H2
 *
 * ! RESPONSABILIDADES DEL CONTROLLER:
 * ✓ Mapear URLs: @GetMapping, @PostMapping, @PutMapping, @DeleteMapping
 * ✓ Recibir JSON: @RequestBody (deserialización automática)
 * ✓ Enviar JSON: automático gracias a @RestController + Jackson
 * ✓ Validar: @Valid (delegando en Bean Validation)
 * ✓ Códigos HTTP correctos: 200, 201, 204, 404
 * ✗ NO incluye lógica de negocio → eso va en ProductoService
 *
 * * ENDPOINTS:
 * GET /api/productos → 200 OK (lista, puede estar vacía)
 * GET /api/productos/{id} → 200 OK / 404 Not Found
 * POST /api/productos → 201 Created (con header Location)
 * PUT /api/productos/{id} → 200 OK / 404 Not Found
 * DELETE /api/productos/{id} → 204 No Content / 404 Not Found
 *
 * TODO:
 * - GET /api/productos?precioMax=100 → filtrar productos baratos
 * - GET /api/productos?nombre=laptop → buscar por nombre (case-insensitive)
 */
@RestController // * Combina @Controller + @ResponseBody (respuestas JSON automáticas)
@RequestMapping("/api/productos") // * Prefijo URI para todos los endpoints
public class ProductoController {

    // ========================================
    // INYECCIÓN DE DEPENDENCIAS
    // ========================================

    /**
     * ! SERVICE de Producto inyectado por constructor
     * ? Seguimos la arquitectura de 3 capas: Controller → Service → Repository.
     * * Cambiamos la dependencia del Repository por el Service.
     */
    private final ProductoService service;

    public ProductoController(ProductoService service) {
        this.service = service;
    }

    // ========================================
    // ENDPOINTS CRUD
    // ========================================

    /**
     * ! GET /api/productos — LISTAR TODOS
     * * HTTP 200 OK siempre (lista vacía [] si no hay productos)
     *
     * ? Ejemplo de respuesta:
     * [
     * { "id": 1, "nombre": "Laptop", "precio": 999.99 },
     * { "id": 2, "nombre": "Mouse Inalámbrico", "precio": 25.50 }
     * ]
     */
    @GetMapping
    public List<Producto> listar() {
        return service.listar(); // * Delega en el Service
    }

    /**
     * ! GET /api/productos/{id} — OBTENER UNO POR ID
     * * HTTP 200 OK → encontrado | HTTP 404 Not Found → no existe
     *
     * ? El @PathVariable extrae el {id} de la URL.
     * Ejemplo: GET /api/productos/3 → id = 3L
     */
    @GetMapping("/{id}")
    public ResponseEntity<Producto> uno(@PathVariable Long id) {
        return service.buscar(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * ! POST /api/productos — CREAR NUEVO PRODUCTO
     * * HTTP 201 Created → creado (+ header Location con la URL del nuevo recurso)
     * * HTTP 400 Bad Request → si @Valid detecta errores de validación
     *
     * ? Las validaciones de la entidad Producto:
     * - nombre: @NotBlank → no puede ser vacío
     * - precio: @Min(0) → no puede ser negativo
     * Si fallan → GlobalExceptionHandler devuelve 400 con mapa de errores
     *
     * ? Ejemplo de petición:
     * POST /api/productos
     * { "nombre": "Teclado Mecánico", "precio": 89.99 }
     *
     * ? Ejemplo de respuesta:
     * HTTP 201 Created
     * Location: /api/productos/5
     * { "id": 5, "nombre": "Teclado Mecánico", "precio": 89.99 }
     */
    @PostMapping
    public ResponseEntity<Producto> crear(@Valid @RequestBody Producto p) {
        Producto guardado = service.crear(p);
        return ResponseEntity
                .created(URI.create("/api/productos/" + guardado.getId()))
                .body(guardado);
    }

    /**
     * ! PUT /api/productos/{id} — ACTUALIZAR PRODUCTO EXISTENTE
     * * HTTP 200 OK → actualizado | HTTP 404 → no existe
     *
     * ! Importante: PUT reemplaza el recurso completo.
     * Si quieres actualizar solo el precio, aun así debes enviar el nombre.
     * Para actualización parcial usa PATCH (no implementado aquí — TODO).
     *
     * ? Ejemplo:
     * PUT /api/productos/3
     * { "nombre": "Laptop Gaming", "precio": 1299.99 }
     */
    @PutMapping("/{id}")
    public ResponseEntity<Producto> actualizar(@PathVariable Long id,
            @Valid @RequestBody Producto datos) {
        return service.actualizar(id, datos)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * ! DELETE /api/productos/{id} — ELIMINAR PRODUCTO
     * * HTTP 204 No Content → eliminado (sin body en la respuesta)
     * * HTTP 404 Not Found → no existe
     *
     * ? ¿Por qué ResponseEntity<Void>?
     * Void indica que el body de la respuesta está vacío.
     * 204 No Content = "acción completada, sin nada que devolver".
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> borrar(@PathVariable Long id) {
        if (!service.existe(id)) {
            return ResponseEntity.notFound().build(); // * 404 si no existe
        }
        service.borrar(id);
        return ResponseEntity.noContent().build(); // * 204 eliminación exitosa
    }
}
