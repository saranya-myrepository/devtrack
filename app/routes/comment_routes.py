from flask import Blueprint, request, redirect, url_for 
import mysql.connector 
from config import Config 

comment_bp = Blueprint("comment_bp", __name__) 

#database connection 
def get_db_connection():
    return mysql.connector.connect(
        host = Config.DB_HOST, 
        user = Config.DB_USER, 
        password = Config.DB_PASSWORD, 
        database = Config.DB_NAME
    ) 
#adding comment to ticket 
@comment_bp.route("/add_comment", methods = ["POST"]) 
def add_comment(user): 

    ticket_id = request.form.get("ticket_id") 
    comment_text = request.form.get("comment") 

    if not ticket_id or not comment_text:
        return "Ticket ID and Comment required", 400 
    
    user_id = user["user_id"] 

    conn = get_db_connection() 
    cursor = conn.cursor() 

    cursor.execute(
        """INSERT INTO comments(ticket_id, user_id, comment)
        VALUES (%s, %s, %s)
        """, 
        (ticket_id, user_id, comment_text)
    ) 

    conn.commit()  
    cursor.close() 
    conn.close() 