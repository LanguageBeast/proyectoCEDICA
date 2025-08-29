from datetime import datetime
from flask import request, jsonify
from flask import Blueprint
from src.web.schemas.content_post import contents_schema
from src.core import entities
from src.core.validators import validate_author,validate_date_not_in_the_future,validate_start_date_before_end_date
api_content_bp = Blueprint('content_api_bp', __name__,url_prefix="/api/module_content")
@api_content_bp.get("/")
def index():
    """
    Endpoint para obtener una lista paginada de contenidos con filtros opcionales.

    Parámetros de consulta:
    - page (int, opcional): Número de página para la paginación (valor predeterminado: 1).
    - per_page (int, opcional): Cantidad de elementos por página (valor predeterminado: 3).
    - start_date (str, opcional): Fecha de inicio en formato 'YYYY-MM-DD' para filtrar los contenidos.
    - end_date (str, opcional): Fecha de fin en formato 'YYYY-MM-DD' para filtrar los contenidos.
    - author (str, opcional): Nombre o alias del autor para filtrar los contenidos.

    Validaciones:
    - Las fechas (start_date y end_date) deben estar en el formato 'YYYY-MM-DD'.
    - Las fechas no pueden ser posteriores a la fecha actual.
    - La fecha de inicio (start_date) no puede ser posterior a la fecha de fin (end_date).
    - El nombre o alias del autor (author) solo puede contener caracteres alfabéticos y espacios.

    Flujo de la función:
    1. Se extraen los parámetros de consulta.
    2. Se validan las fechas y el autor.
    3. Si los filtros son válidos, se consultan los contenidos según los criterios.
    4. Se devuelve una respuesta con los contenidos, la paginación y el total de elementos.

    Respuesta:
    - Código HTTP 200:
        {
            "data": [<lista de contenidos serializados>],
            "page": <número de página>,
            "total": <total de contenidos disponibles>,
            "per_page": <cantidad de contenidos por página>
        }
    - Código HTTP 400 (si hay errores en la validación):
        {
            "error": <mensaje de error>
        }

    Retorna:
    - Response (JSON): Respuesta serializada con los contenidos o un mensaje de error.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 3, type=int)
    start_date = request.args.get('start_date', type=str)
    end_date = request.args.get('end_date', type=str)
    author = request.args.get('author', type=str)

    filters = {}
    try:
        if start_date:
            filters['start_date'] = datetime.strptime(start_date, '%Y-%m-%d')
            if not validate_date_not_in_the_future(filters['start_date']):
                return jsonify({"error": "la fecha de inicio no puede ser posterior a la fecha de hoy."}), 400
        if end_date:
            filters['end_date'] = datetime.strptime(end_date, '%Y-%m-%d')
            if not validate_date_not_in_the_future(filters['end_date']):
                return jsonify({"error": "la fecha de fin no puede ser posterior a la fecha de hoy."}), 400
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Use 'YYYY-MM-DD'."}), 400
    if author:
        if not validate_author(author):
            return jsonify({"error": "solo se deben ingresar caracteres."}), 400
        filters['author'] = author
    if start_date and end_date:
        if not validate_start_date_before_end_date(filters['start_date'],filters['end_date']):
            return jsonify({"error": "la fecha de inicio no puede ser posterior a la fecha de fin."}), 400

    contents, total = entities.get_paginated_contents(page=page, per_page=per_page, filters=filters)
    
    data = contents_schema.dump(contents)
    
    response = {
        "data": data,
        "page": page,
        "total": total,
        "per_page":per_page,
    }
    return jsonify(response), 200
