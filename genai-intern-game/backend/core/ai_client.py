from backend.core import ai_client


USE_FAKE_AI = True    



async def call_genai(guess: str, seed_word: str, persona: str) -> str:

    """
    This function checks if the player's guess beats the seed word.
    If we're using fake AI, it just compares the words (like Rock, Paper, Scissors).
    If we're using real AI (OpenAI), it calls OpenAI's API for a more complex check (removed in this version).
    """
    
    
    if USE_FAKE_AI:
        # Simple logic for fake AI: Just compare the guesses (like Rock, Paper, Scissors)
        guess = guess.lower()  
        seed_word = seed_word.lower()  

        # Checking if the guess beats the seed word 
        if guess == "paper" and seed_word == "rock":
            return "YES"
        elif guess == "scissors" and seed_word == "paper":
            return "YES"
        elif guess == "rock" and seed_word == "scissors":
            return "YES"
        else:
            return "NO"
