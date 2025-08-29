from os import fstat
from flask import Blueprint, render_template, flash, redirect, url_for, request, session, current_app
from src.web.handlers.auth import check, login_required
from src.core.entities import (legajo_jya_exists_by_dni, list_equestrians, query_legajosJyA,order_legajosJyA, search_legajos, get_legajoJyA_by_id, logical_delete, filejya_has_receipts, list_miembros_equipo_not_eliminated, modify_status_receipts_legajoJyA, modify_filejya, add_fileJyA, addDocumentLegajo, addLinkLegajo, list_typedoc_fileJyA, get_document_by_id, delete_document, updateDocumentLegajo)
from src.web.forms import FileJyAForm
import re
from src.core.validators import validate_documents, validate_link
import time
from werkzeug.utils import secure_filename


# Blueprint para las funcionalidades del modulo jinetes y amazonas


# Variables globales para la paginación
queryResult = []
total_pages = 0
per_page = 25

# Se crea un blueprint para el módulo de jinetes y amazonas
jya_bp = Blueprint('module_jya', __name__,
                   url_prefix="/modulo_jinetesyamazonas")


@jya_bp.get('/')
@check("jya_index")
def jya():
    """
    Función que renderiza la vista principal del módulo de jinetes y amazonas.
    Decoradores:
        - @check("jya_index"): verifica que el usuario tenga permisos para acceder a la vista.
        - @login_required: verifica que el usuario haya iniciado sesión.
    Argumentos: Ninguno.
    Retorna:
        - render_template("module_jya.html", current_page='jya'): 
        renderiza la vista principal del módulo de jinetes y amazonas.
    """
    return render_template("module_jya.html", current_page='jya')


# Funcionalidades para DOCUMENTOS

@jya_bp.route('/documentos/<int:id>', methods=['GET'])
@login_required
@check("jya_index")
@check("jya_show")
def documentos(id):
    # recibe el id del JyA
    type_doc=list_typedoc_fileJyA()
    
    legajo=get_legajoJyA_by_id(id)
    docs = [doc for doc in legajo.documents if not doc.deleted]

    return render_template(
        "documentos/explore.html",
        current_page='jya', legajo_id=id, type_doc=type_doc, items_on_page=docs
    )


@jya_bp.route('/cargar_enlace/<int:id>', methods=['POST'])
@login_required
@check("jya_new")
def upload_link(id):
    enlace = request.form.get('enlace')
    if enlace and validate_link(enlace):
        params = request.form.copy()
        flash("Enlace cargado exitosamente.", "alert-success")
        addLinkLegajo(params, id)
    else:
        flash("La URL ingresada es inválida. Por favor, introduce una URL válida.", "alert-danger")
    return redirect(url_for('module_jya.documentos', id=id))


@jya_bp.route('/editar_documento/<int:id>', methods=['GET', 'POST'])
@login_required
@check("jya_update")
def edit_document(id):
    """
    Función que permite editar un documento registrado en la base de datos.
    Decoradores:
        - @jya_bp.route('/editar_documento/<int:id>', methods=['GET', 'POST']): Define la ruta de la página de edición de documentos.
        - @login_required: Requiere que el usuario esté autenticado para acceder a la vista.
        - @check("jya_update"): Requiere que el usuario tenga el permiso "jya_update" para editar un documento.
    Atributos:
        - id: Identificador del documento a editar.
    Retorno:
        - render_template('documento/edit.html', documento=documento):
        Renderiza la plantilla "documento/edit.html" con el formulario de edición y los datos del documento a editar.
    """
    
    document = get_document_by_id(id)
    type_doc=list_typedoc_fileJyA()

    if not document:
        flash("Documento no encontrado.", "alert-danger")
        return redirect(url_for('module_jya.explore'))

    if request.method == 'GET':
        return render_template('documentos/edit.html', document=document, type_doc=type_doc)

    if request.method == 'POST':        
        legajo_id = document.fileJyA_id
        params = request.form.copy()
        enlace = request.form.get('enlace')

        # si es un enlace
        if enlace:
            if validate_link(enlace):
                flash("Enlace modificado exitosamente.", "alert-success")
                updateDocumentLegajo(params, document)
            else:
                flash("La URL ingresada es inválida. Por favor, introduce una URL válida.", "alert-danger")
                return render_template('documentos/edit.html', document=document, type_doc=type_doc)
        # si es un archivo:
        else:
            # si se seleccionó un archivo nuevo en el formulario
            if request.files.get('documento').filename != '':
                files = request.files.getlist('documento')
                errors = validate_documents(files)
                if errors:
                    flash(" ".join(errors), "alert-danger")
                    return render_template('documentos/edit.html', document=document, type_doc=type_doc)
                else:
                    file = request.files['documento']
                    secure_name = secure_filename(file.filename)
                    params['documento'] = secure_name
                    
                    client = current_app.storage.client
                    size = fstat(file.fileno()).st_size
                    file_name = f"{id}.{secure_name}"
                    client.put_object(
                        "grupo07", file_name, file, size, content_type=file.content_type
                    )
            updateDocumentLegajo(params, document)
            flash("Archivo modificado exitosamente.", "alert-success")

        return redirect(url_for('module_jya.documentos', id=legajo_id))


@jya_bp.route('/eliminar_documento/<int:id>', methods=['POST'])
@login_required
@check("jya_destroy")
def delete_doc(id):
    """
    Función que permite eliminar un documento registrado en la base de datos.
    Decoradores:
        - @jya_bp.route('/eliminar_documento/<int:id>', methods=['POST']): Define la ruta de eliminación de codumentos.
        - @login_required: Requiere que el usuario esté autenticado para acceder a la vista.
        - @check("jya_destroy"): Requiere que el usuario tenga el permiso "jya_destroy" para eliminar un documento.
    Atributos:
        - id: identificador del documento a eliminar.
    Retorno:
        - redirect(url_for('module_jya.documentos')):
        Redirecciona a la vista de exploración de documentos.
    """
    document = get_document_by_id(id)
    legajo_id = document.fileJyA_id
    if document:
        delete_document(document)
        flash(f'El documento "{document.name}" se ha eliminado correctamente.', 'alert-success')
    else:
        flash(
            "Ha ocurrido un error y no se ha podido realizar la operación.", "alert-danger")

    return redirect(url_for('module_jya.documentos', id=legajo_id))


@jya_bp.route('/cargar_archivo/<int:id>', methods=['POST'])
@login_required
@check("jya_index")
@check("jya_new")
def upload_document(id):
    # recibe el id de JyA
    params = request.form.copy()

    # ésto es para que funcione con el validador de Mili.
    files = request.files.getlist('documento')

    errors = validate_documents(files)
    if errors:
        flash(" ".join(errors), "alert-danger")
    else:
        file = request.files['documento']
        secure_name = secure_filename(file.filename)
        
        params['documento'] = secure_name
        doc_id = addDocumentLegajo(params, id)
        
        client = current_app.storage.client
        size = fstat(file.fileno()).st_size
        file_name = f"{doc_id}.{secure_name}"
        client.put_object(
            "grupo07", file_name, file, size, content_type=file.content_type
        )
        flash("Archivo cargado exitosamente.", "alert-success")

    return redirect(url_for('module_jya.documentos', id=id))


# Funcionalidades para INDEX

@jya_bp.route('/explore', methods=['GET'])
@login_required
@check("jya_index")
@check("jya_show")
def explore():
    """
    Función que renderiza la vista de exploración de legajos de jinetes y amazonas.
    Decoradores:
        - @check("jya_index"): verifica que el usuario tenga permisos para acceder a la vista.
        - @check("jya_show"): verifica que el usuario tenga permisos para acceder a la vista.
        - @login_required: verifica que el usuario haya iniciado sesión.
        - @route('/explore', methods=['GET']): define la ruta y los métodos HTTP permitidos para acceder a la vista.
    Argumentos: Ninguno.
    Retorna:
        - render_template("jya/explore.html", current_page='jya', items_on_page=items_on_page, 
        total_pages=total_pages, page=page, errors=errors, filters=filters): 
        renderiza la vista de exploración de legajos de jinetes y amazonas.
    """
    global queryResult
    global total_pages
    global per_page
    page = request.args.get('page', 1, type=int)
    items_on_page = []

    # Resetear filtros si `reset=1`
    if request.args.get('reset', 0, type=int) == 1:
        session.pop('query_filters', None)
        queryResult = None  # Limpiar el resultado de la consulta
        total_pages = 0  # Restablecer el total de páginas

    # Obtener filtros de búsqueda de la solicitud GET
    first_name = request.args.get('first_name', '')
    last_name = request.args.get('last_name', '')
    dni = request.args.get('dni', '')

    filters = {
        'first_name': first_name,
        'last_name': last_name,
        'dni': dni,
        'attending_professionals': request.args.get('attending_professionals', '')
    }

    # Validar los filtros
    errors = validateSearchLegajoJyA(first_name, last_name, dni)

    # Guardar filtros en la sesión si no hay errores
    if not errors:
        session['query_filters'] = filters
        queryResult = search_legajos(**filters)
        if not queryResult:
            flash("No se encontraron resultados.", "alert-warning")
        total_pages = (queryResult.count() + per_page - 1) // per_page
    else:
        filters = session.get('query_filters', {})

    # Si no hay una búsqueda activa, cargar datos por defecto
    if not queryResult and not ('query_filters' in session):
        queryResult = query_legajosJyA()
        total_pages = (queryResult.count() + per_page - 1) // per_page

    # Ordenar los resultados
    aux_query = order_legajosJyA(queryResult, request.args.get(
        'orderBy', 'first_name'), order=request.args.get('orderDirection'))

    # Paginación
    start = (page - 1) * per_page
    items_on_page = aux_query[start:start + per_page] if queryResult else []

    if request.args.get('debt', 0, type=int) == 1:
        return render_template(
            "jya/in_debt.html", current_page='receipt',
            items_on_page=items_on_page, total_pages=total_pages,
            page=page, errors=errors, filters=filters
        )

    return render_template(
        "jya/explore.html",
        current_page='jya',
        items_on_page=items_on_page,
        total_pages=total_pages,
        page=page,
        errors=errors,
        filters=filters
    )


def validateSearchLegajoJyA(first_name, last_name, dni):
    """
    Función que valida los filtros de búsqueda de legajos de jinetes y amazonas.
    Argumentos:
        - first_name (str): nombre del jinete o amazona.
        - last_name (str): apellido del jinete o amazona.
        - dni (str): número de documento del jinete o amazona.
    Retorna:
        - errors (dict): diccionario con los errores de validación.
    """
    # Valida que los filtros sean validos
    errors = {}
    if first_name:
        if not bool(re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", first_name)):
            errors["first_name"] = "La fecha desde no puede ser mayor que la fecha actual."
            flash("El nombre solo puede contener letras", "alert-danger")
    if last_name:
        if not bool(re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", last_name)):
            errors["last_name"] = "La fecha desde no puede ser mayor que la fecha actual."
            flash("El apellido solo puede contener letras.", "alert-danger")
    if dni:
        if not bool(re.fullmatch(r"\d+", dni)):
            errors["dni"] = "La fecha desde no puede ser mayor que la fecha hasta."
            flash("El dni solo puede contener numeros.", "alert-danger")
    return errors


# Funcionalidades para DESTROY


@jya_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@check("jya_index")
@check("jya_destroy")
def delete(id):
    """
    Función que maneja la eliminación de un legajo JyA.
    Decoradores:
        - @check("jya_index"): verifica que el usuario tenga permisos para acceder a la vista.
        - @check("jya_destroy"): verifica que el usuario tenga permisos para eliminar un legajo de jinete o amazona.
        - @login_required: verifica que el usuario haya iniciado sesión.
        - @route('/delete/<int:id>', methods=['POST']): define la ruta y los métodos HTTP permitidos para acceder a la
    Argumentos:
        - id (int): identificador del legajo de jinete o amazona a eliminar.
    Retorna:
    """
    # chequeo si se apreto el botón desde la vista de explorar
    global total_pages
    if 'explore' not in request.referrer:
        flash(
            "Ha ocurrido un error y no se ha podido realizar la operación.", "alert-danger")
        return redirect(url_for('module_jya.explore'))
    fileJyA = get_legajoJyA_by_id(id)
    if fileJyA:
        if filejya_has_receipts(fileJyA):
            flash(
                "No es posible eliminar este legajo! Posee registro de cobros asociado", "alert-danger")
            return redirect(url_for('module_jya.explore'))
        else:
            logical_delete(fileJyA)
            # elimino el fileJyA en queryResult
            global queryResult
            queryResult = list(queryResult)
            for e in queryResult:
                if e.id == id:
                    queryResult.remove(e)
            total_pages = (len(queryResult) + per_page - 1) // per_page
            flash(f"El Legajo se ha eliminado correctamente {
                id} se ha eliminado correctamente.", "alert-success")
    else:
        flash(
            "Ha ocurrido un error y no se ha podido realizar la operación.", "alert-danger")
    return redirect(url_for('module_jya.explore'))

# Funcionalidades para Marcar como deudor o no


@jya_bp.route('/mark_not_deudor/<int:id>', methods=['POST'])
@login_required
@check("jya_index")
@check("jya_update")
def mark_not_deudor(id):
    """
    Función que maneja el marcado un legajo de jinete o amazona como no deudor.
    Decoradores:
        - @check("jya_index"): verifica que el usuario tenga permisos para acceder a la vista.
        - @check("jya_update"): verifica que el usuario tenga permisos para actualizar un legajo de jinete o amazona.
        - @login_required: verifica que el usuario haya iniciado sesión.
        - @route('/mark_not_deudor/<int:id>', methods=['POST']): define la ruta y los métodos HTTP permitidos para acceder a la vista.
    Argumentos:
        - id (int): identificador del legajo de jinete o amazona a marcar como no deudor.
    Retorna:
        - redirect(url_for('module_jya.explore', debt=1)): 
        redirige a la vista de exploración de legajos de jinetes y amazonas.
    """
    file_jya = get_legajoJyA_by_id(id)
    if file_jya:
        modify_status_receipts_legajoJyA(file_jya, False)
        flash('El legajo ha sido marcado como no deudor.', 'alert-success')
    else:
        flash('No se encontró el legajo.', 'alert-danger')

    return redirect(url_for('module_jya.explore', debt=1))


@jya_bp.route('/mark_deudor/<int:id>', methods=['POST'])
@login_required
@check("jya_index")
@check("jya_update")
def mark_deudor(id):
    """
    Función que maneja el marcado un legajo de jinete o amazona como deudor.
    Decoradores:
        - @check("jya_index"): verifica que el usuario tenga permisos para acceder a la vista.
        - @check("jya_update"): verifica que el usuario tenga permisos para actualizar un legajo de jinete o amazona.
        - @login_required: verifica que el usuario haya iniciado sesión.
        - @route('/mark_deudor/<int:id>', methods=['POST']): define la ruta y los métodos HTTP permitidos para acceder a la vista.
    Argumentos:
        - id (int): identificador del legajo de jinete o amazona a marcar como deudor.
    Retorna:
        - redirect(url_for('module_jya.explore', debt=1)): 
        redirige a la vista de exploración de legajos de jinetes y amazonas.
    """
    file_jya = get_legajoJyA_by_id(id)
    if file_jya:
        modify_status_receipts_legajoJyA(file_jya, True)
        flash('El legajo ha sido marcado como deudor.', 'alert-success')
    else:
        flash('No se encontró el legajo.', 'alert-danger')

    return redirect(url_for('module_jya.explore', debt=1))


# Funcionalidades para SHOW,EDIT


@jya_bp.route('/edit/<int:id>', methods=['GET'])
@login_required
@check("jya_index")
@check("jya_show")
def edit(id):
    """
    Función que renderiza la vista de edición de un legajo de jinete o amazona.
    Decoradores:
        - @check("jya_index"): verifica que el usuario tenga permisos para acceder a la vista.
        - @check("jya_show"): verifica que el usuario tenga permisos para mostrar un legajo de jinete o amazona.
        - @login_required: verifica que el usuario haya iniciado sesión.
        - @route('/edit/<int:id>', methods=['GET']): define la ruta y los métodos HTTP permitidos para acceder a la vista.
    Argumentos:
        - id (int): identificador del legajo de jinete o amazona a editar.
    Retorna:
        - render_template("jya/edit.html", current_page='jya', form=file_jya_form, id=id): 
        renderiza la vista de edición de un legajo de jinete o amazona.
    """
    equestrians = list_equestrians()
    team_members = list_miembros_equipo_not_eliminated()

    file_jya = get_legajoJyA_by_id(id)

    file_jya_form = FileJyAForm()

    file_jya_form.first_name.data = file_jya.first_name
    file_jya_form.last_name.data = file_jya.last_name
    file_jya_form.dni.data = file_jya.dni
    file_jya_form.age.data = file_jya.age
    file_jya_form.birth_date.data = file_jya.birth_date
    file_jya_form.birth_locality.data = file_jya.birth_locality
    file_jya_form.birth_province.data = file_jya.birth_province
    file_jya_form.adress_street.data = file_jya.adress_street
    file_jya_form.adress_number.data = file_jya.adress_number
    file_jya_form.adress_apartment.data = file_jya.adress_apartment
    file_jya_form.adress_locality.data = file_jya.adress_locality
    file_jya_form.adress_province.data = file_jya.adress_province
    file_jya_form.phone.data = file_jya.phone
    file_jya_form.emergency_contact_name.data = file_jya.emergency_contact_name
    file_jya_form.emergency_contact_phone.data = file_jya.emergency_contact_phone
    file_jya_form.attending_professionals.data = file_jya.attending_professionals

    if (file_jya.disability_certificate):
        file_jya_form.disability_certificate.data = 'si'
    else:
        file_jya_form.disability_certificate.data = 'no'

    file_jya_form.disability_certificate_diagnosis.data = file_jya.disability_certificate_diagnosis or []
    file_jya_form.other_diagnosis_disability.data = file_jya.other_diagnosis_disability
    file_jya_form.disability_type.data = file_jya.disability_type or []

    if (file_jya.scholarship):
        file_jya_form.scholarship.data = 'si'
    else:
        file_jya_form.scholarship.data = 'no'

    file_jya_form.per_scholarship.data = file_jya.per_scholarship
    file_jya_form.scholarship_notes.data = file_jya.scholarship_notes

    if (file_jya.welfare):
        file_jya_form.welfare.data = 'si'
        file_jya_form.welfare_type.data = file_jya_form.welfare_type.data or []
        if file_jya.child_welfare:
            file_jya_form.welfare_type.data.append('child_welfare')
        if file_jya.child_disability_welfare:
            file_jya_form.welfare_type.data.append('child_disability_welfare')
        if file_jya.school_help_welfare:
            file_jya_form.welfare_type.data.append('school_help_welfare')
    else:
        file_jya_form.welfare.data = 'no'

    if (file_jya.pension_beneficiary):
        file_jya_form.pension_beneficiary.data = 'si'
    else:
        file_jya_form.pension_beneficiary.data = 'no'

    file_jya_form.pension_type.data = file_jya.pension_type

    if file_jya.provisional_situation:
        # Accede al primer elemento
        provisional_situation = file_jya.provisional_situation[0]
        if provisional_situation.social_security is not None:
            file_jya_form.social_security.data = provisional_situation.social_security

        if provisional_situation.affiliate_number is not None:
            file_jya_form.affiliate_number.data = provisional_situation.affiliate_number

        if (provisional_situation.has_guardianship):
            file_jya_form.has_guardianship.data = 'si'
        else:
            file_jya_form.has_guardianship.data = 'no'

        if provisional_situation.previsional_situacion_notes is not None:
            file_jya_form.previsional_situacion_notes.data = provisional_situation.previsional_situacion_notes

    if file_jya.school_situacion:  # Verifica si hay una situación escolar
        # Accede a la situación escolar (puede haber solo una)
        school_situation = file_jya.school_situacion[0]

        if school_situation.institution_name is not None:
            file_jya_form.institution_name.data = school_situation.institution_name

        if school_situation.school_address is not None:
            file_jya_form.school_address.data = school_situation.school_address

        if school_situation.school_phone is not None:
            file_jya_form.school_phone.data = school_situation.school_phone

        if school_situation.current_grade is not None:
            file_jya_form.current_grade.data = school_situation.current_grade

        if school_situation.school_notes is not None:
            file_jya_form.school_notes.data = school_situation.school_notes

    # Para Tutor 1
    if file_jya.tutors:  # Verifica si existe un tutor 1
        tutor1 = file_jya.tutors[0]  # Accede al tutor 1

        if tutor1.relationship is not None:
            file_jya_form.relationship1.data = tutor1.relationship

        if tutor1.first_name is not None:
            file_jya_form.first_name1.data = tutor1.first_name

        if tutor1.last_name is not None:
            file_jya_form.last_name1.data = tutor1.last_name

        if tutor1.dni is not None:
            file_jya_form.dni1.data = tutor1.dni

        if tutor1.current_address is not None:
            file_jya_form.current_address1.data = tutor1.current_address

        if tutor1.mobile_phone is not None:
            file_jya_form.mobile_phone1.data = tutor1.mobile_phone

        if tutor1.email is not None:
            file_jya_form.email1.data = tutor1.email

        if tutor1.education_level is not None:
            file_jya_form.education_level1.data = tutor1.education_level

        if tutor1.occupation is not None:
            file_jya_form.occupation1.data = tutor1.occupation

        tutor2 = file_jya.tutors[1]  # Accede al tutor 2

        if tutor2.relationship is not None:
            file_jya_form.relationship2.data = tutor2.relationship

        if tutor2.first_name is not None:
            file_jya_form.first_name2.data = tutor2.first_name

        if tutor2.last_name is not None:
            file_jya_form.last_name2.data = tutor2.last_name

        if tutor2.dni is not None:
            file_jya_form.dni2.data = tutor2.dni

        if tutor2.current_address is not None:
            file_jya_form.current_address2.data = tutor2.current_address

        if tutor2.mobile_phone is not None:
            file_jya_form.mobile_phone2.data = tutor2.mobile_phone

        if tutor2.email is not None:
            file_jya_form.email2.data = tutor2.email

        if tutor2.education_level is not None:
            file_jya_form.education_level2.data = tutor2.education_level

        if tutor2.occupation is not None:
            file_jya_form.occupation2.data = tutor2.occupation

    if file_jya.work_proposal:  # Verifica si existe una propuesta de trabajo
        # Accede a la propuesta de trabajo
        work_proposal = file_jya.work_proposal[0]

        if work_proposal.work_proposal is not None:
            file_jya_form.work_proposal.data = work_proposal.work_proposal

        if work_proposal.condition is not None:
            file_jya_form.condition.data = work_proposal.condition

        if work_proposal.location is not None:
            file_jya_form.location.data = work_proposal.location

        if work_proposal.days is not None:
            file_jya_form.days.data = work_proposal.days

    teacher_or_therapist = None
    horse_handler = None
    track_assistant = None
    equestrian = None

    if work_proposal.teacher_or_therapist:  # Verifica si la relación existe
        teacher_or_therapist = work_proposal.teacher_or_therapist

    if work_proposal.horse_handler:  # Verifica si la relación existe
        horse_handler = work_proposal.horse_handler

    if work_proposal.track_assistant:  # Verifica si la relación existe
        track_assistant = work_proposal.track_assistant

    if work_proposal.equestrian:  # Verifica si la relación existe
        equestrian = work_proposal.equestrian

    return render_template("jya/edit.html",
                           current_page='jya', form=file_jya_form, id=id, equestrians=equestrians, team_members=team_members, teacher_or_therapist=teacher_or_therapist, horse_handler=horse_handler, track_assistant=track_assistant, equestrian=equestrian, legajo_id=id)


@jya_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
@check("jya_index")
@check("jya_show")
@check("jya_update")
def edit_receipt(id):
    """
    Función que maneja la edición de un legajo de jinete o amazona.
    Decoradores:
        - @check("jya_index"): verifica que el usuario tenga permisos para acceder a la vista.
        - @check("jya_show"): verifica que el usuario tenga permisos para mostrar un legajo de jinete o amazona.
        - @check("jya_update"): verifica que el usuario tenga permisos para actualizar un legajo de jinete o amazona.
        - @login_required: verifica que el usuario haya iniciado sesión.
        - @route('/edit/<int:id>', methods=['POST']): define la ruta y los métodos HTTP permitidos para acceder a la vista.
    Argumentos:
        - id (int): identificador del legajo de jinete o amazona a editar.
    Retorna:
        - render_template("jya/edit.html", current_page='jya', form=file_jya_form, id=id): 
        renderiza la vista de edición de un legajo de jinete o amazona.
    """
    newLegajo = FileJyAForm()
    if validateJyAAdd(newLegajo, True):
        modify_filejya(id, newLegajo, obtain_teacher_or_therapist(
        ), obtain_horse_handler(), obtain_track_assistant(), obtain_equestrian())
        flash("¡El Legajo JyA se ha modificado correctamente!", "alert-success")
        return redirect(url_for('module_jya.edit', id=id))
    else:
        flash("¡El Legajo JyA no se ha modificado!", "alert-danger")
        equestrians = list_equestrians()
        team_members = list_miembros_equipo_not_eliminated()

        return render_template("jya/edit.html",
                               current_page='jya',
                               form=newLegajo,
                               id=id,
                               equestrians=equestrians,
                               team_members=team_members,
                               teacher_or_therapist=obtain_teacher_or_therapist(),
                               horse_handler=obtain_horse_handler(),
                               track_assistant=obtain_track_assistant(),
                               equestrian=obtain_equestrian())


# Funcionalidad para cargar legajo

@jya_bp.get('/upload')
@login_required
@check("jya_index")
@check("jya_new")
def upload():
    """
    Función que renderiza la vista de carga de un legajo de jinete o amazona.
    Decoradores:
        - @check("jya_index"): verifica que el usuario tenga permisos para acceder a la vista.
        - @check("jya_new"): verifica que el usuario tenga permisos para crear un legajo de jinete o amazona.
        - @login_required: verifica que el usuario haya iniciado sesión.
        - @jya_bp.get('/upload'): define la ruta y los métodos HTTP permitidos para acceder a la vista.
    Argumentos: Ninguno.
    Retorna:
        - render_template("jya/upload.html", current_page='upload', form=fileJyA_form,team_members=team_members,equestrians=equestrians,teacher_or_therapist='',horse_handler='',track_assistant='',current_equestrian=''):
        renderiza la vista de carga de un legajo de jinete o amazona.
    """
    team_members = list_miembros_equipo_not_eliminated()
    equestrians = list_equestrians()

    fileJyA_form = FileJyAForm()
    return render_template("jya/upload.html", current_page='upload', form=fileJyA_form, team_members=team_members, equestrians=equestrians, teacher_or_therapist='', horse_handler='', track_assistant='', current_equestrian='')


@jya_bp.post('/upload')
@login_required
@check("jya_index")
@check("jya_new")
def upload_post():
    """
    Función que maneja la carga de un legajo de jinete o amazona.
    Decoradores:
        - @check("jya_index"): verifica que el usuario tenga permisos para acceder a la vista.
        - @check("jya_new"): verifica que el usuario tenga permisos para crear un legajo de jinete o amazona.
        - @login_required: verifica que el usuario haya iniciado sesión.
        - @jya_bp.post('/upload'): define la ruta y los métodos HTTP permitidos para acceder a la vista.
    """
    fileJyA_form = FileJyAForm()
    if validateJyAAdd(fileJyA_form, False):
        add_fileJyA(fileJyA_form, obtain_teacher_or_therapist(
        ), obtain_horse_handler(), obtain_track_assistant(), obtain_equestrian())
        flash("¡El Legajo JyA se ha registrado correctamente!", "alert-success")
        return redirect(url_for('module_jya.upload', current_page='jya'))
    team_members = list_miembros_equipo_not_eliminated()
    equestrians = list_equestrians()

    teacher_or_therapist = obtain_teacher_or_therapist()
    horse_handler = obtain_horse_handler()
    track_assistant = obtain_track_assistant()
    equestrian = obtain_equestrian()

    return render_template("jya/upload.html", current_page='jya', form=fileJyA_form, team_members=team_members, equestrians=equestrians,
                           # Devuelve el formulario en caso de error
                           teacher_or_therapist=teacher_or_therapist, horse_handler=horse_handler, track_assistant=track_assistant, current_equestrian=equestrian)


def obtain_teacher_or_therapist():
    """
    Función que obtiene el valor del campo "teacher_or_therapist" del formulario de carga de un legajo de jinete o amazona.
    Argumentos: Ninguno.
    Retorna: str
    """
    return request.form.get('teacher_or_therapist')


def obtain_horse_handler():
    """
    Función que obtiene el valor del campo "horse_handler" del formulario de carga de un legajo de jinete o amazona.
    Argumentos: Ninguno.
    Retorna: str
    """
    return request.form.get('horse_handler')


def obtain_track_assistant():
    """
    Función que obtiene el valor del campo "track_assistant" del formulario de carga de un legajo de jinete o amazona.
    Argumentos: Ninguno.
    Retorna: str
    """
    return request.form.get('track_assistant')


def obtain_equestrian():
    """
    Función que obtiene el valor del campo "equestrian" del formulario de carga de un legajo de jinete o amazona.
    Argumentos: Ninguno.
    Retorna: str
    """
    return request.form.get('equestrian')


def validateJyAAdd(fileJyA_form, mod):
    """
    Función que valida los campos del formulario de carga de un legajo de jinete o amazona.
    Argumentos:
        - fileJyA_form (FileJyAForm): formulario de carga de un legajo de jinete o amazona.
        - mod (bool): indica si se está modificando un legajo existente.
    Retorna:
        - bool: True si los campos son válidos, False en caso
    """
    aux = True
    if not fileJyA_form.validate_on_submit():
        aux = False
    if (aux):
        aux = validateAditional(fileJyA_form, mod)
    else:
        validateAditional(fileJyA_form, mod)
    return aux


def validateAditional(fileJyA_form, modify):
    """
    Función que valida los campos adicionales del formulario de carga de un legajo de jinete o amazona.
    Argumentos:
        - fileJyA_form (FileJyAForm): formulario de carga de un legajo de jinete o amazona.
        - modify (bool): indica si se está modificando un legajo existente.
    Retorna:
        - bool: True si los campos son válidos, False en caso contrario.
    """
    aux = True
    # Validación de discapacidad
    if fileJyA_form.disability_certificate.data == 'si':
        if not (fileJyA_form.disability_certificate_diagnosis.data or fileJyA_form.other_diagnosis_disability.data):
            aux = False
            fileJyA_form.disability_certificate_diagnosis.errors.append(
                "Debes seleccionar al menos un diagnóstico de discapacidad o especificar otra.")
        if not fileJyA_form.disability_type.data:
            aux = False
            fileJyA_form.disability_type.errors.append(
                "Debes seleccionar al menos un tipo de discapacidad.")
    if fileJyA_form.disability_certificate.data == 'no':
        if (fileJyA_form.disability_certificate_diagnosis.data or fileJyA_form.other_diagnosis_disability.data):
            aux = False
            fileJyA_form.disability_certificate_diagnosis.errors.append(
                "No posee certificado de discapacidad, dato no solicitado")
        if fileJyA_form.disability_type.data:
            aux = False
            fileJyA_form.disability_type.errors.append(
                "No posee certificado de discapacidad, dato no solicitado")
    # Validacion de beca
    if fileJyA_form.scholarship.data == 'si':
        if not (fileJyA_form.per_scholarship.data):
            aux = False
            fileJyA_form.per_scholarship.errors.append(
                "Posee beca, indicar porcentaje")
    if fileJyA_form.scholarship.data == 'no':
        if (fileJyA_form.per_scholarship.data):
            aux = False
            fileJyA_form.per_scholarship.errors.append(
                "No posee beca, no indicar porcentaje")
    # Validacion de asignacion
    if fileJyA_form.welfare.data == 'si':
        if not (fileJyA_form.welfare_type.data):
            aux = False
            fileJyA_form.welfare_type.errors.append(
                "Posee asiganción, indicar porcentaje")
    if fileJyA_form.welfare.data == 'no':
        if (fileJyA_form.welfare_type.data):
            aux = False
            fileJyA_form.welfare_type.errors.append(
                "No posee asiganción, no indicar cuales")
    # validacion pension
    if fileJyA_form.pension_beneficiary.data == 'si':
        if not (fileJyA_form.pension_type.data):
            aux = False
            fileJyA_form.pension_type.errors.append(
                "Posee asiganción, indicar porcentaje")
    if fileJyA_form.pension_beneficiary.data == 'no':
        if (fileJyA_form.pension_type.data):
            aux = False
            fileJyA_form.pension_type.errors.append(
                "No posee asiganción, no indicar cuales")
            fileJyA_form.pension_type.data = None
    # validacion dni
    if not modify:
        # DNI NO MODIFICABLE
        if legajo_jya_exists_by_dni(fileJyA_form.dni.data):
            aux = False
            fileJyA_form.dni.errors.append("DNI ya cargado en el sistema")
        return aux
    return aux
