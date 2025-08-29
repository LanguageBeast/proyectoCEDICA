import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """
    Descripción:
    Clase base de configuración.

    ---------
    Atributos:
    - SECRET_KEY: str
        Clave secreta para proteger la sesión del usuario.

    - TESTING: bool
        Indica si la aplicación está en modo de pruebas.

    - SESSION_TYPE: str
        Tipo de sesión a utilizar.

    ----------
    """

    SECRET_KEY = os.getenv("SESSIONS_SECRET_KEY")
    TESTING = False
    SESSION_TYPE = os.environ.get("SESSIONS_SESSION_TYPE")
    BUCKET_NAME = "grupo07"


class ProductionConfig(Config):
    """
    Descripción:
    Configuración para producción.

    ---------
    Atributos:
    - MINIO_SERVER: str
        URL del servidor de MinIO.

    - MINIO_ACCESS_KEY: str
        Clave de acceso a MinIO.

    - MINIO_SECRET_KEY: str
        Clave secreta de MinIO.

    - MINIO_SECURE: bool
        Indica si la conexión a MinIO es segura.

    - SQLALCHEMY_DATABASE_URI: str
        URI de la base de datos.

    - SQLALCHEMY_ENGINE_OPTIONS: dict
        Opciones del motor de base de datos.

    ----------
    """

    MINIO_SERVER = os.environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")


class DevelopmentConfig(Config):
    """
    Descripción:
    Configuración para desarrollo.

    ---------
    Atributos:
    - MINIO_SERVER: str
        URL del servidor de MinIO.

    - MINIO_ACCESS_KEY: str
        Clave de acceso a MinIO.

    - MINIO_SECRET_KEY: str
        Clave secreta de MinIO.

    - MINIO_SECURE: bool
        Indica si la conexión a MinIO es segura.

    - DB_USER: str
        Usuario de la base de datos.

    - DB_PASSWORD: str
        Contraseña de la base de datos.

    - DB_HOST: str
        Host de la base de datos.

    - DB_PORT: str
        Puerto de la base de datos.

    - DB_NAME: str
        Nombre de la base de datos.

    - SQLALCHEMY_DATABASE_URI: str
        URI de la base de datos.

    ----------
    """
    SECRET_KEY = "dev"
    SESSION_TYPE = "filesystem"
    MINIO_SERVER = os.getenv("MINIO_SERVER")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
    MINIO_SECURE = False
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


class TestingConfig(Config):
    """
    Descripción:
    Configuración para pruebas.

    ---------
    Atributos:
    - TESTING: bool
        Indica si la aplicación está en modo de pruebas.

    ----------
    """

    TESTING = True


# Diccionario de configuraciones por entorno
config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig,
}
