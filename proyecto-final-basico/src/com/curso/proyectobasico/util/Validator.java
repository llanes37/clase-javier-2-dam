package com.curso.proyectobasico.util;

import java.util.regex.Pattern;

/*
 * Validaciones reutilizables: no vacio, email basico, numeros positivos.
 */
public final class Validator {
    private Validator() {
    }

    private static final Pattern EMAIL_REGEX = Pattern.compile(
            "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"
    );

    public static boolean isNullOrBlank(String s) {
        return s == null || s.trim().isEmpty();
    }

    public static void require(boolean condition, String message) {
        if (!condition) throw new IllegalArgumentException(message);
    }

    public static void requireNotBlank(String s, String fieldName) {
        if (isNullOrBlank(s)) {
            throw new IllegalArgumentException(fieldName + " no puede estar vacio");
        }
    }

    public static void requireEmail(String email) {
        if (isNullOrBlank(email)) return; // email opcional en este proyecto basico
        if (!EMAIL_REGEX.matcher(email).matches()) {
            throw new IllegalArgumentException("Email no valido");
        }
    }

    public static void requirePositive(double number, String fieldName) {
        if (number < 0) {
            throw new IllegalArgumentException(fieldName + " debe ser >= 0");
        }
    }
}

