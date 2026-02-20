# Flask Proyecto Didactico: Diseno De Curso Y Banco De Ejercicios

## Objetivo del documento
Este archivo es el guion docente para escalar el proyecto `flask_proyecto_didactico` clase a clase, sin improvisar.

## Resultado esperado del alumno
Al terminar el bloque, el alumno debe poder:
- Construir rutas Flask con GET y POST.
- Validar datos de formularios y JSON.
- Responder con HTML y API JSON correctamente.
- Usar codigos HTTP adecuados.
- Persistir datos en SQLite.
- Crear tests basicos con `pytest`.
- Preparar el proyecto para despliegue.

## Mapa de progreso (vision general)

| Bloque | Tema | Dificultad | Tiempo sugerido | Entregable |
|---|---|---|---|---|
| 1 | Formularios y rutas basicas | Baja | 1 clase | Formulario funcional + validacion minima |
| 2 | Query strings y filtros | Baja | 1 clase | Busqueda con filtros y errores 400 |
| 3 | API JSON | Media | 1-2 clases | Endpoints GET/POST con validaciones |
| 4 | Errores, hooks y seguridad basica | Media | 1 clase | API key + headers utiles |
| 5 | Persistencia SQLite | Media | 1-2 clases | Insercion y consulta real en BD |
| 6 | Testing con pytest | Media | 1 clase | Suite minima en verde |
| 7 | Entrega tecnica | Media | 1 clase | README + requirements + run en produccion |

## Ruta didactica detallada

### Sesion 1: Primer flujo completo (tu ejercicio base)
Objetivo:
- Entender el ciclo `frontend -> POST -> backend -> respuesta`.

Archivos:
- `app.py`
- `templates/index.html`
- `templates/resultado.html`

Actividad guiada:
1. Mostrar como llega `nombre` con `request.form.get("nombre")`.
2. Explicar `strip()` y el caso de campo vacio.
3. Ejecutar la redireccion a inicio cuando no hay datos.

Criterios de aceptacion:
- [ ] Si el nombre es valido, muestra `resultado.html`.
- [ ] Si esta vacio, no rompe la app y vuelve a inicio.

Extension para alumnos rapidos:
- Mostrar mensaje de error visual si el nombre va vacio.

### Sesion 2: Formularios con validacion real
Objetivo:
- Validar mas de un campo con reglas claras.

Cambios:
- En `templates/index.html`, agregar `email` y `edad`.
- En `app.py`, validar:
  - `email` contiene `@`
  - `edad` es entero > 0

Criterios de aceptacion:
- [ ] Rechaza edad no numerica.
- [ ] Rechaza email vacio o invalido.
- [ ] Devuelve feedback comprensible al usuario.

Extension:
- Validar longitud minima del nombre.

### Sesion 3: Query strings y filtros
Objetivo:
- Convertir `/buscar` en endpoint de filtros realista.

Cambios:
- Soportar `q`, `page`, `lang`, `sort`, `limit`.
- Si `limit` no es entero o sale de rango, devolver `400`.

Ejemplos de prueba:
- `GET /buscar?q=flask&page=1&lang=es&sort=asc&limit=10`
- `GET /buscar?q=api&limit=abc`

Criterios de aceptacion:
- [ ] Respuesta JSON incluye los filtros parseados.
- [ ] Errores de entrada usan status `400`.

### Sesion 4: API de carrito (GET + POST)
Objetivo:
- Practicar JSON de entrada/salida con reglas de negocio.

Cambios:
- Crear `/api/carrito`:
  - `GET`: listar items en memoria.
  - `POST`: recibir `{nombre, precio, cantidad}` y actualizar total.

Validaciones minimas:
- `nombre` no vacio
- `precio > 0`
- `cantidad >= 1`

Criterios de aceptacion:
- [ ] POST valido agrega item.
- [ ] POST invalido devuelve `400` con error claro.
- [ ] GET refleja estado actual del carrito.

### Sesion 5: Errores, hooks y seguridad basica
Objetivo:
- Entender control de acceso simple y metadatos de respuesta.

Cambios:
- Proteger una ruta con `X-API-Key`.
- Si falta o no coincide, responder `401`.
- En `after_request`, agregar headers utiles (`X-Response-Time` opcional).

Criterios de aceptacion:
- [ ] Sin API key: `401`.
- [ ] Con API key correcta: `200`.
- [ ] La app mantiene manejadores `404/500` coherentes.

### Sesion 6: Persistencia con SQLite
Objetivo:
- Pasar de memoria RAM a datos persistentes.

Cambios:
- Crear tabla `visitas(id, nombre, creado_en)`.
- Insertar en `/procesar`.
- Mostrar contador total de registros.

Criterios de aceptacion:
- [ ] Al reiniciar servidor, los datos siguen existiendo.
- [ ] El contador aumenta en cada envio valido.

Extension:
- Crear endpoint `GET /api/visitas` para listar ultimas visitas.

### Sesion 7: Testing
Objetivo:
- Asegurar que cambios nuevos no rompen lo anterior.

Cambios:
- Configurar `pytest` y cliente de prueba Flask.
- Crear tests minimos para:
  - `/api/echo`
  - `/api/saludo`
  - `/api/calculadora`

Criterios de aceptacion:
- [ ] `pytest -q` pasa en verde.
- [ ] Hay casos de exito y error.

### Sesion 8: Cierre tecnico y entrega
Objetivo:
- Dejar el proyecto listo para compartir y desplegar.

Cambios:
- `requirements.txt`
- Comando de produccion `gunicorn app:app`
- README con pasos de arranque y pruebas.

Criterios de aceptacion:
- [ ] Cualquier compañero puede ejecutar el proyecto siguiendo README.
- [ ] Dependencias y comandos estan documentados.

## Rubrica de evaluacion (100 puntos)

| Criterio | Peso |
|---|---|
| Funcionalidad (rutas/form/API) | 30 |
| Validacion y manejo de errores | 20 |
| Calidad de codigo (claridad y orden) | 15 |
| Testing | 15 |
| Documentacion (README y endpoints) | 10 |
| Mejora opcional / creatividad | 10 |

## Plantilla corta para nuevos ejercicios

```md
### Ejercicio X: [Titulo]
Objetivo:
- [Que aprende el alumno]

Archivos a tocar:
- app.py
- templates/[archivo].html

Requisitos funcionales:
- [ ] ...
- [ ] ...

Criterios de aceptacion:
- [ ] ...
- [ ] ...

Prueba manual minima:
- GET/POST ...

Extension opcional:
- ...
```

## Ideas de ampliacion (backlog)
- Login simple con sesion (`/login`, `/logout`).
- CRUD de tareas (`/api/tareas`).
- Paginacion real y filtros combinados.
- Mini frontend JS que consuma `/api/carrito`.
- Version con Blueprints (`web` y `api`).

## Dinamica recomendada por clase (45-60 min)
1. Explicacion guiada (10-15 min).
2. Demo en vivo del profesor (10 min).
3. Practica guiada (15 min).
4. Reto individual (10-15 min).
5. Cierre con errores frecuentes y soluciones (5 min).

## Nota de uso
- `README.md`: manual tecnico de ejecucion.
- `PLAN_EJERCICIOS_FLASK.md`: guion pedagogico vivo del curso.
- Al cerrar cada sesion, anadir bloque final:
  - realizado
  - bloqueos
  - siguiente objetivo
