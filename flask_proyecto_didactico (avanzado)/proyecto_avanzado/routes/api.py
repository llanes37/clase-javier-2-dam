"""Blueprint API (JSON)."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from ..controllers.items import items_service

# ! Blueprint para API JSON
api_bp = Blueprint("api", __name__)


@api_bp.get("/items")
def api_list_items():
    """Lista de items en JSON."""
    return jsonify(ok=True, items=items_service.to_dict_list())


@api_bp.get("/items/<int:item_id>")
def api_get_item(item_id: int):
    """Detalle de item."""
    item = items_service.get_item(item_id)
    if not item:
        return jsonify(ok=False, error="Item no encontrado"), 404
    return jsonify(ok=True, item=item.to_dict())


@api_bp.post("/items")
def api_create_item():
    """Crea item via JSON."""
    data = request.get_json(silent=True) or {}
    nombre = str(data.get("nombre", "")).strip()
    precio = float(data.get("precio") or 0)
    stock = int(data.get("stock") or 0)

    if not nombre or precio <= 0:
        return jsonify(ok=False, error="Datos invalidos"), 400

    item = items_service.add_item(nombre, precio, stock)
    return jsonify(ok=True, item=item.to_dict()), 201


@api_bp.patch("/items/<int:item_id>/stock")
def api_update_stock(item_id: int):
    """Actualiza stock."""
    data = request.get_json(silent=True) or {}
    stock = int(data.get("stock") or -1)
    if stock < 0:
        return jsonify(ok=False, error="Stock debe ser >= 0"), 400
    item = items_service.update_stock(item_id, stock)
    if not item:
        return jsonify(ok=False, error="Item no encontrado"), 404
    return jsonify(ok=True, item=item.to_dict())

