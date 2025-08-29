from marshmallow import Schema
from marshmallow import fields
class ContentSchema(Schema):
    """
    Esquema de serialización y validación para los datos de un contenido.

    Campos:
    - id (int, solo lectura): Identificador único del contenido.
    - title (str, requerido): Título del contenido. Debe tener una longitud máxima de 100 caracteres.
    - summary (str, requerido): Resumen del contenido. Debe tener una longitud máxima de 255 caracteres.
    - content (str, requerido): Contenido completo. Debe tener una longitud máxima de 1000 caracteres.
    - author_alias (str, solo lectura): Alias del autor asociado al contenido.
        - Obtenido mediante el método `get_author_alias`.
    - published_at (datetime, opcional, solo lectura): Fecha y hora en que el contenido fue publicado.
    - updated_at (datetime, solo lectura): Fecha y hora de la última actualización del contenido.
    - status (str, requerido): Estado del contenido. Debe ser uno de los siguientes valores:
        - "Borrador"
        - "Publicado"
        - "Archivado"

    Métodos:
    - get_author_alias(obj):
        Obtiene el alias del autor asociado al contenido.
        - Parámetros:
            - obj: Instancia del contenido.
        - Retorna: Alias del autor si está disponible; de lo contrario, `None`.

    Instancias:
    - content_schema: Esquema para la serialización o deserialización de un único contenido.
    - contents_schema: Esquema para la serialización o deserialización de múltiples contenidos.

    Uso:
    - Serialización:
        Convierte objetos de contenido en formato JSON según las especificaciones del esquema.
    - Validación:
        Verifica que los datos ingresados cumplan con los requisitos establecidos en el esquema.
    """
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=lambda x: len(x) <= 100)
    summary = fields.Str(required=True, validate=lambda x: len(x) <= 255)
    content = fields.Str(required=True, validate=lambda x: len(x) <= 1000)
    author_alias = fields.Method("get_author_alias", dump_only=True) 
    published_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    status = fields.Str(required=True, validate=lambda x: x in ["Borrador", "Publicado", "Archivado"])

    def get_author_alias(self, obj):
        return obj.author.alias if obj.author else None

content_schema= ContentSchema()
contents_schema = ContentSchema(many=True)