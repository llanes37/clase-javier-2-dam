package com.curso.proyectofinal.persistence;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/*
 * ******************************************************************************************
 * 📘 FileStorage — IO utilitario de ficheros (UTF-8)
 * readAllLines(path) y writeLines(path, lines) con manejo de excepciones.
 *
 * TODO Alumno
 * - [ ] Añadir opción de append (writeLinesAppend).
 * - [ ] Manejar locking simple para evitar condiciones de carrera en escritura.
 * ******************************************************************************************
 */
/** Lectura/escritura de líneas en ficheros (UTF-8). */
public final class FileStorage {
    private FileStorage() {}

    public static List<String> readAllLines(Path path) {
        try {
            if (!Files.exists(path)) return new ArrayList<>();
            return Files.readAllLines(path, StandardCharsets.UTF_8);
        } catch (IOException e) {
            // ! Error de IO: encapsulamos como RuntimeException para simplificar el manejo en repositorios.
            // * En producción podrías usar una excepción checked o logging más fino.
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
            // ! Error de escritura: importante avisar claramente al usuario/operador.
            throw new RuntimeException("Error escribiendo fichero: " + path, e);
        }
    }
}
