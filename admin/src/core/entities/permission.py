from src.core.database import db


class Permission(db.Model):
    """
    Descripción:
    Clase que representa la tabla permisos en la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único del permiso.

    - name: str
        Nombre del permiso.
        restricciones -> no nulo, único

    ---------
    """
    __tablename__ = "permisos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<Permission #{self.id} name="{self.name}">'
