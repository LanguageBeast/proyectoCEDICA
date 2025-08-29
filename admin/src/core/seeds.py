from src.core import entities
from datetime import datetime
import random


def run():
    """
    Función que corre todas las funciones de seed
    Atributos: Ninguno
    Retorna: None
    """
    role_system_admin = entities.create_role(name="Administrador del sistema")
    role_administration = entities.create_role(name="Administrativo")
    role_equestrian = entities.create_role(name="Ecuestre")
    role_technical = entities.create_role(name="Técnico")
    role_volunteer = entities.create_role(name="Voluntariado")
    role_unassigned = entities.create_role(name="No asignado")

    permission_accept = entities.create_permission(name="accept")

    permission_content_index = entities.create_permission(name="content_index")
    permission_content_new = entities.create_permission(name="content_new")
    permission_content_destroy = entities.create_permission(
        name="content_destroy")
    permission_content_update = entities.create_permission(
        name="content_update")
    permission_content_show = entities.create_permission(name="content_show")

    permission_users_index = entities.create_permission(name="users_index")
    permission_users_new = entities.create_permission(name="users_new")
    permission_users_destroy = entities.create_permission(name="users_destroy")
    permission_users_update = entities.create_permission(name="users_update")
    permission_users_show = entities.create_permission(name="users_show")

    permission_equestrian_index = entities.create_permission(
        name="equestrian_index")
    permission_equestrian_new = entities.create_permission(
        name="equestrian_new")
    permission_equestrian_destroy = entities.create_permission(
        name="equestrian_destroy")
    permission_equestrian_update = entities.create_permission(
        name="equestrian_update")
    permission_equestrian_show = entities.create_permission(
        name="equestrian_show")

    permission_team_member_index = entities.create_permission(
        name="team_member_index")
    permission_team_member_new = entities.create_permission(
        name="team_member_new")
    permission_team_member_destroy = entities.create_permission(
        name="team_member_destroy")
    permission_team_member_update = entities.create_permission(
        name="team_member_update")
    permission_team_member_show = entities.create_permission(
        name="team_member_show")

    permission_jya_index = entities.create_permission(name="jya_index")
    permission_jya_new = entities.create_permission(name="jya_new")
    permission_jya_destroy = entities.create_permission(name="jya_destroy")
    permission_jya_update = entities.create_permission(name="jya_update")
    permission_jya_show = entities.create_permission(name="jya_show")

    permission_receipt_index = entities.create_permission(name="receipt_index")
    permission_receipt_new = entities.create_permission(name="receipt_new")
    permission_receipt_destroy = entities.create_permission(
        name="receipt_destroy")
    permission_receipt_update = entities.create_permission(
        name="receipt_update")
    permission_receipt_show = entities.create_permission(name="receipt_show")

    permission_payment_index = entities.create_permission(name="payment_index")
    permission_payment_new = entities.create_permission(name="payment_new")
    permission_payment_destroy = entities.create_permission(
        name="payment_destroy")
    permission_payment_update = entities.create_permission(
        name="payment_update")
    permission_payment_show = entities.create_permission(name="payment_show")

    permission_consultation_index = entities.create_permission(
        name="consultation_index")
    permission_consultation_new = entities.create_permission(
        name="consultation_new")  # no se usa
    permission_consultation_destroy = entities.create_permission(
        name="consultation_destroy")
    permission_consultation_update = entities.create_permission(
        name="consultation_update")
    permission_consultation_show = entities.create_permission(
        name="consultation_show")

    permission_reports_index = entities.create_permission(name="report_index")
    permission_reports_show = entities.create_permission(name="report_show")

    role_unassigned = entities.assign_permissions(role_unassigned, [])

    role_administration = entities.assign_permissions(role_administration, [permission_team_member_show, permission_team_member_update, permission_team_member_destroy, permission_team_member_index, permission_team_member_new, permission_payment_show, permission_payment_update, permission_payment_destroy, permission_payment_index,
                                                      permission_payment_new, permission_jya_show, permission_jya_destroy, permission_jya_index, permission_jya_new, permission_jya_update, permission_receipt_show, permission_receipt_destroy, permission_receipt_index, permission_receipt_new, permission_receipt_update, permission_equestrian_index, permission_equestrian_show, permission_content_index, permission_content_new, permission_content_show, permission_content_update,
                                                      permission_consultation_index, permission_consultation_show, permission_consultation_destroy, permission_consultation_update, permission_consultation_new, permission_reports_index, permission_reports_show, permission_accept])
    role_equestrian = entities.assign_permissions(role_equestrian, [permission_equestrian_show, permission_equestrian_destroy,
                                                  permission_equestrian_index, permission_equestrian_new, permission_equestrian_update, permission_jya_index, permission_jya_show])
    role_system_admin = entities.assign_permissions(role_system_admin, [permission_equestrian_new, permission_equestrian_update, permission_equestrian_destroy, permission_team_member_show, permission_team_member_update, permission_team_member_destroy, permission_team_member_index, permission_team_member_new, permission_payment_show, permission_payment_update, permission_payment_destroy, permission_payment_index, permission_payment_new,
                                                    permission_jya_show, permission_jya_destroy, permission_jya_index, permission_jya_new, permission_jya_update, permission_receipt_show, permission_receipt_destroy, permission_receipt_index, permission_receipt_new, permission_receipt_update, permission_equestrian_index, permission_equestrian_show, permission_users_index, permission_users_destroy, permission_users_new, permission_users_show, permission_users_update, permission_content_index, permission_content_new, permission_content_destroy, permission_content_show, permission_content_update, permission_consultation_index, permission_consultation_show, permission_consultation_destroy, permission_consultation_update, permission_consultation_new, permission_reports_index, permission_reports_show,
                                                    permission_accept])
    role_technical = entities.assign_permissions(role_technical, [permission_receipt_index, permission_receipt_show, permission_equestrian_index,
                                                 permission_equestrian_show, permission_jya_show, permission_jya_destroy, permission_jya_index, permission_jya_new, permission_jya_update, permission_reports_index, permission_reports_show])
    # no se define bien qué permisos tiene volunteer, solo podrá entrar a los index de los módulos
    role_volunteer = entities.assign_permissions(role_volunteer, [
                                                 permission_equestrian_index, permission_team_member_index, permission_jya_index, permission_receipt_index, permission_payment_index])
    user1 = entities.create_user(
        email="juan_perez@hotmail.com",
        alias="juan123",
        password="pincha",
        dni="42546743"
    )
    entities.assign_role(user1, role_system_admin)

    pago_tipo_honorario = entities.create_payment_type(name="Honorarios")
    pago_tipo_proveedor = entities.create_payment_type(name="Proveedor")
    pago_tipo_gastos_varios = entities.create_payment_type(
        name="Gastos varios")

    pago1 = entities.create_payment(
        amount=485000, payment_date=datetime(2024, 10, 1), description="Pago de sueldo de Juan"
    )
    pago2 = entities.create_payment(
        amount=85000, payment_date=datetime(2024, 10, 2), description="Gastos varios"
    )
    pago3 = entities.create_payment(
        amount=250500, payment_date=datetime(2024, 10, 3), description="Pago de proveedor"
    )

    entities.assign_payment_type(pago1, pago_tipo_honorario)
    entities.assign_payment_type(pago2, pago_tipo_gastos_varios)
    entities.assign_payment_type(pago3, pago_tipo_proveedor)

    user2 = entities.create_user(
        email="jorge_perez@hotmail.com",
        alias="jorge",
        password="pincha",
        dni="42546763"
    )
    entities.assign_role(user2, role_technical)

    user3 = entities.create_user(
        email="mateo_perez@hotmail.com",
        alias="juan",
        password="pincha",
        dni="42536743"
    )
    entities.assign_role(user3, role_administration)

    user4 = entities.create_user(
        email="carla_perez@hotmail.com",
        alias="juan1",
        password="pincha",
        dni="23432321"
    )
    entities.assign_role(user4, role_equestrian)

    cons1 = entities.create_consultation(
        full_name="Juan Peralta",
        email="jperalta@correo.com",
        message="Hola, quería saber si tienen disponibilidad para una reunión virtual",
        captcha="123456",
    )

    cons2 = entities.create_consultation(
        full_name="Pedro González",
        email="gonzalezp@correo.com",
        message="Quisiera conocer más sobre el programa de equinoterapia",
        captcha="123456",
    )


def build_jya_types():
    # Hardcodear los tipos de Jinetes y Amazonas
    jya_type1 = entities.create_jya_type(name="Hipoterapia")
    jya_type2 = entities.create_jya_type(name="Monta Terapéutica")
    jya_type2 = entities.create_jya_type(name="Deporte Ecuestre Adaptado")
    jya_type2 = entities.create_jya_type(name="Actividades Recreativas")
    jya_type2 = entities.create_jya_type(name="Equitación")


def build_doc_jya_types():
    # Hardcodear los tipos de Jinetes y Amazonas
    doc_jya1 = entities.create_typedoc_legajoJyA(name="Entrevista")
    doc_jya2 = entities.create_typedoc_legajoJyA(name="Evaluación")
    doc_jya3 = entities.create_typedoc_legajoJyA(name="Planificación")
    doc_jya4 = entities.create_typedoc_legajoJyA(name="Evolución")
    doc_jya5 = entities.create_typedoc_legajoJyA(name="Crónicas")
    doc_jya6 = entities.create_typedoc_legajoJyA(name="Documental")


def build_two_employees():
    # Hardcodear dos empleados
    employee1 = entities.create_team_member(
        first_name="Carlos",
        last_name="Gomez",
        dni="12345678",
        address="123 Main St",
        email="carlos.gomez@example.com",
        location="Buenos Aires",
        phone="1234567890",
        profession="Therapist",
        job_position="Domador",
        start_date=datetime(2020, 1, 1),
        end_date=None,
        emergency_contact_name="Maria Gomez",
        emergency_contact_phone="0987654321",
        health_insurance="HP123456",
        condition="Voluntary",
        active=True,
        created_at=datetime.now().date()
    )

    employee2 = entities.create_team_member(
        first_name="Ana",
        last_name="Martinez",
        dni="87654321",
        address="456 Elm St",
        email="ana.martinez@example.com",
        location="Rosario",
        phone="3216540987",
        profession="Instructor",
        job_position="Domador",
        start_date=datetime(2021, 6, 15),
        end_date=None,
        emergency_contact_name="Juan Martinez",
        emergency_contact_phone="5678901234",
        health_insurance="MC654321",
        condition="Voluntary",
        active=True,
        created_at=datetime.now()
    )

    employee3 = entities.create_team_member(
        first_name="Ana",
        last_name="Rodriguez",
        dni="12345688",
        address="123 Main St",
        email="rodriguez@example.com",
        location="Buenos Aires",
        phone="1234567877",
        profession="Terapista ocupacional",
        job_position="terapeuta",
        start_date=datetime(2020, 1, 1),
        end_date=None,
        emergency_contact_name="Maria Gomez",
        emergency_contact_phone="0987654321",
        health_insurance="HP123456",
        condition="Voluntary",
        active=True,
        created_at=datetime.now()
    )

    employee4 = entities.create_team_member(
        first_name="Maria",
        last_name="Dominguez",
        dni="87654355",
        address="456 Elm St",
        email="maria@example.com",
        location="Rosario",
        phone="3216540987",
        profession="Docente",
        job_position="profesor de equitacion",
        start_date=datetime(2021, 6, 15),
        end_date=None,
        emergency_contact_name="Juan Martinez",
        emergency_contact_phone="5678901234",
        health_insurance="MC654321",
        condition="Voluntary",
        active=True,
        created_at=datetime.now()

    )
    # Listas de profesiones y puestos
    professions = [
        "Psicólogo/a", "Psicomotricista", "Médico/a", "Kinesiólogo/a",
        "Terapista Ocupacional", "Psicopedagogo/a", "Docente", "Profesor",
        "Fonoaudiólogo/a", "Veterinario/a", "Otro"
    ]

    job_positions = [
        "Administrativo/a", "Terapeuta", "Conductor", "Auxiliar de pista",
        "Herrero", "Veterinario", "Entrenador de Caballos", "Domador",
        "Profesor de Equitación", "Docente de Capacitación", "Auxiliar de mantenimiento", "Otro"
    ]
def build_contents():
    """
    Función para crear 5 contenidos de ejemplo en la base de datos.

    """
    user1 = entities.create_user(
        email="carla_martinez@hotmail.com",
        alias="carla martinez",
        password="password1",
        dni="13213563"
    )
    user2 = entities.create_user(
        email="lupe_hernandez@hotmail.com",
        alias="lupe hernandez",
        password="password2",
        dni="13213569"
    )
    content1= entities.create_content_post(
        title= "Clínica de primeros auxilios y prevención para caballos",
        summary= "Aprende técnicas esenciales para el cuidado y emergencia de caballos.",
        content= (
            "En esta clínica se enseñarán técnicas esenciales para actuar en situaciones de emergencia con caballos. "
            "Aprenderás a identificar signos de enfermedad, lesiones o comportamientos atípicos que puedan indicar un problema de salud. "
            "Además, se abordarán estrategias preventivas, como la revisión diaria de los animales, la importancia de una correcta alimentación, "
            "el mantenimiento de los cascos y cómo garantizar un entorno seguro en establos y áreas de trabajo. También se realizarán simulaciones "
            "prácticas, desde cómo aplicar vendajes hasta la estabilización del caballo en casos de trauma, siempre con énfasis en la seguridad del propietario y del animal."
        ),
        author_id= user1.id,
        status= "Publicado",
        published_at= datetime(2023, 10, 1, 10, 0, 0)
    )
    content2=entities.create_content_post(
        title= "Importancia del posicionamiento del paciente durante la monta gemela",
        summary="Exploramos cómo el correcto posicionamiento mejora la terapia ecuestre.",
        content= (
            "La monta gemela es una técnica común en terapias ecuestres que implica la presencia de un terapeuta o asistente montando junto al paciente. "
            "Este artículo detalla cómo el correcto posicionamiento del paciente influye en su seguridad, comodidad y en los beneficios de la terapia. "
            "Se explorarán las diferentes posturas dependiendo de las necesidades físicas y emocionales del paciente, así como la influencia que estas tienen en la biomecánica del caballo. "
            "Además, se analizan casos prácticos para garantizar un equilibrio entre el bienestar del equino y la efectividad de la intervención terapéutica."
        ),
        author_id= user2.id,
        status= "Publicado",
        published_at= datetime(2023, 10, 5, 14, 30, 0)
    )
    content3= entities.create_content_post(
        title= "Teoría polivagal aplicada a caballos",
        summary= "Descubre cómo los caballos ayudan en la regulación emocional humana.",
        content= (
            "La teoría polivagal, desarrollada por Stephen Porges, se centra en cómo el sistema nervioso responde al estrés y a la conexión social. "
            "Este artículo explica cómo los caballos, con su sensibilidad innata, pueden actuar como reguladores emocionales para los humanos. "
            "A través de la interacción con estos animales, las personas experimentan una disminución en los niveles de estrés y ansiedad, favoreciendo un estado de calma y seguridad. "
            "Se incluyen estudios de casos sobre cómo esta teoría se ha integrado en programas terapéuticos, mejorando la comunicación y la empatía entre pacientes y caballos."
        ),
        author_id= user1.id,
        status= "Publicado",
        published_at= datetime(2023, 10, 8, 9, 0, 0)
    )
    content4=entities.create_content_post(
        title= "Concurso ecuestre integrado",
        summary= "Un evento ecuestre inclusivo para jinetes con y sin discapacidades.",
        content= (
            "Este evento ecuestre único busca fomentar la inclusión, permitiendo que jinetes con y sin discapacidades participen juntos en competencias diseñadas para promover la equidad. "
            "A lo largo del concurso, se desarrollan pruebas adaptadas que destacan habilidades como la precisión, el trabajo en equipo y la conexión con los caballos. "
            "Más que una competencia, es un espacio para celebrar la diversidad y demostrar cómo el deporte ecuestre puede ser un medio de integración social. "
            "Historias de participantes en ediciones anteriores inspiran a la comunidad a seguir construyendo espacios inclusivos."
        ),
        author_id= user2.id,
        status= "Borrador",
        published_at= datetime(2023, 10, 12, 15, 45, 0)
    )
    content5=entities.create_content_post(
        title= "Beneficios de la terapia ecuestre",
        summary= "Exploramos cómo las interacciones con caballos mejoran la salud física y emocional.",
        content= (
            "La terapia asistida con caballos es una práctica ampliamente reconocida por sus beneficios físicos, emocionales y sociales. "
            "Este artículo detalla cómo las interacciones con caballos pueden mejorar habilidades motoras, estimular la comunicación y reforzar la autoestima en personas con discapacidades o trastornos emocionales. "
            "Además, se analizan estudios que demuestran cómo el movimiento rítmico del caballo simula el patrón de marcha humano, favoreciendo la rehabilitación física. "
            "También se incluye información sobre el impacto emocional, como la construcción de confianza y la reducción de la ansiedad en pacientes que participan regularmente en estas actividades."
        ),
        author_id= user1.id,
        status= "Archivado",
        published_at= datetime(2023, 10, 15, 11, 0, 0)
    )
