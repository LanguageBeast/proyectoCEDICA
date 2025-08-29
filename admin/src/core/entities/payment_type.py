from src.core.database import db
from datetime import datetime


class PaymentType(db.Model):
    """
    Descripción:
    Una clase que representa la entidad Tipo de Pago de la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único del tipo de pago.

    - name: str
        Nombre del tipo de pago.
        restricciones -> longitud máxima de 50 caracteres, no nulo

    - payments: List<Payment>
        Relación uno a muchos con la entidad Payment.

    - created_at: datetime
        Fecha de creación del tipo de pago.
        restricciones -> no nulo

    - updated_at: datetime
        Fecha de actualización del tipo de pago.
        restricciones -> no nulo

    ---------
    """
    __tablename__ = "tipos_de_pagos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    payments = db.relationship("Payment", back_populates="payment_type")
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<PaymentType #{self.id} name="{self.name}">'
