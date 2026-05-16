import pymysql

def connect_mysql():
    server_name = "localhost"
    db_name = "the_smart_bazaar"
    db_username = "root"
    db_password=""
    try:
        connect = pymysql.connect(host=server_name,
                                database=db_name,
                                user=db_username,
                                password=db_password)
        return connect
    except Exception as e:
        return None