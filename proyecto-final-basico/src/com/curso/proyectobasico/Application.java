package com.curso.proyectobasico;

import com.curso.proyectobasico.controller.CitaController;
import com.curso.proyectobasico.controller.ClienteController;
import com.curso.proyectobasico.model.Cita;
import com.curso.proyectobasico.model.Cliente;
import com.curso.proyectobasico.repository.CitaRepository;
import com.curso.proyectobasico.repository.ClienteRepository;
import com.curso.proyectobasico.view.ConsoleView;

import java.util.List;

/*
 * ==================================================================================
 * // ! APPLICATION — Agenda Básica de Citas (Proyecto Final Básico)
 * ==================================================================================
 *
 * // * ARQUITECTURA MVC APLICADA:
 *   - Model:      Cliente, Cita, EstadoCita (en paquete model/)
 *   - Repository: ClienteRepository, CitaRepository (persistencia CSV en resources/data/)
 *   - Controller: ClienteController, CitaController (reglas de negocio y validaciones)
 *   - View:       ConsoleView + esta clase Application (entrada/salida por consola)
 *
 * // * ROL DE ESTA CLASE:
 *   Solo navegación y lectura de entradas. Sin reglas de negocio.
 *   Las reglas de negocio viven en los Controllers.
 *   Los datos se almacenan en CSV gestionados por los Repositories.
 *
 * // ? POR QUÉ while(true) en los menús:
 *   Simplifica el bucle: se ejecuta hasta que el usuario elige "0) Volver/Salir".
 *   El return dentro del case "0" sale del bucle.
 *
 * // ! FLUJO PRINCIPAL:
 *   main() → run() → menuClientes() / menuCitas() → acciones CRUD
 *
 * // TODO (Alumno):
 *   - [ ] Añadir confirmación (S/N) antes de borrar un cliente o cita.
 *   - [ ] En listarCitas(), mostrar el nombre del cliente (resolver desde repo).
 *   - [ ] Añadir un resumen al salir: "Total clientes: X | Citas pendientes: Y".
 * ==================================================================================
 */
public class Application {

    // ========================================
    // COMPONENTES (creados aquí, inyectados en controllers)
    // ========================================

    // * Vista de consola: maneja entrada/salida de texto
    private final ConsoleView view = new ConsoleView();

    // * Repositorios: acceso a los ficheros CSV
    private final ClienteRepository clienteRepo = new ClienteRepository();
    private final CitaRepository citaRepo = new CitaRepository();

    // * Controladores: reciben los repositorios por constructor (Dependency
    // Injection manual)
    // ? En Spring Boot esto lo haría el framework automáticamente con @Autowired
    private final ClienteController clienteCtl = new ClienteController(clienteRepo);
    private final CitaController citaCtl = new CitaController(citaRepo, clienteRepo);

    // ========================================
    // PUNTO DE ENTRADA
    // ========================================

    /*
     * // ! MÉTODO MAIN - Punto de entrada de la aplicación
     * // * Crea la instancia de Application y arranca el bucle de menús.
     */
    public static void main(String[] args) {
        new Application().run();
    }

    // ========================================
    // MENÚ PRINCIPAL
    // ========================================

    /*
     * // * BUCLE PRINCIPAL — menú raíz
     * // ? Se ejecuta indefinidamente hasta que el usuario elige "0) Salir".
     */
    public void run() {
        while (true) {
            view.title("=== Agenda Basica de Citas ===  Menu principal");
            view.line("1) Clientes");
            view.line("2) Citas");
            view.line("0) Salir");
            String op = view.prompt("Opcion");
            try {
                switch (op) {
                    case "1" -> menuClientes();
                    case "2" -> menuCitas();
                    case "0" -> {
                        mostrarResumen(); // * Muestra estadísticas antes de salir
                        System.out.println("Hasta luego!");
                        return;
                    }
                    default -> view.line("Opcion no valida. Elige 0, 1 o 2.");
                }
            } catch (Exception e) {
                // ! Capturamos cualquier excepción para que la app no se cierre abruptamente
                view.line("[ERROR] " + e.getMessage());
            }
        }
    }

    // ========================================
    // SUBMENÚ: CLIENTES
    // ========================================

    /*
     * // * SUBMENÚ DE CLIENTES — listar / crear / borrar
     * // ? "0) Volver" llama a return para salir de este submenú y volver al menú
     * principal.
     */
    private void menuClientes() {
        while (true) {
            view.title("--- Gestion de Clientes ---");
            view.line("1) Listar todos");
            view.line("2) Crear nuevo");
            view.line("3) Borrar por ID");
            view.line("0) Volver al menu principal");
            String op = view.prompt("Opcion");
            if (op.equals("0"))
                return; // * Salir del submenú

            try {
                switch (op) {
                    case "1" -> listarClientes();
                    case "2" -> crearCliente();
                    case "3" -> borrarCliente();
                    default -> view.line("Opcion no valida.");
                }
            } catch (Exception e) {
                view.line("[ERROR] " + e.getMessage());
            }
            view.pause(); // * Espera ENTER antes de mostrar el menú otra vez
        }
    }

    /*
     * // * LISTAR CLIENTES
     * // ? Muestra: ID | Nombre | Email | Telefono
     * // ! Si no hay clientes, informa al usuario.
     */
    private void listarClientes() {
        List<Cliente> clientes = clienteCtl.listar();
        view.line("--- Clientes registrados ---");
        if (clientes.isEmpty()) {
            view.line("  (No hay clientes. Crea uno con la opcion 2)");
            return;
        }
        // * toString() de Cliente formatea: [id] Nombre | email | tel
        for (Cliente c : clientes) {
            view.line(c.toString());
        }
        view.line("  Total: " + clientes.size() + " cliente(s)");
    }

    /*
     * // * CREAR CLIENTE
     * // ! El email es obligatorio y debe ser único.
     * // ? El teléfono es opcional: si el usuario pulsa ENTER vacío, se guarda como
     * cadena vacía.
     */
    private void crearCliente() {
        String nombre = view.prompt("Nombre del cliente");
        String email = view.prompt("Email (obligatorio, debe ser unico)");
        String telefono = view.prompt("Telefono (opcional, ENTER para omitir)");
        Cliente c = clienteCtl.crear(nombre, email, telefono);
        view.line("✔ Cliente creado con ID: " + c.getId());
    }

    /*
     * // * BORRAR CLIENTE
     * // ! ADVERTENCIA: Las citas del cliente quedarán huérfanas si se borran sin
     * eliminarlas antes.
     */
    private void borrarCliente() {
        view.line("  IDs disponibles: copia el ID del listado (opcion 1).");
        String id = view.prompt("ID del cliente a borrar");
        boolean ok = clienteCtl.borrar(id);
        view.line(ok ? "✔ Cliente borrado correctamente." : "⚠ Cliente no encontrado con ese ID.");
    }

    // ========================================
    // SUBMENÚ: CITAS
    // ========================================

    /*
     * // * SUBMENÚ DE CITAS — listar / crear / marcar / borrar
     */
    private void menuCitas() {
        while (true) {
            view.title("--- Gestion de Citas ---");
            view.line("1) Listar todas");
            view.line("2) Crear nueva cita");
            view.line("3) Marcar como REALIZADA");
            view.line("4) Borrar cita");
            view.line("0) Volver al menu principal");
            String op = view.prompt("Opcion");
            if (op.equals("0"))
                return;

            try {
                switch (op) {
                    case "1" -> listarCitas();
                    case "2" -> crearCita();
                    case "3" -> marcarCitaRealizada();
                    case "4" -> borrarCita();
                    default -> view.line("Opcion no valida.");
                }
            } catch (Exception e) {
                view.line("[ERROR] " + e.getMessage());
            }
            view.pause();
        }
    }

    /*
     * // * LISTAR CITAS con nombre del cliente
     * // ? Resolvemos el nombre del cliente desde el repo para que el listado sea
     * legible.
     * Sin esto, solo veríamos el clienteId (UUID poco amigable).
     */
    private void listarCitas() {
        List<Cita> citas = citaCtl.listar();
        view.line("--- Citas registradas ---");
        if (citas.isEmpty()) {
            view.line("  (No hay citas. Crea una con la opcion 2)");
            return;
        }
        for (Cita c : citas) {
            // * Resolver nombre del cliente para mostrarlo junto a la cita
            // ? Si el cliente fue borrado, mostramos "(cliente eliminado)" como aviso
            String nombreCliente = clienteRepo.findById(c.getClienteId())
                    .map(Cliente::getNombre)
                    .orElse("(cliente eliminado)");

            // * Formato legible: Estado | Fecha | Nombre del cliente | Descripcion
            view.line(String.format(
                    "[%s] %s | Cliente: %-20s | %s",
                    c.getEstado(),
                    c.getFecha(),
                    nombreCliente,
                    c.getDescripcion()));
        }
        view.line("  Total: " + citas.size() + " cita(s)");
    }

    /*
     * // * CREAR CITA
     * // ! El cliente debe existir previamente. Usa el ID mostrado en
     * "Listar Clientes".
     * // ? La fecha debe ser hoy o en el futuro, en formato yyyy-MM-dd.
     */
    private void crearCita() {
        view.line("  Necesitas el ID del cliente. Ve a Clientes → Listar si no lo tienes.");
        String clienteId = view.prompt("ID del cliente");
        String fecha = view.prompt("Fecha de la cita (yyyy-MM-dd, ej: 2026-03-15)");
        String descripcion = view.prompt("Descripcion breve (opcional)");
        Cita cita = citaCtl.crear(clienteId, fecha, descripcion);
        view.line("✔ Cita creada con ID: " + cita.getId());
    }

    /*
     * // * MARCAR CITA COMO REALIZADA
     * // ? El ID de la cita se muestra en "Listar Citas".
     */
    private void marcarCitaRealizada() {
        String citaId = view.prompt("ID de la cita a marcar como REALIZADA");
        boolean ok = citaCtl.marcarRealizada(citaId);
        view.line(ok ? "✔ Cita marcada como REALIZADA." : "⚠ Cita no encontrada con ese ID.");
    }

    /*
     * // * BORRAR CITA
     * // ! La eliminación es permanente (no hay papelera).
     */
    private void borrarCita() {
        String citaId = view.prompt("ID de la cita a borrar");
        boolean ok = citaCtl.borrar(citaId);
        view.line(ok ? "✔ Cita borrada correctamente." : "⚠ Cita no encontrada con ese ID.");
    }

    // ========================================
    // UTILIDADES
    // ========================================

    /*
     * // * RESUMEN AL SALIR
     * // ? Muestra estadísticas rápidas: total de clientes y citas pendientes.
     * // ! Si los repositorios no pueden leer los CSV, puede lanzar excepción
     * (atrapada en run()).
     */
    private void mostrarResumen() {
        try {
            long totalClientes = clienteCtl.listar().size();
            long citasPendientes = citaCtl.listar().stream()
                    .filter(c -> "PENDIENTE".equals(c.getEstado().name()))
                    .count();
            view.line("--- Resumen ---");
            view.line("  Total clientes registrados : " + totalClientes);
            view.line("  Citas pendientes           : " + citasPendientes);
        } catch (Exception ignored) {
            // * Si falla el resumen, no interrumpimos el cierre de la app
        }
    }
}
