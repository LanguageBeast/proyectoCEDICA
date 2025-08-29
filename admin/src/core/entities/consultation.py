from datetime import datetime
from src.core.database import db


class Consultation(db.Model):
    """
    Descripción:
    Una clase que representa la entidad Consulta de la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único de la consulta.

    - full_name: str
        Nombre completo del usuario que realiza la consulta.
        restricciones -> longitud máxima de 100 caracteres, no nulo

    - email: str
        Correo electrónico del usuario que realiza la consulta.
        restricciones -> longitud máxima de 120 caracteres, no nulo

    - message: str
        Mensaje de la consulta.
        restricciones -> no nulo

    - captcha: str
        Captcha de la consulta.
        restricciones -> longitud de 6 caracteres, no nulo

    - status: str
        Estado de la consulta.
        restricciones -> longitud máxima de 50 caracteres, no nulo, por defecto 'Pendiente'

    - comment: str
        Comentario de la consulta.
        restricciones -> no nulo

    - created_at: datetime
        Fecha de creación de la consulta.
        restricciones -> no nulo

    ---------
    """
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    captcha = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pendiente')
    comment = db.Column(db.Text, nullable=True)
    deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Consultation #{self.id} from {self.full_name}>'
