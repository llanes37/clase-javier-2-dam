package com.curso.ut19.model;

/**
 * //! ENTIDAD DE DOMINIO - USUARIO
 * ? Esta clase representa un usuario en el dominio de la aplicación
 *
 * * POJO (Plain Old Java Object):
 *   - No depende de ningún framework
 *   - Solo contiene datos y getters/setters
 *   - Es un JavaBean estándar
 *
 * ! CARACTERÍSTICAS:
 *   - id: Clave primaria (puede ser null antes de insertar en BD)
 *   - nombre: Nombre del usuario (String)
 *   - edad: Edad del usuario (primitivo int)
 *
 * TODO (Alumno):
 *   - Implementa equals() y hashCode() basados en el ID
 *   - Implementa toString() para facilitar el debugging
 *   - Considera añadir más campos (email, teléfono, etc.)
 */
public class Usuario {

    // ========================================
    // ATRIBUTOS
    // ========================================

    /**
     * ! CLAVE PRIMARIA
     * ? Integer (wrapper) permite valor null antes de persistir
     * * La base de datos genera el ID automáticamente con AUTOINCREMENT
     */
    private Integer id;

    /**
     * ? Nombre del usuario
     * * Validado en la capa de servicio (@NotBlank equivalente)
     */
    private String nombre;

    /**
     * ? Edad del usuario
     * * Tipo primitivo int (no puede ser null)
     * * Validado en la capa de servicio (>= 0)
     */
    private int edad;

    // ========================================
    // CONSTRUCTORES
    // ========================================

    /**
     * ! CONSTRUCTOR VACÍO
     * ? Requerido para frameworks y librerías de mapeo (Jackson, Hibernate, etc.)
     */
    public Usuario() {}

    /**
     * ! CONSTRUCTOR COMPLETO
     * ? Útil para crear instancias con todos los campos
     *
     * @param id ID del usuario (puede ser null para nuevos usuarios)
     * @param nombre Nombre del usuario
     * @param edad Edad del usuario
     */
    public Usuario(Integer id, String nombre, int edad) {
        this.id = id;
        this.nombre = nombre;
        this.edad = edad;
    }

    /**
     * ! CONSTRUCTOR SIN ID
     * ? Útil para crear nuevos usuarios antes de insertar en BD
     * * El ID se asignará automáticamente después del INSERT
     *
     * @param nombre Nombre del usuario
     * @param edad Edad del usuario
     */
    public Usuario(String nombre, int edad) {
        this(null, nombre, edad); // * Delega en el constructor completo
    }

    // ========================================
    // GETTERS Y SETTERS
    // ========================================
    // * Patrón JavaBean: métodos get/set para acceder a atributos privados

    /**
     * ? Obtiene el ID del usuario
     * @return ID del usuario (puede ser null si no se ha persistido)
     */
    public Integer getId() {
        return id;
    }

    /**
     * ? Establece el ID del usuario
     * * Generalmente llamado por el repositorio después de INSERT
     * @param id Identificador único
     */
    public void setId(Integer id) {
        this.id = id;
    }

    /**
     * ? Obtiene el nombre del usuario
     * @return Nombre del usuario
     */
    public String getNombre() {
        return nombre;
    }

    /**
     * ? Establece el nombre del usuario
     * @param nombre Nombre del usuario
     */
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    /**
     * ? Obtiene la edad del usuario
     * @return Edad del usuario
     */
    public int getEdad() {
        return edad;
    }

    /**
     * ? Establece la edad del usuario
     * @param edad Edad del usuario
     */
    public void setEdad(int edad) {
        this.edad = edad;
    }

    // TODO: Implementar equals(), hashCode() y toString()
    /*
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Usuario usuario = (Usuario) o;
        return Objects.equals(id, usuario.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return "Usuario{id=" + id + ", nombre='" + nombre + "', edad=" + edad + '}';
    }
    */
}
