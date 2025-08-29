from minio import Minio


class Storage:
    """
    Descripción:
    Una clase que representa el almacenamiento de archivos en Minio.
    """

    def __init__(self, app=None):
        self._client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """ Inicializa el cliente de Minio y lo adjunta a la aplicación de Flask """
        minio_server = app.config.get('MINIO_SERVER')
        access_key = app.config.get('MINIO_ACCESS_KEY')
        secret_key = app.config.get('MINIO_SECRET_KEY')
        secure = app.config.get('MINIO_SECURE', True)
        # para localhost
        # secure = app.config.get('MINIO_SECURE', False)

        # Inicializa el cliente de Minio
        self._client = Minio(
            minio_server, access_key=access_key, secret_key=secret_key, secure=True
        )
        # para localhost
        # self._client = Minio(
        #     minio_server, access_key=access_key, secret_key=secret_key, secure=False
        # )

        # Adjunta el cliente de Minio a la aplicación de Flask
        app.storage = self

        return app

    @property
    def client(self):
        """ Retorna el cliente de Minio """
        return self._client

    @client.setter
    def client(self, value):
        """ Establece el cliente de Minio """
        self._client = value


storage = Storage()
