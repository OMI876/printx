from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
import razorpay
import datetime
import os
from werkzeug.utils import secure_filename

cart_backend = Blueprint('cart_backend', __name__)
mysql = None   # set from app.py

def init_mysql(db):
    global mysql
    mysql = db

# ----------------- RAZORPAY CLIENT -----------------
razorpay_client = razorpay.Client(auth=("rzp_test_RL9E4kDmQnuJ7w", "gVzBbOe6CO2nhSZFyvzXUPiN"))

# ----------------- UPLOADS -----------------
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@cart_backend.route('/add_banner_order', methods=['POST'])
def add_banner_order():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    product_type = request.form.get("productType", "banner")
    height = request.form.get("height")
    width = request.form.get("width")
    border = request.form.get("border")
    wooden_frame = request.form.get("frame", "no")
    price = request.form.get("finalPrice") or 0   # ✅ price from frontend

    # ✅ product title with type & details
    product_title = f"{product_type.capitalize()} - Height({height} ft), Width({width} ft), Border({border} inch), Wooden Frame: {wooden_frame.capitalize()}"

    # ✅ handle image
    image_path = None
    if "bannerImage" in request.files:
        file = request.files["bannerImage"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
            image_path = f"uploads/{filename}"

    # ✅ insert into cart
    cur = mysql.connection.cursor()
    cur.execute(
        """INSERT INTO cart (user_id, product_id, title, price, size, quantity, border_color, border_width, image_path) 
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (session['user_id'], None, product_title, price, None, 1, None, border, image_path)
    )
    mysql.connection.commit()
    cur.close()

    flash("✅ Item added to cart!", "success")
    return redirect(url_for("cart_backend.cart"))


# ----------------- ADD NORMAL PRODUCT TO CART (AJAX) -----------------
@cart_backend.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "⚠️ Please login first!"}), 401

    product_id = request.form.get('product_id')
    title = request.form.get('title', "Product")
    price = request.form.get('price', 0)
    size = request.form.get('size')
    quantity = request.form.get('quantity', 1)
    border_color = request.form.get('border_color')
    border_width = request.form.get('border_width')
    image_path = request.form.get('image_path')

    if "image" in request.files:
        file = request.files["image"]
        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
            image_path = f"uploads/{filename}"

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """INSERT INTO cart 
               (user_id, product_id, title, price, size, quantity, border_color, border_width, image_path) 
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (session['user_id'], product_id, title, price, size, quantity,
             border_color, border_width, image_path)
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({"success": True, "message": "✅ Item added to cart!"})
    except Exception as e:
        return jsonify({"success": False, "message": f"❌ Error: {str(e)}"}), 500

# ----------------- VIEW CART -----------------
@cart_backend.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("""SELECT id, product_id, title, price, size, quantity,
                          border_color, border_width, image_path 
                   FROM cart WHERE user_id = %s""", (session['user_id'],))
    items = cur.fetchall()
    cur.close()

    total = 0
    for item in items:
        try:
            price = float(item[3] or 0)
            qty = int(item[5] or 0)
            total += price * qty
        except:
            pass

    return render_template("cart.html", items=items, total=total)

# ----------------- REMOVE FROM CART (AJAX) -----------------
@cart_backend.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "⚠️ Please login first!"}), 401
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM cart WHERE id = %s AND user_id = %s",
                    (item_id, session['user_id']))
        mysql.connection.commit()
        cur.close()
        return jsonify({"success": True, "message": "🗑️ Item removed from cart"})
    except Exception as e:
        return jsonify({"success": False, "message": f"❌ Error: {str(e)}"}), 500

# ----------------- CREATE PAYMENT ORDER -----------------
@cart_backend.route('/create_order', methods=['POST'])
def create_order():
    if 'user_id' not in session:
        return jsonify({"message": "Please login first!"}), 401

    try:
        amount_rupees = float(request.form.get('amount', 0))
    except:
        return jsonify({"message": "Invalid amount"}), 400

    amount = int(amount_rupees * 100)
    currency = "INR"
    receipt = f"order_rcptid_{session['user_id']}"

    try:
        order = razorpay_client.order.create({
            "amount": amount,
            "currency": currency,
            "receipt": receipt,
            "payment_capture": "1"
        })
        return jsonify(order)
    except Exception as e:
        return jsonify({"message": f"Error creating order: {str(e)}"}), 500

# ----------------- PAYMENT SUCCESS -----------------
@cart_backend.route('/payment/success', methods=['POST'])
def payment_success():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    data = request.form
    try:
        params_dict = {
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature']
        }
        razorpay_client.utility.verify_payment_signature(params_dict)

        now = datetime.datetime.now()
        custom_order_id = f"ORD{now.strftime('%Y%m%d%H%M%S')}{session['user_id']}"
        amount = float(request.form.get('amount', 0))

        cur = mysql.connection.cursor()
        # save payment
        cur.execute("""
            INSERT INTO payments (user_id, order_id, razorpay_order_id, payment_id,
                                  amount, payment_status, payment_method, order_status, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW())
        """, (session['user_id'], custom_order_id, data['razorpay_order_id'],
              data['razorpay_payment_id'], amount, 'SUCCESS', 'ONLINE', 'Pending'))

        # save address
        cur.execute("""
            INSERT INTO addresses (user_id, order_id, line1, line2, city, state, pin, phone)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (session['user_id'], custom_order_id,
              data.get("line1"), data.get("line2"), data.get("city"),
              data.get("state"), data.get("zip"), data.get("phone")))

        # copy cart → order_items
        cur.execute("""
            INSERT INTO order_items (order_id, user_id, product_id, title, price,
                                     quantity, size, border_color, border_width, image_path)
            SELECT %s, user_id, product_id, title, price, quantity,
                   size, border_color, border_width, image_path
            FROM cart WHERE user_id = %s
        """, (custom_order_id, session['user_id']))

        # clear cart
        cur.execute("DELETE FROM cart WHERE user_id=%s", (session['user_id'],))
        mysql.connection.commit()
        cur.close()

        return render_template("success.html",
                               order_id=custom_order_id,
                               payment_id=data['razorpay_payment_id'])
    except Exception as e:
        return render_template("failure.html", error=str(e))

# ----------------- CASH ON DELIVERY -----------------
@cart_backend.route('/place_cod_order', methods=['POST'])
def place_cod_order():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    now = datetime.datetime.now()
    custom_order_id = f"COD{now.strftime('%Y%m%d%H%M%S')}{session['user_id']}"
    try:
        amount = float(request.form.get('amount', 0))
    except:
        amount = 0

    cur = mysql.connection.cursor()
    # save payment
    cur.execute("""
        INSERT INTO payments (user_id, order_id, amount, payment_status,
                              payment_method, order_status, created_at)
        VALUES (%s,%s,%s,%s,%s,%s,NOW())
    """, (session['user_id'], custom_order_id, amount,
          'COD PENDING', 'COD', 'Pending'))

    # save address
    cur.execute("""
        INSERT INTO addresses (user_id, order_id, line1, line2, city, state, pin, phone)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (session['user_id'], custom_order_id,
          request.form.get("line1"), request.form.get("line2"),
          request.form.get("city"), request.form.get("state"),
          request.form.get("zip"), request.form.get("phone")))

    # copy cart → order_items
    cur.execute("""
        INSERT INTO order_items (order_id, user_id, product_id, title, price,
                                 quantity, size, border_color, border_width, image_path)
        SELECT %s, user_id, product_id, title, price, quantity,
               size, border_color, border_width, image_path
        FROM cart WHERE user_id=%s
    """, (custom_order_id, session['user_id']))

    # clear cart
    cur.execute("DELETE FROM cart WHERE user_id=%s", (session['user_id'],))
    mysql.connection.commit()
    cur.close()

    return render_template("success.html",
                           order_id=custom_order_id,
                           payment_id="Cash on Delivery")

# ----------------- TRACK ORDER -----------------
@cart_backend.route('/track_order', methods=['GET', 'POST'])
def track_order():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    order = None
    error = None
    delivery_date = None

    if request.method == 'POST':
        order_id = request.form.get('order_id')
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT p.order_id, p.order_status, p.amount, p.created_at,
                   a.line1, a.line2, a.city, a.state, a.pin
            FROM payments p
            LEFT JOIN addresses a ON p.order_id = a.order_id
            WHERE p.order_id = %s AND p.user_id = %s
        """, (order_id, session['user_id']))
        order = cur.fetchone()
        cur.close()

        if not order:
            error = "⚠️ Order not found!"
        else:
            delivery_date = order[3] + datetime.timedelta(days=2)

    return render_template("track_order.html",
                           order=order,
                           error=error,
                           delivery_date=delivery_date)
