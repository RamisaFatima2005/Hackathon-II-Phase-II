# auth_utils.py
import bcrypt

# Salt rounds for hashing. Higher value means more secure but slower.
# 12 is a reasonable default for many applications.
SALT_ROUNDS = 12

def get_password_hash(password: str) -> str:
    """
    Hashes a password using bcrypt.
    """
    # Generate a salt and hash the password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=SALT_ROUNDS)
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a bcrypt hashed password.
    """
    # Encode the plain password and hash it using the salt from the hashed password
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)