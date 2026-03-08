"""Controlador/servicio para items (CRUD en memoria)."""

from __future__ import annotations

from typing import Dict, List, Optional

from ..models import Item, seed_items


class ItemService:
    """Gestiona items en memoria (demo)."""

    def __init__(self) -> None:
        # * Data store en memoria
        self._items: List[Item] = seed_items()
        self._next_id = max(i.id for i in self._items) + 1 if self._items else 1

    # ! CRUD basico ---------------------------------------------------------
    def list_items(self) -> List[Item]:
        return list(self._items)

    def get_item(self, item_id: int) -> Optional[Item]:
        return next((i for i in self._items if i.id == item_id), None)

    def add_item(self, nombre: str, precio: float, stock: int) -> Item:
        nuevo = Item(id=self._next_id, nombre=nombre, precio=precio, stock=stock)
        self._items.append(nuevo)
        self._next_id += 1
        return nuevo

    def update_stock(self, item_id: int, stock: int) -> Optional[Item]:
        item = self.get_item(item_id)
        if item:
            item.stock = stock
        return item

    # ? Helpers -------------------------------------------------------------
    def to_dict_list(self) -> List[Dict[str, object]]:
        """Devuelve items como lista de dicts (para JSON)."""
        return [i.to_dict() for i in self._items]


# * Instancia global (simple) para usar en rutas
items_service = ItemService()

