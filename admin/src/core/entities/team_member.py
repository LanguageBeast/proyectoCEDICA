from datetime import datetime
from src.core.database import db


class TeamMember(db.Model):
    """
    Descripción:
    Una clase que representa la entidad de un miembro de equipo en la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único del miembro de equipo.

    - first_name: str
        Nombre del miembro de equipo.
        restricciones -> no puede ser nulo.

    - last_name: str
        Apellido del miembro de equipo.
        restricciones -> no puede ser nulo.

    - dni: str
        DNI del miembro de equipo.
        restricciones -> no puede ser nulo, único.

    - address: str
        Dirección del miembro de equipo.
        restricciones -> longitud máxima de 100 caracteres.

    - email: str
        Correo electrónico del miembro de equipo.
        restricciones -> no puede ser nulo, único.

    - location: str
        Localidad del miembro de equipo.
        restricciones -> longitud máxima de 100 caracteres.

    - phone: str
        Número de teléfono del miembro de equipo.
        restricciones -> no puede ser nulo, longitud máxima de 20 caracteres.

    - profession: str
        Profesión del miembro de equipo.
        restricciones -> no puede ser nulo, longitud máxima de 100 caracteres.

    - job_position: str
        Cargo del miembro de equipo.
        restricciones -> no puede ser nulo, longitud máxima de 100 caracteres.

    - start_date: datetime
        Fecha de inicio del miembro de equipo.
        restricciones -> no puede ser nulo.

    - end_date: datetime
        Fecha de finalización del miembro de equipo.
        restricciones -> puede ser nulo.

    - emergency_contact_name: str
        Nombre del contacto de emergencia del miembro de equipo.
        restricciones -> no puede ser nulo, longitud máxima de 100 caracteres.

    - emergency_contact_phone: str
        Número de teléfono del contacto de emergencia del miembro de equipo.
        restricciones -> no puede ser nulo, longitud máxima de 20 caracteres.

    - health_insurance: str
        Obra social del miembro de equipo.
        restricciones -> longitud máxima de 100 caracteres.

    - insurance_number: str
        Número de afiliado a la obra social del miembro de equipo.
        restricciones -> longitud máxima de 50 caracteres.

    - condition: str
        Condición del miembro de equipo.
        restricciones -> longitud máxima de 100 caracteres.

    - active: bool
        Indica si el miembro de equipo está activo.
        restricciones -> no nulo, valor por defecto = True.

    - deleted: bool
        Indica si el miembro de equipo fue eliminado.
        restricciones -> no nulo, valor por defecto = False

    - user_id: int
        Clave foránea del usuario asociado al miembro de equipo.
        restricciones -> puede ser nulo, único.

    - user: User
        Relación uno a uno con la entidad Usuario.

    - documents: List<Document>
        Relación uno a muchos con la entidad Documento.

    - payments: List<Payment>
        Relación uno a muchos con la entidad Pago.

    - receipts: List<Receipt>
        Relación uno a muchos con la entidad Recibo.

    - equestrians: List<Equestrian>
        Relación muchos a muchos con la entidad Ecuestres.

    - work_teacher_or_therapist: List<WorkProposal>
        Relación uno a muchos con la entidad Propuesta de Trabajo.

    - work_horse_handler: List<WorkProposal>
        Relación uno a muchos con la entidad Propuesta de Trabajo.

    - work_track_assistant: List<WorkProposal>
        Relación uno a muchos con la entidad Propuesta de Trabajo.

    - created_at: datetime
        Fecha de creación del miembro de equipo.
        restricciones -> valor por defecto = fecha actual.

    - updated_at: datetime
        Fecha de última actualización del miembro de equipo.
        restricciones -> valor por defecto = fecha actual, actualizado automáticamente.

    ---------
    """
    __tablename__ = "miembros_equipo"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), nullable=False, unique=True)
    address = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    location = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=False)
    profession = db.Column(db.String(100), nullable=False)
    job_position = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    emergency_contact_name = db.Column(db.String(100), nullable=False)
    emergency_contact_phone = db.Column(db.String(20), nullable=False)
    health_insurance = db.Column(db.String(100), nullable=True)
    insurance_number = db.Column(db.String(50), nullable=True)
    condition = db.Column(db.String(100), nullable=True)
    active = db.Column(db.Boolean, default=True)
    deleted = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'usuarios.id'), nullable=True, unique=True)
    documents = db.relationship("Document", back_populates="team_member")
    payments = db.relationship("Payment", back_populates="team_member")
    receipts = db.relationship("Receipt", back_populates="team_member")
    equestrians = db.relationship(
        'Equestrian', secondary='ecuestre_miembro_equipo', back_populates='team_member')
    work_teacher_or_therapist = db.relationship(
        'WorkProposal', foreign_keys='WorkProposal.teacher_or_therapist_id', back_populates='teacher_or_therapist')
    work_horse_handler = db.relationship(
        'WorkProposal', foreign_keys='WorkProposal.horse_handler_id', back_populates='horse_handler')
    work_track_assistant = db.relationship(
        'WorkProposal', foreign_keys='WorkProposal.track_assistant_id', back_populates='track_assistant')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<miembro_equipo #{self.id} first_name="{self.first_name}" last_name="{self.last_name}">'
