package com.curso.ut20.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

/**
 * //! ENTIDAD JPA - PRODUCTO
 * ? Esta clase representa la tabla "producto" en la base de datos
 * * JPA (Java Persistence API) mapea automáticamente esta clase a una tabla
 * * Hibernate se encarga de crear la tabla y gestionar las operaciones CRUD
 *
 * TODO: Considera añadir más campos como descripción, categoría, stock, etc.
 */
@Entity // * Marca esta clase como una entidad JPA (se convertirá en tabla de BD)
public class Producto {

    // ========================================
    // ATRIBUTOS DE LA ENTIDAD
    // ========================================

    /**
     * ! CLAVE PRIMARIA
     * ? @Id marca este campo como PRIMARY KEY en la base de datos
     * ? @GeneratedValue con IDENTITY delega la generación del ID a la base de datos
     * * La BD auto-incrementa este valor automáticamente (1, 2, 3, 4...)
     * * No es necesario setear manualmente el ID al crear un producto
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * ! VALIDACIÓN: NOMBRE OBLIGATORIO
     * ? @NotBlank valida que el nombre no sea null, vacío ("") ni solo espacios ("   ")
     * * Si se intenta guardar un producto sin nombre, Spring lanzará una excepción
     * * El GlobalExceptionHandler capturará esta excepción y devolverá HTTP 400
     */
    @NotBlank(message = "El nombre del producto es obligatorio")
    private String nombre;

    /**
     * ! VALIDACIÓN: PRECIO POSITIVO
     * ? @Min(0) valida que el precio sea mayor o igual a 0
     * * No permite precios negativos
     * * Acepta 0.0 (producto gratuito)
     * TODO: Considera usar @DecimalMin si necesitas excluir el 0
     */
    @Min(value = 0, message = "El precio debe ser mayor o igual a 0")
    private double precio;

    // ========================================
    // GETTERS Y SETTERS
    // ========================================
    // * Spring Data JPA necesita estos métodos para acceder a los campos privados
    // * Jackson (librería JSON) los usa para serializar/deserializar objetos

    /**
     * ? Obtiene el ID del producto (generado automáticamente por la BD)
     * @return ID único del producto
     */
    public Long getId() {
        return id;
    }

    /**
     * ? Establece el ID del producto
     * ! ADVERTENCIA: Generalmente no se debe llamar manualmente, la BD lo genera
     * @param id Identificador único
     */
    public void setId(Long id) {
        this.id = id;
    }

    /**
     * ? Obtiene el nombre del producto
     * @return Nombre del producto (nunca null ni vacío gracias a @NotBlank)
     */
    public String getNombre() {
        return nombre;
    }

    /**
     * ? Establece el nombre del producto
     * * Se validará con @NotBlank antes de persistir en BD
     * @param nombre Nombre del producto (obligatorio)
     */
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    /**
     * ? Obtiene el precio del producto
     * @return Precio del producto (siempre >= 0 gracias a @Min)
     */
    public double getPrecio() {
        return precio;
    }

    /**
     * ? Establece el precio del producto
     * * Se validará con @Min(0) antes de persistir en BD
     * @param precio Precio del producto (debe ser >= 0)
     */
    public void setPrecio(double precio) {
        this.precio = precio;
    }
}
