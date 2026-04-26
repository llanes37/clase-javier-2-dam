"""Servicio de usuarios y login rapido persistido en SQLite."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from uuid import uuid4

from werkzeug.datastructures import FileStorage
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from .db import get_conn

AVATAR_REL_DIR = "avatars"
ALLOWED_AVATAR_EXTS = {"png", "jpg", "jpeg", "webp"}


@dataclass
class User:
    id: int
    username: str
    display_name: str
    bio: str
    avatar_path: Optional[str]
    role: str


class UserService:
    """CRUD de usuarios y opciones de login rapido."""

    def __init__(self, static_root: Path) -> None:
        self._avatar_dir = static_root / AVATAR_REL_DIR
        self._avatar_dir.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with get_conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    bio TEXT NOT NULL DEFAULT '',
                    avatar_path TEXT,
                    role TEXT NOT NULL DEFAULT 'usuario' CHECK (role IN ('usuario', 'admin')),
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            existing_columns = {
                row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()
            }
            if "role" not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'usuario'")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS quick_login_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
                """
            )
            conn.commit()

    def _row_to_user(self, row) -> User:
        return User(
            id=row["id"],
            username=row["username"],
            display_name=row["display_name"],
            bio=row["bio"],
            avatar_path=row["avatar_path"],
            role=row["role"],
        )

    def _save_avatar(self, avatar: FileStorage | None) -> Optional[str]:
        if not avatar or not avatar.filename:
            return None
        filename = secure_filename(avatar.filename)
        if "." not in filename:
            return None
        ext = filename.rsplit(".", 1)[1].lower()
        if ext not in ALLOWED_AVATAR_EXTS:
            return None
        final_name = f"{uuid4().hex}.{ext}"
        target = self._avatar_dir / final_name
        avatar.save(target)
        return f"{AVATAR_REL_DIR}/{final_name}"

    def create_user(
        self,
        username: str,
        password: str,
        display_name: str,
        bio: str,
        avatar: FileStorage | None,
        role: str,
    ) -> Optional[User]:
        if role not in {"usuario", "admin"}:
            return None
        avatar_path = self._save_avatar(avatar)
        with get_conn() as conn:
            try:
                cursor = conn.execute(
                    """
                    INSERT INTO users (username, password_hash, display_name, bio, avatar_path, role)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        username,
                        generate_password_hash(password),
                        display_name,
                        bio,
                        avatar_path,
                        role,
                    ),
                )
                conn.commit()
            except sqlite3.IntegrityError:
                return None
            user_id = int(cursor.lastrowid)
        return self.get_user(user_id)

    def get_user(self, user_id: int) -> Optional[User]:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT id, username, display_name, bio, avatar_path, role FROM users WHERE id = ?",
                (user_id,),
            ).fetchone()
            if not row:
                return None
            return self._row_to_user(row)

    def get_user_by_username(self, username: str) -> Optional[User]:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT id, username, display_name, bio, avatar_path, role FROM users WHERE username = ?",
                (username,),
            ).fetchone()
            if not row:
                return None
            return self._row_to_user(row)

    def verify_credentials(self, username: str, password: str) -> Optional[User]:
        with get_conn() as conn:
            row = conn.execute(
                """
                SELECT id, username, display_name, bio, avatar_path, role, password_hash
                FROM users
                WHERE username = ?
                """,
                (username,),
            ).fetchone()
            if not row:
                return None
            if not check_password_hash(row["password_hash"], password):
                return None
            return self._row_to_user(row)

    def verify_password_for_user(self, user_id: int, password: str) -> Optional[User]:
        with get_conn() as conn:
            row = conn.execute(
                """
                SELECT id, username, display_name, bio, avatar_path, role, password_hash
                FROM users
                WHERE id = ?
                """,
                (user_id,),
            ).fetchone()
            if not row:
                return None
            if not check_password_hash(row["password_hash"], password):
                return None
            return self._row_to_user(row)

    def remember_user_for_quick_login(self, user_id: int) -> None:
        with get_conn() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO quick_login_users (user_id) VALUES (?)",
                (user_id,),
            )
            conn.commit()

    def list_quick_login_users(self) -> List[User]:
        with get_conn() as conn:
            rows = conn.execute(
                """
                SELECT u.id, u.username, u.display_name, u.bio, u.avatar_path, u.role
                FROM quick_login_users q
                JOIN users u ON u.id = q.user_id
                ORDER BY q.created_at DESC
                """
            ).fetchall()
            return [self._row_to_user(row) for row in rows]

    def is_quick_login_user(self, user_id: int) -> bool:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT 1 FROM quick_login_users WHERE user_id = ?",
                (user_id,),
            ).fetchone()
            return row is not None

    def remove_quick_login_user(self, user_id: int) -> None:
        with get_conn() as conn:
            conn.execute("DELETE FROM quick_login_users WHERE user_id = ?", (user_id,))
            conn.commit()


users_service = UserService(static_root=Path(__file__).resolve().parents[1] / "static")
