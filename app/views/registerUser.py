from app.config.common import request, render_template, flash, Blueprint, mysql
from app.db.conectiondb import getConnection
from app.utils.validations import nameValidation, docValidation, emailValidation, telValidation, userValdiation, passwordValidation

bp = Blueprint('registerUser', __name__,)

@bp.route('/registerUser', methods=["GET","POST"])
def registerUser():
    name = request.form['txtName']
    lastname = request.form['txtLastName']
    document = request.form['txtDocument']
    email = request.form['txtMail']
    tel = request.form['txtTel']
    
    user = request.form['txtUser']
    password = request.form['txtPassword']
    
    if (not nameValidation(name) or 
        not nameValidation(lastname) or 
        not docValidation(document) or 
        not emailValidation(email) or 
        not telValidation(tel) or
        not userValdiation(user) or
        not passwordValidation(password)):
        flash('Datos invalidos, por favor intentelo nuevamente', 'danger')
        return render_template('index.html', name=name, lastname=lastname, document=document, email=email, tel=tel, user=user, password=password, openModal=True, registerUser=True)
    
    if getUserValidation(user):
        flash('El usuario ya existe, por favor intentelo nuevamente', 'danger')
        return render_template('index.html', name=name, lastname=lastname, document=document, email=email, tel=tel, user=user, password=password, openModal=True, registerUser=True)
    
    if getUserDoc(document):
        flash('Ya existe un usuario con ese número de documento', 'danger')
        return render_template('index.html', name=name, lastname=lastname, document=document, email=email, tel=tel, user=user, password=password, openModal=True, registerUser=True)
    
    if getUserEmail(email):
        flash('Ya existe un usuario con ese correo', 'danger')
        return render_template('index.html', name=name, lastname=lastname, document=document, email=email, tel=tel, user=user, password=password, openModal=True, registerUser=True)
        
    else:
        conn = getConnection()
        try:
            saveClient(name, lastname, document, email, tel)
            saveUser(user, password, document)
            flash('Usuario registrado correctamente', 'success')
            return render_template('index.html', loginMessage= True)
        except Exception as ex:
            conn.rollback()
            flash(f'Ha ocurrido un error {ex}', 'warning')
            return render_template('index.html', loginMessage= True)
        finally:
            conn.close()
            
def getUserValidation(user):
    try:
        connection = getConnection()
        cur = connection.cursor()
        cur.execute('Select name from users where name =  %s',(user,))
        repetitionUser = cur.fetchone()
    except mysql.connector.Error as error:
        print(f'Error al consultar el usuario: {error}')
        connection.rollback()
    finally:
        if connection:
            connection.close()
        if cur:
            cur.close()
    return repetitionUser

def getUserDoc(document):
    try:
        connection = getConnection()
        cur = connection.cursor()
        cur.execute('Select document from clients where document = %s',(document,))
        repetitionDoc = cur.fetchone()
        cur.close()
    except mysql.connector.Error as error:
        print(f'Error al consultar el documento: {error}')
        connection.rollback()
    finally:
        if connection:
            connection.close()
        if cur:
            cur.close()
    return repetitionDoc

def getUserEmail(email):
    try:
        connection = getConnection()
        cur = connection.cursor()
        cur.execute('Select email from clients where email = %s',(email,))
        repetitionEmail = cur.fetchone()
        cur.close()
    except mysql.connector.Error as error:
        print(f'Error al consultar el correo: {error}')
        connection.rollback()
    finally:
        if connection:
            connection.close()
        if cur:
            cur.close()
    return repetitionEmail

def saveClient(name, lastname, document, email, tel):
    try:   
        conn = getConnection()
        cur = conn.cursor()
        cur.execute('INSERT INTO clients (name, lastName, document, email, telephone, registerDate) VALUES (%s, %s, %s, %s, %s, current_timestamp)', (name, lastname, document, email, tel))
        conn.commit()
    except mysql.connector.Error as error:
        print(f'Error al guardar el cliente: {error}')
        conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    
def saveUser(user, password, document):
    try:
        conn = getConnection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (name, password, docNumb, idprofile) VALUES (%s, %s, %s, 2)', (user, password, document))
        conn.commit()
    except mysql.connector.Error as error:
        print(f'Error al guardar el usuario: {error}')
        conn.rollback()
    finally:
        if conn:
            conn.close()
        if cur:    
            cur.close()
    