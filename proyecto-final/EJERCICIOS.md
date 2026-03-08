# Cuaderno de Ejercicios — Proyecto Final

Este cuaderno guía prácticas incrementales. Completa los TODO marcados en el código (Better Comments) y verifica que todo compila y corre.

## 🔧 Preparación
- Asegúrate de poder compilar (`build.bat`) y ejecutar (`run.bat`).
- Explora el código y lee los encabezados didácticos de cada clase.

## 🟢 Nivel 1 — Fundamentos (Modelo/Repos)
1) Modelo: `Alumno`, `Curso`, `Matricula`
   - [ ] Añade validaciones ligeras en setters (p.ej., `nombre` no vacío) solo si no rompen tests actuales.
   - [ ] Implementa `toString()` más legible (ya existe una base; mejóralo si quieres).
2) Repositorios CSV
   - [ ] Añade método `count()` a `Repository` y a las implementaciones.
   - [ ] En `AlumnoRepository`, implementa `findByNombreContains(String texto)` (case-insensitive).
   - [ ] En `CursoRepository`, implementa `findByTipo(CursoTipo tipo)`.
   - [ ] En `MatriculaRepository`, implementa `existsByAlumnoAndCurso(String alumnoId, String cursoId)`.

## ➕ Extensiones del Nivel 1 (más ejercicios)
- [ ] Añade `deleteAll()` en repositorios para poder resetear datos desde pruebas manuales.
- [ ] Implementa `findAllPaged(int page, int size)` en repositorios (retorna sublista paginada).
- [ ] Añade un dataset de ejemplo (ver sección "Dataset de ejemplo" abajo) y un script small para rellenar `resources/data` si no existe.

## 🟡 Nivel 2 — Negocio (Controladores)

## 🟡 Nivel 2 — Negocio (Controladores)
3) Alumnos
   - [ ] Evita duplicados por email (ya implementado en crear). Añade TODO: actualizar nombre por id.
4) Cursos
   - [ ] Valida que `precio >= 0` (ya está) y que la duración no sea superior a 365 días (añade una regla opcional).
   - [ ] Añade caso de uso: listar cursos por tipo (ONLINE/PRESENCIAL).
5) Matrículas

## ➕ Extensiones del Nivel 2 (más ejercicios)
- [ ] Implementa actualización parcial (PATCH) en controladores: `actualizarNombreAlumno(id, nuevoNombre)` y `actualizarPrecioCurso(id, nuevoPrecio)`.
- [ ] Añade control de integridad: no permitir borrar un curso que tenga matrículas activas (o pedir confirmación y anularlas antes).
- [ ] Añade excepciones de negocio más ricas: `BusinessException` con códigos y usa mensajes localizables.

## 🔵 Nivel 3 — Vista (Consola)
   - [ ] Impide matricular dos veces al mismo alumno en el mismo curso (usa tu `existsByAlumnoAndCurso`).
   - [ ] Añade transición a `FINALIZADA` si la fecha actual es posterior a fin del curso (método nuevo).

## 🔵 Nivel 3 — Vista (Consola)
6) Menús y entradas
   - [ ] Añade opción en menús para las nuevas funcionalidades de Nivel 2.

## ➕ Extensiones del Nivel 3 (más ejercicios)
- [ ] Implementa `ConsoleView.confirm(String pregunta)` que devuelva boolean y úsalo al borrar.
- [ ] Crea un comando `exportar <entidad>` que exporte a `exports/` (CSV) lo que hay en memoria.
- [ ] Mejora la presentación: implementa `ConsoleView.table(String[] headers, List<String[]> rows)` para mostrar tablas.

## 🟣 Nivel 4 — Extras (Extensión técnica)
   - [ ] Añade confirmación al borrar entidades.
7) UX
   - [ ] Muestra listados con columnas alineadas (usa `String.format`).
   - [ ] Añade paginación opcional (tamaño configurable).

## 🟣 Nivel 4 — Extras (Extensión técnica)
8) Persistencia

## ➕ Extensiones del Nivel 4 (avanzado)
- [ ] Añade pruebas unitarias con JUnit 5 para controladores y utilidades (ej.: `DateUtils`, `Validator`).
- [ ] Añade un pipeline simple de GitHub Actions que compile y ejecute los builds (sin tests obligatorios al principio).
- [ ] Refactoriza la persistencia para soportar un repositorio en memoria + otro CSV (usa una fábrica/factory para intercambiar implementaciones).
- [ ] Añade un pequeño módulo de importación de CSV con detección y reporte de líneas inválidas.

## ✅ Criterios de aceptación (por módulo)
- Compila sin errores. Menús siguen funcionando.
- Reglas de negocio nuevas probadas manualmente desde la consola.
- CSVs mantienen cabeceras y formato correcto.

## 🧪 Cómo probar
- Usa datos mínimos: crea 1-2 alumnos, 1-2 cursos, 1-2 matrículas.
- Prueba errores: fechas inválidas, emails inválidos, y duplicados.
- Revisa que no se generan duplicados en CSV ni líneas vacías.

## 📝 Entregables
- Código modificado con TODOs resueltos (marca tus cambios con `// DONE:` cuando acabes una tarea).
- Capturas de consola mostrando resultados de cada funcionalidad.

## 🧭 Guía rápida por archivos (qué editar para cada ejercicio)
- `src/.../model/*.java` — Validaciones ligeras, helpers (getEdad, getDuracionDias).
- `src/.../repository/*Repository.java` — Añadir count(), deleteAll(), búsquedas y paginación.
- `src/.../controller/*Controller.java` — Reglas de negocio, evitar duplicados, actualizar campos.
- `src/.../persistence/*` — Mejora de CSV parsing y write append/locking.
- `src/.../view/ConsoleView.java` — Agregar confirm(), table(), prompt mejorados.

## 💡 Hints y pistas (por tarea)
- Implementar `count()` → devuelve `data.size()` en repositorios y actualizar la interfaz `Repository`.
- `findByNombreContains`: usa `toLowerCase().contains(...)` sobre `getNombre()`.
- `existsByAlumnoAndCurso`: recorre `data.values()` en `MatriculaRepository` y compara ambos ids.
- `findAllPaged`: calcula índices `from = page*size` y `to = Math.min(from+size, total)`.

## ⏱️ Estimaciones (orientativas)
- Nivel 1: 1–3 horas.
- Nivel 2: 2–6 horas (dependiendo de reglas adicionales).
- Nivel 3: 2–5 horas (si mejoras UI en consola).
- Nivel 4: 4–12 horas (tests/CI/refactor). 

## 📁 Dataset de ejemplo (pega en `resources/data/*.csv` si quieres empezar rápido)

alumnos.csv
```
id;nombre;email;fechaNacimiento
1;Ana Pérez;ana.perez@example.com;1990-05-12
2;Luis Gómez;luis.gomez@example.com;1985-11-03
```

cursos.csv
```
id;nombre;tipo;fechaInicio;fechaFin;precio
1;Java Básico;ONLINE;2025-11-01;2025-12-15;120.0
2;Introducción a Swing;PRESENCIAL;2025-09-01;2025-09-30;200.0
```

matriculas.csv
```
id;alumnoId;cursoId;fechaMatricula;estado
1;1;1;2025-10-20;ACTIVA
2;2;2;2025-09-05;ACTIVA
```

## ✅ Sugerencia de flujo de trabajo para completar ejercicios
1. Crea una rama feature/ejericios-N donde N sea el número del ejercicio.
2. Implementa y añade tests mínimos (si procede).
3. Compila con `build.bat` y ejecuta `run.bat`.
4. Documenta cambios y marca `// DONE:` en los archivos editados.

## 🏁 Finaliza con entrega
- Genera un ZIP con las fuentes modificadas y los CSV de ejemplo.
- Añade un pequeño README-resumen indicando: qué se hizo, cómo probar y capturas.

¡Avanza por niveles y pregunta cualquier duda!
   - [ ] Exporta listados a CSV independiente (carpeta `exports/`).
   - [ ] Añade bloqueo simple de escritura para evitar corrupción en concurrencia (sin hilos, simulado).
9) Utilidades
   - [ ] Añade `DateUtils.isBetweenInclusive(LocalDate d, LocalDate ini, LocalDate fin)` y úsalos en controladores.
10) Calidad
   - [ ] Añade logs simples con niveles (INFO/ERROR) usando `System.out` y `System.err` en puntos clave.

## ✅ Criterios de aceptación (por módulo)
- Compila sin errores. Menús siguen funcionando.
- Reglas de negocio nuevas probadas manualmente desde la consola.
- CSVs mantienen cabeceras y formato correcto.

## 🧪 Cómo probar
- Usa datos mínimos: crea 1-2 alumnos, 1-2 cursos, 1-2 matrículas.
- Prueba errores: fechas inválidas, emails inválidos, y duplicados.
- Revisa que no se generan duplicados en CSV ni líneas vacías.

## 📝 Entregables
- Código modificado con TODOs resueltos (marca tus cambios con `// DONE:` cuando acabes una tarea).
- Capturas de consola mostrando resultados de cada funcionalidad.

¡Avanza por niveles y pregunta cualquier duda! 