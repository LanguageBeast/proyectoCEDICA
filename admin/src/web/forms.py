from flask_wtf import FlaskForm
from wtforms import DateField, FileField, RadioField, StringField, PasswordField, SubmitField, DateField, SelectField, DecimalField, FileField, RadioField, FloatField, FormField, BooleanField, SelectMultipleField, IntegerField, TextAreaField, widgets, TelField
from wtforms.validators import DataRequired, Email, NumberRange, Length, Optional, Regexp, ValidationError
from datetime import datetime


# form para el formulario de /auth/login

class LoginForm(FlaskForm):
    """
    Descripción:
    Clase para el formulario de login.
    Usa types de Flask-WTF para crear un formulario de login.
    ---------
    Atributos:
    - email: StringField
        Campo de texto para el email.
        restricciones -> no nulo, tipo email

    - password: PasswordField
        Campo de texto para la contraseña.
        restricciones -> no nulo

    - submit: SubmitField
        Botón de submit.

    ---------
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


# form para el formulario de /ecuestre/upload

class EquestrianForm(FlaskForm):
    """
    Descripción:
    Clase para el formulario de registro de un ecuestre.
    Usa types de Flask-WTF para crear un formulario de registro de un ecuestre.

    ---------
    Atributos:
    - name: StringField
        Campo de texto para el nombre del ecuestre.
        restricciones -> no nulo, longitud máxima de 100 caracteres

    - sex: StringField
        Campo de texto para el sexo del ecuestre.
        restricciones -> no nulo, longitud máxima de 10 caracteres

    - breed: StringField
        Campo de texto para la raza del ecuestre.
        restricciones -> no nulo, longitud máxima de 50 caracteres

    - coat: StringField
        Campo de texto para el pelaje del ecuestre.
        restricciones -> no nulo, longitud máxima de 50 caracteres

    - purchase_or_donation: RadioField
        Campo de radio para seleccionar si el ecuestre fue comprado o donado.
        restricciones -> no nulo

    - location: StringField
        Campo de texto para la sede del ecuestre.
        restricciones -> no nulo, longitud máxima de 100 caracteres

    - birth_date: DateField
        Campo de fecha para la fecha de nacimiento del ecuestre.
        restricciones -> no nulo

    - entry_date: DateField
        Campo de fecha para la fecha de ingreso del ecuestre.
        restricciones -> no nulo

    - documents: FileField
        Campo de archivo para subir documentos.
        No en uso.

    - submit: SubmitField
        Botón de submit.
    """

    name = StringField("Nombre", validators=[DataRequired(
        message="Por favor, escriba el nombre del ecuestre."), Length(max=100, message="El nombre no puede tener una longitud mayor a 100 carácteres.")], render_kw={"placeholder": "Escribir nombre"})
    sex = StringField("Sexo", validators=[DataRequired(
        message="Por favor, escriba el sexo del ecuestre."), Length(max=10, message="El sexo no puede tener una longitud mayor a 10 carácteres.")], render_kw={"placeholder": "Escribir sexo"})
    breed = StringField("Raza", validators=[DataRequired(
        message="Por favor, escriba la raza del ecuestre."), Length(max=50, message="La raza no puede tener una longitud mayor a 50 carácteres.")], render_kw={"placeholder": "Escribir raza"})
    coat = StringField("Pelaje", validators=[DataRequired(
        message="Por favor, escriba el pelaje del ecuestre."), Length(max=50, message="El pelaje no puede tener una longitud mayor a 50 carácteres.")], render_kw={"placeholder": "Escribir pelaje"})
    purchase_or_donation = RadioField("Seleccione uno", choices=[(
        'purchase', 'Es Compra'), ('donation', 'Es Donación')], validators=[DataRequired(message="Por favor, seleccione una opción.")])
    location = StringField("Sede", validators=[DataRequired(
        message="Por favor, escriba la sede del ecuestre."), Length(max=100, message="La sede no puede tener una longitud mayor a 100 carácteres.")], render_kw={"placeholder": "Escribir sede"})
    birth_date = DateField("Fecha de Nacimiento",
                           format='%Y-%m-%d', validators=[DataRequired(message="Por favor, escriba la fecha de nacimiento del ecuestre.")], render_kw={"placeholder": "Escribir fecha de nacimiento"})
    entry_date = DateField(
        "Fecha de Ingreso", format='%Y-%m-%d', validators=[DataRequired(message="Por favor, escriba la fecha de ingreso del ecuestre.")], render_kw={"placeholder": "Escribir fecha de ingreso"})
    documents = FileField("Documentos", render_kw={"multiple": True})
    # faltan los campos de entrenadores asignados y jinetes asociados; esos son más complejos
    # y los tengo que hardcodear y validar a mano
    submit = SubmitField("Enviar")


class TeamMemberForm(FlaskForm):
    """
    Descripción:
    Clase para el formulario de registro de un miembro de equipo.
    Usa types de Flask-WTF para crear un formulario de registro de un miembro de equipo.

    ---------
    Atributos:
    - first_name: StringField
        Campo de texto para el nombre del miembro de equipo.
        restricciones -> no nulo, longitud máxima de 50 caracteres

    - last_name: StringField
        Campo de texto para el apellido del miembro de equipo.
        restricciones -> no nulo, longitud máxima de 50 caracteres

    - dni: StringField
        Campo de texto para el DNI del miembro de equipo.
        restricciones -> no nulo, longitud máxima de 20 caracteres

    - address: StringField
        Campo de texto para el domicilio del miembro de equipo.
        restricciones -> no nulo, longitud máxima de 100 caracteres

    - email: StringField
        Campo de texto para el email del miembro de equipo.
        restricciones -> no nulo, tipo email

    - location: StringField
        Campo de texto para la localidad del miembro de equipo.
        restricciones -> no nulo, longitud máxima de 50 caracteres

    - phone: StringField
        Campo de texto para el teléfono del miembro de equipo.
        restricciones -> no nulo, longitud máxima de 20 caracteres

    - profession: SelectField
        Campo de selección para la profesión del miembro de equipo.
        restricciones -> no nulo

    - job_position: SelectField
        Campo de selección para el puesto laboral en la institución del miembro de equipo.
        restricciones -> no nulo

    - start_date: DateField
        Campo de fecha para la fecha de inicio del miembro de equipo.
        restricciones -> no nulo

    - end_date: DateField
        Campo de fecha para la fecha de cese del miembro de equipo.
        restricciones -> no nulo

    - emergency_contact_name: StringField
        Campo de texto para el nombre del contacto de emergencia del miembro de equipo.
        restricciones -> no nulo, longitud máxima de 50 caracteres

    - emergency_contact_phone: StringField
        Campo de texto para el teléfono del contacto de emergencia del miembro de equipo.
        restricciones -> no nulo, longitud máxima de 20 caracteres

    - health_insurance: StringField
        Campo de texto para la obra social del miembro de equipo.
        restricciones -> longitud máxima de 50 caracteres

    - insurance_number: StringField
        Campo de texto para el número de afiliado del miembro de equipo.
        restricciones -> longitud máxima de 50 caracteres

    - condition: RadioField
        Campo de radio para seleccionar la condición del miembro de equipo.

    - active: BooleanField
        Campo de booleano para activar o desactivar al miembro de equipo.

    - submit: SubmitField
        Botón de submit.

    ---------
    """

    first_name = StringField("Nombre", validators=[DataRequired(
        message="Por favor, ingrese el nombre.")], render_kw={"placeholder": "Escribir nombre"})
    last_name = StringField("Apellido", validators=[DataRequired(
        message="Por favor, ingrese el apellido.")], render_kw={"placeholder": "Escribir apellido"})
    dni = StringField("DNI", validators=[DataRequired(
        message="Por favor, ingrese el DNI.")], render_kw={"placeholder": "Escribir DNI"})
    address = StringField("Domicilio", validators=[Optional()], render_kw={
                          "placeholder": "Escribir domicilio"})
    email = StringField("Email", validators=[DataRequired(message="Por favor, ingrese el email."), Email(
        message="Por favor, ingrese un email válido.")], render_kw={"placeholder": "Escribir email"})
    location = StringField("Localidad", validators=[Optional()], render_kw={
                           "placeholder": "Escribir localidad"})
    phone = TelField("Teléfono", validators=[DataRequired(
        message="Por favor, ingrese el teléfono.")], render_kw={"placeholder": "Escribir teléfono"})

    # Profesión
    profession = SelectField("Profesión", choices=[
        ('', 'Seleccione una profesión'),
        ('Psicólogo/a', 'Psicólogo/a'),
        ('Psicomotricista', 'Psicomotricista'),
        ('Médico/a', 'Médico/a'),
        ('Kinesiólogo/a', 'Kinesiólogo/a'),
        ('Terapista Ocupacional', 'Terapista Ocupacional'),
        ('Psicopedagogo/a', 'Psicopedagogo/a'),
        ('Docente', 'Docente'),
        ('Profesor', 'Profesor'),
        ('Fonoaudiólogo/a', 'Fonoaudiólogo/a'),
        ('Veterinario/a', 'Veterinario/a'),
        ('Otro', 'Otro')
    ], validators=[DataRequired(message="Por favor, seleccione una profesión.")])

    # Puesto Laboral en la Institución
    job_position = SelectField("Puesto laboral en la Institución", choices=[
        ('', 'Seleccione un puesto laboral'),
        ('Administrativo/a', 'Administrativo/a'),
        ('Terapeuta', 'Terapeuta'),
        ('Conductor', 'Conductor'),
        ('Auxiliar de pista', 'Auxiliar de pista'),
        ('Herrero', 'Herrero'),
        ('Veterinario', 'Veterinario'),
        ('Entrenador de Caballos', 'Entrenador de Caballos'),
        ('Domador', 'Domador'),
        ('Profesor de Equitación', 'Profesor de Equitación'),
        ('Docente de Capacitación', 'Docente de Capacitación'),
        ('Auxiliar de mantenimiento', 'Auxiliar de mantenimiento'),
        ('Otro', 'Otro')
    ], validators=[DataRequired(message="Por favor, seleccione un puesto laboral.")])

    start_date = DateField("Fecha de Inicio", format='%Y-%m-%d', validators=[
                           DataRequired(message="Por favor, ingrese la fecha de inicio.")])
    end_date = DateField("Fecha de Cese", format='%Y-%m-%d',
                         validators=[Optional()], render_kw={"placeholder": "Opcional"})

    emergency_contact_name = StringField("Nombre del contacto de Emergencia", validators=[DataRequired(
        message="Por favor, ingrese el nombre del contacto de emergencia.")], render_kw={"placeholder": "Escribir nombre"})
    emergency_contact_phone = StringField("Teléfono del contacto de Emergencia", validators=[DataRequired(
        message="Por favor, ingrese el teléfono del contacto de emergencia.")], render_kw={"placeholder": "Escribir teléfono"})

    health_insurance = StringField("Obra Social", validators=[Optional()], render_kw={
                                   "placeholder": "Escribir obra social"})
    insurance_number = StringField("N° de Afiliado", validators=[Optional()], render_kw={
                                   "placeholder": "Escribir número de afiliado"})

    condition = RadioField(
        "Condición",
        choices=[
            ('Voluntario', 'Voluntario'),
            ('Personal Rentado', 'Personal Rentado')
        ],
        validators=[Optional()]
    )
    documents = FileField("Documentos", render_kw={"multiple": True})
    # Activo
    active = BooleanField('Active')
    submit = SubmitField("Enviar")

# form para el formulario de /users/upload

# form para el formulario de /users/upload


class UserForm(FlaskForm):
    """
    Descripción:
    Clase para el formulario de registro de un usuario.
    Usa types de Flask-WTF para crear un formulario de registro de un usuario.

    ---------
    Atributos:
    - email: StringField
        Campo de texto para el email del usuario.
        restricciones -> no nulo, tipo email, longitud máxima de 100 caracteres

    - dni: StringField
        Campo de texto para el DNI del usuario.
        restricciones -> no nulo

    - alias: StringField
        Campo de texto para el alias del usuario.
        restricciones -> no nulo, longitud máxima de 50 caracteres

    - password: PasswordField
        Campo de texto para la contraseña del usuario.
        restricciones -> no nulo, longitud entre 3 y 255 caracteres

    - isEnabled: RadioField
        Campo de radio para activar o desactivar al usuario.
        restricciones -> no nulo

    - role: RadioField
        Campo de radio para seleccionar el rol del usuario.
        restricciones -> no nulo

    - submit: SubmitField
        Botón de submit.

    ---------
    """

    email = StringField("Email", validators=[DataRequired(
        message="Por favor, escriba el email del usuario."), Email(message="Por favor, escriba un email correcto."), Length(max=100, message="El email no puede tener una longitud mayor a 100 carácteres.")], render_kw={"placeholder": "Escribir email"})
    dni = StringField("DNI", validators=[DataRequired(
        message="Por favor, ingrese el DNI.")], render_kw={"placeholder": "Escribir DNI"})
    alias = StringField("Alias", validators=[DataRequired(
        message="Por favor, escriba el alias del usuario."), Length(max=50, message="El alias no puede tener una longitud mayor a 50 carácteres.")], render_kw={"placeholder": "Escribir alias"})
    password = PasswordField("Contraseña", validators=[DataRequired(
        message="Por favor, escriba la contraseña del usuario."), Length(min=3, max=255, message="La contraseña debe de estar entre 3-255 carácteres.")], render_kw={"placeholder": "Escribir contraseña"})
    isEnabled = RadioField("Activo", choices=[(
        'yes', 'Sí'), ('no', 'No')], validators=[DataRequired(message="Por favor, seleccione una opción.")])
    role = RadioField(
        "Rol",
        choices=[
            ('administration', 'Administración'),
            ('equestrian', 'Ecuestre'),
            ('technical', 'Técnico'),
            ('volunteer', 'Voluntario'),
        ],
        validators=[DataRequired(message="Por favor, seleccione un rol.")]
    )
    submit = SubmitField("Enviar")


# form para el formulario de upload registro de cobro

class ReceiptForm(FlaskForm):
    """
    Descripción:
    Clase para el formulario de registro de un cobro.
    Usa types de Flask-WTF para crear un formulario de registro de un cobro.

    ---------
    Atributos:
    - payment_date: DateField
        Campo de fecha para la fecha de cobro.
        restricciones -> no nulo

    - payment_method: StringField
        Campo de texto para el método de pago.
        restricciones -> no nulo, longitud máxima de 50 caracteres

    - amount: DecimalField
        Campo de texto para el monto del cobro.
        restricciones -> no nulo, mayor que cero

    - notes: StringField
        Campo de texto para las observaciones del cobro.
        restricciones -> longitud máxima de 255 caracteres

    - submit: SubmitField
        Botón de submit.

    ---------
    """

    payment_date = DateField("Fecha de Cobro", format='%Y-%m-%d', validators=[DataRequired(
        message="Por favor, escriba la fecha de cobro.")], render_kw={"placeholder": "Escribir fecha de cobro"})
    payment_method = StringField("Metodo de Pago", validators=[DataRequired(message="Por favor, ingre el metodo de pago"),  Length(
        max=50, message="El método de pago no puede exceder los 50 caracteres")], render_kw={"placeholder": "Escribir el metodo de pago"})
    amount = DecimalField("Monto",
                          validators=[DataRequired(message="Por favor, escriba el monto."),
                                      NumberRange(min=0, message="El monto debe ser mayor que cero.")],
                          render_kw={"placeholder": "$0000"})
    notes = StringField("Observaciones", validators=[Length(
        max=255, message="El método de pago no puede exceder los 255 caracteres")], render_kw={"placeholder": "Escribir observaciones"})
    submit = SubmitField("Enviar")


# form para el formulario de /payment/upload

class PaymentForm(FlaskForm):
    """
    Descripción:
    Clase para el formulario de registro de un pago.
    Usa types de Flask-WTF para crear un formulario de registro de un pago.

    ---------
    Atributos:
    - amount: FloatField
        Campo de texto para el monto del pago.
        restricciones -> no nulo, mayor que cero

    - payment_date: DateField
        Campo de fecha para la fecha de pago.
        restricciones -> no nulo

    - description: StringField
        Campo de texto para la descripción del pago.
        restricciones -> longitud máxima de 255 caracteres

    - payment_type: SelectField
        Campo de selección para el tipo de pago.
        restricciones -> no nulo

    - team_member: SelectField
        Campo de selección para el miembro de equipo.


    - submit: SubmitField
        Botón de submit.

    ---------
    """

    amount = FloatField(
        "Monto",
        validators=[
            DataRequired(message="Por favor, escriba el monto."),
            NumberRange(
                min=1, message="El monto debe ser un número mayor que cero."),
        ],
    )
    payment_date = DateField(
        "Fecha de Pago",
        format="%Y-%m-%d",
        validators=[
            DataRequired(message="Por favor, ingrese la fecha de pago.")
        ],
        render_kw={"placeholder": "Seleccionar fecha de ingreso"},
    )
    description = StringField(
        "Descripción",
        validators=[
            Length(
                max=255, message="La descripcióon no puede exceder los 255 caracteres."
            )
        ],
    )
    payment_type = SelectField(
        "Tipo de pago",
        coerce=int,
        validators=[DataRequired(
            message="Por favor, seleccione un tipo de pago.")],
    )
    team_member = SelectField(
        "Miembro de equipo (si es pago de honorarios)",
        coerce=int,
        validators=[Optional()]
    )
    submit = SubmitField("Enviar")


# form para el formulario de upload registro de cobro

def validate_date(form, field):
    """
    Función para validar la fecha de un campo. Retorna un error si la fecha no es válida.
    Atributos:
    - form (FlaskForm): formulario de Flask
    - field (DateField): campo de fecha
    """
    min_date = datetime(1904, 1, 1).date()
    max_date = datetime.today().date()
    if not (min_date < field.data < max_date):
        raise ValidationError(f"La fecha debe estar entre {
                              min_date} y {max_date}.")


class FileJyAForm(FlaskForm):
    """
    Descripción:
    Clase para el formulario de registro de un legajo de Jinetes y Amazonas.
    Usa types de Flask-WTF para crear un formulario de registro de un legajo de Jinetes y Amazonas.

    ---------
    Atributos:
    - first_name: StringField
        Campo de texto para el nombre del jinete/amazona.
        restricciones -> no nulo, longitud máxima de 50 caracteres, solo letras y espacios

    - last_name: StringField
        Campo de texto para el apellido del jinete/amazona.
        restricciones -> no nulo, longitud máxima de 50 caracteres, solo letras y espacios

    - dni: StringField
        Campo de texto para el DNI del jinete/amazona.
        restricciones -> no nulo, solo números

    - age: IntegerField
        Campo de texto para la edad del jinete/amazona.
        restricciones -> no nulo, mayor que cero

    - birth_date: DateField
        Campo de fecha para la fecha de nacimiento del jinete/amazona.
        restricciones -> no nulo

    - birth_locality: StringField
        Campo de texto para la localidad de nacimiento del jinete/amazona.
        restricciones -> no nulo, longitud máxima de 50 caracteres, solo letras y espacios

    - birth_province: StringField
        Campo de texto para la provincia de nacimiento del jinete/amazona.
        restricciones -> no nulo, longitud máxima de 50 caracteres, solo letras y espacios

    - adress_street: StringField
        Campo de texto para la calle del domicilio del jinete/amazona.
        restricciones -> no nulo, longitud máxima de 50 caracteres, solo letras, números, espacios, puntos y guiones

    - adress_number: IntegerField
        Campo de texto para el número del domicilio del jinete/amazona.
        restricciones -> no nulo, mayor que cero

    - adress_apartment: StringField
        Campo de texto para el departamento del domicilio del jinete/amazona.
        restricciones -> longitud máxima de 20 caracteres, solo letras, números, espacios, puntos y guiones

    - adress_locality: StringField
        Campo de texto para la localidad del domicilio del jinete/amazona.
        restricciones -> no nulo, longitud máxima de 50 caracteres, solo letras y espacios

    - adress_province: StringField
        Campo de texto para la provincia del domicilio del jinete/amazona.
        restricciones -> no nulo, longitud máxima de 50 caracteres, solo letras y espacios

    - phone: StringField
        Campo de texto para el teléfono del jinete/amazona.
        restricciones -> longitud máxima de 50 caracteres, solo números y sin espacios

    - emergency_contact_name: StringField
        Campo de texto para el nombre del contacto de emergencia del jinete/amazona.
        restricciones -> no nulo, longitud máxima de 50 caracteres, solo letras y espacios

    - emergency_contact_phone: StringField
        Campo de texto para el teléfono del contacto de emergencia del jinete/amazona.
        restricciones -> no nulo, longitud máxima de 50 caracteres, solo números y sin espacios

    - disability_certificate: RadioField
        Campo de radio para seleccionar si el jinete/amazona tiene certificado de discapacidad.
        restricciones -> no nulo

    - disability_certificate_diagnosis: SelectMultipleField
        Campo de selección múltiple para el diagnóstico del certificado de discapacidad.
        restricciones -> no nulo, longitud máxima de 20 caracteres, solo letras

    - other_diagnosis_disability: StringField
        Campo de texto para otro diagnóstico de discapacidad.
        restricciones -> longitud máxima de 20 caracteres, solo letras y espacios

    - disability_type: SelectMultipleField
        Campo de selección múltiple para el tipo de discapacidad.
        restricciones -> no nulo, longitud máxima de 20 caracteres, solo letras y espacios

    - scholarship: RadioField
        Campo de radio para seleccionar si el jinete/amazona tiene beca.
        restricciones -> no nulo

    - per_scholarship: IntegerField
        Campo numérico para el monto de la beca.
        restricciones -> no nulo, mayor que cero

    - scholarship_notes: StringField
        Campo de texto para la observación de la beca.
        restricciones -> longitud máxima de 255 caracteres

    - welfare: RadioField
        Campo de radio para seleccionar si el jinete/amazona tiene asistencia social.
        restricciones -> no nulo

    - welfare_type: RadioField
        Campo de radio para seleccionar el tipo de asistencia social.
        restricciones -> no nulo

    - pension_beneficiary: RadioField
        Campo de radio para seleccionar si el jinete/amazona es beneficiario de pensión.
        restricciones -> no nulo

    - pension_type: RadioField
        Campo de radio para seleccionar el tipo de pensión.
        restricciones -> no nulo

    - social_security: StringField
        Campo de texto para la seguridad social del jinete/amazona.
        restricciones -> longitud máxima de 25 caracteres

    - affiliate_number: StringField
        Campo de texto para el número de afiliado del jinete/amazona.
        restricciones -> longitud máxima de 25 caracteres

    - has_guardianship: RadioField
        Campo de radio para seleccionar si el jinete/amazona tiene tutela.
        restricciones -> no nulo

    - previsional_situacion_notes: StringField
        Campo de texto para la observación de la situación previsional.
        restricciones -> longitud máxima de 255 caracteres

    - institution_name: StringField
        Campo de texto para el nombre de la institución.
        restricciones -> longitud máxima de 50 caracteres

    - school_address: StringField
        Campo de texto para la dirección de la escuela.
        restricciones -> longitud máxima de 50 caracteres

    - school_phone: StringField
        Campo de texto para el teléfono de la institución.
        restricciones -> longitud máxima de 20 caracteres

    - current_grade: StringField
        Campo de texto para el grado actual.
        restricciones -> longitud máxima de 50 caracteres

    - school_notes: StringField
        Campo de texto para la observación de la escuela.
        restricciones -> longitud máxima de 255 caracteres

    - attending_professionals: StringField
        Campo de texto para los profesionales que atienden al jinete/amazona.
        restricciones -> longitud máxima de 100 caracteres

    - relationship1: StringField
        Campo de texto para el tutor 1
        restricciones -> longitud máxima de 50 caracteres

    - first_name1: StringField
        Campo de texto para el nombre del tutor 1
        restricciones -> longitud máxima de 50 caracteres

    - last_name1: StringField
        Campo de texto para el apellido del tutor 1
        restricciones -> longitud máxima de 50 caracteres

    - dni1: StringField
        Campo de texto para el DNI del tutor 1
        restricciones -> longitud máxima de 20 caracteres

    - current_address1: StringField
        Campo de texto para la dirección del tutor 1
        restricciones -> longitud máxima de 255 caracteres

    - mobile_phone1: StringField
        Campo de texto para el teléfono del tutor 1
        restricciones -> longitud máxima de 20 caracteres

    - email1: StringField
        Campo de texto para el email del tutor 1
        restricciones -> longitud máxima de 100 caracteres

    - education_level1: RadioField
        Campo de radio para seleccionar el nivel educativo del tutor 1
        restricciones -> longitud máxima de 50 caracteres

    - occupation1: StringField
        Campo de texto para la ocupación del tutor 1
        restricciones -> longitud máxima de 50 caracteres

    - relationship2: StringField
        Campo de texto para el tutor 2
        restricciones -> longitud máxima de 50 caracteres

    - first_name2: StringField
        Campo de texto para el nombre del tutor 2
        restricciones -> longitud máxima de 50 caracteres

    - last_name2: StringField
        Campo de texto para el apellido del tutor 2
        restricciones -> longitud máxima de 50 caracteres

    - dni2: StringField
        Campo de texto para el DNI del tutor 2
        restricciones -> longitud máxima de 20 caracteres

    - current_address2: StringField
        Campo de texto para la dirección del tutor 2
        restricciones -> longitud máxima de 255 caracteres

    - mobile_phone2: StringField
        Campo de texto para el teléfono del tutor 2
        restricciones -> longitud máxima de 20 caracteres

    - email2: StringField
        Campo de texto para el email del tutor 2
        restricciones -> longitud máxima de 100 caracteres

    - education_level2: RadioField
        Campo de radio para seleccionar el nivel educativo del tutor 2
        restricciones -> longitud máxima de 50 caracteres

    - occupation2: StringField
        Campo de texto para la ocupación del tutor 2
        restricciones -> longitud máxima de 50 caracteres

    - work_proposal: RadioField
        Campo de radio para seleccionar si el jinete/amazona tiene propuesta laboral
        restricciones -> no nulo

    - condition: RadioField
        Campo de radio para seleccionar la condición del jinete/amazona

    - location: StringField
        Campo de texto para la sede del jinete/amazona.

    - submit: SubmitField
        Botón de submit.

    ---------
    """

    # Pestaña informacion general

    first_name = StringField("Nombre/s",
                             validators=[DataRequired(message="Por favor, escriba el nombre."),
                                         Length(
                                 max=25, message="El nombre no puede superar los 50 caracteres"),
                                 Regexp(
                                             regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="El nombre solo puede contener letras y espacios."),
                             ],
                             render_kw={"placeholder": "Escribir nombre/s"})

    last_name = StringField("Apellido/s",
                            validators=[DataRequired(message="Por favor, escriba el apellido."),
                                        Length(
                                max=25, message="El apellido no puede superar los 50 caracteres"),
                                Regexp(regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="El apellido solo puede contener letras y espacios.")],
                            render_kw={"placeholder": "Escribir apellidos/s"})

    dni = StringField("DNI",
                      validators=[DataRequired(message="Por favor, escriba el dni."),
                                  Length(
                          max=15, message="El DNI no puede superar los 15 caracteres"),
                          Regexp(regex=r'^\d+$', message="El DNI solo puede contener números.")],
                      render_kw={"placeholder": "Ingrese el DNI"})

    age = IntegerField("Edad",
                       validators=[DataRequired(message="Por favor, escriba el monto."),
                                   NumberRange(min=0, max=120, message="La edad debe estar entre 0 y 120.")],

                       render_kw={"placeholder": "Ingrese la edad"})
    birth_date = DateField("Fecha de Nacimiento",
                           format='%Y-%m-%d',
                           validators=[DataRequired(message="Por favor, ingrese la fecha de nacimiento."),
                                       ],
                           render_kw={"placeholder": "Ingresar la fecha de nacimiento"})
    birth_locality = StringField("Localidad",
                                 validators=[DataRequired(message="Por favor, ingrese la localidad de nacimiento."),
                                             Length(
                                     max=50, message="La localidad no puede superar los 50 caracteres"),
                                     Regexp(regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="La localidad solo puede contener letras y espacios.")],
                                 render_kw={"placeholder": "Localidad"})
    birth_province = StringField("Provincia",
                                 validators=[DataRequired(message="Por favor, ingrese la provincia de nacimiento."),
                                             Length(
                                     max=50, message="El provincia no puede superar los 50 caracteres"),
                                     Regexp(regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="La provincia solo puede contener letras y espacios.")],
                                 render_kw={"placeholder": "Provincia"})

    adress_street = StringField("Calle",
                                validators=[DataRequired(message="Por favor, ingrese la calle de domicilio."),
                                            Length(
                                    max=50, message="La calle no puede superar los 50 caracteres"),
                                    Regexp(regex=r'^[A-Za-z0-9\s\.\-]+$', message="La calle solo puede contener letras, números, espacios, puntos y guiones.")],
                                render_kw={"placeholder": "Calle"})
    adress_number = IntegerField("Numero",
                                 validators=[DataRequired(
                                     message="Por favor, ingrese el numero de domicilio.")],
                                 render_kw={"placeholder": "0"})
    adress_apartment = StringField("Depto",
                                   validators=[
                                       Length(max=20, message="El departamento no puede superar los 50 caracteres")],
                                   render_kw={"placeholder": "Depto"})
    adress_locality = StringField("Localidad",
                                  validators=[DataRequired(message="Por favor, ingrese la localidad."),
                                              Length(
                                      max=50, message="La localidad no puede superar los 50 caracteres"),
                                      Regexp(regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="La localidad solo puede contener letras y espacios.")],
                                  render_kw={"placeholder": "Localidad"})
    adress_province = StringField("Provincia",
                                  validators=[DataRequired(message="Por favor, ingrese la provincia."),
                                              Length(
                                      max=50, message="La provincia no puede superar los 50 caracteres"),
                                      Regexp(regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="La provincia solo puede contener letras y espacios.")],
                                  render_kw={"placeholder": "Provincia"})

    phone = StringField("Teléfono",
                        validators=[Optional(),
                                    Length(
                            max=50, message="El telefono no puede superar los 50 caracteres"),
                            Regexp(regex=r'^\d+$', message="El telefono solo puede contener números.")],
                        render_kw={"placeholder": "Ingrese el número de teléfono sin espacios ni guiones"})
    emergency_contact_name = StringField("Nombre de contacto de emergencia",
                                         validators=[DataRequired(message="Por favor, ingrese el nombre de contacto de emergencia."),
                                                     Length(
                                             max=50, message="El nombre de contacto de emergencia no puede superar los 50 caracteres"),
                                             Regexp(regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="El nombre del contacto de emergencia solo puede contener letras y espacios.")],
                                         render_kw={"placeholder": "Nombre"})
    emergency_contact_phone = StringField("Telefono de contacto de emergencia",
                                          validators=[DataRequired(message="Por favor, ingrese el telefono de contacto de emergencia."),
                                                      Length(
                                              max=50, message="El telefono de contacto de emergencia no puede superar los 50 caracteres"),
                                              Regexp(regex=r'^\d+$', message="El telefono solo puede contener números.")],
                                          render_kw={"placeholder": "Ingrese el número de teléfono sin espacios ni guiones"})
    ###
    disability_certificate = RadioField("Seleccione uno", choices=[('si', 'Si'), ('no', 'No')], validators=[
                                        DataRequired(message="Por favor, seleccione una opción.")])

    disability_certificate_diagnosis = SelectMultipleField(
        "Tipo de discapacidad",
        choices=[
            ("ECNE", "ECNE"),
            ("Lesión post-traumática", "Lesión post-traumática"),
            ("Mielomeningocele", "Mielomeningocele"),
            ("Esclerosis Múltiple", "Esclerosis Múltiple"),
            ("Escoliosis Leve", "Escoliosis Leve"),
            ("Secuelas de ACV", "Secuelas de ACV"),
            ("Discapacidad Intelectual", "Discapacidad Intelectual"),
            ("Trastorno del Espectro Autista", "Trastorno del Espectro Autista"),
            ("Trastorno del Aprendizaje", "Trastorno del Aprendizaje"),
            ("Trastorno por Déficit de Atención/Hiperactividad",
             "Trastorno por Déficit de Atención/Hiperactividad"),
            ("Trastorno de la Comunicación", "Trastorno de la Comunicación"),
            ("Trastorno de Ansiedad", "Trastorno de Ansiedad"),
            ("Síndrome de Down", "Síndrome de Down"),
            ("Retraso Madurativo", "Retraso Madurativo"),
            ("Psicosis", "Psicosis"),
            ("Trastorno de Conducta", "Trastorno de Conducta"),
            ("Trastornos del ánimo y afectivos",
             "Trastornos del ánimo y afectivos"),
            ("Trastorno Alimentario", "Trastorno Alimentario")
        ],
        coerce=str,
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )

    other_diagnosis_disability = StringField("Otra discapacidad (especificar)", validators=[Optional(), Length(max=20, message="No puede superar los 20 caracteres"),
                                                                                            Regexp(regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="Solo puede contener letras y espacios.")],
                                             render_kw={"placeholder": "Si es otro diagnóstico especificar cual"})

    disability_type = SelectMultipleField(
        "Tipos de discapacidad",
        choices=[("Mental", "Mental"),
                 ("Motora", "Motora"),
                 ("lomenSensorial", "Sensorial"),
                 ("Visceral", "Visceral"),
                 ],
        coerce=str,
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )

    scholarship = RadioField("Seleccione uno", choices=[('si', 'Si'), ('no', 'No')], validators=[
                             DataRequired(message="Por favor, seleccione una opción.")])

    per_scholarship = IntegerField("Porcentaje de Beca",
                                   validators=[Optional(),
                                               NumberRange(min=0, max=120, message="La edad debe estar entre 0 y 100.")],
                                   render_kw={"placeholder": "Porcentaje de beca"})

    scholarship_notes = StringField("Observaciones de beca",
                                    validators=[
                                        Length(max=50, message="No puede superar los 255 caracteres")],
                                    render_kw={"placeholder": "Observaciones"})

    welfare = RadioField("Seleccione uno", choices=[('si', 'Si'), ('no', 'No')], validators=[
                         DataRequired(message="Por favor, seleccione una opción.")])

    welfare_type = SelectMultipleField(
        "Tipos de asignaciones",
        choices=[("child_welfare", " Asignación Universal por hijo"),
                 ("child_disability_welfare",
                  "Asignación Universal por hijo con Discapacidad"),
                 ("school_help_welfare", "Asignación por ayuda escolar anual"),
                 ],
        coerce=str,
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )

    pension_beneficiary = RadioField("Seleccione uno", choices=[('si', 'Si'), ('no', 'No')], validators=[
                                     DataRequired(message="Por favor, seleccione una opción.")])
    pension_type = RadioField("Seleccione uno", choices=[(
        'Provincial', 'Provincial'), ('Nacional', 'Nacional')], validators=[Optional()])

    # situacion previsional
    social_security = StringField("Obra Social", validators=[Optional(),
                                                             Length(
                                                                 max=25, message="El nombre no puede superar los 25 caracteres"),
                                                             Regexp(
                                                                 regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="La obra social solo puede contener letras y espacios."),
                                                             ],
                                  render_kw={"placeholder": "Obra Social"})

    affiliate_number = StringField("Numero de afiliado", validators=[Optional(),
                                                                     Length(
                                                                         max=50, message="El nombre no puede superar los 50 caracteres")
                                                                     ],
                                   render_kw={"placeholder": "Numero afiliado"})

    has_guardianship = RadioField("¿Posee curatela?", choices=[
                                  ('si', 'Si'), ('no', 'No')], validators=[Optional()])

    previsional_situacion_notes = StringField("Observaciones de situacion previsional", validators=[Optional(),
                                                                                                    Length(
                                                                                                        max=255, message="El nombre no puede superar los 255 caracteres"),
                                                                                                    Regexp(regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="La obra social solo puede contener letras y espacios.")],
                                              render_kw={"placeholder": "Observaciones"})

    # Institucion

    institution_name = StringField("Nombre de la institucion", validators=[Optional(),
                                                                           Length(
                                                                               max=50, message="El nombre no puede superar los 50 caracteres"),
                                                                           Regexp(
                                                                               regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="El nombre solo puede contener letras y espacios."),
                                                                           ], render_kw={"placeholder": "Nombre de la institución"})

    school_address = StringField("Dirección", validators=[Optional(),
                                                          Length(
                                                              max=100, message="El nombre no puede superar los 50 caracteres"),
                                                          ], render_kw={"placeholder": "Dirección de la institución"})
    school_phone = StringField("Teléfono",
                               validators=[Optional(),
                                           Length(
                                   max=20, message="El teléfono no puede superar los 20 caracteres"),
                                   Regexp(regex=r'^\d+$', message="El teléfono solo puede contener números.")],
                               render_kw={"placeholder": "Ingrese el número de teléfono sin espacios ni guiones"})
    current_grade = StringField("Grado/Año actual", validators=[Optional(),
                                                                Length(
                                                                    max=50, message="No nombre no puede superar los 50 caracteres"),
                                                                ], render_kw={"placeholder": "Grado o año actual"})
    school_notes = StringField("Observaciones",
                               validators=[
                                   Length(max=255, message="No puede superar los 255 caracteres")],
                               render_kw={"placeholder": "Observaciones"})

    attending_professionals = StringField("Profesionales que lo atienden",
                                          validators=[DataRequired(message="Por favor complete este campo"),
                                                      Length(max=100, message="No puede superar los 255 caracteres")],
                                          render_kw={"placeholder": "Profesionales que lo atiendes"})

    # Campos para Tutor 1
    relationship1 = StringField("Parentesco",
                                validators=[DataRequired(message="Por favor, ingrese la relación."),
                                            Length(
                                                max=50, message="El parentesco no puede superar los 50 caracteres."),
                                            Regexp(regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="El parentesco solo puede contener letras y espacios.")],
                                render_kw={"placeholder": "Ej: Padre, Madre, etc."})

    first_name1 = StringField("Nombre",
                              validators=[DataRequired(message="Por favor, ingrese el nombre."),
                                          Length(
                                              max=100, message="El nombre no puede superar los 100 caracteres."),
                                          Regexp(regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="El nombre solo puede contener letras y espacios.")],
                              render_kw={"placeholder": "Escribir nombre"})

    last_name1 = StringField("Apellido",
                             validators=[DataRequired(message="Por favor, ingrese el apellido."),
                                         Length(
                                             max=100, message="El apellido no puede superar los 100 caracteres."),
                                         Regexp(regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="El apellido solo puede contener letras y espacios.")],
                             render_kw={"placeholder": "Escribir apellido"})

    dni1 = StringField("DNI",
                       validators=[DataRequired(message="Por favor, ingrese el DNI del tutor."),
                                   Length(
                                       max=20, message="El DNI del tutor no puede superar los 20 caracteres."),
                                   Regexp(regex=r'^\d+$', message="El DNI del tutor olo puede contener números.")],
                       render_kw={"placeholder": "Ingrese el DNI"})

    current_address1 = StringField("Dirección",
                                   validators=[DataRequired(message="Por favor, ingrese la dirección actual del tutor."),
                                               Length(max=255, message="La dirección no puede superar los 255 caracteres.")],
                                   render_kw={"placeholder": "Escribir dirección actual del tutor"})

    mobile_phone1 = StringField("Teléfono",
                                validators=[DataRequired(message="Por favor, ingrese el teléfono del tutor."),
                                            Length(
                                                max=20, message="El teléfono del tutor no puede superar los 20 caracteres."),
                                            Regexp(regex=r'^\d+$', message="El teléfono del tutor solo puede contener números.")],
                                render_kw={"placeholder": "Ingrese el número de teléfono sin espacios ni guiones"})

    email1 = StringField("Correo electrónico",
                         validators=[Optional(),
                                     Email(
                                         message="Ingrese un correo electrónico válido."),
                                     Length(max=100, message="El correo electrónico no puede superar los 100 caracteres.")],
                         render_kw={"placeholder": "Escribir correo electrónico"})

    education_level1 = RadioField("Seleccione un nivel de educación", validators=[Optional()],
                                  choices=[('primario', 'Primario'), ('secundario', 'Secundario'), ('terciario', 'Terciario'), ('universitario', 'Universitario')])

    occupation1 = StringField("Ocupación",
                              validators=[Optional(),
                                          Length(
                                              max=100, message="La ocupación no puede superar los 100 caracteres."),
                                          Regexp(regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="La ocupación solo puede contener letras y espacios.")],
                              render_kw={"placeholder": "Ej: Profesor, Abogado"})

    # Campos para Tutor 2
    relationship2 = StringField("Parentesco",
                                validators=[
                                    Optional(),  # Agregado
                                    Length(
                                        max=50, message="La relación no puede superar los 50 caracteres."),
                                    Regexp(
                                        regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="La relación solo puede contener letras y espacios.")
                                ],
                                render_kw={"placeholder": "Ej: Padre, Madre, etc."})

    first_name2 = StringField("Nombre",
                              validators=[
                                  Optional(),  # Agregado
                                  Length(
                                      max=100, message="El nombre no puede superar los 100 caracteres."),
                                  Regexp(regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$',
                                         message="El nombre solo puede contener letras y espacios.")
                              ],
                              render_kw={"placeholder": "Escribir nombre"})

    last_name2 = StringField("Apellido",
                             validators=[
                                 Optional(),  # Agregado
                                 Length(
                                     max=100, message="El apellido no puede superar los 100 caracteres."),
                                 Regexp(regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$',
                                        message="El apellido solo puede contener letras y espacios.")
                             ],
                             render_kw={"placeholder": "Escribir apellido"})

    dni2 = StringField("DNI",
                       validators=[
                           Optional(),  # Agregado
                           Length(
                               max=20, message="El DNI no puede superar los 20 caracteres."),
                           Regexp(regex=r'^\d+$',
                                  message="El DNI solo puede contener números.")
                       ],
                       render_kw={"placeholder": "Ingrese el DNI"})

    current_address2 = StringField("Dirección actual",
                                   validators=[
                                       Optional(),  # Agregado
                                       Length(
                                           max=255, message="La dirección no puede superar los 255 caracteres.")
                                   ],
                                   render_kw={"placeholder": "Escribir dirección actual"})

    mobile_phone2 = StringField("Teléfono",
                                validators=[
                                    Optional(),  # Agregado
                                    Length(
                                        max=20, message="El teléfono no puede superar los 20 caracteres."),
                                    Regexp(
                                        regex=r'^\d+$', message="El teléfono solo puede contener números.")
                                ],
                                render_kw={"placeholder": "Ingrese el número de teléfono sin espacios ni guiones"})

    email2 = StringField("Correo electrónico",
                         validators=[
                             Optional(),  # Agregado
                             Email(message="Ingrese un correo electrónico válido."),
                             Length(
                                 max=100, message="El correo electrónico no puede superar los 100 caracteres.")
                         ],
                         render_kw={"placeholder": "Escribir correo electrónico"})

    education_level2 = RadioField("Seleccione un nivel de educación",
                                  validators=[Optional()],  # Agregado
                                  choices=[('primario', 'Primario'), ('secundario', 'Secundario'), ('terciario', 'Terciario'), ('universitario', 'Universitario')])

    occupation2 = StringField("Ocupación",
                              validators=[
                                  Optional(),  # Agregado
                                  Length(
                                      max=100, message="La ocupación no puede superar los 100 caracteres."),
                                  Regexp(regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$',
                                         message="La ocupación solo puede contener letras y espacios.")
                              ],
                              render_kw={"placeholder": "Ej: Profesor, Abogado"})

    # Trabajo en la instituciion
    work_proposal = SelectMultipleField("Propuesta de trabajo institucional",
                                        choices=[
                                            ("hipoterapia", "Hipoterapia"),
                                            ("montaTerapeutica",
                                             "Monta Terapéutica"),
                                            ("deporteEcuestreAdaptado",
                                             "Deporte Ecuestre Adaptado"),
                                            ("actividadesRecreativas",
                                             "Actividades Recreativas"),
                                            ("equitacion", "Equitación")
                                        ],
                                        coerce=str,
                                        option_widget=widgets.CheckboxInput(),
                                        widget=widgets.ListWidget(
                                            prefix_label=False)
                                        )

    condition = RadioField("Condición", validators=[Optional()], choices=[
                           ('regular', 'REGULAR'), ('deBaja', 'DE BAJA')])

    location = RadioField("Sede", validators=[Optional()], choices=[
                          ('casj', 'CASJ'), ('hlp', 'HLP'), ('otro', 'OTRO')])

    days = SelectMultipleField("Propuesta de trabajo institucional",
                               choices=[
                                   ("lunes", "Lunes"),
                                   ("martes", "Martes"),
                                   ("miercoles", "Miércoles"),
                                   ("jueves", "Jueves"),
                                   ("viernes", "Viernes"),
                                   ("sabado", "Sábado"),
                                   ("domingo", "Domingo")
                               ],
                               coerce=str,
                               option_widget=widgets.CheckboxInput(),
                               widget=widgets.ListWidget(prefix_label=False)
                               )

    submit = SubmitField("Enviar")

# NOTA: este formulario tiene 2 campos extras (status y comment) para la manipulacion solamente de EDICIÓN interna,
# no se muestran en la vista de usuario cuando envia la consulta.


class ConsultationForm(FlaskForm):
    """
    Descripción:
    Clase para el formulario de consulta.
    Usa types de Flask-WTF para crear un formulario de consulta.

    ---------
    Atributos:
    - full_name: StringField
        Campo de texto para el nombre completo.
        restricciones -> no nulo, longitud máxima de 100 caracteres

    - email: StringField
        Campo de texto para el correo electrónico.
        restricciones -> no nulo, correo electrónico válido

    - message: TextAreaField
        Campo de texto para el cuerpo del mensaje.
        restricciones -> no nulo

    - captcha: StringField
        Campo de texto para el captcha.
        restricciones -> no nulo, longitud de 6 caracteres

    - status: SelectField
        Campo de selección para el estado.
        restricciones -> no nulo

    - comment: TextAreaField
        Campo de texto para el comentario.
        restricciones -> longitud máxima de 255 caracteres

    - submit: SubmitField
        Botón de submit.

    ---------
    """
    full_name = StringField('Nombre completo', validators=[DataRequired(
        message="Este campo es obligatorio."), Length(max=100)])
    email = StringField('Correo electrónico', validators=[DataRequired(
        message="Este campo es obligatorio."), Email(message="Correo electrónico no válido.")])
    message = TextAreaField('Cuerpo del mensaje', validators=[
                            DataRequired(message="Este campo es obligatorio.")])
    captcha = StringField('Captcha', validators=[DataRequired(message="Este campo es obligatorio.")])
    status = SelectField('Estado', choices=[
        ('Pendiente', 'Pendiente'),
        ('En progreso', 'En progreso'),
        ('Descartado', 'Descartado'),
        ('Resuelto', 'Resuelto')
    ], validators=[DataRequired(message="Este campo es obligatorio.")])
    comment = TextAreaField('Comentario', validators=[Length(
        max=255, message="El comentario no puede superar los 255 caracteres.")])
    submit = SubmitField('Enviar')


class ContentPostForm(FlaskForm):
    """
    Descripción:
    Clase para el formulario de contenido.
    Usa types de Flask-WTF para crear un formulario de contenido.

    ---------
    Atributos:
    - title: str
        Campo para el titulo del contenido.
        restricciones ->  longitud máxima de 100 caracteres, no nulo

   - summary: str
        Campo para el copete del contenido.
        restricciones -> longitud máxima de 255 caracteres

    - content: str
        Campo para el cuerpo del contenido.
        restricciones -> longitud máxima de 1000 caracteres

    - submit: SubmitField
        Botón de submit.

    ---------
    """

    title = StringField("Título", validators=[Length(
        max=100, message="El título no puede exceder los 100 carácteres"), DataRequired(message="Por favor, ingrese un título.")], render_kw={"placeholder": "Ingrese un título"})
    summary = StringField("Copete", validators=[Length(
        max=255, message="El copete no puede exceder los 255 carácteres"), DataRequired(message="Por favor, ingrese un copete.")], render_kw={"placeholder": "Ingrese un copete"})
    content = StringField("Cuerpo del Contenido", validators=[Length(
        max=1000, message="El copete no puede exceder los 1000 carácteres"), DataRequired(message="Por favor, ingrese un contenido.")], render_kw={"placeholder": "Escriba el cuerpo del contenido"})

    submit = SubmitField("Enviar")
