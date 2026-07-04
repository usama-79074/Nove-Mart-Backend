from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.security import decode_access_token
from app.models.user_model import User

# HTTPBearer: Swagger mein seedha ek clean token field aata hai
# Pehle OAuth2PasswordBearer tha jisme username/password ka confusing popup aata tha
# Ab sirf token paste karo aur Authorize karo - simple!
bearer_scheme = HTTPBearer()


# Token se current logged-in user nikalta hai
# Har protected route mein ye dependency use hogi
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # credentials.credentials mein sirf token hota hai (Bearer word ke baad wala)
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("user_id")
    if user_id is None:
        raise credentials_exception

    # Database se user dhoondh rahe hain
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


# Ye dependency check karti hai ke current user "admin" hai ya nahi
# Categories/Products add-edit-delete sirf admin kar sake, isliye ye use hoga
def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin is allowed to perform this action",
        )
    return current_user
