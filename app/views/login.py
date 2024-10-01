from app.config.common import request, render_template, session, flash, Blueprint
from app.db.conectiondb import mysql

bp = Blueprint('login', __name__, url_prefix='/login')

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/acces-login', methods=["GET","POST"])
def login():
    
    if request.method == 'POST' and 'txtUser' in request.form and 'txtPassword' in request.form:
        _correo = request.form['txtUser']
        _password = request.form['txtPassword']
        
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE name = %s AND password = %s ',(_correo, _password,))
        account = cur.fetchone()
        cur.close()
        
        if account:
            session['logueado'] = True
            session['ididusers']= account['idusers']
            session['idprofile'] = account['idprofile']
            #session['cliente'] = account['cliente']
            return render_template("views/menu.html")
        
        else:
            flash('El usuario y/o la contraseña son incorrectos', 'danger')
            return render_template('index.html')