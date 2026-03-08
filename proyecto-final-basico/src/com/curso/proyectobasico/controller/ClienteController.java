package com.curso.proyectobasico.controller;

import com.curso.proyectobasico.exception.ValidationException;
import com.curso.proyectobasico.model.Cliente;
import com.curso.proyectobasico.repository.ClienteRepository;
import com.curso.proyectobasico.util.Validator;

import java.util.List;
import java.util.UUID;

/*
 * ==================================================================================
 * // ! CONTROLLER — ClienteController (Capa de Negocio)
 * ==================================================================================
 *
 * // * RESPONSABILIDADES:
 *   - Validar el nombre y el email del cliente.
 *   - Garantizar que no existan dos clientes con el mismo email.
 *   - Delegar la persistencia en ClienteRepository.
 *
 * // ? POR QUÉ EL CONTROLLER VALIDA Y NO EL REPOSITORY:
 *   El repositorio solo sabe de datos (CSV). Las REGLAS DE NEGOCIO
 *   (email único, nombre obligatorio) pertenecen al controller.
 *   Así podemos cambiar el repositorio (CSV → BD) sin tocar las reglas.
 *
 * // ! REGLAS DE NEGOCIO IMPLEMENTADAS:
 *   1. Nombre obligatorio (no vacío ni solo espacios).
 *   2. Email con formato válido.
 *   3. Email único: no pueden existir dos clientes con el mismo email.
 *
 * // TODO (Alumno):
 *   - Añadir metodo actualizar(String id, String nombre, String telefono).
 *   - Añadir buscarPorEmail(String email) para búsquedas desde el menú.
 *   - Añadir validación de longitud mínima del nombre (ej: min 2 caracteres).
 * ==================================================================================
 */
public class ClienteController {

    // ========================================
    // DEPENDENCIAS
    // ========================================

    // * Repositorio de clientes: responsable de leer/escribir el CSV
    private final ClienteRepository repo;

    /*
     * // * CONSTRUCTOR CON INYECCIÓN DE DEPENDENCIAS
     * // ? Al recibir el repo desde fuera, podemos pasar un repo "falso" en tests
     * sin necesidad de leer/escribir ficheros reales.
     */
    public ClienteController(ClienteRepository repo) {
        this.repo = repo;
    }

    // ========================================
    // OPERACIONES CRUD + NEGOCIO
    // ========================================

    /*
     * // ! LISTAR todos los clientes almacenados
     * // * Retorna lista vacía si no hay ninguno (nunca null).
     */
    public List<Cliente> listar() {
        return repo.findAll(); // * Delega directamente; sin lógica de negocio
    }

    /*
     * // ! CREAR un nuevo cliente
     *
     * // * FLUJO:
     * 1. Validar nombre (obligatorio).
     * 2. Validar formato de email.
     * 3. Comprobar que el email no esté ya en uso (unicidad).
     * 4. Crear el cliente con un UUID como ID.
     * 5. Persistir y retornar el cliente creado.
     *
     * // ! IMPORTANTE: El email se normaliza a minúsculas para comparación
     * insensible.
     * // ? Si email es null o vacío, Validator.requireEmail lanza
     * ValidationException.
     *
     * @param nombre Nombre del cliente (obligatorio, no vacío)
     * 
     * @param email Email del cliente (formato válido, único en el sistema)
     * 
     * @param telefono Teléfono del cliente (opcional, puede ser null o vacío)
     * 
     * @return Cliente creado y persistido
     * 
     * @throws ValidationException si nombre/email inválidos o email duplicado
     */
    public Cliente crear(String nombre, String email, String telefono) {
        // ========================================
        // 1. VALIDAR NOMBRE
        // ========================================
        // ! Nombre obligatorio: null y cadena vacía no están permitidos
        Validator.requireNotBlank(nombre, "Nombre");

        // ========================================
        // 2. VALIDAR FORMATO DE EMAIL
        // ========================================
        // * Validator.requireEmail comprueba formato básico (contiene @ y dominio)
        Validator.requireEmail(email);

        // ========================================
        // 3. COMPROBAR UNICIDAD DE EMAIL
        // ========================================
        // ! Regla de negocio clave: no pueden existir dos clientes con el mismo email
        // * findByEmail usa comparación insensible a mayúsculas internamente
        if (repo.findByEmail(email).isPresent()) {
            throw new ValidationException(
                    "Ya existe un cliente con el email '" + email + "'. "
                            + "Cada cliente debe tener un email único.");
        }

        // ========================================
        // 4. CREAR Y PERSISTIR EL CLIENTE
        // ========================================
        String id = UUID.randomUUID().toString(); // * UUID garantiza unicidad global del ID
        Cliente c = new Cliente(
                id,
                nombre.trim(), // * Eliminar espacios en blanco
                email == null ? "" : email.trim().toLowerCase(), // * Normalizar email a minúsculas
                telefono == null ? "" : telefono.trim());

        Cliente guardado = repo.save(c);

        System.out.println("  → Cliente creado: " + guardado.getNombre()
                + " | Email: " + guardado.getEmail()
                + " | ID: " + guardado.getId());

        return guardado;
    }

    /*
     * // ! BORRAR un cliente por su ID
     *
     * // * La eliminación es permanente.
     * // ! ADVERTENCIA: Si el cliente tiene citas asociadas, esas citas quedarán
     * huérfanas (con clienteId que ya no existe). En un sistema real,
     * deberías borrar también las citas del cliente o impedirlo.
     *
     * // TODO: Añadir validación: no borrar cliente si tiene citas PENDIENTES.
     *
     * @param id ID del cliente a eliminar
     * 
     * @return true si se eliminó, false si el cliente no existía
     */
    public boolean borrar(String id) {
        // ! Siempre validar el ID antes de operar
        Validator.requireNotBlank(id, "Id");
        return repo.delete(id);
    }
}
