from passlib.context import CryptContext

# Configure a stable password hashing scheme for this backend
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

# Hash a plain password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verify a plain password against the hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)