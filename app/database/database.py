from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

# Engine: yeh actual connection PostgreSQL database se banata hai
engine = create_engine(DATABASE_URL)

# SessionLocal: har request ke liye ek naya database session banane ke liye
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class: hamare saare models (tables) isi se inherit karenge
Base = declarative_base()


# Dependency function: ye FastAPI routes mein use hoga
# Request aane par DB session open hota hai, kaam khatam hone par close ho jata hai
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
