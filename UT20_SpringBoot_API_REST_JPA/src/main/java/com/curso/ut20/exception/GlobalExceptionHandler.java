package com.curso.ut20.exception;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

import java.util.HashMap;
import java.util.Map;

/**
 * //! MANEJADOR GLOBAL DE EXCEPCIONES
 * ? Captura y procesa todas las excepciones lanzadas en los controladores
 *
 * * @ControllerAdvice permite interceptar excepciones de TODOS los controladores
 * * Extiende ResponseEntityExceptionHandler para heredar manejo de excepciones de Spring
 *
 * ! FLUJO DE VALIDACIÓN:
 * 1. Cliente envía JSON al endpoint (POST/PUT)
 * 2. @Valid en el controlador activa las validaciones (@NotBlank, @Min, etc.)
 * 3. Si hay errores, Spring lanza MethodArgumentNotValidException
 * 4. Este handler captura la excepción
 * 5. Extrae todos los errores de validación
 * 6. Retorna HTTP 400 Bad Request con un JSON de errores
 *
 * ? Ejemplo de respuesta de error (400 Bad Request):
 * {
 *   "nombre": "no debe estar en blanco",
 *   "precio": "debe ser mayor o igual que 0"
 * }
 *
 * TODO: Considera añadir otros handlers para:
 *   - EntityNotFoundException → 404 Not Found
 *   - DataIntegrityViolationException → 409 Conflict
 *   - Exception genérica → 500 Internal Server Error
 */
@ControllerAdvice // * Permite interceptar excepciones de todos los @RestController
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {

    /**
     * ! MANEJO DE ERRORES DE VALIDACIÓN
     * ? Intercepta excepciones cuando @Valid falla en los controladores
     *
     * * Se ejecuta cuando:
     *   - Un campo con @NotBlank recibe valor vacío
     *   - Un campo con @Min recibe valor menor al mínimo
     *   - Cualquier otra validación de Bean Validation falla
     *
     * Flujo de procesamiento:
     * 1. Extraer todos los errores del BindingResult
     * 2. Para cada error, obtener el nombre del campo y el mensaje
     * 3. Construir un Map<String, String> con campo → mensaje
     * 4. Retornar HTTP 400 Bad Request con el mapa como JSON
     *
     * @param ex Excepción lanzada por @Valid
     * @param headers Headers HTTP de la petición
     * @param status Código de estado (400 Bad Request)
     * @param request Contexto de la petición web
     * @return ResponseEntity con mapa de errores y código 400
     */
    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(
            MethodArgumentNotValidException ex,
            HttpHeaders headers,
            HttpStatusCode status,
            WebRequest request) {

        // * Mapa para almacenar los errores: campo → mensaje
        Map<String, String> errores = new HashMap<>();

        // * Iterar sobre todos los errores de validación
        ex.getBindingResult().getAllErrors().forEach(err -> {
            // * Extraer el nombre del campo que falló (ej: "nombre", "precio")
            String campo = ((FieldError) err).getField();

            // * Extraer el mensaje de error (ej: "no debe estar en blanco")
            String msg = err.getDefaultMessage();

            // * Añadir al mapa de errores
            errores.put(campo, msg);
        });

        // * Retornar 400 Bad Request con el mapa de errores como JSON
        return ResponseEntity.badRequest().body(errores);
    }

    // TODO: Añadir más handlers para otras excepciones
    /*
    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<String> handleNotFound(EntityNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(ex.getMessage());
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    public ResponseEntity<String> handleConflict(DataIntegrityViolationException ex) {
        return ResponseEntity.status(HttpStatus.CONFLICT).body("Violación de integridad de datos");
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<String> handleGenericError(Exception ex) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error interno del servidor: " + ex.getMessage());
    }
    */
}
