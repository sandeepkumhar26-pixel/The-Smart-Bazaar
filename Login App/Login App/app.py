from flask import Flask, render_template, request, redirect, session, send_from_directory, g
from flask_caching import Cache
from auth import user_login
from category import insertCategory, getCategoryById, updateCategory, getAllCategory, deleteCategory
from products import insertProduct, getAllProductForAdmin, getProductById, updateProduct
import os

app = Flask(__name__)

# ================= CONFIG =================
app.secret_key = "codemines_secure_key"
UPLOAD_FOLDER = "upload"

app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 60
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

cache = Cache(app)

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ================= GLOBAL DATA =================
@app.before_request
def loadGlobalData():
    try:
        response = getAllCategory()
        g.categoryList = [{"id": i[0], "name": i[1]} for i in response] if response else []
    except:
        g.categoryList = []

    user = session.get("user")
    g.username = user["name"] if user else None


# ================= ROUTES =================
@app.route("/upload/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/addproduct")
def addproduct():
    return render_template("addproduct.html")


@app.route("/<category>")
def displayCategoryData(category):
    return render_template("category-details.html", categoryName=category)


# ================= LOGIN =================
@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/user-login", methods=["POST"])
def authUser():
    username = request.form.get("username")
    password = request.form.get("password")

    response = user_login(username, password)

    if isinstance(response, tuple):
        session["user"] = {
            "id": response[0],
            "name": response[1],
            "mobile": response[2],
            "email": response[3]
        }
        return redirect("/dashboard")

    return render_template("login.html", message=response)


@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect("/login")
    return render_template("dashboard.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/login")


# ================= CATEGORY =================
@app.route("/category")
def categoryList():
    response = getAllCategory()
    data = [{"id": i[0], "name": i[1]} for i in response] if response else []
    return render_template("category.html", data=data)


@app.route("/delete-category")
def removeCategory():
    id = request.args.get("id")
    if id:
        deleteCategory(id)
    return redirect("/category")


@app.route("/manage-category", methods=["GET", "POST"])
def manageCategory():
    if request.method == "POST":
        id = request.form.get("id", "0")
        name = request.form.get("name")

        if id.isdigit() and int(id) > 0:
            updateCategory(id, name)
        else:
            insertCategory(name)

        return redirect("/category")

    # GET
    id = request.args.get("id", "0")

    if id.isdigit() and int(id) > 0:
        categoryData = getCategoryById(id)
        if isinstance(categoryData, tuple):
            return render_template("manage-category.html",
                                   action_name="Edit",
                                   data_id=id,
                                   data_name=categoryData[1])

    return render_template("manage-category.html", action_name="Add New", data_id=0)


# ================= PRODUCTS =================
@app.route("/product")
def productList():
    response = getAllProductForAdmin()
    data = [{
        "id": i[0],
        "name": i[1],
        "image": i[2],
        "category": i[3],
        "price": i[4],
        "description": i[5]
    } for i in response] if response else []

    return render_template("product.html", data=data)


@app.route("/manage-product", methods=["GET", "POST"])
def manageProduct():
    if request.method == "POST":
        pid = request.form.get("pid", "0")
        pid = int(pid) if pid.isdigit() else 0

        name = request.form.get("productName")
        category = request.form.get("categoryName")
        price = request.form.get("amount")
        desc = request.form.get("productDesc")

        image_file = request.files.get("productImage")
        filename = request.form.get("filename", "")

        if image_file and image_file.filename:
            filename = image_file.filename
            image_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        if pid <= 0:
            insertProduct(name, category, filename, price, desc)
        else:
            updateProduct(pid, name, category, filename, price, desc)

        return redirect("/product")

    # ========== GET ==========
    id = request.args.get("id", "0")
    product = None

    if id.isdigit() and int(id) > 0:
        productData = getProductById(id)

        if isinstance(productData, tuple) and len(productData) >= 6:
            product = {
                "id": productData[0],
                "name": productData[1],
                "image": productData[2],
                "category_id": productData[3],
                "price": productData[4],
                "description": productData[5],
            }

    categories = [{"id": i[0], "name": i[1]} for i in getAllCategory()]
    return render_template("manage-product.html", categories=categories, product_data=product)


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
