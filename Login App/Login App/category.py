
from mysqloperations import insertData,getSingleData,updateData,getAllData,deleteData

def insertCategory(name):
    query = "insert into category(Name) values('"+name+"')"
    response = insertData(query)
    return response

def updateCategory(id,name):
    query = "update category set Name='"+name+"' where id="+str(id)
    response = updateData(query)
    return response

def deleteCategory(id):
    query = "delete from category where id="+str(id)
    response = deleteData(query)
    return response

def getCategoryById(id):
    query = "select * from category where id="+str(id)
    response = getSingleData(query)
    return response

def getAllCategory():
    query = "select * from category"
    response = getAllData(query)
    return response