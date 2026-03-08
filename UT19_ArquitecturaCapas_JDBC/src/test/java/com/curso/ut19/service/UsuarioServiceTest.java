package com.curso.ut19.service;

import com.curso.ut19.model.Usuario;
import com.curso.ut19.repository.UsuarioRepository;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

class UsuarioServiceTest {

    @Test
    void crearDebeValidarNombreYEdad() {
        UsuarioRepository repo = Mockito.mock(UsuarioRepository.class);
        UsuarioService service = new UsuarioService(repo);

        assertThrows(IllegalArgumentException.class, () -> service.crear("", 10));
        assertThrows(IllegalArgumentException.class, () -> service.crear("Ana", -1));
    }

    @Test
    void crearOkDebeDevolverUsuarioConId() {
        UsuarioRepository repo = Mockito.mock(UsuarioRepository.class);
        when(repo.save(any())).thenAnswer(invocation -> {
            Usuario u = invocation.getArgument(0);
            u.setId(1);
            return u;
        });
        UsuarioService service = new UsuarioService(repo);

        Usuario u = service.crear("Ana", 20);
        assertNotNull(u.getId());
        assertEquals("Ana", u.getNombre());
        assertEquals(20, u.getEdad());
    }
}
