from src.core.database import db


class ProvisionalSituation(db.Model):
    """
    Descripción:
    Clase que representa la entidad de la situación previsional de un legajo de Jóvenes y Adultos.

    ---------
    Atributos:
    - id: int
        Identificador único de la situación previsional.

    - social_security: str
        Número de seguridad social de la persona.
        restricciones -> no nulo, longitud máxima de 25 caracteres

    - affiliate_number: str
        Número de afiliado de la persona.
        restricciones -> no nulo, longitud máxima de 50 caracteres

    - has_guardianship: bool
        Indica si la persona tiene tutela.
        restricciones -> no nulo

    - previsional_situacion_notes: str
        Notas de la situación previsional.
        restricciones -> longitud máxima de 255 caracteres

    - fileJyA_id: int
        Clave foránea del legajo de Jóvenes y Adultos.

    - fileJyA: LegajoJyA
        Relación uno a uno con el legajo de Jóvenes y Adultos.

    ---------
    """
    __tablename__ = "situaciones_provisorias"

    id = db.Column(db.Integer, primary_key=True)
    social_security = db.Column(db.String(25), nullable=True)
    affiliate_number = db.Column(db.String(50), nullable=True)
    has_guardianship = db.Column(db.Boolean, nullable=True)
    previsional_situacion_notes = db.Column(db.String(255), nullable=True)
    fileJyA_id = db.Column(db.Integer, db.ForeignKey(
        "legajos_jya.id"), unique=True)
    fileJyA = db.relationship(
        "LegajoJyA", back_populates="provisional_situation")

    def __repr__(self):
        return f'<ProvisionalSituation# id={self.id} social_security="{self.social_security}">'
