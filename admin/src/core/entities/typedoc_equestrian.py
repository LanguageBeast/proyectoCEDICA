from src.core.database import db


class TypeDocEquestrian(db.Model):
    """
    Descripción:
    Una clase que representa la entidad de un tipo de documento ecuestre en la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único del tipo de documento ecuestre.

    - name: str
        Nombre del tipo de documento ecuestre.
        restricciones -> no puede ser nulo.

    - documents: List<Document>
        Relación uno a muchos con la entidad Documento.

    ---------
    """
    __tablename__ = "tipo_documentos_ecuestre"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    documents = db.relationship(
        "Document", back_populates="typedoc_equestrian")

    def __repr__(self):
        return f'<TypeDocEquestrian id={self.id} name="{self.name}">'
