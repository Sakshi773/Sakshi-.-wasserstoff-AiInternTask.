
# Importing necessary things from FastAPI and other files
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.core.game_logic import process_guess                                 # This decides if the guess is right/wrong
from backend.core.cache import get_cached_verdict, cache_guess_verdict            # Caching guess results
from backend.core.moderation import check_for_profanity                           # Checking if a guess is inappropriate
from backend.db.database import get_db                                            # Getting the database session
from backend.db import models                                                     # Database models (GameSession, GuessHistory)

# This will handle the routing of requests (API calls) for the game
router = APIRouter()

# This class defines what data to expect when a player makes a guess
class GuessRequest(BaseModel):
    guess: str  
    session_id: int  
    persona: str = 'serious'                                                   # the "mood" of the AI (default is serious)

# Endpoint: Starting a new game session
@router.post("/start-session/")
async def start_session(seed_word: str, db: Session = Depends(get_db)):
    """
    This function starts a new game with a seed word like 'Rock' and creates a game session.
    It returns the session ID so the player can continue making guesses in that session.
    """
    new_session = models.GameSession(seed_word=seed_word)  
    db.add(new_session)                                                        # Save the session to the database
    db.commit()                                                                
    db.refresh(new_session)                                                     # Refresh to get the new session ID
    
    # Return the session ID to the player so they can start guessing
    return {"session_id": new_session.id}

# Endpoint: Player makes a guess
@router.post("/guess/")
async def make_guess(request: GuessRequest, db: Session = Depends(get_db)):
    """
    When a player makes a guess, I'll first check if the guess is clean (no bad words),
    then I'll check if we've already calculated this guess and if not, calculate it.
    """
    # Step 1: Check if the guess contains any bad words
    if check_for_profanity(request.guess):
        raise HTTPException(status_code=400, detail="❌ Your guess contains bad words.")
    
    # Step 2: Check if we've already calculated this guess result (cache)
    cached_result = get_cached_verdict(str(request.session_id), request.guess)
    if cached_result:
        # If we've already calculated the result before, return the cached result
        return {
            "message": cached_result.decode('utf-8'),  
            "cached": True  # Lets the player know we used a cached result
        }
    
    # Step 3: Call the AI to calculate if the guess beats the seed word 
    result_message = await process_guess(request.guess, request.session_id, request.persona, db)

    # Step 4: Cache the result so we don’t have to calculate it again in the future
    cache_guess_verdict(str(request.session_id), request.guess, result_message)

    # Return the result of the guess (whether it was right or wrong)
    return {
        "message": result_message,  
        "cached": False  # Lets the player know this result was freshly calculated
    }

# Endpoint: Show the last 5 guesses for a given game session
@router.get("/history/{session_id}")
async def get_guess_history(session_id: int, db: Session = Depends(get_db)):
    """
    This endpoint returns the last 5 guesses made in a given game session.
    If no guesses are found, a 404 error is returned.
    """
    guesses = db.query(models.GuessHistory).filter(models.GuessHistory.session_id == session_id).all()

    if not guesses:
        raise HTTPException(status_code=404, detail="No guesses found for this session.")

    # Return only the last 5 guesses 
    recent_guesses = [guess.guess for guess in guesses][-5:]

    return {"guesses": recent_guesses}





    

