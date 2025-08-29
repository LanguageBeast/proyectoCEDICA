from datetime import datetime
from src.core.database import db


class Equestrian(db.Model):
    """
    Descripción:
    Una clase que representa la entidad Ecuestre de la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único del ecuestre.

    - name: str
        Nombre del ecuestre.
        restricciones -> longitud máxima de 100 caracteres, no nulo

    - sex: str
        Sexo del ecuestre.
        restricciones -> longitud máxima de 10 caracteres, no nulo

    - breed: str
        Raza del ecuestre.
        restricciones -> longitud máxima de 50 caracteres, no nulo

    - coat: str
        Pelaje del ecuestre.
        restricciones -> longitud máxima de 50 caracteres, no nulo

    - is_purchase: bool
        Indica si el ecuestre fue comprado.
        restricciones -> no nulo

    - is_donation: bool
        Indica si el ecuestre fue donado.
        restricciones -> no nulo

    - location: str
        Sede del ecuestre.
        restricciones -> longitud máxima de 100 caracteres, no nulo

    - birth_date: datetime
        Fecha de nacimiento del ecuestre.
        restricciones -> no nulo

    - entry_date: datetime
        Fecha de ingreso del ecuestre.
        restricciones -> no nulo, valor por defecto = fecha y hora actual

    - documents: List<Document>
        Lista de documentos del ecuestre.

    - team_member: List<TeamMember>
        Relación muchos a muchos con la entidad Miembro de Equipo.

    - jya_type: List<JyaType>
        Relación muchos a muchos con la entidad Tipo JyA.

    - work_proposal: WorkProposal
        Propuesta de trabajo del ecuestre.

    - deleted: bool
        Indica si el ecuestre fue eliminado.
        restricciones -> no nulo, valor por defecto = False

    ---------
    """
    __tablename__ = "ecuestres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    coat = db.Column(db.String(50), nullable=False)
    is_purchase = db.Column(db.Boolean, nullable=False)
    is_donation = db.Column(db.Boolean, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.now)
    documents = db.relationship("Document", back_populates="equestrian")
    team_member = db.relationship(
        'TeamMember', secondary='ecuestre_miembro_equipo', back_populates='equestrians')
    jya_type = db.relationship(
        'JyaType', secondary='ecuestre_tipoJyA', back_populates='equestrians')
    work_proposal = db.relationship(
        "WorkProposal", back_populates="equestrian")
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Equestrian# id={self.id} name="{self.name}">'
