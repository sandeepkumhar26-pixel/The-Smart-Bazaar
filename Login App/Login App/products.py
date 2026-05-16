
from mysqloperations import insertData,getAllData,getSingleData,updateData

def insertProduct(name,categoryId,productImage,amount,productDescription):
    query = "insert into product(Name,Product_image,Category_id,Price,Product_description) values('"+name+"','"+productImage+"',"+categoryId+","+amount+",'"+productDescription+"')"
    response = insertData(query)
    return response

def updateProduct(id,name,categoryId,productImage,amount,productDescription):
    query = "update product set Name='"+name+"',Product_image='"+productImage+"',Category_id="+categoryId+",Price="+amount+",Product_description='"+productDescription+"' where id="+str(id)
    response = updateData(query)
    return response

def getAllProductForAdmin():
    query = "SELECT p.Id,p.Name,p.Product_image,c.Name as CategoryName,p.Price,p.Product_description FROM product p inner join category c on p.Category_id=c.Id"
    response = getAllData(query)
    return response

def getProductById(id):
    query = "SELECT * FROM product where id="+str(id)
    response = getSingleData(query)
    return response

