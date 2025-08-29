from src.web import create_app

app = create_app()
app.testing = True

# client en éste caso estaría reemplazando al navegador.
client = app.test_client()


def test_web():
    """
    Función que prueba la ruta raíz de la aplicación web.
    """
    response = client.get("/")
    assert 200 == response.status_code
    assert b"Hola mundo!" in response.data
