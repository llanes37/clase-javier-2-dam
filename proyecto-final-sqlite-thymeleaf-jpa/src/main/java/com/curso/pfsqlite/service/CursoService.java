package com.curso.pfsqlite.service;

import com.curso.pfsqlite.domain.Curso;
import com.curso.pfsqlite.domain.EstadoMatricula;
import com.curso.pfsqlite.repository.CursoRepository;
import com.curso.pfsqlite.repository.MatriculaRepository;
import com.curso.pfsqlite.web.form.CursoForm;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: CursoService  |  CAPA: Service (Lógica de Negocio)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: Reglas de negocio que implementa esta clase
// ? 1) La fecha de fin no puede ser anterior a la fecha de inicio.
// ? 2) No se puede borrar un curso que tenga matrículas ACTIVAS.

// * 🧠 TEORÍA: ¿Por qué validar las fechas aquí si la BD ya tiene un CHECK constraint?
// ? CHECK en BD (ck_cursos_fechas) → segunda barrera de seguridad ante inserciones directas.
// ? Service → lanza BusinessException con mensaje claro para el usuario.
// ? Regla general: validar en service para UX, reforzar en BD para integridad.

@Service
public class CursoService {

    // * Logger: registra lo que pasa en cada operación sin usar System.out.println
    private static final Logger log = LoggerFactory.getLogger(CursoService.class);

    // * Dos repositorios: CursoRepository para CRUD + MatriculaRepository para
    // borrado protegido
    private final CursoRepository cursoRepository;
    private final MatriculaRepository matriculaRepository;

    public CursoService(CursoRepository cursoRepository, MatriculaRepository matriculaRepository) {
        this.cursoRepository = cursoRepository;
        this.matriculaRepository = matriculaRepository;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 listar() → devuelve todos los cursos ordenados por ID
    // ─────────────────────────────────────────────────────────────────────────

    // * readOnly=true → transacción optimizada de solo lectura (sin tracking de
    // cambios)
    @Transactional(readOnly = true)
    public List<Curso> listar() {
        log.debug("Consultando listado completo de cursos");
        return cursoRepository.findAllByOrderByIdAsc();
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 crear() → valida coherencia de fechas y persiste el curso
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: Método isBefore() de LocalDate
    // ? Compara fechas sin componente de hora (solo año-mes-día).
    // ? LocalDate.of(2026,4,1).isBefore(LocalDate.of(2026,3,1)) → false → OK.
    // ? LocalDate.of(2026,2,1).isBefore(LocalDate.of(2026,3,1)) → true → error.
    @Transactional
    public Curso crear(CursoForm form) {
        log.debug("Intentando crear curso '{}', rango [{} - {}]",
                form.getNombre(), form.getFechaInicio(), form.getFechaFin());

        Curso curso = new Curso();
        aplicarFormulario(curso, form);

        Curso guardado = cursoRepository.save(curso);
        log.info("Curso creado → id={}, nombre='{}'", guardado.getId(), guardado.getNombre());
        return guardado;
    }

        // ─────────────────────────────────────────────────────────────────────────
        // * 🔵 buscarPorId() → carga un curso para rellenar el formulario de edición
        // ─────────────────────────────────────────────────────────────────────────

        @Transactional(readOnly = true)
        public Curso buscarPorId(Integer id) {
        return cursoRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("Curso no encontrado"));
        }

        // ─────────────────────────────────────────────────────────────────────────
        // * 🔵 actualizar() → valida y guarda cambios sobre un curso existente
        // ─────────────────────────────────────────────────────────────────────────

        @Transactional
        public Curso actualizar(Integer id, CursoForm form) {
        Curso curso = cursoRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("Curso no encontrado"));

        log.debug("Actualizando curso id={} con rango [{} - {}]",
            id, form.getFechaInicio(), form.getFechaFin());

        aplicarFormulario(curso, form);

        Curso guardado = cursoRepository.save(curso);
        log.info("Curso actualizado → id={}, nombre='{}'", guardado.getId(), guardado.getNombre());
        return guardado;
        }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 borrar() → elimina un curso con borrado protegido
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: Mismo patrón de borrado protegido que en AlumnoService
    // ? Si borramos el curso, sus matrículas quedarían huérfanas.
    // ? La FK ON DELETE RESTRICT en BD también bloquea el borrado,
    // ? pero con un error SQL incomprensible. Aquí damos un mensaje claro.
    @Transactional
    public void borrar(Integer id) {
        log.debug("Intentando borrar curso id={}", id);

        Curso curso = cursoRepository.findById(id)
                .orElseThrow(() -> {
                    log.warn("Curso no encontrado para borrar, id={}", id);
                    return new NotFoundException("Curso no encontrado");
                });

        // ! Comprobación de matrículas ACTIVAS antes de borrar
        if (matriculaRepository.existsByCursoIdAndEstado(id, EstadoMatricula.ACTIVA)) {
            log.warn("Borrado bloqueado: curso id={} tiene matrículas ACTIVAS", id);
            throw new BusinessException("No puedes borrar el curso porque tiene matrículas ACTIVAS");
        }

        cursoRepository.delete(curso);
        log.info("Curso eliminado → id={}", id);
    }

    private void aplicarFormulario(Curso curso, CursoForm form) {
        validarRangoFechas(form);
        curso.setNombre(form.getNombre().trim());
        curso.setTipo(form.getTipo());
        curso.setFechaInicio(form.getFechaInicio());
        curso.setFechaFin(form.getFechaFin());
        curso.setPrecio(form.getPrecio());
    }

    private void validarRangoFechas(CursoForm form) {
        if (form.getFechaFin().isBefore(form.getFechaInicio())) {
            log.warn("Curso rechazado por fechas inválidas: inicio={}, fin={}",
                    form.getFechaInicio(), form.getFechaFin());
            throw new BusinessException("La fecha de fin no puede ser anterior a la fecha de inicio");
        }
    }
}
