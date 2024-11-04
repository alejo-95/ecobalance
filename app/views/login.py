from app.config.common import request, render_template, session, flash, Blueprint, mysql
from app.db.conectiondb import getConnection

bp = Blueprint('login', __name__, url_prefix='/login')

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/acces-login', methods=["GET","POST"])
def login():
    
    if request.method == 'POST' and 'txtUser' in request.form and 'txtPassword' in request.form:
        _email = request.form['txtUser']
        _password = request.form['txtPassword']
        
        account = userValidation(_email,_password)
        
        if account:
            session['logueado'] = True
            session['ididusers']= account['idusers']
            session['idprofile'] = account['idprofile']
            session['name'] = account['name']
            return render_template("views/menu3.html")
        
        else:
            flash('El usuario y/o la contraseña son incorrectos', 'danger')
            return render_template('index.html', loginMessage=True)
        
def userValidation(email, password):
    try:
        connection = getConnection()
        cur = connection.cursor(dictionary=True)
        cur.execute('SELECT * FROM users WHERE name = %s AND password = %s', (email, password,))
        user = cur.fetchone()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
    finally:
        if cur:
            cur.close()
        if connection:
            connection.close()
    return user
