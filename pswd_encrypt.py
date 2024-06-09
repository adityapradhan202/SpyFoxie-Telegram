# Password hasing
import bcrypt

def password_hasher(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(entered_password, hashed_password):
    bool_val = bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password)
    return bool_val

