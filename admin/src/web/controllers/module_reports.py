from collections import defaultdict
from flask import Blueprint, render_template, session, request, flash
from core.entities import count_scholarships_jya, legajos_in_debt, get_amount_spent, list_consultations, list_legajosJyA, list_miembros_equipo_active_paid, list_receipts
from web.handlers.auth import check, login_required
from datetime import date, datetime

import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import base64

matplotlib.use('Agg')

report_bp = Blueprint('module_report', __name__,
                      url_prefix="/module_report", template_folder='templates/report')


@report_bp.route('/', methods=['GET'])
@login_required
@check('report_index')
def report():
    """
    Descripción:
    Función que renderiza la vista de reportes y gráficos de la aplicación.

    Decoradores:
    - @login_required:
        Verifica si el usuario ha iniciado sesión.
    - @reports_bp.route('/report', methods=['GET']):
        Define la ruta para acceder a la vista de reportes.

    Retorna:
    - render_template('module_report.html', current_page='report', session=session):
        Retorna la vista de reportes de la aplicación.
    """

    filesJyA_in_debt = legajos_in_debt()

    personal = list_miembros_equipo_active_paid()

    start_date = request.args.get('start_date', None)

    end_date = request.args.get('end_date', None)

    errors = validate_date(start_date, end_date)

    amount = 0

    if not errors:
        amount = get_amount_spent(start_date, end_date)

    scholarship_true, scholarship_false = 0, 0
    scholarship_true, scholarship_false = get_scholarship_counts()
    scholarship_chart_url = create_scholarship_chart(
        scholarship_true, scholarship_false)

    payments_by_year = get_receipt_by_year()
    income_bar_chart_url = create_income_bar_chart(payments_by_year)

    consultations_by_month = get_consultations_by_month()
    consultations_line_chart_url = create_consultations_line_chart(
        consultations_by_month)

    return render_template('module_report.html', current_page='report', session=session, filesJyA_in_debt=filesJyA_in_debt, personal=personal, start_date=start_date, end_date=end_date, amount=amount, errors=errors, scholarship_chart_url=scholarship_chart_url, income_bar_chart_url=income_bar_chart_url, consultations_line_chart_url=consultations_line_chart_url)


def validate_date(from_date, to_date):
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


def create_scholarship_chart(scholarship_true, scholarship_false):
    labels = ['Becados', 'No Becados']
    sizes = [scholarship_true, scholarship_false]
    colors = ['#ff9999', '#66b3ff']

    if scholarship_true == 0 and scholarship_false == 0:
        return no_info_graph()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(sizes, labels=labels, colors=colors,
           autopct='%1.1f%%', startangle=90,  textprops={'fontsize': 20},
           wedgeprops={'linewidth': 1.0, 'edgecolor': 'white'})
    ax.axis('equal')
    plt.margins(0, 0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return chart_url


def get_scholarship_counts():
    return count_scholarships_jya()


def get_receipt_by_year():
    from collections import defaultdict

    receipt = list_receipts()
    receipt_by_year = defaultdict(int)

    for receipt in receipt:
        year = receipt.payment_date.year
        receipt_by_year[year] += receipt.amount

    return dict(receipt_by_year)


def create_income_bar_chart(receipts_by_year):
    if not receipts_by_year:
        return no_info_graph()

    years = list(receipts_by_year.keys())
    amounts = list(receipts_by_year.values())

    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.5
    ax.bar(years, amounts, color='blue', width=bar_width)
    ax.set_xlabel('Año', fontsize=20)
    ax.set_ylabel('Ingresos Totales', fontsize=20)
    ax.tick_params(axis='x', rotation=45, labelsize=20)
    ax.tick_params(axis='y', labelsize=20)

    ax.set_xticks(years)
    ax.set_xticklabels(years)

    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return chart_url


def get_consultations_by_month():
    consultations = list_consultations(True)
    consultations_by_month = defaultdict(int)

    for consultation in consultations:
        month = consultation.created_at.strftime('%Y-%m')
        consultations_by_month[month] += 1

    return consultations_by_month


def create_consultations_line_chart(consultations_by_month):
    months = sorted(consultations_by_month.keys())
    counts = [consultations_by_month[month] for month in months]

    if not months or not counts:
        return no_info_graph()

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(months, counts, marker='o', linestyle='-', color='blue')
    ax.set_xlabel('Mes', fontsize=20)
    ax.set_ylabel('Número de Consultas', fontsize=20)
    ax.tick_params(axis='x', rotation=45, labelsize=20)
    ax.tick_params(axis='y', labelsize=20)

    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return chart_url


def no_info_graph():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.text(0.5, 0.5, 'No hay datos disponibles', horizontalalignment='center',
            verticalalignment='center', fontsize=20, transform=ax.transAxes)
    ax.axis('off')

    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return chart_url
