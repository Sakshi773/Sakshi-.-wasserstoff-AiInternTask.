from sqlalchemy.orm import Session
from backend.db import models

from backend.core.ai_client import call_genai
from backend.core.cache import get_cached_verdict


async def process_guess(guess: str, session_id: str, persona: str, db: Session):
    
    
    # Get the current game session from the database using the session_id
    game_session = db.query(models.GameSession).filter(models.GameSession.id == session_id).first()
    
    # If no session found it will raise an exception
    if not game_session:
        raise Exception("Game session not found")

    seed_word = game_session.seed_word                                                   # Retrieving the seed word from the session

    # Checking if the guess has been validated before 
    cached_verdict = get_cached_verdict(session_id, guess)
    
    if cached_verdict:
        # If the verdict is cached i will return it without checking the AI again
        return cached_verdict.decode('utf-8')                                            # The use of caching here is to avoid repeatedly asking the AI for the same question.

    # Calling the  fake AI logic to check if the guess beats the seed word
    ai_verdict = await call_genai(guess, seed_word, persona)

    if ai_verdict.lower() == 'yes':
        

        # Checking if this guess has been made before in the current game session
        existing_guess = db.query(models.GuessHistory).filter(models.GuessHistory.session_id == session_id, models.GuessHistory.guess == guess).first()
        
        if existing_guess:
            return "Game Over! Duplicate guess."

        # If it's a new guess i will add it to the history
        new_guess = models.GuessHistory(session_id=session_id, guess=guess)
        db.add(new_guess)
        db.commit()

        # Updating the score 
        game_session.score += 1
        db.commit()

        
        return f"✅ Nice! {guess} beats {seed_word}. You've scored {game_session.score} points."
    
    else:
        
        return f"❌ {guess} does not beat {seed_word}. Try again."           # If the AI says "no", the guess doesn't beat the seed word
