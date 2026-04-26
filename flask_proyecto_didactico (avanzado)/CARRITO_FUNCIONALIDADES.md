# Carrito de Compra - Funcionalidades Implementadas

Este documento resume todo lo que se añadió en la web para soportar carrito tipo tienda online.

## 1) Objetivo

Se implementó un carrito persistente por usuario para poder:

- añadir productos,
- ver productos del carrito,
- modificar cantidades,
- eliminar líneas,
- vaciar carrito,
- y calcular subtotales + total final.

## 2) Persistencia en base de datos (SQLite)

Se añadieron dos tablas nuevas en la misma base (`items.db`):

- `carts`
  - `id` (PK)
  - `user_id` (UNIQUE, FK a `users.id`)
  - `created_at`
- `cart_items`
  - `id` (PK)
  - `cart_id` (FK a `carts.id`)
  - `item_id` (FK a `items.id`)
  - `cantidad` (`CHECK cantidad > 0`)
  - `UNIQUE(cart_id, item_id)` para no duplicar la misma línea

Archivo clave: `proyecto_avanzado/controllers/cart.py`.

## 3) Lógica de negocio del carrito

Servicio principal: `CartService` (`proyecto_avanzado/controllers/cart.py`).

Incluye:

- creación automática de carrito por usuario (`_get_or_create_cart_id`),
- `add_item(user_id, item_id, cantidad=1)`,
- `set_quantity(user_id, item_id, cantidad)`,
- `remove_item(user_id, item_id)`,
- `clear_cart(user_id)`,
- `get_cart_items(user_id)` con cálculo de `subtotal`,
- `cart_count(user_id)` para badge del icono,
- `cart_total(user_id)` para total final.

## 4) Validaciones implementadas

Se añadieron validaciones para que el carrito sea robusto:

- no permite cantidad <= 0 al añadir,
- no permite superar el stock disponible,
- no permite añadir artículos inexistentes,
- si cantidad en update es `<= 0`, elimina la línea,
- mensajes de feedback con `flash` (`success`, `danger`, `info`, `warning`).

## 5) Rutas web añadidas

En `proyecto_avanzado/routes/web.py`:

- `GET /carrito` -> vista completa del carrito
- `POST /carrito/add/<item_id>` -> añade 1 unidad
- `POST /carrito/update/<item_id>` -> actualiza cantidad
- `POST /carrito/remove/<item_id>` -> elimina una línea
- `POST /carrito/clear` -> vacía todo el carrito

Todas requieren sesión iniciada (`_require_login`).

## 6) UI/UX añadida

### Navbar (arriba derecha)

- Icono de carrito estilo e-commerce.
- Badge con cantidad total de unidades en carrito.

Se inyecta globalmente con un context processor en `proyecto_avanzado/__init__.py`.

### Home (`index.html`)

- Botón `Añadir al carrito` por cada producto.
- Si no hay sesión iniciada, CTA para iniciar sesión.

### Detalle (`detalle_item.html`)

- Botón `Añadir al carrito` también disponible en detalle.

### Vista de carrito (`cart.html`)

Incluye tabla con:

- producto,
- precio unitario,
- cantidad editable,
- subtotal por línea,
- acciones (`Quitar`),
- resumen lateral con total final,
- botón `Vaciar carrito`,
- botón `Seguir comprando`.

## 7) Comportamiento por usuario

El carrito es independiente por usuario logueado:

- cada usuario tiene su propio `cart`,
- el badge y la vista muestran solo su contenido.

## 8) Archivos añadidos/modificados (carrito)

- Añadido: `proyecto_avanzado/controllers/cart.py`
- Añadido: `proyecto_avanzado/templates/cart.html`
- Modificado: `proyecto_avanzado/routes/web.py`
- Modificado: `proyecto_avanzado/templates/index.html`
- Modificado: `proyecto_avanzado/templates/detalle_item.html`
- Modificado: `proyecto_avanzado/templates/base.html`
- Modificado: `proyecto_avanzado/__init__.py`

## 9) Flujo de uso (rápido)

1. Iniciar sesión.
2. Añadir artículos desde Home o Detalle.
3. Abrir carrito desde el icono superior derecho.
4. Ajustar cantidades / quitar líneas.
5. Revisar total.

## 10) Estado actual

La funcionalidad de carrito está operativa y persistida en SQLite.

Pendiente opcional (si se desea): implementar checkout real para descontar stock y registrar pedidos.
