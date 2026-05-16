from flask import Flask,render_template,session,request,make_response,redirect,url_for
from mysqlconnection import connection

prac=Flask(__name__)

prac.secret_key="sandeep26"


@prac.route("/")
def index():
    return render_template("/index.html")

@prac.route("/login", methods=["POST", "GET"])
def login():
    if  request.method == "POST":
        email=request.form.get("email")
        password=request.form.get("password")
        
        try:
            if not connection.open:
                connection.ping(reconnect=True)

            query = "SELECT * FROM tsb_regs_record WHERE Email=%s"
            
            with connection.cursor() as cur:
                cur.execute(query, (email,))
                user = cur.fetchone()

            if user is None:
                return render_template("login.html", message="Invalid username.")

            if password == user[4]:
                session["user"] = user
                return redirect(url_for("dashboard"))
            else:
                return render_template("login.html", message="Invalid password.")

        except Exception as e:
            print("Login Error:", e)
            return render_template("login.html", message="Something went wrong!")
    return render_template("/login.html")



@prac.route("/dashboard")
def dashboard():
     if len(session)!=0:
        if session["user"] is not None:
            user = session["user"]
            return render_template("dashboard.html",email=user[1])
        return redirect (url_for("login"))


if __name__ == '__main__':
    prac.run(debug=True)