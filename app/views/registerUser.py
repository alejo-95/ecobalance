from app.config.common import request, render_template, flash, Blueprint
from app.db.conectiondb import mysql
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
    
    cur = mysql.connection.cursor()
    cur.execute('Select name from users where name =  %s',(user,))
    repetitionUser = cur.fetchone()
    cur.execute('Select document from clients where document = %s',(document,))
    repetitionDoc = cur.fetchone()
    cur.close()
    
    if (not nameValidation(name) or 
        not nameValidation(lastname) or 
        not docValidation(document) or 
        not emailValidation(email) or 
        not telValidation(tel) or
        not userValdiation(user) or
        not passwordValidation(password)):
        flash('Datos invalidos, por favor intentelo nuevamente', 'danger')
        return render_template('index.html', name=name, lastname=lastname, document=document, email=email, tel=tel, user=user, password=password, openModal=True, registerUser=True)
    
    if repetitionUser:
        flash('El usuario ya existe, por favor intentelo nuevamente', 'danger')
        return render_template('index.html', name=name, lastname=lastname, document=document, email=email, tel=tel, user=user, password=password, openModal=True, registerUser=True)
    
    if repetitionDoc:
        flash('Ya existe un usuario con ese número de documento', 'danger')
        return render_template('index.html', name=name, lastname=lastname, document=document, email=email, tel=tel, user=user, password=password, openModal=True, registerUser=True)
        
    else:
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO clients (name, lastName, document, email, telephone, registerDate) VALUES (%s, %s, %s, %s, %s, current_timestamp)', (name, lastname, document, email, tel))
            cur.execute('INSERT INTO users (name, password, docNumb, idprofile) VALUES (%s, %s, %s, 2)', (user, password, document))
            mysql.connection.commit()
            cur.close()
            flash('Usuario registrado correctamente', 'success')
            return render_template('index.html', loginMessage= True)
        except Exception as ex:
            mysql.connection.rollback()
            flash(f'Ha ocurrido un error {ex}', 'warning')
            return render_template('index.html', loginMessage= True)
            
    
    