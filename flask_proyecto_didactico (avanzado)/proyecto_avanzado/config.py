"""Configuraciones separadas (desarrollo/produccion)."""


class BaseConfig:
    # * Config comun
    SECRET_KEY = "dev-key"  # ! Cambia en produccion
    JSON_AS_ASCII = False
    TEMPLATES_AUTO_RELOAD = True
    ECHO_LOGS = True
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024


class DevConfig(BaseConfig):
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False

