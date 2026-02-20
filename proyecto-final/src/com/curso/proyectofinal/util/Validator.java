package com.curso.proyectofinal.util;

import java.util.regex.Pattern;

/*
 * ******************************************************************************************
 * 📘 Validator — Validaciones reutilizables
 * Email por regex, comprobaciones de no-vacío y positivos.
 *
 * TODO Alumno
 * - [ ] Añadir requireBetween(double n, double min, double max, String field).
 * - [ ] Añadir requireNotNull(Object o, String fieldName).
 * ******************************************************************************************
 */
/** Validaciones reutilizables. */
public final class Validator {
    private Validator() {}

    private static final Pattern EMAIL_REGEX = Pattern.compile(
            "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");

    public static boolean isNullOrBlank(String s) {
        return s == null || s.trim().isEmpty();
    }

    public static void require(boolean condition, String message) {
        if (!condition) throw new IllegalArgumentException(message);
    }

    public static void requireNotBlank(String s, String fieldName) {
        // ! Validación básica: lanzar IllegalArgumentException si cadena vacía o null.
        // * Los controladores capturan/transforman estas excepciones según convenga.
        if (isNullOrBlank(s)) throw new IllegalArgumentException(fieldName + " no puede estar vacío");
    }

    public static void requireEmail(String email) {
        // ? Validación por regex: cubre formatos comunes pero no todos los casos RFC.
        if (isNullOrBlank(email) || !EMAIL_REGEX.matcher(email).matches())
            throw new IllegalArgumentException("Email no válido");
    }

    public static void requirePositive(double number, String fieldName) {
        if (number < 0) throw new IllegalArgumentException(fieldName + " debe ser >= 0");
    }
}
