from app import create_app
from app.config.common import redirect, url_for

app = create_app()

if __name__ == "__main__":
    app.secret_key="projectoEcobalance"
    
    @app.route('/')
    def redirect_to_home():
        return redirect(url_for('login.home'))
    
    app.run(debug=True, host='0.0.0.0')