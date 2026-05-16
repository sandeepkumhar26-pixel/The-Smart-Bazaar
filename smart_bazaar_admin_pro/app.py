from flask import Flask, render_template, request, redirect, session, flash, g
import pymysql
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = "smartbazaar_secret"

# ================= DATABASE CONNECTION =================
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="the_smart_bazaar",
        cursorclass=pymysql.cursors.DictCursor
    )

# ================= UPLOAD CONFIG =================
UPLOAD_FOLDER = "static/images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ================= LOGIN REQUIRED =================
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "admin" not in session:
            return redirect("/")
        return func(*args, **kwargs)
    return wrapper

# ================= GLOBAL DATA =================
@app.before_request
def load_global_data():
    g.categoryList = []
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM categories")
        g.categoryList = cur.fetchall()
        con.close()
    except Exception as e:
        print("Category Load Error:", e)
        g.categoryList = []

# ================= ADMIN LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM admins WHERE email=%s AND password=%s", (email, password))
        admin = cur.fetchone()
        con.close()

        if admin:
            session["admin"] = admin["email"]
            return redirect("/admindashboard")
        else:
            flash("Invalid login credentials")

    return render_template("adminlogin.html")

# ================= DASHBOARD =================
@app.route("/admindashboard")
@login_required
def dashboard():
    return render_template("admindashboard.html")

# ================= ADD CATEGORY =================
@app.route("/add-category", methods=["GET", "POST"])
@login_required
def add_category():
    if request.method == "POST":
        name = request.form["name"]

        con = get_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO categories(name) VALUES(%s)", (name,))
        con.commit()
        con.close()

        flash("✅ Category added successfully")
        return redirect("/add-category")

    return render_template("add_category.html")

# ================= ADD PRODUCT =================
@app.route('/add-product', methods=['GET','POST'])
@login_required
def add_product():

    con = get_connection()
    cur = con.cursor()

    # categories fetch
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        category_id = request.form['category_id']

        image = request.files['image']
        filename = image.filename

        # Save image
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Insert product
        cur.execute("""
        INSERT INTO products(name,description,price,image,category_id)
        VALUES(%s,%s,%s,%s,%s)
        """,(name,description,price,filename,category_id))

        con.commit()
        con.close()

        flash("✅ Product Added Successfully")
        return redirect("/add-product")

    return render_template("add_product.html", categories=categories)

# ================= USER HOME =================
@app.route("/home")
def home():
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
    SELECT products.*, categories.name as category_name 
    FROM products 
    JOIN categories ON products.category_id = categories.id
    """)
    products = cur.fetchall()
    con.close()

    return render_template("home.html", products=products)

# ================= CATEGORY FILTER =================
@app.route("/category/<int:cid>")
def category_products(cid):
    con = get_connection()
    cur = con.cursor()

    cur.execute("SELECT * FROM products WHERE category_id=%s", (cid,))
    products = cur.fetchall()
    con.close()

    return render_template("home.html", products=products)

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)