"""Blueprint web (HTML)."""

from __future__ import annotations

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from ..controllers.cart import cart_service
from ..controllers.items import items_service
from ..controllers.users import users_service

# ! Blueprint para vistas HTML
web_bp = Blueprint("web", __name__)


def _is_admin() -> bool:
    return session.get("role") == "admin"


def _require_admin():
    if not session.get("user_id"):
        flash("Necesitas iniciar sesion para realizar esta accion.", "warning")
        return redirect(url_for("auth.login_view"))
    if not _is_admin():
        flash("Tu rol no tiene permisos para esta accion.", "warning")
        return redirect(url_for("web.home"))
    return None


def _require_login():
    if not session.get("user_id"):
        flash("Necesitas iniciar sesion para usar el carrito.", "warning")
        return redirect(url_for("auth.login_view"))
    return None


def _render_home(*, mensaje: str | None = None, item_edicion=None, search_query: str = ""):
    """Render de Home centralizado para reutilizar formulario crear/editar."""
    user_profile = None
    if session.get("user_id"):
        user_profile = users_service.get_user(int(session["user_id"]))
    normalized_query = search_query.strip()
    items = (
        items_service.search_items_by_name(normalized_query)
        if normalized_query
        else items_service.list_items()
    )
    return render_template(
        "index.html",
        title="Home",
        items=items,
        mensaje=mensaje,
        item_edicion=item_edicion,
        user_profile=user_profile,
        search_query=normalized_query,
        can_manage=_is_admin(),
    )


@web_bp.route("/")
def home():
    """Pagina principal: lista de items."""
    search_query = (request.args.get("q") or "").strip()
    editar = request.args.get("editar")
    item_edicion = None
    if editar is not None:
        if not _is_admin():
            flash("Solo un admin puede editar articulos.", "warning")
            return redirect(url_for("web.home"))
        try:
            item_id = int(editar)
        except ValueError:
            abort(400)
        item_edicion = items_service.get_item(item_id)
        if not item_edicion:
            abort(404)
    return _render_home(item_edicion=item_edicion, search_query=search_query)


@web_bp.route("/item/<int:item_id>")
def item_detalle(item_id: int):
    """Detalle de un item con control de errores."""
    item = items_service.get_item(item_id)
    if not item:
        abort(404)
    promedio = item.promedio_estrellas()
    return render_template(
        "detalle_item.html",
        title=f"Item {item_id}",
        item=item,
        promedio_estrellas=round(promedio, 1),
        promedio_redondeado=int(round(promedio)),
        total_resenas=len(item.resenas),
        can_manage=_is_admin(),
    )


@web_bp.route("/carrito")
def carrito_view():
    guard = _require_login()
    if guard:
        return guard
    user_id = int(session["user_id"])
    items = cart_service.get_cart_items(user_id)
    total = cart_service.cart_total(user_id)
    return render_template("cart.html", title="Carrito", cart_items=items, cart_total=total)


@web_bp.route("/carrito/add/<int:item_id>", methods=["POST"])
def carrito_add(item_id: int):
    guard = _require_login()
    if guard:
        return guard
    user_id = int(session["user_id"])
    ok, message = cart_service.add_item(user_id=user_id, item_id=item_id, cantidad=1)
    flash(message, "success" if ok else "danger")
    return redirect(request.referrer or url_for("web.home"))


@web_bp.route("/carrito/update/<int:item_id>", methods=["POST"])
def carrito_update(item_id: int):
    guard = _require_login()
    if guard:
        return guard
    user_id = int(session["user_id"])
    try:
        cantidad = int(request.form.get("cantidad") or 0)
    except ValueError:
        flash("Cantidad invalida.", "danger")
        return redirect(url_for("web.carrito_view"))
    ok, message = cart_service.set_quantity(user_id=user_id, item_id=item_id, cantidad=cantidad)
    flash(message, "success" if ok else "danger")
    return redirect(url_for("web.carrito_view"))


@web_bp.route("/carrito/remove/<int:item_id>", methods=["POST"])
def carrito_remove(item_id: int):
    guard = _require_login()
    if guard:
        return guard
    user_id = int(session["user_id"])
    ok, message = cart_service.remove_item(user_id=user_id, item_id=item_id)
    flash(message, "success" if ok else "danger")
    return redirect(url_for("web.carrito_view"))


@web_bp.route("/carrito/clear", methods=["POST"])
def carrito_clear():
    guard = _require_login()
    if guard:
        return guard
    user_id = int(session["user_id"])
    cart_service.clear_cart(user_id)
    flash("Carrito vaciado.", "info")
    return redirect(url_for("web.carrito_view"))


@web_bp.route("/about")
def about():
    """Pagina informativa."""
    return render_template("about.html", title="Acerca de")


@web_bp.route("/crear", methods=["POST"])
def crear_item():
    """Crea item rapido desde la portada (form simple)."""
    guard = _require_admin()
    if guard:
        return guard
    nombre = (request.form.get("nombre") or "").strip()
    try:
        precio = float(request.form.get("precio") or 0)
        stock = int(request.form.get("stock") or -1)
    except ValueError:
        flash("Datos invalidos. Revisa precio y stock.", "danger")
        return redirect(url_for("web.home"))
    if not nombre or precio <= 0 or stock < 0:
        flash("El nombre es obligatorio, precio > 0 y stock >= 0.", "danger")
        return redirect(url_for("web.home"))
    items_service.add_item(nombre, precio, stock)
    flash("Articulo creado correctamente.", "success")
    return redirect(url_for("web.home"))


@web_bp.route("/eliminar/<int:item_id>", methods=["POST"])
def eliminar_item(item_id: int):
    """Elimina un item por su ID."""
    guard = _require_admin()
    if guard:
        return guard
    eliminado = items_service.delete_item(item_id)
    if not eliminado:
        flash("No se encontro el articulo a eliminar.", "danger")
        return redirect(url_for("web.home"))
    flash("Articulo eliminado correctamente.", "success")
    return redirect(url_for("web.home"))


@web_bp.route("/editar/<int:item_id>", methods=["GET", "POST"])
def editar_item(item_id: int):
    """Edita un item existente usando el formulario reutilizado de Home."""
    guard = _require_admin()
    if guard:
        return guard
    item = items_service.get_item(item_id)
    if not item:
        abort(404)

    if request.method == "GET":
        return redirect(f"{url_for('web.home', editar=item_id)}#form-item")

    nombre = (request.form.get("nombre") or "").strip()
    try:
        precio = float(request.form.get("precio") or 0)
        stock = int(request.form.get("stock") or -1)
    except ValueError:
        flash("Datos invalidos. Revisa precio y stock.", "danger")
        return redirect(url_for("web.home", editar=item_id))

    if not nombre or precio <= 0 or stock < 0:
        flash("El nombre es obligatorio, precio > 0 y stock >= 0.", "danger")
        return redirect(url_for("web.home", editar=item_id))

    item_actualizado = items_service.update_item(
        item_id=item_id, nombre=nombre, precio=precio, stock=stock
    )
    if not item_actualizado:
        flash("No se encontro el articulo para actualizar.", "danger")
        return redirect(url_for("web.home"))
    flash("Articulo actualizado correctamente.", "success")
    return redirect(url_for("web.home"))


@web_bp.route("/item/<int:item_id>/resena", methods=["POST"])
def crear_resena(item_id: int):
    """Crea una resena para un item."""
    guard = _require_admin()
    if guard:
        return guard
    item = items_service.get_item(item_id)
    if not item:
        abort(404)

    autor = (request.form.get("autor") or "").strip()
    comentario = (request.form.get("comentario") or "").strip()
    try:
        estrellas = int(request.form.get("estrellas") or 0)
    except ValueError:
        flash("La puntuacion debe ser un numero valido.", "danger")
        return redirect(url_for("web.item_detalle", item_id=item_id))

    if not autor or not comentario or estrellas < 1 or estrellas > 5:
        flash("Completa nombre, comentario y una puntuacion de 1 a 5.", "danger")
        return redirect(url_for("web.item_detalle", item_id=item_id))

    creada = items_service.add_review(item_id, autor, comentario, estrellas)
    if not creada:
        flash("No se pudo crear la resena para este articulo.", "danger")
        return redirect(url_for("web.item_detalle", item_id=item_id))
    flash("Resena publicada correctamente.", "success")
    return redirect(url_for("web.item_detalle", item_id=item_id))

