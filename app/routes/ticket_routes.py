from flask import Blueprint, request, render_template, redirect, url_for
import mysql.connector
from config import Config 
from app.middleware.auth_middleware import token_required 

ticket_bp = Blueprint("ticket_bp", __name__)


def get_db_connection():
    return mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )


# -------------------------
# CREATE TICKET PAGE
# -------------------------
@ticket_bp.route("/create_ticket", methods=["GET"])
def create_ticket_page():
    return render_template("create_ticket.html")


# -------------------------
# CREATE TICKET
# -------------------------
@ticket_bp.route("/create_ticket", methods=["POST"])
@token_required 
def create_ticket(user): 

    data = request.get_json() 

    title = data.get("title")
    description = data.get("description")
    priority = data.get("priority")

    if not title or not description:
        return "Title and description required", 400

    created_by = user["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tickets (title, description, priority, created_by)
        VALUES (%s,%s,%s,%s)
        """,
        (title, description, priority, created_by)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Ticket created successfully"}


# -------------------------
# VIEW MY ISSUES
# -------------------------
@ticket_bp.route("/view_my_issues") 
@token_required 
def view_my_issues(user):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tickets WHERE created_by=%s", (user["user_id"],))
    tickets = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("ticket_list.html", tickets=tickets)

# -------------------------
# TICKET DETAILS
# -------------------------
# -------------------------
# TICKET DETAILS
# -------------------------
@ticket_bp.route("/ticket/<int:ticket_id>")
@token_required
def ticket_details(user, ticket_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch ticket
    cursor.execute("SELECT * FROM tickets WHERE id=%s", (ticket_id,))
    ticket = cursor.fetchone()

    # Fetch developers
    cursor.execute(
        "SELECT id, email FROM users WHERE role=%s",
        ("developer",)
    )
    developers = cursor.fetchall()

    cursor.close()
    conn.close()

    if not ticket:
        return "Ticket not found", 404

    return render_template(
        "ticket_details.html",
        ticket=ticket,
        developers=developers,
        role=user["role"]
    )
# -------------------------
# VIEW ALL ISSUES (ADMIN)
# -------------------------
@ticket_bp.route("/all_issues")
@token_required
def all_issues(user):

    print("\n---- ADMIN VIEW ALL ISSUES ----")

    if user["role"] != "admin":
        return "Unauthorized User", 403

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT tickets.id, tickets.title, tickets.priority,
               tickets.status, users.name AS created_by
        FROM tickets
        JOIN users ON tickets.created_by = users.id
    """)

    tickets = cursor.fetchall()

    print("Tickets fetched:", tickets)

    cursor.close()
    conn.close()

    return render_template(
        "all_issues.html",
        tickets=tickets,
        role=user["role"]
    )   

