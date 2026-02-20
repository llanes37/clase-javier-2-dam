package com.curso.proyectofinal.util;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;

/*
 * ******************************************************************************************
 * 📘 DateUtils — Utilidades de fechas (yyyy-MM-dd)
 * parse(String) con validación y format(LocalDate).
 *
 * TODO Alumno
 * - [ ] Añadir isBetweenInclusive(LocalDate d, LocalDate ini, LocalDate fin).
 * - [ ] Añadir parseOrNull(String s) para campos opcionales.
 * ******************************************************************************************
 */
/** Fechas comunes: parseo y formato yyyy-MM-dd. */
public final class DateUtils {
    private DateUtils() {}

    public static final DateTimeFormatter FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd");

    public static LocalDate parse(String s) {
        try {
            return LocalDate.parse(s, FMT);
        } catch (DateTimeParseException e) {
            // ! Lanzamos IllegalArgumentException con mensaje claro para el usuario/console.
            throw new IllegalArgumentException("Fecha inválida, usa yyyy-MM-dd");
        }
    }

    public static String format(LocalDate d) {
        return d != null ? d.format(FMT) : "";
    }
}
