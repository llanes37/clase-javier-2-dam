package com.curso.pfsqlite.service;

import com.curso.pfsqlite.domain.*;
import com.curso.pfsqlite.repository.AlumnoRepository;
import com.curso.pfsqlite.repository.CursoRepository;
import com.curso.pfsqlite.repository.MatriculaRepository;
import com.curso.pfsqlite.web.form.MatriculaForm;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: MatriculaService  |  CAPA: Service (Lógica de Negocio)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: Este es el servicio más complejo del proyecto
// ? La matrícula depende de dos entidades (Alumno y Curso) y tiene su propio
// ? ciclo de vida (ACTIVA → ANULADA / FINALIZADA), lo que genera más reglas.

// * 🧠 TEORÍA: Reglas que implementa esta clase
// ? 1) Alumno y curso deben existir en la base de datos.
// ? 2) La fecha de matriculación debe estar dentro del rango del curso.
// ? 3) No puede existir una matrícula ACTIVA duplicada para el mismo alumno+curso.

// * 🧠 TEORÍA: ¿Por qué anular() en vez de borrar() para desactivar?
// ? Borrar elimina el historial. Anular conserva el registro con estado ANULADA.
// ? En sistemas reales, el historial es valioso (auditoría, estadísticas, reclamaciones).

@Service
public class MatriculaService {

        private static final Logger log = LoggerFactory.getLogger(MatriculaService.class);

        // * Tres repositorios necesarios: uno por cada entidad implicada en la
        // operación
        // ? Nota didáctica: cuando un servicio necesita más de 3 repos es señal de que
        // ? quizá está haciendo demasiado (principio de responsabilidad única).
        // ? En este caso está justificado porque la matrícula conecta exactamente esas
        // tres entidades.
        private final MatriculaRepository matriculaRepository;
        private final AlumnoRepository alumnoRepository;
        private final CursoRepository cursoRepository;

        public MatriculaService(
                        MatriculaRepository matriculaRepository,
                        AlumnoRepository alumnoRepository,
                        CursoRepository cursoRepository) {
                this.matriculaRepository = matriculaRepository;
                this.alumnoRepository = alumnoRepository;
                this.cursoRepository = cursoRepository;
        }

        // ─────────────────────────────────────────────────────────────────────────
        // * 🔵 listar() → devuelve todas las matrículas (más recientes primero)
        // ─────────────────────────────────────────────────────────────────────────

        // * readOnly=true → transacción optimizada de solo lectura
        // ? El repositorio carga alumno y curso con @EntityGraph → evita problema N+1
        @Transactional(readOnly = true)
        public List<Matricula> listar() {
                log.debug("Consultando listado completo de matrículas");
                return matriculaRepository.findAllByOrderByFechaMatriculaDescIdDesc();
        }

        // ─────────────────────────────────────────────────────────────────────────
        // * 🔵 crear() → valida TODAS las reglas de negocio y persiste la matrícula
        // ─────────────────────────────────────────────────────────────────────────

        // * 🧠 TEORÍA: Flujo de validación (el orden importa):
        // ? Paso 1: Verificar existencia de alumno y curso → NotFoundException si no
        // existen.
        // ? Paso 2: Aplicar fecha por defecto (hoy) si no se especificó ninguna.
        // ? Paso 3: Comprobar ventana temporal del curso (fecha entre inicio y fin).
        // ? Paso 4: Comprobar que no hay matrícula ACTIVA duplicada para alumno+curso.
        // ? Paso 5: Persistir con estado ACTIVA.
        @Transactional
        public Matricula crear(MatriculaForm form) {

                // * Paso 1: recuperar entidades relacionadas
                // ? orElseThrow es más idiomático y seguro que comprobar null manualmente
                Alumno alumno = alumnoRepository.findById(form.getAlumnoId())
                                .orElseThrow(() -> new NotFoundException("Alumno no encontrado"));
                Curso curso = cursoRepository.findById(form.getCursoId())
                                .orElseThrow(() -> new NotFoundException("Curso no encontrado"));

                log.debug("Creando matrícula: alumnoId={}, cursoId={}", alumno.getId(), curso.getId());

                // * Paso 2: si el usuario no eligió fecha, usamos 'hoy' como valor por defecto
                LocalDate fecha = form.getFechaMatricula() == null ? LocalDate.now() : form.getFechaMatricula();

                // ! Paso 3: validar ventana temporal del curso
                // ? isBefore(inicio) → fecha ANTERIOR al comienzo del curso → inválida
                // ? isAfter(fin) → fecha POSTERIOR al fin del curso → inválida
                if (fecha.isBefore(curso.getFechaInicio()) || fecha.isAfter(curso.getFechaFin())) {
                        log.warn("Matrícula rechazada: fecha={} fuera de rango [{}, {}]",
                                        fecha, curso.getFechaInicio(), curso.getFechaFin());
                        throw new BusinessException(
                                        "La fecha de matrícula debe estar entre el inicio y fin del curso");
                }

                // ! Paso 4: unicidad de matrícula ACTIVA
                // ? Una matrícula ANULADA NO bloquea: el alumno puede volver a matricularse.
                // ? Es una decisión de negocio: el historial se conserva pero no impide
                // re-inscripción.
                if (matriculaRepository.existsByAlumnoIdAndCursoIdAndEstado(
                                alumno.getId(), curso.getId(), EstadoMatricula.ACTIVA)) {
                        log.warn("Matrícula ACTIVA duplicada bloqueada: alumnoId={}, cursoId={}",
                                        alumno.getId(), curso.getId());
                        throw new BusinessException(
                                        "No se permite una matrícula ACTIVA duplicada para el mismo alumno y curso");
                }

                // * Paso 5: construir entidad y persistir con estado ACTIVA
                // TODO: si se implementan cupos máximos por curso, añadir la validación aquí
                // antes del save
                Matricula matricula = new Matricula();
                matricula.setAlumno(alumno);
                matricula.setCurso(curso);
                matricula.setFechaMatricula(fecha);
                matricula.setEstado(EstadoMatricula.ACTIVA);

                Matricula guardada = matriculaRepository.save(matricula);
                log.info("Matrícula creada → id={}, alumno='{}', curso='{}'",
                                guardada.getId(), alumno.getNombre(), curso.getNombre());
                return guardada;
        }

        // ─────────────────────────────────────────────────────────────────────────
        // * 🔵 anular() → borrado lógico (cambia estado de ACTIVA a ANULADA)
        // ─────────────────────────────────────────────────────────────────────────

        // * 🧠 TEORÍA: Máquina de estados simple → ACTIVA → ANULADA
        // ? El registro permanece en BD con el historial intacto.
        // TODO: validar que el estado actual sea ACTIVA antes de anular (ejercicio
        // avanzado)
        @Transactional
        public void anular(Long id) {
                log.debug("Anulando matrícula id={}", id);
                Matricula matricula = matriculaRepository.findById(id)
                                .orElseThrow(() -> new NotFoundException("Matrícula no encontrada"));

                matricula.setEstado(EstadoMatricula.ANULADA);
                // * save() detecta que la entidad ya tiene ID → hace UPDATE en vez de INSERT
                matriculaRepository.save(matricula);
                log.info("Matrícula anulada → id={}", id);
        }

        // ─────────────────────────────────────────────────────────────────────────
        // * 🔵 borrar() → borrado físico (elimina el registro de la BD)
        // ─────────────────────────────────────────────────────────────────────────

        // ! ⚠️ Diferencia clave con anular():
        // ! anular() → cambia estado, conserva el registro (preferible en producción).
        // ! borrar() → elimina el registro definitivamente (útil para limpiar datos de
        // prueba).
        @Transactional
        public void borrar(Long id) {
                log.debug("Borrando físicamente matrícula id={}", id);
                Matricula matricula = matriculaRepository.findById(id)
                                .orElseThrow(() -> new NotFoundException("Matrícula no encontrada"));

                matriculaRepository.delete(matricula);
                log.info("Matrícula eliminada físicamente → id={}", id);
        }
}
