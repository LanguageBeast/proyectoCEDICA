from src.core.database import db


class TypeDocFileJyA(db.Model):
    """
    Descripción:
    Una clase que representa la entidad de un tipo de documento en la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único del tipo de documento.  

    - name: str
        Nombre del tipo de documento.
        restricciones -> no puede ser nulo.

    - documents: List<Document>
        Relación uno a muchos con la entidad Document.

    ---------
    """
    __tablename__ = "tipo_documentos_legajoJyA"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    documents = db.relationship("Document", back_populates="typedoc_fileJyA")

    def __repr__(self):
        return f'<TypeDocLegajoJyA id={self.id} name="{self.name}">'
