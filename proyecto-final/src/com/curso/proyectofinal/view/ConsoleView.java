package com.curso.proyectofinal.view;

import java.util.Scanner;

/*
 * ******************************************************************************************
 * 📘 ConsoleView — Vista de consola
 * Encapsula I/O por System.in/out. Métodos de utilidad para títulos, líneas y prompts.
 *
 * TODO Alumno
 * - [ ] Añadir confirm(String pregunta) que devuelva boolean.
 * - [ ] Añadir table(List<String[]> filas) para listar con columnas.
 * ******************************************************************************************
 */
/** Vista de consola: entrada/salida simple. */
public class ConsoleView {
    private final Scanner sc = new Scanner(System.in);

    public void title(String text) {
        System.out.println();
        System.out.println("== " + text + " ==");
    }

    public void line(String text) { System.out.println(text); }

    public String prompt(String label) {
        System.out.print(label + ": ");
        // * Leemos la línea completa y devolvemos trim().
        // ? Si necesitas un valor por defecto, añade otro método promptDefault.
        return sc.nextLine().trim();
    }

    public int promptInt(String label, int defaultValue) {
        System.out.print(label + " [" + defaultValue + "]: ");
        String s = sc.nextLine().trim();
        if (s.isEmpty()) return defaultValue;
        try { return Integer.parseInt(s); }
        catch (NumberFormatException e) { return defaultValue; }
    }

    public double promptDouble(String label, double defaultValue) {
        System.out.print(label + " [" + defaultValue + "]: ");
        String s = sc.nextLine().trim();
        if (s.isEmpty()) return defaultValue;
        try {
            // * Aceptamos coma como separador decimal y la normalizamos a punto para parseo.
            return Double.parseDouble(s.replace(",", "."));
        } catch (NumberFormatException e) {
            // ! Si la entrada no es válida, devolvemos el valor por defecto en lugar de lanzar.
            return defaultValue;
        }
    }

    public void pause() {
        System.out.print("Pulsa ENTER para continuar...");
        sc.nextLine();
    }
}
