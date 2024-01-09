from passlib.context import CryptContext

pwd_context = CryptContext(scheme=["bcrypt"])


def encrypt_password(password):
    return pwd_context(password)