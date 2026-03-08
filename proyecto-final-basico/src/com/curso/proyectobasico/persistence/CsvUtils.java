package com.curso.proyectobasico.persistence;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

/*
 * Utilidades simples para CSV con separador ';'.
 */
public final class CsvUtils {
    private CsvUtils() {
    }

    public static String toCsvLine(List<String> fields) {
        return fields.stream()
                .map(v -> v == null ? "" : v.replace(";", ","))
                .collect(Collectors.joining(";"));
    }

    public static List<String> parseCsvLine(String line) {
        String[] arr = line.split(";");
        return Arrays.asList(arr);
    }
}

