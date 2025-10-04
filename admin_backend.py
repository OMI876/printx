from flask import Blueprint, render_template, session, redirect, request, flash, jsonify
import MySQLdb.cursors

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")
mysql = None   # init from app.py


def init_mysql(db):
    global mysql
    mysql = db


# ✅ Admin Dashboard
@admin_bp.route("/")
def dashboard():
    if session.get("role") != "admin":
        return redirect("/login")

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Total Orders
    cur.execute("SELECT COUNT(*) as cnt FROM payments")
    total_orders = cur.fetchone()["cnt"]

    # Customers count
    cur.execute("SELECT COUNT(*) as cnt FROM users WHERE role = 'customer'")
    total_customers = cur.fetchone()["cnt"]

    # Total revenue
    cur.execute("""
        SELECT COALESCE(SUM(amount),0) as total 
        FROM payments 
        WHERE (payment_method='ONLINE' AND payment_status='SUCCESS')
        OR (payment_method='COD' AND order_status='Delivered')
    """)
    total_revenue = cur.fetchone()["total"]

    # Latest 5 Orders (✅ with user_id + status)
    cur.execute("""
        SELECT p.order_id, p.user_id, p.amount, 
               p.payment_status, p.payment_method, 
               p.order_status, p.created_at
        FROM payments p
        ORDER BY p.created_at DESC LIMIT 5
    """)
    latest_orders = cur.fetchall()
    cur.close()

    return render_template("admin/admin_dashboard.html",
                           total_orders=total_orders,
                           total_customers=total_customers,
                           total_revenue=total_revenue,
                           latest_orders=latest_orders)


# ✅ Manage Users
@admin_bp.route("/users")
def manage_users():
    if session.get("role") != "admin":
        return redirect("/login")

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT id, name, email, role FROM users ORDER BY id DESC")
    users = cur.fetchall()
    cur.close()

    return render_template("admin/admin_users.html", users=users)


# ✅ Manage Orders
@admin_bp.route("/orders")
def manage_orders():
    if session.get("role") != "admin":
        return redirect("/login")

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT p.order_id, u.name as customer, p.amount, 
               p.payment_status, p.payment_method, 
               p.order_status, p.created_at
        FROM payments p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
    """)
    orders = cur.fetchall()
    cur.close()

    return render_template("admin/admin_orders.html", orders=orders)


# ✅ Get Order Details (AJAX for modal)
@admin_bp.route("/order/<order_id>")
def order_details(order_id):
    if session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 401

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("""
        SELECT p.order_id, p.amount, p.payment_method, p.payment_status, 
               p.order_status, p.created_at,
               u.name as customer_name, u.email, u.phone as user_phone,
               a.phone as address_phone,
               COALESCE(CONCAT_WS(', ', a.line1, a.line2, a.city, a.state, a.pin), 'N/A') as address
        FROM payments p
        JOIN users u ON p.user_id = u.id
        LEFT JOIN addresses a ON p.order_id = a.order_id
        WHERE p.order_id = %s
    """, (order_id,))
    order = cur.fetchone()

    if not order:
        return jsonify({"error": "Order not found"}), 404

    cur.execute("""
        SELECT title AS product_name, quantity, price, size, border_color, border_width, image_path
        FROM order_items
        WHERE order_id = %s
    """, (order_id,))
    items = cur.fetchall()
    cur.close()

    return jsonify({
        "order_id": order["order_id"],
        "customer_name": order["customer_name"],
        "email": order["email"],
        "phone": order["address_phone"] or order["user_phone"],
        "address": order["address"],
        "order_date": str(order["created_at"]),
        "payment_method": order["payment_method"],
        "payment_status": order["payment_status"],
        "order_status": order["order_status"],
        "total": order["amount"],
        "items": items
    })


# ✅ Update Order Status
@admin_bp.route("/update_order_status", methods=["POST"])
def update_order_status():
    if session.get("role") != "admin":
        return redirect("/login")

    order_id = request.form["order_id"]
    new_status = request.form["status"]

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT payment_method, payment_status FROM payments WHERE order_id=%s", (order_id,))
    order = cur.fetchone()

    if order:
        # Update payments table
        cur.execute("UPDATE payments SET order_status=%s WHERE order_id=%s", (new_status, order_id))

        # ✅ If COD + Delivered, mark as paid
        if order["payment_method"] == "COD" and new_status == "Delivered":
            cur.execute("UPDATE payments SET payment_status=%s WHERE order_id=%s", ("SUCCESS", order_id))

        # ✅ Sync with return_requests table
        if new_status in ["Returned", "Exchanged"]:
            cur.execute("""
                UPDATE return_requests 
                SET status=%s 
                WHERE order_id=%s
            """, ("Approved", order_id))  # 👈 Approved mark karte hi dikh jayega

    mysql.connection.commit()
    cur.close()

    flash("✅ Order status updated successfully!", "success")
    return redirect("/admin/orders")


# ✅ Manage Returns/Exchange
@admin_bp.route("/returns")
def manage_returns():
    if session.get("role") != "admin":
        return redirect("/login")

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT r.id, r.order_id, u.name as customer, u.email, r.request_type, r.reason, 
               r.upi, r.details, r.image, r.status, r.created_at
        FROM return_requests r
        JOIN users u ON r.user_id = u.id
        ORDER BY r.created_at DESC
    """)
    return_requests = cur.fetchall()
    cur.close()

    return render_template("admin/admin_return.html", return_requests=return_requests)


# ✅ Manage Messages
@admin_bp.route("/messages")
def manage_messages():
    if session.get("role") != "admin":
        return redirect("/login")

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM messages ORDER BY created_at DESC")
    messages = cur.fetchall()
    cur.close()

    return render_template("admin/admin_messages.html", messages=messages)


# ✅ Delete User
@admin_bp.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if session.get("role") != "admin":
        return redirect("/login")

    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM addresses WHERE user_id=%s", (user_id,))
        cur.execute("DELETE FROM order_items WHERE user_id=%s", (user_id,))
        cur.execute("DELETE FROM payments WHERE user_id=%s", (user_id,))
        cur.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))
        cur.execute("DELETE FROM users WHERE id=%s AND role!='admin'", (user_id,))
        mysql.connection.commit()
        cur.close()
        flash("✅ User deleted successfully!", "success")
    except Exception as e:
        flash(f"❌ Error deleting user: {str(e)}", "danger")

    return redirect("/admin/users")
