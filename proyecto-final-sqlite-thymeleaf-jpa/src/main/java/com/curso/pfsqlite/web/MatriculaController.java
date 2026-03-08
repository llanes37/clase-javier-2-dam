package com.curso.pfsqlite.web;

import com.curso.pfsqlite.service.AlumnoService;
import com.curso.pfsqlite.service.BusinessException;
import com.curso.pfsqlite.service.CursoService;
import com.curso.pfsqlite.service.MatriculaService;
import com.curso.pfsqlite.web.form.MatriculaForm;
import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: MatriculaController  |  CAPA: Web (Controlador MVC)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: Responsabilidad del controlador en arquitectura en capas
// ? El controlador SOLO gestiona HTTP: recibe → valida formulario → delega → responde.
// ? NUNCA contiene reglas de negocio. Eso es responsabilidad del Service.

// * 🧠 TEORÍA: ¿Por qué este controlador necesita TRES servicios?
// ? El formulario de nueva matrícula necesita mostrar la lista de alumnos (AlumnoService)
// ? y la lista de cursos (CursoService) para que el usuario seleccione uno de cada uno.
// ? Además, la lógica de crear/anular/eliminar la delega en MatriculaService.

// * 🧠 TEORÍA: @RequestMapping en la clase = prefijo común para todos los endpoints
// ? GET  /matriculas               → listar()
// ? GET  /matriculas/nueva         → nueva()
// ? POST /matriculas               → crear()
// ? POST /matriculas/{id}/anular   → anular()
// ? POST /matriculas/{id}/eliminar → eliminar()

@Controller
@RequestMapping("/matriculas")
public class MatriculaController {

    // * Los tres servicios que necesita este controlador para funcionar
    private final MatriculaService matriculaService;
    private final AlumnoService alumnoService;
    private final CursoService cursoService;

    // * 🧠 TEORÍA: Inyección por constructor (patrón recomendado frente a
    // @Autowired en campo)
    // ? 1) Permite usar `final` → los servicios no pueden reasignarse
    // accidentalmente.
    // ? 2) Facilita tests unitarios: se pasan mocks directamente sin necesitar
    // Spring.
    public MatriculaController(
            MatriculaService matriculaService,
            AlumnoService alumnoService,
            CursoService cursoService) {
        this.matriculaService = matriculaService;
        this.alumnoService = alumnoService;
        this.cursoService = cursoService;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GET /matriculas → Muestra la lista de todas las matrículas
    // ─────────────────────────────────────────────────────────────────────────

    // ? El servicio devuelve las matrículas con alumno y curso ya cargados
    // ? gracias al @EntityGraph del repositorio (evita el problema N+1 de consultas
    // SQL).
    @GetMapping
    public String listar(Model model) {
        // * model.addAttribute("matriculas", ...) → Thymeleaf accede como ${matriculas}
        // en la vista
        model.addAttribute("matriculas", matriculaService.listar());
        return "matriculas/lista";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GET /matriculas/nueva → Muestra el formulario con combos precargados
    // ─────────────────────────────────────────────────────────────────────────

    // ? Pasamos un MatriculaForm vacío para que Thymeleaf lo vincule con
    // th:object="${form}"
    @GetMapping("/nueva")
    public String nueva(Model model) {
        model.addAttribute("form", new MatriculaForm());
        // * Cargamos los combos de alumnos y cursos para rellenar los <select> del
        // formulario
        cargarListas(model);
        return "matriculas/nueva";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 POST /matriculas → Procesa el formulario de alta de matrícula
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: Flujo completo del POST con doble validación
    // ? Paso 1: @Valid activa Bean Validation sobre MatriculaForm (@NotNull en
    // alumnoId y cursoId).
    // ? Paso 2: Si hay errores de formulario (BindingResult) → volvemos al
    // formulario con errores.
    // ? Paso 3: El service valida reglas de negocio (fecha en rango, duplicado
    // ACTIVA).
    // ? Paso 4: Si todo OK → redirect con mensaje flash de éxito.

    // * 🧠 TEORÍA: ¿Qué es un atributo flash de redirect?
    // ? Es un atributo que sobrevive UNA sola redirección y desaparece
    // automáticamente.
    // ? Perfecto para mensajes de "ok" o "error" tras un redirect.
    // ? Si el usuario recarga la página, el mensaje NO vuelve a aparecer (evita
    // doble POST).
    @PostMapping
    public String crear(
            @Valid @ModelAttribute("form") MatriculaForm form,
            BindingResult bindingResult,
            Model model,
            RedirectAttributes redirectAttributes) {

        if (bindingResult.hasErrors()) {
            // ! ⚠️ IMPORTANTE: hay que recargar los combos porque el modelo se pierde al
            // re-renderizar
            cargarListas(model);
            return "matriculas/nueva";
        }

        try {
            matriculaService.crear(form);
            redirectAttributes.addFlashAttribute("ok", "Matrícula creada correctamente");
            return "redirect:/matriculas";
        } catch (BusinessException ex) {
            // ! Error de regla de negocio: fecha fuera de rango o duplicado ACTIVA
            cargarListas(model);
            model.addAttribute("error", ex.getMessage());
            return "matriculas/nueva";
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 POST /matriculas/{id}/anular → Borrado lógico (cambia estado a ANULADA)
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: Borrado lógico vs. borrado físico
    // ? Anular conserva el registro en BD con estado ANULADA → el historial queda
    // intacto.
    // ? Eliminar borra el registro completamente → no hay vuelta atrás.
    // ? En sistemas reales, el historial tiene valor (auditoría, estadísticas,
    // reclamaciones).
    @PostMapping("/{id}/anular")
    public String anular(@PathVariable Long id, RedirectAttributes redirectAttributes) {
        try {
            matriculaService.anular(id);
            redirectAttributes.addFlashAttribute("ok", "Matrícula anulada correctamente");
        } catch (BusinessException ex) {
            redirectAttributes.addFlashAttribute("error", ex.getMessage());
        }
        return "redirect:/matriculas";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 POST /matriculas/{id}/eliminar → Borrado físico (DELETE en BD)
    // ─────────────────────────────────────────────────────────────────────────

    // ? Se usa POST (no DELETE) porque los formularios HTML estándar solo soportan
    // GET y POST.
    @PostMapping("/{id}/eliminar")
    public String eliminar(@PathVariable Long id, RedirectAttributes redirectAttributes) {
        try {
            matriculaService.borrar(id);
            redirectAttributes.addFlashAttribute("ok", "Matrícula eliminada correctamente");
        } catch (BusinessException ex) {
            redirectAttributes.addFlashAttribute("error", ex.getMessage());
        }
        return "redirect:/matriculas";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 MÉTODO AUXILIAR PRIVADO: cargarListas()
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: Principio DRY → Don't Repeat Yourself
    // ? Este método centraliza la carga de alumnos y cursos para los combos del
    // formulario.
    // ? Sin él, tendríamos el mismo código repetido en 3 sitios distintos:
    // ? - en nueva() al mostrar el formulario por primera vez
    // ? - en crear() al volver por error de validación
    // ? - en crear() al volver por error de regla de negocio
    private void cargarListas(Model model) {
        model.addAttribute("alumnos", alumnoService.listar());
        model.addAttribute("cursos", cursoService.listar());
    }
}
