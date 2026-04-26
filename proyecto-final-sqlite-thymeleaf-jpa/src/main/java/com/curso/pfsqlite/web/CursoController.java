package com.curso.pfsqlite.web;

import com.curso.pfsqlite.domain.Curso;
import com.curso.pfsqlite.domain.CursoTipo;
import com.curso.pfsqlite.service.BusinessException;
import com.curso.pfsqlite.service.CursoService;
import com.curso.pfsqlite.web.form.CursoForm;
import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: CursoController  |  CAPA: Web (Controlador MVC)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: Patrón idéntico al de AlumnoController
// ? GET lista → GET formulario → POST crear → POST eliminar.
// ? Estudiando un controlador, entiendes todos los demás del proyecto.

// * 🧠 TEORÍA: ¿Por qué pasamos CursoTipo.values() al modelo?
// ? El formulario HTML necesita la lista de tipos para renderizar el <select> dinámicamente.
// ? Cuando Thymeleaf vuelve a renderizar la vista (por error), el modelo se descarta.
// ? Por eso hay que recargarlo explícitamente en cada return al formulario.
// ? Ventaja: si añadimos un nuevo tipo al enum (ej: HIBRIDO), el <select> se actualiza solo.

// TODO: añadir filtros por tipo y rango de fechas en la vista de listado (ejercicio intermedio)

@Controller
@RequestMapping("/cursos")
public class CursoController {

    private final CursoService cursoService;

    // * Inyección por constructor: patrón recomendado (permite `final` y facilita
    // tests)
    public CursoController(CursoService cursoService) {
        this.cursoService = cursoService;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GET /cursos → Muestra la lista de cursos disponibles
    // ─────────────────────────────────────────────────────────────────────────

    @GetMapping
    public String listar(Model model) {
        // * model.addAttribute("cursos", ...) → Thymeleaf accede como ${cursos} en la
        // vista
        model.addAttribute("cursos", cursoService.listar());
        return "cursos/lista";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GET /cursos/nuevo → Muestra el formulario de alta con tipos precargados
    // ─────────────────────────────────────────────────────────────────────────

    // ? CursoTipo.values() devuelve todos los valores del enum: [ONLINE,
    // PRESENCIAL]
    // ? Thymeleaf los usa para generar las opciones del <select> automáticamente.
    @GetMapping("/nuevo")
    public String nuevo(Model model) {
        model.addAttribute("form", new CursoForm());
        model.addAttribute("tipos", CursoTipo.values());
        return "cursos/nuevo";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 POST /cursos → Procesa el formulario de alta de curso
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: Flujo del POST con validación en dos capas
    // ? Capa 1 → Bean Validation (@Valid): campos obligatorios y formato correcto.
    // ? Capa 2 → Service (BusinessException): regla de fechas (fin >= inicio).
    // ! ⚠️ IMPORTANTE: en cada return al formulario hay que recargar `tipos`.
    // ! Si no se recarga, el <select> de tipo aparecerá vacío para el usuario.
    @PostMapping
    public String crear(
            @Valid @ModelAttribute("form") CursoForm form,
            BindingResult bindingResult,
            Model model,
            RedirectAttributes redirectAttributes) {

        if (bindingResult.hasErrors()) {
            // ! Recargamos 'tipos' porque el modelo se descarta al volver a renderizar
            model.addAttribute("tipos", CursoTipo.values());
            return "cursos/nuevo";
        }

        try {
            cursoService.crear(form);
            redirectAttributes.addFlashAttribute("ok", "Curso creado correctamente");
            return "redirect:/cursos";
        } catch (BusinessException ex) {
            // ! La regla de fechas falló en el service → mostramos el mensaje en el
            // formulario
            model.addAttribute("tipos", CursoTipo.values());
            model.addAttribute("error", ex.getMessage());
            return "cursos/nuevo";
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 POST /cursos/{id}/eliminar → Borrado protegido
    // ─────────────────────────────────────────────────────────────────────────

    // ? Si el curso tiene matrículas ACTIVAS, el service lanza BusinessException.
    // ? El curso NO se borra y el mensaje de error aparece como flash en la lista.
    @PostMapping("/{id}/eliminar")
    public String eliminar(@PathVariable Integer id, RedirectAttributes redirectAttributes) {
        try {
            cursoService.borrar(id);
            redirectAttributes.addFlashAttribute("ok", "Curso eliminado correctamente");
        } catch (BusinessException ex) {
            redirectAttributes.addFlashAttribute("error", ex.getMessage());
        }
        return "redirect:/cursos";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GET /cursos/{id}/editar → Muestra el formulario de edición relleno
    // ─────────────────────────────────────────────────────────────────────────

    @GetMapping("/{id}/editar")
    public String editar(@PathVariable Integer id, Model model) {
        Curso curso = cursoService.buscarPorId(id);
        CursoForm form = new CursoForm();
        form.setNombre(curso.getNombre());
        form.setTipo(curso.getTipo());
        form.setFechaInicio(curso.getFechaInicio());
        form.setFechaFin(curso.getFechaFin());
        form.setPrecio(curso.getPrecio());
        model.addAttribute("form", form);
        model.addAttribute("tipos", CursoTipo.values());
        model.addAttribute("cursoId", id);
        return "cursos/editar";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 POST /cursos/{id}/editar → Procesa y guarda los cambios del curso
    // ─────────────────────────────────────────────────────────────────────────

    @PostMapping("/{id}/editar")
    public String actualizar(
            @PathVariable Integer id,
            @Valid @ModelAttribute("form") CursoForm form,
            BindingResult bindingResult,
            Model model,
            RedirectAttributes redirectAttributes) {

        if (bindingResult.hasErrors()) {
            model.addAttribute("tipos", CursoTipo.values());
            model.addAttribute("cursoId", id);
            return "cursos/editar";
        }

        try {
            cursoService.actualizar(id, form);
            redirectAttributes.addFlashAttribute("ok", "Curso actualizado correctamente");
            return "redirect:/cursos";
        } catch (BusinessException ex) {
            model.addAttribute("tipos", CursoTipo.values());
            model.addAttribute("cursoId", id);
            model.addAttribute("error", ex.getMessage());
            return "cursos/editar";
        }
    }
}
