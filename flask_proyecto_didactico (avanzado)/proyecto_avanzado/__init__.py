"""App factory y registro de blueprints (estructura MVC ligera)."""

from __future__ import annotations

from flask import Flask

from .config import DevConfig
from .routes.api import api_bp
from .routes.web import web_bp


def create_app() -> Flask:
    """Crea la aplicacion Flask con configuracion y blueprints."""
    app = Flask(__name__, template_folder="templates")

    # * Cargar configuracion (podrias cambiar a ProdConfig en despliegue)
    app.config.from_object(DevConfig)

    # ! Registrar blueprints
    app.register_blueprint(web_bp)  # HTML
    app.register_blueprint(api_bp, url_prefix="/api")  # JSON

    # ? Hook simple para logs de rutas
    @app.before_request
    def _log_request():  # type: ignore[no-untyped-def]
        if app.config.get("ECHO_LOGS", False):
            from flask import request

            print(f"[REQ] {request.method} {request.path}")

    return app

