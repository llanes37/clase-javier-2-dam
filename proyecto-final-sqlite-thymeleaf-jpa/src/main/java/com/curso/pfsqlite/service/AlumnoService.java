package com.curso.pfsqlite.service;

import com.curso.pfsqlite.domain.Alumno;
import com.curso.pfsqlite.domain.EstadoMatricula;
import com.curso.pfsqlite.repository.AlumnoRepository;
import com.curso.pfsqlite.repository.MatriculaRepository;
import com.curso.pfsqlite.web.form.AlumnoForm;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.regex.Pattern;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: AlumnoService  |  CAPA: Service (Lógica de Negocio)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: Principio clave de arquitectura en capas
// ? Las reglas de negocio viven AQUÍ en el service, NUNCA en el controlador ni en la entidad.
// ? Controlador = gestiona HTTP. Entidad = almacena estado. Service = lógica de negocio.

// * 🧠 TEORÍA: Reglas que implementa esta clase
// ? 1) El email debe tener formato válido (regex).
// ? 2) El email debe ser único sin importar mayúsculas/minúsculas.
// ? 3) No se puede borrar un alumno con matrículas ACTIVAS (borrado protegido).

// * 🧠 TEORÍA: ¿Por qué doble barrera para el email único?
// ? Service → mensaje claro y amigable al usuario ("Ya existe un alumno con ese email").
// ? BD (UNIQUE constraint) → segunda barrera ante inserciones directas o bugs concurrentes.

// * @Service → Spring detecta esta clase en el arranque y la registra como componente
@Service
public class AlumnoService {

    // * 🧠 TEORÍA: Logger SLF4J → herramienta profesional para registrar mensajes
    // ? Tiene niveles (DEBUG, INFO, WARN, ERROR): se pueden filtrar sin cambiar
    // código.
    // ? System.out.println siempre imprime y no se puede configurar ni desactivar.
    private static final Logger log = LoggerFactory.getLogger(AlumnoService.class);

    // ! ⚠️ Regex de email: cubre el 99% de los casos reales
    // ! No es perfecta (existen emails raros válidos), pero es suficiente para este
    // dominio
    private static final Pattern EMAIL_REGEX = Pattern.compile(
            "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");

    // * Inyección por constructor → permite `final` y facilita tests unitarios con
    // mocks
    private final AlumnoRepository alumnoRepository;
    private final MatriculaRepository matriculaRepository;

    public AlumnoService(AlumnoRepository alumnoRepository, MatriculaRepository matriculaRepository) {
        this.alumnoRepository = alumnoRepository;
        this.matriculaRepository = matriculaRepository;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 listar() → devuelve todos los alumnos ordenados por ID
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: @Transactional(readOnly = true)
    // ? readOnly=true → Hibernate no rastrea cambios en entidades → menos memoria y
    // CPU.
    // ? Usar SIEMPRE en métodos que solo leen datos sin modificarlos.
    @Transactional(readOnly = true)
    public List<Alumno> listar() {
        log.debug("Consultando listado completo de alumnos");
        return alumnoRepository.findAllByOrderByIdAsc();
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 crear() → valida todas las reglas de negocio y persiste el alumno
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: Flujo completo paso a paso
    // ? Paso 1: Normalizar email (trim + lowercase).
    // ? Paso 2: Validar formato con regex.
    // ? Paso 3: Comprobar unicidad en BD.
    // ? Paso 4: Construir entidad y persistir.
    @Transactional
    public Alumno crear(AlumnoForm form) {

        // * Paso 1: normalizar ANTES de validar
        // ? "ANA@MAIL.COM " y "ana@mail.com" deben tratarse como el mismo email
        String emailNormalizado = normalizarEmail(form.getEmail());
        log.debug("Intentando crear alumno con email: {}", emailNormalizado);

        // ! Paso 2: validar formato → lanza BusinessException si el formato es inválido
        if (!EMAIL_REGEX.matcher(emailNormalizado).matches()) {
            log.warn("Email con formato inválido rechazado: {}", emailNormalizado);
            throw new BusinessException("El email no tiene un formato válido");
        }

        // ! Paso 3: comprobar unicidad en BD
        // ? existsByEmailIgnoreCase es más eficiente que findByEmail().isPresent()
        // ? porque solo devuelve true/false sin cargar la entidad completa
        if (alumnoRepository.existsByEmailIgnoreCase(emailNormalizado)) {
            log.warn("Email duplicado bloqueado: {}", emailNormalizado);
            throw new BusinessException("Ya existe un alumno con ese email");
        }

        // * Paso 4: construir entidad con datos limpios y persistir
        Alumno alumno = new Alumno();
        alumno.setNombre(form.getNombre().trim());
        alumno.setEmail(emailNormalizado);
        alumno.setFechaNacimiento(form.getFechaNacimiento());

        // * save() persiste la entidad y devuelve la instancia con el ID generado por
        // BD
        Alumno guardado = alumnoRepository.save(alumno);
        log.info("Alumno creado → id={}, email={}", guardado.getId(), guardado.getEmail());
        return guardado;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 borrar() → elimina un alumno con borrado protegido
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: Borrado protegido
    // ? Si borramos el alumno con matrículas ACTIVAS, esas matrículas quedarían
    // huérfanas
    // ? (registros apuntando a una fila inexistente en la tabla alumnos).
    // ? La FK ON DELETE RESTRICT en BD también lo impide, pero su mensaje de error
    // ? es técnico e incomprensible. Aquí damos un mensaje claro al usuario.
    @Transactional
    public void borrar(Integer id) {
        log.debug("Intentando borrar alumno id={}", id);

        // * orElseThrow: si findById devuelve empty(), lanzamos NotFoundException
        // ? Es más idiomático y seguro que comprobar null manualmente
        Alumno alumno = alumnoRepository.findById(id)
                .orElseThrow(() -> {
                    log.warn("Alumno no encontrado para borrar, id={}", id);
                    return new NotFoundException("Alumno no encontrado");
                });

        // ! Comprobación de matrículas ACTIVAS antes de borrar
        if (matriculaRepository.existsByAlumnoIdAndEstado(id, EstadoMatricula.ACTIVA)) {
            log.warn("Borrado bloqueado: alumno id={} tiene matrículas ACTIVAS", id);
            throw new BusinessException("No puedes borrar el alumno porque tiene matrículas ACTIVAS");
        }

        alumnoRepository.delete(alumno);
        log.info("Alumno eliminado → id={}", id);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 buscarPorId() → carga un alumno por su ID (para formulario de edición)
    // ─────────────────────────────────────────────────────────────────────────

    @Transactional(readOnly = true)
    public Alumno buscarPorId(Integer id) {
        return alumnoRepository.findById(id)
                .orElseThrow(() -> new NotFoundException("Alumno no encontrado"));
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 actualizar() → valida y actualiza los datos de un alumno existente
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: Diferencia clave con crear()
    // ? Solo bloqueamos el email duplicado si el alumno CAMBIÓ de email.
    // ? Si guarda el mismo email que ya tenía no debe lanzar error de duplicado.
    @Transactional
    public Alumno actualizar(Integer id, AlumnoForm form) {
        Alumno alumno = alumnoRepository.findById(id)
                .orElseThrow(() -> new NotFoundException("Alumno no encontrado"));

        String emailNormalizado = normalizarEmail(form.getEmail());
        log.debug("Actualizando alumno id={} con email={}", id, emailNormalizado);

        if (!EMAIL_REGEX.matcher(emailNormalizado).matches()) {
            log.warn("Email inválido al actualizar alumno id={}: {}", id, emailNormalizado);
            throw new BusinessException("El email no tiene un formato válido");
        }

        // ! Solo comprobar unicidad si el email realmente ha cambiado
        if (!emailNormalizado.equalsIgnoreCase(alumno.getEmail())
                && alumnoRepository.existsByEmailIgnoreCase(emailNormalizado)) {
            log.warn("Email duplicado al actualizar alumno id={}: {}", id, emailNormalizado);
            throw new BusinessException("Ya existe un alumno con ese email");
        }

        alumno.setNombre(form.getNombre().trim());
        alumno.setEmail(emailNormalizado);
        alumno.setFechaNacimiento(form.getFechaNacimiento());

        Alumno guardado = alumnoRepository.save(alumno);
        log.info("Alumno actualizado → id={}, email={}", guardado.getId(), guardado.getEmail());
        return guardado;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 normalizarEmail() → método privado auxiliar
    // ─────────────────────────────────────────────────────────────────────────

    // * Centraliza la normalización del email en un único punto
    // ? Si algún día cambia la lógica (ej: eliminar puntos del local part), solo se
    // modifica aquí
    private String normalizarEmail(String email) {
        return email == null ? "" : email.trim().toLowerCase();
    }
}
