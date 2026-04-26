package com.curso.pfsqlite.web;

import com.curso.pfsqlite.domain.Alumno;
import com.curso.pfsqlite.service.AlumnoService;
import com.curso.pfsqlite.service.BusinessException;
import com.curso.pfsqlite.web.form.AlumnoForm;
import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: AlumnoController  |  CAPA: Web (Controlador MVC)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: Responsabilidad del controlador en arquitectura en capas
// ? El controlador SOLO gestiona HTTP: recibe → valida formulario → delega → responde.
// ! ⚠️ REGLA DE ORO: el controlador NO contiene reglas de negocio.
// ! Si encuentras una regla aquí (ej: "si el email empieza por 'admin'..."),
// ! es un error de arquitectura → muévela al Service.

// * 🧠 TEORÍA: ¿Por qué @RequestMapping("/alumnos") en la clase?
// ? Es un prefijo común para todos los endpoints. Spring lo combina con los @GetMapping/@PostMapping:
// ? GET  /alumnos               → listar()
// ? GET  /alumnos/nuevo         → nuevo()
// ? POST /alumnos               → crear()
// ? POST /alumnos/{id}/eliminar → eliminar()

@Controller
@RequestMapping("/alumnos")
public class AlumnoController {

    private final AlumnoService alumnoService;

    // * 🧠 TEORÍA: Inyección por constructor (patrón recomendado)
    // ? `final` garantiza que el servicio no puede reasignarse accidentalmente.
    // ? Facilita los tests unitarios al poder pasar un mock directamente.
    public AlumnoController(AlumnoService alumnoService) {
        this.alumnoService = alumnoService;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GET /alumnos → Muestra la lista de alumnos registrados
    // ─────────────────────────────────────────────────────────────────────────

    // ? model.addAttribute("alumnos", ...) → Thymeleaf accede como ${alumnos} en la
    // vista HTML
    @GetMapping
    public String listar(Model model) {
        model.addAttribute("alumnos", alumnoService.listar());
        return "alumnos/lista";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GET /alumnos/nuevo → Muestra el formulario de alta en blanco
    // ─────────────────────────────────────────────────────────────────────────

    // ? Pasamos un AlumnoForm vacío para que Thymeleaf lo vincule con
    // th:object="${form}"
    @GetMapping("/nuevo")
    public String nuevo(Model model) {
        model.addAttribute("form", new AlumnoForm());
        return "alumnos/nuevo";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 POST /alumnos → Procesa el formulario de alta de alumno
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: Flujo del POST con validación en dos capas
    // ? Capa 1 → Bean Validation (@Valid): valida anotaciones de AlumnoForm
    // (@NotBlank, @Email).
    // ? Capa 2 → Service (BusinessException): valida reglas de negocio (email
    // único, formato).
    // ? Si la Capa 1 falla → volvemos al formulario con los errores de campo
    // resaltados.
    // ? Si la Capa 2 falla → volvemos al formulario con un mensaje de error
    // general.

    // * 🧠 TEORÍA: ¿Qué es un atributo flash de redirect?
    // ? Sobrevive UNA sola redirección y desaparece automáticamente.
    // ? Si el usuario recarga la página, el mensaje NO vuelve a aparecer (evita
    // doble POST).
    @PostMapping
    public String crear(
            @Valid @ModelAttribute("form") AlumnoForm form,
            BindingResult bindingResult,
            Model model,
            RedirectAttributes redirectAttributes) {

        // Paso 1: errores de validación de formulario (campo vacío, email mal formado,
        // etc.)
        if (bindingResult.hasErrors()) {
            return "alumnos/nuevo";
        }

        try {
            // Paso 2: delegar al service (valida email único, normaliza y persiste)
            alumnoService.crear(form);
            redirectAttributes.addFlashAttribute("ok", "Alumno creado correctamente");
            return "redirect:/alumnos";
        } catch (BusinessException ex) {
            // ! Error de regla de negocio (ej: email duplicado) → se muestra en el
            // formulario
            model.addAttribute("error", ex.getMessage());
            return "alumnos/nuevo";
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 POST /alumnos/{id}/eliminar → Borrado protegido
    // ─────────────────────────────────────────────────────────────────────────

    // ? Se usa POST (no DELETE) porque los formularios HTML estándar solo soportan
    // GET y POST.
    // ? Si hay matrículas ACTIVAS, el service lanza BusinessException y el alumno
    // NO se borra.
    @PostMapping("/{id}/eliminar")
    public String eliminar(@PathVariable Integer id, RedirectAttributes redirectAttributes) {
        try {
            alumnoService.borrar(id);
            redirectAttributes.addFlashAttribute("ok", "Alumno eliminado correctamente");
        } catch (BusinessException ex) {
            redirectAttributes.addFlashAttribute("error", ex.getMessage());
        }
        return "redirect:/alumnos";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GET /alumnos/{id}/editar → Muestra el formulario de edición relleno
    // ─────────────────────────────────────────────────────────────────────────

    @GetMapping("/{id}/editar")
    public String editar(@PathVariable Integer id, Model model) {
        Alumno alumno = alumnoService.buscarPorId(id);
        AlumnoForm form = new AlumnoForm();
        form.setNombre(alumno.getNombre());
        form.setEmail(alumno.getEmail());
        form.setFechaNacimiento(alumno.getFechaNacimiento());
        model.addAttribute("form", form);
        model.addAttribute("alumnoId", id);
        return "alumnos/editar";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 POST /alumnos/{id}/editar → Procesa y guarda los cambios del alumno
    // ─────────────────────────────────────────────────────────────────────────

    @PostMapping("/{id}/editar")
    public String actualizar(
            @PathVariable Integer id,
            @Valid @ModelAttribute("form") AlumnoForm form,
            BindingResult bindingResult,
            Model model,
            RedirectAttributes redirectAttributes) {

        if (bindingResult.hasErrors()) {
            model.addAttribute("alumnoId", id);
            return "alumnos/editar";
        }

        try {
            alumnoService.actualizar(id, form);
            redirectAttributes.addFlashAttribute("ok", "Alumno actualizado correctamente");
            return "redirect:/alumnos";
        } catch (BusinessException ex) {
            model.addAttribute("error", ex.getMessage());
            model.addAttribute("alumnoId", id);
            return "alumnos/editar";
        }
    }
}
