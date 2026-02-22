# Guia Completa: Migrar persistencia a SQLite (simple y didactico)

## 1. Objetivo
Este documento explica como pasar de CSV a `SQLite` en tu proyecto, priorizando simplicidad y didactica.

Incluye dos caminos:
- Camino A (recomendado para empezar): `SQLite + JDBC`.
- Camino B (siguiente nivel): `SQLite + Spring Data JPA`.

Tambien incluye prompts listos para Codex (GPT-5.3).

---

## 2. Cuando hacerlo
Haz primero la migracion web a Thymeleaf estable y luego cambia datos.

Orden ideal:
1. Consola/CSV (ya lo tienes).
2. Web/Thymeleaf con CSV.
3. SQLite.

Asi no mezclas demasiados cambios en una sola iteracion.

---

## 3. Modelo de datos SQLite propuesto

Tablas:
- `alumnos`
- `cursos`
- `matriculas`

DDL sugerido:

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS alumnos (
  id TEXT PRIMARY KEY,
  nombre TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  fecha_nacimiento TEXT
);

CREATE TABLE IF NOT EXISTS cursos (
  id TEXT PRIMARY KEY,
  nombre TEXT NOT NULL,
  tipo TEXT NOT NULL,
  fecha_inicio TEXT NOT NULL,
  fecha_fin TEXT NOT NULL,
  precio REAL NOT NULL CHECK (precio >= 0)
);

CREATE TABLE IF NOT EXISTS matriculas (
  id TEXT PRIMARY KEY,
  alumno_id TEXT NOT NULL,
  curso_id TEXT NOT NULL,
  fecha_matricula TEXT NOT NULL,
  estado TEXT NOT NULL,
  FOREIGN KEY (alumno_id) REFERENCES alumnos(id),
  FOREIGN KEY (curso_id) REFERENCES cursos(id)
);

CREATE INDEX IF NOT EXISTS idx_matriculas_alumno ON matriculas(alumno_id);
CREATE INDEX IF NOT EXISTS idx_matriculas_curso ON matriculas(curso_id);
```

Notas:
- Guardar fechas como `TEXT` en formato ISO `yyyy-MM-dd`.
- `email` unico en DB para reforzar regla de negocio.

---

## 4. Camino A (recomendado): SQLite + JDBC
Este camino es el mas facil si quieres mantener control didactico del SQL.

### 4.1 Dependencia Maven
En `pom.xml` agrega:

```xml
<dependency>
  <groupId>org.xerial</groupId>
  <artifactId>sqlite-jdbc</artifactId>
  <version>3.47.1.0</version>
</dependency>
```

### 4.2 Configuracion
En `application.properties`:

```properties
app.db.path=data/proyecto-final.db
```

### 4.3 Crear proveedor de conexion
Clase sugerida: `infrastructure/sqlite/SqliteConnectionFactory.java`

Responsabilidades:
- Construir URL JDBC: `jdbc:sqlite:${ruta}`.
- Entregar `Connection`.
- Activar `PRAGMA foreign_keys = ON` por conexion.

### 4.4 Script de inicializacion
- Crear `src/main/resources/sql/schema.sql` con el DDL.
- En el arranque, ejecutar este script si tablas no existen.

### 4.5 Repositorios SQLite
Crear implementaciones JDBC:
- `SqliteAlumnoRepository`
- `SqliteCursoRepository`
- `SqliteMatriculaRepository`

Mantener misma interfaz `Repository<T>` para minimizar impacto.

Metodos clave:
- `findAll`, `findById`, `save`, `update`, `delete`
- Extra: `findByAlumnoId`, `findByCursoId`, `existsByAlumnoAndCurso`

### 4.6 Inyeccion de dependencias
Si estas en Spring:
- Marca repos con `@Repository`.
- Inyecta en `service`.

Si no estas en Spring todavia:
- Instancia manual en `Application`.

### 4.7 Migrador CSV -> SQLite (muy recomendado)
Crear comando de migracion que:
1. Lea CSV legacy.
2. Inserte en SQLite si DB vacia.
3. Informe cuantos registros importo.

Asi no pierdes datos de pruebas.

---

## 5. Camino B: SQLite + Spring Data JPA
Usalo cuando quieras mas productividad y menos SQL manual.

### 5.1 Dependencias
- `spring-boot-starter-data-jpa`
- `sqlite-jdbc`
- Dialecto SQLite (lib externa o dialecto propio)

### 5.2 Configuracion tipica
En `application.properties`:

```properties
spring.datasource.url=jdbc:sqlite:data/proyecto-final.db
spring.datasource.driver-class-name=org.sqlite.JDBC
spring.jpa.show-sql=true
spring.jpa.hibernate.ddl-auto=update
```

Nota importante:
- Hibernate + SQLite no es oficial al 100% como otros motores.
- Para clase y didactica funciona, pero JDBC simple suele ser mas predecible.

### 5.3 Entidades JPA
Anotar `Alumno`, `Curso`, `Matricula` con `@Entity` y `@Table`.

Atencion:
- Puedes mantener IDs `String` (UUID generado por app).
- O migrar a `Long` autoincrement (mas trabajo).

### 5.4 Repos JPA
Interfaces:
- `AlumnoJpaRepository extends JpaRepository<Alumno, String>`
- `CursoJpaRepository extends JpaRepository<Curso, String>`
- `MatriculaJpaRepository extends JpaRepository<Matricula, String>`

Consultas derivadas:
- `findByEmail(...)`
- `findByAlumnoId(...)`
- `findByCursoId(...)`

---

## 6. Prompt maestro SQLite para Codex (GPT-5.3)

```text
Quiero migrar la persistencia de mi proyecto `proyecto-final` de CSV a SQLite de forma sencilla y didactica.

Contexto:
- Java 17.
- Ya tengo modelo de dominio y reglas de negocio.
- Repositorios actuales guardan en CSV.

Objetivo:
1) Crear base SQLite local (`data/proyecto-final.db`).
2) Crear schema de tablas alumnos, cursos y matriculas.
3) Implementar repositorios SQLite con JDBC manteniendo mismas interfaces/contratos.
4) Sustituir uso de repos CSV por SQLite sin romper casos de uso.
5) Añadir migracion inicial CSV -> SQLite cuando DB este vacia.
6) Verificar compilacion y funcionamiento.

Instrucciones:
- Haz cambios reales en archivos.
- Mantener codigo claro para nivel didactico.
- Mostrar plan breve y luego implementar.
- Incluir manejo de errores SQL razonable.
- Al final listar archivos modificados y comandos de verificacion.
```

---

## 7. Prompts cortos por fase

### Fase 1: DB base
```text
Agrega SQLite JDBC al proyecto y crea infraestructura de conexion + schema.sql.
Inicializa tablas al arrancar.
```

### Fase 2: Repositorios
```text
Implementa AlumnoRepository, CursoRepository y MatriculaRepository en version SQLite JDBC,
respetando metodos actuales y reglas de conversion de fechas/enums.
```

### Fase 3: Migracion
```text
Crea un migrador CSV->SQLite idempotente: si tablas estan vacias importa datos CSV.
Si ya hay datos, no duplica.
```

### Fase 4: Integracion
```text
Conecta servicios/controladores para usar repos SQLite en vez de CSV.
Ejecuta verificacion completa de flujo CRUD.
```

---

## 8. Checklist de aceptacion

- [ ] Se crea archivo `data/proyecto-final.db` automaticamente.
- [ ] Tablas existen con PK/FK e indice basico.
- [ ] CRUD de alumnos funciona.
- [ ] CRUD de cursos funciona.
- [ ] Matricular/anular funciona.
- [ ] Reglas de validacion se mantienen.
- [ ] Si DB vacia, se importan datos CSV legacy.
- [ ] No se duplican datos en reinicios.

---

## 9. Pruebas manuales recomendadas

1. Crear 2 alumnos y 2 cursos.
2. Matricular 1 alumno en 2 cursos.
3. Intentar email duplicado (debe fallar).
4. Intentar curso con `fecha_fin < fecha_inicio` (debe fallar).
5. Reiniciar app y comprobar persistencia.

---

## 10. Errores comunes

1. `database is locked`:
- Cierra conexiones correctamente con `try-with-resources`.

2. FK no aplicadas:
- Asegura `PRAGMA foreign_keys=ON` en cada conexion.

3. Fechas inconsistentes:
- Guarda/lee solo ISO `yyyy-MM-dd`.

4. Enum invalido:
- Normaliza string antes de `Enum.valueOf`.

---

## 11. Recomendacion final de eleccion
Si quieres lo mas sencillo para clase:
- Elige `SQLite + JDBC`.

Si luego quieres curriculum mas profesional:
- Da el salto a `Spring Data JPA` en una segunda iteracion.

---

## 12. Comandos utiles

```powershell
# Compilar
mvn clean compile

# Ejecutar
mvn spring-boot:run

# Tests (si los tienes)
mvn test
```

---

## 13. Resultado esperado
Al finalizar, tu proyecto tendra:
- Web con Thymeleaf (si seguiste la guia 1).
- Persistencia real en SQLite.
- Mismo dominio y reglas didacticas.
- Mejor base para evolucionar a REST o despliegue.
