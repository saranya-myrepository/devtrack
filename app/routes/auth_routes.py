from flask import Blueprint, request, render_template, redirect, url_for, make_response
from app.utils.password_utils import hash_password, verify_password
from app.utils.jwt_utils import generate_token
import mysql.connector
from config import Config

auth_bp = Blueprint("auth_bp", __name__)


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
# HOME PAGE
# -------------------------
@auth_bp.route("/", methods=["GET"])
def home():
    return render_template("register.html")


# -------------------------
# REGISTER
# -------------------------
@auth_bp.route("/register", methods=["POST"])
def register(): 

    data = request.get_json(silent=True)

    if data:
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        return "Passwords do not match", 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
    if cursor.fetchone():
        return "Email already registered", 409

    hashed_password = hash_password(password)

    cursor.execute(
        """
        INSERT INTO users (name,email,password,role)
        VALUES (%s,%s,%s,%s)
        """,
        (name, email, hashed_password, "client")
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("auth_bp.login_page"))


# -------------------------
# LOGIN PAGE
# -------------------------
@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


# -------------------------
# LOGIN
# -------------------------
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True)

    if data:
        email = data.get("email")
        password = data.get("password")
    else:
        email = request.form.get("email")
        password = request.form.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return "Invalid email or password", 401

    if not verify_password(password, user["password"]):
        return "Invalid email or password", 401

    token = generate_token(user["id"], user["email"], user["role"])

    # API login case
    if data:
        return {
            "message": "Login successful",
            "token": token
        }

    # WEB login case
    response = make_response(redirect("/dashboard"))
    response.set_cookie("token", token)

    return response


# -------------------------
# LOGOUT
# -------------------------
@auth_bp.route("/logout")
def logout():

    response = redirect(url_for("auth_bp.login_page"))
    response.delete_cookie("token")

    return response 