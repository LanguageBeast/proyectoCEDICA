from datetime import date
from flask import Blueprint, flash, redirect, request, session, url_for
from flask import render_template

from core.entities import commit_consultation, get_consultation_by_id, get_permissions, list_consultations, logical_delete, search_consultations
from src.web.handlers.auth import check, login_required
from web.forms import ConsultationForm

# Variables globales para la paginación
queryResultConsultations = []
total_pages = 0


# Blueprint para las funcionalidades del modulo consulta
consultation_bp = Blueprint('module_consultation', __name__,
                            url_prefix="/module_consultation", template_folder='templates/consultation')

# Routes para el modulo de consulta


@consultation_bp.get('/')
@login_required
@check("consultation_index")
def consultation():
    """
    Descripción:
    Función que renderiza la vista principal de la gestión de consultas.

    Decoradores:
    - @consultation_bp.get('/')
        Define la ruta de la vista principal de la gestión de consultas.
    - @login_required
        Verifica si el usuario ha iniciado sesión.
    - @check("consultation_index")
        Verifica si el usuario tiene permisos para acceder a la vista.

    Argumentos: Ninguno.
    Retorna:
    - render_template('module_consultation.html', current_page='consultation', session=session)
        Renderiza la vista principal de la gestión de consultas.
    """
    global queryResultConsultations
    queryResultConsultations = []
    return render_template('module_consultation.html', current_page='consultation', session=session)


@consultation_bp.route('/edit/<int:id>', methods=['GET'])
@login_required
@check("consultation_index")
def edit(id):
    """
    Descripción:
    Función que renderiza la vista de edición de una consulta.

    Decoradores:
    - @consultation_bp.route('/edit/<int:id>', methods=['GET'])
        Define la ruta de la vista de edición de una consulta.
    - @login_required
        Verifica si el usuario ha iniciado sesión.
    - @check("consultation_index")
        Verifica si el usuario tiene permisos para acceder a la vista.

    Argumentos:
    - id: int
        Identificador de la consulta a editar.
    Retorna:
    - render_template('edit_consultation.html', current_page='consultation', session=session, consultation=consulta)
        Renderiza la vista de edición de una consulta.
    """
    consulta = get_consultation_by_id(id)
    if not consulta:
        flash("¡La consulta no existe!", "alert-danger")
        return redirect(url_for('module_consultation.explore, current_page=consultation'))
    consultation_form = ConsultationForm()
    consultation_form.full_name.data = consulta.full_name
    consultation_form.email.data = consulta.email
    consultation_form.message.data = consulta.message
    consultation_form.captcha.data = consulta.captcha
    consultation_form.status.data = consulta.status
    consultation_form.comment.data = consulta.comment

    user_permissions = get_permissions(session.get('user'))

    return render_template('consultation/edit.html', current_page='consultation', form=consultation_form, id=id, user_permissions=user_permissions)


@consultation_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
@check("consultation_index")
@check("consultation_update")
def update(id):
    """
    Descripción:
    Función que actualiza los datos de una consulta.

    Decoradores:
    - @consultation_bp.route('/update/<int:id>', methods=['POST'])
        Define la ruta de actualización de una consulta.
    - @login_required
        Verifica si el usuario ha iniciado sesión.
    - @check("consultation_index")
        Verifica si el usuario tiene permisos para acceder a la vista.
    - @check("consultation_update")
        Verifica si el usuario tiene permisos para actualizar una consulta.

    Argumentos:
    - id: int
        Identificador de la consulta a actualizar.
    Retorna:
    - redirect(url_for('module_consultation.explore'))
        Redirecciona a la vista de exploración de consultas.
    """
    new_consulta = ConsultationForm()
    if validate_consultation(new_consulta):
        modify_consultation(id, new_consulta)
        flash("¡La consulta se ha actualizado correctamente!", "alert-success")
    else:
        flash("¡La consulta no se ha podido actualizar!", "alert-danger")
    return redirect(url_for('module_consultation.edit', id=id, current_page='equestrian'))


@consultation_bp.route('/explore', methods=['GET', 'POST'])
@login_required
@check("consultation_index")
@check("consultation_show")
def explore():
    """
    Descripción:
    Función que renderiza la vista de exploración de consultas.

    Decoradores:
    - @consultation_bp.get('/explore')
        Define la ruta de la vista de exploración de consultas.
    - @login_required
        Verifica si el usuario ha iniciado sesión.
    - @check("consultation_index")
        Verifica si el usuario tiene permisos para acceder a la vista.
    - @check("consultation_explore")
        Verifica si el usuario tiene permisos para explorar consultas.

    Argumentos: Ninguno.
    Retorna:
    - render_template('explore_consultation.html', current_page='consultation', session=session)
        Renderiza la vista de exploración de consultas.
    """
    global queryResultConsultations
    global total_pages
    items_on_page = []
    end = 0
    per_page = 25
    items_on_page = []
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * per_page

    if request.method == 'GET':
        if (not queryResultConsultations):
            queryResultConsultations = list_consultations()
            page = int(request.form.get('page', 1, type=int))
            start = (page-1) * per_page
            items_on_page, total_pages = paginate(
                queryResultConsultations, page, per_page)
        else:
            end = start + per_page
            items_on_page = queryResultConsultations[start:end]
        return render_template('consultation/explore.html', current_page='consultation', search_string="", items_on_page=sort_consultations(items_on_page), total_pages=total_pages, page=page, filtersConsultations=session.get('filtersConsultations'))

    elif request.method == 'POST':
        search_string = request.form.get('search_string')
        status_pending_filter = request.form.get('status_pending')
        status_in_progress_filter = request.form.get('status_in_progress')
        status_discarded_filter = request.form.get('status_discarded')
        status_solved = request.form.get('status_solved')
        if validate_search_petition(search_string, status_pending_filter, status_in_progress_filter, status_discarded_filter, status_solved):
            queryResultConsultations = search_database(
                search_string, status_pending_filter, status_in_progress_filter, status_discarded_filter, status_solved)
            if not queryResultConsultations:
                flash("No se encontraron resultados", "alert-danger")
            else:
                page = int(request.form.get('page', 1, type=int))
                start = (page-1) * per_page
                items_on_page, total_pages = paginate(
                    queryResultConsultations, page, per_page)
        return render_template('consultation/explore.html', current_page='consultation', search_string=search_string, items_on_page=sort_consultations(items_on_page), total_pages=total_pages, page=page, filtersConsultations=session.get('filtersConsultations'))


@consultation_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@check("consultation_index")
@check("consultation_destroy")
def delete(id):
    """
    Función que maneja la eliminación de una consulta.
    Decoradores:
    - @consultation_bp.route('/delete/<int:id>', methods=['POST'])
        Define la ruta para eliminar una consulta.
    - @login_required
        Verifica si el usuario ha iniciado sesión.
    - @check("consultation_index")
        Verifica si el usuario tiene permisos para acceder a la vista.
    - @check("consultation_destroy")    
        Verifica si el usuario tiene permisos para eliminar una consulta.
    Argumentos:
    - id: int
        Identificador de la consulta a eliminar.
    Retorna:
    - redirect(url_for('module_consultation.explore'))
        Redirecciona a la vista de exploración de consultas.
    """

    if 'module_consultation/explore' not in request.referrer:
        flash(
            "Ha ocurrido un error y no se ha podido realizar la operación", "alert-danger")
        return redirect(url_for('module_consultation.explore', current_page='consultation'))
    consulta = get_consultation_by_id(id)
    if consulta:
        logical_delete(consulta)
        global queryResultConsultations
        queryResultConsultations = [
            x for x in queryResultConsultations if x.id != id]
        flash(f"La consulta {
              id} se ha eliminado correctamente.", "alert-success")
    else:
        flash(
            "Ha ocurrido un error y no se ha podido realizar la operación.", "alert-danger")
    return redirect(url_for('module_consultation.explore', current_page='consultation'))


def paginate(query_results, page, per_page):
    """
    Función que pagina los resultados de una consulta.
    Argumentos:
        - query_results: List<Consultation>
        - page: int
        - per_page: int
    Retorna: items_on_page (List<Consultation>), total_pages (int)
    """
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(query_results) + per_page - 1) // per_page
    items_on_page = query_results[start:end]
    return items_on_page, total_pages


def sort_consultations(items_on_page):
    """
    Función que ordena las consultas por fecha de creación.
    Argumentos:
        - consultations: List<Consultation>
    Retorna: List<Consultation>
    """
    if 'filtersConsultations' not in session:
        session['filtersConsultations'] = {}
    filtersConsultations = session.get('filtersConsultations')
    order_by = request.args.get('orderBy')
    order_direction = request.args.get('orderDirection')
    if order_by:
        filtersConsultations['orderBy'] = order_by
    else:
        session['filtersConsultations'].pop('orderBy', None)
    if order_direction:
        filtersConsultations['orderDirection'] = order_direction

    order_by = session.get('filtersConsultations').get('orderBy')
    order_direction = session.get('filtersConsultations').get('orderDirection')

    if order_by:
        if order_by == 'created_at':
            items_on_page = sorted(
                items_on_page, key=lambda x: x.created_at, reverse=order_direction == 'desc')

    if order_direction:
        if order_direction == 'desc':
            items_on_page = items_on_page[::-1]
        else:
            pass
    return items_on_page


def validate_search_petition(search_string, status_pending_filter, status_in_progress_filter, status_discarded_filter, status_solved):
    """
    Función que valida los datos ingresados en el formulario de búsqueda de consultas.
    Argumentos:
        - search_string: str
        - status_pending_filter: str
        - status_in_progress_filter: str
        - status_discarded_filter: str
        - status_solved: str
    Retorna: bool
    """
    # por ahora nada
    return True


def search_database(search_string, status_pending_filter, status_in_progress_filter, status_discarded_filter, status_solved):
    """
    Función que realiza una búsqueda en la base de datos de consultas.
    Argumentos:
        - search_string: str
        - status_pending_filter: str
        - status_in_progress_filter: str
        - status_discarded_filter: str
        - status_solved: str
    Retorna: List<Consultation>
    """
    return search_consultations(search_string, status_pending_filter, status_in_progress_filter, status_discarded_filter, status_solved)


def validate_consultation(consulta):
    """
    Función que valida los datos ingresados en el formulario de consulta.
    Argumentos:
        - consulta: ConsultationForm
    Retorna: bool
    """
    if consulta.validate_on_submit():
        return True
    return False


def modify_consultation(id, new_consulta):
    """
    Función que modifica una consulta.
    Argumentos:
        - id: int
        - new_consulta: ConsultationForm
    Retorna: Consultation
    """
    consulta = get_consultation_by_id(id)
    if consulta:
        consulta.full_name = new_consulta.full_name.data
        consulta.email = new_consulta.email.data
        consulta.message = new_consulta.message.data
        consulta.captcha = new_consulta.captcha.data
        consulta.status = new_consulta.status.data
        consulta.comment = new_consulta.comment.data
    return commit_consultation(consulta)
