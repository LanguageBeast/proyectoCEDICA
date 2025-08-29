from src.web import create_app

app = create_app()

if __name__ == '__main__':
    """
    Función principal que ejecuta la aplicación web.
    """
    # app.run(debug=True)
    app.run(ssl_context='adhoc')
