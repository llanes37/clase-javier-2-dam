/*
 * ******************************************************************************************
 * 📘 MatriculaController — Lógica de negocio para matrículas
 *
 * Responsabilidades:
 * - Validar existencia de Alumno y Curso.
 * - Validar ventana temporal de matrícula dentro de [inicio, fin] del curso.
 * - Gestionar estados (ACTIVA, ANULADA, FINALIZADA).
 *
 * TODO Alumno
 * - [ ] Evitar duplicados: no permitir la misma (alumnoId, cursoId) activa más de una vez.
 * - [ ] Añadir finalizar(String id) → estado FINALIZADA si fecha actual > fin del curso.
 * - [ ] Listar por alumno/curso desde controlador (delegando en repo).
 * ******************************************************************************************
 */
package com.curso.proyectofinal.controller;

import com.curso.proyectofinal.exception.ValidationException;
import com.curso.proyectofinal.model.*;
import com.curso.proyectofinal.repository.AlumnoRepository;
import com.curso.proyectofinal.repository.CursoRepository;
import com.curso.proyectofinal.repository.MatriculaRepository;
import com.curso.proyectofinal.util.DateUtils;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

/** Lógica de negocio para matrículas. */
public class MatriculaController {
    private final MatriculaRepository repo;
    private final AlumnoRepository alumnoRepo;
    private final CursoRepository cursoRepo;

    public MatriculaController(MatriculaRepository repo, AlumnoRepository alumnoRepo, CursoRepository cursoRepo) {
        this.repo = repo;
        this.alumnoRepo = alumnoRepo;
        this.cursoRepo = cursoRepo;
    }

    public List<Matricula> listar() { return repo.findAll(); }

    // * Contrato: crea matrícula ACTIVA si pasa validaciones
    public Matricula matricular(String alumnoId, String cursoId, String fechaStr) {
        // * Validamos existencia de las entidades relacionadas: alumno y curso.
        // ? Si no existen, lanzamos ValidationException con mensaje claro para el usuario.
        Alumno a = alumnoRepo.findById(alumnoId).orElseThrow(() -> new ValidationException("Alumno no encontrado"));
        Curso c = cursoRepo.findById(cursoId).orElseThrow(() -> new ValidationException("Curso no encontrado"));

        // ? Si la fecha es vacía, usamos la fecha actual como fecha de matrícula.
        LocalDate fecha = (fechaStr == null || fechaStr.isBlank()) ? LocalDate.now() : DateUtils.parse(fechaStr);

        // ! Reglas temporales: la fecha de matrícula debe estar dentro de la ventana del curso si existen fechas.
        if (c.getFechaInicio() != null && fecha.isBefore(c.getFechaInicio()))
            throw new ValidationException("La fecha de matrícula no puede ser anterior al inicio del curso");
        if (c.getFechaFin() != null && fecha.isAfter(c.getFechaFin()))
            throw new ValidationException("La fecha de matrícula no puede ser posterior al fin del curso");

        // TODO: Evitar duplicado (alumnoId, cursoId) si ya existe una matrícula ACTIVA

        // * Crear la matrícula con estado ACTIVA y persistir.
        String id = UUID.randomUUID().toString();
        Matricula m = new Matricula(id, a.getId(), c.getId(), fecha, EstadoMatricula.ACTIVA);
        return repo.save(m);
    }

    // ! Anulación: transición a estado ANULADA (persistencia inmediata)
    public boolean anular(String matriculaId) {
        Matricula m = repo.findById(matriculaId).orElseThrow(() -> new ValidationException("Matrícula no encontrada"));
        m.setEstado(EstadoMatricula.ANULADA);
        repo.update(m);
        return true;
    }
}
