from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def init_app(app):
    """
    Función que inicializa la extensión de Flask-Bcrypt
    Atributos: 
    - app: Flask
        Aplicación de Flask

    Retorna: None
    """
    bcrypt.init_app(app)
