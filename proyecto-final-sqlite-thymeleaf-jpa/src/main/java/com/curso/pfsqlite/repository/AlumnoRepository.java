package com.curso.pfsqlite.repository;

import com.curso.pfsqlite.domain.Alumno;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 INTERFAZ: AlumnoRepository  |  CAPA: Repository (Acceso a Datos)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: ¿Qué es Spring Data JPA?
// ? Solo declaramos la interfaz. Spring genera la implementación completa en tiempo de arranque.
// ? No escribimos ni una sola línea de SQL para las operaciones CRUD básicas.

// * 🧠 TEORÍA: ¿Qué hereda JpaRepository<Alumno, Long>?
// ? Alumno → tipo de la entidad que gestiona este repositorio.
// ? Long   → tipo del campo @Id de la entidad (debe coincidir exactamente).
// ? Métodos heredados listos para usar: save(), findById(), findAll(), delete(), count()...

// * 🧠 TEORÍA: Consultas derivadas (Derived Queries)
// ? Spring analiza el nombre de los métodos y genera el SQL automáticamente:
// ? existsByEmailIgnoreCase → SELECT COUNT(*) > 0 FROM alumnos WHERE LOWER(email) = LOWER(?)
// ?   exists  → tipo de la consulta (devuelve boolean)
// ?   By      → separador (equivale a WHERE)
// ?   Email   → campo de la entidad a filtrar
// ?   IgnoreCase → modificador (sin distinción de mayúsculas/minúsculas)

// ! ⚠️ La regla de unicidad debe estar reforzada TAMBIÉN en BD (UNIQUE constraint).
// ! Si dos peticiones llegan simultáneas, ambas pueden pasar existsByEmail=false
// ! antes de que ninguna haga el INSERT. La constraint de BD detecta el conflicto.

public interface AlumnoRepository extends JpaRepository<Alumno, Long> {

    // * existsBy... → SELECT COUNT(*) > 0. Más eficiente que
    // findByEmail().isPresent()
    // ? porque NO carga la entidad completa, solo verifica existencia en BD
    boolean existsByEmailIgnoreCase(String email);

    // * findAllByOrderByIdAsc → SELECT * FROM alumnos ORDER BY id ASC
    // ? Orden determinista: el listado siempre aparece en el mismo orden en la UI
    List<Alumno> findAllByOrderByIdAsc();
}
