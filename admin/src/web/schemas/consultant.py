from marshmallow import Schema, fields


class ConsultantSchema(Schema):
    # dump_only: para indicar que no lo voy a querer setear desde un request.
    id = fields.Int(dump_only=True)
    full_name = fields.Str(required=True, validate=lambda x: len(x) <= 100)
    email = fields.Email(required=True)
    message = fields.Str(required=True)
    status = fields.Str(dump_only=True)
    captcha = fields.Str(required=True, load_only=True)


consultant_schema = ConsultantSchema(only=("full_name", "email", "message", "status"))
# consultants_schema = ConsultantSchema(many=True)
create_consultant_schema = ConsultantSchema(only=("full_name", "email", "message", "captcha"))
