from src.core.database import db


class SchoolSituation(db.Model):
    """
    Descripción:
    Una clase que representa la entidad de una situación escolar en la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único de la situación escolar.

    - institution_name: str
        Nombre de la institución educativa.
        restricciones -> longitud máxima de 50 caracteres.

    - school_address: str
        Dirección de la institución educativa.
        restricciones -> longitud máxima de 100 caracteres.

    - school_phone: str
        Teléfono de la institución educativa.
        restricciones -> longitud máxima de 20 caracteres.

    - current_grade: str
        Grado actual del estudiante.
        restricciones -> longitud máxima de 20 caracteres.

    - school_notes: str
        Notas adicionales sobre la situación escolar.
        restricciones -> longitud máxima de 255 caracteres.

    - fileJyA_id: int
        Clave foránea del legajo JyA al que pertenece la situación escolar.

    - fileJyA: LegajoJyA
        Relación uno a uno con la entidad LegajoJyA.

    ---------
    """
    __tablename__ = "situaciones_escolares"

    id = db.Column(db.Integer, primary_key=True)
    institution_name = db.Column(db.String(50))
    school_address = db.Column(db.String(100))
    school_phone = db.Column(db.String(20))
    current_grade = db.Column(db.String(20))
    school_notes = db.Column(db.String(255))
    fileJyA_id = db.Column(db.Integer, db.ForeignKey(
        "legajos_jya.id"), unique=True)
    fileJyA = db.relationship("LegajoJyA", back_populates="school_situacion")

    def __repr__(self):
        return f'<SchoolSituation# id={self.id} institution_name="{self.institution_name}">'
