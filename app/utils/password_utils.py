import bcrypt


# Hash password during registration
def hash_password(password):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed


# Verify password during login
def verify_password(password, hashed_password):
    password_bytes = password.encode("utf-8")

    # If DB stored hash is string convert to bytes
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_password) 