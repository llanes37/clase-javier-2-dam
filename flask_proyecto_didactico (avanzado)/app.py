# =========================================================================================
#  "YO! FLASK DIDACTICO (AVANZADO)" - Estructura MVC ligera con Blueprints
#  ---------------------------------------------------------------------------------
#  En esta version practicaras:
#    * App factory y configuracion separada
#    * Blueprints para web y API
#    * Controladores/servicios (capa de negocio) y modelos simples
#    * Formularios, plantillas y JSON
#    * Better Comments (# ! # * # ? TODO) en todo el proyecto
#
#  Como ejecutar (Windows):
#    1) python -m venv env
#    2) .\\env\\Scripts\\activate
#    3) pip install flask
#    4) python app.py
#    5) Ir a http://127.0.0.1:5000/
#
#  Estructura:
#    app.py                  -> Punto de entrada
#    proyecto_avanzado/
#      __init__.py           -> create_app y registro de blueprints
#      config.py             -> Config desarrollo/produccion
#      models.py             -> Modelos simples (Item)
#      controllers/items.py  -> Logica de negocio CRUD en memoria
#      routes/web.py         -> Rutas HTML (home, detalle)
#      routes/api.py         -> Rutas API JSON (items)
#      templates/            -> Plantillas Jinja2
# =========================================================================================

from proyecto_avanzado import create_app


# ! Crear app usando app factory
app = create_app()


if __name__ == "__main__":
    # ! MODO DEBUG
    print("=" * 80)
    print(">> Flask Avanzado (MVC ligero) iniciandose...")
    print(">> URL: http://127.0.0.1:5000/")
    print("=" * 80)
    app.run(debug=app.config["DEBUG"])

