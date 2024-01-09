from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])

def encrypt_password(password):
    return pwd_context.hash(password)


def verify_password(password, encrypted_password):
    return pwd_context.verify(password, encrypted_password)