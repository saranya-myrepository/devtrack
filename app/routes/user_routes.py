from flask import Blueprint, render_template, request, redirect
import mysql.connector
from config import Config
from app.middleware.auth_middleware import token_required

user_bp = Blueprint("user_bp", __name__)

# -------------------------
# DATABASE CONNECTION
# -------------------------
def get_db_connection():
    return mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )


# -------------------------
# MANAGE USERS PAGE
# -------------------------
@user_bp.route("/manage_users")
@token_required
def manage_users(user):

    print("\n---- MANAGE USERS PAGE ----")
    print("Logged in user:", user)

    if user["role"] != "admin":
        print("Unauthorized access attempt")
        return "Unauthorized User", 403

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, name, email, role FROM users")
    users = cursor.fetchall()

    print("Users fetched:", users)

    cursor.close()
    conn.close()

    return render_template(
        "manage_users.html",
        users=users,
        role=user["role"]
    )


# -------------------------
# ASSIGN TICKET TO DEVELOPER
# -------------------------
@user_bp.route("/assign_ticket", methods=["POST"])
@token_required
def assign_ticket(user):

    print("\n---- ASSIGN TICKET ROUTE CALLED ----")

    if user["role"] != "admin":
        print("Unauthorized user tried to assign ticket")
        return "Unauthorized User", 403

    ticket_id = request.form.get("ticket_id")
    developer_id = request.form.get("developer_id")

    print("Ticket ID received:", ticket_id)
    print("Developer ID received:", developer_id)

    if not ticket_id or not developer_id:
        print("ERROR: Missing form data")
        return "Invalid form data", 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tickets SET assigned_to=%s WHERE id=%s",
        (developer_id, ticket_id)
    )

    conn.commit()

    print("Ticket assigned successfully")

    cursor.close()
    conn.close()

    return redirect("/dashboard")