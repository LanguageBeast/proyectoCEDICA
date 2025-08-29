from datetime import datetime
from src.core.database import db


class Payment(db.Model):
    """
    Descripción:
    Una clase que representa la entidad Pago de la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único del pago.

    - amount: float
        Monto del pago.
        restricciones -> no nulo

    - payment_date: datetime
        Fecha del pago.
        restricciones -> no nulo

    - description: str
        Descripción del pago.
        restricciones -> longitud máxima de 255 caracteres

    - payment_type_id: int
        Clave foránea del tipo de pago.

    - payment_type: PaymentType
        Relación uno a muchos con la entidad Tipo de Pago.

    - team_member_id: int
        Clave foránea del miembro de equipo.

    - team_member: TeamMember
        Relación uno a muchos con la entidad Miembro de Equipo.

    - deleted: bool
        Indica si el pago fue eliminado.
        restricciones -> valor por defecto = False

    - created_at: datetime
        Fecha de creación del pago.
        restricciones -> valor por defecto = fecha y hora actual

    - updated_at: datetime
        Fecha de actualización del pago.
        restricciones -> valor por defecto = fecha y hora actual, onupdate=datetime.now

    ---------
    """
    __tablename__ = "pagos"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    payment_type_id = db.Column(db.Integer, db.ForeignKey("tipos_de_pagos.id"))
    payment_type = db.relationship(
        "PaymentType", back_populates="payments", uselist=False
    )
    # Este debe quedar nulo si no es un pago de un miembro de equipo, según el ayudante.
    team_member_id = db.Column(
        db.Integer, db.ForeignKey("miembros_equipo.id"), nullable=True
    )
    team_member = db.relationship(
        "TeamMember", back_populates="payments", uselist=False
    )
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Pago# id={self.id} amount={self.amount}>"
