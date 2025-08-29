from dataclasses import dataclass
from flask import render_template


@dataclass
class Error:
    code: int
    message: str
    description: str


def not_found_error(e):
    error = Error(
        404, "Not Found Error", "The requested URL was not found on the server."
    )

    return render_template("error.html", error=error), 404


def unauthorized(e):
    error = Error(401, "Unauthorized", "You are not authorized to access this page.")
    return render_template("error.html", error=error), 401

def forbidden(e):
    error = Error(403, "Forbidden", "You do not have permission to access this page.")
    return render_template("error.html", error=error), 403
