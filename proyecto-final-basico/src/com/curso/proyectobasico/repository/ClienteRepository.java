package com.curso.proyectobasico.repository;

import com.curso.proyectobasico.model.Cliente;
import com.curso.proyectobasico.persistence.CsvUtils;
import com.curso.proyectobasico.persistence.FileStorage;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;

/*
 * Persistencia CSV de Cliente.
 * Fichero: resources/data/clientes.csv
 * Cabecera: id;nombre;email;telefono
 */
public class ClienteRepository implements Repository<Cliente> {
    private final Path file = Paths.get("resources", "data", "clientes.csv");
    private final Map<String, Cliente> data = new LinkedHashMap<>();

    public ClienteRepository() {
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
            String nombre = fields.get(1);
            String email = fields.size() > 2 ? fields.get(2) : "";
            String telefono = fields.size() > 3 ? fields.get(3) : "";
            data.put(id, new Cliente(id, nombre, email, telefono));
        }
    }

    private void persist() {
        List<String> lines = new ArrayList<>();
        lines.add("id;nombre;email;telefono");
        lines.addAll(data.values().stream()
                .map(c -> CsvUtils.toCsvLine(Arrays.asList(
                        c.getId(),
                        c.getNombre(),
                        c.getEmail() == null ? "" : c.getEmail(),
                        c.getTelefono() == null ? "" : c.getTelefono()
                )))
                .collect(Collectors.toList()));
        FileStorage.writeLines(file, lines);
    }

    @Override
    public List<Cliente> findAll() {
        return new ArrayList<>(data.values());
    }

    @Override
    public Optional<Cliente> findById(String id) {
        return Optional.ofNullable(data.get(id));
    }

    public Optional<Cliente> findByEmail(String email) {
        if (email == null || email.isBlank()) return Optional.empty();
        return data.values().stream()
                .filter(c -> email.equalsIgnoreCase(c.getEmail()))
                .findFirst();
    }

    @Override
    public Cliente save(Cliente entity) {
        data.put(entity.getId(), entity);
        persist();
        return entity;
    }

    @Override
    public Cliente update(Cliente entity) {
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

