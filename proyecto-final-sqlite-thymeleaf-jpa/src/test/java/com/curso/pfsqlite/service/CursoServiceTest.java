package com.curso.pfsqlite.service;

import com.curso.pfsqlite.domain.Curso;
import com.curso.pfsqlite.domain.CursoTipo;
import com.curso.pfsqlite.domain.EstadoMatricula;
import com.curso.pfsqlite.repository.CursoRepository;
import com.curso.pfsqlite.repository.MatriculaRepository;
import com.curso.pfsqlite.web.form.CursoForm;
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

// * Tests unitarios de reglas en cursos (fechas, borrado protegido).
@ExtendWith(MockitoExtension.class)
class CursoServiceTest {

    @Mock
    private CursoRepository cursoRepository;
    @Mock
    private MatriculaRepository matriculaRepository;
    @InjectMocks
    private CursoService cursoService;

    private CursoForm form;

    @BeforeEach
    void setUp() {
        form = new CursoForm();
        form.setNombre("SQL");
        form.setTipo(CursoTipo.ONLINE);
        form.setFechaInicio(LocalDate.of(2026, 3, 1));
        form.setFechaFin(LocalDate.of(2026, 3, 10));
        form.setPrecio(new BigDecimal("100.00"));
    }

    @Test
    void crear_fallaSiFechaFinEsAnterior() {
        form.setFechaFin(LocalDate.of(2026, 2, 28));

        assertThrows(BusinessException.class, () -> cursoService.crear(form));
        verify(cursoRepository, never()).save(any());
    }

    @Test
    void crear_guardaCursoValido() {
        when(cursoRepository.save(any(Curso.class))).thenAnswer(inv -> inv.getArgument(0));

        Curso creado = cursoService.crear(form);

        assertEquals(CursoTipo.ONLINE, creado.getTipo());
        assertEquals(new BigDecimal("100.00"), creado.getPrecio());
    }

    @Test
    void borrar_fallaConMatriculaActiva() {
        Curso curso = new Curso();
        when(cursoRepository.findById(20)).thenReturn(Optional.of(curso));
        when(matriculaRepository.existsByCursoIdAndEstado(20, EstadoMatricula.ACTIVA)).thenReturn(true);

        assertThrows(BusinessException.class, () -> cursoService.borrar(20));
        verify(cursoRepository, never()).delete(any());
    }

    @Test
    void actualizar_okAplicaCambios() {
        Curso existente = new Curso();
        when(cursoRepository.findById(7)).thenReturn(Optional.of(existente));
        when(cursoRepository.save(any(Curso.class))).thenAnswer(inv -> inv.getArgument(0));

        form.setNombre("Spring Boot");
        form.setTipo(CursoTipo.PRESENCIAL);
        form.setPrecio(new BigDecimal("250.00"));

        Curso actualizado = cursoService.actualizar(7, form);

        assertEquals("Spring Boot", actualizado.getNombre());
        assertEquals(CursoTipo.PRESENCIAL, actualizado.getTipo());
        assertEquals(new BigDecimal("250.00"), actualizado.getPrecio());
    }
}
