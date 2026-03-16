from flask import Blueprint, render_template
from app.routes.auth_routes import get_db_connection
from app.middleware.auth_middleware import token_required

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.route("/dashboard")
@token_required
def dashboard(user):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    role = user["role"]
    user_id = int(user["user_id"])  

    # ---------------- CLIENT DASHBOARD ---------------- 

    if role == "client":

        cursor.execute(
            "SELECT COUNT(*) AS total FROM tickets WHERE created_by=%s",
            (user_id,)
        )
        total_tickets = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT COUNT(*) AS open_count FROM tickets WHERE status='open' AND created_by=%s",
            (user_id,)
        )
        open_tickets = cursor.fetchone()["open_count"]

        cursor.execute(
            "SELECT COUNT(*) AS progress_count FROM tickets WHERE status='in_progress' AND created_by=%s",
            (user_id,)
        )
        in_progress = cursor.fetchone()["progress_count"]

        cursor.execute(
            "SELECT COUNT(*) AS resolved_count FROM tickets WHERE status='resolved' AND created_by=%s",
            (user_id,)
        )
        resolved = cursor.fetchone()["resolved_count"]

        cursor.close()
        conn.close()

        return render_template(
            "dashboard.html",
            user_name=user["email"],
            role=role,
            total_tickets=total_tickets,
            open_tickets=open_tickets,
            in_progress_tickets=in_progress,
            resolved_tickets=resolved
        )
    # ---------------- DEVELOPER DASHBOARD ----------------

    if role == "developer":

        cursor.execute(
            "SELECT COUNT(*) AS assigned FROM tickets WHERE assigned_to=%s",
            (user_id,)
        )
        assigned_tickets = cursor.fetchone()["assigned"]

        cursor.execute(
            "SELECT COUNT(*) AS progress FROM tickets WHERE status='in_progress' AND assigned_to=%s",
            (user_id,)
        )
        progress_tickets = cursor.fetchone()["progress"]

        cursor.execute(
            "SELECT COUNT(*) AS resolved FROM tickets WHERE status='resolved' AND assigned_to=%s",
            (user_id,)
        )
        resolved_tickets = cursor.fetchone()["resolved"]

        cursor.close()
        conn.close()

        return render_template(
            "dashboard.html",
            user_name=user["email"],
            role=role,
            assigned_tickets=assigned_tickets,
            progress_tickets=progress_tickets,
            resolved_tickets=resolved_tickets
        )

    # ---------------- ADMIN DASHBOARD ----------------

    if role == "admin":

        # total tickets
        cursor.execute("SELECT COUNT(*) AS total FROM tickets")
        total_tickets = cursor.fetchone()["total"]

        # solved tickets
        cursor.execute("SELECT COUNT(*) AS solved FROM tickets WHERE status='resolved'")
        solved_tickets = cursor.fetchone()["solved"]

        # assigned tickets
        cursor.execute("SELECT COUNT(*) AS assigned FROM tickets WHERE assigned_to IS NOT NULL")
        assigned_tickets = cursor.fetchone()["assigned"]

        # ticket status counts
        cursor.execute("SELECT COUNT(*) AS open_count FROM tickets WHERE status='open'")
        open_count = cursor.fetchone()["open_count"]

        cursor.execute("SELECT COUNT(*) AS progress_count FROM tickets WHERE status='in_progress'")
        progress_count = cursor.fetchone()["progress_count"]

        cursor.execute("SELECT COUNT(*) AS solved_count FROM tickets WHERE status='resolved'")
        solved_count = cursor.fetchone()["solved_count"]

        # developer workload
        cursor.execute("""
            SELECT u.id, u.email,
            COUNT(t.id) AS assigned_tasks
            FROM users u
            LEFT JOIN tickets t ON u.id = t.assigned_to
            WHERE u.role='developer'
            GROUP BY u.id
        """)
        developers = cursor.fetchall()

        # total developers
        cursor.execute("SELECT COUNT(*) AS total_dev FROM users WHERE role='developer'")
        total_developers = cursor.fetchone()["total_dev"]

        # unassigned tickets
        cursor.execute("SELECT COUNT(*) AS unassigned FROM tickets WHERE assigned_to IS NULL")
        unassigned_tickets = cursor.fetchone()["unassigned"]

        cursor.close()
        conn.close()

        return render_template(
            "dashboard.html",
            user_name=user["email"],
            role=role,
            total_tickets=total_tickets,
            solved_tickets=solved_tickets,
            assigned_tickets=assigned_tickets,
            open_count=open_count,
            progress_count=progress_count,
            solved_count=solved_count,
            developers=developers,
            total_developers=total_developers,
            unassigned_tickets=unassigned_tickets
        )