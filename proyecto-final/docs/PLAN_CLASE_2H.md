# 🎯 Plan de Clase (2 horas)
## Migracion de Proyecto Java a Maven (base para Spring + Thymeleaf)

> **Nivel:** 2º DAM  
> **Duracion total:** 120 minutos  
> **Formato:** Clase guiada + practica asistida

---

## 🧭 1) Objetivo de la sesion
Al finalizar la clase, el alumnado sera capaz de:
- ✅ Explicar que es Maven y para que sirve.
- ✅ Identificar la estructura estandar de un proyecto Maven.
- ✅ Migrar un proyecto Java tradicional a Maven sin romper ejecucion.
- ✅ Compilar y ejecutar con comandos Maven.
- ✅ Dejar el proyecto listo para el siguiente salto: Spring Boot + Thymeleaf.

---

## 🧰 2) Material necesario
- 💻 PC con **JDK 17**.
- ⚙️ **Maven 3.9+** en PATH.
- 🧑‍💻 VS Code o IntelliJ.
- 📁 Proyecto: `proyecto-final`.
- 📄 Apoyos:
  - `docs/GUIA_MIGRACION_MAVEN.md`
  - `docs/GUIA_MIGRACION_THYMELEAF.md` (solo preview final)

---

## ⏱️ 3) Agenda minuto a minuto (120 min)

| Tiempo | Bloque | Objetivo | Metodo |
|---|---|---|---|
| 00-10 | 🚀 Apertura | Contexto y meta clara | Explicacion breve + mapa de clase |
| 10-25 | 📘 Conceptos Maven | Entender `pom.xml`, dependencias, lifecycle | Pizarra + ejemplos |
| 25-45 | 🧱 Estructura Maven | Ver carpeta estandar y por que mejora diseño | Demo en proyecto real |
| 45-70 | 🛠️ Migracion guiada | Crear `pom.xml`, mover estructura, compilar | Live coding docente |
| 70-95 | 🧪 Practica alumnado | Replicar migracion por parejas | Trabajo guiado |
| 95-110 | 🔍 Debug comun | Resolver errores tipicos de clase | Diagnostico en grupo |
| 110-120 | ✅ Cierre y evaluacion | Checklist final + siguiente paso | Revision rapida |

---

## 🗺️ 4) Guion docente detallado

### 🚀 Bloque 1 (00-10) Apertura
**Mensaje clave:** "Hoy no metemos frontend aun. Primero profesionalizamos el proyecto con Maven."  
**Acciones:**
- Mostrar estructura actual (`src/com/...`, scripts `.bat`).
- Explicar que el objetivo de hoy es dejar build reproducible.

### 📘 Bloque 2 (10-25) Conceptos Maven
**Puntos minimos:**
- `pom.xml` = contrato del proyecto.
- Coordenadas: `groupId`, `artifactId`, `version`.
- Dependencias y plugins.
- Ciclo de vida: `clean`, `compile`, `test`, `package`.

**Micro-demo en terminal:**
```powershell
mvn -v
```

### 🧱 Bloque 3 (25-45) Estructura estandar
**Comparativa didactica:**
- Antes: estructura custom + classpath manual.
- Despues: `src/main/java`, `src/main/resources`, `src/test/java`.

**Checkpoint del grupo:**
- Cada alumno sabe donde va cada tipo de archivo.

### 🛠️ Bloque 4 (45-70) Migracion guiada en directo
**Pasos en orden:**
1. Crear rama de trabajo.
2. Crear `pom.xml` minimo.
3. Mover codigo a `src/main/java`.
4. Verificar main class.
5. Compilar con Maven.
6. Ejecutar con Maven.

**Comandos clave:**
```powershell
mvn clean compile
mvn exec:java
mvn package
```

### 🧪 Bloque 5 (70-95) Practica del alumnado
**Actividad:**
- Por parejas, replicar migracion en su copia.

**Criterio de exito:**
- Debe compilar y ejecutar por Maven sin scripts legacy.

### 🔍 Bloque 6 (95-110) Resolucion de errores tipicos
**Errores frecuentes a tratar en directo:**
- `mvn` no reconocido.
- Java version incorrecta.
- Paquete de `Application` mal ubicado.
- Problemas de UTF-8.

### ✅ Bloque 7 (110-120) Cierre
**Checklist final de salida:**
- [ ] `pom.xml` valido.
- [ ] Estructura Maven correcta.
- [ ] `mvn clean compile` OK.
- [ ] `mvn exec:java` OK.
- [ ] Proyecto listo para Spring en proxima clase.

---

## 🧩 5) Ejercicio de clase (listo para proyectar)
### Enunciado
Migra el proyecto a Maven manteniendo funcionalidad actual de consola.

### Entregable minimo
- Captura o demostracion terminal con:
```powershell
mvn clean compile
mvn exec:java
```

### Entregable extra (sube nota)
- Ejecutar `mvn package` y mostrar `.jar` en `target/`.

---

## 🛟 6) Plan B (si hay bloqueo tecnico)
Si fallan instalaciones en varios equipos:
1. Continuar con demo del profesor (pantalla principal).
2. Alumnos hacen seguimiento en documento guiado.
3. Cerrar con practica corta sobre lectura de `pom.xml`.
4. Dejar instalacion Maven como tarea previa para siguiente clase.

---

## 📊 7) Rubrica rapida de la sesion (10 puntos)
- 4 pts: Proyecto migra a estructura Maven correcta.
- 3 pts: Compila y ejecuta con comandos Maven.
- 2 pts: Explica correctamente que hace `pom.xml`.
- 1 pt: Identifica siguiente paso tecnico (Spring + Thymeleaf).

---

## 🧭 8) Transicion a la siguiente clase
**Siguiente objetivo:** usar esta base Maven para arrancar Spring Boot y primer template Thymeleaf.

**Tarea previa recomendada:**
- Leer `docs/GUIA_MIGRACION_THYMELEAF.md` (secciones 1 a 6).
- Llegar con Maven funcionando en su equipo.

---

## 📝 9) Frase de cierre para clase
"Hoy hemos convertido un proyecto academico en un proyecto profesionalizable. Con Maven, el salto a Spring ya no es salto, es continuidad." 
