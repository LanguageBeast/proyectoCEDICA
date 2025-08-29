from src.core.database import db


class WorkProposal(db.Model):
    """
    Descripción:
    Una clase que representa la entidad de una propuesta de trabajo en la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único de la propuesta de trabajo.

    - work_proposal: str
        Descripción de la propuesta de trabajo.
        restricciones -> longitud máxima de 255 caracteres.

    - condition: str
        Condiciones de la propuesta de trabajo.
        restricciones -> longitud máxima de 255 caracteres.

    - location: str
        Ubicación de la propuesta de trabajo.
        restricciones -> longitud máxima de 255 caracteres.

    - days: str
        Días en los que se realizará la propuesta de trabajo.
        restricciones -> longitud máxima de 255 caracteres.

    - teacher_or_therapist_id: int
        Clave foránea del miembro de equipo que será el profesor o terapeuta.

    - teacher_or_therapist: TeamMember
        Relación muchos a uno con la entidad Miembro de Equipo.

    - horse_handler_id: int
        Clave foránea del miembro de equipo que será el encargado de los caballos.

    - horse_handler: TeamMember
        Relación muchos a uno con la entidad Miembro de Equ

    - track_assistant_id: int
        Clave foránea del miembro de equipo que será el asistente de pista.

    - track_assistant: TeamMember
        Relación muchos a uno con la entidad Miembro de Equipo.

    - equestrian_id: int
        Clave foránea del ecuestre al que pertenece la propuesta de trabajo.

    - equestrian: Equestrian
        Relación uno a uno con la entidad Ecuestre.

    - fileJyA_id: int
        Clave foránea del legajo JyA al que pertenece la propuesta de trabajo.

    - fileJyA: LegajoJyA
        Relación uno a uno con la entidad LegajoJyA.

    ---------
    """
    __tablename__ = "propuestas_trabajo"

    id = db.Column(db.Integer, primary_key=True)
    work_proposal = db.Column(db.String(255), nullable=True)
    condition = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    days = db.Column(db.String(255), nullable=True)
    teacher_or_therapist_id = db.Column(
        db.Integer, db.ForeignKey('miembros_equipo.id'))
    teacher_or_therapist = db.relationship('TeamMember', foreign_keys=[
                                           teacher_or_therapist_id], back_populates='work_teacher_or_therapist')
    horse_handler_id = db.Column(
        db.Integer, db.ForeignKey('miembros_equipo.id'))
    horse_handler = db.relationship('TeamMember', foreign_keys=[
                                    horse_handler_id], back_populates='work_horse_handler')
    track_assistant_id = db.Column(
        db.Integer, db.ForeignKey('miembros_equipo.id'))
    track_assistant = db.relationship('TeamMember', foreign_keys=[
                                      track_assistant_id], back_populates='work_track_assistant')
    equestrian_id = db.Column(db.Integer, db.ForeignKey("ecuestres.id"))
    equestrian = db.relationship("Equestrian", back_populates="work_proposal")
    fileJyA_id = db.Column(db.Integer, db.ForeignKey(
        "legajos_jya.id"), unique=True)
    fileJyA = db.relationship("LegajoJyA", back_populates="work_proposal")

    def __repr__(self):
        return f'<WorkProposal# id={self.id} work_proposal="{self.work_proposal}">'
