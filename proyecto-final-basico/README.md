# 📚 Proyecto Final Básico — Agenda de Citas (Java 17, MVC, CSV, Consola)

> **Proyecto didáctico** que gestiona Clientes y Citas para un pequeño negocio  
> (peluquería, consulta, estética, etc.) con patrón MVC, persistencia CSV y consola.  
> Pensado como **escalón previo** al proyecto completo (Gestor de Cursos).  
> Incluye comentarios Better Comments y cuaderno de 10 ejercicios con prompts para IA.  
> **Autor:** Joaquín Rodríguez Llanes | Uso educativo exclusivo.

---

## 🚀 Arranque rápido

```bash
# 1. Compilar (genera clases en bin/)
build.bat

# 2. Ejecutar
run.bat

# 3. Empaquetar (opcional)
package.bat
java -jar proyecto-final-basico.jar
```

> 💡 **Requisito:** JDK 17+ instalado y en PATH (`java -version` / `javac -version`).  
> Alternativa PowerShell: `.\build.ps1`

### Ejecutar desde VS Code
1. Instala la extensión **"Extension Pack for Java"**.
2. Abre la carpeta `proyecto-final-basico` en VS Code.
3. Abre `Application.java` → clic en **"Run"** (CodeLens encima de `main`).

> ⚠️ El directorio de trabajo debe ser `proyecto-final-basico/` para que `resources/data/` se resuelva bien.

---

## 🏗️ Arquitectura por capas (MVC)

```
Menú de consola (usuario)
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│  📁 view/  (Capa de PRESENTACIÓN)                        │
│  ConsoleView.java → title(), line(), prompt(), pause()   │
│  Application.java → menús y flujo de navegación          │
└────────────────────────┬────────────────────────────────┘
                         │ delega lógica
                         ▼
┌─────────────────────────────────────────────────────────┐
│  📁 controller/  (Capa de NEGOCIO)  ← AQUÍ van reglas   │
│  ClienteController → nombre obligatorio, email único     │
│  CitaController    → cliente existe, parseo de fecha     │
└────────────────────────┬────────────────────────────────┘
                         │ acceso a datos
                         ▼
┌─────────────────────────────────────────────────────────┐
│  📁 repository/  (Capa de DATOS)                         │
│  CRUD genérico: save, findById, findAll, update, delete  │
│  Delega lectura/escritura CSV a persistence/             │
└────────────────────────┬────────────────────────────────┘
                         │ ficheros CSV
                         ▼
┌─────────────────────────────────────────────────────────┐
│  📁 model/  (Entidades puras)                            │
│  Cliente, Cita, EstadoCita (enum)                        │
└────────────────────────┬────────────────────────────────┘
                         │ serialización
                         ▼
              resources/data/*.csv
```

**🔑 Regla de oro:** si no sabes dónde va una regla, la respuesta es **`controller`**.

---

## 📏 Reglas de negocio implementadas

| # | Regla | Dónde vive |
|---|---|---|
| 1 | Nombre de cliente obligatorio (no vacío) | `ClienteController` |
| 2 | Email del cliente con formato válido | `ClienteController` + `Validator` |
| 3 | Email del cliente único (case-insensitive) | `ClienteController` |
| 4 | El cliente debe existir para crear una cita | `CitaController` |
| 5 | Fecha de cita con formato válido (yyyy-MM-dd) | `CitaController` + `DateUtils` |
| 6 | Cambio de estado: PENDIENTE → REALIZADA | `CitaController` |

> ⚠️ **TODOs en el código:** estado CANCELADA, confirmación antes de borrar, filtros → ver `EJERCICIOS.md`.

---

## 🗃️ Persistencia y formato CSV

Los datos se guardan en `resources/data/` con separador `;`:

| Fichero | Columnas |
|---|---|
| `clientes.csv` | `id;nombre;email;telefono` |
| `citas.csv` | `id;clienteId;fecha;estado;descripcion` |

- **Carga:** al iniciar cada repositorio.
- **Guardado:** al crear, actualizar o borrar.
- `fecha` en formato `yyyy-MM-dd`. Campos nulos → cadena vacía.
- Si borras un CSV, se regenera vacío al siguiente arranque.

---

## 📂 Estructura de carpetas

```
proyecto-final-basico/
├── src/com/curso/proyectobasico/
│   ├── Application.java         ← punto de entrada + menús
│   ├── controller/              ← reglas de negocio
│   │   ├── ClienteController.java
│   │   └── CitaController.java
│   ├── exception/               ← excepciones de dominio
│   │   └── ValidationException.java
│   ├── model/                   ← entidades + enums
│   │   ├── Cliente.java
│   │   ├── Cita.java
│   │   └── EstadoCita.java
│   ├── persistence/             ← utilidades CSV
│   │   ├── CsvUtils.java
│   │   └── FileStorage.java
│   ├── repository/              ← acceso a datos
│   │   ├── Repository.java      (interfaz genérica)
│   │   ├── ClienteRepository.java
│   │   └── CitaRepository.java
│   ├── util/                    ← utilidades comunes
│   │   ├── DateUtils.java
│   │   └── Validator.java
│   └── view/                    ← interfaz de consola
│       └── ConsoleView.java
├── resources/data/              ← CSV generados al ejecutar
├── bin/                         ← clases compiladas
├── EJERCICIOS.md                ← 10 ejercicios con prompts IA
├── README.md                    ← este archivo
├── build.bat                    ← compilar
├── build.ps1                    ← compilar (PowerShell)
├── run.bat                      ← ejecutar
└── package.bat                  ← generar JAR
```

---

## 🎨 Better Comments (colores en VS Code)

Instala **`aaron-bond.better-comments`** en VS Code:

| Prefijo | Color | Significado |
|---|---|---|
| `// *` | 🟢 Verde | Explicación de flujo, responsabilidad |
| `// ?` | 🔵 Azul | Justificación técnica, decisión de diseño |
| `// !` | 🔴 Rojo | Regla crítica, advertencia |
| `// TODO` | 🟠 Naranja | Mejora pendiente, ejercicio para el alumno |

---

## 📖 Cómo estudiar este proyecto

**Ruta de lectura recomendada (de menor a mayor complejidad):**

| Orden | Archivo | Qué aprendes |
|---|---|---|
| 1️⃣ | `model/Cliente.java` | Clase POJO simple, encapsulación, toString |
| 2️⃣ | `model/EstadoCita.java` | Qué es un enum y por qué es mejor que un String |
| 3️⃣ | `model/Cita.java` | Relación entre entidades (clienteId) |
| 4️⃣ | `view/ConsoleView.java` | Separación de la presentación |
| 5️⃣ | `controller/ClienteController.java` | Validación, email único, UUID |
| 6️⃣ | `controller/CitaController.java` | Validación cruzada (cliente existe), cambio de estado |
| 7️⃣ | `repository/ClienteRepository.java` | Persistencia CSV, serialización |
| 8️⃣ | `persistence/CsvUtils.java` | Lectura/escritura de ficheros |
| 9️⃣ | `Application.java` | Menús, flujo completo, wiring manual |
| 🔟 | `EJERCICIOS.md` | Practicar todo lo aprendido |

### 🧠 Preguntas didácticas clave
- ¿Qué regla debe vivir en el Controller y cuál en el Repository?
- ¿Qué ventaja tiene UUID sobre un contador incremental?
- ¿Qué se rompe si movemos la validación de email único a Application.java?
- ¿Por qué separamos ConsoleView de Application?

---

## 🔗 Relación con los otros proyectos

| Proyecto | Nivel | Dominio | Persistencia |
|---|---|---|---|
| **proyecto-final-basico** (este) | ⭐ Básico | Clientes + Citas | CSV |
| proyecto-final | ⭐⭐ Intermedio | Alumnos + Cursos + Matrículas | CSV |
| proyecto-final-sqlite-thymeleaf-jpa | ⭐⭐⭐ Avanzado | Alumnos + Cursos + Matrículas | SQLite + JPA + Web |

> 💡 La progresión natural es: **básico → final → sqlite-thymeleaf-jpa**.

---

## ❓ Problemas frecuentes

| Problema | Solución |
|---|---|
| `java` o `javac` no encontrados | Instala JDK 17+ y añade `bin/` a PATH |
| Error de formato de fecha | Usa formato `yyyy-MM-dd` (ej: `2025-10-26`) |
| CSV corrupto | Borra el fichero y reinicia (se regenera vacío) |
| La ventana .bat se cierra | Ejecuta desde terminal abierta |
| Desde VS Code no encuentra CSV | Working directory = `proyecto-final-basico/` |
