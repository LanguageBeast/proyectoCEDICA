from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    session,
)
from src.core.entities import check_user, get_user_by_email, create_user, get_role_by_name
from src.web.handlers.auth import is_authenticated
from src.web.forms import LoginForm
from src.web.oauth import oauth
import secrets, uuid, random

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=("GET", "POST"))
@auth_bp.route("/", methods=("GET", "POST"))
def login():
    """
    Función que maneja la vista de login.
    Decoradores:
        - @auth_bp.route("/login", methods=("GET", "POST")): Define la ruta para acceder a la vista de login.
        - @auth_bp.route("/", methods=("GET", "POST")): Define la ruta para acceder a la vista de login.
    Argumentos: Ninguno.
    Retorna:
        - render_template("login.html", title="Login", form=form): Retorna la vista de login con el formulario de login.
    """
    if is_authenticated(session):
        flash("La sesión se encuentra iniciada.", "alert-info")
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = check_user(form.email.data, form.password.data)
        if user and user.is_enabled and not user.deleted:
            next_page = request.args.get("next")
            flash("¡La sesión se inició correctamente!", "alert-success")
            session["user"] = user.email
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Usuario o contraseña incorrecta.", "alert-danger")
    return render_template("login.html", title="Login", form=form, current_page='login')


@auth_bp.route("/login/google")
def google_login():
    nonce = secrets.token_urlsafe(16)  # Genera un nonce único
    session["oauth_nonce"] = nonce

    redirect_uri = url_for("auth.google_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)


@auth_bp.route("/google/callback")
def google_callback():
    """
    Callback de google para el login y registro de usuario con Google. Al registrarse genera un UUID como password.
    Decoradores:
        - @auth_bp.route("/google/callback"): Define la ruta de regreso a la aplicación para continuar la ejecución.
    Argumentos: Ninguno.
    """

    token = oauth.google.authorize_access_token()

    # Recupera el nonce de la sesión
    nonce = session.get("oauth_nonce")
    user_info = oauth.google.parse_id_token(token, nonce)

    if user_info:
        user_email = user_info["email"].lower()
        user = get_user_by_email(user_email)
        if user and user.is_enabled and not user.deleted:
            session["user"] = user_email
            flash("¡Sesión iniciada con Google!", "alert-success")
            return redirect(url_for("home"))
        
        if user and not user.is_enabled:
            flash("La cuenta se encuentra pendiente de aprobación por el Administrador del sitio.", "alert-primary")
            return redirect(url_for("auth.login"))
        
        random_password = str(uuid.uuid4())
        random_dni = str(random.randint(10000000, 99999999))
        default_role_id = get_role_by_name("No asignado")
        # Extrae información del usuario desde 'user_info'
        new_user = create_user(
            email=user_email,
            alias=user_info.get("name", "Usuario Desconocido"),
            is_enabled=False,
            dni=random_dni,
            password=random_password,
            role_id=default_role_id,
        )
        flash("¡Usuario registrado! Podrá acceder al sistema luego que el Administrador apruebe la creación de la cuenta.", "alert-primary")
        return redirect(url_for("auth.login"))
        
    else:
        flash("Error en la autenticación con Google.", "alert-danger")
        return redirect(url_for("auth.login"))


@auth_bp.route("/logout")
def logout():
    """
    Función que maneja la vista de logout.
    Decoradores:
        - @auth_bp.route("/logout"): Define la ruta para cerrar la sesión.
    Argumentos: Ninguno.
    Retorna:
        - redirect(url_for("home")): Redirige a la página principal.
    """
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("¡La sesión se cerró correctamente!", "alert-info")
    else:
        flash("No hay ninguna sesión activa", "alert-danger")

    return redirect(url_for("home"))
