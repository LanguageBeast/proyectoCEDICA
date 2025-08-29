from datetime import date
from flask import Blueprint, flash, redirect, request, session, url_for
from flask import render_template

from core.entities import assign_jya_type_to_equestrian, assign_team_member_to_equestrian, commit_equestrian, create_equestrian, create_provisional_ecuestrian, delete_equestrian, get_equestrian_by_id, get_permissions, list_equestrians, list_jya_types, list_miembros_equipo, logical_delete, remove_all_jya_type_from_equestrian, remove_all_team_member_from_equestrian, search_equestrians
from src.web.forms import EquestrianForm
from src.web.handlers.auth import check, login_required


# Variables globales para la paginación
queryResultEquestrians = []
total_pages = 0


# Blueprint para las funcionalidades de el modulo ecuestre
ecuestre_bp = Blueprint('module_ecuestre', __name__,
                        url_prefix="/module_ecuestre", template_folder='templates/ecuestre')

# Por alguna razón, module_ecuestre tiene que estar sí o sí en '/templates', y los subdirectorios pueden estar en
# '/templates/ecuestre'

# Routes para el modulo ecuestre


@ecuestre_bp.get('/')
@login_required
@check("equestrian_index")
def ecuestre():
    """
    Función que maneja la vista principal del módulo ecuestre.
    Decoradores:
        - @ecuestre_bp.route('/'): Define la ruta para acceder a la vista principal del módulo ecuestre.
        - @login_required: Requiere que el usuario esté autenticado para acceder a la vista.
        - @check("equestrian_index"): Requiere que el usuario tenga el permiso "equestrian_index" para acceder a la vista.
    Argumentos: Ninguno.
    Retorna:
        - render_template("module_equestrian.html", current_page='equestrian', session=session): 
        Renderiza la plantilla module_equestrian.html con el contexto de la sesión actual
    """
    global queryResultEquestrians
    queryResultEquestrians = []
    return render_template("module_equestrian.html", current_page='equestrian', session=session)


@ecuestre_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@check("equestrian_index")
@check("equestrian_destroy")
def delete(id):
    """
    Función que maneja la eliminación de un ecuestre.
    Decoradores:
        - @ecuestre_bp.route('/delete/<int:id>', methods=['POST']): Define la ruta para acceder a la vista de eliminación de un ecuestre.
        - @login_required: Requiere que el usuario esté autenticado para acceder a la vista.
        - @check("equestrian_index"): Requiere que el usuario tenga el permiso "equestrian_index" para acceder a la vista.
        - @check("equestrian_destroy"): Requiere que el usuario tenga el permiso "equestrian_destroy" para borrar un ecuestre.
    Argumentos:
        - id: Identificador del ecuestre a eliminar.
    Retorna:
        - redirect(url_for('module_ecuestre.explore', current_page='equestrian')): 
        Redirecciona a la vista de exploración de ecuestres.
    """
    # chequeo si se apreto el botón desde la vista de explorar
    if not request.referrer.endswith('explore'):
        flash(
            "Ha ocurrido un error y no se ha podido realizar la operación.", "alert-danger")
        return redirect(url_for('module_ecuestre', current_page='equestrian'))
    equestrian = get_equestrian_by_id(id)
    if equestrian:
        logical_delete(equestrian)
        # elimino el ecuestre en queryResultEquestrians
        global queryResultEquestrians
        queryResultEquestrians = [
            e for e in queryResultEquestrians if e.id != id]
        flash(f"El ecuestre {
              id} se ha eliminado correctamente.", "alert-success")
    else:
        flash(
            "Ha ocurrido un error y no se ha podido realizar la operación.", "alert-danger")
    return redirect(url_for('module_ecuestre.explore', current_page='equestrian'))


@ecuestre_bp.get('/upload')
@login_required
@check("equestrian_index")
@check("equestrian_new")
def upload():
    """
    Función que maneja la vista de subida de un nuevo ecuestre.
    Decoradores:
        - @ecuestre_bp.route('/upload'): Define la ruta para acceder a la vista de subida de un nuevo ecuestre.
        - @login_required: Requiere que el usuario esté autenticado para acceder a la vista.
        - @check("equestrian_index"): Requiere que el usuario tenga el permiso "equestrian_index" para acceder a la vista.
        - @check("equestrian_new"): Requiere que el usuario tenga el permiso "equestrian_new" para crear un ecuestre.
    Argumentos: Ninguno.
    Retorna:
        - render_template("ecuestre/upload.html", current_page='equestrian', form=equestrianForm, employees=employees, type_jya=type_jya): 
        Renderiza la plantilla upload.html con el contexto de la sesión actual, el formulario de subida de un nuevo ecuestre, la lista de empleados y la lista de tipos de JyA.
    """
    employees = list_miembros_equipo()
    type_jya = list_jya_types()
    equestrianForm = EquestrianForm()
    return render_template("ecuestre/upload.html", current_page='equestrian', form=equestrianForm, employees=employees, type_jya=type_jya)


@ecuestre_bp.post('/upload')
@login_required
@check("equestrian_index")
@check("equestrian_new")
def upload_post():
    """
    Función que maneja la subida de un nuevo ecuestre.
    Decoradores:
        - @ecuestre_bp.route('/upload', methods=['POST']): Define la ruta para subir un nuevo ecuestre.
        - @login_required: Requiere que el usuario esté autenticado para acceder a la vista.
        - @check("equestrian_index"): Requiere que el usuario tenga el permiso "equestrian_index" para acceder a la vista.
        - @check("equestrian_new"): Requiere que el usuario tenga el permiso "equestrian_new" para crear un ecuestre.
    Argumentos: Ninguno.
    Retorna:
        - redirect(url_for('module_ecuestre.upload', current_page='equestrian')):
        Redirecciona a la vista de subida de un nuevo ecuestre.
    """
    equestrianForm = EquestrianForm()
    if validate_equestrian(equestrianForm):
        add_equestrian(equestrianForm)
        flash("¡El ecuestre se ha registrado correctamente!", "alert-success")
        return redirect(url_for('module_ecuestre.upload', current_page='equestrian'))
    employees = list_miembros_equipo()
    type_jya = list_jya_types()
    return render_template("ecuestre/upload.html", current_page='equestrian', form=equestrianForm, employees=employees, type_jya=type_jya)


@ecuestre_bp.route('/explore', methods=['GET', 'POST'])
@login_required
@check("equestrian_index")
@check("equestrian_show")
def explore():
    """
    Función que maneja la vista de exploración de ecuestres.
    Decoradores:
        - @ecuestre_bp.route('/explore', methods=['GET', 'POST']): Define la ruta para acceder a la vista de exploración de ecuestres.
        - @login_required: Requiere que el usuario esté autenticado para acceder a la vista.
        - @check("equestrian_index"): Requiere que el usuario tenga el permiso "equestrian_index" para acceder a la vista.
        - @check("equestrian_show"): Requiere que el usuario tenga el permiso "equestrian_show" para ver los ecuestres.
    Argumentos: Ninguno.
    Retorna:
        - render_template("ecuestre/explore.html", current_page='equestrian', search_string="", items_on_page=sort_equestrians(items_on_page), total_pages=total_pages, page=page, filtersEquestrian=session.get('filtersEquestrian')):
        Renderiza la plantilla explore.html con el contexto de la sesión actual, la cadena de búsqueda, los elementos en la página, el total de páginas, la página actual y los filtros de ecuestres en la sesión.
    """
    global queryResultEquestrians
    global total_pages
    items_on_page = []
    end = 0
    per_page = 25
    items_on_page = []
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * per_page
    if request.method == 'GET':
        if (not queryResultEquestrians):
            queryResultEquestrians = list_equestrians()
            page = int(request.form.get('page', 1, type=int))
            start = (page-1) * per_page
            items_on_page, total_pages = paginate(
                queryResultEquestrians, page, per_page)
        else:
            end = start + per_page
            items_on_page = queryResultEquestrians[start:end]
        return render_template("ecuestre/explore.html", current_page='equestrian', search_string="", items_on_page=sort_equestrians(items_on_page), total_pages=total_pages, page=page, filtersEquestrian=session.get('filtersEquestrian'))

    elif request.method == 'POST':
        # obtener el search string y los filtros
        name_filter = request.form.get('name_filter')
        jya_filter = request.form.get('jya_filter')
        search_string = request.form.get('search_string')
        if validate_search_petition(name_filter, jya_filter, search_string):
            queryResultEquestrians = search_database(
                name_filter, jya_filter, search_string)
            if not queryResultEquestrians:
                flash("No se encontraron resultados.", "alert-warning")
            else:
                # pagino el resultado
                page = int(request.form.get('page', 1, type=int))
                start = (page-1) * per_page
                items_on_page, total_pages = paginate(
                    queryResultEquestrians, page, per_page)
        return render_template("ecuestre/explore.html", current_page='equestrian', search_string=search_string,  items_on_page=sort_equestrians(items_on_page), total_pages=total_pages, page=page, filtersEquestrian=session.get('filtersEquestrian'))


@ecuestre_bp.route('/edit/<int:id>', methods=['GET'])
@login_required
@check("equestrian_index")
def edit(id):
    """
    Función que maneja la vista de edición de un ecuestre.
    Decoradores:
        - @ecuestre_bp.route('/edit/<int:id>', methods=['GET']): Define la ruta para acceder a la vista de edición de un ecuestre.
        - @login_required: Requiere que el usuario esté autenticado para acceder a la vista.
        - @check("equestrian_index"): Requiere que el usuario tenga el permiso "equestrian_index" para acceder a la vista.
    Argumentos:
        - id: Identificador del ecuestre a editar.
    Retorna:
        - render_template("ecuestre/edit.html", current_page='equestrian', form=equestrianForm, id=id, employees=employees, type_jya=type_jya, related_employees=related_employees, related_jya_types=related_jya_types, user_permissions=user_permissions):
        Renderiza la plantilla edit.html con el contexto de la sesión actual, el formulario de edición de un ecuestre, el identificador del ecuestre a editar, la lista de empleados, la lista de tipos de JyA, los empleados relacionados y los tipos de JyA relacionados.
    """
    equestrian = get_equestrian_by_id(id)
    if not equestrian or equestrian.deleted:
        flash("¡El ecuestre no existe!", "alert-danger")
        return redirect(url_for('module_ecuestre.explore', current_page='equestrian'))
    employees = list_miembros_equipo()
    type_jya = list_jya_types()
    related_employees = equestrian.team_member
    related_jya_types = equestrian.jya_type
    equestrianForm = EquestrianForm()
    equestrianForm.name.data = equestrian.name
    equestrianForm.sex.data = equestrian.sex
    equestrianForm.breed.data = equestrian.breed
    equestrianForm.coat.data = equestrian.coat
    equestrianForm.purchase_or_donation.data = "purchase" if equestrian.is_purchase else "donation"
    equestrianForm.location.data = equestrian.location
    equestrianForm.birth_date.data = equestrian.birth_date
    equestrianForm.entry_date.data = equestrian.entry_date
    user_permissions = get_permissions(session.get('user'))

    return render_template("ecuestre/edit.html",
                           current_page='equestrian', form=equestrianForm, id=id, employees=employees, type_jya=type_jya, related_employees=related_employees, related_jya_types=related_jya_types, user_permissions=user_permissions)


@ecuestre_bp.route('/edit', methods=['POST'])
@ecuestre_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
@check("equestrian_index")
@check("equestrian_update")
def edit_equestrian(id):
    """
    Función que maneja la edición de un ecuestre.
    Decoradores:
        - @ecuestre_bp.route('/edit', methods=['POST']): Define la ruta para editar un ecuestre.
        - @ecuestre_bp.route('/edit/<int:id>', methods=['POST']): Define la ruta para editar un ecuestre.
        - @login_required: Requiere que el usuario esté autenticado para acceder a la vista.
        - @check("equestrian_index"): Requiere que el usuario tenga el permiso "equestrian_index" para acceder a la vista.
        - @check("equestrian_update"): Requiere que el usuario tenga el permiso "equestrian_update" para editar un ecuestre.
    Argumentos: 
        - id: Identificador del ecuestre a editar.
    Retorna:
        - redirect(url_for('module_ecuestre.edit', id=id, current_page='equestrian')):
        Redirecciona a la vista de edición de un ecuestre.
    """
    new_equestrian = EquestrianForm()
    if validate_equestrian(new_equestrian, True):
        modify_equestrian(id, new_equestrian)
        flash("¡El ecuestre se ha modificado correctamente!", "alert-success")
        return redirect(url_for('module_ecuestre.edit', id=id, current_page='equestrian'))
    else:
        flash("¡El ecuestre no se ha modificado!", "alert-danger")
        return redirect(url_for('module_ecuestre.edit', id=id, current_page='equestrian'))
# Funciones que implementan CRUD, usan los servicios de la entidad ECUESTRE desde el archivo __init__.py de entities o validan cosas


def validate_search_petition(name_filter, jya_filter, search_string):
    """
    Función que valida la petición de búsqueda de un ecuestre.
    Argumentos:
        - name_filter (str): Filtro de nombre.
        - jya_filter (str): Filtro de tipo de JyA.
        - search_string (str): Cadena de búsqueda.
    Retorna:
        - True: Si la petición de búsqueda es válida.
        - False: Si la petición de búsqueda no es válida.
    """
    # validaciones
    if not search_string:
        flash("No se puede buscar con el campo vacío.", "alert-danger")
        return False
    if name_filter and jya_filter:
        flash("No se puede buscar con 2 filtros a la vez.", "alert-danger")
        return False
    if search_string and not (name_filter or jya_filter):
        flash("No se puede buscar sin seleccionar un filtro.", "alert-danger")
        return False

    return True


def search_database(name_filter, jya_filter, search_string):
    """
    Función que busca un ecuestre en la base de datos.
    Argumentos:
        - name_filter (str): Filtro de nombre.
        - jya_filter (str): Filtro de tipo de JyA.
        - search_string (str): Cadena de búsqueda.
    Retorna: List<Equestrian>
    """
    return search_equestrians(name_filter, jya_filter, search_string)


def validate_equestrian(equestrianForm, modify=False):
    """
    Función que valida un formulario de ecuestre.
    Argumentos:
        - equestrianForm: Formulario de ecuestre.
        - modify (bool): Indica si se está modificando un ecuestre.
    Retorna:
        - True: Si el formulario es válido.
        - False: Si el formulario no es válido.
    """
    # validaciones base
    if not equestrianForm.validate_on_submit():

        return False
    # validaciones personalizadas
    birth_date = equestrianForm.birth_date.data
    entry_date = equestrianForm.entry_date.data
    if birth_date > entry_date:
        equestrianForm.birth_date.errors.append(
            "La fecha de nacimiento no puede ser mayor a la fecha de ingreso.")
        return False
    if birth_date > date.today():
        equestrianForm.birth_date.errors.append(
            "La fecha de nacimiento no puede ser mayor a la fecha actual.")
        return False
    if (not modify):
        # valido que haya seleccionado al menos un tipo de JyA
        jya_types = obtain_jya_types()
        if not jya_types:
            flash("Debe seleccionar al menos un tipo de JyA.", "alert-danger")
            redirect(url_for('module_ecuestre.upload',
                     current_page='equestrian'))
            return False
        # valido que se haya seleccionado al menos un empleado
        selected_employees = obtain_selected_employees()
        if not selected_employees:
            flash("Debe seleccionar al menos un empleado.", "alert-danger")
            redirect(url_for('module_ecuestre.upload',
                     current_page='equestrian'))
            return False
    return True


def add_equestrian(equestrianForm):
    """
    Función que añade un ecuestre a la base de datos (haciendo uso de servicios del módulo 'entities').
    Argumentos:
        - equestrianForm: Formulario de ecuestre.
    Retorna: commit_equestrian(equestrian)
    """
    name = equestrianForm.name.data
    sex = equestrianForm.sex.data
    breed = equestrianForm.breed.data
    coat = equestrianForm.coat.data
    purchase_or_donation = equestrianForm.purchase_or_donation.data
    if (purchase_or_donation == "purchase"):
        is_purchase = True
        is_donation = False
    else:
        is_purchase = False
        is_donation = True
    location = equestrianForm.location.data
    birth_date = equestrianForm.birth_date.data
    entry_date = equestrianForm.entry_date.data

    equestrian = create_provisional_ecuestrian(name=name, sex=sex, breed=breed, coat=coat, is_purchase=is_purchase,
                                               is_donation=is_donation, location=location, birth_date=birth_date,
                                               entry_date=entry_date)
    # agregar luego los documentos

    jya_types = obtain_jya_types()
    assign_jya_type_to_equestrian(equestrian, jya_types)
    selected_employees = obtain_selected_employees()
    assign_team_member_to_equestrian(equestrian, selected_employees)
    return commit_equestrian(equestrian)


def modify_equestrian(old_equestrian_id, new_equestrian_form):
    """
    Función que modifica un ecuestre en la base de datos (haciendo uso de servicios del módulo 'entities').
    Argumentos:
        - old_equestrian_id: Identificador del ecuestre a modificar.
        - new_equestrian_form: Formulario de ecuestre.
    Retorna: commit_equestrian(databaseEquestrian)
    """
    databaseEquestrian = get_equestrian_by_id(old_equestrian_id)
    # change all attributes
    databaseEquestrian.name = new_equestrian_form.name.data
    databaseEquestrian.sex = new_equestrian_form.sex.data
    databaseEquestrian.breed = new_equestrian_form.breed.data
    databaseEquestrian.coat = new_equestrian_form.coat.data
    databaseEquestrian.purchase_or_donation = new_equestrian_form.purchase_or_donation.data
    databaseEquestrian.location = new_equestrian_form.location.data
    databaseEquestrian.birth_date = new_equestrian_form.birth_date.data
    databaseEquestrian.entry_date = new_equestrian_form.entry_date.data
    # change related employees
    selected_employees = obtain_selected_employees()
    if (selected_employees):
        # first remove all previous employees
        remove_all_team_member_from_equestrian(
            databaseEquestrian)
        # then add the new ones
        assign_team_member_to_equestrian(
            databaseEquestrian, selected_employees)
    # change related jya types
    jya_types = obtain_jya_types()
    if (jya_types):
        # first remove all previous jya types
        remove_all_jya_type_from_equestrian(databaseEquestrian)
        # then add the new ones
        assign_jya_type_to_equestrian(databaseEquestrian, jya_types)

    # commit changes
    return commit_equestrian(databaseEquestrian)


def obtain_jya_types():
    """
    Función que obtiene los tipos de JyA seleccionados en el DOM.
    Argumentos: Ninguno.
    Retorna: List<JyaType>
    """
    return [request.form.get(f'jya_{i}') for i in range(
        1, 6) if request.form.get(f'jya_{i}') is not None]


def obtain_selected_employees():
    """
    Función que obtiene los empleados seleccionados en el DOM.
    Argumentos: Ninguno.
    Retorna: List<Employee>
    """
    # Get all form keys that match the pattern 'teammember_{id}'
    teammember_keys = [key for key in request.form.keys()
                       if key.startswith('teammember_')]

    # Iterate through the keys and get the values of the checked inputs
    teammember_ids = [key.replace('teammember_', '')
                      for key in teammember_keys if key.startswith('teammember_')]

    return teammember_ids


def sort_equestrians(items_on_page):
    """
    Función que ordena los ecuestres en la página, considerando los filtros elegidos en el DOM.
    Argumentos:
        - items_on_page: List<Equestrian>
    Retorna: items_on_page
    """
    # actualizo el dict filtersEquestrian en session
    if 'filtersEquestrian' not in session:
        session['filtersEquestrian'] = {}
    filtersEquestrian = session.get('filtersEquestrian')
    # Update filtersEquestrian with new or changed values from request
    order_by = request.args.get('orderBy')
    order_direction = request.args.get('orderDirection')

    if order_by:
        filtersEquestrian['orderBy'] = order_by
    if order_direction:
        filtersEquestrian['orderDirection'] = order_direction

    # obtengo todos los filtros desde el dict en session, si fueron seteados previamente
    order_by = session.get('filtersEquestrian').get('orderBy')
    order_direction = session.get('filtersEquestrian').get('orderDirection')

    # ordeno si existe o no el filtro
    if order_by:
        if order_by == 'name':
            items_on_page = sorted(
                items_on_page, key=lambda x: x.name)
        elif order_by == 'entry_date':
            items_on_page = sorted(
                items_on_page, key=lambda x: x.entry_date)
        elif order_by == 'birth_date':
            items_on_page = sorted(
                items_on_page, key=lambda x: x.birth_date)

    if order_direction:
        if order_direction == 'desc':
            items_on_page = items_on_page[::-1]
        elif order_direction == 'asc':
            pass

    return items_on_page


def paginate(query_results, page, per_page):
    """
    Función que pagina los resultados de una consulta.
    Argumentos:
        - query_results: List<Equestrian>
        - page: int
        - per_page: int
    Retorna: items_on_page (List<Equestrian>), total_pages (int)
    """
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(query_results) + per_page - 1) // per_page
    items_on_page = query_results[start:end]
    return items_on_page, total_pages
