package com.curso.proyectobasico.persistence;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/*
 * Lectura/escritura de lineas en ficheros (UTF-8).
 */
public final class FileStorage {
    private FileStorage() {
    }

    public static List<String> readAllLines(Path path) {
        try {
            if (!Files.exists(path)) return new ArrayList<>();
            return Files.readAllLines(path, StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new RuntimeException("Error leyendo fichero: " + path, e);
        }
    }

    public static void writeLines(Path path, List<String> lines) {
        try {
            if (path.getParent() != null && !Files.exists(path.getParent())) {
                Files.createDirectories(path.getParent());
            }
            Files.write(path, lines, StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new RuntimeException("Error escribiendo fichero: " + path, e);
        }
    }
}

