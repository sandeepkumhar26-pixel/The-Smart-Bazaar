
from mysqloperations import getSingleData

def user_login(username,password):
    query="select * from users where email='"+username+"'"
    user_data = getSingleData(query)
    if type(user_data).__name__!="str":
        if password==user_data[4]:
            return user_data
        else:
            return "invalid credentials"
    else:
        return user_data
