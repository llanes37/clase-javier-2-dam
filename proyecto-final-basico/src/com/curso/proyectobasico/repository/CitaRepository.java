package com.curso.proyectobasico.repository;

import com.curso.proyectobasico.model.Cita;
import com.curso.proyectobasico.model.EstadoCita;
import com.curso.proyectobasico.persistence.CsvUtils;
import com.curso.proyectobasico.persistence.FileStorage;
import com.curso.proyectobasico.util.DateUtils;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

/*
 * Persistencia CSV de Cita.
 * Fichero: resources/data/citas.csv
 * Cabecera: id;clienteId;fecha;estado;descripcion
 */
public class CitaRepository implements Repository<Cita> {
    private final Path file = Paths.get("resources", "data", "citas.csv");
    private final Map<String, Cita> data = new LinkedHashMap<>();

    public CitaRepository() {
        load();
    }

    private void load() {
        data.clear();
        List<String> lines = FileStorage.readAllLines(file);
        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i);
            if (i == 0 && line.startsWith("id;")) continue;
            if (line.trim().isEmpty()) continue;
            List<String> fields = CsvUtils.parseCsvLine(line);
            String id = fields.get(0);
            String clienteId = fields.get(1);
            LocalDate fecha = DateUtils.parse(fields.get(2));
            EstadoCita estado = EstadoCita.valueOf(fields.get(3));
            String descripcion = fields.size() > 4 ? fields.get(4) : "";
            data.put(id, new Cita(id, clienteId, fecha, estado, descripcion));
        }
    }

    private void persist() {
        List<String> lines = new ArrayList<>();
        lines.add("id;clienteId;fecha;estado;descripcion");
        lines.addAll(data.values().stream()
                .map(c -> CsvUtils.toCsvLine(Arrays.asList(
                        c.getId(),
                        c.getClienteId(),
                        DateUtils.format(c.getFecha()),
                        c.getEstado().name(),
                        c.getDescripcion() == null ? "" : c.getDescripcion()
                )))
                .collect(Collectors.toList()));
        FileStorage.writeLines(file, lines);
    }

    @Override
    public List<Cita> findAll() {
        return new ArrayList<>(data.values());
    }

    @Override
    public Optional<Cita> findById(String id) {
        return Optional.ofNullable(data.get(id));
    }

    @Override
    public Cita save(Cita entity) {
        data.put(entity.getId(), entity);
        persist();
        return entity;
    }

    @Override
    public Cita update(Cita entity) {
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

