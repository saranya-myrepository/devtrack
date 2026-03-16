import os 
from dotenv import load_dotenv 

load_dotenv() 

class Config: 
    SECRET_KEY = os.getenv("SECRET_KEY", "devtrack_secret_key")  

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root") 
    DB_PASSWORD = os.getenv("DB_PASSWORD", "") 
    DB_NAME = os.getenv("DB_NAME", "devtrack_db")  

    JWT_ALGORITHM = "HS256" 
    JWT_EXPIRATION_HOURS = 2 