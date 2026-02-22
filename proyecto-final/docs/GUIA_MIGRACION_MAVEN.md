# Guia Completa y Didactica: Que es Maven y como migrar este proyecto paso a paso

## 1. Objetivo de esta guia
Esta guia esta pensada para clase y para trabajo real en tu proyecto.

Al terminar, el alumnado deberia poder:
- Entender que es Maven y para que sirve.
- Diferenciar compilar manualmente vs compilar con Maven.
- Migrar un proyecto Java tradicional a estructura Maven.
- Ejecutar comandos basicos (`clean`, `compile`, `test`, `package`).
- Dejar el proyecto preparado para el siguiente salto (Spring Boot + Thymeleaf).

---

## 2. Que es Maven (explicacion clara)
Maven es una herramienta de automatizacion de proyectos Java.

En la practica, Maven te resuelve 4 problemas tipicos:

1. Dependencias:
- En lugar de descargar `.jar` a mano, Maven los trae automaticamente.

2. Estructura estandar:
- Define una forma comun de organizar carpetas (`src/main/java`, `src/test/java`, etc.).

3. Ciclo de vida de build:
- Comandos estandar para limpiar, compilar, testear y empaquetar.

4. Reproducibilidad:
- Cualquier equipo puede compilar igual usando el mismo `pom.xml`.

Idea corta para alumnos:
- "Maven es el gestor del proyecto: organiza, descarga librerias y ejecuta tareas de build".

---

## 3. Que es el `pom.xml`
`pom.xml` significa **Project Object Model**.
Es el archivo central de Maven.

Define:
- Identidad del proyecto (`groupId`, `artifactId`, `version`).
- Version de Java.
- Dependencias externas.
- Plugins de compilacion/empaquetado.

Ejemplo mental:
- Si el proyecto fuera una receta, `pom.xml` es la lista de ingredientes y pasos de cocina.

---

## 4. Conceptos clave de Maven (explicados simple)

### 4.1 Coordenadas del proyecto
- `groupId`: "apellido" del proyecto (ej. `com.curso`).
- `artifactId`: nombre del proyecto (ej. `proyecto-final`).
- `version`: version actual (ej. `1.0.0-SNAPSHOT`).

### 4.2 Dependencias
Bloques `<dependency>` que Maven descarga desde repositorios (normalmente Maven Central).

### 4.3 Plugins
Herramientas que Maven ejecuta en fases.
Ejemplo: `maven-compiler-plugin` para compilar.

### 4.4 Ciclo de vida
Fases mas usadas:
- `clean`: borra build anterior (`target/`).
- `compile`: compila codigo principal.
- `test`: ejecuta tests.
- `package`: genera `.jar`.
- `install`: instala el artefacto en repositorio local.

---

## 5. Comparativa didactica: antes vs despues

Antes (tu proyecto actual):
- Scripts `build.bat`, `run.bat`, `package.bat`.
- Gestion manual de classpath.
- Estructura custom (`src/com/...`).

Despues (Maven):
- Comandos estandar multiplataforma.
- Dependencias automaticas.
- Estructura conocida por IDEs y equipos.
- Base ideal para Spring Boot.

---

## 6. Requisitos previos
En Windows (PowerShell):

```powershell
java -version
javac -version
mvn -version
```

Recomendado:
- Java 17.
- Maven 3.9+.

Si `mvn` no existe en PATH, instala Maven y configura variables de entorno.

---

## 7. Estrategia de migracion para este proyecto (sin romper todo)
Hazlo en 2 etapas.

### Etapa A: Maven puro (sin Spring aun)
Objetivo:
- Mover estructura y compilar con Maven manteniendo app de consola actual.

### Etapa B: Maven + Spring Boot
Objetivo:
- Una vez estable Maven, meter Spring Boot/Thymeleaf.

Ventaja didactica:
- Cada clase tiene un foco claro.

---

## 8. Migracion practica: paso a paso

## Paso 1. Crear rama

```powershell
cd "c:\Users\MediaMarktVillaverde\Desktop\clase javier 2 dam\proyecto-final"
git checkout -b feature/migracion-maven
```

## Paso 2. Crear estructura Maven estandar
Estructura destino:

```text
proyecto-final/
  pom.xml
  src/main/java/com/curso/proyectofinal/...
  src/main/resources/
  src/test/java/
```

Que mover:
- Todo lo Java actual de `src/com/curso/proyectofinal/...` a `src/main/java/com/curso/proyectofinal/...`.
- Los CSV a `src/main/resources/data` (o temporalmente mantener ruta legacy y ajustar luego).

## Paso 3. Crear `pom.xml` base (Maven puro)
Usa esta plantilla inicial:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.curso</groupId>
  <artifactId>proyecto-final</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <name>proyecto-final</name>

  <properties>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <dependencies>
    <!-- Tests -->
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>5.11.4</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.13.0</version>
      </plugin>

      <plugin>
        <groupId>org.codehaus.mojo</groupId>
        <artifactId>exec-maven-plugin</artifactId>
        <version>3.5.0</version>
        <configuration>
          <mainClass>com.curso.proyectofinal.Application</mainClass>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

## Paso 4. Compilar y ejecutar

```powershell
mvn clean compile
mvn exec:java
```

Si esto funciona, la migracion base esta bien.

## Paso 5. Empaquetar JAR

```powershell
mvn package
```

Resultado esperado:
- archivo en `target/`.

## Paso 6. Ajustar recursos (CSV)
Si tus repos usan rutas relativas tipo `resources/data/...`, revisa working directory.
En Maven, lo habitual es leer recursos desde classpath o usar una carpeta externa `data/`.

Recomendacion didactica:
- corto plazo: mantener ruta externa `data/*.csv`.
- medio plazo: migrar a SQLite (ver guia correspondiente).

---

## 9. Errores frecuentes en clase y solucion

1. `mvn` no reconocido:
- Maven no esta en PATH.

2. `Source option 17 is no longer supported` o similar:
- JDK incorrecto o mezcla de versiones.

3. No encuentra `Application`:
- paquete/ruta mal movidos en `src/main/java`.

4. Problemas de acentos (`Ã¡`, `Ã±`):
- forzar UTF-8 en IDE y `pom.xml`.

5. CSV no aparece:
- revisar ruta relativa y directorio de ejecucion.

---

## 10. Cuando meter Spring Boot
Cuando cumplas esto:
- `mvn clean compile` OK.
- `mvn exec:java` OK.
- Estructura Maven limpia.

Entonces si: pasar a `spring-boot-starter-web` + `thymeleaf`.

---

## 11. Prompt maestro para Codex GPT-5.3 (migracion Maven)
Copia y pega:

```text
Quiero migrar mi proyecto `proyecto-final` a Maven de forma didactica sin meter Spring todavia.

Contexto:
- Proyecto Java 17 actual con estructura no Maven.
- Entrada principal: com.curso.proyectofinal.Application
- Persistencia actual CSV.

Objetivo:
1) Crear estructura Maven estandar.
2) Mover codigo fuente a src/main/java.
3) Crear pom.xml con compiler plugin y exec-maven-plugin.
4) Dejar compilando con `mvn clean compile`.
5) Dejar ejecutando con `mvn exec:java`.
6) Mantener comportamiento actual de consola.

Instrucciones:
- Haz cambios reales en archivos.
- Muestra plan corto y ejecuta.
- No introducir Spring en esta etapa.
- Al final lista archivos tocados y comandos ejecutados.
```

---

## 12. Prompt para segunda fase (Maven -> Spring Boot)

```text
Partiendo de proyecto ya migrado a Maven, quiero pasar a Spring Boot + Thymeleaf.
Mantener dominio y reglas de negocio actuales.
Crear clase @SpringBootApplication, dependencias de web+thymeleaf+validation,
controladores web y vistas base.
```

---

## 13. Dinamica de clase recomendada (2 horas)

Bloque 1 (20 min):
- Que es Maven y `pom.xml`.

Bloque 2 (35 min):
- Migracion estructura en directo.

Bloque 3 (25 min):
- Compilar/ejecutar con Maven + troubleshooting.

Bloque 4 (25 min):
- Ejercicio guiado alumno: clonar pasos y levantar app.

Bloque 5 (15 min):
- Cierre + checklist + siguiente paso (Spring).

---

## 14. Checklist final de esta etapa

- [ ] Existe `pom.xml` valido.
- [ ] Codigo en `src/main/java`.
- [ ] Compila con `mvn clean compile`.
- [ ] Ejecuta con `mvn exec:java`.
- [ ] Se entiende diferencia scripts legacy vs Maven.
- [ ] Proyecto listo para saltar a Spring Boot.

---

## 15. Mensaje didactico de cierre
Si el alumnado entiende Maven, ya puede trabajar como en proyectos reales:
- dependencias serias,
- builds reproducibles,
- integracion continua,
- y transicion natural a Spring.

Ese es el valor real de esta fase.
