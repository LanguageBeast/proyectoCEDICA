from src.core.database import db


class JyaType(db.Model):
    """
    Descripción:
    Una clase que representa la entidad Tipo de JyA de la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único del tipo de JyA.

    - name: str
        Nombre del tipo de JyA.
        restricciones -> longitud máxima de 100 caracteres, no nulo

    - equestrians: List[Equestrian]
        Relación uno a muchos con la entidad Ecuestre.

    ---------
    """
    __tablename__ = "jya_tipos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    equestrians = db.relationship(
        'Equestrian', secondary='ecuestre_tipoJyA', back_populates='jya_type')

    def __repr__(self):
        return f'<JyaType# id={self.id} name="{self.name}">'
