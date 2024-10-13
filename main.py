from fastapi import FastAPI
from app.api import users, books , rents
from app.db import models
from app.db.database import engine
from fastapi.middleware.cors import CORSMiddleware

# Créer l'application FastAPI
app = FastAPI(
    title="API de gestion de bibliothèque",
    description="Une API pour gérer une bibliothèque, les utilisateurs, les livres et les emprunts.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=['*'],
    allow_origins=["http://localhost","http://127.0.0.1:3000", 'http://localhost:8080', "http://localhost:3000", "https://samsara-web.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Inclure les routeurs pour chaque module de l'API
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(rents.router, prefix="/rents", tags=["Rents"])


# Endpoint racine pour vérifier si l'API fonctionne
@app.get("/")
def read_root():
    return {"message": "Bienvenue à l'API de gestion de bibliothèque"}