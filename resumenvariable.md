# Resumen de 01_variable.py

## Objetivo
Script didactico de Python para practicar:
- variables y f-strings
- entrada segura con `input`
- listas y diccionarios
- operadores
- mini laboratorio IA
- autoevaluacion final

## Configuracion general
- `RUN_INTERACTIVE`: activa/desactiva preguntas por consola.
- `PAUSE`: pausa entre opciones del menu.
- `IA_DEMO`: activa demo corta de laboratorio IA.

## Utilidades principales
- `print_firma()`: muestra autor y cabecera.
- `pause()`: pausa opcional.
- `safe_input(prompt, caster, default)`: lee y convierte entrada con valor por defecto si falla.
- `encabezado(titulo)`: imprime separadores de seccion.

## Secciones del contenido
1. `seccion_1()`
- Variables basicas (`str`, `int`, `float`, `bool`) y f-strings.
- Incluye TODO de perfil rapido.

2. `seccion_2()`
- Entrada segura + mini calculo de compra.
- Incluye TODO de conversion km -> millas.

3. `seccion_3()`
- Listas y diccionarios.
- Incluye ejercicio agenda (tareas y contacto).

4. `seccion_4()`
- Operadores aritmeticos, comparacion, logicos y asignacion.
- Incluye calculadora mini con control de division por cero.

5. `seccion_5_ia()`
- Guia para pedir a ChatGPT un mini programa.
- Demo opcional de marcador con listas y `sum`.

6. `autoevaluacion()`
- Ejercicio integrador con variables, entrada, colecciones y operadores.

## Menu principal
Funcion `menu()` con opciones:
- `1` a `6`: ejecutar cada seccion.
- `7`: ejecutar todo seguido.
- `0`: salir.

## Ejecucion
El script arranca con:
```python
if __name__ == "__main__":
    menu()
```
