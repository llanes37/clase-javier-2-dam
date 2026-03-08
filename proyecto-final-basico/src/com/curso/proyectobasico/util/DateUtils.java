package com.curso.proyectobasico.util;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;

/*
 * Utilidades de fechas para formato yyyy-MM-dd.
 */
public final class DateUtils {
    private DateUtils() {
    }

    public static final DateTimeFormatter FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd");

    public static LocalDate parse(String s) {
        try {
            return LocalDate.parse(s, FMT);
        } catch (DateTimeParseException e) {
            throw new IllegalArgumentException("Fecha invalida, usa yyyy-MM-dd");
        }
    }

    public static String format(LocalDate d) {
        return d != null ? d.format(FMT) : "";
    }
}

