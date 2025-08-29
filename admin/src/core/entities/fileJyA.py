from datetime import datetime
from src.core.database import db
from sqlalchemy.dialects.postgresql import JSON

# Tabla intermedia para la relación muchos a muchos entre legajos y tutores
fileJyA_tutor = db.Table(
    "fileJyA_tutor",
    db.Column("fileJyA_id", db.Integer, db.ForeignKey(
        "legajos_jya.id"), primary_key=True),
    db.Column("tutor_id", db.Integer, db.ForeignKey(
        "tutores.id"), primary_key=True)
)


class LegajoJyA(db.Model):
    """
    Descripción:
    Una clase que representa la entidad Legajo de JyA de la base de datos.

    ---------
    Atributos:
    - id: int
        Identificador único del legajo de JyA.

    - first_name: str
        Nombre del beneficiario.
        restricciones -> longitud máxima de 25 caracteres, no nulo

    - last_name: str
        Apellido del beneficiario.
        restricciones -> longitud máxima de 25 caracteres, no nulo

    - dni: str
        DNI del beneficiario.
        restricciones -> longitud máxima de 15 caracteres, no nulo

    - age: int
        Edad del beneficiario.
        restricciones -> no nulo

    - birth_date: datetime
        Fecha de nacimiento del beneficiario.
        restricciones -> no nulo

    - birth_locality: str
        Localidad de nacimiento del beneficiario.
        restricciones -> longitud máxima de 50 caracteres, no nulo

    - birth_province: str
        Provincia de nacimiento del beneficiario.
        restricciones -> longitud máxima de 50 caracteres, no nulo

    - adress_street: str
        Calle de la dirección del beneficiario.
        restricciones -> longitud máxima de 50 caracteres, no nulo

    - adress_number: int
        Número de la dirección del beneficiario.
        restricciones -> no nulo

    - adress_apartment: str
        Departamento de la dirección del beneficiario.
        restricciones -> longitud máxima de 20 caracteres

    - adress_locality: str
        Localidad de la dirección del beneficiario.
        restricciones -> longitud máxima de 50 caracteres, no nulo

    - adress_province: str
        Provincia de la dirección del beneficiario.
        restricciones -> longitud máxima de 50 caracteres, no nulo

    - phone: str
        Teléfono del beneficiario.
        restricciones -> longitud máxima de 20 caracteres

    - emergency_contact_name: str
        Nombre del contacto de emergencia del beneficiario.
        restricciones -> longitud máxima de 50 caracteres, no nulo

    - emergency_contact_phone: str
        Teléfono del contacto de emergencia del beneficiario.
        restricciones -> longitud máxima de 20 caracteres, no nulo

    - disability_certificate: bool
        Indica si el beneficiario posee certificado de discapacidad.
        restricciones -> no nulo

    - disability_certificate_diagnosis: JSON
        Diagnóstico del certificado de discapacidad del beneficiario.

    - other_diagnosis_disability: str
        Otro diagnóstico de discapacidad del beneficiario.
        restricciones -> longitud máxima de 20 caracteres

    - disability_type: JSON
        Tipo de discapacidad del beneficiario.

    - scholarship: bool
        Indica si el beneficiario posee beca.
        restricciones -> no nulo

    - per_scholarship: int
        Porcentaje de la beca del beneficiario.

    - scholarship_notes: str
        Notas de la beca del beneficiario.
        restricciones -> longitud máxima de 255 caracteres

    - welfare: bool
        Indica si el beneficiario recibe asistencia social.
        restricciones -> no nulo

    - child_welfare: bool
        Indica si el beneficiario recibe asistencia social por ser menor de edad.

    - child_disability_welfare: bool
        Indica si el beneficiario recibe asistencia social por tener discapacidad.

    - school_help_welfare: bool
        Indica si el beneficiario recibe asistencia social para la escuela.

    - pension_beneficiary: bool
        Indica si el beneficiario es beneficiario de pensión.
        restricciones -> no nulo

    - pension_type: str
        Tipo de pensión del beneficiario.
        restricciones -> longitud máxima de 100 caracteres

    - attending_professionals: str
        Profesionales que atienden al beneficiario.
        restricciones -> longitud máxima de 100 caracteres, no nulo

    - in_debt: bool
        Indica si el beneficiario posee deuda.
        restricciones -> no nulo, valor por defecto = False

    - deleted: bool
        Indica si el beneficiario fue eliminado.
        restricciones -> no nulo, valor por defecto = False

    - files: str
        Archivos del beneficiario.
        restricciones -> longitud máxima de 255 caracteres

    - provisional_situation: List[ProvisionalSituation]
        Relación uno a muchos con la entidad Situación Provisional.

    - work_proposal: List[WorkProposal]
        Relación uno a muchos con la entidad Propuesta de Trabajo.

    - school_situacion: List[SchoolSituation]
        Relación uno a muchos con la entidad Situación Escolar.

    - documents: List[Document]
        Relación uno a muchos con la entidad Documento.

    - receipts: List[Receipt]
        Relación uno a muchos con la entidad Recibo.

    - tutors: List[Tutor]
        Relación muchos a muchos con la entidad Tutor.

    - creation_date: datetime
        Fecha de creación del legajo de JyA.
        restricciones -> no nulo, valor por defecto = datetime.now

    - update_date: datetime
        Fecha de actualización del legajo de JyA.
        restricciones -> no nulo, valor por defecto = datetime.now, onupdate=datetime.now

    ---------
    """
    __tablename__ = "legajos_jya"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    dni = db.Column(db.String(15), nullable=False)

    age = db.Column(db.Integer, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    birth_locality = db.Column(db.String(50), nullable=False)
    birth_province = db.Column(db.String(50), nullable=False)

    adress_street = db.Column(db.String(50), nullable=False)
    adress_number = db.Column(db.Integer, nullable=False)
    adress_apartment = db.Column(db.String(20))
    adress_locality = db.Column(db.String(50), nullable=False)
    adress_province = db.Column(db.String(50), nullable=False)

    phone = db.Column(db.String(20))
    emergency_contact_name = db.Column(db.String(50), nullable=False)
    emergency_contact_phone = db.Column(db.String(20), nullable=False)

    disability_certificate = db.Column(db.Boolean, nullable=False)
    disability_certificate_diagnosis = db.Column(JSON)
    other_diagnosis_disability = db.Column(db.String(20))
    disability_type = db.Column(JSON, nullable=True)

    scholarship = db.Column(db.Boolean, nullable=False)
    per_scholarship = db.Column(db.Integer, nullable=True)
    scholarship_notes = db.Column(db.String(255), nullable=True)

    welfare = db.Column(db.Boolean, nullable=False)
    child_welfare = db.Column(db.Boolean, nullable=True)
    child_disability_welfare = db.Column(db.Boolean, nullable=True)
    school_help_welfare = db.Column(db.Boolean, nullable=True)

    pension_beneficiary = db.Column(db.Boolean, nullable=False)
    pension_type = db.Column(db.String(100), nullable=True)

    attending_professionals = db.Column(db.String(100), nullable=False)

    in_debt = db.Column(db.Boolean, nullable=False, default=False)

    deleted = db.Column(db.Boolean, nullable=False, default=False)

    provisional_situation = db.relationship(
        "ProvisionalSituation", back_populates="fileJyA", uselist=True)
    work_proposal = db.relationship(
        "WorkProposal", back_populates="fileJyA", uselist=True)
    school_situacion = db.relationship(
        "SchoolSituation", back_populates="fileJyA", uselist=True)
    documents = db.relationship("Document", back_populates="fileJyA")
    receipts = db.relationship(
        "Receipt", back_populates="fileJyA", lazy='dynamic')
    tutors = db.relationship("Tutor", secondary=fileJyA_tutor)

    creation_date = db.Column(
        db.DateTime, nullable=True, default=datetime.now)

    update_date = db.Column(db.DateTime, nullable=True,
                            default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<LegajoJyA# id={self.id} first_name="{self.first_name}" last_name="{self.last_name}">'
