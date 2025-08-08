from jose import JWTError,jwt
from datetime import datetime, timedelta
from . import schemas
#SECRET_KEY
#Algorithm
#Expiration time

#SECRET_KEY = 
#ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_enconde = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_enconde.update({"exp":expire})
    
    encoded_jwt = jwt.encode(to_enconde,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
    
    
def verify_access_token(token: str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id:str= payload.get("users_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    
def get_current_user():
    pass