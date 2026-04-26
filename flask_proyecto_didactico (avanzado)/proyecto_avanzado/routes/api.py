"""
=========================================================================================
Blueprint API (JSON) - Rutas REST para acceder a items
=========================================================================================
Este modulo contiene todas las rutas de la API JSON que permiten:
  * Listar todos los items
  * Obtener detalle de un item especifico
  * Crear nuevos items
  * Actualizar el stock de un item
  
Las respuestas siempre son en formato JSON con estructura: {"ok": bool, "data": ...}
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from ..controllers.items import items_service

# ! Blueprint para API JSON
# * Este blueprint se registra en __init__.py con el prefijo "/api"
# * Todas las rutas aqui tendran la url base: http://localhost:5000/api/...
api_bp = Blueprint("api", __name__)



# =========================================================================================
# * RUTA 1: GET /api/items - LISTAR TODOS LOS ITEMS
# =========================================================================================
@api_bp.get("/items")
def api_list_items():
    """
    Lista de todos los items en formato JSON.
    
    Metodo HTTP: GET
    URL: http://localhost:5000/api/items
    
    Respuesta exitosa (200):
    {
        "ok": true,
        "items": [
            {"id": 1, "nombre": "Laptop", "precio": 999.99, "stock": 5},
            {"id": 2, "nombre": "Monitor", "precio": 299.99, "stock": 10}
        ]
    }
    
    ? Uso: Obtener lista completa de productos para mostrar en frontend
    """
    return jsonify(ok=True, items=items_service.to_dict_list())




# =========================================================================================
# * RUTA 2: GET /api/items/<id> - OBTENER DETALLE DE UN ITEM
# =========================================================================================
@api_bp.get("/items/<int:item_id>")
def api_get_item(item_id: int):
    """
    Obtiene el detalle de un item especifico por su ID.
    
    Metodo HTTP: GET
    URL: http://localhost:5000/api/items/1
    
    Parametros:
      - item_id (int): ID del item a consultar (en la URL)
    
    Respuesta exitosa (200):
    {
        "ok": true,
        "item": {"id": 1, "nombre": "Laptop", "precio": 999.99, "stock": 5}
    }
    
    Respuesta error (404):
    {
        "ok": false,
        "error": "Item no encontrado"
    }
    
    ? Uso: Obtener informacion detallada de un producto en particular
    """
    item = items_service.get_item(item_id)
    if not item:
        return jsonify(ok=False, error="Item no encontrado"), 404
    return jsonify(ok=True, item=item.to_dict())




# =========================================================================================
# * RUTA 3: POST /api/items - CREAR UN NUEVO ITEM
# =========================================================================================
@api_bp.post("/items")
def api_create_item():
    """
    Crea un nuevo item en la tienda.
    
    Metodo HTTP: POST
    URL: http://localhost:5000/api/items
    Content-Type: application/json
    
    Body (JSON esperado):
    {
        "nombre": "Teclado",
        "precio": 79.99,
        "stock": 20
    }
    
    Respuesta exitosa (201 - Created):
    {
        "ok": true,
        "item": {"id": 3, "nombre": "Teclado", "precio": 79.99, "stock": 20}
    }
    
    Respuesta error (400 - Bad Request):
    {
        "ok": false,
        "error": "Datos invalidos"
    }
    
    ! Validaciones:
      - nombre: No puede estar vacio
      - precio: Debe ser > 0
      - stock: Puede ser 0 o mayor
    
    ? Uso: Agregar nuevos productos a la tienda desde la API
    """
    data = request.get_json(silent=True) or {}
    nombre = str(data.get("nombre", "")).strip()
    precio = float(data.get("precio") or 0)
    stock = int(data.get("stock") or 0)

    if not nombre or precio <= 0:
        return jsonify(ok=False, error="Datos invalidos"), 400

    item = items_service.add_item(nombre, precio, stock)
    return jsonify(ok=True, item=item.to_dict()), 201




# =========================================================================================
# * RUTA 4: PATCH /api/items/<id>/stock - ACTUALIZAR STOCK DE UN ITEM
# =========================================================================================
@api_bp.patch("/items/<int:item_id>/stock")
def api_update_stock(item_id: int):
    """
    Actualiza el stock de un item especifico.
    
    Metodo HTTP: PATCH
    URL: http://localhost:5000/api/items/1/stock
    Content-Type: application/json
    
    Parametros:
      - item_id (int): ID del item cuyo stock se actualiza (en la URL)
    
    Body (JSON esperado):
    {
        "stock": 15
    }
    
    Respuesta exitosa (200):
    {
        "ok": true,
        "item": {"id": 1, "nombre": "Laptop", "precio": 999.99, "stock": 15}
    }
    
    Respuesta error - Stock invalido (400):
    {
        "ok": false,
        "error": "Stock debe ser >= 0"
    }
    
    Respuesta error - Item no existe (404):
    {
        "ok": false,
        "error": "Item no encontrado"
    }
    
    ! Validaciones:
      - stock: Debe ser >= 0 (no se permite stock negativo)
      - item_id: El item debe existir en el sistema
    
    ? Uso: Actualizar inventario cuando se vende un producto o llega nueva mercancia
    """
    data = request.get_json(silent=True) or {}
    stock = int(data.get("stock") or -1)
    if stock < 0:
        return jsonify(ok=False, error="Stock debe ser >= 0"), 400
    item = items_service.update_stock(item_id, stock)
    if not item:
        return jsonify(ok=False, error="Item no encontrado"), 404
    return jsonify(ok=True, item=item.to_dict())


@api_bp.put("/items/<int:item_id>")
def api_update_item(item_id: int):
    """
    Actualiza un item completo (nombre, precio y stock).

    Metodo HTTP: PUT
    URL: http://localhost:5000/api/items/1
    Content-Type: application/json
    """
    data = request.get_json(silent=True) or {}
    nombre = str(data.get("nombre", "")).strip()

    try:
        precio = float(data.get("precio") or 0)
        stock = int(data.get("stock") or -1)
    except (TypeError, ValueError):
        return jsonify(ok=False, error="Datos invalidos"), 400

    if not nombre or precio <= 0 or stock < 0:
        return jsonify(ok=False, error="Datos invalidos"), 400

    item = items_service.update_item(item_id, nombre, precio, stock)
    if not item:
        return jsonify(ok=False, error="Item no encontrado"), 404
    return jsonify(ok=True, item=item.to_dict())

