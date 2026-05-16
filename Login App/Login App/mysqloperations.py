
import mysqlconnection

def insertData(query):
    try:
        connect = mysqlconnection.connect_mysql()
        if not(connect is None):
            if connect.open:
                with connect.cursor() as cur:
                    cur.execute(query)
                    connect.commit()
                    return "success"
            else:
                return "connection closed"
        else:
            return "failed"
    except Exception as e:
        return e

def updateData(query):
    try:
        connect = mysqlconnection.connect_mysql()
        if not(connect is None):
            if connect.open:
                with connect.cursor() as cur:
                    cur.execute(query)
                    connect.commit()
                    return "success"
            else:
                return "connection closed"
        else:
            return "failed"
    except Exception as e:
        return e

def deleteData(query):
    try:
        connect = mysqlconnection.connect_mysql()
        if not(connect is None):
            if connect.open:
                with connect.cursor() as cur:
                    cur.execute(query)
                    connect.commit()
                    return "success"
            else:
                return "connection closed"
        else:
            return "failed"
    except Exception as e:
        return e
    
def getAllData(query):
    try:
        connect = mysqlconnection.connect_mysql()
        if not(connect is None):
            if connect.open:
                with connect.cursor() as cur:
                    cur.execute(query)
                    data = cur.fetchall()
                    return data
            else:
                return "connection closed"
        else:
            return "failed"
    except Exception as e:
        return e

def getSingleData(query):
    try:
        connect = mysqlconnection.connect_mysql()
        if not(connect is None):
            if connect.open:
                with connect.cursor() as cur:
                    cur.execute(query)
                    data = cur.fetchone()
                    if not(data is None):
                        return data
                    else:
                        return "not found"
            else:
                return "connection closed"
        else:
            return "failed"
    except Exception as e:
        return "error"
            
