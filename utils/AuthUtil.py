from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])

class AuthUtil:
    def encrypt_password(self, password):
        return pwd_context.hash(password)


    def verify_password(self, password, encrypted_password):
        return pwd_context.verify(password, encrypted_password)
    