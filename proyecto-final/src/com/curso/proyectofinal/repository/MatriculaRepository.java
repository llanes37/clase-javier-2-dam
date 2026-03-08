/*
 * ******************************************************************************************
 * 📘 MatriculaRepository — Persistencia CSV de Matricula
 * Fichero: resources/data/matriculas.csv
 * Cabecera: id;alumnoId;cursoId;fechaMatricula;estado
 *
 * TODO Alumno
 * - [ ] Implementar count()/deleteAll().
 * - [ ] Implementar existsByAlumnoAndCurso(String alumnoId, String cursoId).
 * ******************************************************************************************
 */
package com.curso.proyectofinal.repository;

import com.curso.proyectofinal.model.EstadoMatricula;
import com.curso.proyectofinal.model.Matricula;
import com.curso.proyectofinal.persistence.CsvUtils;
import com.curso.proyectofinal.persistence.FileStorage;
import com.curso.proyectofinal.util.DateUtils;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

public class MatriculaRepository implements Repository<Matricula> {
    private final Path file = Paths.get("resources", "data", "matriculas.csv");
    private final Map<String, Matricula> data = new LinkedHashMap<>();

    public MatriculaRepository() { load(); }

    // * Carga inicial desde CSV
    private void load() {
        data.clear();
        List<String> lines = FileStorage.readAllLines(file);
        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i);
            if (i == 0 && line.startsWith("id;")) continue;
            if (line.trim().isEmpty()) continue;
            List<String> f = CsvUtils.parseCsvLine(line);
            String id = f.get(0);
            String alumnoId = f.get(1);
            String cursoId = f.get(2);
            // ? Fecha de matrícula: puede estar vacía en CSV
            LocalDate fecha = f.get(3).isEmpty() ? null : DateUtils.parse(f.get(3));
            // * Estado: si vacío, por compatibilidad asumimos ACTIVA.
            EstadoMatricula estado = f.get(4).isEmpty() ? EstadoMatricula.ACTIVA : EstadoMatricula.valueOf(f.get(4));
            data.put(id, new Matricula(id, alumnoId, cursoId, fecha, estado));
        }
    }

    // * Persistencia: reescribe CSV con cabecera
    private void persist() {
        List<String> lines = new ArrayList<>();
        lines.add("id;alumnoId;cursoId;fechaMatricula;estado");
        lines.addAll(data.values().stream().map(m ->
                CsvUtils.toCsvLine(Arrays.asList(
                        m.getId(), m.getAlumnoId(), m.getCursoId(),
                        m.getFechaMatricula() == null ? "" : DateUtils.format(m.getFechaMatricula()),
                        m.getEstado() == null ? "" : m.getEstado().name()
                ))
        ).collect(Collectors.toList()));
        FileStorage.writeLines(file, lines);
    }

    @Override
    public List<Matricula> findAll() { return new ArrayList<>(data.values()); }

    @Override
    public Optional<Matricula> findById(String id) { return Optional.ofNullable(data.get(id)); }

    @Override
    public Matricula save(Matricula entity) {
        data.put(entity.getId(), entity);
        persist();
        return entity;
    }

    @Override
    public Matricula update(Matricula entity) {
        data.put(entity.getId(), entity);
        persist();
        return entity;
    }

    @Override
    public boolean delete(String id) {
        boolean removed = data.remove(id) != null;
        if (removed) persist();
        return removed;
    }

    public List<Matricula> findByAlumnoId(String alumnoId) {
        List<Matricula> list = new ArrayList<>();
        for (Matricula m : data.values()) if (m.getAlumnoId().equals(alumnoId)) list.add(m);
        return list;
    }

    public List<Matricula> findByCursoId(String cursoId) {
        List<Matricula> list = new ArrayList<>();
        for (Matricula m : data.values()) if (m.getCursoId().equals(cursoId)) list.add(m);
        return list;
    }

    // TODO: existsByAlumnoAndCurso(String alumnoId, String cursoId)
}
