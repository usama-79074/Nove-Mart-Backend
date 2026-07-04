from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# bcrypt scheme use karenge password hash karne ke liye
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Plain password ko hash mein convert karta hai (register ke time)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Login ke time plain password ko hash se match karta hai
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# JWT access token banata hai
# data mein hum user ki id aur role daalenge (payload)
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Token ko decode/verify karta hai
# Agar token invalid ya expire ho gaya to None return karega
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
