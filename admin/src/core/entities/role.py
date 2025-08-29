from src.core.database import db

# Tabla intermedia para la relación muchos a muchos entre roles y permisos
permission_role = db.Table(
    "permiso_rol",
    db.Column("role_id", db.Integer, db.ForeignKey(
        "roles.id"), primary_key=True),
    db.Column("permission_id", db.Integer, db.ForeignKey(
        "permisos.id"), primary_key=True)
)


class Role(db.Model):
    """
    Descripción:
    Una clase que representa la entidad de un rol en la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único del rol.

    - name: str
        Nombre del rol.
        restricciones -> no puede ser nulo, valor único.

    - users: List<User>
        Relación uno a muchos con la entidad Usuario.

    - permissions: List<Permission>
        Relación muchos a muchos con la entidad Permiso.

    ---------
    """
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    users = db.relationship("User", back_populates="role")
    permissions = db.relationship("Permission", secondary=permission_role)

    def __repr__(self):
        return f'<Role #{self.id} name="{self.name}">'
