"""Servicio alternativo con SQLite (pendiente de activar manualmente).

# TODO: Para usar este servicio en lugar del de memoria:
#   1) Crea la base y tabla con init_db().
#   2) En web.py y api.py importa y usa SqliteItemService en vez de items_service.
#   3) Ajusta rutas si quieres persistir datos reales.
#
# Nota: mantenemos la logica parecida al servicio en memoria para que sea intercambiable.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, List, Optional

DB_PATH = Path(__file__).resolve().parents[1] / "instance" / "items.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_conn() -> sqlite3.Connection:
    """Obtiene conexion SQLite (row_factory a dict)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Crea tabla si no existe."""
    with get_conn() as conn:
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
        conn.commit()


class SqliteItemService:
    """CRUD usando SQLite."""

    def list_items(self) -> List[Dict[str, object]]:
        with get_conn() as conn:
            rows = conn.execute("SELECT id, nombre, precio, stock FROM items ORDER BY id").fetchall()
            return [dict(r) for r in rows]

    def get_item(self, item_id: int) -> Optional[Dict[str, object]]:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT id, nombre, precio, stock FROM items WHERE id = ?", (item_id,)
            ).fetchone()
            return dict(row) if row else None

    def add_item(self, nombre: str, precio: float, stock: int) -> Dict[str, object]:
        with get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO items (nombre, precio, stock) VALUES (?, ?, ?)",
                (nombre, precio, stock),
            )
            conn.commit()
            new_id = cur.lastrowid
            return {"id": new_id, "nombre": nombre, "precio": precio, "stock": stock}

    def update_stock(self, item_id: int, stock: int) -> Optional[Dict[str, object]]:
        with get_conn() as conn:
            conn.execute("UPDATE items SET stock = ? WHERE id = ?", (stock, item_id))
            conn.commit()
            return self.get_item(item_id)

# * Instancia opcional (solo si activas SQLite)
sqlite_items_service = SqliteItemService()

