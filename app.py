from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify
import pymysql
from dotenv import load_dotenv
import os
import os
import random
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import razorpay

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------------- DB ----------------
def db():
    return pymysql.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )
# ---------------- HOME ----------------
@app.route("/")
def index():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM product ORDER BY RAND() LIMIT 16")
    products = cur.fetchall()
    conn.close()
    return render_template("index.html", products=products)

@app.route('/category/<int:cat_id>')
def category_redirect(cat_id):
    return redirect(f"/products/{cat_id}")

@app.route("/home")
def home():
    return redirect("/")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        conn = db()
        cur = conn.cursor()
        try:
            password = generate_password_hash(request.form["password"])

            cur.execute(
        "INSERT INTO tsb_regs_record(fullname,email,mobile,password) VALUES(%s,%s,%s,%s)",
        (
            request.form["fullname"],
            request.form["email"],
            request.form["mobile"],
            password
        )
)
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            flash("Email already exists")
            conn.close()
    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = db()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM tsb_regs_record WHERE email=%s",
            (request.form["email"],)
        )
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], request.form["password"]):
            session["user"] = user["id"]
            return redirect("/")
        else:
            flash("Invalid Email or Password")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)   # user session remove
    session.pop("cart", None)   # optional (cart clear)
    return redirect("/login")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tsb_regs_record WHERE id=%s", (session["user"],))
    user = cur.fetchone()
    conn.close()

    return render_template("dashboard.html", email=user["email"])

# ---------------- STATIC ----------------
@app.route("/contactus", methods=["GET", "POST"])
def contactus():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # yaha DB me save kar sakte ho
        print(name, email, message)

        return redirect("/feedback")  # success page

    return render_template("contactus.html")

@app.route("/category/<category_name>")
def category(category_name):
    return render_template("slug.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/orders")
def orders():
    if "user" not in session:
        return redirect("/login")

    conn = db()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM orders
        WHERE user_id=%s
        ORDER BY id DESC
    """, (session["user"],))

    data = cur.fetchall()
    conn.close()

    return render_template("orders.html", orders=data)

@app.route("/forget")
def forget():
    return render_template("forget.html")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")




# ---------------- SHOP ----------------
@app.route("/shop")
def shop():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM category")
    category_data = cur.fetchall()
    conn.close()
    return render_template("shop.html", category_data=category_data)

# ---------------- CATEGORY VIEW ----------------
@app.route("/category")
def get_all():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM category")
    data = cur.fetchall()
    conn.close()

    category_list = []
    for i in data:
        category_list.append({"ID": i["id"], "Name": i["name"]})

    return render_template("category.html", category_data=category_list)

# ---------------- PRODUCTS ----------------
@app.route("/products/<int:cat_id>")
def products(cat_id):
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM product WHERE category_id=%s", (cat_id,))
    products = cur.fetchall()

    return render_template("products.html", products=products,cat_id=cat_id)
@app.route("/home-furniture")
def home_furniture():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM product WHERE category_id=%s", (3,))
    products = cur.fetchall()
    conn.close()
    return render_template("home_furniture.html", products=products,)

# ---------------- CART ----------------
@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    items = []
    total = 0

    if cart:
        conn = db()
        cur = conn.cursor(pymysql.cursors.DictCursor)

        for pid, qty in cart.items():
            cur.execute("SELECT id, name, price, image FROM product WHERE id=%s", (pid,))
            p = cur.fetchone()

            if p:
                p["qty"] = qty
                p["subtotal"] = qty * float(p["price"])
                items.append(p)
                total += p["subtotal"]

        conn.close()

    return render_template("cart.html", items=items, total=total)

@app.route("/add-to-cart/<int:pid>")
def add_to_cart(pid):

    if "user" not in session:
        return jsonify({"status": "login_required"})

    # 🔥 FIX: ensure cart dict ho
    if "cart" not in session or not isinstance(session["cart"], dict):
        session["cart"] = {}

    cart = session["cart"]
    pid = str(pid)

    if pid in cart:
        cart[pid] += 1
    else:
        cart[pid] = 1

    session["cart"] = cart
    session.modified = True

    return jsonify({"status": "success"})

@app.route("/increase/<int:pid>")
def increase(pid):
    cart = session.get("cart", {})
    pid = str(pid)

    if pid in cart:
        cart[pid] += 1

    session["cart"] = cart
    session.modified = True
    return redirect("/cart")


@app.route("/decrease/<int:pid>")
def decrease(pid):
    cart = session.get("cart", {})
    pid = str(pid)

    if pid in cart:
        cart[pid] -= 1

        if cart[pid] <= 0:
            del cart[pid]

    session["cart"] = cart
    session.modified = True
    return redirect("/cart")

# ---------------- BUY NOW ----------------
@app.route("/buy-now/<int:pid>")
def buy_now(pid):
    session["buy_now"] = pid
    return redirect("/checkout")

# ---------------- CHECKOUT ----------------
@app.route("/checkout")
def checkout():
    if "user" not in session:
        return redirect("/login")

    conn = db()
    cur = conn.cursor()

    products = []
    total = 0

    if session.get("buy_now"):
        pid = session["buy_now"]
        cur.execute("SELECT * FROM product WHERE id=%s", (pid,))
        p = cur.fetchone()
        if p:
            products.append(p)
            total += int(p["price"])

    elif session.get("cart"):
        for pid in session["cart"]:
            cur.execute("SELECT * FROM product WHERE id=%s", (pid,))
            p = cur.fetchone()
            if p:
                products.append(p)
                total += int(p["price"])

    conn.close()

    if not products:
        return "No product selected ❌"

    return render_template("checkout.html", products=products, total=total)


KEY_ID = os.getenv("RAZORPAY_KEY")
SECRET = os.getenv("RAZORPAY_SECRET")

client = razorpay.Client(auth=(KEY_ID, SECRET))


# ✅ Payment Page (GET)
@app.route("/payment")
def payment():
    return render_template("payment.html")


# ✅ Create Order (POST only)
@app.route("/create-order", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data or "amount" not in data:
        return jsonify({"error": "Invalid data"}), 400

    amount = int(data["amount"]) * 100  # ₹ to paise

    order = client.order.create({
        "amount": amount,
        "currency": "INR"
    })

    return jsonify(order)


# ✅ Verify Payment (POST only)
@app.route("/verify-payment", methods=["POST"])
def verify_payment():
    data = request.get_json()

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": data.get("razorpay_order_id"),
            "razorpay_payment_id": data.get("razorpay_payment_id"),
            "razorpay_signature": data.get("razorpay_signature")
        })
        return jsonify({"status": "success"})
    except Exception as e:
        print("VERIFY ERROR:", e)
        return jsonify({"status": "failed"})


@app.route('/product/<int:pid>')
def product_detail(pid):
    conn = db()
    cur = conn.cursor()

    # PRODUCT + CATEGORY NAME
    cur.execute("""
        SELECT p.*, c.name AS category_name
        FROM product p
        LEFT JOIN category c ON p.category_id = c.id
        WHERE p.id=%s
    """, (pid,))
    product = cur.fetchone()

    # RELATED PRODUCTS (IMPORTANT FIX)
    cur.execute("""
        SELECT * FROM product 
        WHERE category_id=%s AND id!=%s LIMIT 6
    """, (product['category_id'], pid))
    related = cur.fetchall()

    return render_template("prod_detail.html", product=product, related=related)



# ---------------- PLACE ORDER ----------------
@app.route("/place_order", methods=["POST"])
def place_order():

    if "user" not in session:
        return redirect("/login")

    name = request.form.get("name")
    mobile = request.form.get("mobile")
    address = request.form.get("address")
    payment = request.form.get("payment")

    conn = db()
    cur = conn.cursor()

    total = 0
    products = []

    order_id = "ORD" + str(random.randint(10000, 99999))

    # CART
    if session.get("cart"):
        for pid in session["cart"]:
            cur.execute("SELECT * FROM product WHERE id=%s", (pid,))
            p = cur.fetchone()

            if p:
                products.append({
                    "name": p["name"],
                    "image": p["image"]
                })
                total += int(p["price"])

    # BUY NOW
    elif session.get("buy_now"):
        pid = session["buy_now"]
        cur.execute("SELECT * FROM product WHERE id=%s", (pid,))
        p = cur.fetchone()

        if p:
            products.append({
                "name": p["name"],
                "image": p["image"]
            })
            total += int(p["price"])

    if not products:
        conn.close()
        return "No product ❌"

    # 🔥 TRY-EXCEPT START
    try:
        cur.execute("""
            INSERT INTO orders
            (order_id, user_id, product_name, total_amount, payment_method, address, mobile, image, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            order_id,
            session["user"],
            ",".join([p["name"] for p in products]),
            total,
            payment,
            address,
            mobile,
            products[0]["image"],
            "Pending"
        ))

        conn.commit()
        print("✅ ORDER SAVED IN DB")

    except Exception as e:
        print("❌ DB ERROR:", e)
        return "Database Error ❌"

    finally:
        conn.close()
    # 🔥 TRY-EXCEPT END

    # SAVE FOR SUCCESS PAGE
    session["last_order"] = {
        "order_id": order_id,
        "products": products,
        "total": total
    }

    return redirect("/order_success")

# ---------------- ORDER SUCCESS ----------------
@app.route("/order_success")
def order_success():

    if "user" not in session:
        return redirect("/login")

    order = session.get("last_order")

    if not order:
        return "No recent order ❌"

    # CLEAR CART AFTER SUCCESS
    session.pop("cart", None)
    session.pop("buy_now", None)

    return render_template(
        "order_success.html",
        order_id=order["order_id"],
        products=order["products"],
        total=order["total"]
    )
@app.route("/cancel-order/<int:id>")
def cancel_order(id):

    if "user" not in session:
        return redirect("/login")

    conn = db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE orders 
        SET status='Cancelled'
        WHERE id=%s AND user_id=%s
    """, (id, session["user"]))

    conn.commit()
    conn.close()

    return redirect("/orders")
@app.route("/delete-order/<int:id>")
def delete_order(id):

    if "user" not in session:
        return redirect("/login")

    conn = db()
    cur = conn.cursor()

    cur.execute("DELETE FROM orders WHERE id=%s AND user_id=%s",
                (id, session["user"]))

    conn.commit()
    conn.close()

    return redirect("/orders")


@app.route("/cartcleared")
def cartcleared():
    session.pop("cart", None)
    return render_template("cartcleared.html")
@app.route("/search")
def search():

    q = request.args.get("q")

    conn = db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM product WHERE name LIKE %s",
        ('%' + q + '%',)
    )

    products = cur.fetchall()

    print(q)
    print(products)

    conn.close()

    return render_template(
        "products.html",
        products=products
    )

@app.route("/filter/<int:cat_id>")
def filter_products(cat_id):

    sort = request.args.get("sort")

    conn = db()
    cur = conn.cursor()

    query = """
        SELECT * FROM product
        WHERE category_id=%s
    """

    if sort == "low-high":

        query += " ORDER BY price ASC"

    elif sort == "high-low":

        query += " ORDER BY price DESC"

    elif sort == "a-z":

        query += " ORDER BY name ASC"

    elif sort == "z-a":

        query += " ORDER BY name DESC"

    cur.execute(query, (cat_id,))

    products = cur.fetchall()

    conn.close()

    return render_template(
        "products.html",
        products=products,
        cat_id=cat_id
    )

@app.route("/add-wishlist/<int:pid>")
def add_wishlist(pid):

    if "user" not in session:
        return jsonify({"status":"login_required"})

    conn = db()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM wishlist
        WHERE user_id=%s AND product_id=%s
    """, (session["user"], pid))

    exist = cur.fetchone()

    if not exist:

        cur.execute("""
            INSERT INTO wishlist(user_id, product_id)
            VALUES(%s,%s)
        """, (session["user"], pid))

        conn.commit()

    conn.close()

    return jsonify({"status":"success"})

@app.route("/wishlist")
def wishlist():

    # LOGIN CHECK
    if "user" not in session:
        return redirect("/login")

    conn = db()
    cur = conn.cursor()

    # FETCH PRODUCTS
    cur.execute("""
        SELECT p.*
        FROM wishlist w
        JOIN product p
        ON w.product_id = p.id
        WHERE w.user_id=%s
    """, (session["user"],))

    products = cur.fetchall()

    conn.close()

    return render_template(
        "wishlist.html",
        products=products
    )

@app.route("/remove-wishlist/<int:pid>")
def remove_wishlist(pid):

    if "user" not in session:
        return redirect("/login")

    conn = db()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM wishlist
        WHERE user_id=%s AND product_id=%s
    """, (session["user"], pid))

    conn.commit()
    conn.close()

    return redirect("/wishlist")
# ---------------- ADMIN ----------------
@app.route("/adminlogin", methods=["GET", "POST"])
def adminlogin():
    if request.method == "POST":
        conn = db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin WHERE username=%s AND password=%s",
                    (request.form["username"], request.form["password"]))
        admin = cur.fetchone()
        conn.close()

        if admin:
            session["admin"] = request.form["username"]
            return redirect("/admindashboard")
        else:
            flash("Invalid Login")

    return render_template("adminlogin.html")

@app.route("/admindashboard")
def admindashboard():
    if "admin" not in session:
        return redirect("/")
    return render_template("admindashboard.html")

@app.route("/add-category", methods=["GET", "POST"])
def add_category():
    conn = db()
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form.get("name")
        file = request.files.get("image")

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = ""

        cur.execute(
            "INSERT INTO category(name, image) VALUES(%s, %s)",
            (name, filename)
        )
        conn.commit()

        return redirect("/manage-category")

    return render_template("add_category.html")

# ---------------- MANAGE CATEGORY ----------------
@app.route("/manage-category")
def manage_category():
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM category")
    data = cur.fetchall()

    return render_template("manage_category.html", category_data=data)

@app.route("/delete-category/<int:id>")
def delete_category(id):
    conn = db()
    cur = conn.cursor()
    cur.execute("DELETE FROM category WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect("/manage-category")

# ---------------- PRODUCT CRUD ----------------
@app.route("/manage-product")
def manage_product():
    conn = db()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.id, p.name, p.price, p.image, c.name as category
        FROM product p
        LEFT JOIN category c ON p.category_id = c.id
    """)
    products = cur.fetchall()
    conn.close()

    return render_template("manage_product.html", products=products)

@app.route("/delete-product/<int:id>")
def delete_product(id):
    conn = db()
    cur = conn.cursor()
    cur.execute("DELETE FROM product WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect("/manage-product")

# ---------------- ADD PRODUCT ----------------
@app.route("/add-product", methods=["GET", "POST"])
def add_product():
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM category")
    categories = cur.fetchall()

    if request.method == "POST":
        file = request.files["image"]
        filename = secure_filename(file.filename)

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        file.save(os.path.join(UPLOAD_FOLDER, filename))

        cur.execute("""
            INSERT INTO product(name,price,description,image,category_id)
            VALUES(%s,%s,%s,%s,%s)
        """, (
            request.form["name"],
            request.form["price"],
            request.form["description"],
            filename,
            request.form["category"]
        ))

        conn.commit()

    conn.close()
    return render_template("add_product.html", categories=categories)

@app.route("/edit-product/<int:id>", methods=["GET","POST"])
def edit_product(id):
    conn = db()
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]
        category = request.form["category"]

        # check image upload
        if "image" in request.files and request.files["image"].filename != "":
            file = request.files["image"]
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cur.execute("""
                UPDATE product 
                SET name=%s, price=%s, description=%s, image=%s, category_id=%s
                WHERE id=%s
            """, (name, price, description, filename, category, id))
        else:
            cur.execute("""
                UPDATE product 
                SET name=%s, price=%s, description=%s, category_id=%s
                WHERE id=%s
            """, (name, price, description, category, id))

        conn.commit()
        conn.close()
        return redirect("/manage-product")

    # GET request
    cur.execute("SELECT * FROM product WHERE id=%s", (id,))
    product = cur.fetchone()

    cur.execute("SELECT * FROM category")
    categories = cur.fetchall()

    conn.close()

    return render_template("edit_product.html", product=product, categories=categories)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run()
