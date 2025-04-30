# main.py

from fastapi import FastAPI
from backend.api import game  

from backend.core import ai_client 
from backend.core import cache

# This is the main FastAPI app
app = FastAPI(title="Generative AI Game API")

# Registering API routes from our game module (which now includes session logic)
app.include_router(game.router)

# Basic root route for testing
@app.get("/")
def read_root():
    return {"message": "Welcome to the Generative AI Game API!"}

# ---- TEMPORARY Creating DB tables ----
from backend.db.database import Base, engine
from backend.db import models

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
# -------------------------------------
