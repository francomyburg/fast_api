from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashpassword(user):
    """funcion que recibe usuario del response y encripta su contraseña"""
    hash_password = pwd_context.hash(user.password)
    user.password = hash_password
    
    return user

def verifyPassword(password,password_to_verify):
    return pwd_context.verify(password, password_to_verify)