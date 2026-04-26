"""Controlador/servicio para items persistidos en SQLite."""

from __future__ import annotations

import sqlite3
from typing import Dict, List, Optional

from ..models import Item, Review, seed_items
from .db import get_conn


class ItemService:
    """Gestiona items y reseñas en SQLite."""

    def __init__(self) -> None:
        self._init_db()
        self._seed_if_empty()

    def _get_conn(self) -> sqlite3.Connection:
        return get_conn()

    def _init_db(self) -> None:
        with self._get_conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL,
                    stock INTEGER NOT NULL DEFAULT 0
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    autor TEXT NOT NULL,
                    comentario TEXT NOT NULL,
                    estrellas INTEGER NOT NULL CHECK (estrellas BETWEEN 1 AND 5),
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
                );
                """
            )
            conn.commit()

    def _seed_if_empty(self) -> None:
        with self._get_conn() as conn:
            current_count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
            if current_count > 0:
                return
            for item in seed_items():
                cursor = conn.execute(
                    "INSERT INTO items (nombre, precio, stock) VALUES (?, ?, ?)",
                    (item.nombre, item.precio, item.stock),
                )
                item_id = int(cursor.lastrowid)
                for review in item.resenas:
                    conn.execute(
                        """
                        INSERT INTO reviews (item_id, autor, comentario, estrellas)
                        VALUES (?, ?, ?, ?)
                        """,
                        (item_id, review.autor, review.comentario, review.estrellas),
                    )
            conn.commit()

    def _get_reviews_for_item(self, conn: sqlite3.Connection, item_id: int) -> List[Review]:
        rows = conn.execute(
            """
            SELECT autor, comentario, estrellas
            FROM reviews
            WHERE item_id = ?
            ORDER BY id DESC
            """,
            (item_id,),
        ).fetchall()
        return [
            Review(autor=row["autor"], comentario=row["comentario"], estrellas=row["estrellas"])
            for row in rows
        ]

    def _row_to_item(self, conn: sqlite3.Connection, row: sqlite3.Row) -> Item:
        return Item(
            id=row["id"],
            nombre=row["nombre"],
            precio=row["precio"],
            stock=row["stock"],
            resenas=self._get_reviews_for_item(conn, row["id"]),
        )

    def list_items(self) -> List[Item]:
        with self._get_conn() as conn:
            rows = conn.execute("SELECT id, nombre, precio, stock FROM items ORDER BY id").fetchall()
            return [self._row_to_item(conn, row) for row in rows]

    def search_items_by_name(self, query: str) -> List[Item]:
        """Busca items por nombre (case-insensitive)."""
        normalized_query = query.strip()
        if not normalized_query:
            return self.list_items()
        with self._get_conn() as conn:
            # Busqueda parcial sin distinguir mayusculas/minusculas.
            # Ejemplo: "tec" encuentra "Teclado".
            rows = conn.execute(
                """
                SELECT id, nombre, precio, stock
                FROM items
                WHERE nombre LIKE ? COLLATE NOCASE
                ORDER BY id
                """,
                (f"%{normalized_query}%",),
            ).fetchall()
            return [self._row_to_item(conn, row) for row in rows]

    def get_item(self, item_id: int) -> Optional[Item]:
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT id, nombre, precio, stock FROM items WHERE id = ?",
                (item_id,),
            ).fetchone()
            if not row:
                return None
            return self._row_to_item(conn, row)

    def add_item(self, nombre: str, precio: float, stock: int) -> Item:
        with self._get_conn() as conn:
            cursor = conn.execute(
                "INSERT INTO items (nombre, precio, stock) VALUES (?, ?, ?)",
                (nombre, precio, stock),
            )
            conn.commit()
            item_id = int(cursor.lastrowid)
        created_item = self.get_item(item_id)
        if not created_item:
            raise RuntimeError("No se pudo recuperar el item creado.")
        return created_item

    def update_stock(self, item_id: int, stock: int) -> Optional[Item]:
        with self._get_conn() as conn:
            cursor = conn.execute("UPDATE items SET stock = ? WHERE id = ?", (stock, item_id))
            conn.commit()
            if cursor.rowcount == 0:
                return None
        return self.get_item(item_id)

    def update_item(self, item_id: int, nombre: str, precio: float, stock: int) -> Optional[Item]:
        """Actualiza todos los campos editables de un item."""
        with self._get_conn() as conn:
            cursor = conn.execute(
                "UPDATE items SET nombre = ?, precio = ?, stock = ? WHERE id = ?",
                (nombre, precio, stock, item_id),
            )
            conn.commit()
            if cursor.rowcount == 0:
                return None
        return self.get_item(item_id)

    def delete_item(self, item_id: int) -> bool:
        """Elimina un item por su ID. Retorna True si se eliminó."""
        with self._get_conn() as conn:
            cursor = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
            conn.commit()
            return cursor.rowcount > 0

    def add_review(self, item_id: int, autor: str, comentario: str, estrellas: int) -> Optional[Review]:
        """Agrega una reseña a un item."""
        with self._get_conn() as conn:
            item_exists = conn.execute("SELECT 1 FROM items WHERE id = ?", (item_id,)).fetchone()
            if not item_exists:
                return None
            conn.execute(
                """
                INSERT INTO reviews (item_id, autor, comentario, estrellas)
                VALUES (?, ?, ?, ?)
                """,
                (item_id, autor, comentario, estrellas),
            )
            conn.commit()
        return Review(autor=autor, comentario=comentario, estrellas=estrellas)

    def to_dict_list(self) -> List[Dict[str, object]]:
        """Devuelve items como lista de dicts (para JSON)."""
        return [item.to_dict() for item in self.list_items()]


# * Instancia global para usar en rutas
items_service = ItemService()

