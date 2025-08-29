from datetime import datetime
from src.core.database import db


class User(db.Model):
    """
    Descripción:    
    Una clase que representa la entidad de un usuario en la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único del usuario.

    - email: str
        Correo electrónico del usuario.
        restricciones -> no puede ser nulo, longitud máxima de 100 caracteres, único.

    - dni: str
        DNI del usuario.
        restricciones -> no puede ser nulo, longitud máxima de 20 caracteres, único.

    - alias: str
        Alias del usuario.
        restricciones -> no puede ser nulo, longitud máxima de 50 caracteres, único.

    - password: str
        Contraseña del usuario.
        restricciones -> no puede ser nulo, longitud máxima de 255 caracteres.

    - is_enabled: bool
        Indica si el usuario está habilitado.
        restricciones -> valor por defecto = True.

    - role_id: int
        Clave foránea del rol del usuario.

    - role: Role
        Relación uno a muchos con la entidad Rol.

    - member: TeamMember
        Relación uno a uno con la entidad Miembro de Equipo.

    - created_at: datetime
        Fecha de creación del usuario.
        restricciones -> valor por defecto = fecha y hora actual.

    - updated_at: datetime
        Fecha de actualización del usuario.
        restricciones -> valor por defecto = fecha y hora actual, onupdate=datetime.now.

    - deleted: bool
        Indica si el usuario fue eliminado.
        restricciones -> no nulo, valor por defecto = False

    ---------
    """
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    dni = db.Column(db.String(20), nullable=False, unique=True)
    alias = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_enabled = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    role = db.relationship("Role", back_populates="users")
    member = db.relationship('TeamMember', backref='user', uselist=False)
    content_posts = db.relationship("ContentPost", back_populates="author")
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<User #{self.id} email="{self.email}" alias="{self.alias}">'
