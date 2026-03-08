package com.curso.proyectofinal.repository;

import com.curso.proyectofinal.model.Alumno;
import com.curso.proyectofinal.persistence.CsvUtils;
import com.curso.proyectofinal.persistence.FileStorage;
import com.curso.proyectofinal.util.DateUtils;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

/*
 * ******************************************************************************************
 * 📘 AlumnoRepository — Persistencia CSV de Alumno
 *
 * - Fichero: resources/data/alumnos.csv
 * - Cabecera: id;nombre;email;fechaNacimiento
 * - Serializa LocalDate con DateUtils (yyyy-MM-dd) o vacío si null.
 *
 * TODO Alumno
 * - [ ] Implementar count() y deleteAll().
 * - [ ] Implementar findByNombreContains(String texto) (case-insensitive).
 * ******************************************************************************************
 */
/**
 * Repositorio de alumnos con persistencia CSV.
 */
public class AlumnoRepository implements Repository<Alumno> {
    private final Path file = Paths.get("resources", "data", "alumnos.csv");
    private final Map<String, Alumno> data = new LinkedHashMap<>();

    public AlumnoRepository() {
        load();
    }

    // * Carga inicial desde CSV a memoria (Map ordenado por inserción)
    private void load() {
        data.clear();
        List<String> lines = FileStorage.readAllLines(file);
        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i);
            // * Saltamos la cabecera si existe (primera línea que comienza por "id;")
            if (i == 0 && line.startsWith("id;")) continue; // cabecera
            if (line.trim().isEmpty()) continue;
            List<String> f = CsvUtils.parseCsvLine(line);
            String id = f.get(0);
            String nombre = f.get(1);
            String email = f.get(2);
            // ? El campo fecha puede estar vacío: en ese caso dejamos null.
            LocalDate fnac = f.get(3).isEmpty() ? null : DateUtils.parse(f.get(3));
            data.put(id, new Alumno(id, nombre, email, fnac));
        }
    }

    // * Persistencia: reescribe CSV completo (con cabecera)
    private void persist() {
        List<String> lines = new ArrayList<>();
        lines.add("id;nombre;email;fechaNacimiento");
        lines.addAll(data.values().stream().map(a ->
                CsvUtils.toCsvLine(Arrays.asList(
                        a.getId(), a.getNombre(), a.getEmail(),
            // * Formateamos la fecha a yyyy-MM-dd o cadena vacía si es null
            a.getFechaNacimiento() == null ? "" : DateUtils.format(a.getFechaNacimiento())
                ))
        ).collect(Collectors.toList()));
        FileStorage.writeLines(file, lines);
    }

    @Override
    public List<Alumno> findAll() { return new ArrayList<>(data.values()); }

    @Override
    public Optional<Alumno> findById(String id) { return Optional.ofNullable(data.get(id)); }

    public Optional<Alumno> findByEmail(String email) {
        return data.values().stream().filter(a -> a.getEmail().equalsIgnoreCase(email)).findFirst();
    }

    // TODO: Búsqueda por nombre contiene (case-insensitive)

    @Override
    public Alumno save(Alumno entity) {
        data.put(entity.getId(), entity);
        persist();
        return entity;
    }

    @Override
    public Alumno update(Alumno entity) {
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
