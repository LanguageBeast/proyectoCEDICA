from datetime import datetime
import re
from core import entities

def validate_start_date(form):
    """
    Valida que la fecha de inicio no sea mayor a la fecha actual.

    Atributos:
    - form (Flask-WTF Form): Formulario que contiene el campo `start_date`.

    Reglas de validación:
    - La fecha de inicio debe ser menor o igual a la fecha actual.

    Retorna:
    - bool: `True` si la fecha de inicio es válida, `False` en caso contrario.
    """
    if form.start_date.data > datetime.today().date():
        form.start_date.errors.append("La fecha de inicio no puede ser mayor a la fecha actual.")
        return False
    return True


def validate_end_date(form):
    """
    Valida que la fecha de cese sea válida en relación con las fechas de inicio y la actual.

    Atributos:
    - form (Flask-WTF Form): Formulario que contiene los campos `start_date` y `end_date`.

    Reglas de validación:
    - La fecha de cese no puede ser mayor a la fecha actual.
    - La fecha de cese no puede ser anterior a la fecha de inicio.

    Retorna:
    - bool: `True` si la fecha de cese es válida, `False` en caso contrario.
    """
    end_date = form.end_date.data
    start_date = form.start_date.data
    
    if end_date > datetime.today().date():
        form.end_date.errors.append("La fecha de fin no puede ser mayor a la fecha actual.")
        return False
    if start_date > end_date:
        form.end_date.errors.append("La fecha de fin no puede ser anterior a la fecha de inicio.")
        return False
    return True


def validate_insurance_number(insurance_number):
    """
    Valida que el número de afiliado sea numérico.

    Atributos:
    - insurance_number (Field): Campo que contiene el número de afiliado.

    Reglas de validación:
    - El valor debe contener solo dígitos.

    Retorna:
    - bool: `True` si el número de afiliado es válido, `False` en caso contrario.
    """
    if not insurance_number.data.isdigit():
        insurance_number.errors.append("El número de afiliado debe ser un número.")
        return False
    return True


def validate_dni(dni):
    """
    Valida que el DNI sea un número de 8 dígitos.

    Atributos:
    - dni (Field): Campo que contiene el DNI.

    Reglas de validación:
    - El valor debe contener solo dígitos.
    - Debe tener exactamente 8 caracteres.

    Retorna:
    - bool: `True` si el DNI es válido, `False` en caso contrario.
    """
    if not dni.data.isdigit() or len(dni.data) != 8:
        dni.errors.append("El DNI debe ser un número de 8 dígitos.")
        return False
    return True


def validate_email_format(email):
    """
    Valida el formato del email.

    Atributos:
    - email (Field): Campo que contiene la dirección de correo electrónico.

    Reglas de validación:
    - El valor debe cumplir con el formato estándar de un correo electrónico.

    Retorna:
    - bool: `True` si el formato es válido, `False` en caso contrario.
    """
    email_regex = r'^\S+@\S+\.\S+$'
    if not re.match(email_regex, email.data):
        email.errors.append("Formato de email inválido.")
        return False
    return True


def validate_text_field(field):
    """
    Valida que un campo contenga solo caracteres alfabéticos.

    Atributos:
    - field (Field): Campo que contiene el texto a validar.

    Reglas de validación:
    - El valor debe contener solo letras, espacios y caracteres acentuados.

    Retorna:
    - bool: `True` si el texto es válido, `False` en caso contrario.
    """
    if not re.match(r'^[A-Za-zÁÉÍÓÚÑáéíóúñ\s]+$', field.data):
        field.errors.append("Solo se permiten caracteres alfabéticos.")
        return False
    return True


def validate_phone(phone):
    """
    Valida el formato del número de teléfono.

    Atributos:
    - phone (Field): Campo que contiene el número de teléfono.

    Reglas de validación:
    - El valor debe contener entre 7 y 15 dígitos, opcionalmente precedidos por un '+'.

    Retorna:
    - bool: `True` si el número de teléfono es válido, `False` en caso contrario.
    """
    if not re.match(r'^\+?\d{7,15}$', phone.data):
        phone.errors.append("Formato de teléfono inválido.")
        return False
    return True


def validate_options(field, valid_options):
    """
    Valida que el valor de un campo esté dentro de una lista de opciones válidas.

    Atributos:
    - field (Field): Campo que contiene el valor a validar.
    - valid_options (list): Lista de valores permitidos.

    Reglas de validación:
    - El valor debe coincidir (sin distinción de mayúsculas/minúsculas) con una de las opciones válidas.

    Retorna:
    - bool: `True` si el valor es válido, `False` en caso contrario.
    """
    if field.data.lower() not in valid_options:
        field.errors.append(f"Opción inválida: {field.data}. Debe ser una de: {', '.join(valid_options)}.")
        return False
    return True

def validate_address(address):
    """
    Función para validar el campo de Domicilio.

    Atributos:
    - address (str): Cadena que representa el domicilio ingresado por el usuario.

    Reglas de validación:
    - Solo puede contener letras (mayúsculas, minúsculas y acentuadas), números, espacios, puntos, y guiones.

    Acciones:
    - Si el domicilio no cumple las reglas de validación, se agrega un mensaje de error al atributo `errors` del formulario.

    Retorna:
    - bool: `True` si el domicilio cumple con las reglas de validación, `False` en caso contrario.
    """
    if not re.match(r'^[A-Za-z0-9ÁÉÍÓÚÑáéíóúñ\s.,-]+$', address.data):
        address.errors.append("El domicilio solo puede contener letras, números, espacios, puntos y guiones.")
        return False
    return True


def validate_team_member_data_upload(form):
    """
    Función para validar los datos al cargar un nuevo miembro del equipo.

    Atributos:
    - form (objeto): Formulario que contiene los datos del miembro del equipo.

    Reglas de validación:
    - El email ingresado no debe estar registrado previamente.
    - El DNI ingresado no debe estar registrado previamente.
    - Se ejecutan las validaciones generales de los datos mediante la función `validate_team_member_data`.

    Acciones:
    - Si el email ya está registrado, se agrega un mensaje de error al atributo `errors` del formulario.
    - Si el DNI ya está registrado, se agrega un mensaje de error al atributo `errors` del formulario.

    Retorna:
    - bool: `True` si los datos cumplen con todas las reglas de validación, `False` en caso contrario.
    """
    if entities.is_email_taken(form.email.data):
        form.email.errors.append("El email ya está registrado.")
        return False
    
    if entities.is_dni_taken(form.dni.data):
        form.dni.errors.append("El DNI ya está registrado.")
        return False
    return validate_team_member_data(form)

def validate_team_member_data_edit(form, id):
    """
    Función para validar los datos de un miembro del equipo al editar su información.

    Atributos:
    - form (objeto): Formulario que contiene los datos editados del miembro del equipo.
    - id (int): Identificador único del miembro del equipo que se está editando.

    Reglas de validación:
    - El DNI ingresado no debe pertenecer a otro miembro del equipo diferente al que se está editando.
    - El email ingresado no debe pertenecer a otro miembro del equipo diferente al que se está editando.
    - Se ejecutan las validaciones generales de los datos mediante la función `validate_team_member_data`.

    Acciones:
    - Si el DNI ya pertenece a otro miembro, se agrega un mensaje de error al atributo `errors` del formulario.
    - Si el email ya pertenece a otro miembro, se agrega un mensaje de error al atributo `errors` del formulario.

    Retorna:
    - bool: `True` si los datos cumplen con todas las reglas de validación, `False` en caso contrario.
    """
    member_dni= entities.is_dni_taken(form.dni.data)

    if  member_dni and not member_dni.id==id:
        form.dni.errors.append("El DNI pertenece a otro miembro del equipo.")
        return False
        
    member_email= entities.is_email_taken(form.email.data)

    if  member_email and not member_email.id==id:
        form.email.errors.append("El email pertenece a otro miembro del equipo.")
        return False
    return validate_team_member_data(form)

# Función para validar los datos
def validate_team_member_data(form):
    """
    Función para realizar validaciones generales sobre los datos de un miembro del equipo.

    Atributos:
    - form (objeto): Formulario que contiene los datos del miembro del equipo.

    Reglas de validación:
    - Las fechas deben ser válidas (fecha de inicio requerida y fecha de fin opcional).
    - El DNI debe tener un formato válido.
    - El email debe tener un formato válido.
    - El domicilio (si se ingresa) debe cumplir con las reglas establecidas.
    - Los campos de texto (nombre, apellido, nombre de contacto de emergencia, localidad) deben contener valores válidos.
    - Los números de teléfono deben tener un formato válido.
    - Las profesiones y los puestos laborales deben coincidir con las opciones predefinidas.
    - La condición (voluntario o personal rentado) debe ser válida, si se proporciona.
    - El número de afiliado de la obra social (si se ingresa) debe tener un formato válido.

    Acciones:
    - Si algún campo no cumple con las reglas de validación, se agrega un mensaje de error al atributo `errors` del formulario.

    Retorna:
    - bool: `True` si los datos cumplen con todas las reglas de validación, `False` en caso contrario.
    """
    if not validate_start_date(form):
        return False
    
    if form.end_date.data and not validate_end_date(form):
        return False
    
    if not validate_dni(form.dni):
        return False

    if not validate_email_format(form.email):
        return False
    if form.address.data and not validate_address(form.address):
        return False
    
    if not validate_text_field(form.first_name):
        return False
    if not validate_text_field(form.last_name):
        return False
    if not validate_text_field(form.emergency_contact_name):
        return False
    
    if form.location.data and not validate_text_field(form.location):
        return False

    if not validate_phone(form.phone):
        return False
    

    if not validate_phone(form.emergency_contact_phone):
        return False
    
    
    if not validate_options(form.profession, [
    'psicólogo/a', 'psicomotricista', 'médico/a', 'kinesiólogo/a',
    'terapista ocupacional', 'psicopedagogo/a', 'docente',
    'profesor', 'fonoaudiólogo/a', 'veterinario/a', 'otro']):
        return False

    
    if not validate_options(form.job_position, [
    'administrativo/a', 'terapeuta', 'conductor', 'auxiliar de pista',
    'herrero', 'veterinario', 'entrenador de caballos', 'domador',
    'profesor de equitación', 'docente de capacitación',
    'auxiliar de mantenimiento', 'otro']):
        return False
    if form.condition.data and not validate_options(form.condition, ['voluntario', 'personal rentado']):
        return False

    if form.insurance_number.data and not validate_insurance_number(form.insurance_number):
        return False
    return True


def validate_search_criteria(filter, search_string, job_position):
    """
    Función para validar los criterios de búsqueda al filtrar miembros del equipo.

    Atributos:
    - filter (str): Filtro seleccionado para realizar la búsqueda (ejemplo: 'dni', 'first_name', 'last_name', 'job_position').
    - search_string (str): Cadena de texto ingresada como criterio de búsqueda.
    - job_position (str): Puesto laboral seleccionado, si corresponde.

    Reglas de validación:
    - Si se proporciona un `search_string`, debe seleccionarse un filtro.
    - Si el filtro es 'dni', el `search_string` solo puede contener números.
    - Si el filtro es 'first_name' o 'last_name', el `search_string` solo puede contener letras y espacios.
    - Si el filtro es 'job_position', el puesto laboral debe ser válido según las opciones predefinidas.

    Opciones válidas para `job_position`:
    - administrativo/a, terapeuta, conductor, auxiliar de pista, herrero, veterinario,
      entrenador de caballos, domador, profesor de equitación, docente de capacitación,
      auxiliar de mantenimiento, otro.

    Acciones:
    - Si algún criterio de búsqueda no es válido, se devuelve un mensaje de error.

    Retorna:
    - tuple: `(bool, str)` donde:
      - `True` y `None` si los criterios son válidos.
      - `False` y un mensaje de error si los criterios no son válidos.
    """
    valid_job_positions = [
        'administrativo/a', 'terapeuta', 'conductor', 'auxiliar de pista',
        'herrero', 'veterinario', 'entrenador de caballos', 'domador',
        'profesor de equitación', 'docente de capacitación', 'auxiliar de mantenimiento', 'otro'
    ]

    # Validar que haya un filtro si hay un search_string
    if search_string and not filter:
        return False, 'Debes seleccionar un filtro antes de buscar.'

    # Validar según el filtro seleccionado
    if filter == 'dni':
        if not search_string.isdigit():
            return False, 'Solo se permiten números para buscar por DNI.'


    elif filter == 'first_name' or filter == 'last_name':
        if not re.match(r'^[A-Za-zÁÉÍÓÚÑáéíóúñ\s]+$', search_string):
            return False, 'Solo se permiten letras y espacios.'

    elif filter == 'job_position':
        if job_position.lower() not in valid_job_positions:
            return False, 'El puesto laboral seleccionado no es válido.'

    return True, None

def allowed_file(filename):
    """
    Función para verificar si un archivo tiene una extensión permitida.

    Atributos:
    - filename (str): Nombre del archivo que se desea validar.

    Reglas de validación:
    - El nombre del archivo debe incluir un punto (.) seguido de la extensión.
    - La extensión debe pertenecer a las permitidas.

    Extensiones permitidas:
    - pdf, docx, doc, png, jpg, jpeg, xls.

    Acciones:
    - Si el archivo cumple con los criterios, se considera válido.

    Retorna:
    - bool: `True` si el archivo tiene una extensión permitida, `False` en caso contrario.
    """
    # Extensiones válidas
    valid_extensions = {'pdf', 'docx', 'doc', 'png', 'jpg', 'jpeg', 'xls'}
    return bool(filename) and '.' in filename and filename.rsplit('.', 1)[1].lower() in valid_extensions

def validate_documents(files):
    """
    Valida una lista de archivos, verificando que cumplan con los requisitos de formato y tamaño.

    Atributos:
    - files (list): Lista de archivos a validar. Cada archivo debe ser un objeto compatible con el estándar de Flask para manejo de archivos.

    Reglas de validación:
    - Cada archivo debe tener una extensión permitida.
    - Cada archivo no debe exceder el tamaño máximo permitido de 5 MB.

    Extensiones permitidas:
    - pdf, docx, doc, png, jpg, jpeg, xls.

    Acciones:
    - Verifica la extensión del archivo utilizando la función `allowed_file`.
    - Verifica el tamaño del archivo en bytes.
    - Si un archivo no cumple con las reglas, se agrega un mensaje de error a la lista de errores.

    Retorna:
    - list: Una lista de mensajes de error. Si la lista está vacía, todos los archivos son válidos.

    Notas:
    - Se utiliza `file.seek(0)` para restablecer el puntero de lectura del archivo, permitiendo que se pueda leer nuevamente en otras operaciones.
    """
    max_file_size = 5 * 1024 * 1024  # 5 MB
    errors = []
    for file in files:
        if not allowed_file(file.filename):
            errors.append(f'El archivo {file.filename} tiene una extensión no permitida. Los formatos permitidos son: pdf, docx, doc, png, jpg, jpeg, xls.')
        if len(file.read()) > max_file_size:
            errors.append(f'El archivo {file.filename} excede el tamaño máximo permitido de 5MB.')
        file.seek(0)
    return errors


def validate_link(url):
    """
    Valida una URL ingresada para asegurar que cumple con un formato correcto.

    Atributos:
    - url (str): Enlace ingresado que se desea validar.

    Reglas de validación:
    - La URL debe comenzar opcionalmente con un protocolo (`http` o `https`).
    - Debe contener un dominio válido que puede incluir letras, números, puntos y guiones.
    - Puede incluir una extensión de dominio como `.com`, `.org`, `.net`, etc.
    - Puede contener una ruta opcional después del dominio.

    Acciones:
    - Valida la URL utilizando una expresión regular.

    Retorna:
    - bool: `True` si la URL es válida, `False` en caso contrario.

    Notas:
    - Se utiliza una expresión regular para validar tanto el dominio como la ruta opcional.
    - Una URL vacía o nula también se considera no válida.
    """
    url_pattern = re.compile(
        r'^(https?:\/\/)?'       # Protocolo (http o https)
        r'([a-zA-Z0-9.-]+)'      # Dominio (letras, números, puntos, guiones)
        r'(\.[a-zA-Z]{2,6})'     # Extensión del dominio (.com, .org, .net, etc.)
        r'([\/\w.-]*)*\/?$'      # Ruta opcional (cualquier combinación de /, letras, números, etc.)
    )

    # Validar si el enlace ingresado coincide con el patrón de la expresión regular
    return True if url and url_pattern.match(url) else False

def validate_author(author):
    """
    Función para validar el formato del autor.

    Atributos:
    - author (str): Cadena que representa el nombre o alias del autor.

    Reglas de validación:
    - Solo puede contener letras (incluidas mayúsculas, minúsculas y acentuadas), espacios y la letra 'ñ'.

    Retorna:
    - bool: `True` si el autor cumple con las reglas de validación, `False` en caso contrario.
    """
    if not re.match(r'^[A-Za-zÁÉÍÓÚÑáéíóúñ0-9\s]+$', author):
        return False
    return True


def validate_date_not_in_the_future(date):
    """
    Función para validar que una fecha no sea mayor a la fecha actual.

    Atributos:
    - date (datetime): Fecha que se desea validar.

    Regla de validación:
    - La fecha debe ser menor o igual a la fecha actual.

    Retorna:
    - bool: `True` si la fecha es válida (no excede la fecha actual), `False` en caso contrario.
    """
    today = datetime.today()
    if date > today:
        return False
    return True


def validate_start_date_before_end_date(start_date, end_date):
    """
    Función para validar que la fecha de inicio no sea mayor a la fecha de fin.

    Atributos:
    - start_date (datetime): Fecha de inicio.
    - end_date (datetime): Fecha de fin.

    Regla de validación:
    - La fecha de inicio debe ser menor o igual a la fecha de fin.

    Retorna:
    - bool: `True` si la fecha de inicio es válida (menor o igual a la de fin), `False` en caso contrario.
    """
    if start_date > end_date:
        return False
    return True
