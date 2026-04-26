package com.curso.pfsqlite.repository;

import com.curso.pfsqlite.domain.Curso;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 INTERFAZ: CursoRepository  |  CAPA: Repository (Acceso a Datos)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: Mismo patrón que AlumnoRepository → interfaz pura, Spring genera la implementación
// ? JpaRepository<Curso, Integer> → gestiona la entidad Curso cuya clave primaria es Integer

// TODO: añadir findAllByTipoOrderByIdAsc(CursoTipo tipo) para el ejercicio de filtrado por tipo
// TODO: añadir findAllByFechaInicioAfter(LocalDate fecha) para listar cursos futuros

public interface CursoRepository extends JpaRepository<Curso, Integer> {

    // * findAllByOrderByIdAsc → SELECT * FROM cursos ORDER BY id ASC
    // ? Orden estable en la UI aunque se borren registros intermedios
    List<Curso> findAllByOrderByIdAsc();
}
