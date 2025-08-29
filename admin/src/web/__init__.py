from flask import Flask, render_template
from core.entities import get_role, get_documents_by_team_member_id
from src.core import database
from src.core import seeds
from src.core.bcrypt import bcrypt
from src.core.config import config
from src.web.handlers import error
from src.web.handlers.auth import is_authenticated
from src.web.handlers.auth import check_permission
from core.entities import truncate_message
from web.controllers.module_equestrian import ecuestre_bp
from web.controllers.module_team_member import team_member_bp
from web.controllers.module_jya import jya_bp
from web.controllers.user import user_bp
from src.web.controllers.module_users import users_bp
from src.web.controllers.auth import auth_bp
from src.web.controllers.receipt import receipt_bp
from src.web.controllers.module_payment import payment_bp
from src.web.api.module_content import api_content_bp
from src.web.controllers.module_content import content_bp
from src.web.controllers.module_consultation import consultation_bp
from src.web.controllers.module_reports import report_bp
from src.web.api.consultant import api_consultant_blueprint
from flask_session import Session
from src.web.storage import storage
from flask_cors import CORS
import logging
from src.web.oauth import configure_oauth
from src.web import file_handlers

session = Session()

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    @app.get("/")
    def home():
        return render_template("home.html", current_page="home")

    # Carga de la configuración
    app.config.from_object(config[env])

    # Inicializa OAuth con la aplicación
    configure_oauth(app)

    # Inicialización de la base de datos
    database.init_app(app)

    # Registro de los blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(ecuestre_bp)
    app.register_blueprint(team_member_bp)
    app.register_blueprint(jya_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(receipt_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(api_content_bp)
    app.register_blueprint(consultation_bp)
    app.register_blueprint(report_bp)

    # Registro de los blueprints de la API
    app.register_blueprint(api_consultant_blueprint)

    # Registro de los manejadores de errores
    app.register_error_handler(404, error.not_found_error)
    app.register_error_handler(401, error.unauthorized)
    app.register_error_handler(403, error.forbidden)

    # Inicialización de la sesión
    session.init_app(app)

    # Inicialización de bcrypt
    bcrypt.init_app(app)

    # Inicialización de Minio
    storage.init_app(app)

    # Inicialización de CORS
    CORS(app, resources=r"/api/*")

    # Registra funciones en Jinja
    app.jinja_env.globals.update(is_authenticated=is_authenticated)
    app.jinja_env.globals.update(check_permission=check_permission)
    app.jinja_env.globals.update(get_role=get_role)
    app.jinja_env.globals.update(document_url=file_handlers.document_url)
    app.jinja_env.globals.update(get_documents=get_documents_by_team_member_id)
    app.jinja_env.globals.update(truncate_message=truncate_message)
    
    # Registro de comandos CLI
    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()

    @app.cli.command(name="seeds-jya-types")
    def seeds_jya_types():
        seeds.build_jya_types()

    @app.cli.command(name="seeds-doc-jya-types")
    def seeds_jya_types():
        seeds.build_doc_jya_types()

    @app.cli.command(name="seeds-employees")
    def seeds_employees():
        seeds.build_two_employees()
        
    @app.cli.command(name="seeds-contents")
    def build_contents():
        seeds.build_contents()

    return app
