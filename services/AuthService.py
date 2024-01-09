from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def encrypt_password(password):
    return pwd_context.hash(password)