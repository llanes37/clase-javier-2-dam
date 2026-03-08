package com.curso.pfsqlite.repository;

import com.curso.pfsqlite.domain.EstadoMatricula;
import com.curso.pfsqlite.domain.Matricula;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 INTERFAZ: MatriculaRepository  |  CAPA: Repository (Acceso a Datos)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: @EntityGraph → solución al problema N+1 de consultas SQL
// ? Por defecto, Matricula carga alumno y curso en modo LAZY (no los carga hasta que se acceden).
// ? Si listamos matrículas en la vista y Thymeleaf accede a matricula.alumno.nombre,
// ? Hibernate lanzaría una consulta SQL ADICIONAL por CADA matrícula → problema N+1:
// ?   1 query para las N matrículas
// ?   + N queries para cargar el alumno de cada matrícula
// ?   + N queries para cargar el curso de cada matrícula
// ?   = 2N+1 queries en total (¡puede ser miles si hay muchos datos!)
// ? Con @EntityGraph indicamos: "carga alumno y curso en el mismo SELECT con JOIN" → 1 sola query.

// * 🧠 TEORÍA: Los métodos existsBy... son las guardas de las reglas críticas del service
// ? existsByAlumnoIdAndCursoIdAndEstado → regla anti-duplicado ACTIVA en MatriculaService.crear()
// ? existsByAlumnoIdAndEstado           → protege el borrado de alumnos en AlumnoService.borrar()
// ? existsByCursoIdAndEstado            → protege el borrado de cursos en CursoService.borrar()

public interface MatriculaRepository extends JpaRepository<Matricula, Long> {

    // * Usado en AlumnoService.borrar() → impide borrar un alumno con matrículas
    // ACTIVAS
    boolean existsByAlumnoIdAndEstado(Long alumnoId, EstadoMatricula estado);

    // * Usado en CursoService.borrar() → impide borrar un curso con matrículas
    // ACTIVAS
    boolean existsByCursoIdAndEstado(Long cursoId, EstadoMatricula estado);

    // * Usado en MatriculaService.crear() → impide duplicado ACTIVA para el mismo
    // par alumno+curso
    boolean existsByAlumnoIdAndCursoIdAndEstado(Long alumnoId, Long cursoId, EstadoMatricula estado);

    // * @EntityGraph carga alumno y curso en la misma query con JOIN → evita N+1
    // ? attributePaths indica los campos LAZY que deben cargarse de forma EAGER en
    // esta consulta
    @EntityGraph(attributePaths = { "alumno", "curso" })
    List<Matricula> findAllByOrderByFechaMatriculaDescIdDesc();
}
