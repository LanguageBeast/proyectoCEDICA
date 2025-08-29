from src.core.database import db


class EquestrianJyAType(db.Model):
    """
    Descripción:
    Una clase que representa la relacion entre un ecuestre y un tipo de Jinetes y Amazonas.

    ---------
    Atributos:
    - equestrian_id: int
        Identificador del ecuestre.

    - jya_type_id: int
        Identificador del tipo de Jinetes y Amazonas.

    ---------
    """
    __tablename__ = 'ecuestre_tipoJyA'
    equestrian_id = db.Column(db.Integer, db.ForeignKey(
        'ecuestres.id', ondelete='CASCADE'), primary_key=True)
    jya_type_id = db.Column(db.Integer, db.ForeignKey(
        'jya_tipos.id', ondelete='CASCADE'), primary_key=True)
