package com.curso.pfsqlite.repository;

import com.curso.pfsqlite.domain.*;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

import java.math.BigDecimal;
import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.assertTrue;

// * Test de repositorio real para validar consultas derivadas en SQLite.
// ? Se usa `@DataJpaTest` para comprobar que la query de existencia funciona con JPA.
@DataJpaTest(properties = {
        "spring.datasource.url=jdbc:sqlite:file:./target/test-repository.db",
        "spring.datasource.driver-class-name=org.sqlite.JDBC",
        "spring.jpa.database-platform=org.hibernate.community.dialect.SQLiteDialect",
        "spring.jpa.hibernate.ddl-auto=create-drop",
        "spring.flyway.enabled=false"
})
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class MatriculaRepositoryTest {

    @Autowired
    private AlumnoRepository alumnoRepository;
    @Autowired
    private CursoRepository cursoRepository;
    @Autowired
    private MatriculaRepository matriculaRepository;

    @Test
    void existsByAlumnoCursoEstado_detectaActiva() {
        Alumno alumno = new Alumno();
        alumno.setNombre("Repo");
        alumno.setEmail("repo@mail.com");
        alumno = alumnoRepository.save(alumno);

        Curso curso = new Curso();
        curso.setNombre("Repo Curso");
        curso.setTipo(CursoTipo.ONLINE);
        curso.setFechaInicio(LocalDate.of(2026, 3, 1));
        curso.setFechaFin(LocalDate.of(2026, 3, 20));
        curso.setPrecio(new BigDecimal("10.00"));
        curso = cursoRepository.save(curso);

        Matricula matricula = new Matricula();
        matricula.setAlumno(alumno);
        matricula.setCurso(curso);
        matricula.setFechaMatricula(LocalDate.of(2026, 3, 2));
        matricula.setEstado(EstadoMatricula.ACTIVA);
        matriculaRepository.save(matricula);

        assertTrue(matriculaRepository.existsByAlumnoIdAndCursoIdAndEstado(
                alumno.getId(), curso.getId(), EstadoMatricula.ACTIVA));
    }
}
