package com.curso.proyectobasico.repository;

import java.util.List;
import java.util.Optional;

/*
 * Contrato generico de acceso a datos (CRUD basico).
 */
public interface Repository<T> {
    List<T> findAll();

    Optional<T> findById(String id);

    T save(T entity);

    T update(T entity);

    boolean delete(String id);
}

