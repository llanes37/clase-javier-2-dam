/*
 * ******************************************************************************************
 * 📘 CursoRepository — Persistencia CSV de Curso
 * Fichero: resources/data/cursos.csv
 * Cabecera: id;nombre;tipo;fechaInicio;fechaFin;precio
 *
 * TODO Alumno
 * - [ ] Implementar count()/deleteAll().
 * - [ ] Implementar findByTipo(CursoTipo tipo).
 * ******************************************************************************************
 */
package com.curso.proyectofinal.repository;

import com.curso.proyectofinal.model.Curso;
import com.curso.proyectofinal.model.CursoTipo;
import com.curso.proyectofinal.persistence.CsvUtils;
import com.curso.proyectofinal.persistence.FileStorage;
import com.curso.proyectofinal.util.DateUtils;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

public class CursoRepository implements Repository<Curso> {
    private final Path file = Paths.get("resources", "data", "cursos.csv");
    private final Map<String, Curso> data = new LinkedHashMap<>();

    public CursoRepository() { load(); }

    // * Carga inicial desde CSV a memoria
    private void load() {
        data.clear();
        List<String> lines = FileStorage.readAllLines(file);
        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i);
            if (i == 0 && line.startsWith("id;")) continue;
            if (line.trim().isEmpty()) continue;
            List<String> f = CsvUtils.parseCsvLine(line);
            String id = f.get(0);
            String nombre = f.get(1);
            // ? Parseo de campos: algunos pueden estar vacíos en CSV
            CursoTipo tipo = f.get(2).isEmpty() ? null : CursoTipo.valueOf(f.get(2));
            LocalDate ini = f.get(3).isEmpty() ? null : DateUtils.parse(f.get(3));
            LocalDate fin = f.get(4).isEmpty() ? null : DateUtils.parse(f.get(4));
            // * Precio: si vacío, asumimos 0.0; ojo con NumberFormatException si CSV mal formado.
            double precio = f.get(5).isEmpty() ? 0.0 : Double.parseDouble(f.get(5));
            data.put(id, new Curso(id, nombre, tipo, ini, fin, precio));
        }
    }

    // * Persistencia: reescribe CSV con cabecera
    private void persist() {
        List<String> lines = new ArrayList<>();
        lines.add("id;nombre;tipo;fechaInicio;fechaFin;precio");
        lines.addAll(data.values().stream().map(c ->
                CsvUtils.toCsvLine(Arrays.asList(
                        c.getId(), c.getNombre(), c.getTipo() == null ? "" : c.getTipo().name(),
                        c.getFechaInicio() == null ? "" : DateUtils.format(c.getFechaInicio()),
                        c.getFechaFin() == null ? "" : DateUtils.format(c.getFechaFin()),
                        String.valueOf(c.getPrecio())
                ))
        ).collect(Collectors.toList()));
        FileStorage.writeLines(file, lines);
    }

    @Override
    public List<Curso> findAll() { return new ArrayList<>(data.values()); }

    @Override
    public Optional<Curso> findById(String id) { return Optional.ofNullable(data.get(id)); }

    @Override
    public Curso save(Curso entity) {
        data.put(entity.getId(), entity);
        persist();
        return entity;
    }

    @Override
    public Curso update(Curso entity) {
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
}
