from flask import Blueprint, flash, redirect, request, session, url_for
from flask import render_template
from core.entities import assign_user_role_with_roleid_filled_in, commit_user, create_provisional_user, delete_user, encrypt_user_password, get_user_by_email, get_user_by_dni, get_user_by_id, list_users, logical_delete, reattach_to_session, search_users
from src.web.forms import UserForm
from src.web.handlers.auth import check, login_required
from core import entities

# Blueprint para las funcionalidades del modulo usuarios
users_bp = Blueprint("module_users", __name__,
                     url_prefix="/modulo_usuarios", template_folder='templates/ecuestre')

# Variables globales para la paginación
queryResultUsers = []
total_pages = 0


@users_bp.route("/", methods=["GET"])
@login_required
@check("users_index")
def users():
    """
    Función que renderiza la vista principal del módulo de usuarios.
    Decoradores:
        - @login_required: Requiere que el usuario esté logueado.
        - @check("users_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @users_bp.route("/", methods=["GET"]): Define la ruta de la vista.
    Atributos: Ninguno
    Retorna:
        - render_template("module_users.html", current_page='users', session=session): 
        Renderiza la vista principal del módulo de usuarios.
    """
    global queryResultUsers
    queryResultUsers = []
    return render_template("module_users.html", current_page='users', session=session)


@users_bp.route("/upload", methods=["GET"])
@login_required
@check("users_index")
@check("users_new")
def upload():
    """
    Función que renderiza la vista de carga de usuarios.
    Decoradores:
        - @login_required: Requiere que el usuario esté logueado.
        - @check("users_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @check("users_new"): Requiere que el usuario tenga permisos para crear un usuario.
        - @users_bp.route("/upload", methods=["GET"]): Define la ruta de la vista.
    Atributos: Ninguno
    Retorna:
        - render_template("users/upload.html", current_page='users', session=session, form=userForm): 
        Renderiza la vista de carga de usuarios.
    """
    userForm = UserForm()
    return render_template("users/upload.html", current_page='users', session=session, form=userForm)


@users_bp.route("/upload", methods=["POST"])
@login_required
@check("users_index")
@check("users_new")
def upload_user():
    """
    Función que se encarga de cargar un usuario en la base de datos.
    Decoradores:
        - @login_required: Requiere que el usuario esté logueado.
        - @check("users_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @check("users_new"): Requiere que el usuario tenga permisos para crear un usuario.
        - @users_bp.route("/upload", methods=["POST"]): Define la ruta de la vista.
    Atributos: Ninguno
    Retorna:
        - redirect(url_for('module_users.upload', current_page='users')): 
        Redirecciona a la vista de carga de usuarios.
    """
    userForm = UserForm()
    if validate_user(userForm):
        add_user(userForm)
        flash("¡El usuario se ha registrado correctamente!", "alert-success")
        return redirect(url_for('module_users.upload', current_page='users'))
    return render_template("users/upload.html", current_page='users', session=session, form=userForm)


@users_bp.route("/explore", methods=["GET", "POST"])
@login_required
@check("users_index")
@check("users_show")
def explore():
    """
    Función que renderiza la vista de exploración de usuarios.
    Decoradores:
        - @login_required: Requiere que el usuario esté logueado.
        - @check("users_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @check("users_show"): Requiere que el usuario tenga permisos para mostrar los usuarios.
        - @users_bp.route("/explore", methods=["GET", "POST"]): Define la ruta de la vista.
    Atributos: Ninguno
    Retorna:
        - render_template("users/explore.html", current_page='users', items_on_page=sort_users(items_on_page), total_pages=total_pages, 
        page=page, filtersUsers=session.get('filtersUsers')): 
        Renderiza la vista de exploración de usuarios.
    """
    global queryResultUsers
    global total_pages
    end = 0
    per_page = 25
    items_on_page = []
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * per_page
    if request.method == 'GET':
        if (not queryResultUsers):
            queryResultUsers = list_users()
            page = int(request.form.get('page', 1, type=int))
            start = (page-1) * per_page
            items_on_page, total_pages = paginate(
                queryResultUsers, page, per_page)
        else:
            end = start + per_page
            items_on_page = queryResultUsers[start:end]
        return render_template("users/explore.html", current_page='users', items_on_page=sort_users(items_on_page), total_pages=total_pages, page=page, filtersUsers=session.get('filtersUsers'))

    elif request.method == 'POST':
        email_filter = request.form.get('email_filter')
        active_filter = request.form.get('active_filter')
        role_filter = request.form.get('role_filter')
        search_string = request.form.get('search_string')
        if validateSearchPetition(email_filter, active_filter, role_filter, search_string):
            queryResultUsers = search_database(
                email_filter, active_filter, role_filter, search_string)
            if not queryResultUsers:
                flash("No se encontraron resultados.", "alert-danger")
            else:
                page = int(request.form.get('page', 1, type=int))
                start = (page-1) * per_page
                items_on_page, total_pages = paginate(
                    queryResultUsers, page, per_page)

        return render_template("users/explore.html", current_page='users', items_on_page=sort_users(items_on_page), total_pages=total_pages, page=page, filtersUsers=session.get('filtersUsers'))


@users_bp.route("/edit/<int:id>", methods=["GET"])
@login_required
@check("users_index")
def edit(id):
    """
    Función que renderiza la vista de edición de un usuario.
    Decoradores:
        - @login_required: Requiere que el usuario esté logueado.
        - @check("users_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @users_bp.route("/edit/<int:id>", methods=["GET"]): Define la ruta de la vista.
    Atributos:
        - id: Identificador del usuario a editar.
    Retorna:
        - render_template("users/edit.html", current_page='users', id=id, form=userForm):
        Renderiza la vista de edición de un usuario.
    """
    # obtengo todos los datos del usuario
    user = get_user_by_id(id)
    if not user or user.deleted:
        flash("No se ha encontrado el usuario.", "alert-danger")
        return redirect(url_for('module_users.explore', current_page='users'))
    user_role_id = user.role.id
    userForm = UserForm()
    userForm.email.data = user.email
    userForm.dni.data = user.dni
    userForm.alias.data = user.alias
    userForm.password.data = user.password
    userForm.isEnabled.data = 'yes' if user.is_enabled else 'no'
    if user_role_id == 2:
        userForm.role.data = 'administration'
    elif user_role_id == 3:
        userForm.role.data = 'equestrian'
    elif user_role_id == 4:
        userForm.role.data = 'technical'
    elif user_role_id == 5:
        userForm.role.data = 'volunteer'

    return render_template("users/edit.html", current_page='users', id=id, form=userForm)


@users_bp.route("/edit/<int:id>", methods=["POST"])
@login_required
@check("users_index")
@check("users_update")
def edit_user(id):
    """
    Función que se encarga de modificar un usuario en la base de datos.
    Decoradores:
        - @login_required: Requiere que el usuario esté logueado.
        - @check("users_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @check("users_update"): Requiere que el usuario tenga permisos para modificar un usuario.
        - @users_bp.route("/edit/<int:id>", methods=["POST"]): Define la ruta de la vista.
    Atributos:
        - id: Identificador del usuario a modificar.
    Retorna:
        - redirect(url_for('module_users.edit', id=id, current_page='users')):
        Redirecciona a la vista de edición de un usuario.
    """
    new_user = UserForm()
    previous_user = get_user_by_id(id)
    if validate_user_modify(previous_user, new_user):
        modify_user(previous_user, new_user)
        flash("¡El usuario se ha modificado correctamente!", "alert-success")
        return redirect(url_for('module_users.edit', id=id, current_page='users'))
    else:
        flash("¡No se ha podido modificar el usuario!", "alert-danger")
        return redirect(url_for('module_users.edit', id=id, current_page='users'))


@users_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
@check("users_index")
@check("users_destroy")
def delete(id):
    """
    Función que se encarga de eliminar un usuario de la base de datos.
    Decoradores:
        - @login_required: Requiere que el usuario esté logueado.
        - @check("users_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @check("users_destroy"): Requiere que el usuario tenga permisos para eliminar un usuario.
        - @users_bp.route("/delete/<int:id>", methods=["POST"]): Define la ruta de la vista.
    Atributos:
        - id: Identificador del usuario a eliminar.
    Retorna:
        - redirect(url_for('module_users.explore', current_page='users')):
        Redirecciona a la vista de exploración de usuarios.
    """
    if not request.referrer.endswith('explore'):
        flash(
            "Ha ocurrido un error y no se ha podido realizar la operación.", "alert-danger")
        return redirect(url_for('module_users.explore', current_page='users'))
    users = list_users()
    user = get_user_by_id(id)
    if user:
        logical_delete(user)
        if (user.member):
            logical_delete(user.member)
        global queryResultUsers
        queryResultUsers = [x for x in queryResultUsers if x.id != id]
        flash("¡El usuario se ha eliminado correctamente!", "alert-success")
    else:
        flash(
            "Ha ocurrido un error y no se ha podido realizar la operación.", "alert-danger")
    return redirect(url_for('module_users.explore', current_page='users'))



@users_bp.route("/profile", methods=["GET"])
@login_required
@check("users_show")
def profile():
    """
    Función que renderiza la vista de perfil de usuario.
    Decoradores:
        - @login_required: Requiere que el usuario esté logueado.
        - @users_bp.get("/profile", methods=["GET"]): Define la ruta de la vista.
    Atributos: Ninguno
    Retorna:
        - render_template("users/profile.html", current_page='users', session=session): 
        Renderiza la vista de perfil de usuario.
    """
    user = get_user_by_email(session.get('user'))
    return render_template("users/profile.html", current_page='users', user=user)


# Funciones que implementan CRUD, usan los servicios de la entidad USUARIO desde el archivo __init__.py de entities o validan cosas


def validate_user(userForm):
    """
    Función que se encarga de validar los datos de un usuario.
    Atributos:
        - userForm: Formulario con los datos del usuario.
    Retorna:
        - True: Si los datos del usuario son válidos.
        - False: Si los datos del usuario no son válidos.
    """
    # validaciones base
    if not userForm.validate_on_submit():
        return False

    # validaciones personalizadas
    # valido que el email no esté repetido
    email = userForm.email.data
    dni = userForm.dni.data
    fetchedUser = get_user_by_email(email)
    if fetchedUser:
        userForm.email.errors.append(
            "El email ya se encuentra registrado.")
        return False
    fetchedDniUser = get_user_by_dni(dni)
    if fetchedDniUser:
        userForm.dni.errors.append(
            "El dni ya se encuentra registrado.")
        return False
    return True


def validate_user_modify(previous_user, new_userForm):
    """
    Función que se encarga de validar los datos de un usuario a modificar.
    Atributos:
        - previous_user User: Usuario a modificar.
        - new_userForm: Formulario con los datos del usuario a modificar.
    Retorna:
        - True: Si los datos del usuario a modificar son válidos.
        - False: Si los datos del usuario a modificar no son válidos.
    """
    if not (new_userForm.password.data):
        password_field = new_userForm.password
        del new_userForm.password
    if not new_userForm.validate_on_submit():
        return False
    # checkeo si el email y/o el dni cambiaron
    if previous_user.email != new_userForm.email.data:
        fetchedUser = get_user_by_email(new_userForm.email.data)
        if fetchedUser:
            new_userForm.email.errors.append(
                "El email ya se encuentra registrado.")
            return False
    if previous_user.dni != new_userForm.dni.data:
        fetchedDniUser = get_user_by_dni(new_userForm.dni.data)
        if fetchedDniUser:
            new_userForm.dni.errors.append(
                "El dni ya se encuentra registrado.")
            return False
    if not (new_userForm.password):
        new_userForm.password = password_field
    return True


def modify_user(previous_user, userForm):
    """
    Función que se encarga de modificar un usuario en la base de datos (con servicios de 'entities').
    Atributos:
        - previous_user User: Usuario a modificar.
        - userForm: Formulario con los datos del usuario a modificar.
    Retorna:
        - commit_user(previous_user): Usuario modificado.
    """
    previous_user.email = userForm.email.data
    previous_user.dni = userForm.dni.data
    previous_user.alias = userForm.alias.data
    if (userForm.password.data):
        previous_user.password = userForm.password.data
    if userForm.isEnabled.data == 'yes':
        previous_user.is_enabled = True
    else:
        previous_user.is_enabled = False
    roleChosen = userForm.role.data
    if roleChosen == 'administration':
        previous_user.role_id = 2
    elif roleChosen == 'equestrian':
        previous_user.role_id = 3
    elif roleChosen == 'technical':
        previous_user.role_id = 4
    elif roleChosen == 'volunteer':
        previous_user.role_id = 5

    # asigno nuevo rol
    assign_user_role_with_roleid_filled_in(previous_user)
    # encripto contraseña
    if (userForm.password.data):
        encrypt_user_password(previous_user)

    # me fijo si existe un miembro de equipo con el mismo dni, y lo asigno al usuario
    member = entities.get_member_by_dni(previous_user.dni)
    if member:
        previous_user.member = member
    
    return commit_user(previous_user)


def add_user(userForm):
    """
    Función que se encarga de agregar un usuario en la base de datos (con servicios de 'entities').
    Atributos:
        - userForm: Formulario con los datos del usuario a agregar.
    Retorna:
        - commit_user(user): Usuario agregado.
    """
    email = userForm.email.data
    dni = userForm.dni.data
    alias = userForm.alias.data
    password = userForm.password.data
    if userForm.isEnabled.data == 'yes':
        is_enabled = True
    else:
        is_enabled = False
    roleChosen = userForm.role.data
    if roleChosen == 'administration':
        role_id = 2
    elif roleChosen == 'equestrian':
        role_id = 3
    elif roleChosen == 'technical':
        role_id = 4
    elif roleChosen == 'volunteer':
        role_id = 5
    user = create_provisional_user(
        email=email, dni=dni, alias=alias, password=password, is_enabled=is_enabled, role_id=role_id)

    # asigno rol
    assign_user_role_with_roleid_filled_in(user)
    # me fijo si existe un miembro de equipo con el mismo dni, y lo asigno al usuario
    member = entities.get_member_by_dni(dni)
    if member:
        user.member = member
    return commit_user(user)


def sort_users(items_on_page):
    """
    Función que se encarga de ordenar los usuarios en la vista de exploración.
    Atributos:
        - items_on_page: Usuarios a ordenar.
    Retorna:
        - items_on_page: Usuarios ordenados.
    """
    # actualizo el dict filtersUsers en session
    if 'filtersUsers' not in session:
        session['filtersUsers'] = {}
    filtersUsers = session.get('filtersUsers')
    # actualizo el dict filtersUsers en session
    order_by = request.args.get('orderBy')
    order_direction = request.args.get('orderDirection')

    if order_by:
        filtersUsers['orderBy'] = order_by
    if order_direction:
        filtersUsers['orderDirection'] = order_direction

    order_by = session.get('filtersUsers').get('orderBy')
    order_direction = session.get('filtersUsers').get('orderDirection')

    if order_by:
        if order_by == 'email':
            items_on_page = sorted(items_on_page, key=lambda x: x.email)
        elif order_by == 'created_at':
            items_on_page = sorted(items_on_page, key=lambda x: x.created_at)

    if order_direction:
        if order_direction == 'desc':
            items_on_page = items_on_page[::-1]
        elif order_direction == 'asc':
            pass

    reattach_to_session(items_on_page)
    return items_on_page


def validateSearchPetition(email_filter, active_filter, role_filter, search_string):
    """
    Función que se encarga de validar una petición de búsqueda de usuarios.
    Atributos:
        - email_filter (str): Filtro de búsqueda por email.
        - active_filter (str): Filtro de búsqueda por estado.
        - role_filter (str): Filtro de búsqueda por rol.
        - search_string (str): Cadena de búsqueda.
    Retorna:
        - True: Si la petición de búsqueda es válida.
        - False: Si la petición de búsqueda no es válida.
    """
    # validaciones base
    if not search_string:
        flash("No se puede buscar con el campo vacío.", "alert-danger")
        return False
    # validar si se eligió 2 o más filtros a la misma vez
    if email_filter and active_filter and role_filter:
        flash("No se puede buscar con 3 filtros a la vez.", "alert-danger")
        return False
    if (email_filter and active_filter) or (email_filter and role_filter) or (active_filter and role_filter):
        flash("No se puede buscar con 2 filtros a la vez.", "alert-danger")
        return False
    if search_string and not (email_filter or active_filter or role_filter):
        flash("Debe seleccionar al menos un filtro.", "alert-danger")
        return False
    return True


def search_database(email_filter, active_filter, role_filter, search_string):
    """
    Función que se encarga de buscar usuarios en la base de datos.
    Atributos:
        - email_filter (str): Filtro de búsqueda por email.
        - active_filter (str): Filtro de búsqueda por estado.
        - role_filter (str): Filtro de búsqueda por rol.
        - search_string (str): Cadena de búsqueda.
    Retorna:
        - search_users(email_filter, active_filter, role_filter, search_string): Usuarios encontrados.
    """
    # si se seleccionó el filtro de email
    return search_users(email_filter, active_filter, role_filter, search_string)


def paginate(query_results, page, per_page):
    """
    Función que se encarga de paginar los resultados de la búsqueda.
    Atributos:
        - query_results List<User>: Resultados de la búsqueda.
        - page int: Página actual.
        - per_page int: Cantidad de resultados por página.
    Retorna:
        - items_on_page List<User>: Resultados paginados.
        - total_pages int: Cantidad total de páginas.
    """
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(query_results) + per_page - 1) // per_page
    items_on_page = query_results[start:end]
    return items_on_page, total_pages
