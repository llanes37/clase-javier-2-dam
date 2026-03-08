/*
 * ******************************************************************************************
 * 📘 AlumnoController — Lógica de negocio para alumnos
 *
 * Responsabilidades:
 * - Validar entradas (nombre no vacío, email válido y único).
 * - Orquestar creación/borrado con el repositorio.
 * - Transformar/normalizar datos (trim, lowercase email, parseo de fecha opcional).
 *
 * Contrato rápido
 * - listar(): List<Alumno>
 * - crear(nombre, email, fechaNacStr): Alumno (puede lanzar ValidationException)
 * - borrar(id): boolean (true si existía)
 *
 * TODO Alumno
 * - [ ] Añadir método actualizarNombre(String id, String nuevoNombre).
 * - [ ] Añadir búsqueda por texto (delegando en repo): listarPorNombreContiene(String texto).
 * - [ ] Añadir validación de edad mínima opcional (p.ej. >= 16 años).
 * ******************************************************************************************
 */
package com.curso.proyectofinal.controller;

import com.curso.proyectofinal.exception.ValidationException;
import com.curso.proyectofinal.model.Alumno;
import com.curso.proyectofinal.repository.AlumnoRepository;
import com.curso.proyectofinal.util.DateUtils;
import com.curso.proyectofinal.util.Validator;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

/** Lógica de negocio para alumnos. */
public class AlumnoController {
    private final AlumnoRepository repo;

    public AlumnoController(AlumnoRepository repo) {
        this.repo = repo;
    }

    // * Devuelve todos los alumnos en memoria
    public List<Alumno> listar() { return repo.findAll(); }

    // * Contrato
    // - Entradas: nombre (no vacío), email (válido, único), fecha opcional (yyyy-MM-dd)
    // - Salida: Alumno persistido con id (UUID)
    // - Errores: ValidationException si email duplicado; IllegalArgumentException si formato inválido
    public Alumno crear(String nombre, String email, String fechaNacStr) {
        Validator.requireNotBlank(nombre, "Nombre");
        Validator.requireEmail(email);
        if (repo.findByEmail(email).isPresent())
            throw new ValidationException("Ya existe un alumno con ese email");
        // ? Si el usuario no facilita una fecha, la dejamos null (campo opcional).
        // * DateUtils.parse() lanzará IllegalArgumentException con mensaje "Fecha inválida..." si el formato es incorrecto.
        LocalDate fnac = fechaNacStr == null || fechaNacStr.isBlank() ? null : DateUtils.parse(fechaNacStr);
        String id = UUID.randomUUID().toString();
        // * Normalizamos entradas: trim para nombre; email en minúsculas para comparaciones case-insensitive.
        Alumno a = new Alumno(id, nombre.trim(), email.trim().toLowerCase(), fnac);
        return repo.save(a);
    }

    // ! Borrado físico: elimina y persiste el CSV
    public boolean borrar(String id) {
        Validator.requireNotBlank(id, "Id");
        return repo.delete(id);
    }
}
