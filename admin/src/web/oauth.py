from authlib.integrations.flask_client import OAuth

oauth = OAuth()


def configure_oauth(app):
    # Inicializa OAuth con la aplicación Flask
    oauth.init_app(app)

    # Configuración de Google OAuth
    oauth.register(
        name="google",
        client_id=app.config.get("GOOGLE_CLIENT_ID"),
        client_secret=app.config.get("GOOGLE_CLIENT_SECRET"),
        # authorize_url="https://accounts.google.com/o/oauth2/auth",
        # access_token_url="https://accounts.google.com/o/oauth2/token",
        redirect_uri=app.config.get("GOOGLE_REDIRECT_URI"),
        client_kwargs={"scope": "openid profile email"},
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    )
