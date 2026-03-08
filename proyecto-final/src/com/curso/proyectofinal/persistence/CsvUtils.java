package com.curso.proyectofinal.persistence;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

/*
 * ******************************************************************************************
 * 📘 CsvUtils — Utilidades CSV con separador ';'
 * - Reemplaza ';' en valores por ',' para mantener la integridad de columnas.
 * - toCsvLine(List<String>), parseCsvLine(String).
 *
 * TODO Alumno
 * - [ ] Soportar comillas dobles para valores con ';' (CSV RFC básico).
 * - [ ] Trim de campos al parsear.
 * ******************************************************************************************
 */
/** Utilidades simples para CSV con separador ';'. No soporta ';' en valores (se reemplaza por ','). */
public final class CsvUtils {
    private CsvUtils() {}

    public static String toCsvLine(List<String> fields) {
        return fields.stream()
                .map(v -> v == null ? "" : v.replace(";", ","))
                .collect(Collectors.joining(";"));
    }

    public static List<String> parseCsvLine(String line) {
        // * Simple split por ';'. No se soportan comillas ni escapes.
        // ? Si un valor contiene ';' se habrá reemplazado por ',' al guardarlo (toCsvLine).
        String[] arr = line.split(";");
        return Arrays.asList(arr);
    }
}
