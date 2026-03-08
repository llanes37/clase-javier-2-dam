# 🏋️ EJERCICIOS PRÁCTICOS — Proyecto Final Básico (Agenda de Citas)

> **Autor:** Joaquín Rodríguez Llanes  
> **Nivel:** Java Básico–Intermedio (sin frameworks)  
> **Tiempo total estimado:** 5–7 horas  
> **Prerrequisitos:** Java 17, compilación desde línea de comandos, conceptos básicos de POO.

> 💡 **Cómo usar estos ejercicios:**  
> Cada ejercicio incluye un **análisis técnico** que explica QUÉ hay que hacer, POR QUÉ y EN QUÉ ARCHIVOS.  
> Al final de cada uno hay una **📋 Cajita de Prompt** lista para copiar y enviar a una IA  
> (Gemini, ChatGPT, etc.) si quieres que lo implemente automáticamente.  
> **Recomendación:** intenta hacerlo tú primero. Si te atascas, usa el prompt.

---

## 📋 Índice de Ejercicios

| # | Ejercicio | Nivel | Tiempo | Capas que toca |
|---|-----------|-------|--------|----------------|
| 1 | Ejecutar, explorar y crear datos | ⭐ Básico | 15 min | Todas (lectura) |
| 2 | Entender el patrón MVC en consola | ⭐ Básico | 20 min | Todas (lectura) |
| 3 | Añadir campo `direccion` al Cliente | ⭐⭐ Intermedio | 40 min | Model → Repository → Controller → Application |
| 4 | Buscar clientes por nombre parcial | ⭐⭐ Intermedio | 30 min | Controller → Application |
| 5 | Confirmación S/N antes de borrar | ⭐ Básico | 20 min | View → Application |
| 6 | Marcar cita como CANCELADA (nuevo estado) | ⭐⭐ Intermedio | 30 min | Model → Controller → Application |
| 7 | Filtrar citas por estado (PENDIENTE/REALIZADA) | ⭐⭐ Intermedio | 30 min | Controller → Application |
| 8 | Mostrar nombre del cliente en el listado de citas | ⭐⭐ Intermedio | 30 min | Application |
| 9 | Editar teléfono de un cliente | ⭐⭐ Intermedio | 30 min | Controller → Repository → Application |
| 10 | Exportar informe completo a fichero .txt | ⭐⭐⭐ Avanzado | 45 min | Application |

---

## ⭐ EJERCICIO 1 — Ejecutar y explorar (básico)

### 🎯 Objetivo
Familiarizarte con la app, crear datos de prueba y entender cómo se persisten en CSV.

### ✅ Pasos
1. Compila el proyecto con `build.bat` (doble clic o desde terminal).
2. Ejecuta con `run.bat`. Aparecerá el menú principal.
3. Crea **2 clientes** y **3 citas** (una para cada cliente y una extra).
4. Marca una cita como **REALIZADA**.
5. Cierra la app y vuelve a abrirla. ¿Se conservan los datos?
6. Abre `resources/data/` y examina los ficheros CSV generados.

### 🧠 Preguntas para responder
1. ¿Dónde se guardan los datos? *(pista: busca ficheros `.csv` en `resources/data/`)*
2. ¿Qué pasa si borras el fichero CSV de clientes y reinicias la app?
3. ¿Qué formato tiene cada línea del CSV? ¿Qué separador usa?
4. ¿Qué es el campo `id` que aparece en cada registro? *(pista: UUID)*
5. ¿Cuántos estados tiene una cita? ¿Dónde se definen?

---

## ⭐ EJERCICIO 2 — Entender el patrón MVC (básico)

### 🎯 Objetivo
Trazar el flujo de una operación **desde el menú hasta el fichero CSV** y entender la separación de capas.

### ✅ Pasos
1. Sigue el flujo de **"Crear cliente"** paso a paso:
   - `Application.java` → lee nombre, email y teléfono del usuario
   - `ClienteController.crear()` → valida datos y crea el objeto
   - `ClienteRepository.save()` → escribe la línea en el fichero CSV
2. Dibuja un diagrama en papel con flechas mostrando las llamadas entre clases.

### 🧠 Preguntas para responder
1. ¿En qué clase se valida que el email sea único? ¿Controller, Repository o Application?
2. ¿En qué clase se escribe al fichero CSV?
3. ¿Qué pasaría si pusiéramos la validación del email en el Repository?
4. ¿Por qué el Controller recibe el Repository por constructor en vez de crearlo él mismo?
5. ¿Qué patrón de diseño sigue este proyecto? *(pista: 3 letras)*

---

## ⭐⭐ EJERCICIO 3 — Añadir campo `direccion` al Cliente (intermedio)

### 🎯 Objetivo
Practicar el **ciclo completo** de añadir un campo: modelo → repositorio → controller → menú.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Model** | `Cliente.java` | Añadir campo `direccion` (String), actualizar constructor, getter/setter, toString |
| **Repository** | `ClienteRepository.java` | Actualizar serialización/deserialización CSV (5º campo) |
| **Controller** | `ClienteController.java` | Actualizar `crear()` para recibir y guardar `direccion` |
| **Application** | `Application.java` | Pedir dirección al usuario (campo opcional) |

### 🧠 Decisiones de diseño
- La dirección es **opcional** → si el usuario pulsa ENTER vacío, se guarda como cadena vacía `""`.
- En el CSV, se añade como **5º campo** (índice 4). Ejemplo: `uuid;Ana;ana@mail.com;612345678;Calle Mayor 1`.
- **Compatibilidad hacia atrás:** el CSV antiguo solo tiene 4 campos. Al leer, si la línea tiene solo 4 campos, la dirección se asume vacía.
- El campo NO necesita validación (es texto libre opcional).

### ⚠️ Errores comunes
- Olvidar actualizar `toString()` → la dirección no aparece al listar.
- No gestionar CSV antiguo (4 campos) → `ArrayIndexOutOfBoundsException` al leer datos existentes.
- Olvidar actualizar la serialización de escritura → la dirección se pierde al guardar.

### 📋 Prompt para la IA
> ```
> En mi proyecto Java MVC "proyecto-final-basico" (Agenda de Citas), necesito
> añadir un campo opcional "direccion" (String) al Cliente.
>
> Arquitectura: Application.java (vista+menús) → *Controller.java (negocio) → *Repository.java (CSV)
>
> Archivos a modificar:
> - src/com/curso/proyectobasico/model/Cliente.java
>   → añadir campo direccion con getter/setter, actualizar constructor y toString()
> - src/com/curso/proyectobasico/repository/ClienteRepository.java
>   → actualizar serialización CSV: escribir dirección como 5º campo con ;
>   → actualizar deserialización: leer 5º campo si existe, sino asumir vacío
>     (compatibilidad con CSV antiguos de 4 campos)
> - src/com/curso/proyectobasico/controller/ClienteController.java
>   → actualizar crear() para recibir String direccion y pasarlo al constructor
> - src/com/curso/proyectobasico/Application.java
>   → pedir dirección al usuario (opcional, ENTER para omitir)
>
> Usa el mismo estilo de comentarios Better Comments del proyecto (// *, // ?, // !, // TODO).
> ```

---

## ⭐⭐ EJERCICIO 4 — Buscar clientes por nombre parcial (intermedio)

### 🎯 Objetivo
Añadir una **búsqueda por nombre parcial** al menú de clientes usando Streams.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Controller** | `ClienteController.java` | Crear `buscarPorNombre(String texto)` con Streams + filter |
| **Application** | `Application.java` | Añadir opción "4) Buscar por nombre" al menú de clientes |

### 🧠 Decisiones de diseño
- La búsqueda es **case-insensitive** → convertimos ambos a lowercase antes de comparar.
- Se usa `String.contains()` para búsqueda parcial → "ana" encuentra "Ana María" y "Mariana".
- Si no hay resultados, se muestra un mensaje informativo (no un error).
- El filtrado va en el **Controller** (es lógica de negocio, no de presentación).

### 📋 Prompt para la IA
> ```
> En mi proyecto Java MVC "proyecto-final-basico", necesito una búsqueda de
> clientes por nombre parcial (case-insensitive) en el menú de clientes.
>
> Archivos a modificar:
> - src/com/curso/proyectobasico/controller/ClienteController.java
>   → crear buscarPorNombre(String texto) que:
>     1) Obtiene todos los clientes con repo.findAll()
>     2) Filtra con .stream().filter() donde nombre.toLowerCase() contiene texto.toLowerCase()
>     3) Retorna la lista filtrada (.toList())
> - src/com/curso/proyectobasico/Application.java
>   → añadir opción "4) Buscar por nombre" al menú de clientes
>   → pedir texto, llamar al controller, mostrar resultados o "No encontrado"
>
> Usa estilo Better Comments.
> ```

---

## ⭐ EJERCICIO 5 — Confirmación S/N antes de borrar (básico)

### 🎯 Objetivo
Pedir confirmación al usuario **antes de borrar** un cliente o una cita.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **View** | `ConsoleView.java` | Crear método `confirmar(String pregunta)` que devuelve `boolean` |
| **Application** | `Application.java` | Llamar a `confirmar()` antes de ejecutar `borrar()` |

### 🧠 Decisiones de diseño
- El método `confirmar()` va en `ConsoleView` porque es **lógica de presentación** (no de negocio).
- Se reutiliza el mismo método en clientes y citas (principio DRY).
- Acepta "S", "s", "SI", "si" como afirmativo → `"S".equalsIgnoreCase(respuesta)`.
- Cualquier otra respuesta se interpreta como cancelación.
- **NO** se modifica ningún Controller → la capa de negocio no cambia.

### 📋 Prompt para la IA
> ```
> En mi proyecto Java MVC "proyecto-final-basico", necesito confirmación S/N
> antes de borrar clientes, citas o anular citas.
>
> Archivos a modificar:
> - src/com/curso/proyectobasico/view/ConsoleView.java
>   → crear método confirmar(String pregunta) que:
>     1) Imprime la pregunta + " (S/N): "
>     2) Lee la respuesta con scanner.nextLine().trim()
>     3) Retorna "S".equalsIgnoreCase(respuesta)
> - src/com/curso/proyectobasico/Application.java
>   → en los métodos de borrar cliente y borrar/anular cita:
>     si !view.confirmar("¿Seguro?") → mostrar "Operación cancelada" y return
>
> No modificar Controllers. Estilo Better Comments.
> ```

---

## ⭐⭐ EJERCICIO 6 — Estado CANCELADA para citas (intermedio)

### 🎯 Objetivo
Añadir un **tercer estado** (`CANCELADA`) al enum y un método para **cancelar citas** con reglas.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Model** | `EstadoCita.java` | Añadir valor `CANCELADA` al enum |
| **Controller** | `CitaController.java` | Crear método `cancelar(String citaId)` con validaciones |
| **Application** | `Application.java` | Añadir opción "5) Cancelar cita" al menú |

### 🧠 Decisiones de diseño
- **Regla de transición:** solo se puede cancelar una cita **PENDIENTE**.
  - Si ya está REALIZADA → `ValidationException("No se puede cancelar una cita ya realizada")`.
  - Si ya está CANCELADA → `ValidationException("La cita ya está cancelada")`.
- Se usa `Optional.map()` para encadenar la búsqueda y la acción.
- El CSV no cambia de estructura → `CANCELADA` se guarda como texto en la columna de estado.

### 📋 Prompt para la IA
> ```
> En mi proyecto Java MVC "proyecto-final-basico", necesito añadir el estado
> CANCELADA a las citas y un método para cancelarlas con validaciones.
>
> Archivos a modificar:
> - src/com/curso/proyectobasico/model/EstadoCita.java
>   → añadir CANCELADA al enum (después de REALIZADA)
> - src/com/curso/proyectobasico/controller/CitaController.java
>   → crear cancelar(String citaId) que:
>     1) Busca la cita con repo.findById() + orElseThrow
>     2) Si estado es REALIZADA → lanza ValidationException (no se puede cancelar)
>     3) Si estado es CANCELADA → lanza ValidationException (ya cancelada)
>     4) Si estado es PENDIENTE → cambia a CANCELADA, repo.update(), retorna true
> - src/com/curso/proyectobasico/Application.java
>   → añadir opción "5) Cancelar cita" al menú de citas
>
> Usa estilo Better Comments y ValidationException para los errores.
> ```

---

## ⭐⭐ EJERCICIO 7 — Filtrar citas por estado (intermedio)

### 🎯 Objetivo
Poder ver **solo las citas PENDIENTES**, solo las REALIZADAS, etc.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Controller** | `CitaController.java` | Crear `listarPorEstado(EstadoCita estado)` con Streams |
| **Application** | `Application.java` | Añadir opciones "6) Ver PENDIENTES" y "7) Ver REALIZADAS" |

### 🧠 Decisiones de diseño
- Se usa `repo.findAll().stream().filter(c -> c.getEstado() == estado).toList()`.
- La comparación de enums usa `==` (no `.equals()`) porque los enums son **singletons** en Java.
- El filtrado va en el **Controller** (lógica de negocio).
- Se reutiliza el método de mostrar citas de Application (DRY).

### 📋 Prompt para la IA
> ```
> En mi proyecto Java MVC "proyecto-final-basico", necesito filtrar citas por
> estado en el menú de citas.
>
> Archivos a modificar:
> - src/com/curso/proyectobasico/controller/CitaController.java
>   → crear listarPorEstado(EstadoCita estado) con Streams + filter
>   → comparar enums con == (no .equals())
> - src/com/curso/proyectobasico/Application.java
>   → añadir opciones al menú: "6) Ver PENDIENTES" y "7) Ver REALIZADAS"
>   → reutilizar el formato de listado existente
>
> Usa estilo Better Comments.
> ```

---

## ⭐⭐ EJERCICIO 8 — Mostrar nombre del cliente en citas (intermedio)

### 🎯 Objetivo
Que el listado de citas muestre el **nombre del cliente** en vez de solo el UUID.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Application** | `Application.java` | Modificar el método que lista citas para resolver nombres |

### 🧠 Decisiones de diseño
- La cita almacena `clienteId` (UUID). Para mostrar el nombre, hay que buscar el cliente en su repositorio.
- Se usa `clienteCtl.listar()` o directamente el repo para buscar por ID.
- Si el cliente fue borrado → mostrar `"(cliente eliminado)"` en vez del nombre.
- **NO** se modifica el Model ni el Controller → es lógica de presentación.

### ⚠️ Errores comunes
- No contemplar el caso de cliente borrado → `NullPointerException`.
- Hacer la búsqueda dentro del `toString()` de Cita → acopla el modelo al repositorio.

### 📋 Prompt para la IA
> ```
> En mi proyecto Java MVC "proyecto-final-basico", necesito que el listado de
> citas muestre el nombre del cliente en vez de solo el UUID.
>
> Archivo a modificar:
> - src/com/curso/proyectobasico/Application.java
>   → en el método que lista citas, para cada cita:
>     1) Buscar el cliente por cita.getClienteId() usando el clienteController o repo
>     2) Si existe: mostrar cliente.getNombre()
>     3) Si no existe (fue borrado): mostrar "(cliente eliminado)"
>   → Formato sugerido: "Fecha | Nombre Cliente | Estado | Descripción"
>
> NO modificar el Model ni el Controller. Estilo Better Comments.
> ```

---

## ⭐⭐ EJERCICIO 9 — Editar teléfono de un cliente (intermedio)

### 🎯 Objetivo
Implementar una **actualización parcial** (solo el teléfono) en el flujo MVC.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Controller** | `ClienteController.java` | Crear `actualizarTelefono(String id, String nuevoTelefono)` |
| **Application** | `Application.java` | Añadir opción al menú de clientes |

### 🧠 Decisiones de diseño
- El Controller busca el cliente con `repo.findById(id)`.
- Usa `.map()` para modificar y `.orElse(false)` si no existe.
- Se hace `trim()` al nuevo teléfono.
- Se valida con `Validator.requireNotBlank()` que el teléfono no esté vacío.
- Se usa `repo.update()` (no `save()`) para no duplicar el registro.

### 📋 Prompt para la IA
> ```
> En mi proyecto Java MVC "proyecto-final-basico", necesito actualizar el
> teléfono de un cliente existente.
>
> Archivos a modificar:
> - src/com/curso/proyectobasico/controller/ClienteController.java
>   → crear actualizarTelefono(String id, String nuevoTelefono) que:
>     1) Valida id y nuevoTelefono con Validator.requireNotBlank()
>     2) Busca con repo.findById(id)
>     3) Si existe: actualiza teléfono (trim), llama repo.update(), retorna true
>     4) Si no existe: retorna false
> - src/com/curso/proyectobasico/Application.java
>   → añadir opción al menú de clientes para actualizar teléfono
>   → pedir ID y nuevo teléfono, mostrar resultado
>
> Usa estilo Better Comments.
> ```

---

## ⭐⭐⭐ EJERCICIO 10 — Exportar informe a fichero .txt (avanzado)

### 🎯 Objetivo
Crear una opción que genere un **fichero de texto** con un resumen completo de la agenda.

### 📖 Análisis técnico

| Capa | Archivo | Qué hacer |
|------|---------|-----------|
| **Application** | `Application.java` | Crear método `exportarInforme()` y añadir opción al menú principal |

### 🧠 Decisiones de diseño
- Se usa `PrintWriter` con `FileWriter` para escribir el fichero (`try-with-resources`).
- Fichero: `informe_agenda.txt` en la raíz del proyecto.
- Contenido: fecha de generación, lista de clientes (nombre + email), citas pendientes, estadísticas.
- Si hay un `IOException`, se muestra un mensaje de error pero la app **no se cae**.
- **Concepto clave:** `try-with-resources` cierra automáticamente el fichero aunque haya excepciones.

### 📋 Prompt para la IA
> ```
> En mi proyecto Java MVC "proyecto-final-basico", necesito una opción en el
> menú principal que genere un informe completo en "informe_agenda.txt".
>
> Archivo a modificar:
> - src/com/curso/proyectobasico/Application.java
>   → crear método privado exportarInforme() que:
>     1) Usa PrintWriter + FileWriter con try-with-resources
>     2) Escribe: fecha actual, lista de clientes (nombre + email + teléfono),
>        citas pendientes (fecha + descripción + nombre del cliente),
>        estadísticas (total clientes, total citas, pendientes, realizadas)
>     3) Informa con view.line("✔ Informe exportado a 'informe_agenda.txt'")
>     4) Captura IOException con mensaje de error
>   → añadir opción "3) Exportar informe" en el menú principal (run())
>
> Usa estilo Better Comments.
> ```

---

## 📚 Tabla resumen: Conceptos clave del proyecto

| Concepto | Dónde verlo en el código |
|----------|--------------------------|
| **Patrón MVC manual** | Application (Vista) → Controllers (Negocio) → Repositories (CSV) |
| **Enum** | `EstadoCita` (PENDIENTE, REALIZADA) |
| **UUID como ID** | `UUID.randomUUID().toString()` en Controllers |
| **Optional** | `findById().map()` / `.orElseThrow()` en Controllers |
| **Streams (filter)** | Búsquedas y filtrados en Controllers |
| **Validación centralizada** | `Validator` + `DateUtils` + `ValidationException` |
| **Persistencia CSV** | `CsvUtils.java` + `FileStorage.java` |
| **Inyección manual** | Constructores de Controllers reciben Repositories |
| **LocalDate** | Fechas de citas, parseo con `DateUtils` |
| **Try-with-resources** | Escritura de ficheros (ejercicio 10) |

---

## 🎓 Metodología de trabajo

### 🔁 Flujo recomendado para cada ejercicio

1. 🔎 **Lee el análisis:** entiende QUÉ hay que hacer y EN QUÉ archivos.
2. 📜 **Piensa antes de codificar:** ¿qué debería pasar? ¿qué errores podrían ocurrir?
3. 🛠️ **Implementa paso a paso:** 1 cambio → compila → prueba.
4. ✅ **Verifica:** ejecuta la app y prueba el caso normal + los casos borde.
5. 🧑‍🏫 **Reflexiona:** ¿por qué va en esa capa? ¿qué se rompería si lo pusiera en otra?

### 📌 Checklist rápido
- [ ] ¿La regla de negocio está en el Controller (no en Application)?
- [ ] ¿Se puede probar en 1 minuto desde la consola?
- [ ] ¿Los datos se conservan al cerrar y reabrir la app?
- [ ] ¿Si algo falla, el mensaje de error es claro para el usuario?

### 🏁 Rúbrica de evaluación
| Criterio | Peso |
|---|---|
| **Correctitud:** funciona bien en caso normal y borde | 40% |
| **Diseño por capas:** cada responsabilidad en su sitio | 25% |
| **Robustez:** errores controlados con mensajes claros | 20% |
| **Claridad:** nombres descriptivos, código legible | 15% |

---

## 🚀 ¿Quieres ir más allá?

| Idea | Dificultad | Qué aprenderías |
|------|-----------|-----------------|
| Listar solo citas de hoy | ⭐⭐ | `LocalDate.now()`, comparación de fechas |
| Resumen al salir (total clientes/citas) | ⭐ | Contadores, `stream().count()` |
| Validar formato de teléfono con regex | ⭐⭐ | `Pattern.matches()`, expresiones regulares |
| Editar email con unicidad | ⭐⭐ | Update parcial + validación excluyente |
| Persistir en JSON en vez de CSV | ⭐⭐⭐ | Gson/Jackson, serialización |
| Migrar a `proyecto-final` (Gestor de Cursos) | ⭐⭐⭐ | Dominio más complejo, más reglas de negocio |
