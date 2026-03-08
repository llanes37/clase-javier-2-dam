package com.curso.proyectobasico.view;

import java.util.Scanner;

/*
 * Vista de consola simple: titulos, lineas y prompts.
 */
public class ConsoleView {
    private final Scanner scanner = new Scanner(System.in);

    public void title(String text) {
        System.out.println();
        System.out.println("== " + text + " ==");
    }

    public void line(String text) {
        System.out.println(text);
    }

    public String prompt(String label) {
        System.out.print(label + ": ");
        return scanner.nextLine().trim();
    }

    public void pause() {
        System.out.print("Pulsa ENTER para continuar...");
        scanner.nextLine();
    }
}

