from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.routers import (
    auth_router,
    category_router,
    product_router,
    cart_router,
    order_router,
)

# Database tables create karega (development ke liye)
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(title="E-Commerce Backend API")

# -----------------------------
# CORS Configuration
# -----------------------------
origins = [
    "http://localhost:5173",                     # Local frontend
    "https://nova-mart-frontend-kappa.vercel.app",  # Vercel frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# API Routers
# -----------------------------
app.include_router(auth_router.router)
app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(cart_router.router)
app.include_router(order_router.router)

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "E-Commerce API is running"}