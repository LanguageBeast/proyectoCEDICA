# Esta clase se usará para obtener los documentos cargados que no sean links

from flask import current_app
from src.core.config import Config
from datetime import timedelta

def document_url(document):
    """
    Función que obtiene la URL de un documento cargado
    Parámetros:
        - document (str): Documento cargado
    Retorna:
        - client.presigned_get_object("grupo07", document, expires=3600): 
        URL del documento cargado
    """
    if not document:
        return None
    client = current_app.storage.client
    expires = timedelta(hours=1)
    return client.presigned_get_object(Config.BUCKET_NAME, document, expires=expires)
