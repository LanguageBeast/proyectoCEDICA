from src.core.database import db


class Tutor(db.Model):
    """
    Descripción:
    Una clase que representa la entidad de un tutor en la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único del tutor.

    - relationship: str
        Relación con el estudiante.
        restricciones -> longitud máxima de 50 caracteres.

    - first_name: str
        Nombre del tutor.
        restricciones -> longitud máxima de 100 caracteres.

    - last_name: str
        Apellido del tutor.
        restricciones -> longitud máxima de 100 caracteres.

    - dni: str
        DNI del tutor.
        restricciones -> longitud máxima de 20 caracteres.

    - current_address: str
        Dirección actual del tutor.
        restricciones -> longitud máxima de 255 caracteres.

    - mobile_phone: str
        Número de teléfono móvil del tutor.
        restricciones -> longitud máxima de 20 caracteres.

    - email: str
        Correo electrónico del tutor.
        restricciones -> longitud máxima de 100 caracteres.

    - education_level: str
        Nivel educativo del tutor.
        restricciones -> longitud máxima de 50 caracteres.

    - occupation: str
        Ocupación del tutor.
        restricciones -> longitud máxima de 100 caracteres.

    ---------
    """
    __tablename__ = "tutores"

    id = db.Column(db.Integer, primary_key=True)
    relationship = db.Column(db.String(50), nullable=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    dni = db.Column(db.String(20), nullable=True)
    current_address = db.Column(db.String(255), nullable=True)
    mobile_phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    education_level = db.Column(db.String(50), nullable=True)
    occupation = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Tutor# id={self.id} first_name="{self.first_name}" last_name="{self.last_name}">'
