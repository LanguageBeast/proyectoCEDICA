from flask import Blueprint, request, jsonify
import re
from src.core.entities import create_consultation
from src.web.schemas.consultant import create_consultant_schema, consultant_schema


api_consultant_blueprint = Blueprint(
    "consultant_api", __name__, url_prefix="/api/consultant"
)

# dump: convierte objeto a json. Cuando se hace un response (para afuera)
# load: convierte json a objeto. Cuando se recibe un request (de afuera)

@api_consultant_blueprint.post("/")
def create():
    data = request.get_json()
    errors = create_consultant_schema.validate(data)

    if errors:
        return jsonify(errors), 400
    
    if data.get("captcha") != "equinoterapia":
        return jsonify({"error": "captcha inválido"}), 400
    
    # mapear los datos del json a los atributos del objeto Consultant.
    kwargs = create_consultant_schema.load(data)
    # crear la consulta en la base de datos.
    new_consultant = create_consultation(**kwargs)
    # devolver la consulta creada en el response, solo para ver el resultado.
    data = consultant_schema.dump(new_consultant)
    return jsonify(data), 200
