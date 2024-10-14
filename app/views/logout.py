from app.config.common import request, render_template, session, flash, Blueprint

bp = Blueprint('logout', __name__,)

@bp.route('/logout')
def logout():
    session.clear()
    flash('Te has desconectado con exito', 'success')
    return render_template('index.html', loginMessage=True)