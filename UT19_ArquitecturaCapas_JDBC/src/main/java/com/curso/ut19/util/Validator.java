package com.curso.ut19.util;

/**
 * //! UTILIDADES DE VALIDACIÓN
 * ? Teoría: Centraliza validaciones reutilizables.
 */
public class Validator {
    public static boolean isNonEmpty(String s) { return s != null && !s.trim().isEmpty(); }
}
