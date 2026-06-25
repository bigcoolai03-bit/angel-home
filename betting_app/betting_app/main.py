from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random
from datetime import datetime

app = FastAPI(title="ANGEL HOME - Paris Sportifs")

# Permet au frontend de fonctionner
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulation de base de données
users = {}
matches = [
    {"id": 1, "home": "PSG", "away": "OM", "cote_home": 1.85, "cote_draw": 3.60, "cote_away": 4.10, "time": "21:00"},
    {"id": 2, "home": "Real Madrid", "away": "Barcelone", "cote_home": 2.10, "cote_draw": 3.40, "cote_away": 3.30, "time": "22:00"},
    {"id": 3, "home": "Manchester City", "away": "Liverpool", "cote_home": 1.95, "cote_draw": 3.50, "cote_away": 3.70, "time": "Maintenant"},
]

class Bet(BaseModel):
    match_id: int
    choice: str   # "home", "draw" ou "away"
    amount: float

bets = []

@app.get("/")
def home():
    return {"message": "Bienvenue sur **ANGEL HOME** ⚽️", "status": "online"}

@app.get("/matches")
def get_matches():
    return matches

@app.post("/register")
def register(username: str, email: str, password: str):
    if username in users:
        raise HTTPException(status_code=400, detail="Cet utilisateur existe déjà")
    users[username] = {
        "email": email,
        "password": password,
        "balance": 100.0
    }
    return {"message": "Compte créé avec succès !", "solde": 100.0}

@app.post("/bet")
def place_bet(username: str, bet: Bet):
    if username not in users:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    user = users[username]
    if user["balance"] < bet.amount:
        raise HTTPException(status_code=400, detail="Solde insuffisant")
    
    user["balance"] -= bet.amount
    bets.append({
        "user": username,
        "match_id": bet.match_id,
        "choice": bet.choice,
        "amount": bet.amount,
        "time": datetime.now().strftime("%H:%M")
    })
    return {
        "message": "Pari placé avec succès !",
        "nouveau_solde": round(user["balance"], 2)
    }

@app.get("/bets/{username}")
def get_user_bets(username: str):
    return [b for b in bets if b["user"] == username]

@app.get("/user/{username}")
def get_user(username: str):
    if username not in users:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return users[username]
