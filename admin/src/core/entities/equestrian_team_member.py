from src.core.database import db


class EquestrianTeamMember(db.Model):
    """
    Descripción:
    Una clase que representa la relación muchos a muchos entre la entidad Ecuestre y la entidad Miembro de Equipo en la base de datos.

    ---------
    Atributos:
    - equestrian_id: int
        Identificador del ecuestre.

    - team_member_id: int
        Identificador del miembro del equipo.

    ---------
    """
    __tablename__ = 'ecuestre_miembro_equipo'
    equestrian_id = db.Column(db.Integer, db.ForeignKey(
        'ecuestres.id', ondelete='CASCADE'), primary_key=True)
    team_member_id = db.Column(db.Integer, db.ForeignKey(
        'miembros_equipo.id', ondelete='CASCADE'), primary_key=True)
    # type_team_member = db.Column(db.String(100), nullable=False)
