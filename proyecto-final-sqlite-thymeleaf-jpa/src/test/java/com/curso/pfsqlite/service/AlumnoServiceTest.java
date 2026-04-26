package com.curso.pfsqlite.service;

import com.curso.pfsqlite.domain.Alumno;
import com.curso.pfsqlite.domain.EstadoMatricula;
import com.curso.pfsqlite.repository.AlumnoRepository;
import com.curso.pfsqlite.repository.MatriculaRepository;
import com.curso.pfsqlite.web.form.AlumnoForm;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

// * Tests unitarios de reglas de negocio para alumnos.
// ! Validan email unico y borrado protegido.
@ExtendWith(MockitoExtension.class)
class AlumnoServiceTest {

    @Mock
    private AlumnoRepository alumnoRepository;
    @Mock
    private MatriculaRepository matriculaRepository;
    @InjectMocks
    private AlumnoService alumnoService;

    private AlumnoForm form;

    @BeforeEach
    void setUp() {
        form = new AlumnoForm();
        form.setNombre(" Ana ");
        form.setEmail(" ANA@MAIL.COM ");
    }

    @Test
    void crear_normalizaEmailYGurda() {
        when(alumnoRepository.existsByEmailIgnoreCase("ana@mail.com")).thenReturn(false);
        when(alumnoRepository.save(any(Alumno.class))).thenAnswer(inv -> inv.getArgument(0));

        Alumno creado = alumnoService.crear(form);

        assertEquals("ana@mail.com", creado.getEmail());
        assertEquals("Ana", creado.getNombre());
    }

    @Test
    void crear_fallaSiEmailDuplicado() {
        when(alumnoRepository.existsByEmailIgnoreCase("ana@mail.com")).thenReturn(true);

        BusinessException ex = assertThrows(BusinessException.class, () -> alumnoService.crear(form));

        assertTrue(ex.getMessage().contains("Ya existe"));
        verify(alumnoRepository, never()).save(any());
    }

    @Test
    void borrar_fallaConMatriculaActiva() {
        Alumno alumno = new Alumno();
        when(alumnoRepository.findById(10)).thenReturn(Optional.of(alumno));
        when(matriculaRepository.existsByAlumnoIdAndEstado(10, EstadoMatricula.ACTIVA)).thenReturn(true);

        assertThrows(BusinessException.class, () -> alumnoService.borrar(10));
        verify(alumnoRepository, never()).delete(any());
    }
}
