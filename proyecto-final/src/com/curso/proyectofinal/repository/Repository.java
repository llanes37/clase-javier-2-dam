/*
 * ******************************************************************************************
 * 📘 Repository<T> — Contrato de acceso a datos en memoria/CSV
 * Métodos CRUD mínimos. Implementaciones: AlumnoRepository, CursoRepository, MatriculaRepository.
 *
 * TODO Alumno
 * - [ ] Añadir `long count()` a la interfaz e implementarlo.
 * - [ ] Añadir `void deleteAll()` para pruebas o reseteo.
 * ******************************************************************************************
 */
package com.curso.proyectofinal.repository;

import java.util.List;
import java.util.Optional;

public interface Repository<T> {
    // * Devuelve todos los elementos en memoria (podría paginarse en implementaciones).
    List<T> findAll();

    // * Busca por id; devuelve Optional para que el llamador trate la ausencia explícitamente.
    Optional<T> findById(String id);

    // * Inserta y persiste la entidad; suele devolver la misma instancia o la instancia persistida.
    T save(T entity);

    // * Actualiza una entidad ya existente y persiste los cambios.
    T update(T entity);

    // * Borra por id; devuelve true si existía y fue eliminada.
    boolean delete(String id);
}
