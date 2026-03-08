package com.curso.ut20.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

/**
 * //! ENTIDAD JPA - USUARIO
 * ? Esta clase representa la tabla "usuario" en la base de datos
 * * JPA (Java Persistence API) mapea automáticamente esta clase a una tabla
 * * Hibernate se encarga de crear la tabla y gestionar las operaciones CRUD
 *
 * TODO: Considera añadir campos como email, teléfono, fecha de registro, rol, etc.
 */
@Entity // * Marca esta clase como una entidad JPA (se convertirá en tabla de BD)
public class Usuario {

    // ========================================
    // ATRIBUTOS DE LA ENTIDAD
    // ========================================

    /**
     * ! CLAVE PRIMARIA
     * ? @Id marca este campo como PRIMARY KEY en la base de datos
     * ? @GeneratedValue con IDENTITY delega la generación del ID a la base de datos
     * * La BD auto-incrementa este valor automáticamente (1, 2, 3, 4...)
     * * No es necesario setear manualmente el ID al crear un usuario
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * ! VALIDACIÓN: NOMBRE OBLIGATORIO
     * ? @NotBlank valida que el nombre no sea null, vacío ("") ni solo espacios ("   ")
     * * Si se intenta guardar un usuario sin nombre, Spring lanzará una excepción
     * * El GlobalExceptionHandler capturará esta excepción y devolverá HTTP 400
     */
    @NotBlank(message = "El nombre del usuario es obligatorio")
    private String nombre;

    /**
     * ! VALIDACIÓN: EDAD POSITIVA
     * ? @Min(0) valida que la edad sea mayor o igual a 0
     * * No permite edades negativas
     * * Acepta 0 (recién nacido)
     * TODO: Considera añadir @Max si hay un límite superior de edad
     */
    @Min(value = 0, message = "La edad debe ser mayor o igual a 0")
    private int edad;

    // ========================================
    // GETTERS Y SETTERS
    // ========================================
    // * Spring Data JPA necesita estos métodos para acceder a los campos privados
    // * Jackson (librería JSON) los usa para serializar/deserializar objetos

    /**
     * ? Obtiene el ID del usuario (generado automáticamente por la BD)
     * @return ID único del usuario
     */
    public Long getId() {
        return id;
    }

    /**
     * ? Establece el ID del usuario
     * ! ADVERTENCIA: Generalmente no se debe llamar manualmente, la BD lo genera
     * @param id Identificador único
     */
    public void setId(Long id) {
        this.id = id;
    }

    /**
     * ? Obtiene el nombre del usuario
     * @return Nombre del usuario (nunca null ni vacío gracias a @NotBlank)
     */
    public String getNombre() {
        return nombre;
    }

    /**
     * ? Establece el nombre del usuario
     * * Se validará con @NotBlank antes de persistir en BD
     * @param nombre Nombre del usuario (obligatorio)
     */
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    /**
     * ? Obtiene la edad del usuario
     * @return Edad del usuario (siempre >= 0 gracias a @Min)
     */
    public int getEdad() {
        return edad;
    }

    /**
     * ? Establece la edad del usuario
     * * Se validará con @Min(0) antes de persistir en BD
     * @param edad Edad del usuario (debe ser >= 0)
     */
    public void setEdad(int edad) {
        this.edad = edad;
    }
}
