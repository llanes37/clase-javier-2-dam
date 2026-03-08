"""Modelos simples (sin ORM) para la demo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Item:
    """Representa un item de inventario."""

    id: int
    nombre: str
    precio: float
    stock: int

    def to_dict(self) -> Dict[str, object]:
        """Convierte el item a dict para JSON o plantillas."""
        return {"id": self.id, "nombre": self.nombre, "precio": self.precio, "stock": self.stock}


def seed_items() -> List[Item]:
    """Carga datos iniciales (mock)."""
    return [
        Item(id=1, nombre="Teclado mecanico", precio=89.99, stock=5),
        Item(id=2, nombre="Mouse inalambrico", precio=29.50, stock=12),
        Item(id=3, nombre="Monitor 24\"", precio=179.00, stock=4),
    ]

