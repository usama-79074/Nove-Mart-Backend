from fastapi import FastAPI
from app.database.database import Base, engine
from app.routers import auth_router, category_router, product_router, cart_router, order_router

# Sare models ke tables database mein create kar dega (agar pehle se nahi bane)
# Note: Hum Alembic bhi use karenge proper migrations ke liye, ye sirf dev ke liye line hai
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce Backend API")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers ko app mein include kar rahe hain
app.include_router(auth_router.router)
app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(cart_router.router)
app.include_router(order_router.router)


# Simple test route, check karne ke liye ke server chal raha hai
@app.get("/")
def root():
    return {"message": "E-Commerce API is running"}




#alembic migration commands
#alembic init alembic
#alembic revision --autogenerate -m "Initial migration"
#alembic upgrade head