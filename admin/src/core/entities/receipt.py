from datetime import date
from src.core.database import db


class Receipt(db.Model):
    """
    Descripción:
    Una clase que representa la entidad de un cobro en la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único del cobro.

    - payment_date: date
        Fecha en la que se realizó el cobro.
        restricciones -> no puede ser nulo, valor por defecto = fecha actual.

    - payment_method: str
        Método de pago utilizado.
        restricciones -> no puede ser nulo.

    - amount: float
        Monto del cobro.
        restricciones -> no puede ser nulo.

    - notes: str
        Notas adicionales sobre el cobro.
        restricciones -> longitud máxima de 255 caracteres.

    - fileJyA_id: int
        Clave foránea del legajo JyA al que pertenece el cobro.

    - fileJyA: LegajoJyA
        Relación muchos a uno con la entidad LegajoJyA.

    - team_member_id: int
        Clave foránea del miembro de equipo que realizó el cobro.

    - team_member: TeamMember
        Relación muchos a uno con la entidad Miembro de Equipo.

    - deleted: bool
        Indica si el cobro fue eliminado.
        restricciones -> no nulo, valor por defecto = False

    ---------
    """
    __tablename__ = "cobros"

    id = db.Column(db.Integer, primary_key=True)
    payment_date = db.Column(
        db.Date, nullable=False, default=date.today)
    payment_method = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String(255))
    fileJyA_id = db.Column(db.Integer, db.ForeignKey("legajos_jya.id"))
    fileJyA = db.relationship("LegajoJyA", back_populates="receipts")
    team_member_id = db.Column(db.Integer, db.ForeignKey("miembros_equipo.id"))
    team_member = db.relationship("TeamMember", back_populates="receipts")
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Cobro id={self.id} amount={self.amount}>'
