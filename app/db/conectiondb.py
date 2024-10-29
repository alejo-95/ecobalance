from app.config.common import mysql, config
    
def getConnection():
    connection = mysql.connector.connect(
        host = config("MYSQL_HOST"),
        user = config("MYSQL_USER"),
        password = config("MYSQL_PASSWORD"),
        database = config("MYSQL_DB"),
    )
    return connection
    
    

