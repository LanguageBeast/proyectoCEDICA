from flask import Blueprint
from flask import render_template
from flask import Flask, redirect, url_for


# Blueprint para las funcionalidades del usuario
user_bp = Blueprint("user", __name__, url_prefix="/usuario")


@user_bp.route("/perfil")
def perfil():
    """
    Función que renderiza la plantilla de perfil del usuario
    Decoradores:
        - @user_bp.route("/perfil"): Indica la ruta de la página
    Retorna:
        - render_template("profile.html"): 
        Renderiza la plantilla de perfil del usuario
    """
    return render_template("profile.html")


@user_bp.route("/logout")
def logout():
    """
    Función que redirige a la página principal
    Decoradores:
        - @user_bp.route("/logout"): Indica la ruta de la página
    Retorna:
        - redirect(url_for("index")): 
        Redirige a la página
    """
    return redirect(url_for("index"))
