from app.config.common import Blueprint, render_template

bp = Blueprint('ecobalance', __name__,)

@bp.route('/ecobalance')
def ecobalance():
    return render_template("views/menu3.html")