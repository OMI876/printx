from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, make_response
from flask_bcrypt import Bcrypt
from datetime import datetime
import pdfkit
import os
from werkzeug.utils import secure_filename
import MySQLdb.cursors

profile_bp = Blueprint("profile", __name__)
mysql = None
bcrypt = None

# ✅ Init function (MySQL + Bcrypt inject)
def init_mysql(db, bc):
    global mysql, bcrypt
    mysql = db
    bcrypt = bc

# ✅ Upload folder
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------- ROUTES ----------------

# Profile page render
@profile_bp.route("/profilepage")
def profile_page():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("profilepage.html")


# --------- USER INFO ---------
@profile_bp.route("/api/user/me")
def get_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({}), 401

    cur = mysql.connection.cursor()
    cur.execute("SELECT name, email, phone, dob FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()

    if not row:
        return jsonify({})
    
    return jsonify({
        "full_name": row[0],
        "email": row[1],
        "phone": row[2] if row[2] else "",
        "dob": row[3].strftime("%Y-%m-%d") if row[3] else ""
    })


@profile_bp.route("/api/user/update", methods=["POST"])
def update_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"ok": False}), 401

    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE users SET name=%s, email=%s, phone=%s, dob=%s WHERE id=%s
    """, (data["full_name"], data["email"], data["phone"], data["dob"], user_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"ok": True})


# --------- ADDRESSES ---------
@profile_bp.route("/api/addresses")
def get_addresses():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify([])

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, type, CONCAT(line1, ', ', line2, ', ', city, ', ', state), pin
        FROM addresses WHERE user_id = %s
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()

    return jsonify([
        {"id": r[0], "type": r[1], "address": r[2], "pin": r[3]} for r in rows
    ])


@profile_bp.route("/api/addresses/save", methods=["POST"])
def save_address():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"ok": False}), 401

    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO addresses (user_id, type, line1, line2, city, state, pin)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (user_id, data["type"], data["line1"], data["line2"], data["city"], data["state"], data["pin"]))
    mysql.connection.commit()
    cur.close()

    return jsonify({"ok": True})


@profile_bp.route("/api/addresses/delete", methods=["POST"])
def delete_address():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"ok": False}), 401

    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM addresses WHERE id = %s AND user_id = %s", (data["id"], user_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"ok": True})


# --------- ORDERS ---------
@profile_bp.route("/api/orders/history")
def get_order_history():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify([])

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.order_id, p.created_at, p.amount, p.order_status, p.payment_status, p.payment_method
        FROM payments p
        WHERE p.user_id = %s
        ORDER BY p.created_at DESC
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()

    return jsonify([
        {
            "id": row[0],
            "date": row[1].strftime("%Y-%m-%d %H:%M") if row[1] else "",
            "total": f"₹{row[2]}",
            "status": row[3] if row[3] else "Pending",
            "payment": f"{row[4]} ({row[5]})"
        }
        for row in rows
    ])


# --------- CANCEL ORDER ---------
@profile_bp.route("/api/orders/cancel", methods=["POST"])
def cancel_order():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"ok": False, "msg": "Unauthorized"}), 401

    data = request.get_json()
    order_id = str(data.get("order_id")).strip()  # ✅ ensure string & clean

    if not order_id:
        return jsonify({"ok": False, "msg": "Missing order_id"}), 400

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # ✅ Debug log
    print(f"🔎 Cancel request => order_id={order_id}, user_id={user_id}")

    # ✅ Check if order exists for this user
    cur.execute("SELECT order_id FROM payments WHERE order_id=%s AND user_id=%s", (order_id, user_id))
    order = cur.fetchone()
    if not order:
        cur.close()
        return jsonify({"ok": False, "msg": f"Order {order_id} not found for user {user_id}"}), 404

    # ✅ Get user details
    cur.execute("SELECT name, email, phone FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()

    # ✅ Insert into admin_cancel table
    cur.execute("""
        INSERT INTO admin_cancel (order_id, customer_name, phone, email)
        VALUES (%s, %s, %s, %s)
    """, (order_id, user["name"], user["phone"], user["email"]))
    mysql.connection.commit()

    # ✅ Update payments table
    cur.execute("UPDATE payments SET order_status='Cancelled' WHERE order_id=%s AND user_id=%s", (order_id, user_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"ok": True, "msg": f"Order {order_id} cancelled successfully"})


# --------- ADMIN CANCELLED VIEW ---------
@profile_bp.route("/admin/cancelled")
def admin_cancelled():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM admin_cancel ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    # ✅ load correct template from admin/ folder
    return render_template("admin/admin_cancel.html", rows=rows)


# --------- INVOICE VIEW ---------
@profile_bp.route("/api/orders/<order_id>/invoice")
def order_invoice(order_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.order_id, p.amount, p.payment_status, p.payment_method, p.order_status, 
               p.created_at, u.name, u.email
        FROM payments p
        JOIN users u ON p.user_id = u.id
        WHERE p.order_id = %s AND p.user_id = %s
    """, (order_id, user_id))
    order = cur.fetchone()

    if not order:
        cur.close()
        return "Order not found", 404

    cur.execute("""
        SELECT title, quantity, price, size, border_color, border_width
        FROM order_items
        WHERE order_id = %s AND user_id = %s
    """, (order_id, user_id))
    items = cur.fetchall()
    cur.close()

    return render_template("invoice.html", order=order, items=items)


# --------- DOWNLOAD INVOICE AS PDF ---------
@profile_bp.route("/api/orders/<order_id>/invoice/pdf")
def order_invoice_pdf(order_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.order_id, p.amount, p.payment_status, p.payment_method, 
               p.order_status, p.created_at, u.name, u.email
        FROM payments p
        JOIN users u ON p.user_id = u.id
        WHERE p.order_id = %s AND p.user_id = %s
    """, (order_id, user_id))
    order = cur.fetchone()

    if not order:
        cur.close()
        return "Order not found", 404

    cur.execute("""
        SELECT title, quantity, price, size, border_color, border_width
        FROM order_items
        WHERE order_id = %s AND user_id = %s
    """, (order_id, user_id))
    items = cur.fetchall()
    cur.close()

    html = render_template("invoice.html", order=order, items=items, pdf_mode=True)

    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdf = pdfkit.from_string(html, False, configuration=config)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=invoice_{order_id}.pdf"
    return response


# --------- ORDER ITEMS ---------
@profile_bp.route("/api/orders/<order_id>/items")
def get_order_items(order_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify([]), 401

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT title, quantity, price, size, border_color, border_width, image_path
        FROM order_items
        WHERE order_id = %s AND user_id = %s
    """, (order_id, user_id))
    rows = cur.fetchall()
    cur.close()

    return jsonify([
        {
            "name": r[0],
            "qty": r[1],
            "price": float(r[2]),
            "size": r[3],
            "border": f"{r[4]} / {r[5]}px" if r[4] else "",
            "image": r[6]
        }
        for r in rows
    ])


# --------- TRACK ORDER ---------
@profile_bp.route("/api/orders/track")
def track_order():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({}), 401

    order_id = request.args.get("id")

    cur = mysql.connection.cursor()
    cur.execute("SELECT order_id, order_status FROM payments WHERE order_id=%s AND user_id=%s", (order_id, user_id))
    row = cur.fetchone()

    if not row:
        cur.close()
        return jsonify({})

    cur.execute("SELECT time, text FROM order_updates WHERE order_id = %s ORDER BY time ASC", (row[0],))
    updates = cur.fetchall()
    cur.close()

    return jsonify({
        "id": row[0],
        "status": row[1],
        "updates": [{"time": u[0].strftime("%Y-%m-%d %H:%M"), "text": u[1]} for u in updates]
    })


# --------- PASSWORD CHANGE ---------
@profile_bp.route("/api/user/change-password", methods=["POST"])
def change_password():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"ok": False}), 401

    data = request.get_json()
    new_password = data["password"]
    hashed = bcrypt.generate_password_hash(new_password).decode("utf-8")

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET password=%s WHERE id=%s", (hashed, user_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"ok": True})


# --------- RETURN / EXCHANGE PAGE ---------
@profile_bp.route("/return")
def return_page():
    if "user_id" not in session:
        return redirect(url_for("login"))
    order_id = request.args.get("order")
    return render_template("return.html", order_id=order_id)


# --------- RETURN / EXCHANGE SUBMIT ---------
@profile_bp.route("/submit-return-exchange", methods=["POST"])
def submit_return_exchange():
    if "user_id" not in session:
        return jsonify({"ok": False, "msg": "Unauthorized"}), 401

    user_id = session["user_id"]
    order_id = request.form.get("orderId")
    email = request.form.get("email")
    reason = request.form.get("reason")
    req_type = request.form.get("type")
    upi = request.form.get("upi")
    details = request.form.get("details")

    image_file = request.files.get("image")
    image_filename = None
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        image_filename = f"{order_id}_{filename}"
        image_file.save(os.path.join(UPLOAD_FOLDER, image_filename))

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO return_requests (order_id, user_id, email, request_type, reason, upi, details, image, status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (order_id, user_id, email, req_type, reason, upi, details, image_filename, "Pending"))
    mysql.connection.commit()
    cur.close()

    return jsonify({
        "ok": True,
        "msg": "✅ Thank you! We have received your return/exchange request. "
               "You will receive updates via email within 2–3 working days."
    })


# --------- LOGOUT ---------
@profile_bp.route("/api/auth/logout", methods=["POST"])
def api_logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return jsonify({"ok": True})
