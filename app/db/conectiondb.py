from app.config.common import MySQL, Flask 

mysql = MySQL()
    
def getConnection(app):
    app.config['MYSQL_HOST']='localhost'
    app.config['MYSQL_USER']='root'
    app.config['MYSQL_PASSWORD']='Alejodev1995'
    app.config['MYSQL_DB']='ecobalance'
    app.config['MYSQL_CURSORCLASS']='DictCursor'
    
    mysql.init_app(app)

