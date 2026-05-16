import pymysql


db_host="localhost"
db_name="the_smart_bazaar"
db_username="root"
db_password=""

connection = pymysql.connect(
    host=db_host,
    database=db_name,
    
    user=db_username,
    password=db_password
    )

if connection.open:
    print("database connected successfully")
else:
    ("something went wrong")