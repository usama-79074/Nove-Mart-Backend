# E-Commerce Backend API (FastAPI + PostgreSQL)

Mukammal project — 5 modules ke sath:
1. Authentication (JWT)
2. Category Management
3. Product Management
4. Cart Management
5. Order Management

## Setup Steps

1. PostgreSQL mein database banayein:
   CREATE DATABASE ecommerce_db;

2. `.env` file mein apna DATABASE_URL aur SECRET_KEY set karein.

3. Virtual environment banayein aur dependencies install karein:
   python -m venv venv
   source venv/bin/activate   (Windows: venv\Scripts\activate)
   pip install -r requirements.txt

4. Alembic se migration generate aur apply karein:
   alembic revision --autogenerate -m "create all tables"
   alembic upgrade head

   Note: Agar alembic skip karna chahein, "Base.metadata.create_all()" line
   (main.py mein) automatically tables bana degi.

5. Server run karein:
   uvicorn app.main:app --reload

6. Swagger UI (testing ke liye):
   http://127.0.0.1:8000/docs

## Folder Structure

app/
├── main.py              -> app entry point, sare routers yahan include hote hain
├── database/             -> DB connection (SQLAlchemy engine, session)
├── models/                -> SQLAlchemy tables (User, Category, Product, Cart, Order...)
├── schemas/               -> Pydantic request/response validation
├── routers/                -> API endpoints (URL + HTTP method definitions)
├── services/               -> Actual business logic (routers inhi ko call karte hain)
├── core/                  -> config.py (.env load) + security.py (JWT, hashing)
└── utils/                 -> dependencies.py (get_current_user, get_current_admin)

## End-to-End Testing Flow (Swagger se)

1. **POST /register** -> ek admin user banayein (role="admin") aur ek customer user (role="customer")
2. **POST /login** -> donon ka token alag alag le lein
3. Swagger ke "Authorize" button se admin ka token lagayein
4. **POST /categories** -> category banayein (e.g. "Electronics")
5. **POST /products** -> us category mein product banayein (price, stock_quantity ke sath)
6. Ab "Authorize" mein customer ka token lagayein (logout karke dobara authorize karein)
7. **POST /cart/add** -> product_id aur quantity bhej kar cart mein add karein
8. **GET /cart** -> cart dekhein, total_amount check karein
9. **POST /orders/create** -> order create hoga (cart se order banega, stock kam hoga, cart khali ho jayega)
10. **GET /orders** -> apne saare orders ki list dekhein
11. **GET /orders/{id}** -> ek specific order ki detail dekhein

## Important Logic Points (Interview/Viva ke liye yaad rakhein)

- **Password kabhi plain text mein save nahi hota** — bcrypt se hash hota hai (core/security.py)
- **JWT token** mein user_id aur role chhupa hota hai, har protected route token verify karta hai
- **Role-based access**: Categories/Products ka Create/Update/Delete sirf admin kar sakta hai
  (get_current_admin dependency check karti hai)
- **Cart -> Order conversion**: order create hone se pehle stock check hota hai (sab products ka),
  tabhi order banta hai aur stock minus hota hai — taake order aadha na bane
- **Order item mein price save hoti hai** (product ki current price nahi) — taake future mein
  product price change ho to purane orders ka record na badle
- **Partial updates**: PUT endpoints mein sirf wahi fields update hoti hain jo user bheje (baqi None ignore)
 