from datetime import datetime
from src.core.database import db


class ContentPost(db.Model):
    """
    Descripción: 
    Una clase que representa la entidad Contenido de la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único del contenido.

    - title: str
        Titulo del contenido.
        restricciones -> longitud máxima de 100 caracteres, no nulo

    - summary: str
        Copete del contenido.
        restricciones -> longitud máxima de 255 caracteres

    - content: str
        Contenido(texto enriquecido) del contenido.
    
    - status: str
        Estado del contenido.
        restricciones -> no nulo
    
    - author_id: int
        Clave foránea del autor(usuario) del contenido.

    - author: User
        Relación uno a muchos con la entidad User.

    - created_at: datetime
        Fecha y hora de creación del contenido.
        restricciones -> no nulo, valor por defecto = fecha y hora actual

    - published_at: datetime
        Fecha y hora de publicación del contenido.
        restricciones -> no nulo.
    
    - updated_at: datetime
        Fecha y hora de actualización del contenido.
        restricciones -> no nulo, valor por defecto = fecha y hora actual

    ---------
    """

    __tablename__ = "contenidos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum("Borrador","Publicado","Archivado", name="status_enum"), default="Borrador",nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    author = db.relationship("User", back_populates="content_posts")

    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    published_at = db.Column(
        db.DateTime)
    updated_at = db.Column(
        db.DateTime, onupdate=datetime.now)
    
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Contenidos# id={self.id} name="{self.title}">'

