"""Modelos simples (sin ORM) para la demo."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Review:
    """Resena de un producto."""

    autor: str
    comentario: str
    estrellas: int  # 1..5

    def to_dict(self) -> Dict[str, object]:
        return {
            "autor": self.autor,
            "comentario": self.comentario,
            "estrellas": self.estrellas,
        }


@dataclass
class Item:
    """Representa un item de inventario."""

    id: int
    nombre: str
    precio: float
    stock: int
    resenas: List[Review] = field(default_factory=list)

    def promedio_estrellas(self) -> float:
        """Promedio de estrellas para mostrar reputacion del producto."""
        if not self.resenas:
            return 0.0
        return sum(r.estrellas for r in self.resenas) / len(self.resenas)

    def to_dict(self) -> Dict[str, object]:
        """Convierte el item a dict para JSON o plantillas."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "promedio_estrellas": round(self.promedio_estrellas(), 1),
            "total_resenas": len(self.resenas),
        }


def seed_items() -> List[Item]:
    """Carga datos iniciales (mock)."""
    return [
        Item(
            id=1,
            nombre="Teclado mecanico",
            precio=89.99,
            stock=5,
            resenas=[
                Review(autor="Ana", comentario="Excelente tacto y muy comodo.", estrellas=5),
                Review(autor="Luis", comentario="Buena compra para jugar.", estrellas=4),
            ],
        ),
        Item(
            id=2,
            nombre="Mouse inalambrico",
            precio=29.50,
            stock=12,
            resenas=[Review(autor="Marta", comentario="Ligero y preciso.", estrellas=4)],
        ),
        Item(id=3, nombre="Monitor 24\"", precio=179.00, stock=4),
    ]

