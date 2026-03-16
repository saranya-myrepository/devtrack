import jwt 
from datetime import datetime, timedelta 
from config import Config 

def generate_token(user_id, email, role):
    try:
        
        payload = {
        "user_id" : user_id, 
        "email" : email, 
        "role" : role, 
        "exp" : datetime.utcnow() + timedelta(hours = 24)
    }  
        token = jwt.encode(payload, Config.SECRET_KEY, algorithm = "HS256") 
        return token  
    
    except Exception as e:
        raise e 
    
def verify_token(token):
    try: 
        decoded = jwt.decode(token, Config.SECRET_KEY, algorithms= ["HS256"]) 
        return decoded 
    except jwt.ExpiredSignatureError:
        return {"error": "Token Expired"} 
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}