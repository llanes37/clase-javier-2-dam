"""Blueprint de autenticacion y sesion de usuarios."""

from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, session, url_for

from ..controllers.users import users_service

auth_bp = Blueprint("auth", __name__)


def _set_user_session(
    user_id: int, username: str, display_name: str, avatar_path: str | None, role: str
) -> None:
    session["user_id"] = user_id
    session["username"] = username
    session["display_name"] = display_name
    session["avatar_path"] = avatar_path
    session["role"] = role


@auth_bp.get("/register")
def register_view():
    return render_template("register.html", title="Registro", selected_role="usuario")


@auth_bp.post("/register")
def register_action():
    username = (request.form.get("username") or "").strip().lower()
    display_name = (request.form.get("display_name") or "").strip()
    bio = (request.form.get("bio") or "").strip()
    password = request.form.get("password") or ""
    password_confirm = request.form.get("password_confirm") or ""
    role = (request.form.get("role") or "usuario").strip().lower()
    remember_quick = (request.form.get("remember_quick") or "") == "on"
    avatar = request.files.get("avatar")

    if (
        not username
        or not display_name
        or len(password) < 6
        or password != password_confirm
        or role not in {"usuario", "admin"}
    ):
        return render_template(
            "register.html",
            title="Registro",
            error="Revisa los datos: usuario, nombre visible y contrasena valida.",
            selected_role=role,
        )

    user = users_service.create_user(
        username=username,
        password=password,
        display_name=display_name,
        bio=bio,
        avatar=avatar,
        role=role,
    )
    if not user:
        return render_template(
            "register.html",
            title="Registro",
            error="No se pudo crear el usuario. Puede que el nombre ya exista.",
            selected_role=role,
        )

    _set_user_session(user.id, user.username, user.display_name, user.avatar_path, user.role)
    if remember_quick:
        users_service.remember_user_for_quick_login(user.id)
    return redirect(url_for("web.home"))


@auth_bp.get("/login")
def login_view():
    quick_users = users_service.list_quick_login_users()
    return render_template("login.html", title="Iniciar sesion", quick_users=quick_users)


@auth_bp.post("/login")
def login_action():
    username = (request.form.get("username") or "").strip().lower()
    password = request.form.get("password") or ""
    remember_quick = (request.form.get("remember_quick") or "") == "on"

    user = users_service.verify_credentials(username=username, password=password)
    if not user:
        return render_template(
            "login.html",
            title="Iniciar sesion",
            error="Usuario o contrasena incorrectos.",
            quick_users=users_service.list_quick_login_users(),
        )

    _set_user_session(user.id, user.username, user.display_name, user.avatar_path, user.role)
    if remember_quick:
        users_service.remember_user_for_quick_login(user.id)
    return redirect(url_for("web.home"))


@auth_bp.get("/quick-login/<int:user_id>")
def quick_login_view(user_id: int):
    if not users_service.is_quick_login_user(user_id):
        return redirect(url_for("auth.login_view"))
    user = users_service.get_user(user_id)
    if not user:
        return redirect(url_for("auth.login_view"))
    return render_template("quick_login.html", title="Acceso rapido", user=user)


@auth_bp.post("/quick-login/<int:user_id>")
def quick_login_action(user_id: int):
    if not users_service.is_quick_login_user(user_id):
        return redirect(url_for("auth.login_view"))
    password = request.form.get("password") or ""
    user = users_service.verify_password_for_user(user_id=user_id, password=password)
    if not user:
        user_found = users_service.get_user(user_id)
        return render_template(
            "quick_login.html",
            title="Acceso rapido",
            user=user_found,
            error="Contrasena incorrecta.",
        )
    _set_user_session(user.id, user.username, user.display_name, user.avatar_path, user.role)
    return redirect(url_for("web.home"))


@auth_bp.post("/quick-login/<int:user_id>/remove")
def quick_login_remove(user_id: int):
    users_service.remove_quick_login_user(user_id)
    return redirect(url_for("auth.login_view"))


@auth_bp.post("/logout")
def logout_action():
    session.clear()
    return redirect(url_for("auth.login_view"))
