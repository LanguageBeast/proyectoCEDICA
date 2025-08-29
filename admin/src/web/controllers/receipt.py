from flask import Blueprint
from flask import render_template, url_for, redirect, flash, request, session
from src.core.entities import (get_receipt_by_id,
                               delete_receipt,
                               order_receipts,
                               search_receipts,
                               list_miembros_equipo_not_eliminated,
                               list_legajosJyA,
                               modify_receipt,
                               add_receipt)
from src.web.forms import ReceiptForm
from datetime import date, datetime
from src.web.handlers.auth import check, login_required

# Blueprint para las funcionalidades del modulo de cobros

queryResult = []
total_pages = 0
per_page = 25

receipt_bp = Blueprint('module_receipt', __name__,
                       url_prefix="/module_receipt")


@receipt_bp.get('/')
@login_required
@check("receipt_index")
def receipt():
    """
    Función que renderiza la página principal del módulo de cobros.
    Decoradores:
        - @login_required: Requiere que el usuario esté autenticado.
        - @check("receipt_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @receipt_bp.get('/'): Define la ruta para acceder a la vista.
    Atributos: Ninguno
    Retorna:
        - render_template("module_receipt.html",current_page='receipt'): Renderiza la vista del módulo de cobros.
    """
    return render_template("module_receipt.html", current_page='receipt')

# Funcionalidades para INDEX


@receipt_bp.route('/explore', methods=['GET'])
@login_required
@check("receipt_index")
@check("receipt_show")
def explore():
    """
    Función que renderiza la vista de exploración de registros de cobros.
    Decoradores:
        - @login_required: Requiere que el usuario esté autenticado.
        - @check("receipt_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @receipt_bp.route('/explore', methods=['GET']): Define la ruta para acceder a la vista.
    Atributos: Ninguno
    Retorna:
        - render_template("receipt/explore.html", current_page='receipt', items_on_page=items_on_page, total_pages=total_pages, 
        page=page, errors=errors, filters=filters): 
        Renderiza la vista de exploración de registros de cobros.
    """
    global queryResult, total_pages, per_page
    page = request.args.get('page', 1, type=int)
    items_on_page = []

    # Resetear filtros si `reset=1`
    if request.args.get('reset', 0, type=int) == 1:
        session.pop('query_filters', None)
        queryResult = None
        total_pages = 0

    # Obtener filtros de búsqueda de la solicitud GET
    filters = {
        'team_member_name': request.args.get('team_member_name', ''),
        'team_member_surname': request.args.get('team_member_surname', ''),
        'payment_method': request.args.get('payment_method', ''),
        'start_date': request.args.get('start_date', ''),
        'end_date': request.args.get('end_date', '')
    }

    errors = validateReceipt(
        filters['start_date'] or None, filters['end_date'] or None)

    # Guardar filtros válidos en la sesión si no hay errores
    if not errors:
        session['query_filters'] = filters
        queryResult = search_receipts(**filters)
        if not queryResult:
            flash("No se encontraron resultados.", "alert-warning")
        else:
            total_pages = (queryResult.count() + per_page - 1) // per_page
    else:
        filters = session.get('query_filters', {})

    aux_query = order_receipts(
        queryResult, order_by_date=request.args.get('orderDirection'))
    start = (page - 1) * per_page
    items_on_page = aux_query[start:start + per_page] if queryResult else []

    return render_template(
        "receipt/explore.html", current_page='receipt',
        items_on_page=items_on_page, total_pages=total_pages,
        page=page, errors=errors, filters=filters
    )


def validateReceipt(from_date, to_date):
    """
    Función que valida los filtros de búsqueda de registros de cobros.
    Argumentos:
        - from_date (date): Fecha de inicio de la búsqueda.
        - to_date (date): Fecha de fin de la búsqueda.
    Retorna:
        - errors (dict): Diccionario con los errores de valid
    """
    # Valida que los filtros sean validos
    errors = {}
    if from_date:
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        if from_date > date.today():
            errors["from_date"] = "La fecha desde no puede ser mayor que la fecha actual."
            flash("La fecha desde no puede ser mayor que la fecha actual.",
                  "alert-danger")
    if to_date:
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        if to_date > date.today():
            errors["to_date"] = "La fecha hasta no puede ser mayor que la fecha actual."
    if to_date and from_date:
        if from_date > to_date:
            errors["from_date"] = "La fecha desde no puede ser mayor que la fecha hasta."
            flash("La fecha desde no puede ser mayor que la fecha hasta.",
                  "alert-danger")
    return errors


# Funcionalidades para SHOW, UPDATE

@receipt_bp.route('/edit/<int:id>', methods=['GET'])
@login_required
@check("receipt_index")
@check("receipt_show")
def edit(id):
    """
    Función que renderiza la vista de edición de un registro de cobro.
    Decoradores:
        - @login_required: Requiere que el usuario esté autenticado.
        - @check("receipt_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @check("receipt_show"): Requiere que el usuario tenga permisos para explorar los recibos.
        - @receipt_bp.route('/edit/<int:id>', methods=['GET']): Define la ruta para acceder a la vista.
    Atributos:
        - id (int): Identificador del registro de cobro a editar.
    Retorna:
        - render_template("receipt/edit.html", current_page='receipt', form=receiptForm, id=id, current_team_member=current_team_member, 
        current_fileJyA=current_fileJyA, fileJyAs=fileJyAs, team_members=team_members):
        Renderiza la vista de edición de un registro de cob
    """
    fileJyAs = list_legajosJyA()
    team_members = list_miembros_equipo_not_eliminated()

    receipt = get_receipt_by_id(id)
    current_team_member = receipt.team_member
    current_fileJyA = receipt.fileJyA
    receiptForm = ReceiptForm()
    receiptForm.payment_date.data = receipt.payment_date
    receiptForm.payment_method.data = receipt.payment_method
    receiptForm.amount.data = receipt.amount
    receiptForm.notes.data = receipt.notes

    return render_template("receipt/edit.html",
                           current_page='receipt', form=receiptForm, id=id, current_team_member=current_team_member, current_fileJyA=current_fileJyA, fileJyAs=fileJyAs, team_members=team_members)


@receipt_bp.route('/edit', methods=['POST'])
@receipt_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
@check("receipt_index")
@check("receipt_show")
@check("receipt_update")
def edit_receipt(id):
    """
    Función que modifica un registro de cobro.
    Decoradores:
        - @login_required: Requiere que el usuario esté autenticado.
        - @check("receipt_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @check("receipt_show"): Requiere que el usuario tenga permisos para explorar los recibos.
        - @check("receipt_update"): Requiere que el usuario tenga permisos para modificar los recibos.
        - @receipt_bp.route('/edit', methods=['POST']): Define la ruta para acceder a la vista.
        - @receipt_bp.route('/edit/<int:id>', methods=['POST']): Define la ruta para acceder a la vista.
    Atributos:
        - id (int): Identificador del registro de cobro a modificar.
    Retorna:
        - redirect(url_for('module_receipt.edit', id=id)): 
        Redirecciona a la vista de edición del registro de cobro.
    """
    newReceipt = ReceiptForm()
    if validateReceiptAdd(newReceipt, True):
        modify_receipt(id, newReceipt, obtain_team_member(), obtain_file_JyA())
        flash("¡El Registro de Cobro se ha modificado correctamente!", "alert-success")
        return redirect(url_for('module_receipt.edit', id=id))
    else:
        flash("¡El Registro de Cobro no se ha modificado!", "alert-danger")
        return redirect(url_for('module_receipt.edit', id=id))


# Funcionalidades para DESTROY


@receipt_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@check("receipt_index")
@check("receipt_destroy")
def delete(id):
    """
    Función que elimina un registro de cobro.
    Decoradores:
        - @login_required: Requiere que el usuario esté autenticado.
        - @check("receipt_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @check("receipt_destroy"): Requiere que el usuario tenga permisos para eliminar los recibos.
        - @receipt_bp.route('/delete/<int:id>', methods=['POST']): Define la ruta para acceder a la vista.
    Atributos:
        - id (int): Identificador del registro de cobro a eliminar.
    Retorna:
        - redirect(url_for('module_receipt.explore')): 
        Redirecciona a la vista de exploración de registros de cobros.
    """
    # chequeo si se apreto el botón desde la vista de explorar
    global total_pages
    if 'explore' not in request.referrer:
        flash(
            "Ha ocurrido un error y no se ha podido realizar la operación.", "alert-danger")
        return redirect(url_for('module_receipt.explore'))
    receipt = get_receipt_by_id(id)
    if receipt:
        delete_receipt(receipt)
        # elimino el receipt en queryResult
        global queryResult
        for e in queryResult:
            if e.id == id:
                queryResult.remove(e)
        total_pages = (queryResult.count() + per_page - 1) // per_page
        flash(f"El Registro de Cobro {
              id} se ha eliminado correctamente.", "alert-success")
    else:
        flash(
            "Ha ocurrido un error y no se ha podido realizar la operación.", "alert-danger")
    return redirect(url_for('module_receipt.explore'))

# Funcionalidades para CREATE


@receipt_bp.get('/upload')
@login_required
@check("receipt_index")
@check("receipt_new")
def upload():
    """
    Función que renderiza la vista de creación de un registro de cobro.
    Decoradores:
        - @login_required: Requiere que el usuario esté autenticado.
        - @check("receipt_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @check("receipt_new"): Requiere que el usuario tenga permisos para crear los recibos.
        - @receipt_bp.get('/upload'): Define la ruta para acceder a la vista.
    Atributos: Ninguno
    Retorna:
        - render_template("receipt/upload.html", current_page='receipt', form=receipt_form, team_members=team_members, fileJyAs=fileJyAs, 
        current_team_member=None, current_fileJyA=None): 
        Renderiza la vista de creación de un registro de cobro.
    """
    fileJyAs = list_legajosJyA()
    team_members = list_miembros_equipo_not_eliminated()

    receipt_form = ReceiptForm()
    return render_template("receipt/upload.html", current_page='receipt', form=receipt_form, team_members=team_members, fileJyAs=fileJyAs, current_team_member=None, current_fileJyA=None)


@receipt_bp.post('/upload')
@login_required
@check("receipt_index")
@check("receipt_new")
def upload_post():
    """
    Función que crea un registro de cobro.
    Decoradores:
        - @login_required: Requiere que el usuario esté autenticado.
        - @check("receipt_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @check("receipt_new"): Requiere que el usuario tenga permisos para crear los recibos.
        - @receipt_bp.post('/upload'): Define la ruta para acceder a la vista.
    Atributos: Ninguno
    Retorna:
        - redirect(url_for('module_receipt.upload', current_page='receipt')): 
        Redirecciona a la vista de creación de un registro de cobro.
    """
    receipt_form = ReceiptForm()

    if validateReceiptAdd(receipt_form, False):
        add_receipt(receipt_form, obtain_team_member(), obtain_file_JyA())
        flash("¡El registro de cobro se ha registrado correctamente!", "alert-success")
        return redirect(url_for('module_receipt.upload', current_page='receipt'))

    current_team_member = obtain_team_member()
    current_fileJyA = obtain_file_JyA()

    fileJyAs = list_legajosJyA()
    team_members = list_miembros_equipo_not_eliminated()
    # Devuelve el formulario en caso de error
    return render_template("receipt/upload.html", current_page='receipt', form=receipt_form, team_members=team_members, fileJyAs=fileJyAs, current_team_member=current_team_member, current_fileJyA=current_fileJyA)


def obtain_team_member():
    """
    Función que obtiene el miembro de equipo seleccionado en el formulario.
    Argumentos: Ninguno
    Retorna:
        - nombre del miembro de equipo seleccionado en el formulario (str).
    """
    return request.form.get('team_member')


def obtain_file_JyA():
    """
    Función que obtiene el jinete o amazona seleccionado en el formulario.
    Argumentos: Ninguno
    Retorna:
        - nombre del jinete o amazona seleccionado en el formulario (str).
    """
    return request.form.get('fileJyA')


def validateReceiptAdd(receiptForm, mod):
    """
    Función que valida los datos de un registro de cobro.
    Argumentos:
        - receiptForm (ReceiptForm): Formulario con los datos del registro de cobro.
        - mod (bool): Indica si se está modificando un registro de cobro.
    Retorna:
        - True si los datos son válidos, False en caso contrario.
        - False si los datos no son válidos.
    """

    if not receiptForm.validate_on_submit():
        return False

    if receiptForm.payment_date.data > date.today():
        receiptForm.payment_date.errors.append(
            "La fecha de pago no puede ser mayor que la fecha actual.")
        flash("La fecha de pago no puede ser mayor que la fecha actual.", "alert-danger")
        return False

    if (not mod):
        if (obtain_team_member() is None):
            flash("Debes seleccionar un miembro de equipo!", "alert-danger")
            return False

        if (obtain_file_JyA() is None):
            flash("Debes seleccionar un jinete o amazona!", "alert-danger")
            return False

    return True
