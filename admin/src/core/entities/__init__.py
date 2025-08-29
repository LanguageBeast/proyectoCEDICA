from core.entities.consultation import Consultation
from src.core.database import db
from src.core.bcrypt import bcrypt
from sqlalchemy import and_, asc, desc, func
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import  load_only
from core.entities import (
    typedoc_equestrian,
)
from core.entities.document import Document
from core.entities.permission import Permission
from core.entities.fileJyA import LegajoJyA
from core.entities.user import User
from core.entities.role import Role
from core.entities.receipt import Receipt
from core.entities.equestrian_team_member import EquestrianTeamMember
from core.entities.equestrian_jya_type import EquestrianJyAType
from core.entities.payment import Payment
from core.entities.payment_type import PaymentType
from core.entities.equestrian import Equestrian
from core.entities.jya_type import JyaType
from core.entities.team_member import TeamMember
from core.entities.school_situation import SchoolSituation
from core.entities.provisional_situation import ProvisionalSituation
from core.entities.tutor import Tutor
from core.entities.work_proposal import WorkProposal
from core.entities.content_post import ContentPost
from core.entities.typedoc_fileJyA import TypeDocFileJyA
from datetime import datetime


# funcion para usar el lazy loading (los campos de relationship)


def reattach_to_session(objects):
    """
    Función para reasignar objetos a la sesión de la base de datos.
    Atributos: objects (list) - Lista de objetos a reasignar.
    Retorna: None
    """
    for obj in objects:
        db.session.add(obj)

# funcion baja logica general


def logical_delete(obj):
    """
    Función para realizar una baja lógica de un objeto.
    Atributos: obj (object) - Objeto a eliminar.
    Retorna: None
    """
    obj.deleted = True
    db.session.commit()

# Funciones para la creación de tablas de legajosJYA


def list_legajosJyA():
    """ 
    Función para listar los legajos de JyA.
    Atributos: Ninguno.
    Retorna: Lista de legajos de JyA (list<LegajoJyA>).
    """
    legajosJyA = LegajoJyA.query.filter_by(deleted=False).all()
    return legajosJyA


def modify_status_receipts_legajoJyA(fileJyA, status):
    """
    Función para modificar el estado de los recibos de un legajo de JyA.
    Atributos: 
    - fileJyA (LegajoJyA) - Legajo de JyA a modificar.
    - status (bool) - Nuevo estado de los recibos.
    Retorna: None
    """
    fileJyA.in_debt = status
    commit_legajosJyA(fileJyA)


def get_legajoJyA_by_id(id):
    """
    Función para obtener un legajo de JyA por su ID.
    Atributos: id (int) - ID del legajo de JyA.
    Retorna: Legajo de JyA (LegajoJyA).
    """
    legajoJyA = LegajoJyA.query.filter_by(
        deleted=False).filter_by(id=id).first()
    return legajoJyA


def query_legajosJyA():
    """ 
    Función para obtener una query de los legajos de JyA.
    Atributos: Ninguno.
    Retorna: Lista de legajos de JyA (list<LegajoJyA>).
    """
    legajosJyA = LegajoJyA.query.filter_by(deleted=False)
    return legajosJyA


def order_legajosJyA_by_name(query, order_by_first_name="asc"):
    """
    Función para ordenar los legajos de JyA por nombre.
    Atributos:
    - query (query) - Query de los legajos de JyA.
    - order_by_first_name (str, default='asc') - Orden de los legajos de JyA.
    Retorna: Lista de legajos de JyA (list<LegajoJyA>).
    """
    if order_by_first_name == "desc":
        return query.order_by(desc(LegajoJyA.first_name))
    else:
        return query.order_by(asc(LegajoJyA.first_name))


def create_provisional_legajosJyA(**kwargs):
    """
    Función para crear un legajo de JyA provisional.
    Atributos: kwargs (dict) - Diccionario con los atributos del legajo de JyA.
    Retorna: Legajo de JyA (LegajoJyA).
    """
    return LegajoJyA(**kwargs)


def add_fileJyA(fileJyA_form, teacher_or_therapist, horse_handler, track_assistant, equestrian):
    """ 
    Función para agregar un legajo de JyA a partir de un formulario.
    Atributos:
    - fileJyA_form (Form) - Formulario con los datos del legajo de JyA.
    - teacher_or_therapist (TeamMember) (opcional) - Miembro del equipo que es profesor o terapeuta.
    - horse_handler (TeamMember) (opcional) - Miembro del equipo que es cuidador de caballos.
    - track_assistant (TeamMember) (opcional) - Miembro del equipo que es asistente de pista.
    - equestrian (Equestrian) (opcional) - Jinete.
    """

    first_name = fileJyA_form.first_name.data
    last_name = fileJyA_form.last_name.data
    dni = fileJyA_form.dni.data

    age = fileJyA_form.age.data
    birth_date = fileJyA_form.birth_date.data
    birth_locality = fileJyA_form.birth_locality.data
    birth_province = fileJyA_form.birth_province.data

    adress_street = fileJyA_form.adress_street.data
    adress_number = fileJyA_form.adress_number.data
    adress_apartment = fileJyA_form.adress_apartment.data
    adress_locality = fileJyA_form.adress_locality.data
    adress_province = fileJyA_form.adress_province.data

    phone = fileJyA_form.phone.data
    emergency_contact_name = fileJyA_form.emergency_contact_name.data
    emergency_contact_phone = fileJyA_form.emergency_contact_phone.data

    if (fileJyA_form.disability_certificate.data == 'si'):
        disability_certificate_diagnosis = []
        disability_certificate = True
        disability_certificate_diagnosis = fileJyA_form.disability_certificate_diagnosis.data
        other_diagnosis_disability = fileJyA_form.other_diagnosis_disability.data
        disability_type = fileJyA_form.disability_type.data
    else:
        disability_certificate = False

    if (fileJyA_form.scholarship.data == 'si'):
        scholarship = True
        per_scholarship = fileJyA_form.per_scholarship.data
        scholarship_notes = fileJyA_form.scholarship_notes.data
    else:
        scholarship = False

    if (fileJyA_form.welfare.data == 'si'):
        welfare = True
        child_welfare = 'child_welfare' in fileJyA_form.welfare_type.data
        child_disability_welfare = 'child_disability_welfare' in fileJyA_form.welfare_type.data
        school_help_welfare = 'school_help_welfare' in fileJyA_form.welfare_type.data
    else:
        welfare = False

    if (fileJyA_form.pension_beneficiary.data == 'si'):
        pension_beneficiary = True
        pension_type = fileJyA_form.pension_type.data
    else:
        pension_beneficiary = False

    attending_professionals = fileJyA_form.attending_professionals.data

    file_jya = create_provisional_legajosJyA(
        first_name=first_name,
        last_name=last_name,
        dni=dni,
        age=age,
        birth_date=birth_date,
        birth_locality=birth_locality,
        birth_province=birth_province,
        adress_street=adress_street,
        adress_number=adress_number,
        adress_apartment=adress_apartment,
        adress_locality=adress_locality,
        adress_province=adress_province,
        phone=phone,
        emergency_contact_name=emergency_contact_name,
        emergency_contact_phone=emergency_contact_phone,
        disability_certificate=disability_certificate,
        disability_certificate_diagnosis=disability_certificate_diagnosis if disability_certificate else None,
        other_diagnosis_disability=other_diagnosis_disability if disability_certificate else None,
        disability_type=disability_type if disability_certificate else None,
        scholarship=scholarship,
        per_scholarship=per_scholarship if scholarship else None,
        scholarship_notes=scholarship_notes if scholarship else None,
        welfare=welfare,
        child_welfare=child_welfare if welfare else None,
        child_disability_welfare=child_disability_welfare if welfare else None,
        school_help_welfare=school_help_welfare if welfare else None,
        pension_beneficiary=pension_beneficiary,
        pension_type=pension_type if pension_beneficiary else None,
        attending_professionals=attending_professionals
    )

    # Situacion previsional

    social_security = fileJyA_form.social_security.data
    affiliate_number = fileJyA_form.affiliate_number.data
    has_guardianship = None
    if (fileJyA_form.has_guardianship.data == 'si'):
        has_guardianship = True
    elif (fileJyA_form.has_guardianship.data == 'no'):
        has_guardianship = False
    previsional_situacion_notes = fileJyA_form.previsional_situacion_notes.data

    previsional_situacion = create_provisional_provisional_situation(social_security=social_security,
                                                                     affiliate_number=affiliate_number,
                                                                     has_guardianship=has_guardianship if has_guardianship is not None else None,
                                                                     previsional_situacion_notes=previsional_situacion_notes)
    assign_fileJyA_provisional_situations(previsional_situacion, file_jya)
    commit_provisional_situacion(previsional_situacion)

    # Situacion escolar
    institution_name = fileJyA_form.institution_name.data
    school_address = fileJyA_form.school_address.data
    school_phone = fileJyA_form.school_phone.data
    current_grade = fileJyA_form.current_grade.data
    school_notes = fileJyA_form.school_notes.data

    school_situation = create_provisional_school_situation(
        institution_name=institution_name,
        school_address=school_address,
        school_phone=school_phone,
        current_grade=current_grade,
        school_notes=school_notes
    )
    assign_fileJyA_school_situation(school_situation, file_jya)
    commit_school_situation(school_situation)

    # Tutor 1
    relationship1 = fileJyA_form.relationship1.data
    first_name1 = fileJyA_form.first_name1.data
    last_name1 = fileJyA_form.last_name1.data
    dni1 = fileJyA_form.dni1.data
    current_address1 = fileJyA_form.current_address1.data
    mobile_phone1 = fileJyA_form.mobile_phone1.data
    email1 = fileJyA_form.email1.data
    education_level1 = fileJyA_form.education_level1.data
    occupation1 = fileJyA_form.occupation1.data

    tutor1 = create_tutor(relationship=relationship1,
                          first_name=first_name1,
                          last_name=last_name1,
                          dni=dni1,
                          current_address=current_address1,
                          mobile_phone=mobile_phone1,
                          email=email1,
                          education_level=education_level1,
                          occupation=occupation1
                          )

    relationship2 = fileJyA_form.relationship2.data
    first_name2 = fileJyA_form.first_name2.data
    last_name2 = fileJyA_form.last_name2.data
    dni2 = fileJyA_form.dni2.data
    current_address2 = fileJyA_form.current_address2.data
    mobile_phone2 = fileJyA_form.mobile_phone2.data
    email2 = fileJyA_form.email2.data
    education_level2 = fileJyA_form.education_level2.data
    occupation2 = fileJyA_form.occupation2.data

    tutor2 = create_tutor(
        relationship=relationship2,
        first_name=first_name2,
        last_name=last_name2,
        dni=dni2,
        current_address=current_address2,
        mobile_phone=mobile_phone2,
        email=email2,
        education_level=education_level2,
        occupation=occupation2
    )

    assign_tutors(file_jya, [tutor1, tutor2])

    work_proposal = fileJyA_form.work_proposal.data
    condition = fileJyA_form.condition.data
    location = fileJyA_form.location.data
    days = fileJyA_form.days.data

    previsional_work_proposal = create_provisional_work_proposal(work_proposal=work_proposal,
                                                                 condition=condition,
                                                                 location=location,
                                                                 days=days)

    assign_fileJyA_work_proposal(previsional_work_proposal, file_jya)

    if teacher_or_therapist:
        assign_teacher_or_teraphist_work_proposal(
            previsional_work_proposal, teacher_or_therapist)

    if horse_handler:
        assign_horse_handler_work_proposal(
            previsional_work_proposal, horse_handler)

    if track_assistant:
        assign_track_assistant_work_proposal(
            previsional_work_proposal, track_assistant)

    if equestrian:
        assign_equestrian_work_proposal(previsional_work_proposal, equestrian)

    commit_work_proposal(previsional_work_proposal)

    return commit_legajosJyA(file_jya)


def modify_filejya(oldFileJyAId, newLegajoForm, teacher_or_therapist, horse_handler, track_assistant, equestrian):
    """
    Función para modificar un legajo de JyA a partir de un formulario.
    Atributos:
    - oldFileJyAId (int) - ID del legajo de JyA a modificar.
    - newLegajoForm (Form) - Formulario con los datos del legajo de JyA.
    - teacher_or_therapist (TeamMember) (opcional) - Miembro del equipo que es profesor o terapeuta.
    - horse_handler (TeamMember) (opcional) - Miembro del equipo que es cuidador de caballos.
    - track_assistant (TeamMember) (opcional) - Miembro del equipo que es asistente de pista.
    - equestrian (Equestrian) (opcional) - Jinete.
    """
    databaseFileJyA = get_legajoJyA_by_id(oldFileJyAId)

    databaseFileJyA.first_name = newLegajoForm.first_name.data
    databaseFileJyA.last_name = newLegajoForm.last_name.data

    databaseFileJyA.age = newLegajoForm.age.data
    databaseFileJyA.birth_date = newLegajoForm.birth_date.data
    databaseFileJyA.birth_locality = newLegajoForm.birth_locality.data
    databaseFileJyA.birth_province = newLegajoForm.birth_province.data

    databaseFileJyA.adress_street = newLegajoForm.adress_street.data
    databaseFileJyA.adress_number = newLegajoForm.adress_number.data
    databaseFileJyA.adress_apartment = newLegajoForm.adress_apartment.data
    databaseFileJyA.adress_locality = newLegajoForm.adress_locality.data
    databaseFileJyA.adress_province = newLegajoForm.adress_province.data

    databaseFileJyA.phone = newLegajoForm.phone.data
    databaseFileJyA.emergency_contact_name = newLegajoForm.emergency_contact_name.data
    databaseFileJyA.emergency_contact_phone = newLegajoForm.emergency_contact_phone.data

    # Manejo de certificado de discapacidad
    if newLegajoForm.disability_certificate.data == 'si':
        databaseFileJyA.disability_certificate = True
        databaseFileJyA.disability_certificate_diagnosis = newLegajoForm.disability_certificate_diagnosis.data
        databaseFileJyA.other_diagnosis_disability = newLegajoForm.other_diagnosis_disability.data
        databaseFileJyA.disability_type = newLegajoForm.disability_type.data
    else:
        databaseFileJyA.disability_certificate = False
        databaseFileJyA.disability_certificate_diagnosis = None
        databaseFileJyA.other_diagnosis_disability = None
        databaseFileJyA.disability_type = None

    # Manejo de beca
    if newLegajoForm.scholarship.data == 'si':
        databaseFileJyA.scholarship = True
        databaseFileJyA.per_scholarship = newLegajoForm.per_scholarship.data
        databaseFileJyA.scholarship_notes = newLegajoForm.scholarship_notes.data
    else:
        databaseFileJyA.scholarship = False
        databaseFileJyA.per_scholarship = None
        databaseFileJyA.scholarship_notes = None

    # Manejo de bienestar
    if newLegajoForm.welfare.data == 'si':
        databaseFileJyA.welfare = True
        databaseFileJyA.child_welfare = 'child_welfare' in newLegajoForm.welfare_type.data
        databaseFileJyA.child_disability_welfare = 'child_disability_welfare' in newLegajoForm.welfare_type.data
        databaseFileJyA.school_help_welfare = 'school_help_welfare' in newLegajoForm.welfare_type.data
    else:
        databaseFileJyA.welfare = False
        databaseFileJyA.child_welfare = None
        databaseFileJyA.child_disability_welfare = None
        databaseFileJyA.school_help_welfare = None

    # Manejo de pensión
    if newLegajoForm.pension_beneficiary.data == 'si':
        databaseFileJyA.pension_beneficiary = True
        databaseFileJyA.pension_type = newLegajoForm.pension_type.data
    else:
        databaseFileJyA.pension_beneficiary = False
        databaseFileJyA.pension_type = None

    # Actualiza los profesionales que asisten
    databaseFileJyA.attending_professionals = newLegajoForm.attending_professionals.data

    # Accede al primer elemento
    provisional_situation = databaseFileJyA.provisional_situation[0]
    provisional_situation.social_security = newLegajoForm.social_security.data
    provisional_situation.affiliate_number = newLegajoForm.affiliate_number.data
    provisional_situation.previsional_situacion_notes = newLegajoForm.previsional_situacion_notes.data

    if (newLegajoForm.has_guardianship.data == 'si'):
        provisional_situation.has_guardianship = True
    elif (newLegajoForm.has_guardianship.data == 'no'):
        provisional_situation.has_guardianship = False

    commit_provisional_situacion(provisional_situation)

    school_situation = databaseFileJyA.school_situacion[0]

    # Actualiza los atributos de la situación escolar
    school_situation.institution_name = newLegajoForm.institution_name.data
    school_situation.school_address = newLegajoForm.school_address.data
    school_situation.school_phone = newLegajoForm.school_phone.data
    school_situation.current_grade = newLegajoForm.current_grade.data
    school_situation.school_notes = newLegajoForm.school_notes.data

    # Guarda los cambios en la base de datos
    commit_school_situation(school_situation)

    # Accede al primer tutor (tutor 1)
    tutor1 = databaseFileJyA.tutors[0]

    tutor1.relationship = newLegajoForm.relationship1.data
    tutor1.first_name = newLegajoForm.first_name1.data
    tutor1.last_name = newLegajoForm.last_name1.data
    tutor1.dni = newLegajoForm.dni1.data
    tutor1.current_address = newLegajoForm.current_address1.data
    tutor1.mobile_phone = newLegajoForm.mobile_phone1.data
    tutor1.email = newLegajoForm.email1.data
    tutor1.education_level = newLegajoForm.education_level1.data
    tutor1.occupation = newLegajoForm.occupation1.data

    commit_tutor(tutor1)

    # Accede al segundo tutor (tutor 2)
    tutor2 = databaseFileJyA.tutors[1]

    # Actualiza los atributos del segundo tutor
    tutor2.relationship = newLegajoForm.relationship2.data
    tutor2.first_name = newLegajoForm.first_name2.data
    tutor2.last_name = newLegajoForm.last_name2.data
    tutor2.dni = newLegajoForm.dni2.data
    tutor2.current_address = newLegajoForm.current_address2.data
    tutor2.mobile_phone = newLegajoForm.mobile_phone2.data
    tutor2.email = newLegajoForm.email2.data
    tutor2.education_level = newLegajoForm.education_level2.data
    tutor2.occupation = newLegajoForm.occupation2.data

    commit_tutor(tutor2)

    work_proposal = databaseFileJyA.work_proposal[0]

    work_proposal.work_proposal = newLegajoForm.work_proposal.data
    work_proposal.condition = newLegajoForm.condition.data
    work_proposal.location = newLegajoForm.location.data
    work_proposal.days = newLegajoForm.days.data

    if work_proposal.teacher_or_therapist:
        id = work_proposal.teacher_or_therapist.id
        if not teacher_or_therapist or int(teacher_or_therapist) != id:
            remove_teacher_or_teraphist_work_proposal(work_proposal)

        if teacher_or_therapist and int(teacher_or_therapist) != id:
            assign_teacher_or_teraphist_work_proposal(
                work_proposal, teacher_or_therapist)
    else:
        if teacher_or_therapist:
            assign_teacher_or_teraphist_work_proposal(
                work_proposal, teacher_or_therapist)

    if work_proposal.horse_handler:
        id = work_proposal.horse_handler.id
        if not horse_handler or int(horse_handler) != id:
            remove_horse_handler_work_proposal(work_proposal)

        if horse_handler and int(horse_handler) != id:
            assign_horse_handler_work_proposal(work_proposal, horse_handler)
    else:
        if horse_handler:
            assign_horse_handler_work_proposal(work_proposal, horse_handler)

    if work_proposal.track_assistant:
        id = work_proposal.track_assistant.id
        if not track_assistant or int(track_assistant) != id:
            remove_track_assistant_work_proposal(work_proposal)

        if track_assistant and int(track_assistant) != id:
            assign_track_assistant_work_proposal(
                work_proposal, track_assistant)
    else:
        if track_assistant:
            assign_track_assistant_work_proposal(
                work_proposal, track_assistant)

    if work_proposal.equestrian:
        id = work_proposal.equestrian.id
        if not equestrian or int(equestrian) != id:
            remove_equestrian_work_proposal(work_proposal)

        if equestrian and int(equestrian) != id:
            assign_equestrian_work_proposal(work_proposal, equestrian)
    else:
        if equestrian:
            assign_equestrian_work_proposal(work_proposal, equestrian)

    commit_work_proposal(work_proposal)

    return commit_legajosJyA(databaseFileJyA)


def commit_legajosJyA(file_jya):
    """
    Función para confirmar los cambios en un legajo de JyA en la base de datos.
    Atributos: 
    - file_jya (LegajoJyA) - Legajo de JyA a confirmar.
    Retorna: Legajo de JyA (LegajoJyA).
    """
    db.session.add(file_jya)
    db.session.commit()
    return file_jya


def order_legajosJyA(query, propiedad, order='asc'):
    """
    Función para ordenar los legajos de JyA.
    Atributos:
    - query (query) - Query de los legajos de JyA.
    - propiedad (str) - Propiedad por la cual ordenar.
    - order (str, default='asc') - Orden de los legajos de JyA.
    Retorna: Lista de Legajos JyA (list<LegajoJyA>).
    """

    def order_prop(query, parametro, order):
        if order == "desc":
            return query.order_by(desc(parametro))
        else:
            return query.order_by(asc(parametro))

    if (propiedad == 'first_name'):
        return order_prop(query, LegajoJyA.first_name, order)
    if (propiedad == 'last_name'):
        return order_prop(query, LegajoJyA.last_name, order)


def search_legajos(first_name=None, last_name=None, dni=None, attending_professionals=None):
    """
    Función para buscar legajos de JyA a partir de filtros.
    Atributos:
    - first_name (str) - Nombre del legajo de JyA.
    - last_name (str, default='None') - Apellido del legajo de JyA.
    - dni (str, default='None') - DNI del legajo de JyA.
    - attending_professionals (list<TeamMember>, default='None') - Profesionales que asisten al legajo de JyA.
    Retorna: Lista de legajos de JyA (list<LegajoJyA>).
    """
    legajos = query_legajosJyA()
    # legajos = legajos.filter_by(deleted=False)

    if first_name:
        legajos = legajos.filter(func.lower(
            LegajoJyA.first_name).contains(first_name.lower()))
    if last_name:
        legajos = legajos.filter(func.lower(
            LegajoJyA.last_name).contains(last_name.lower()))
    if dni:
        legajos = legajos.filter(LegajoJyA.dni.startswith(dni))
    if attending_professionals:
        legajos = legajos.filter(func.lower(
            LegajoJyA.attending_professionals).contains(attending_professionals.lower()))

    return legajos


def create_legajoJyA(**kwargs):
    """
    Función para crear un legajo de JyA. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Diccionario con los atributos del legajo de JyA.
    Retorna: Legajo de JyA (LegajoJyA).
    """
    legajoJyA = LegajoJyA(**kwargs)
    db.session.add(legajoJyA)
    db.session.commit()

    return legajoJyA


def legajo_jya_exists_by_dni(dni):
    """
    Función para verificar si un legajo de JyA existe a partir de un DNI.
    Atributos: dni (int) - DNI del legajo de JyA.
    Retorna: bool - True si existe, False si no.
    """
    return LegajoJyA.query.filter_by(deleted=False).filter_by(dni=dni).first() is not None


def assign_tutors(fileJyA, tutors):
    """
    Función para asignar tutores a un legajo de JyA.
    Atributos:
    - fileJyA (LegajoJyA) - Legajo de JyA al que asignar los tutores.
    - tutors (list<Tutor>) - Lista de tutores a asignar.
    Retorna: Legajo de JyA (LegajoJyA).
    """
    fileJyA.tutors = tutors
    db.session.add(fileJyA)
    db.session.commit()

    return fileJyA


def filejya_has_receipts(filejya):
    """
    Función para verificar si un legajo de JyA tiene recibos.
    Atributos: filejya (LegajoJyA) - Legajo de JyA.
    Retorna: Legajo de JyA (LegajoJyA) o None - .
    """
    return filejya.receipts.filter_by(deleted=False).first()


def legajos_in_debt():
    """
    Función para buscar legajos de JyA con deuda.
    Retorna: Lista de legajos de JyA (list<LegajoJyA>).
    """
    legajos = query_legajosJyA()
    return legajos.filter_by(in_debt=True).all()


# Funciones para la creación de tablas de usuario


def list_users():
    """
    Función para listar los usuarios.
    Atributos: Ninguno.
    Retorna: Lista de usuarios (list<User>).
    """
    users = User.query.filter(User.deleted == False, User.role_id != 1).all()
    return users


def create_user(**kwargs):
    """
    Función para crear un usuario. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Diccionario con los atributos del usuario.
    Retorna: Usuario (User).
    """
    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs["password"] = hash.decode("utf-8")
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user


def assign_role(user, role):
    """
    Función para asignar un rol a un usuario.
    Atributos:
    - user (User) - Usuario al que asignar el rol.
    - role (Role) - Rol a asignar.
    Retorna: Usuario (User).
    """
    user.role = role
    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_email(email):
    """
    Función para obtener un usuario por su email.
    Atributos: email (str) - Email del usuario.
    Retorna: Usuario (User) o None.
    """
    user = User.query.filter_by(email=email).first()
    return user


def get_permissions(user_email):
    """
    Función para obtener los permisos de un usuario.
    Atributos: user_email (str) - Email del usuario.
    Retorna: Conjunto de permisos (set<Permission>).
    (No se usa)
    """
    permissions = (
        User.query.join(Role)
        .join(Role.permissions)
        .filter(User.email == user_email)
        .with_entities(Permission.name)
        .all()
    )


def get_user_by_id(id):
    """
    Función para obtener un usuario por su ID.
    Atributos: id (int) - ID del usuario.
    Retorna: Usuario (User) o None.
    """
    user = User.query.filter_by(id=id).first()
    return user


def get_permissions(user_email):
    """
    Función para obtener los permisos de un usuario.
    Atributos: user_email (str) - Email del usuario.
    Retorna: Conjunto de permisos (set<Permission>).
    """
    permissions = User.query.join(Role).join(Role.permissions).filter(
        User.email == user_email).with_entities(Permission.name).all()
    permissions_set = {perm[0] for perm in permissions}
    return permissions_set


def check_user(email, password):
    """
    Función para verificar un usuario al iniciar sesión.
    Atributos:
    - email (str) - Email del usuario.
    - password (str) - Contraseña del usuario.
    Retorna: Usuario (User) o None (si falla la verificación).
    """
    user = get_user_by_email(email)
    # si el usuario existe y la contraseña es correcta
    if user and bcrypt.check_password_hash(user.password, password):
        return user

    return None


def get_role(session):
    """
    Función para obtener el rol de un usuario a partir de la sesión activa.
    Atributos: 
    - session (dict) Sesión activa.
    Retorna: Rol (Role).
    """
    user_email = session.get("user")
    role = User.query.join(Role).filter(
        User.email == user_email).with_entities(Role.name).first()
    return role


def get_user_by_dni(dni):
    """
    Función para obtener un usuario por su DNI.
    Atributos: 
    - dni (int) - DNI del usuario.
    Retorna: Usuario (User) o None.
    """
    user = User.query.filter_by(dni=dni).first()
    return user


def create_provisional_user(**kwargs):
    """
    Función para crear un usuario provisional.
    Atributos: kwargs (dict) - Diccionario con los atributos del usuario.
    Retorna: Usuario (User).
    """
    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs["password"] = hash.decode("utf-8")
    return User(**kwargs)


def encrypt_user_password(user):
    """
    Función para encriptar la contraseña de un usuario.
    Atributos: user (User) - Usuario.
    Retorna: Usuario (User) con el atributo 'password' encriptado.
    """
    hash = bcrypt.generate_password_hash(user.password.encode("utf-8"))
    user.password = hash.decode("utf-8")
    return user


def assign_user_role_with_roleid_filled_in(user):
    """
    Función para asignar un rol a un usuario a partir de su ID de rol.
    Atributos: user (User) - Usuario.
    Retorna: None.
    """
    # Aquí el role_id existe
    if (user.role_id):
        role = Role.query.get(user.role_id)
        user.role = role


def commit_user(user):
    """
    Función para confirmar los cambios en un usuario en la base de datos.
    Atributos: user (User) - Usuario.
    Retorna: Usuario (User).
    """
    db.session.add(user)
    db.session.commit()
    return user


def search_users(email_filter, active_filter, role_filter, search_string):
    """
    Función para buscar usuarios a partir de filtros, obviando al system admin.
    Atributos:
    - email_filter (string) - Filtro por email.
    - active_filter (string) - Filtro por activo.
    - role_filter (string) - Filtro por rol.
    - search_string (string) - Cadena de búsqueda.
    Retorna: Lista de usuarios (list<User>).
    """

    query = User.query
    if search_string:
        search_string = f"{search_string.strip()}"
        if email_filter:
            query = query.filter(User.email.ilike(f"%{search_string}%"))
        elif active_filter:
            if search_string.lower() == "si" or search_string.lower() == "sí":
                query = query.filter(
                    User.is_enabled == True)
            else:
                query = query.filter(
                    User.is_enabled == False)
        elif role_filter:
            query = query.join(User.role).filter(
                Role.name.ilike(f"%{search_string}%"))
    results = query.filter(User.deleted == False).all()
    # eliminar system admin del resultado, si existe, chequeando el campo de rol
    results = [user for user in results if user.role_id != 1]

    return results


def delete_user(user):
    """ 
    Función para eliminar un usuario físicamente. No se debe usar.
    Atributos: user (User) - Usuario.
    Retorna: None.
    """
    db.session.delete(user)
    db.session.commit()

# Funciones para la creacion de tablas de rol


def list_roles():
    """
    Función para listar los roles.
    Atributos: Ninguno.
    Retorna: Lista de roles (list<Role>).
    """
    roles = Role.query.all()
    return roles


def create_role(**kwargs):
    """
    Función para crear un rol. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Diccionario con los atributos del rol.
    Retorna: Rol (Role).
    """
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()
    return role


def get_role_by_name(name):
    """
    Función para obtener el ID del rol por su nombre.
    Atributos: name (str) - Nombre del rol.
    Retorna: id del rol.
    """
    role = Role.query.filter_by(name=name).first()
    return role.id


def assign_permissions(role, permissions):
    """
    Función para asignar permisos a un rol.
    Atributos:
    - role (Role) - Rol al que asignar los permisos.
    - permissions (list<Permission>) - Lista de permisos a asignar.
    Retorna: Rol (Role).
    """
    role.permissions = permissions
    db.session.add(role)
    db.session.commit()

    return role


# Funciones para la creacion de tablas de permiso


def list_permissions():
    """
    Función para listar los permisos.
    Atributos: Ninguno.
    Retorna: Lista de permisos (list<Permission>).
    """
    permissions = Permission.query.all()
    return permissions


def create_permission(**kwargs):
    """
    Función para crear un permiso. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Diccionario con los atributos del permiso.
    Retorna: Permiso (Permission).
    """
    permission = Permission(**kwargs)
    db.session.add(permission)
    db.session.commit()
    return permission


# Funciones para la creacion de tablas de cobro


def list_receipts():
    """
    Función para listar los recibos.
    Atributos: Ninguno.
    Retorna: Lista de recibos (list<Receipt>).
    """
    receipts = Receipt.query.all()
    return receipts


def query_receipts():
    """
    Función para listar los recibos.
    Atributos: Ninguno.
    Retorna: Lista de recibos (list<Receipt>).
    """
    receipts = Receipt.query.filter_by(deleted=False)
    return receipts


def create_receipt(**kwargs):
    """
    Función para crear un recibo. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Diccionario con los atributos del recibo.
    Retorna: Recibo (Receipt).
    """
    receipt = Receipt(**kwargs)
    db.session.add(receipt)
    db.session.commit()
    return receipt


def create_provisional_receipt(**kwargs):
    """
    Función para crear un recibo provisional.
    Atributos: kwargs (dict) - Diccionario con los atributos del recibo.
    Retorna: Recibo (Receipt).
    """
    return Receipt(**kwargs)


def commit_receipt(receipt):
    """
    Función para confirmar los cambios en un recibo en la base de datos.
    Atributos: receipt (Receipt) - Recibo.
    Retorna: Recibo (Receipt).
    """
    db.session.add(receipt)
    db.session.commit()
    return receipt


def assign_fileJyA_receipt(receipt, fileJyA):
    """
    Función para asignar un legajo de JyA a un recibo.
    Atributos:
    - receipt (Receipt) - Recibo al que asignar el legajo de JyA.
    - fileJyA (LegajoJyA) - Legajo de JyA a asignar.
    Retorna: Recibo (Receipt).
    """
    receipt.fileJyA = LegajoJyA.query.get(fileJyA)
    db.session.add(receipt)
    db.session.commit()

    return receipt


def assign_team_member_receipt(receipt, team_member):
    """
    Función para asignar un miembro del equipo a un recibo.
    Atributos:
    - receipt (Receipt) - Recibo al que asignar el miembro del equipo.
    - team_member (TeamMember) - Miembro del equipo a asignar.
    Retorna: Recibo (Receipt).
    """
    receipt.team_member = TeamMember.query.get(team_member)
    db.session.add(receipt)
    db.session.commit()

    return receipt


def filter_receipts(receipts, team_member_name=None, team_member_surname=None, start_date=None, end_date=None, payment_method=None):
    """
    Función para filtrar recibos a partir de filtros.
    Atributos:
    - receipts (query) - Query de los recibos.
    - team_member_name (str, default='None') - Nombre del miembro del equipo.
    - team_member_surname (str, default='None') - Apellido del miembro del equipo.
    - start_date (date, default='None') - Fecha de inicio.
    - end_date (date, default='None') - Fecha de fin.
    - payment_method (str, default='None') - Método de pago.
    Retorna: Lista de recibos (list<Receipt>).
    """
    receipts = receipts.filter_by(deleted=False)
    if team_member_name:
        # Filtra por el nombre del miembro del equipo
        receipts = receipts.join(Receipt.team_member).filter(func.lower(
            TeamMember.first_name).startswith(team_member_name.lower()))
    if team_member_surname:
        # Filtra por el apellido del miembro del equipo
        receipts = receipts.join(Receipt.team_member).filter(func.lower(
            TeamMember.last_name).startswith(team_member_surname.lower()))
    if payment_method:
        receipts = receipts.filter(func.lower(
            Receipt.payment_method).startswith(payment_method.lower()))
    if start_date and end_date:
        receipts = receipts.filter(
            and_(Receipt.payment_date >= start_date, Receipt.payment_date <= end_date))
    elif start_date:
        receipts = receipts.filter(Receipt.payment_date >= start_date)
    elif end_date:
        receipts = receipts.filter(Receipt.payment_date <= end_date)

    return receipts


def order_receipts(query, order_by_date="asc"):
    """
    Función para ordenar los recibos.
    Atributos:
    - query (query) - Query de los recibos.
    - order_by_date (str, default='asc') - Orden de los recibos.
    Retorna: Lista de recibos (list<Receipt>).
    """
    if order_by_date == "desc":
        return query.order_by(desc(Receipt.payment_date))
    else:
        return query.order_by(asc(Receipt.payment_date))


def search_receipts(team_member_name=None, team_member_surname=None, start_date=None, end_date=None, payment_method=None):
    """
    Función para buscar recibos a partir de filtros.
    Atributos:
    - team_member_name (str, default='None') - Nombre del miembro del equipo.
    - team_member_surname (str, default='None') - Apellido del miembro del equipo.
    - start_date (date, default='None') - Fecha de inicio.
    - end_date (date, default='None') - Fecha de fin.
    - payment_method (str, default='None') - Método de pago.
    Retorna: Lista de recibos (list<Receipt>).
    """
    query = Receipt.query.options(joinedload(Receipt.team_member))

    # Aplicar filtros
    query = filter_receipts(
        query, team_member_name, team_member_surname, start_date, end_date, payment_method)

    return query


def remove_team_member_receipt(receipt):
    """
    Función para remover un miembro del equipo de un recibo.
    Atributos: receipt (Receipt) - Recibo.
    Retorna: None.
    """
    receipt.team_member = None


def remove_fileJyA_receipt(receipt):
    """
    Función para remover un legajo de JyA de un recibo.
    Atributos: receipt (Receipt) - Recibo.
    Retorna: None.
    """
    receipt.fileJyA = None


def get_receipt_by_id(receipt_id):
    """
    Función para obtener un recibo por su ID.
    Atributos: receipt_id (int) - ID del recibo.
    Retorna: Recibo (Receipt).
    """
    receipt = Receipt.query.get(receipt_id)
    return receipt


def delete_receipt(receipt):
    """
    Función para eliminar un recibo lógicamente.
    Atributos: receipt (Receipt) - Recibo.
    Retorna: None.
    """
    receipt.deleted = True
    db.session.commit()


def modify_receipt(oldReceiptId, newReceiptForm, team_member, fileJyA):
    """
    Función para modificar un recibo a partir de un formulario.
    Atributos:
    - oldReceiptId (int) - ID del recibo a modificar.
    - newReceiptForm (Form) - Formulario con los nuevos datos del recibo.
    - team_member (TeamMember) - Miembro del equipo a asignar.
    - fileJyA (LegajoJyA) - Legajo de JyA a asignar.
    Retorna: None.
    """
    databaseReceipt = get_receipt_by_id(oldReceiptId)

    databaseReceipt.payment_method = newReceiptForm.payment_method.data
    databaseReceipt.payment_date = newReceiptForm.payment_date.data
    databaseReceipt.amount = newReceiptForm.amount.data
    databaseReceipt.notes = newReceiptForm.notes.data

    if (not (team_member == databaseReceipt.team_member.id)):

        remove_team_member_receipt(databaseReceipt)
        assign_team_member_receipt(databaseReceipt, team_member)

    if (not (fileJyA == databaseReceipt.fileJyA.id)):

        remove_fileJyA_receipt(databaseReceipt)
        assign_fileJyA_receipt(databaseReceipt, fileJyA)

    return commit_receipt(databaseReceipt)


def add_receipt(receiptForm, team_member, file_JyA):
    """ 
    Función para agregar un recibo a partir de un formulario.
    Atributos:
    - receiptForm (Form) - Formulario con los datos del recibo.
    - team_member (TeamMember) - Miembro del equipo a asignar.
    - file_JyA (LegajoJyA) - Legajo de JyA a asignar.
    Retorna: Recibo (Receipt).
    """
    payment_date = receiptForm.payment_date.data
    payment_method = receiptForm.payment_method.data
    amount = receiptForm.amount.data
    notes = receiptForm.notes.data

    receipt = create_provisional_receipt(
        payment_date=payment_date, payment_method=payment_method, amount=amount, notes=notes)

    assign_team_member_receipt(receipt, team_member)
    assign_fileJyA_receipt(receipt, file_JyA)
    return commit_receipt(receipt)


# Funciones para la creacion de tablas de miembro_equipo


def list_miembros_equipo():
    """
    Función para listar los miembros del equipo.
    Atributos: Ninguno.
    Retorna: Lista de miembros del equipo (list<TeamMember>).
    """
    miembros_equipo = TeamMember.query.all()
    return miembros_equipo


def list_miembros_equipo_not_eliminated():
    """
    Función para listar los miembros del equipo no eliminados.
    Atributos: Ninguno.
    Retorna: Lista de miembros del equipo (list<TeamMember>).
    """
    miembros_equipo = TeamMember.query.filter(
        TeamMember.deleted == False).all()
    return miembros_equipo


def list_miembros_equipo_active_paid():
    """
    Función para listar los miembros del equipo no eliminados, activos y rentados.
    Atributos: Ninguno.
    Retorna: Lista de miembros del equipo (list<TeamMember>).
    """
    miembros_equipo = TeamMember.query.filter(
        TeamMember.deleted == False)
    miembros_equipo = miembros_equipo.filter_by(active=True)
    miembros_equipo = miembros_equipo.filter_by(
        condition="Personal Rentado").all()
    return miembros_equipo


def is_email_taken(email):
    """
    Función para verificar si un email ya está en uso.
    Atributos: email (str) - Email a verificar.
    Retorna: bool - True si el email está en uso, False si no.
    """
    return TeamMember.query.filter_by(email=email).first()


def is_dni_taken(dni):
    """
    Función para verificar si un DNI ya está en uso.
    Atributos: dni (int) - DNI a verificar.
    Retorna: bool - True si el DNI está en uso, False si no.
    """
    return TeamMember.query.filter_by(dni=dni).first()


def create_team_member(**kwargs):
    """
    Función para crear un miembro del equipo. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Diccionario con los atributos del miembro del equipo.
    Retorna: Miembro del equipo (TeamMember).
    """
    # Extraer el DNI del argumento kwargs
    dni = kwargs.get('dni')

    # Verificar si el usuario ya existe
    usuario_existente = User.query.filter_by(dni=dni, deleted=False).first()
    if usuario_existente:
        usuario = usuario_existente
    else:
        usuario = None  # No hay usuario asociado

    # Crear un nuevo miembro del equipo con el usuario correspondiente
    new_member = TeamMember(user=usuario, **kwargs)

    db.session.add(new_member)
    db.session.commit()
    return new_member


def update_team_member(team_member, form):
    """
    Función para actualizar un miembro del equipo a partir de un formulario.
    Atributos:
    - team_member (TeamMember) - Miembro del equipo a actualizar.
    - form (Form) - Formulario con los nuevos datos del miembro del equipo.
    Retorna: None.
    """
    for field_name, field_value in form.data.items():
        if field_name != 'documents':  # Excluir 'documents'
            setattr(team_member, field_name, field_value)
    db.session.commit()


def get_team_member_by_id(id):
    """
    Función para obtener un miembro del equipo por su ID.
    Atributos: id (int) - ID del miembro del equipo.
    Retorna: Miembro del equipo (TeamMember) o None.
    """
    return db.session.query(TeamMember).filter(TeamMember.id == id, TeamMember.deleted == False).first()


def get_member_by_dni(dni):
    """
    Función para obtener un miembro del equipo por su DNI.
    Atributos: dni (int) - DNI del miembro del equipo.
    Retorna: Miembro del equipo (TeamMember) o None.
    """
    member = db.session.query(TeamMember).filter(
        TeamMember.dni == dni, TeamMember.deleted == False).first()
    return member


def delete_team_member(team_member):
    """
    Función para eliminar un miembro del equipo lógicamente. Elimina también al usuario asociado, si existe.
    Atributos: team_member (TeamMember) - Miembro del equipo.
    Retorna: None.
    """
    team_member.deleted = True
    if team_member.user:
        team_member.user.is_enabled = False
    if team_member.documents:
        for document in team_member.documents:
            delete_document(document)
    db.session.commit()


def get_members(page, per_page, selected_filter, search_string, job_position, order_by='created_at', order_position='asc'):
    """
    Función para obtener los miembros del equipo a partir de filtros y paginación.
    Atributos:
    - page (int) - Página actual.
    - per_page (int) - Cantidad de miembros por página.
    - selected_filter (str) - Filtro seleccionado.
    - search_string (str) - Cadena de búsqueda.
    - job_position (str) - Puesto laboral.
    - order_by (str, default='created_at') - Ordenar por.
    - order_position (str, default='asc') - Orden.
    Retorna: Lista de miembros del equipo (list<TeamMember>), Número total de páginas (int).
    """
    query = db.session.query(TeamMember).filter(TeamMember.deleted == False)

    # Filtrar según el filtro seleccionado
    if selected_filter == 'first_name':
        query = query.filter(TeamMember.first_name.ilike(f'%{search_string}%'))
    elif selected_filter == 'last_name':
        query = query.filter(TeamMember.last_name.ilike(f'%{search_string}%'))
    elif selected_filter == 'dni':
        query = query.filter(TeamMember.dni.ilike(f'%{search_string}%'))
    elif selected_filter == 'email':
        query = query.filter(TeamMember.email.ilike(f'%{search_string}%'))
    elif selected_filter == 'job_position':
        query = query.filter(TeamMember.job_position.ilike(
            f'%{job_position}%'))  # Filtrar por puesto laboral

    total_members = query.with_entities(
        func.count()).scalar()  # Contar el total de miembros

    # Manejar ordenamiento
    if order_position == 'asc':
        query = query.order_by(asc(getattr(TeamMember, order_by)))
    else:
        query = query.order_by(desc(getattr(TeamMember, order_by)))
    # Paginación manual
    # Obtener los miembros de la página actual
    members = query.offset((page - 1) * per_page).limit(per_page).all()

    # Calcular el número total de páginas
    total_pages = (total_members + per_page - 1) // per_page

    return members, total_pages


def query_miembros_equipo():
    """
    Función para listar los miembros del equipo.
    Atributos: Ninguno.
    Retorna: query de miembros del equipo (query<TeamMember>).
    """
    query = TeamMember.query  # Esto devuelve la query sin ejecutarla
    return query


def order_team_members_last_name(query, order="asc"):
    """
    Función para ordenar los miembros del equipo por apellido.
    Atributos:
    - query (query) - Query de los miembros del equipo.
    - order (str, default='asc') - Orden de los miembros del equipo.
    Retorna: Lista de miembros del equipo (list<TeamMember>).
    """
    if order == "desc":
        return query.order_by(desc(TeamMember.last_name))
    else:
        return query.order_by(asc(TeamMember.last_name))


def get_documents_by_team_member_id(team_member_id):
    # Realizar la consulta a la base de datos para obtener los documentos
    return Document.query.filter_by(team_member_id=team_member_id, deleted=False).all()


# Funciones para la creacion de tablas de documentos


def list_documents():
    """
    Función para listar los documentos.
    Atributos: Ninguno.
    Retorna: Lista de documentos (list<Document>).
    """
    documents = Document.query.all()
    return documents


def delete_document(document):
    if document:
        document.deleted = True
        db.session.commit()
        return True
    return False


def get_document_by_id(id):
    document = Document.query.filter_by(id=id, deleted=False).first()
    return document


def create_document(**kwargs):
    """
    Función para crear un documento. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Diccionario con los atributos del documento.
    Retorna: Documento (Document).
    """
    documento = Document(**kwargs)
    db.session.add(documento)
    db.session.commit()
    return documento


def addDocumentLegajo(params, id):
    name = params["title"]
    path = params["documento"]
    id_type_doc = params['type_doc']
    document = Document(name=name, path=path)
    db.session.add(document)

    type_doc = TypeDocFileJyA.query.filter_by(id=id_type_doc).first()
    assign_typedoc_fileJyA(document, type_doc)

    legajo = get_legajoJyA_by_id(id)
    assign_fileJyA_document(document, legajo)

    db.session.commit()

    return document.id


def addLinkLegajo(params, id):
    name = params["title"]
    link = params["enlace"]
    id_type_doc = params['type_doc']
    document = Document(name=name, link=link)
    db.session.add(document)

    type_doc = TypeDocFileJyA.query.filter_by(id=id_type_doc).first()
    assign_typedoc_fileJyA(document, type_doc)

    legajo = get_legajoJyA_by_id(id)
    assign_fileJyA_document(document, legajo)

    db.session.commit()

    return document.id


def updateDocumentLegajo(params, document):
    document.name = params["title"]
    if document.link:
        document.link = params["enlace"]
    elif "documento" in params:
        document.path = params["documento"]
    id_type_doc = params['type_doc']
    type_doc = TypeDocFileJyA.query.filter_by(id=id_type_doc).first()
    assign_typedoc_fileJyA(document, type_doc)
    db.session.add(document)
    db.session.commit()


def assign_team_member_document(document, team_member):
    """
    Función para asignar un miembro del equipo a un documento.
    Atributos:
    - document (Document) - Documento al que asignar el miembro del equipo.
    - team_member (TeamMember) - Miembro del equipo a asignar.
    Retorna: Documento (Document).
    """
    document.team_member = team_member
    db.session.add(document)
    db.session.commit()

    return document


def assign_equestrian(document, equestrian):
    """
    Función para asignar un jinete a un documento.
    Atributos:
    - document (Document) - Documento al que asignar el jinete.
    - equestrian (Equestrian) - Jinete a asignar.
    Retorna: Documento (Document).
    """
    document.equestrian = equestrian
    db.session.add(document)
    db.session.commit()

    return document


def assign_fileJyA_document(document, fileJyA):
    """
    Función para asignar un legajo de JyA a un documento.
    Atributos:
    - document (Document) - Documento al que asignar el legajo de JyA.
    - fileJyA (LegajoJyA) - Legajo de JyA a asignar.
    Retorna: Documento (Document).
    """
    document.fileJyA = fileJyA
    db.session.add(document)
    db.session.commit()

    return document


def assign_typedoc_fileJyA(document, typedoc_fileJyA):
    """
    Función para asignar un tipo de documento a un documento.
    Atributos:
    - document (Document) - Documento al que asignar el tipo de documento.
    - typedoc_fileJyA (TypedocFileJyA) - Tipo de documento a asignar.
    Retorna: Documento (Document).
    """
    document.typedoc_fileJyA = typedoc_fileJyA
    db.session.add(document)
    db.session.commit()

    return document


def assign_typedoc_equestrian(document, typedoc_equestrian):
    """
    Función para asignar un tipo de documento a un documento.
    Atributos:
    - document (Document) - Documento al que asignar el tipo de documento.
    - typedoc_equestrian (TypedocEquestrian) - Tipo de documento a asignar.
    Retorna: Documento (Document).
    """
    document.typedoc_equestrian = typedoc_equestrian
    db.session.add(document)
    db.session.commit()

    return document


# Funciones para la creacion de tablas de pagos


def list_payments():
    """
    Función para listar los pagos.
    Atributos: Ninguno
    Retorna: Los pagos (list<Payment>).
    """
    payments = Payment.query.all()
    return payments


def create_payment(**kwargs):
    """
    Función para crear un pago. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Los atributos del pago.
    Retorna: El pago creado.
    """
    pago = Payment(**kwargs)
    db.session.add(pago)
    db.session.commit()
    return pago


def get_payment_by_id(id):
    """
    Función para obtener un pago por su ID.
    Atributos: id (int) - El ID del pago.
    Retorna: El pago o None.
    """
    payment_type = Payment.query.filter_by(id=id).first()
    return payment_type


def assign_payment_type(payment, payment_type):
    """
    Función para asignar un tipo de pago a un pago. Retorna el pago.
    Atributos:
    - payment (Payment) - El pago a asignar.
    - payment_type (PaymentType) - El tipo de pago a asignar.
    Retorna: El pago (Payment).
    """
    payment.payment_type = payment_type
    db.session.add(payment)
    db.session.commit()

    return payment


def assign_team_member_payment(payment, team_member):
    """
    Función para asignar un miembro del equipo a un pago. Retorna el pago.
    Atributos:
    - payment (Payment) - El pago a asignar.
    - team_member (TeamMember) - El miembro del equipo a asignar.
    Retorna: El pago (Payment).
    """
    payment.team_member = team_member
    db.session.add(payment)
    db.session.commit()
    return payment


def get_payments(page, per_page, selected_filter, start_date, end_date, payment_type, order_by='created_at', order_direction='asc'):
    """
    Función para obtener los pagos a partir de filtros y paginación.
    Atributos:
    - page (int) - Página actual.
    - per_page (int) - Cantidad de pagos por página.
    - selected_filter (str) - Filtro seleccionado.
    - start_date (date) - Fecha de inicio.
    - end_date (date) - Fecha de fin.
    - payment_type (str) - Tipo de pago.
    - order_by (str, default='created_at') - Ordenar por.
    - order_direction (str, default='asc') - Orden.
    Retorna: Lista de pagos (list<Payment>), Número total de páginas (int).
    """
    # Iniciar la consulta a la base de datos
    query = db.session.query(Payment).filter(Payment.deleted == False)

    # Filtrar según el filtro seleccionado
    if selected_filter == 'payment_date':
        query = query.filter(
            Payment.payment_date.between(start_date, end_date))
    elif selected_filter == 'payment_type':
        query = query.join(PaymentType).filter(
            PaymentType.name == payment_type)

    total_payments = query.with_entities(
        func.count()).scalar()  # Contar el total de pagos

    # Manejar ordenamiento
    if order_direction == 'asc':
        query = query.order_by(asc(getattr(Payment, order_by)))
    else:
        query = query.order_by(desc(getattr(Payment, order_by)))

    # Paginación manual
    # Obtener los pagos de la página actual
    payments = query.offset((page - 1) * per_page).limit(per_page).all()

    total_pages = (total_payments + per_page - 1) // per_page

    return payments, total_pages


def update_payment(payment, form):
    """
    Función para actualizar un pago a partir de un formulario.
    Atributos:
    - payment (Payment) - El pago a actualizar.
    - form (Form) - El formulario con los nuevos datos del pago.
    Retorna: El pago (Payment).
    """
    payment.amount = form.amount.data
    payment.payment_date = form.payment_date.data
    payment.description = form.description.data
    db.session.commit()
    return payment


def delete_payment(payment):
    """ 
    Función para eliminar un pago lógicamente.
    Atributos: payment (Pago) El pago a eliminar.
    Retorna: None
    """
    payment.deleted = True
    db.session.commit()


# Funciones para la creacion de tablas de paymentType


def list_payment_type():
    """
    Función para listar los tipos de pago.
    Atributos: Ninguno
    Retorna: Los tipos de pago (PaymentType).
    """
    payment_type = PaymentType.query.all()
    return payment_type


def create_payment_type(**kwargs):
    """
    Función para crear un tipo de pago. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Los atributos del tipo de pago.
    Retorna: El tipo de pago creado (PaymentType).
    """
    payment_type = PaymentType(**kwargs)
    db.session.add(payment_type)
    db.session.commit()
    return payment_type


def get_payment_type_by_id(id):
    """
    Función para obtener un tipo de pago por su ID.
    Atributos: id (int) - El ID del tipo de pago.
    Retorna: El tipo de pago (PaymentType) o None.
    """
    payment_type = PaymentType.query.filter_by(id=id).first()
    return payment_type


def filter_payment_dates(start_date=None, end_date=None):
    """
    Función para filtrar pagos entre dos fechas.
    Atributos:
    - payments (query) - Query de los pagos.
    - start_date (date, default='None') - Fecha de inicio.
    - end_date (date, default='None') - Fecha de fin.
    Retorna: Lista de pagos (list<Payment>).
    """
    payments = Payment.query.filter_by(deleted=False)

    if start_date and end_date:
        payments = payments.filter(
            and_(Payment.payment_date >= start_date, Payment.payment_date <= end_date))
    elif start_date:
        payments = payments.filter(Payment.payment_date >= start_date)
    elif end_date:
        payments = payments.filter(Payment.payment_date <= end_date)

    return payments


def get_amount_spent(start_date=None, end_date=None):
    payments = filter_payment_dates(start_date, end_date)
    total_amount = payments.with_entities(
        func.sum(Payment.amount)).scalar() or 0
    return total_amount


# Funciones para la creacion de tablas de situacion_provisional


def list_provisional_situations():
    """
    Función para listar las situaciones provisionales.
    Atributos: Ninguno
    Retorna: Las situaciones provisionales (list<ProvisionalSituation>).
    """
    provisional_situations = ProvisionalSituation.query.all()
    return provisional_situations


def create_provisional_situation(**kwargs):
    """
    Función para crear una situación provisional. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Los atributos de la situación provisional.
    Retorna: La situación provisional creada (ProvisionalSituation).
    """
    situacion_provisional = ProvisionalSituation(**kwargs)
    db.session.add(situacion_provisional)
    db.session.commit()
    return situacion_provisional


def create_provisional_provisional_situation(**kwargs):
    """
    Función para crear una situación provisional.
    Atributos: kwargs (dict) - Los atributos de la situación provisional.
    Retorna: La situación provisional creada (ProvisionalSituation).
    """
    situacion_provisional = ProvisionalSituation(**kwargs)
    return situacion_provisional


def commit_provisional_situacion(situacion_provisional):
    """
    Función para confirmar los cambios en una situación provisional en la base de datos.
    Atributos: situacion_provisional (ProvisionalSituation) - La situación provisional.
    Retorna: La situación provisional (ProvisionalSituation).
    """
    db.session.add(situacion_provisional)
    db.session.commit()
    return situacion_provisional


def assign_fileJyA_provisional_situations(provisional_situations, fileJyA):
    """
    Función para asignar un legajo de JyA a una situación provisional.
    Atributos:
    - provisional_situations (ProvisionalSituation) - La situación provisional a asignar.
    - fileJyA (LegajoJyA) - El legajo de JyA a asignar.
    Retorna: La situación provisional (ProvisionalSituation).
    """
    provisional_situations.fileJyA = fileJyA
    db.session.add(provisional_situations)
    db.session.commit()

    return provisional_situations


# Funciones para la creacion de tablas de tutor


def list_tutors():
    """
    Función para listar los tutores.
    Atributos: Ninguno
    Retorna: Los tutores (list<Tutor>).
    """
    tutors = Tutor.query.all()
    return tutors


def create_tutor(**kwargs):
    """
    Función para crear un tutor. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Los atributos del tutor.
    Retorna: El tutor creado (Tutor).
    """
    tutorAux = Tutor(**kwargs)
    db.session.add(tutorAux)
    db.session.commit()
    return tutorAux


def commit_tutor(tutorAux):
    """
    Función para confirmar los cambios en un tutor en la base de datos.
    Atributos: tutorAux (Tutor) - El tutor.
    Retorna: El tutor (Tutor).
    """
    db.session.add(tutorAux)
    db.session.commit()
    return tutorAux

# Funciones para la creacion de tablas de propuesta_trabajo


def list_work_proposals():
    """
    Función para listar las propuestas de trabajo.
    Atributos: Ninguno
    Retorna: Las propuestas de trabajo (list<WorkProposal>).
    """
    propuesta_trabajo = WorkProposal.query.all()
    return propuesta_trabajo


def create_work_proposal(**kwargs):
    """
    Función para crear una propuesta de trabajo. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Los atributos de la propuesta de trabajo.
    Retorna: La propuesta de trabajo creada (WorkProposal).
    """
    propuesta_trabajo = WorkProposal(**kwargs)
    db.session.add(propuesta_trabajo)
    db.session.commit()
    return propuesta_trabajo


def create_provisional_work_proposal(**kwargs):
    """
    Función para crear una propuesta de trabajo.
    Atributos: kwargs (dict) - Los atributos de la propuesta de trabajo.
    Retorna: La propuesta de trabajo creada (WorkProposal).
    """
    propuesta_trabajo = WorkProposal(**kwargs)
    return propuesta_trabajo


def commit_work_proposal(propuesta_trabajo):
    """
    Función para confirmar los cambios en una propuesta de trabajo en la base de datos.
    Atributos: propuesta_trabajo (WorkProposal) - La propuesta de trabajo.
    Retorna: La propuesta de trabajo (WorkProposal).
    """
    db.session.add(propuesta_trabajo)
    db.session.commit()
    return propuesta_trabajo


def assign_fileJyA_work_proposal(work_proposal, fileJyA):
    """
    Función para asignar un legajo de JyA a una propuesta de trabajo.
    Atributos:
    - work_proposal (WorkProposal) - La propuesta de trabajo a asignar.
    - fileJyA (LegajoJyA) - El legajo de JyA a asignar.
    Retorna: La propuesta de trabajo (WorkProposal).
    """
    work_proposal.fileJyA = fileJyA
    db.session.add(work_proposal)
    db.session.commit()

    return work_proposal


def assign_teacher_or_teraphist_work_proposal(work_proposal, team_member):
    """
    Función para asignar un profesor o terapeuta a una propuesta de trabajo.
    Atributos:
    - work_proposal (WorkProposal) - La propuesta de trabajo a asignar.
    - team_member (TeamMember) - El miembro del equipo a asignar.
    Retorna: La propuesta de trabajo (WorkProposal).
    """
    work_proposal.teacher_or_therapist = TeamMember.query.get(team_member)
    db.session.add(work_proposal)
    db.session.commit()

    return work_proposal


def assign_horse_handler_work_proposal(work_proposal, team_member):
    """
    Función para asignar un cuidador de caballos a una propuesta de trabajo.
    Atributos:
    - work_proposal (WorkProposal) - La propuesta de trabajo a asignar.
    - team_member (TeamMember) - El miembro del equipo a asignar.
    Retorna: La propuesta de trabajo (WorkProposal).
    """
    work_proposal.horse_handler = TeamMember.query.get(team_member)
    db.session.add(work_proposal)
    db.session.commit()

    return work_proposal


def assign_track_assistant_work_proposal(work_proposal, team_member):
    """
    Función para asignar un asistente de pista a una propuesta de trabajo.
    Atributos:
    - work_proposal (WorkProposal) - La propuesta de trabajo a asignar.
    - team_member (TeamMember) - El miembro del equipo a asignar.
    Retorna: La propuesta de trabajo (WorkProposal).
    """
    work_proposal.track_assistant = TeamMember.query.get(team_member)
    db.session.add(work_proposal)
    db.session.commit()

    return work_proposal


def assign_equestrian_work_proposal(work_proposal, equestrian):
    """
    Función para asignar un jinete a una propuesta de trabajo.
    Atributos:
    - work_proposal (WorkProposal) - La propuesta de trabajo a asignar.
    - equestrian (Equestrian) - El jinete a asignar.
    Retorna: La propuesta de trabajo (WorkProposal).
    """
    work_proposal.equestrian = Equestrian.query.get(equestrian)
    db.session.add(work_proposal)
    db.session.commit()

    return work_proposal


def remove_teacher_or_teraphist_work_proposal(work_proposal):
    """
    Función para remover un profesor o terapeuta de una propuesta de trabajo.
    Atributos: work_proposal (WorkProposal) - La propuesta de trabajo.
    Retorna: None.
    """
    work_proposal.teacher_or_therapist = None


def remove_horse_handler_work_proposal(work_proposal):
    """
    Función para remover un cuidador de caballos de una propuesta de trabajo.
    Atributos: work_proposal (WorkProposal) - La propuesta de trabajo.
    Retorna: None.
    """
    work_proposal.horse_handler = None


def remove_track_assistant_work_proposal(work_proposal):
    """
    Función para remover un asistente de pista de una propuesta de trabajo.
    Atributos: work_proposal (WorkProposal) - La propuesta de trabajo.
    Retorna: None.
    """
    work_proposal.track_assistant = None


def remove_equestrian_work_proposal(work_proposal):
    """
    Función para remover un jinete de una propuesta de trabajo.
    Atributos: work_proposal (WorkProposal) - La propuesta de trabajo.
    Retorna: None.
    """
    work_proposal.equestrian = None


# Funciones para la creacion de tablas de ecuestre, y miscalenas
def list_equestrians():
    """
    Función para listar los ecuestres.
    Atributos: Ninguno
    Retorna: Los ecuestres (list<Equestrian>).
    """
    ecuestre = Equestrian.query.filter(Equestrian.deleted == False).all()
    return ecuestre


def create_equestrian(**kwargs):
    """
    Función para crear un ecuestre. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Los atributos del ecuestre.
    Retorna: El ecuestre creado (Equestrian).
    """
    ecuestre = Equestrian(**kwargs)
    db.session.add(ecuestre)
    db.session.commit()
    return ecuestre


def create_provisional_ecuestrian(**kwargs):
    """
    Función para crear un ecuestre provisional.
    Atributos: kwargs (dict) - Los atributos del ecuestre.
    Retorna: El ecuestre creado (Equestrian).
    """
    return Equestrian(**kwargs)


def assign_jya_type_to_equestrian(equestrian, jya_types):
    """
    Función para asociar un ecuestre con el/los tipo(s) de JyA especificado(s).
    Atributos:
    - equestrian (Equestrian) - El ecuestre a asociar.
    - jya_types (list<JyaType>) - Lista de tipos de JyA a asociar.
    Retorna: None.
    """
    for jya_type_id in jya_types:
        jya_type_obj = JyaType.query.get(jya_type_id)
        if jya_type_obj:
            equestrian.jya_type.append(jya_type_obj)


def remove_all_jya_type_from_equestrian(equestrian):
    """
    Función para remover todos los tipos de JyA de un ecuestre.
    Atributos: equestrian (Equestrian) - El ecuestre.
    Retorna: None.
    """
    equestrian.jya_type.clear()


def assign_team_member_to_equestrian(equestrian, team_member):
    """
    Función para asociar un ecuestre con el/los miembro(s) de equipo especificado(s).
    Atributos:
    - equestrian (Equestrian) - El ecuestre a asociar.
    - team_member (list<TeamMember>) - Lista de miembros de equipo a asociar.
    Retorna: None.
    """
    for team_member_id in team_member:
        team_member_obj = TeamMember.query.get(team_member_id)
        if team_member_obj:
            equestrian.team_member.append(team_member_obj)


def remove_all_team_member_from_equestrian(equestrian):
    """
    Función para remover todos los miembros de equipo de un ecuestre.
    Atributos: equestrian (Equestrian) - El ecuestre.
    Retorna: None.
    """
    equestrian.team_member.clear()


def commit_equestrian(equestrian):
    """
    Función para confirmar los cambios en un ecuestre en la base de datos.
    Atributos: equestrian (Equestrian) - El ecuestre.
    Retorna: El ecuestre (Equestrian).
    """
    db.session.add(equestrian)
    db.session.commit()
    return equestrian


def search_equestrians(name_filter, jya_filter, search_string):
    """
    Función para buscar ecuestres en la base de datos.
    Atributos:
    - name_filter (string) - Filtro por nombre.
    - jya_filter (string) - Filtro por tipo de JyA.
    - search_string (string) - Cadena de búsqueda.
    Retorna: Los ecuestres (list<Equestrain>).
    """
    # Base query
    query = Equestrian.query

    # Add search query condition
    if search_string:
        search_string = f"{search_string.strip()}"
        if name_filter:
            query = query.filter(
                Equestrian.name.ilike(f"%{search_string}%"))
        elif jya_filter:
            query = query.join(Equestrian.jya_type).filter(
                JyaType.name.ilike(f"%{search_string}%")
            )

    # Execute the query
    results = query.filter(Equestrian.deleted == False).all()

    return results


def get_equestrian_by_id(equestrian_id):
    """
    Función para obtener un ecuestre por su ID.
    Atributos: equestrian_id (int) - ID del ecuestre.
    Retorna: El ecuestre (Equestrian) o None.
    """
    equestrian = Equestrian.query.get(equestrian_id)
    return equestrian


def delete_equestrian(equestrian):
    """
    Función para eliminar un ecuestre fisicamente. No se debe usar.
    Atributos: equestrian (Equestrian) - El ecuestre.
    Retorna: None.
    """
    db.session.delete(equestrian)
    db.session.commit()


# Funciones para la creacion de tablas de tipo_documento_ecuestre


def list_typedoc_equestrians():
    """
    Función para listar los tipos de documento ecuestre.
    Atributos: Ninguno
    Retorna: Los tipos de documento ecuestre (list<TypedocEquestrian>).
    """
    tipo_documento_ecuestre = typedoc_equestrian.query.all()
    return tipo_documento_ecuestre


def create_typedoc_equestrian(**kwargs):
    """
    Función para crear un tipo de documento ecuestre. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Los atributos del tipo de documento ecuestre.
    Retorna: El tipo de documento ecuestre creado (TypedocEquestrian).
    """
    tipo_documento_ecuestre = typedoc_equestrian(**kwargs)
    db.session.add(tipo_documento_ecuestre)
    db.session.commit()
    return tipo_documento_ecuestre


# Funciones para la creacion de tablas de jya_tipo


def list_jya_types():
    """
    Función para listar los tipos de JyA.
    Atributos: Ninguno
    Retorna: Los tipos de JyA (list<JyaType>).
    """
    jya_tipo = JyaType.query.all()
    return jya_tipo


def create_jya_type(**kwargs):
    """
    Función para crear un tipo de JyA. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Los atributos del tipo de JyA.
    Retorna: El tipo de JyA creado (JyaType).
    """
    jya_tipo = JyaType(**kwargs)
    db.session.add(jya_tipo)
    db.session.commit()
    return jya_tipo


# Funciones para la creacion de tablas de tipo_documento_legajoJyA


def list_typedoc_fileJyA():
    """
    Función para listar los tipos de documento de legajo JyA.
    Atributos: Ninguno
    Retorna: Los tipos de documento de legajo JyA (list<TypedocFileJyA>).
    """
    tipo_documento_legajoJyA = TypeDocFileJyA.query.all()
    return tipo_documento_legajoJyA


def create_typedoc_legajoJyA(**kwargs):
    """
    Función para crear un tipo de documento de legajo JyA. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Los atributos del tipo de documento de legajo JyA.
    Retorna: El tipo de documento de legajo JyA creado (TypedocFileJyA).
    """
    tipo_documento_legajoJyA = TypeDocFileJyA(**kwargs)
    db.session.add(tipo_documento_legajoJyA)
    db.session.commit()
    return tipo_documento_legajoJyA


# Funciones para la creacion de tablas de situacion_escolar


def list_school_situations():
    """
    Función para listar las situaciones escolares.
    Atributos: Ninguno
    Retorna: Las situaciones escolares (list<SchoolSituation>).
    """
    situacion_escolar = SchoolSituation.query.all()
    return situacion_escolar


def create_school_situation(**kwargs):
    """
    Función para crear una situación escolar. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Los atributos de la situación escolar.
    Retorna: La situación escolar creada (SchoolSituation).
    """
    situacion_escolar = SchoolSituation(**kwargs)
    db.session.add(situacion_escolar)
    db.session.commit()
    return situacion_escolar


def commit_school_situation(situacion_escolar):
    """
    Función para confirmar los cambios en una situación escolar en la base de datos.
    Atributos: situacion_escolar (SchoolSituation) - La situación escolar.
    Retorna: La situación escolar (SchoolSituation).
    """
    db.session.add(situacion_escolar)
    db.session.commit()
    return situacion_escolar


def create_provisional_school_situation(**kwargs):
    """
    Función para crear una situación escolar.
    Atributos: kwargs (dict) - Los atributos de la situación escolar.
    Retorna: La situación escolar creada (SchoolSituation).
    """
    situacion_escolar = SchoolSituation(**kwargs)
    return situacion_escolar


def assign_fileJyA_school_situation(school_situacion, fileJyA):
    """
    Función para asignar un legajo de JyA a una situación escolar.
    Atributos:
    - school_situacion (SchoolSituation) - La situación escolar a asignar.
    - fileJyA (LegajoJyA) - El legajo de JyA a asignar.
    Retorna: La situación escolar (SchoolSituation).
    """
    school_situacion.fileJyA = fileJyA
    db.session.add(school_situacion)
    db.session.commit()

    return school_situacion


# Funciones para la relacion ecuestre, miembro de equipo


def assign_equestrian_team_member(ecuestre, team_member, tipo_team_member):
    """
    Función para asignar un miembro del equipo a un ecuestre.
    Atributos:
    - ecuestre (Equestrian) - El ecuestre a asignar.
    - team_member (TeamMember) - El miembro del equipo a asignar.
    - tipo_team_member (str) - El tipo de miembro del equipo.
    Retorna: La relación (EquestrianTeamMember).
    """
    relationship = EquestrianTeamMember(
        ecuestre_id=ecuestre.id,
        team_member_id=team_member.id,
        type_team_member=tipo_team_member,
    )
    db.session.add(relationship)
    db.session.commit()
    return relationship


# Funciones para la relacion ecuestre, tipo de jya


def assign_equestrian_team_member(ecuestre, jya_tipos):
    """
    Función para asignar un tipo de JyA a un ecuestre.
    Atributos:
    - ecuestre (Equestrian) - El ecuestre a asignar.
    - jya_tipos (JyaType) - El tipo de JyA a asignar.
    Retorna: La relación (EquestrianJyAType).
    """
    relationship = EquestrianJyAType(
        ecuestre_id=ecuestre.id, jya_tipos_id=jya_tipos.id)
    db.session.add(relationship)
    db.session.commit()
    return relationship

# Funciones para la creacion de tablas Consulta


def list_consultations(seek_deleted=False):
    """
    Función para listar las consultas.
    Atributos: Ninguno
    Retorna: Las consultas (list<Consultation>).
    """
    if (seek_deleted):
        consultas = Consultation.query.all()
    else:
        consultas = Consultation.query.filter(
            Consultation.deleted == False).all()
    return consultas


def create_consultation(**kwargs):
    """
    Función para crear una consulta. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Los atributos de la consulta.
    Retorna: La consulta creada (Consultation).
    """
    consulta = Consultation(**kwargs)
    db.session.add(consulta)
    db.session.commit()
    return consulta


def commit_consultation(consulta):
    """
    Función para confirmar los cambios en una consulta en la base de datos.
    Atributos: consulta (Consultation) - La consulta.
    Retorna: La consulta (Consultation).
    """
    db.session.add(consulta)
    db.session.commit()
    return consulta


def create_provisional_consultation(**kwargs):
    """
    Función para crear una consulta.
    Atributos: kwargs (dict) - Los atributos de la consulta.
    Retorna: La consulta creada (Consultation).
    """
    consulta = Consultation(**kwargs)
    return consulta


def truncate_message(message, length=10):
    """
    Función para truncar un mensaje a una longitud máxima.
    Atributos: 
    - message (str) - Mensaje a truncar.
    - length (int, default=50) - Longitud máxima.
    Retorna: Mensaje truncado (str).
    """
    if len(message) > length:
        return message[:length] + '...'
    return message


def search_consultations(search_string, status_pending_filter, status_in_progress_filter, status_discarded_filter, status_solved):
    """
    Función para buscar consultas en la base de datos.
    Atributos:
    - search_string (string) - Cadena de búsqueda.
    - status_pending_filter (bool) - Filtro por estado pendiente.
    - status_in_progress_filter (bool) - Filtro por estado en progreso.
    - status_discarded_filter (bool) - Filtro por estado descartado.
    - status_solved (bool) - Filtro por estado resuelto.
    Retorna: Las consultas (list<Consultation>).
    """
    query = Consultation.query

    if search_string:
        search_string = f"{search_string.strip()}"
        query = query.filter(
            Consultation.full_name.ilike(f"%{search_string}%")
        )

    if status_pending_filter:
        query = query.filter(Consultation.status == 'Pendiente')
    if status_in_progress_filter:
        query = query.filter(Consultation.status == 'En progreso')
    if status_discarded_filter:
        query = query.filter(Consultation.status == 'Descartado')
    if status_solved:
        query = query.filter(Consultation.status == 'Resuelto')

    results = query.filter(Consultation.deleted == False).all()

    return results


def get_consultation_by_id(consulta_id):
    """
    Función para obtener una consulta por su ID.
    Atributos: consulta_id (int) - ID de la consulta.
    Retorna: La consulta (Consultation) o None.
    """
    consulta = Consultation.query.filter_by(
        id=consulta_id, deleted=False).first()
    return consulta


def create_provisional_consultation(**kwargs):
    """
    Función para crear una consulta.
    Atributos: kwargs (dict) - Los atributos de la consulta.
    Retorna: La consulta creada (Consultation).
    """
    consulta = Consultation(**kwargs)
    return consulta


def commit_consultation(consulta):
    """
    Función para confirmar los cambios en una consulta en la base de datos.
    Atributos: consulta (Consultation) - La consulta.
    Retorna: La consulta (Consultation).
    """
    db.session.add(consulta)
    db.session.commit()
    return consulta

# Funciones para la entidad ContentPost


def get_content_post_by_id(content_post_id):
    """
    Función para obtener un contenido por su ID.
    Atributos: content_post_id (int) - ID del contenido.
    Retorna: El contenido (ContentPost) o None.
    """
    content_post = ContentPost.query.get(content_post_id)
    return content_post

def list_content_post():
    """
    Función para listar los contenidos.
    Atributos: Ninguno
    Retorna: Los contenidos (list<ContentPost>).
    """
    content_post = ContentPost.query.all()
    return content_post

def get_paginated_contents(page=1, per_page=10, filters=None):
    """
    Función para obtener una lista paginada de contenidos publicados.

    Atributos:
    - page (int): Número de página para la paginación. Valor por defecto: 1.
    - per_page (int): Número de elementos por página. Valor por defecto: 10.
    - filters (dict): Diccionario con los filtros aplicables. 
      Puede incluir:
        - 'start_date' (datetime): Fecha mínima de publicación de los contenidos.
        - 'end_date' (datetime): Fecha máxima de publicación de los contenidos.
        - 'author' (str): alias del autor a buscar.

    Retorna:
    - contents (list): Lista de objetos `ContentPost` que cumplen con los filtros y la paginación.
    - total (int): Número total de contenidos que cumplen los filtros (sin paginación).
    """
    query = ContentPost.query.filter_by(deleted=False)
    if filters:
        if 'start_date' in filters:
            query = query.filter(ContentPost.created_at >= filters['start_date'])
        if 'end_date' in filters:
            query = query.filter(ContentPost.created_at <= filters['end_date'])
        if 'author' in filters:
            query = query.join(User).filter(User.alias.ilike(f"%{filters['author']}%"))

    
    total = query.with_entities(
        func.count()).scalar() 

    contents = query.order_by(ContentPost.created_at.desc()) \
                    .offset((page - 1) * per_page) \
                    .limit(per_page) \
                    .all()
    return contents, total

def create_content_post(**kwargs):
    """
    Función para crear un contenido. Usado al levantar la DB, o al cargar información.
    Atributos: kwargs (dict) - Los atributos del tipo del contenido.
    Retorna: El contenido creado (ContentPost).
    """
    content_post = ContentPost(**kwargs)
    db.session.add(content_post)
    db.session.commit()
    return content_post


def create_provisional_content_post(**kwargs):
    """
    Función para crear un contenido provisional.
    Atributos: kwargs (dict) - Diccionario con los atributos del contenido.
    Retorna: Contenido (ContentPost).
    """
    return ContentPost(**kwargs)


def assign_author_content_post(content_post, user):
    """
    Función para asignar un author a un contenido.
    Atributos:
    - content_post (ContentPost) - Contenido al que asignar el usuario.
    - user (User) - usuario a asignar.
    Retorna: Usuario (User).
    """
    content_post.author = user
    db.session.add(content_post)
    db.session.commit()

    return user


def add_content_post(content_post_form, author_email):
    """ 
    Función para agregar un contenido a partir de un formulario.
    Atributos:
    - contenttForm (Form) - Formulario con los datos del contenido.
    - author (User) - Autor a asignar.
    Retorna: ContentPost (ContentPost).
    """
    title = content_post_form.title.data
    summary = content_post_form.summary.data
    content = content_post_form.content.data

    author = get_user_by_email(author_email)

    content_post = create_provisional_content_post(
        title=title, summary=summary, content=content)

    assign_author_content_post(content_post, author)

    return commit_receipt(content_post)


def filter_content_post(content_post, title=None, author_alias=None):
    """
    Función para filtrar contenidos a partir de filtros.
    Atributos:
    - content_post (query) - Query de los contenidos.
    - author_alias (str, default='None') - alias del autor.
    Retorna: Lista de contenidos (list<ContentPost>).
    """
    content_post = content_post.filter_by(deleted=False)
    if author_alias:
        content_post = content_post.join(ContentPost.author).filter(func.lower(
            User.alias).startswith(author_alias.lower()))
    if title:
        content_post = content_post.filter(func.lower(
            ContentPost.title).startswith(title.lower()))

    return content_post


def order_content_post(query, order_by_date="asc"):
    """
    Función para ordenar los contenidos.
    Atributos:
    - query (query) - Query de los contenidos.
    - order_by_date (str, default='asc') - Orden de los contenidos.
    Retorna: Lista de contenidos (list<ContentPost>).
    """
    if order_by_date == "desc":
        return query.order_by(desc(ContentPost.created_at))
    else:
        return query.order_by(asc(ContentPost.created_at))


def search_content_post(title=None, author_alias=None):
    """
    Función para buscar contenidos a partir de filtros.
    Atributos:
    - author_alias (str, default='None') - Alias del autor
    - title (str, default='None') - Método de pago.
    Retorna: Lista de contenidos (list<ContentPost>).
    """
    query = ContentPost.query.options(joinedload(ContentPost.author))

    # Aplicar filtros
    query = filter_content_post(
        query, title, author_alias)

    return query


def modify_content_post(oldContentPost, newContentPostForm):
    """
    Función para modificar un contenido a partir de un formulario.
    Atributos:
    - oldContentPost (int) - ID del contenido a modificar.
    - newContentPostForm (Form) - Formulario con los nuevos datos del conyenido.
    Retorna: None.
    """
    databaseContentPost = get_content_post_by_id(oldContentPost)

    databaseContentPost.title = newContentPostForm.title.data
    databaseContentPost.summary = newContentPostForm.summary.data
    databaseContentPost.content = newContentPostForm.content.data
    # databaseContentPost.status = newContentPostForm.status.data

    return commit_receipt(databaseContentPost)


def publish_content_post(contentPost, actufecha):
    """
    Función para modificar el estado de un contenido a publicado.
    Atributos:
    - contentPost (ContentPost) - Icontenido a modificar.
    Retorna: None.
    """

    contentPost.status = "Publicado"

    if (actufecha):
        contentPost.published_at = datetime.now()

    return commit_receipt(contentPost)


def store_content_post(contentPost):
    """
    Función para modificar el estado de un contenido a archivado.
    Atributos:
    - contentPost (ContentPost) - contenido a modificar.
    Retorna: None.
    """

    contentPost.status = "Archivado"

    return commit_receipt(contentPost)

####


def count_scholarships_jya():
    """
    Función para contar qué JYA están becados o no.
    Atributos: Ninguno
    Retorna: El número de becas de JyA (int).
    """
    jya = list_legajosJyA()
    has_scholarship = 0
    no_scholarship = 0
    for j in jya:
        if j.scholarship:
            has_scholarship += 1
        else:
            no_scholarship += 1
    return has_scholarship, no_scholarship
