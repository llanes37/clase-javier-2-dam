"""App factory y registro de blueprints (estructura MVC ligera)."""

from __future__ import annotations

from flask import Flask

from .controllers.cart import cart_service
from .config import DevConfig
from .routes.auth import auth_bp
from .routes.api import api_bp
from .routes.web import web_bp


def create_app() -> Flask:
    """Crea la aplicacion Flask con configuracion y blueprints."""
    app = Flask(__name__, template_folder="templates")

    # * Cargar configuracion (podrias cambiar a ProdConfig en despliegue)
    app.config.from_object(DevConfig)

    # ! Registrar blueprints
    app.register_blueprint(web_bp)  # HTML
    app.register_blueprint(auth_bp, url_prefix="/auth")  # Auth
    app.register_blueprint(api_bp, url_prefix="/api")  # JSON

    @app.context_processor
    def inject_cart_badge():  # type: ignore[no-untyped-def]
        from flask import session

        user_id = session.get("user_id")
        if not user_id:
            return {"cart_badge_count": 0}
        return {"cart_badge_count": cart_service.cart_count(int(user_id))}

    # ? Hook simple para logs de rutas
    @app.before_request
    def _log_request():  # type: ignore[no-untyped-def]
        if app.config.get("ECHO_LOGS", False):
            from flask import request

            print(f"[REQ] {request.method} {request.path}")

    return app

