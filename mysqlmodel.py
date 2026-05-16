from mysqlconnection import connection

#insert,update,delete
def IUD(query):
    with connection.cursor() as cur:
     response_data={}
     try:
        cur.execute(query)
        connection.commit() # store data permanently on database
        response_data={"status":"success"}
     except Exception as e:
        response_data={"status":"failed","error":e}
     finally:
        connection.close()
        return response_data


#fetch all data 
def get_all(query):
    with connection.cursor() as cur:
     response_data={}
     try:
        cur.execute(query)
        data=cur.fetchall()
        response_data={"status":"success" ,"data":data}
     except Exception as e:
        response_data={"status":"failed","error":e}
     finally:
        connection.close()
        return response_data

#fetch only one data 
def get_one(query):
    with connection.cursor() as cur:
     response_data={}
     try:
        cur.execute(query)
        data=cur.fetchone()
        response_data={"status":"success" ,"data":data}
     except Exception as e:
        response_data={"status":"failed","error":e}
     finally:
        connection.close()
        return response_data