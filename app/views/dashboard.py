from app.config.common import render_template, jsonify, Blueprint
from app.db.conectiondb import getConnection

bp = Blueprint('dashboard', __name__,)

@bp.route('/historico')
def dashboard():
    return render_template('views/dashboard.html')

@bp.route('/historico/data')
def data():
    try:
        
        
        rows = historicData()
        if not rows:
            return jsonify({'error': 'No hay datos para mostrar'})

        data_all = {
            'labels': [row['day'] for row in rows],
            'values': [row['point'] for row in rows]
        }

        rowsMax = maxPointData()
        
        if not rowsMax:
            return jsonify({'error': 'No se encuentran datos'})

        data_max = {
            'labels': [row['day'] for row in rowsMax],
            'values': [row['point'] for row in rowsMax]
        }
        
        rowsMin = minPointData()           

        if not rowsMin:
            return jsonify({'error': 'No se encuentran datos'})

        data_min = {
            'labels': [row['day'] for row in rowsMin],
            'values': [row['point'] for row in rowsMin]
        }

        return jsonify({'all': data_all, 'max': data_max, 'min': data_min})

    except Exception as e:
        return jsonify({'error': str(e)})
    
    
def historicData():
    try:
        conn = getConnection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    SELECT
                        DATE_FORMAT(date_register, '%Y-%m-%d') AS day,
                            point
                        FROM
                            point_data
                        WHERE
                            date_register between '2024-09-01 00:00:01' and '2024-12-31 11:59:00'
                        GROUP BY
                            day,
                            point
                        Order by 1 asc
                    """)
        data = cur.fetchall()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()
    return data

def maxPointData():
    try:
        conn = getConnection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    SELECT
                        DATE_FORMAT(date_register, '%Y-%m-%d') AS day,
                        point
                        FROM
                            point_data
                        WHERE
                            date_register between '2024-09-01 00:00:01' and '2024-12-31 11:59:00'
                        GROUP BY
                            day,
                            point
                        order by point desc
                        limit 1
                    """)
        maxTemp = cur.fetchall()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()
    return maxTemp
    

def minPointData():
    try:
        conn = getConnection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    SELECT
                        DATE_FORMAT(date_register, '%Y-%m-%d') AS day,
                        point
                        FROM
                            point_data
                        WHERE
                            date_register between '2024-09-01 00:00:01' and '2024-12-31 11:59:00'
                        GROUP BY
                            day,
                            point
                        order by point
                        limit 1
                    """)
        minTemp = cur.fetchall()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()
    return minTemp
    
        