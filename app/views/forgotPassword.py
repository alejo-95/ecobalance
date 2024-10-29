from app.config.common import redirect, url_for, render_template, request, flash, random, timedelta, datetime, Blueprint, smtplib, config, mysql, MIMEText
from app.db.conectiondb import getConnection
from app.utils.validations import passwordValidation, emailValidation

bp = Blueprint('forgot-password', __name__,)

@bp.route('/forgot-password', methods=["POST", "GET"])
def forgot_password():
    if request.method == "POST":
        
        email = request.form['txtEmail']
        
        if not emailValidation(email):
            flash('Por favor, ingresa un correo electrónico válido.', 'danger')
            return render_template('views/sendMail.html', sendMessage=True)
        else:
            user = getUserByEmail(email)
        
        if not user:
            flash('El correo electrónico no está registrado.', 'danger')
            return render_template('views/sendMail.html', sendMessage=True)
        
        try:
            code = random.randint(100000, 999999)
            expiration = datetime.now() + timedelta(minutes=10)
            sendEmail(email, code)
            savePasswordCode(user, code, expiration)
            print(code, user, expiration)
        
            flash('Se ha enviado un código a su correo electrónico.', 'success')
            print('el usuario enviado a veri es', user)
            return redirect(url_for('forgot-password.code_verification', user_name=user))
        
        except Exception as e:
            flash(f'Ha ocurrido un error al enviar el correo electrónico{e}.', 'danger')
            print(e)
            return render_template('views/sendMail.html', sendMessage=True)
    
    return render_template('views/sendMail.html', sendMessage=False)

@bp.route('/code-verification', methods=["POST", "GET"])
def code_verification():
    user = request.args.get('user_name')
    #acá esta el problema
    if request.method == "POST":
        codeForm = request.form['txtCode']
        user = request.form.get('user_name')
        print('el usuario recueprado es', user)
        
        if not codeForm:
            flash('Por favor, ingresa el código de verificación.', 'danger')
            return render_template('views/verificationCode.html', codeMessage=True, user=user)
        else:
            passwordCode = getPasswordCode(user)
        
        if not passwordCode:
            flash('Códgio incorrecto', 'danger')
            return render_template('views/verificationCode.html', codeMessage=True, user=user)
        
        if  str(passwordCode) == str(codeForm.strip()):
            print('ok')
            return redirect(url_for('forgot-password.reset_password', user_name=user))
    
    return render_template('views/verificationCode.html', codeMessage=False, user=user)
    
@bp.route('/reset-password', methods=["POST", "GET"])
def reset_password():
    user = request.args.get('user_name')
    print('Usuario recuperado para guardar',user)
    if request.method == "POST":
        password1 = request.form['txtPassword1']
        password2 = request.form['txtPassword2']
        user = request.form.get('user_name')
        
        print('Usuario recuperado para guardar ok ok',user)
        print('contraseña 1',password1, 'contraseña 2', password2)
        
        if not passwordValidation(password1) or not passwordValidation(password2):
            flash('Las contraseñas no cumplen con los requisitos.', 'danger')
            return render_template('views/ressetPasword.html', resetMessage=True, user=user)
        
        if password1 != password2:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('views/ressetPasword.html', resetMessage=True, user=user)
        else:
            try:
                updatePassword(user,password1)
                flash('Contraseña actualizada correctamente.', 'success')
                return render_template('index.html', loginMessage=True)
            except Exception as e:
                flash('Ha ocurrido un error al actualizar la contraseña.', 'danger')
                return render_template('views/ressetPasword.html', resetMessage=True, user=user)
        
    return render_template('views/ressetPasword.html', resetMessage=False, user=user)
    
    
    
    
    

def sendEmail(email, code):
    user = config('EMAIL_USER')
    password = config('EMAIL_PASSWORD')

    subject = 'Código de verificación'
    message = f'Su código de verificación es: {code}'

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(user, password)
            server.send_message(msg)
        print(f'Código enviado a {email} correctamente.')
    except Exception as e:
        print(f'Error al enviar el correo: {e}')
        
def getUserByEmail(email):
    userEmail = None
    try:
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""Select u.name
                            FROM ecobalance.users u
                            INNER JOIN ecobalance.clients c on u.docNumb = c.document
                            WHERE c.email = %s;""", (email,))
        userEmail = cur.fetchone()
    except mysql.connector.Error as err:
        print("Error al obtener el usuario por correo electrónico:", err)
        conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return userEmail[0] if userEmail else None

def savePasswordCode(user, code, expiration):
    try:
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""INSERT INTO ecobalance.password_reset_codes (user, code, expiration) 
                    VALUES (%s, %s, %s)""", (user, code, expiration,))
        conn.commit()
        print(f'Se inserta {user,code,expiration}')
    except Exception as e:
        flash(f'Error al guardar el código de recuperación{e}.', 'danger')
        conn.rollback()
    finally:
        if conn:
            conn.close()
        if cur:
            cur.close()
        
    
def getPasswordCode(user):
    passWordCode = None
    try:
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""SELECT code
                            FROM ecobalance.password_reset_codes
                            WHERE user = %s
                                AND expiration > NOW()
                                AND TIMESTAMPDIFF(MINUTE, NOW(), expiration) <= 10
                            order by  expiration desc
                            limit 1""", (user,))
        passWordCode = cur.fetchone()
        print('el codigo es', passWordCode)
    except mysql.connector.Error as err:
        print("Error al obtener el código de recuperación:", err)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return passWordCode[0] if passWordCode else None

def updatePassword(user, newPassword):
    try:
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""UPDATE ecobalance.users SET password = %s WHERE name = %s""", (newPassword, user,))
        conn.commit()
    except mysql.connector.Error as err:
        print("Error al actualizar la contraseña:", err)
        conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    

    