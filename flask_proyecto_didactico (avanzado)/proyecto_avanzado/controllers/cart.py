"""Servicio de carrito persistido en SQLite."""

from __future__ import annotations

from typing import Dict, List, Tuple

from .db import get_conn


class CartService:
    """Gestiona carrito por usuario."""

    def __init__(self) -> None:
        self._init_db()

    def _init_db(self) -> None:
        with get_conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS carts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cart_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cart_id INTEGER NOT NULL,
                    item_id INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL DEFAULT 1 CHECK (cantidad > 0),
                    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
                    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
                    UNIQUE(cart_id, item_id)
                );
                """
            )
            conn.commit()

    def _get_or_create_cart_id(self, user_id: int) -> int:
        with get_conn() as conn:
            row = conn.execute("SELECT id FROM carts WHERE user_id = ?", (user_id,)).fetchone()
            if row:
                return int(row["id"])
            cursor = conn.execute("INSERT INTO carts (user_id) VALUES (?)", (user_id,))
            conn.commit()
            return int(cursor.lastrowid)

    def add_item(self, user_id: int, item_id: int, cantidad: int = 1) -> Tuple[bool, str]:
        if cantidad <= 0:
            return False, "Cantidad invalida."
        cart_id = self._get_or_create_cart_id(user_id)
        with get_conn() as conn:
            item_row = conn.execute(
                "SELECT id, stock, nombre FROM items WHERE id = ?",
                (item_id,),
            ).fetchone()
            if not item_row:
                return False, "El articulo no existe."
            stock = int(item_row["stock"])
            nombre = str(item_row["nombre"])
            if stock <= 0:
                return False, f'"{nombre}" no tiene stock disponible.'

            current_row = conn.execute(
                "SELECT cantidad FROM cart_items WHERE cart_id = ? AND item_id = ?",
                (cart_id, item_id),
            ).fetchone()
            current_qty = int(current_row["cantidad"]) if current_row else 0
            new_qty = current_qty + cantidad
            if new_qty > stock:
                return False, f'Stock insuficiente para "{nombre}". Maximo disponible: {stock}.'

            conn.execute(
                """
                INSERT INTO cart_items (cart_id, item_id, cantidad)
                VALUES (?, ?, ?)
                ON CONFLICT(cart_id, item_id)
                DO UPDATE SET cantidad = excluded.cantidad
                """,
                (cart_id, item_id, new_qty),
            )
            conn.commit()
        return True, "Articulo agregado al carrito."

    def set_quantity(self, user_id: int, item_id: int, cantidad: int) -> Tuple[bool, str]:
        cart_id = self._get_or_create_cart_id(user_id)
        with get_conn() as conn:
            item_row = conn.execute(
                "SELECT stock, nombre FROM items WHERE id = ?",
                (item_id,),
            ).fetchone()
            if not item_row:
                return False, "El articulo no existe."
            stock = int(item_row["stock"])
            nombre = str(item_row["nombre"])

            if cantidad <= 0:
                conn.execute(
                    "DELETE FROM cart_items WHERE cart_id = ? AND item_id = ?",
                    (cart_id, item_id),
                )
                conn.commit()
                return True, "Articulo eliminado del carrito."

            if cantidad > stock:
                return False, f'Stock insuficiente para "{nombre}". Maximo disponible: {stock}.'

            updated = conn.execute(
                """
                UPDATE cart_items
                SET cantidad = ?
                WHERE cart_id = ? AND item_id = ?
                """,
                (cantidad, cart_id, item_id),
            )
            conn.commit()
            if updated.rowcount == 0:
                return False, "El articulo no estaba en el carrito."
        return True, "Cantidad actualizada."

    def remove_item(self, user_id: int, item_id: int) -> Tuple[bool, str]:
        cart_id = self._get_or_create_cart_id(user_id)
        with get_conn() as conn:
            deleted = conn.execute(
                "DELETE FROM cart_items WHERE cart_id = ? AND item_id = ?",
                (cart_id, item_id),
            )
            conn.commit()
            if deleted.rowcount == 0:
                return False, "El articulo no estaba en el carrito."
        return True, "Articulo eliminado del carrito."

    def clear_cart(self, user_id: int) -> None:
        cart_id = self._get_or_create_cart_id(user_id)
        with get_conn() as conn:
            conn.execute("DELETE FROM cart_items WHERE cart_id = ?", (cart_id,))
            conn.commit()

    def get_cart_items(self, user_id: int) -> List[Dict[str, object]]:
        cart_id = self._get_or_create_cart_id(user_id)
        with get_conn() as conn:
            rows = conn.execute(
                """
                SELECT
                    i.id AS item_id,
                    i.nombre AS nombre,
                    i.precio AS precio,
                    i.stock AS stock,
                    c.cantidad AS cantidad
                FROM cart_items c
                JOIN items i ON i.id = c.item_id
                WHERE c.cart_id = ?
                ORDER BY c.id DESC
                """,
                (cart_id,),
            ).fetchall()
        result: List[Dict[str, object]] = []
        for row in rows:
            precio = float(row["precio"])
            cantidad = int(row["cantidad"])
            subtotal = precio * cantidad
            result.append(
                {
                    "item_id": int(row["item_id"]),
                    "nombre": row["nombre"],
                    "precio": precio,
                    "stock": int(row["stock"]),
                    "cantidad": cantidad,
                    "subtotal": subtotal,
                }
            )
        return result

    def cart_count(self, user_id: int) -> int:
        cart_id = self._get_or_create_cart_id(user_id)
        with get_conn() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(cantidad), 0) AS total FROM cart_items WHERE cart_id = ?",
                (cart_id,),
            ).fetchone()
            return int(row["total"])

    def cart_total(self, user_id: int) -> float:
        items = self.get_cart_items(user_id)
        return sum(float(item["subtotal"]) for item in items)


cart_service = CartService()
