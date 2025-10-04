from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import MySQLdb.cursors

# Import blueprints
from cart_backend import cart_backend, init_mysql as init_cart_mysql
from profile_backend import profile_bp, init_mysql as init_profile_mysql
from admin_backend import admin_bp, init_mysql as init_admin_mysql
from forgot_backend import forgot_bp

# ------------------ FLASK APP ------------------
app = Flask(__name__)
app.secret_key = "your_secret_key"

# ✅ MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'chandu'
app.config['MYSQL_DB'] = 'printx'

# ✅ Init MySQL + Bcrypt
mysql = MySQL(app)
bcrypt = Bcrypt(app)

# ✅ Pass MySQL + Bcrypt instance to blueprints
init_cart_mysql(mysql)
init_profile_mysql(mysql, bcrypt)   # 👈 profile backend needs both mysql + bcrypt
init_admin_mysql(mysql)

# ✅ Register Blueprints
app.register_blueprint(cart_backend)
app.register_blueprint(profile_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(forgot_bp)

# ------------------ ROUTES ------------------

@app.route("/test")
def test():
    return "ok"

@app.route('/')
def home():
    username = session.get('username')
    return render_template('navigation.html', username=username)

@app.route('/about')
def about():
    return render_template('aboutuspage.html')

# ---------- CONTACT ----------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO messages (name, email, phone, message) VALUES (%s, %s, %s, %s)",
            (name, email, phone, message)
        )
        mysql.connection.commit()
        cur.close()

        flash("✅ Your message has been submitted successfully!", "success")
        return redirect("/contact")

    return render_template("contact.html")

# ---------- COLLECTION PAGES ----------
@app.route("/banner")
def banner():
    return render_template("banner.html")

@app.route('/photoframe')
def photoframe():
    return render_template('photoframe.html')

@app.route('/sticker')
def sticker():
    return render_template('sticker.html')

@app.route('/tshirt')
def tshirt():
    return render_template('tshirt.html')

# ---------- PRODUCT DETAIL ROUTE (static productX.html) ----------
@app.route('/product<int:product_id>')
def product_page(product_id):
    try:
        return render_template(f'product{product_id}.html')
    except:
        return "Product page not found", 404

# ---------- SEARCH API ----------
@app.route('/search')
def search():
    query = request.args.get('q', '')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT name, page_link FROM products WHERE name LIKE %s LIMIT 5", ('%' + query + '%',))
    results = cursor.fetchall()
    cursor.close()
    return jsonify(results)

# ---------- AUTH ----------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form.get('confirmPassword')

        # ✅ Backend validations
        if len(password) < 8:
            flash("❌ Password must be at least 8 characters!", "danger")
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash("❌ Passwords do not match!", "danger")
            return redirect(url_for('signup'))

        # ✅ Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur = mysql.connection.cursor()
        # ✅ Default role = customer
        cur.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)", 
            (name, email, hashed_password, "customer")
        )
        mysql.connection.commit()
        cur.close()

        flash("✅ Account created successfully! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.check_password_hash(user["password"], password):
            session['user_id'] = user['id']
            session['username'] = user['name']
            session['role'] = user['role']   # admin/customer

            if user['role'] == "admin":
                return redirect("/admin")
            else:
                return redirect(url_for("home"))
        else:
            flash("❌ Invalid email or password!", "danger")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('home'))

# ------------------ MAIN ------------------
if __name__ == '__main__':
    app.run(debug=True)
