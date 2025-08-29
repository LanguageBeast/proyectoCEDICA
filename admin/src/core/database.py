from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


db = SQLAlchemy()


def init_app(app):
    """
    Funcion de inicializacion de la base de datos
    Atributos:
    - app: Aplicacion de Flask
    Retorna: Aplicacion de Flask
    """
    db.init_app(app)
    config(app)

    return app


def config(app):
    """
    Funcion de configuracion de la base de datos
    Atributos:
    - app: Aplicacion de Flask
    Retorna: Aplicacion de Flask
    """

    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.close()

    return app


def reset():
    """
    Funcion de reseteo de la base de datos
    Atributos: None
    Retorna: None
    """
    print("Eliminado base de datos...")
    db.session.execute(text("DROP SCHEMA public CASCADE"))
    db.session.execute(text("CREATE SCHEMA public"))
    db.session.commit()
    print("Creando base de datos...")
    db.create_all()
    print("Done!")
