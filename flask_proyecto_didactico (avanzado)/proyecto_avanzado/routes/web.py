"""Blueprint web (HTML)."""

from __future__ import annotations

from flask import Blueprint, abort, render_template, request, url_for

from ..controllers.items import items_service

# ! Blueprint para vistas HTML
web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def home():
    """Pagina principal: lista de items."""
    items = items_service.list_items()
    return render_template("index.html", title="Home", items=items)


@web_bp.route("/item/<int:item_id>")
def item_detalle(item_id: int):
    """Detalle de un item con control de errores."""
    item = items_service.get_item(item_id)
    if not item:
        abort(404)
    return render_template("detalle_item.html", title=f"Item {item_id}", item=item)


@web_bp.route("/about")
def about():
    """Pagina informativa."""
    return render_template("about.html", title="Acerca de")


@web_bp.route("/crear", methods=["POST"])
def crear_item():
    """Crea item rapido desde la portada (form simple)."""
    nombre = (request.form.get("nombre") or "").strip()
    precio = float(request.form.get("precio") or 0)
    stock = int(request.form.get("stock") or 0)
    if not nombre or precio <= 0:
        # ? en un curso real agregarias flash() y redireccion con mensaje
        abort(400)
    items_service.add_item(nombre, precio, stock)
    return render_template(
        "index.html",
        title="Home",
        items=items_service.list_items(),
        mensaje="Item creado!",
        url_home=url_for("web.home"),
    )

