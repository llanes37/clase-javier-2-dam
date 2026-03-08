/*
 * ******************************************************************************************
 * 📘 CursoController — Lógica de negocio para cursos
 *
 * Responsabilidades:
 * - Validar nombre, tipo, fechas y precio.
 * - Regla: fechaFin >= fechaInicio; precio >= 0.
 *
 * TODO Alumno
 * - [ ] Añadir método listarPorTipo(String tipo).
 * - [ ] Añadir regla opcional: duración máxima 365 días.
 * - [ ] Añadir actualización de precio con validación.
 * ******************************************************************************************
 */
package com.curso.proyectofinal.controller;

import com.curso.proyectofinal.exception.ValidationException;
import com.curso.proyectofinal.model.Curso;
import com.curso.proyectofinal.model.CursoTipo;
import com.curso.proyectofinal.repository.CursoRepository;
import com.curso.proyectofinal.util.DateUtils;
import com.curso.proyectofinal.util.Validator;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

/** Lógica de negocio para cursos. */
public class CursoController {
    private final CursoRepository repo;

    public CursoController(CursoRepository repo) { this.repo = repo; }

    public List<Curso> listar() { return repo.findAll(); }

    // * Contrato: entradas válidas → Curso persistido, id UUID
    public Curso crear(String nombre, String tipoStr, String fIniStr, String fFinStr, double precio) {
        Validator.requireNotBlank(nombre, "Nombre");
        Validator.requirePositive(precio, "Precio");
        // * Convertimos el string a enum; lanzará IllegalArgumentException si tipoStr no es válido.
        CursoTipo tipo = CursoTipo.valueOf(tipoStr.toUpperCase());
        // ? Parseo de fechas (DateUtils valida formato yyyy-MM-dd)
        LocalDate ini = DateUtils.parse(fIniStr);
        LocalDate fin = DateUtils.parse(fFinStr);
    if (fin.isBefore(ini)) throw new ValidationException("Fecha fin no puede ser anterior a inicio");
    // TODO: Validar duración máxima opcional (p.ej. <= 365 días)

        String id = UUID.randomUUID().toString();
        // * Creamos la entidad Curso con datos normalizados y la persistimos a través del repo.
        Curso c = new Curso(id, nombre.trim(), tipo, ini, fin, precio);
        return repo.save(c);
    }

    // ! Borrado físico: elimina y persiste el CSV
    public boolean borrar(String id) { return repo.delete(id); }
}
