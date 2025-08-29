from flask import Blueprint
from flask import render_template, url_for, redirect, flash, request, session
from src.core.entities import (add_content_post,
                               search_content_post,
                               order_content_post,
                               get_content_post_by_id,
                               modify_content_post,
                               logical_delete,
                               get_user_by_id,
                               publish_content_post,
                               store_content_post)
from src.web.forms import ContentPostForm
from datetime import date, datetime
from src.web.handlers.auth import check, login_required

# Blueprint para las funcionalidades del modulo de contenidos

queryResult = []
total_pages = 0
per_page = 25

content_bp = Blueprint('module_content', __name__,
                       url_prefix="/module_content")


@content_bp.get('/')
@login_required
@check("content_index")
def content():
    """
    Función que renderiza la página principal del módulo de contenidos.
    Decoradores:
        - @login_required: Requiere que el usuario esté autenticado.
        - @check("content_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @content_bp.get('/'): Define la ruta para acceder a la vista.
    Atributos: Ninguno
    Retorna:
        - render_template("module_content.html",current_page='content'): Renderiza la vista del módulo de contenidos.
    """
    return render_template("module_content.html", current_page='content')


# Funcionalidades para CREATE


@content_bp.get('/upload')
@login_required
@check("content_index")
@check("content_new")
def upload():
    """
    Función que renderiza la vista de creación de un contenido.
    Decoradores:
        - @login_required: Requiere que el usuario esté autenticado.
        - @check("content_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @check("content_new"): Requiere que el usuario tenga permisos para crear los contenidos.
        - @content_bp.get('/upload'): Define la ruta para acceder a la vista.
    Atributos: Ninguno
    Retorna:
        - render_template("content/upload.html", current_page='content', form=content_form): 
        Renderiza la vista de creación de un contenido.
    """
    content_post_form = ContentPostForm()
    return render_template("content/upload.html", current_page='content', form=content_post_form)


@content_bp.post('/upload')
@login_required
@check("content_index")
@check("content_new")
def upload_post():
    """
    Función que crea un contenido.
    Decoradores:
        - @login_required: Requiere que el usuario esté autenticado.
        - @check("content_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @check("content_new"): Requiere que el usuario tenga permisos para crear los contenidos.
        - @content_bp.post('/upload'): Define la ruta para acceder a la vista.
    Atributos: Ninguno
    Retorna:
        - redirect(url_for('module_content.upload', current_page='content')): 
        Redirecciona a la vista de creación de un contenido.
    """
    content_form = ContentPostForm()

    if validateContentAdd(content_form):
        add_content_post(content_form,session.get("user"))
        flash("¡El contenido se ha cargado correctamente!", "alert-success")
        return redirect(url_for('module_content.upload', current_page='content'))

    # Devuelve el formulario en caso de error
    return render_template("content/upload.html", current_page='content', form=content_form)


def validateContentAdd(contentForm):
    """
    Función que valida los datos de un contenido.
    Argumentos:
        - contentForm (ContentForm): Formulario con los datos del contenido.
    Retorna:
        - True si los datos son válidos, False en caso contrario.
    """

    if not contentForm.validate_on_submit():
        return False

    return True


# # Funcionalidades para INDEX


@content_bp.route('/explore', methods=['GET'])
@login_required
@check("content_index")
def explore():
    """
    Función que renderiza la vista de exploración de contenidos.
    Decoradores:
        - @login_required: Requiere que el usuario esté autenticado.
        - @check("content_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @contente_bp.route('/explore', methods=['GET']): Define la ruta para acceder a la vista.
    Atributos: Ninguno
    Retorna:
        - render_template("content/explore.html", current_page='content', items_on_page=items_on_page, total_pages=total_pages, 
        page=page, errors=errors, filters=filters): 
        Renderiza la vista de exploración de contenidos.
    """
    global queryResult, total_pages, per_page
    page = request.args.get('page', 1, type=int)
    items_on_page = []

    if request.args.get('reset', 0, type=int) == 1:
        session.pop('query_filters', None)
        queryResult = None
        total_pages = 0

    filters = {
        'title': request.args.get('title', ''),
        'author_alias': request.args.get('author_alias', ''),
    }

    session['query_filters'] = filters
    queryResult = search_content_post(**filters)

    if not queryResult:
        flash("No se encontraron resultados.", "alert-warning")
    else:
        total_pages = (queryResult.count() + per_page - 1) // per_page

    aux_query = order_content_post(queryResult, order_by_date=request.args.get('orderDirection'))
    start = (page - 1) * per_page
    items_on_page = aux_query[start:start + per_page] if aux_query else []

    return render_template(
        "content/explore.html", current_page='content',
        items_on_page=items_on_page, total_pages=total_pages,
        page=page, filters=filters
    )


# Funcionalidades para SHOW, UPDATE

@content_bp.route('/edit/<int:id>', methods=['GET'])
@login_required
@check("content_index")
@check("content_show")
def edit(id):
    """
    Función que renderiza la vista de edición de un contenido.
    Decoradores:
        - @login_required: Requiere que el usuario esté autenticado.
        - @check("content_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @check("content_show"): Requiere que el usuario tenga permisos para explorar los contenidos.
        - @receipt_bp.route('/edit/<int:id>', methods=['GET']): Define la ruta para acceder a la vista.
    Atributos:
        - id (int): Identificador del contenudi a editar.
    Retorna:
        - render_template("content/edit.html", current_page='content', form=contentForm, id=id):
        Renderiza la vista de edición de un contenido
    """

    content_post = get_content_post_by_id(id)
    contentForm = ContentPostForm()
    author = get_user_by_id(content_post.author_id)
    contentForm.title.data = content_post.title
    contentForm.summary.data = content_post.summary
    contentForm.content.data = content_post.content

    return render_template("content/edit.html",
                           current_page='content', form=contentForm, author=author.alias,status=content_post.status,fecha_creacion=content_post.created_at,id=id)


@content_bp.route('/edit', methods=['POST'])
@content_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
@check("content_index")
@check("content_show")
@check("content_update")
def edit_receipt(id):
    """
    Función que maneja la edición de un contenido y sus acciones (guardar, publicar, archivar).
    """
    
    content_post = get_content_post_by_id(id)
    modContent = ContentPostForm(request.form)

    if validateContentAdd(modContent):
        modify_content_post(id, modContent)

        action = request.form.get('action')

        if action == 'publish':
            publish_content_post(content_post,True)
            flash(f"El Contenido {id} se ha publicado correctamente.", "alert-success")
        elif action == 'archive':
            store_content_post(content_post)
            flash(f"El Contenido {id} se ha archivado correctamente.", "alert-success")
        elif action == 'des-archive':
            publish_content_post(content_post,False)
            flash(f"El Contenido {id} se ha publicado correctamente.", "alert-success")
        else:
            flash("¡El Contenido se ha modificado correctamente!", "alert-success")
    else:
        flash("¡El Contenido no se ha modificado!", "alert-danger")

    return redirect(url_for('module_content.edit', id=id))


# Funcionalidades para DESTROY


@content_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@check("content_index")
@check("content_destroy")
def delete(id):
    """
    Función que elimina un contemido.
    Decoradores:
        - @login_required: Requiere que el usuario esté autenticado.
        - @check("content_index"): Requiere que el usuario tenga permisos para acceder a la vista.
        - @check("content_destroy"): Requiere que el usuario tenga permisos para eliminar los contenidos.
        - @content_bp.route('/delete/<int:id>', methods=['POST']): Define la ruta para acceder a la vista.
    Atributos:
        - id (int): Identificador del contenido a eliminar.
    Retorna:
        - redirect(url_for('module_content.explore')): 
        Redirecciona a la vista de exploración de contenidos.
    """
    global total_pages
    if 'explore' not in request.referrer:
        flash(
            "Ha ocurrido un error y no se ha podido realizar la operación.", "alert-danger")
        return redirect(url_for('module_content.explore'))
    content = get_content_post_by_id(id)
    if content:
        logical_delete(content)
        global queryResult
        for e in queryResult:
            if e.id == id:
                queryResult.remove(e)
        total_pages = (queryResult.count() + per_page - 1) // per_page
        flash(f"El Contenido {
              id} se ha eliminado correctamente.", "alert-success")
    else:
        flash(
            "Ha ocurrido un error y no se ha podido realizar la operación.", "alert-danger")
    return redirect(url_for('module_content.explore'))

