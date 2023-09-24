from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashpassword(user):
    """funcion que recibe usuario del response y encripta su contraseña"""
    hash_password = pwd_context.hash(user.password)
    user.password = hash_password
    
    return user