import os
from dotenv import load_dotenv

# .env file se environment variables load kar rahe hain
load_dotenv()

# Database URL .env se le rahe hain
DATABASE_URL = os.getenv("DATABASE_URL")

# JWT related settings
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
