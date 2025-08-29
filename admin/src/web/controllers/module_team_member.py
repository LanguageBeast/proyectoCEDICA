from os import fstat
from flask import Blueprint
from src.web.handlers.auth import check, login_required
from flask import render_template, request, redirect, url_for, flash
from src.web.forms import TeamMemberForm
from core import entities, validators
from flask import current_app
from werkzeug.utils import secure_filename
from src.core.config import Config


# Blueprint para las funcionalidades del modulo equipo
team_member_bp = Blueprint(
    'module_team_member', __name__, url_prefix="/modulo_equipo")


@team_member_bp.get('/')
@login_required
@check("team_member_index")
def equipo():
    """
    Función que renderiza la vista principal del módulo de equipo
    Decoradores:
        - @login_required: Valida que el usuario haya iniciado sesión
        - @check("team_member_index"): Valida que el usuario tenga permisos para acceder a la vista
    Argumentos: Ninguno
    Retorna: La vista principal del módulo de equipo
    """
    return render_template("module_team_member.html", current_page='team_member')


@team_member_bp.get('/crear')
@login_required
@check("team_member_index")
@check("team_member_new")
def upload_get():
    """
    Función que renderiza el formulario para registrar un nuevo miembro del equipo.
    Decoradores:
        - @login_required: Valida que el usuario haya iniciado sesión
        - @check("team_member_index"): Valida que el usuario tenga permisos para acceder a la vista
        - @check("team_member_new"): Valida que el usuario tenga permisos para crear un nuevo miembro del equipo
        - @team_member_bp.route('/crear', methods=['GET']): Define la ruta para acceder a la vista
    Argumentos: Ninguno
    Retorna: render_template('team_member/upload.html', form=form,current_page='team_member'):
        - Renderiza la vista para registrar un nuevo miembro del equipo
    """
    form = TeamMemberForm()
    return render_template('team_member/upload.html', form=form, current_page='team_member')


@team_member_bp.post('/crear')
@login_required
@check("team_member_index")
@check("team_member_new")
def upload_post():
    """
    Función que procesa el formulario para registrar un nuevo miembro del equipo.
    Decoradores:
        - @login_required: Valida que el usuario haya iniciado sesión
        - @check("team_member_index"): Valida que el usuario tenga permisos para acceder a la vista
        - @check("team_member_new"): Valida que el usuario tenga permisos para crear un nuevo miembro del equipo
        - @team_member_bp.route('/crear', methods=['POST']): Define la ruta para procesar el formulario
    Argumentos: Ninguno
    Retorna: 
        - Caso 1: redirect(url_for('module_team_member.upload_get')): 
        Redirige al usuario a la vista de registro de miembro del equipo
        - Caso 2: render_template("team_member/upload.html", current_page='team_member', form=form): 
        Renderiza la vista de registro de miembro del equipo
    """
    form = TeamMemberForm()
    # Validar y procesar el formulario
    if form.validate_on_submit() and validators.validate_team_member_data_upload(form):
        files = request.files.getlist('documents')
        if form.documents.data:
            errors = validators.validate_documents(files)

            if errors:
                flash(" ".join(errors), "alert-danger")
                return render_template("team_member/upload.html", current_page='team_member', form=form)
        team_member = entities.create_team_member(first_name=form.first_name.data,last_name=form.last_name.data,dni=form.dni.data,address=form.address.data,email=form.email.data,location=form.location.data,phone=form.phone.data,profession=form.profession.data,job_position=form.job_position.data,start_date=form.start_date.data,end_date=form.end_date.data,emergency_contact_name=form.emergency_contact_name.data,emergency_contact_phone=form.emergency_contact_phone.data,health_insurance=form.health_insurance.data,insurance_number=form.insurance_number.data,condition=form.condition.data,active=form.active.data)
        if form.documents.data:
            client = current_app.storage.client
            for file in files:
                upload_document(file,team_member, client)
            
        flash('El miembro del equipo ha sido registrado exitosamente.', "alert-success")
        return redirect(url_for('module_team_member.upload_get'))

    else:
        flash("Por favor, corrige los errores en el formulario.", "alert-danger")
        return render_template("team_member/upload.html", current_page='team_member', form=form)

def upload_document(file, team_member, client):
    secure_name = secure_filename(file.filename)
    document=entities.create_document(name=secure_name)
    entities.assign_team_member_document(document, team_member)
    file_name = f"{document.id}.{secure_name}"  # Concatenar ambos
    file.seek(0)  # Restablece el puntero del archivo
    size = len(file.read())
    file.seek(0)  # Restablece el puntero nuevamente para la subida
    # Subir archivo a MinIO
    client.put_object(
        bucket_name=Config.BUCKET_NAME,
        object_name=file_name,
        data=file,
        length=size,
        content_type=file.content_type
    )

@team_member_bp.route('/explorar', methods=['GET', 'POST'])
@login_required
@check("team_member_index")
@check("team_member_show")
def explore():
    """
    Función que permite explorar los miembros del equipo.
    Decoradores:
        - @login_required: Valida que el usuario haya iniciado sesión
        - @check("team_member_index"): Valida que el usuario tenga permisos para acceder a la vista
        - @check("team_member_show"): Valida que el usuario tenga permisos para explorar los miembros del equipo
        - @team_member_bp.route('/explorar', methods=['GET', 'POST']): Define la ruta para acceder a la vista
    Argumentos: Ninguno
    Retorna: 
        - Caso 1: render_template('team_member/explore.html',current_page='team_member',members=members, page=page, 
        total_pages=total_pages,order_direction=order_direction,order_by=order_by,filter=filter,search_string=search_string,job_position=job_position):
        Renderiza la vista de exploración de miembros del equipo
        - Caso 2: redirect(url_for('module_team_member.explore')):
        Redirige al usuario a la vista de exploración de miembros del equipo
    """
    page = request.args.get('page', 1, type=int)  # Obtener el número de página
    per_page = 25

    order_by = request.args.get('order_by', 'created_at')
    order_direction = request.args.get('order_direction', 'asc')

    filter = request.form.get(
        'filter') if request.method == 'POST' else request.args.get('filter')
    search_string = request.form.get(
        'search_string') if request.method == 'POST' else request.args.get('search_string')
    job_position = request.form.get('job_position') if request.method == 'POST' else request.args.get(
        'job_position')  # Obtener el puesto laboral

    is_valid, error_message = validators.validate_search_criteria(
        filter, search_string, job_position)
    if not is_valid:
        flash(error_message, "alert-danger")
        return redirect(url_for('module_team_member.explore', page=page))

    members, total_pages = entities.get_members(
        page, per_page, filter, search_string, job_position, order_by, order_direction)
    if not members:
        flash('No se encontraron resultados.', 'alert-warning')
    return render_template('team_member/explore.html',current_page='team_member',members=members, page=page, total_pages=total_pages,order_direction=order_direction,order_by=order_by,filter=filter,search_string=search_string,job_position=job_position)

@team_member_bp.route('/editar/<int:id>', methods=['GET'])
@login_required
@check("team_member_index")
@check("team_member_update")
def edit_get(id):
    """
    Función que renderiza el formulario para editar un miembro del equipo.
    Decoradores:
        - @login_required: Valida que el usuario haya iniciado sesión
        - @check("team_member_index"): Valida que el usuario tenga permisos para acceder a la vista
        - @check("team_member_update"): Valida que el usuario tenga permisos para editar un miembro del equipo
        - @team_member_bp.route('/editar/<int:id>', methods=['GET']): Define la ruta para acceder a la vista
    Argumentos:
        - id: Identificador del miembro del equipo
    Retorna:
        - Caso 1: render_template('team_member/edit.html',current_page='team_member', form=form, team_member=team_member):
        Renderiza la vista para editar un miembro del equipo
        - Caso 2: redirect(url_for('module_team_member.explore')):
        Redirige al usuario a la vista de exploración de miembros del equipo
    """
    team_member = entities.get_team_member_by_id(id)

    if not team_member:
        flash("Miembro del equipo no encontrado.", "alert-danger")
        return redirect(url_for('module_team_member.explore'))

    # Crear una instancia del formulario con los datos actuales del miembro del equipo
    form = TeamMemberForm(obj=team_member)

    return render_template('team_member/edit.html', current_page='team_member', form=form, team_member=team_member)


@team_member_bp.route('/editar/<int:id>', methods=['POST'])
@login_required
@check("team_member_index")
@check("team_member_update")
def edit_post(id):
    """
    Función que procesa el formulario para editar un miembro del equipo.
    Decoradores:
        - @login_required: Valida que el usuario haya iniciado sesión
        - @check("team_member_index"): Valida que el usuario tenga permisos para acceder a la vista
        - @check("team_member_update"): Valida que el usuario tenga permisos para editar un miembro del equipo
        - @team_member_bp.route('/editar/<int:id>', methods=['POST']): Define la ruta para procesar el formulario
    Argumentos:
        - id: Identificador del miembro del equipo
    Retorna:
        - Caso 1: redirect(url_for('module_team_member.explore')):
        Redirige al usuario a la vista de exploración de miembros del equipo
        - Caso 2: render_template('team_member/edit.html',current_page='team_member', form=form, team_member=team_member):
        Renderiza la vista para editar un miembro del equipo
    """
    team_member = entities.get_team_member_by_id(id)

    if not team_member:
        flash("Miembro del equipo no encontrado.", "alert-danger")
        return redirect(url_for('module_team_member.explore'))

    form = TeamMemberForm()
    
    if form.validate_on_submit() and validators.validate_team_member_data_edit(form, id):
        files=request.files.getlist('documents')
        if form.documents.data:
            errors = validators.validate_documents(files)

            if errors:
                flash(" ".join(errors), "alert-danger")
                return render_template('team_member/edit.html',current_page='team_member' ,form=form, team_member=team_member)
            existing_documents = entities.get_documents_by_team_member_id(id)
            client = current_app.storage.client
            existing_names = {doc.name for doc in existing_documents}  # Nombres de documentos existentes
            for file in files:
                if secure_filename(file.filename) not in existing_names:
                    upload_document(file, team_member, client)
        entities.update_team_member(team_member,form)
        flash("Miembro del equipo actualizado con éxito.", "alert-success")
        return redirect(url_for('module_team_member.explore'))
    else:
        # Si hay errores, se regresa el formulario con los errores al usuario
        flash("Por favor, corrige los errores en el formulario.", "alert-danger")
        return render_template('team_member/edit.html',current_page='team_member' ,form=form, team_member=team_member)


@team_member_bp.route('/delete_document/<int:document_id>/<int:team_member_id>', methods=['POST'])
def delete_document(document_id,team_member_id):
    document = entities.get_document_by_id(document_id)  
    if not document:
        flash("Documento no encontrado.", "alert-danger")
        return redirect(url_for('module_team_member.edit', id=team_member_id))
    
    entities.delete_document(document)

    flash("Documento eliminado con éxito.", "alert-success")
    return redirect(url_for('module_team_member.edit_get', id=team_member_id))


@team_member_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@check("team_member_index")
@check("team_member_destroy")
def delete(id):
    """
    Función que elimina un miembro del equipo.
    Decoradores:
        - @login_required: Valida que el usuario haya iniciado sesión
        - @check("team_member_index"): Valida que el usuario tenga permisos para acceder a la vista
        - @check("team_member_destroy"): Valida que el usuario tenga permisos para eliminar un miembro del equipo
        - @team_member_bp.route('/eliminar/<int:id>', methods=['POST']): Define la ruta para procesar la eliminación
    Argumentos:
        - id: Identificador del miembro del equipo
    Retorna:
        - redirect(url_for('module_team_member.explore')):
        Redirige al usuario a la vista de exploración de miembros del equipo
    """
    team_member = entities.get_team_member_by_id(id)
    if team_member:
        entities.delete_team_member(team_member)
        flash(f"El miembro del equipo {
              id} se ha eliminado correctamente.", "alert-success")
    else:
        flash(
            "Ha ocurrido un error y no se ha podido realizar la operación.", "alert-danger")

    return redirect(url_for('module_team_member.explore'))
