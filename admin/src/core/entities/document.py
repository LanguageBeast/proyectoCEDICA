from datetime import datetime
from src.core.database import db


class Document(db.Model):
    """
    Descripción: 
    Una clase que representa la entidad Documento de la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único del documento.

    - name: str
        Nombre del documento.
        restricciones -> longitud máxima de 100 caracteres, no nulo

    - path: str
        Ruta del documento.
        restricciones -> longitud máxima de 255 caracteres

    - link: str
        Enlace del documento.
        restricciones -> longitud máxima de 255 caracteres

    - creation_date: datetime
        Fecha y hora de creación del documento.
        restricciones -> no nulo, valor por defecto = fecha y hora actual

    - team_member_id: int
        Identificador del miembro del equipo al que pertenece el documento.

    - team_member: List<TeamMember>
        Relación muchos a uno con la entidad Miembro de Equipo.

    - fileJyA_id: int
        Identificador del legajo de Jinetes y Amazonas al que pertenece el documento.

    - fileJyA: List<LegajoJyA>
        Relación muchos a uno con la entidad LegajoJyA.

    - equestrian_id: int
        Identificador del ecuestre al que pertenece el documento.

    - equestrian: List<Equestrian>
        Relación muchos a uno con la entidad Ecuestre.

    - typedoc_fileJyA_id: int
        Identificador del tipo de documento del legajo de Jinetes y Amazonas.

    - typedoc_fileJyA: TypeDocFileJyA
        Relación muchos a uno con la entidad Tipo de Documento del legajo de Jinetes y Amazonas.

    - typedoc_equestrian_id: int
        Identificador del tipo de documento del ecuestre.

    - typedoc_equestrian: TypeDocEquestrian
        Relación muchos a uno con la entidad Tipo de Documento del ecuestre.

    ---------
    """
    __tablename__ = "documentos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(255))
    link = db.Column(db.String(255))
    deleted = db.Column(db.Boolean, default=False)
    creation_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    team_member_id = db.Column(db.Integer, db.ForeignKey("miembros_equipo.id"))
    team_member = db.relationship("TeamMember", back_populates="documents")
    fileJyA_id = db.Column(db.Integer, db.ForeignKey("legajos_jya.id"))
    fileJyA = db.relationship("LegajoJyA", back_populates="documents")
    equestrian_id = db.Column(db.Integer, db.ForeignKey("ecuestres.id"))
    equestrian = db.relationship("Equestrian", back_populates="documents")
    typedoc_fileJyA_id = db.Column(
        db.Integer, db.ForeignKey("tipo_documentos_legajoJyA.id"))
    typedoc_fileJyA = db.relationship(
        "TypeDocFileJyA", back_populates="documents")
    typedoc_equestrian_id = db.Column(
        db.Integer, db.ForeignKey("tipo_documentos_ecuestre.id"))
    typedoc_equestrian = db.relationship(
        "TypeDocEquestrian", back_populates="documents")

    def __repr__(self):
        return f'<Documento# id={self.id} name="{self.name}">'
