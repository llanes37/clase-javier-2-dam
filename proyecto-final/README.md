# Proyecto Final — Gestor de Cursos (Java 17, MVC, CSV, consola)

Este proyecto final consolida todo lo aprendido con una app realista que gestiona Alumnos, Cursos y Matrículas. Usa patrón MVC, persistencia en ficheros CSV, y se compila/ejecuta sin Maven/Gradle (scripts Windows). Incluye guía didáctica, comentarios enriquecidos (Better Comments) y un cuaderno de ejercicios.

## 🎯 Objetivos didácticos
- Repasar fundamentos: control de flujo, POO (clases, objetos, encapsulación), colecciones, enums, excepciones, validaciones (regex), fechas (LocalDate), IO (CSV), paquetes y arquitectura MVC.
- Practicar diseño por capas: Modelo, Repositorios (persistencia), Controladores (negocio) y Vista (consola).
- Trabajar con scripts de build/ejecución/packaging sin herramientas externas.

## 🧩 Arquitectura (alto nivel)
- Modelo (`model`): entidades puras (Alumno, Curso, Matricula) y enums (CursoTipo, EstadoMatricula).
- Persistencia (`repository` + `persistence`): almacenamiento en CSV con utilidades (`CsvUtils`, `FileStorage`).
- Negocio (`controller`): validaciones, reglas y orquestación.
- Presentación (`view`): consola simple con menús.

Flujo típico: Vista solicita acción → Controlador valida/orquesta → Repositorio persiste/recupera → Vista muestra resultado.

## 📁 Estructura de carpetas
- `src/com/curso/proyectofinal`  código fuente Java (paquetes por capa)
- `resources/data/`               ficheros CSV (se crean tras la primera ejecución)
- `bin/`                          clases compiladas (generadas por build)
- `build.bat`                     compilar todo el código
- `run.bat`                       ejecutar la aplicación
- `package.bat`                   generar JAR ejecutable
- `build.ps1`                     alternativa PowerShell
- `EJERCICIOS.md`                 prácticas guiadas por módulos (nuevo)

## 🚀 Cómo compilar y ejecutar
1. Compilar: doble clic en `build.bat` o ejecutarlo en terminal desde esta carpeta.
2. Ejecutar: doble clic en `run.bat` tras compilar. Aparece el menú principal.
3. Empaquetar (opcional): `package.bat` para crear `proyecto-final.jar` (ejecutable con doble clic o `java -jar proyecto-final.jar`).

Requisitos: JDK 17+ en PATH (java/javac/jar). Sistema: Windows (scripts .bat). PowerShell opcional: `build.ps1`.

## 🧾 Cómo ejecutar desde Visual Studio Code (VS Code)

Si trabajas con VS Code puedes compilar y lanzar la app directamente desde el editor.

- Requisitos en VS Code:
	- Instala la extensión "Extension Pack for Java" (o al menos "Language Support for Java" y "Debugger for Java").
	- Abre la carpeta del proyecto (`proyecto-final`) en VS Code.

- Opciones para ejecutar:
	1) Ejecutar la clase `Application` desde el editor:
		 - Abre `src/com/curso/proyectofinal/Application.java`.
		 - Verás un pequeño enlace "Run | Debug" arriba del método `main` (CodeLens) si tienes la extensión Java instalada; haz clic en "Run" para iniciar la app.
		 - Esto usa el classpath de VS Code y ejecuta el `main` directamente.

	2) Usar una configuración de depuración (`launch.json`):
		 - Crea la carpeta `.vscode` en la raíz del proyecto y añade un archivo `launch.json` con esta configuración mínima:

```json
{
	"version": "0.2.0",
	"configurations": [
		{
			"type": "java",
			"name": "Launch Application",
			"request": "launch",
			"mainClass": "com.curso.proyectofinal.Application",
			"projectName": "proyecto-final"
		}
	]
}
```

	- Después abre el panel de ejecución (Run) y lanza "Launch Application". Podrás depurar, poner breakpoints y ver la consola integrada.

 3) Usar el terminal integrado de VS Code (PowerShell):
		- Abre el terminal integrado (Terminal → New Terminal).
		- Ejecuta los scripts como en cualquier terminal Windows (ejemplos abajo).

> NOTA: Asegúrate de que el directorio de trabajo de la ejecución sea la raíz del proyecto (`proyecto-final`) para que `resources/data/` se resuelva correctamente.

## ▶️ Ejecutar con los scripts (.bat / PowerShell)

Puedes ejecutar los scripts tanto haciendo doble clic sobre ellos como desde PowerShell o CMD. Si trabajas desde VS Code usa el terminal integrado.

Ejemplos (PowerShell):

```powershell
# Compilar
.\build.bat

# Ejecutar (usa las clases compiladas)
.\run.bat

# Empaquetar en JAR
.\package.bat

# Alternativa: ejecutar el JAR si lo has empaquetado
java -jar proyecto-final.jar
```

Si prefieres PowerShell con la versión del script:

```powershell
# Usar el script de PowerShell (si quieres output más detallado o ejecutarlo en entornos con políticas de ejecución)
.\build.ps1
```

## 🧰 Consideraciones al ejecutar

- Al ejecutar desde VS Code con el debugger, la consola puede ser la integrada. Si la aplicación no encuentra los CSV en `resources/data`, verifica que el working directory sea la carpeta raíz del proyecto.
- Doble clic en `.bat` abre una consola separada; la ventana puede cerrarse al terminar. Para ver la salida, ejecuta desde una terminal abierta o añade una pausa al final del .bat.
- Si obtienes errores de Java (java/javac no encontrado), instala JDK 17+ y añade `bin` a la variable de entorno `PATH`.

## 🗃️ Persistencia y formato de datos (CSV)
Se guardan en `resources/data/` con separador `;` (valores con `;` se normalizan a `,`).

- `alumnos.csv`: `id;nombre;email;fechaNacimiento(yyyy-MM-dd|vacío)`
- `cursos.csv`: `id;nombre;tipo[ONLINE|PRESENCIAL];fechaInicio;fechaFin;precio`
- `matriculas.csv`: `id;alumnoId;cursoId;fechaMatricula;estado[ACTIVA|ANULADA|FINALIZADA]`

Carga: al iniciar cada repositorio. Guardado: al crear/actualizar/borrar.

## 🧠 Dominio y reglas clave
- Alumno: email único; fecha de nacimiento opcional.
- Curso: `precio >= 0`; `fechaFin >= fechaInicio`.
- Matrícula: fecha entre `[curso.inicio, curso.fin]` (inclusive). Estados: ACTIVA/ANULADA/FINALIZADA.

Validaciones centralizadas en `Validator` y `DateUtils`. Errores de negocio con `ValidationException`.

## 🧪 Casos de uso implementados
- Alumnos: listar, crear (id UUID, email único), borrar por id.
- Cursos: listar, crear (tipo, fechas, precio), borrar por id.
- Matrículas: listar, crear (alumnoId+cursoId+fecha opcional=HOY), anular.

## 🖥️ Interfaz (consola)
Menús navegables con entradas de texto. Métodos en `ConsoleView`: `title`, `line`, `prompt`, `pause`. Entrada robusta con defaults para números.

## 🔧 Scripts y tareas
- `build.bat`/`build.ps1`: compilan a `bin/` respetando paquetes.
- `run.bat`: ejecuta `com.curso.proyectofinal.Application`.
- `package.bat`: empaqueta en `proyecto-final.jar` con `Main-Class`.

## 🧰 Extensibilidad (ideas)
- Edición/actualización de entidades desde menú.
- Búsquedas y filtros (por email, por rango de fechas, por tipo de curso).
- Estadísticas: nº de matrículas por curso, importe total, etc.
- Exportación a otro formato (JSON) y tests unitarios.

## 📗 Guía didáctica y ejercicios
Este repo incluye comentarios enriquecidos usando la extensión “Better Comments” (// !, // ?, // *, // TODO) en todo el código. Para practicar, sigue el cuaderno de ejercicios: `EJERCICIOS.md`.

## 🛠️ Troubleshooting
- “No se encuentra java o javac”: revisa instalación de JDK y la variable PATH.
- Error de formato de fecha: usa `yyyy-MM-dd` (p.ej. 2025-10-26).
- CSV corrupto: borra la línea problemática o elimina el fichero para regenerarlo (perderás datos).

## 📦 Paquete principal y clase Main
- Paquete: `com.curso.proyectofinal`
- Clase principal: `Application`

— Disfruta construyendo. Lee los comentarios del código y completa los TODO marcados para afianzar conceptos —
