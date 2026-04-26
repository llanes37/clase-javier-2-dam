package com.curso.pfsqlite.service;

import com.curso.pfsqlite.domain.*;
import com.curso.pfsqlite.repository.AlumnoRepository;
import com.curso.pfsqlite.repository.CursoRepository;
import com.curso.pfsqlite.repository.MatriculaRepository;
import com.curso.pfsqlite.web.form.MatriculaForm;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.util.ReflectionTestUtils;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

// * Tests unitarios de matriculas: ventana temporal y duplicado ACTIVA.
@ExtendWith(MockitoExtension.class)
class MatriculaServiceTest {

    @Mock
    private MatriculaRepository matriculaRepository;
    @Mock
    private AlumnoRepository alumnoRepository;
    @Mock
    private CursoRepository cursoRepository;
    @InjectMocks
    private MatriculaService matriculaService;

    private Alumno alumno;
    private Curso curso;
    private MatriculaForm form;

    @BeforeEach
    void setUp() {
        alumno = new Alumno();
        ReflectionTestUtils.setField(alumno, "id", 1);
        alumno.setNombre("Ana");
        alumno.setEmail("ana@mail.com");

        curso = new Curso();
        ReflectionTestUtils.setField(curso, "id", 2);
        curso.setNombre("Java");
        curso.setTipo(CursoTipo.ONLINE);
        curso.setFechaInicio(LocalDate.of(2026, 3, 1));
        curso.setFechaFin(LocalDate.of(2026, 4, 1));
        curso.setPrecio(new BigDecimal("150.00"));

        form = new MatriculaForm();
        form.setAlumnoId(1);
        form.setCursoId(2);
        form.setFechaMatricula(LocalDate.of(2026, 3, 10));

        lenient().when(alumnoRepository.findById(1)).thenReturn(Optional.of(alumno));
        lenient().when(cursoRepository.findById(2)).thenReturn(Optional.of(curso));
    }

    @Test
    void crear_fallaSiFechaFueraDeRango() {
        form.setFechaMatricula(LocalDate.of(2026, 5, 1));

        assertThrows(BusinessException.class, () -> matriculaService.crear(form));
        verify(matriculaRepository, never()).save(any());
    }

    @Test
    void crear_fallaSiDuplicadaActiva() {
        when(matriculaRepository.existsByAlumnoIdAndCursoIdAndEstado(1, 2, EstadoMatricula.ACTIVA))
                .thenReturn(true);

        assertThrows(BusinessException.class, () -> matriculaService.crear(form));
        verify(matriculaRepository, never()).save(any());
    }

    @Test
    void crear_okConDatosValidos() {
        when(matriculaRepository.existsByAlumnoIdAndCursoIdAndEstado(1, 2, EstadoMatricula.ACTIVA))
                .thenReturn(false);
        when(matriculaRepository.save(any(Matricula.class))).thenAnswer(inv -> inv.getArgument(0));

        Matricula creada = matriculaService.crear(form);

        assertEquals(EstadoMatricula.ACTIVA, creada.getEstado());
        assertEquals(LocalDate.of(2026, 3, 10), creada.getFechaMatricula());
    }

    @Test
    void actualizar_fallaSiNuevaRelacionDuplicadaActiva() {
        Alumno otroAlumno = new Alumno();
        ReflectionTestUtils.setField(otroAlumno, "id", 3);
        otroAlumno.setNombre("Luis");
        otroAlumno.setEmail("luis@mail.com");

        Curso otroCurso = new Curso();
        ReflectionTestUtils.setField(otroCurso, "id", 4);
        otroCurso.setNombre("SQL");
        otroCurso.setTipo(CursoTipo.PRESENCIAL);
        otroCurso.setFechaInicio(LocalDate.of(2026, 3, 1));
        otroCurso.setFechaFin(LocalDate.of(2026, 4, 1));
        otroCurso.setPrecio(new BigDecimal("90.00"));

        Matricula existente = new Matricula();
        ReflectionTestUtils.setField(existente, "id", 9);
        existente.setAlumno(alumno);
        existente.setCurso(curso);
        existente.setFechaMatricula(LocalDate.of(2026, 3, 10));
        existente.setEstado(EstadoMatricula.ACTIVA);

        form.setAlumnoId(3);
        form.setCursoId(4);
        form.setFechaMatricula(LocalDate.of(2026, 3, 15));

        when(matriculaRepository.findDetalleById(9)).thenReturn(Optional.of(existente));
        when(alumnoRepository.findById(3)).thenReturn(Optional.of(otroAlumno));
        when(cursoRepository.findById(4)).thenReturn(Optional.of(otroCurso));
        when(matriculaRepository.existsByAlumnoIdAndCursoIdAndEstado(3, 4, EstadoMatricula.ACTIVA))
                .thenReturn(true);

        assertThrows(BusinessException.class, () -> matriculaService.actualizar(9, form));
        verify(matriculaRepository, never()).save(any());
    }

    @Test
    void actualizar_okMantieneEstadoExistente() {
        Matricula existente = new Matricula();
        ReflectionTestUtils.setField(existente, "id", 10);
        existente.setAlumno(alumno);
        existente.setCurso(curso);
        existente.setFechaMatricula(LocalDate.of(2026, 3, 8));
        existente.setEstado(EstadoMatricula.ANULADA);

        form.setFechaMatricula(LocalDate.of(2026, 3, 20));

        when(matriculaRepository.findDetalleById(10)).thenReturn(Optional.of(existente));
        when(matriculaRepository.save(any(Matricula.class))).thenAnswer(inv -> inv.getArgument(0));

        Matricula actualizada = matriculaService.actualizar(10, form);

        assertEquals(EstadoMatricula.ANULADA, actualizada.getEstado());
        assertEquals(LocalDate.of(2026, 3, 20), actualizada.getFechaMatricula());
        assertEquals(1, actualizada.getAlumno().getId());
        assertEquals(2, actualizada.getCurso().getId());
    }
}
