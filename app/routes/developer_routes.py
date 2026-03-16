from flask import Blueprint, render_template, request, redirect
from app.middleware.auth_middleware import token_required
from app.routes.auth_routes import get_db_connection

developer_bp = Blueprint("developer_bp", __name__)


# -----------------------------------
# VIEW ASSIGNED ISSUES
# -----------------------------------
@developer_bp.route("/assigned_issues")
@token_required
def assigned_issues(user):

    print("Developer accessing assigned issues")
    print("Logged in user:", user)

    if user["role"] != "developer":
        print("Unauthorized access attempt")
        return "Unauthorized User", 403

    developer_id = user["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    print("Fetching tickets assigned to developer:", developer_id)

    cursor.execute("""
        SELECT id, title, description, priority, status
        FROM tickets
        WHERE assigned_to = %s
    """, (developer_id,))

    tickets = cursor.fetchall()

    print("Tickets fetched:", tickets)

    cursor.close()
    conn.close()

    return render_template(
        "assigned_issues.html",
        tickets=tickets,
        user_name=user["email"],
        role=user["role"]
    )


# -----------------------------------
# UPDATE ISSUE STATUS
# -----------------------------------
@developer_bp.route("/update_issue_status", methods=["POST"])
@token_required
def update_issue_status(user):

    print("\n---- UPDATE STATUS ROUTE CALLED ----")

    print("Request Method:", request.method)

    if user["role"] != "developer":
        print("Unauthorized developer attempt")
        return "Unauthorized User", 403

    ticket_id = request.form.get("ticket_id")
    new_status = request.form.get("status")

    print("Ticket ID received:", ticket_id)
    print("New Status received:", new_status)

    if not ticket_id or not new_status:
        print("ERROR: Form data missing")
        return "Invalid form data", 400

    conn = get_db_connection()
    cursor = conn.cursor()

    print("Updating ticket in database...")

    cursor.execute(
        "UPDATE tickets SET status=%s WHERE id=%s",
        (new_status, ticket_id)
    )

    conn.commit()

    print("Database updated successfully")

    cursor.close()
    conn.close()

    print("Redirecting back to assigned issues\n")

    return redirect("/assigned_issues")