from fastapi import FastAPI
from app.api import users, books
from app.db import models
from app.db.database import engine


# Créer l'application FastAPI
app = FastAPI(
    title="API de gestion de bibliothèque",
    description="Une API pour gérer une bibliothèque, les utilisateurs, les livres et les emprunts.",
    version="1.0.0"
)

# Inclure les routeurs pour chaque module de l'API
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(books.router, prefix="/books", tags=["Books"])

# Endpoint racine pour vérifier si l'API fonctionne
@app.get("/")
def read_root():
    return {"message": "Bienvenue à l'API de gestion de bibliothèque"}