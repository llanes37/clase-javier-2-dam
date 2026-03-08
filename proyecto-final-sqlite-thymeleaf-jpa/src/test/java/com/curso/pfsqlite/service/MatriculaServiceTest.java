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
        alumno.setNombre("Ana");
        alumno.setEmail("ana@mail.com");

        curso = new Curso();
        curso.setNombre("Java");
        curso.setTipo(CursoTipo.ONLINE);
        curso.setFechaInicio(LocalDate.of(2026, 3, 1));
        curso.setFechaFin(LocalDate.of(2026, 4, 1));
        curso.setPrecio(new BigDecimal("150.00"));

        form = new MatriculaForm();
        form.setAlumnoId(1L);
        form.setCursoId(2L);
        form.setFechaMatricula(LocalDate.of(2026, 3, 10));

        when(alumnoRepository.findById(1L)).thenReturn(Optional.of(alumno));
        when(cursoRepository.findById(2L)).thenReturn(Optional.of(curso));
    }

    @Test
    void crear_fallaSiFechaFueraDeRango() {
        form.setFechaMatricula(LocalDate.of(2026, 5, 1));

        assertThrows(BusinessException.class, () -> matriculaService.crear(form));
        verify(matriculaRepository, never()).save(any());
    }

    @Test
    void crear_fallaSiDuplicadaActiva() {
        when(matriculaRepository.existsByAlumnoIdAndCursoIdAndEstado(1L, 2L, EstadoMatricula.ACTIVA))
                .thenReturn(true);

        assertThrows(BusinessException.class, () -> matriculaService.crear(form));
        verify(matriculaRepository, never()).save(any());
    }

    @Test
    void crear_okConDatosValidos() {
        when(matriculaRepository.existsByAlumnoIdAndCursoIdAndEstado(1L, 2L, EstadoMatricula.ACTIVA))
                .thenReturn(false);
        when(matriculaRepository.save(any(Matricula.class))).thenAnswer(inv -> inv.getArgument(0));

        Matricula creada = matriculaService.crear(form);

        assertEquals(EstadoMatricula.ACTIVA, creada.getEstado());
        assertEquals(LocalDate.of(2026, 3, 10), creada.getFechaMatricula());
    }
}
