package com.curso.proyectobasico.controller;

import com.curso.proyectobasico.exception.ValidationException;
import com.curso.proyectobasico.model.Cita;
import com.curso.proyectobasico.model.Cliente;
import com.curso.proyectobasico.model.EstadoCita;
import com.curso.proyectobasico.repository.CitaRepository;
import com.curso.proyectobasico.repository.ClienteRepository;
import com.curso.proyectobasico.util.DateUtils;
import com.curso.proyectobasico.util.Validator;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

/*
 * ==================================================================================
 * // ! CONTROLLER — CitaController (Capa de Negocio)
 * ==================================================================================
 *
 * // * RESPONSABILIDADES:
 *   - Verificar que el cliente existe antes de crear una cita.
 *   - Validar que la fecha no sea en el pasado.
 *   - Gestionar el cambio de estado de las citas (PENDIENTE → REALIZADA).
 *   - Delegar la persistencia en los repositorios.
 *
 * // ? POR QUÉ DOS REPOSITORIOS:
 *   CitaController necesita tanto CitaRepository (para CRUD de citas)
 *   como ClienteRepository (para verificar que el clienteId existe).
 *   Esta es una regla de negocio: no se puede crear una cita sin cliente.
 *
 * // ! REGLAS DE NEGOCIO IMPLEMENTADAS:
 *   1. clienteId obligatorio y debe existir.
 *   2. fecha obligatoria, formato yyyy-MM-dd, no puede ser en el pasado.
 *   3. Una cita solo puede marcarse REALIZADA si existe (no si ya fue borrada).
 *
 * // TODO (Alumno):
 *   - Añadir metodo cancelar(String citaId) → estado CANCELADA.
 *   - Añadir listadoPorCliente(String clienteId) → filtrar citas de un cliente.
 *   - Añadir listadoPorFecha(LocalDate fecha) → citas de un día concreto.
 * ==================================================================================
 */
public class CitaController {

    // ========================================
    // DEPENDENCIAS (inyectadas por constructor)
    // ========================================

    // * Repositorio de citas: operaciones CRUD sobre Cita
    private final CitaRepository citaRepo;

    // * Repositorio de clientes: solo para verificar existencia del clienteId
    private final ClienteRepository clienteRepo;

    /*
     * // * CONSTRUCTOR CON INYECCIÓN DE DEPENDENCIAS
     * // ? Recibimos las implementaciones desde fuera (Application.java).
     *   Esto facilita el testing: podemos pasar repos "falsos" en los tests.
     */
    public CitaController(CitaRepository citaRepo, ClienteRepository clienteRepo) {
        this.citaRepo = citaRepo;
        this.clienteRepo = clienteRepo;
    }

    // ========================================
    // OPERACIONES CRUD + NEGOCIO
    // ========================================

    /*
     * // ! LISTAR todas las citas almacenadas
     * // * Retorna lista vacía si no hay ninguna (nunca null).
     * // ? Útil para mostrar todas las citas en el menú principal.
     */
    public List<Cita> listar() {
        return citaRepo.findAll(); // * Delega al repo; no hay lógica de negocio aquí
    }

    /*
     * // ! CREAR una nueva cita (PENDIENTE)
     *
     * // * FLUJO:
     *   1. Validar que clienteId y fecha no estén vacíos.
     *   2. Verificar que el cliente existe (lanza ValidationException si no).
     *   3. Parsear la fecha (lanza ValidationException si formato incorrecto).
     *   4. Verificar que la fecha no es pasada.
     *   5. Crear la cita con estado PENDIENTE y un UUID como identificador.
     *   6. Persistir y retornar la cita creada.
     *
     * // ! REGLA: No se puede crear una cita con fecha en el pasado.
     * // ? Si fecha es null o vacía, Validator.requireNotBlank lanzará excepción descriptiva.
     *
     * @param clienteId   ID del cliente (debe existir en ClienteRepository)
     * @param fechaStr    Fecha en formato yyyy-MM-dd
     * @param descripcion Texto libre opcional (null se convierte en cadena vacía)
     * @return Cita creada con estado PENDIENTE
     * @throws ValidationException si clienteId/fecha inválidos o cliente no existe
     */
    public Cita crear(String clienteId, String fechaStr, String descripcion) {
        // ========================================
        // 1. VALIDAR DATOS OBLIGATORIOS
        // ========================================
        // ! Si llegamos aquí con campos vacíos es un error de uso del controlador
        Validator.requireNotBlank(clienteId, "ClienteId");
        Validator.requireNotBlank(fechaStr, "Fecha");

        // ========================================
        // 2. VERIFICAR QUE EL CLIENTE EXISTE
        // ========================================
        // * Buscamos el cliente para mostrar su nombre en el mensaje de error
        // ! Regla de negocio: no crear cita sin cliente válido
        Cliente cliente = clienteRepo.findById(clienteId)
                .orElseThrow(() -> new ValidationException(
                        "Cliente no encontrado con id: " + clienteId
                        + ". Crea primero el cliente desde el menú de Clientes."));

        // ========================================
        // 3. PARSEAR Y VALIDAR FECHA
        // ========================================
        // * DateUtils.parse() lanza ValidationException si el formato es incorrecto
        LocalDate fecha = DateUtils.parse(fechaStr);

        // ! Regla: la fecha de la cita no puede estar en el pasado
        if (fecha.isBefore(LocalDate.now())) {
            throw new ValidationException(
                    "La fecha " + fechaStr + " no puede estar en el pasado. "
                    + "Usa una fecha de hoy o futura.");
        }

        // ========================================
        // 4. CREAR Y PERSISTIR LA CITA
        // ========================================
        String id = UUID.randomUUID().toString(); // * ID único generado automáticamente
        Cita cita = new Cita(
                id,
                clienteId,
                fecha,
                EstadoCita.PENDIENTE,                        // * Estado inicial siempre PENDIENTE
                descripcion == null ? "" : descripcion.trim()
        );

        // ? Nota: guardamos clienteId (no el objeto Cliente) para mantener el CSV simple
        Cita guardada = citaRepo.save(cita);

        System.out.println("  → Cita creada para el cliente: " + cliente.getNombre()
                + " | Fecha: " + fechaStr
                + " | Estado: PENDIENTE");

        return guardada;
    }

    /*
     * // ! MARCAR una cita como REALIZADA
     *
     * // * FLUJO:
     *   1. Buscar la cita por ID (Optional.map para evitar null).
     *   2. Si existe → cambiar estado a REALIZADA y persistir.
     *   3. Si no existe → retornar false.
     *
     * // ? Por qué usamos Optional.map:
     *   Evita el clásico null-check. El código es más expresivo y funcional.
     *
     * @param citaId ID de la cita a marcar como realizada
     * @return true si se marcó, false si la cita no existe
     */
    public boolean marcarRealizada(String citaId) {
        // ! Validamos antes de buscar: citaId vacío es un error de usuario
        Validator.requireNotBlank(citaId, "Id cita");

        // * Programación funcional con Optional: si existe → marcar, si no → false
        return citaRepo.findById(citaId)
                .map(cita -> {
                    cita.setEstado(EstadoCita.REALIZADA); // * Cambiar estado
                    citaRepo.update(cita);                // * Persistir cambio en CSV
                    System.out.println("  → Cita marcada como REALIZADA");
                    return true;
                })
                .orElse(false); // * Cita no encontrada
    }

    /*
     * // ! BORRAR una cita por su ID
     *
     * // * La eliminación es permanente (no hay papelera ni soft-delete).
     * // ? Considera añadir confirmación en la capa de vista antes de llamar a este método.
     *
     * // TODO: Implementar "soft delete" → cambiar estado a CANCELADA en lugar de borrar.
     *
     * @param citaId ID de la cita a eliminar
     * @return true si se eliminó, false si la cita no existía
     */
    public boolean borrar(String citaId) {
        // ! Validar siempre los IDs antes de operar
        Validator.requireNotBlank(citaId, "Id cita");
        return citaRepo.delete(citaId);
    }
}
