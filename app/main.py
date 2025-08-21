from fastapi import FastAPI
from app.routes import auth_routes, money_routes

app = FastAPI()

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(money_routes.router, prefix="/money", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}
