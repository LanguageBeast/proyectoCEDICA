from datetime import datetime
from flask import Blueprint, flash, redirect, request, session, url_for, render_template
from src.web.handlers.auth import check, login_required
from src.web.forms import PaymentForm
from src.core.entities import get_team_member_by_id, assign_team_member_payment, assign_payment_type, get_payment_type_by_id, create_payment, list_miembros_equipo, list_payment_type, get_payments, get_payment_by_id, update_payment, delete_payment

# Se crea un Blueprint para agrupar las rutas relacionadas con el módulo de pagos
payment_bp = Blueprint(
    "module_payment",
    __name__,
    url_prefix="/module_payment",
    template_folder="templates/payment",
)


@payment_bp.get("/")
@login_required
@check("payment_index")
def payment():
    """
    Función que renderiza la plantilla de la página principal del módulo de pagos.
    Decoradores:
        - @payment_bp.get("/"): Define la ruta de la página principal del módulo de pagos.
        - @login_required: Requiere que el usuario esté autenticado para acceder a la vista.
        - @check("payment_index"): Requiere que el usuario tenga el permiso "payment_index" para acceder a la vista.
    Retorno:
        - render_template("module_payment.html", current_page="payment", session=session): 
        Renderiza la plantilla "module_payment.html" con la variable "current_page" igual a "payment" y la variable "session" igual a "session".
    """
    return render_template(
        "module_payment.html", current_page="payment", session=session
    )


@payment_bp.route("/upload", methods=("GET", "POST"))
@login_required
@check("payment_new")
def upload():
    """
    Función que permite subir un nuevo pago a la base de datos.
    Decoradores:
        - @payment_bp.route("/upload", methods=("GET", "POST")): Define la ruta de la página de subida de pagos.
        - @login_required: Requiere que el usuario esté autenticado para acceder a la vista.
        - @check("payment_new"): Requiere que el usuario tenga el permiso "payment_new" para explorar pagos.
    Atributos: Ninguno.
    Retorno:
        - render_template("payment/upload.html", title="Pagos", form=paymentForm, current_page="payment"):
        Renderiza la plantilla "payment/upload.html" con la variable "title" igual a "Pagos", la variable "form" igual a "paymentForm" 
        y la variable "current_page" igual a "payment".

    """
    paymentForm = PaymentForm()

    # Cargar tipos de pago desde la base de datos
    payment_types = list_payment_type()
    paymentForm.payment_type.choices = [
        (pt.id, pt.name) for pt in payment_types]
    paymentForm.payment_type.choices.insert(
        0, (0, '- Seleccione una opción -'))

    # Cargar miembros del equipo desde la base de datos
    team_members = list_miembros_equipo()
    paymentForm.team_member.choices = [(tm.id, tm.dni) for tm in team_members]
    paymentForm.team_member.choices.insert(0, (0, '- Seleccione DNI -'))

    if paymentForm.validate_on_submit() and validate_payment_data(paymentForm):
        payment_type = paymentForm.payment_type.data
        pm = create_payment(
            amount=paymentForm.amount.data,
            payment_date=paymentForm.payment_date.data,
            description=paymentForm.description.data,
        )
        assign_payment_type(pm, get_payment_type_by_id(payment_type))

        team_member = (
            get_team_member_by_id(paymentForm.team_member.data)
            if paymentForm.team_member.data != 0
            else None
        )
        assign_team_member_payment(pm, team_member)
        flash("¡El pago se ha registrado correctamente!", "alert-success")
        return redirect(url_for("module_payment.payment", current_page="payment"))
    return render_template(
        "payment/upload.html", title="Pagos", form=paymentForm, current_page="payment"
    )


@payment_bp.route("/explore", methods=("GET", "POST"))
@login_required
@check("payment_show")
def explore():
    """
    Función que permite explorar los pagos registrados en la base de datos.
    Decoradores:
        - @payment_bp.route("/explore", methods=("GET", "POST")): Define la ruta de la página de exploración de pagos.
        - @login_required: Requiere que el usuario esté autenticado para acceder a la vista.
        - @check("payment_show"): Requiere que el usuario tenga el permiso "payment_show" para explorar pagos.
    Atributos: Ninguno.
    Retorno: 
        - render_template("payment/explore.html", title="Pagos", current_page="payment", payments=payments, page=page, total_pages=total_pages, order_direction=order_direction, order_by=order_by, filter=filter, payment_type_s=payment_type, start_date=start_date, end_date=end_date):
        Renderiza la plantilla "payment/explore.html" con variables de información y paginado.
    """
    page = request.args.get('page', 1, type=int)  # Obtener el número de página
    per_page = 25

    # Obtener ordenamiento
    # Ordenar por el campo elegido, o created_at por defecto
    order_by = request.args.get('order_by', 'created_at')
    # 'asc' por defecto, 'desc' si se especifica
    order_direction = request.args.get('order_direction', 'asc')

    # Obtener filtro de búsqueda
    filter = request.form.get(
        'filter') if request.method == 'POST' else request.args.get('filter')
    # Obtener el tipo de pago
    payment_type = request.form.get(
        'payment_type_s') if request.method == 'POST' else request.args.get('payment_type_s')
    # Obtener fecha de inicio
    start_date = request.form.get(
        'start_date') if request.method == 'POST' else request.args.get('start_date')
    # Obtener fecha de fin
    end_date = request.form.get(
        'end_date') if request.method == 'POST' else request.args.get('end_date')

    if filter == 'payment_date':
        if not (validate_start_date(start_date) and validate_end_date(start_date, end_date)):
            return redirect(url_for('module_payment.explore', page=page, title="Pagos", order_direction=order_direction, order_by=order_by, filter=filter, payment_type_s=payment_type, start_date=start_date, end_date=end_date))

    # Llamar a la función para obtener los pagos con ordenamiento
    payments, total_pages = get_payments(
        page, per_page, filter, start_date, end_date, payment_type, order_by, order_direction)
    if not payments:
        flash('No se encontraron resultados.', 'alert-warning')

    return render_template("payment/explore.html", title="Pagos", current_page="payment", payments=payments, page=page, total_pages=total_pages, order_direction=order_direction, order_by=order_by, filter=filter, payment_type_s=payment_type, start_date=start_date, end_date=end_date)


@payment_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@check("payment_update")
def edit(id):
    """
    Función que permite editar un pago registrado en la base de datos.
    Decoradores:
        - @payment_bp.route('/editar/<int:id>', methods=['GET', 'POST']): Define la ruta de la página de edición de pagos.
        - @login_required: Requiere que el usuario esté autenticado para acceder a la vista.
        - @check("payment_update"): Requiere que el usuario tenga el permiso "payment_update" para editar un pago.
    Atributos:
        - id: Identificador del pago a editar.
    Retorno:
        - render_template('payment/edit.html', form=form, payment=payment):
        Renderiza la plantilla "payment/edit.html" con el formulario de edición y los datos del pago a editar.
    """
    # Obtener el pago por su id
    payment = get_payment_by_id(id)

    if not payment:
        flash("Pago no encontrado.", "alert-danger")
        return redirect(url_for('module_payment.explore'))

    # Crear una instancia del formulario con los datos actuales del pago
    form = PaymentForm(obj=payment)

    # Cargar tipos de pago desde la base de datos
    payment_types = list_payment_type()
    form.payment_type.choices = [(pt.id, pt.name) for pt in payment_types]
    form.payment_type.choices.insert(0, (0, '- Seleccione una opción -'))

    # Cargar miembros del equipo desde la base de datos
    team_members = list_miembros_equipo()
    form.team_member.choices = [(tm.id, tm.dni) for tm in team_members]
    form.team_member.choices.insert(0, (0, '- Seleccione DNI -'))

    # Preseleccionar campos
    if request.method == 'GET':
        form.payment_type.data = payment.payment_type_id
        form.team_member.data = payment.team_member_id

    if form.validate_on_submit() and validate_payment_data(form):
        payment_type = form.payment_type.data
        pm = update_payment(payment, form)
        assign_payment_type(pm, get_payment_type_by_id(payment_type))
        team_member = (
            get_team_member_by_id(form.team_member.data)
            if form.team_member.data != 0
            else None
        )
        assign_team_member_payment(pm, team_member)

        flash("¡El pago se ha actualizado correctamente!", "alert-success")
        return redirect(url_for('module_payment.explore'))

    # Renderizar la plantilla con el formulario y los datos actuales del pago
    return render_template('payment/edit.html', form=form, payment=payment)


@payment_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@check("payment_destroy")
def delete(id):
    """
    Función que permite eliminar un pago registrado en la base de datos.
    Decoradores:
        - @payment_bp.route('/eliminar/<int:id>', methods=['POST']): Define la ruta de eliminación de pagos.
        - @login_required: Requiere que el usuario esté autenticado para acceder a la vista.
        - @check("payment_destroy"): Requiere que el usuario tenga el permiso "payment_destroy" para eliminar un pago.
    Atributos:
        - id: Identificador del pago a eliminar.
    Retorno:
        - redirect(url_for('module_payment.explore')):
        Redirecciona a la vista de exploración de pagos.
    """
    payment = get_payment_by_id(id)
    if payment:
        delete_payment(payment)
        flash(f"El pago nº {
              id} se ha eliminado correctamente.", "alert-success")
    else:
        flash(
            "Ha ocurrido un error y no se ha podido realizar la operación.", "alert-danger")

    return redirect(url_for('module_payment.explore'))


# Función para validar los datos del formulario
def validate_payment_data(form):
    """
    Función que valida los datos del formulario de pagos.
    Atributos:
        - form: Formulario de pagos.
    Retorno:
        - True: Si los datos son válidos.
        - False: Si los datos no son válidos.
    """

    # Validar fecha de pago
    if not validate_payment_date(form.payment_date):
        return False

    # Validar monto
    if not validate_amount(form.amount):
        return False

    # Validar que el tipo de pago sea válido
    # if not validate_options(form.payment_type, ['Honorarios', 'Proveedor', 'Gastos varios']):
    #     return False

    return True


# Validar que la opción sea válida
# def validate_options(field, valid_options):
#     if field.data.lower() not in valid_options:
#         field.errors.append(f"Opción inválida: {field.}. Debe ser una de: {', '.join(valid_options)}.")
#         return False
    # return True


# Validar monto
def validate_amount(amount):
    """
    Función que valida el monto ingresado en el formulario de pagos.
    Atributos:
        - amount (int): Monto ingresado en el formulario.
    Retorno:
        - True: Si el monto es válido.
        - False: Si el monto no es válido
    """
    try:
        value = float(amount.data)
        if value <= 0:
            amount.errors.append("El monto debe ser un número mayor que cero.")
            return False
    except ValueError:
        # Si falla la conversión a float, no es un número válido
        amount.errors.append("El monto debe ser un número válido.")
        return False
    # Si todas las validaciones pasan, devolver True
    return True


# Validar que la fecha de pago no sea mayor a la fecha actual
def validate_payment_date(payment_date):
    """
    Función que valida que la fecha de pago no sea mayor a la fecha actual.
    Atributos:
        - payment_date (datetime): Fecha de pago ingresada en el formulario.
    Retorno:
        - True: Si la fecha de pago es válida.
        - False: Si la fecha de pago no es válida.
    """
    if payment_date.data > datetime.today().date():
        payment_date.errors.append(
            "La fecha de pago no puede ser mayor a la fecha actual.")
        return False
    return True


# Validar que la fecha de inicio no sea mayor a la fecha actual
def validate_start_date(start_d):
    """
    Función que valida que la fecha de inicio no sea mayor a la fecha actual.
    Atributos:
        - start_d (datetime): Fecha de inicio ingresada en el formulario.
    Retorno:
        - True: Si la fecha de inicio es válida.
        - False: Si la fecha de inicio no es válida.
    """
    start_date = datetime.strptime(start_d, "%Y-%m-%d")
    if start_date > datetime.today():
        flash("La fecha de inicio no puede ser mayor a la fecha actual.", "alert-danger")
        return False
    return True


# Validar que la fecha de fin no sea mayor a la fecha actual y que no sea anterior a la fecha de inicio
def validate_end_date(start_d, end_d):
    """
    Función que valida que la fecha de fin no sea mayor a la fecha actual y que no sea anterior a la fecha de inicio.
    Atributos:
        - start_d (datetime): Fecha de inicio ingresada en el formulario.
        - end_d (datetime): Fecha de fin ingresada en el formulario.
    Retorno:
        - True: Si la fecha de fin es válida.
        - False: Si la fecha de fin
    """
    start_date = datetime.strptime(start_d, "%Y-%m-%d")
    end_date = datetime.strptime(end_d, "%Y-%m-%d")
    if end_date > datetime.today():
        flash("La fecha de fin no puede ser mayor a la fecha actual.", "alert-danger")
        return False
    if start_date > end_date:
        flash("La fecha de fin no puede ser anterior a la fecha de inicio.", "alert-danger")
        return False
    return True
