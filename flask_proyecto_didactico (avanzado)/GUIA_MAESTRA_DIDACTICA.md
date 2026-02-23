# Guia Maestra Didactica - Flask Proyecto Avanzado

Ruta del proyecto: `C:\Users\MediaMarktVillaverde\Desktop\clase javier 2 dam\flask_proyecto_didactico (avanzado)`

## 1) Objetivo de esta guia
Esta guia te sirve como hoja de ruta para seguir creciendo el proyecto de forma ordenada.
Cada bloque trae:
- Que construir.
- Prompt recomendado para Codex 5.3 Pro.
- Pasos manuales de validacion.
- Que aprendes tecnicamente.

La idea es que puedas encender el proyecto y elegir un ejercicio nuevo cada dia.

---

## 2) Radiografia real de tu proyecto actual

### Estructura principal
- `app.py`: punto de entrada.
- `proyecto_avanzado/__init__.py`: `create_app()`, config y blueprints.
- `proyecto_avanzado/routes/web.py`: rutas HTML.
- `proyecto_avanzado/routes/api.py`: API JSON.
- `proyecto_avanzado/controllers/items.py`: CRUD en memoria.
- `proyecto_avanzado/controllers/items_sqlite.py`: CRUD SQLite listo para activar.
- `proyecto_avanzado/models.py`: dataclass `Item` + seed inicial.
- `proyecto_avanzado/templates/*.html`: vistas con Bootstrap.

### Lo que esta bien ahora
- Arquitectura limpia para curso: separacion por capas.
- App Factory + Blueprints: muy buena base para escalar.
- API y web separadas: excelente para didactica fullstack.
- Servicio SQLite alternativo ya preparado.

### Limites actuales (buenos para practicar)
- Validaciones minimas.
- Sin tests automatizados.
- Sin autenticacion.
- Manejo de errores basico.
- Frontend funcional pero simple.

---

## 3) Como meter SQLite correctamente (explicacion didactica)

Tu proyecto ya incluye `controllers/items_sqlite.py`.
Ahora mismo web y api usan `items_service` (memoria). Para persistencia real:

1. Inicializa DB una vez:
```bash
python -c "from proyecto_avanzado.controllers.items_sqlite import init_db; init_db()"
```

2. Cambia imports:
- En `proyecto_avanzado/routes/web.py`, cambiar `from ..controllers.items import items_service`
  por `from ..controllers.items_sqlite import sqlite_items_service as items_service`
- En `proyecto_avanzado/routes/api.py`, mismo cambio.

3. Ajusta diferencias de tipo:
- Servicio memoria devuelve `Item` (objeto).
- Servicio SQLite devuelve `dict`.
- Por eso debes unificar acceso en rutas/plantillas (ej: siempre dict o siempre objeto).

4. Reinicia app y prueba crear/listar.

### Que aprendes aqui
- Intercambio de capa de persistencia sin romper rutas.
- Contratos de servicio (muy importante en arquitectura).
- Diferencia entre estado en RAM vs estado persistente.

---

## 4) Modo de trabajo recomendado con Codex 5.3 Pro

Para cada ejercicio usa esta rutina:

1. Pide a Codex analisis del estado actual.
2. Pide plan corto de cambios.
3. Pide implementacion completa.
4. Pide pruebas/manual test plan.
5. Pide mini resumen de aprendizaje.

Plantilla base de prompt:

```text
Analiza este proyecto Flask y aplica esta mejora: [OBJETIVO].
Condiciones:
- Mantener arquitectura actual (app factory + blueprints + controllers).
- Explicar brevemente cada cambio en comentarios didacticos.
- Implementar codigo real, no solo sugerencias.
- Ejecutar verificacion minima (o indicar por que no se pudo).
- Entregar lista de archivos tocados y que se aprendio.
```

---

## 5) Plan didactico por fases (ejercicios incrementales)

## Fase A - Base solida

### Ejercicio A1: Validacion robusta de entradas (web + api)
Objetivo:
- Evitar `float()`/`int()` rompiendo con texto invalido.
- Mensajes de error claros.

Prompt para Codex:
```text
Implementa validaciones robustas en routes/web.py y routes/api.py:
- Si precio o stock no son validos, devolver error amigable.
- No permitir stock negativo.
- Mantener estructura actual.
- Añadir funciones helper de parseo para evitar codigo duplicado.
- Incluye ejemplos de requests validos e invalidos.
```

Checklist manual:
- Probar formulario web con texto en precio.
- Probar API POST con `precio: "abc"`.
- Confirmar que responde 400 sin traceback.

Aprendizaje:
- Validacion defensiva.
- Sanitizacion de input.

### Ejercicio A2: Errores HTML personalizados (400/404/500)
Objetivo:
- Crear UX mejor para errores.

Prompt:
```text
Agrega manejadores de error globales para 400, 404 y 500 con plantillas HTML personalizadas.
Usa app factory en __init__.py y manten coherencia visual con base.html.
```

Aprendizaje:
- Error handlers en Flask.
- Separar errores tecnicos de UX.

### Ejercicio A3: Logging serio a archivo
Objetivo:
- Guardar trazas utiles en `logs/app.log`.

Prompt:
```text
Configura logging en Flask:
- RotatingFileHandler en logs/app.log
- Nivel INFO en desarrollo
- Log de metodo, ruta, status y tiempo de respuesta
- Mantener print didactico actual si aporta, pero priorizar logging formal
```

Aprendizaje:
- Observabilidad basica.
- Diagnostico de fallos.

---

## Fase B - SQL real y limpio

### Ejercicio B1: Unificar contrato de servicio (memoria y sqlite)
Objetivo:
- Que ambos servicios devuelvan la misma forma de datos.

Prompt:
```text
Refactoriza controllers/items.py y controllers/items_sqlite.py para que ambos servicios tengan el mismo contrato:
- list_items()
- get_item(id)
- add_item(...)
- update_stock(...)
Todos deben devolver diccionarios serializables.
Actualiza rutas y templates para que funcionen igual con memoria o sqlite.
```

Aprendizaje:
- Interfaces de servicio.
- Cambio de backend sin cambiar capa web/api.

### Ejercicio B2: Migracion simple de seed a SQLite
Objetivo:
- Cargar datos iniciales solo si tabla vacia.

Prompt:
```text
Crea una funcion seed_if_empty() en items_sqlite.py que inserte datos iniciales si no hay registros.
Invocala en init_db().
```

Aprendizaje:
- Bootstrap de datos.
- Idempotencia.

### Ejercicio B3: Filtros y paginacion en API
Objetivo:
- `GET /api/items?min_precio=10&max_precio=100&page=1&size=10`

Prompt:
```text
Implementa filtros y paginacion para GET /api/items:
- min_precio, max_precio, q (busqueda por nombre)
- page y size con limites razonables
- devuelve metadata: total, page, size, total_pages
Hazlo compatible con servicio en memoria y sqlite.
```

Aprendizaje:
- API profesional.
- Query params y metadata.

---

## Fase C - Frontend didactico potente

### Ejercicio C1: Rehacer portada en estilo dashboard
Objetivo:
- Mantener Bootstrap pero con layout mas moderno.

Prompt:
```text
Rediseña templates/index.html para que parezca un dashboard:
- tarjetas KPI: total items, stock total, valor inventario
- tabla responsive con acciones
- formulario crear item en modal
- mantener base.html y rutas actuales
```

Aprendizaje:
- UX de datos.
- Reutilizacion de componentes.

### Ejercicio C2: Front con HTMX o fetch sin recargar
Objetivo:
- Crear item y actualizar stock dinamicamente.

Prompt:
```text
Integra interaccion sin recarga total en index.html usando fetch API:
- Crear item por POST /api/items
- Actualizar lista en pantalla
- Mensajes de exito/error visibles
No introducir frameworks pesados; solo JS vanilla.
```

Aprendizaje:
- Front reactivo sin SPA.
- API consumida desde navegador.

### Ejercicio C3: Tema visual propio
Objetivo:
- Que el proyecto tenga identidad (no solo bootstrap default).

Prompt:
```text
Refactoriza base.html:
- Define variables CSS para color, espacio y tipografia
- Mejora navbar, cards y botones con estilo consistente
- Mantener buena legibilidad en movil y desktop
```

Aprendizaje:
- Design tokens.
- Escalado visual.

---

## Fase D - Calidad profesional

### Ejercicio D1: Tests API con pytest
Objetivo:
- Cubrir happy path + errores comunes.

Prompt:
```text
Configura pytest para este proyecto Flask.
Crea tests para:
- GET /api/items
- GET /api/items/<id> existente y no existente
- POST /api/items valido e invalido
- PATCH /api/items/<id>/stock valido e invalido
Usa app factory y test client.
```

Aprendizaje:
- Testing backend.
- Prevencion de regresiones.

### Ejercicio D2: Pre-commit de calidad
Objetivo:
- Formato, lint y tipos.

Prompt:
```text
Añade herramientas de calidad:
- ruff
- black
- mypy (minimo en rutas y servicios)
Configura comandos y una guia de uso en README.
```

Aprendizaje:
- Calidad automatizada.
- Disciplina de equipo.

### Ejercicio D3: Documentar API estilo mini OpenAPI
Objetivo:
- Endpoint docs claras en markdown.

Prompt:
```text
Crea docs/API.md con:
- Endpoints
- Payloads
- Ejemplos curl
- Errores esperados
- Contrato de respuesta JSON estandar
```

Aprendizaje:
- Documentacion que evita malentendidos.

---

## 6) Ejercicios extra de IA aplicada (muy utiles)

### IA-1: Refactor guiado por contrato
Prompt:
```text
Actua como arquitecto de software.
Primero define el contrato de ItemService (metodos, inputs, outputs y errores).
Luego refactoriza memoria y sqlite para cumplir exactamente ese contrato.
Finalmente explica en una tabla que problemas de mantenibilidad resolviste.
```

### IA-2: Generador de escenarios de prueba
Prompt:
```text
Genera 20 casos de prueba para este inventario Flask, agrupados por categoria:
- validaciones
- errores de negocio
- concurrencia basica
- regresiones comunes
Incluye expected result para cada caso.
```

### IA-3: Review critico de seguridad
Prompt:
```text
Haz una revision de seguridad sobre este proyecto Flask.
Lista vulnerabilidades reales o potenciales, severidad y solucion practica.
Evita teoria general: quiero hallazgos aplicados al codigo actual.
```

---

## 7) Roadmap sugerido (4 semanas)

Semana 1:
- A1 Validaciones
- A2 Errores custom
- D1 Tests base

Semana 2:
- B1 Contrato unificado
- B2 Seed sqlite
- B3 Filtros API

Semana 3:
- C1 Dashboard
- C2 Front dinamico con fetch
- C3 Tema visual

Semana 4:
- D2 Calidad automatizada
- D3 Documentacion API
- IA-3 Review seguridad y cierre

---

## 8) Criterio de "terminado" por ejercicio
Un ejercicio solo cuenta como terminado si cumple todo:
- Codigo implementado.
- Verificacion manual o automatizada hecha.
- README o MD actualizado.
- Se entiende que aprendiste (1 parrafo de leccion).

---

## 9) Siguiente paso inmediato recomendado
Empieza por `Ejercicio A1` y luego `B1`.
Es la combinacion con mejor retorno: menos bugs + base lista para escalar SQLite sin dolor.

Si quieres, en la siguiente iteracion te lo implemento directamente (A1 + B1) en codigo real dentro de tu proyecto.
