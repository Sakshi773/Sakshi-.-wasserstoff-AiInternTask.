# Sakshi-.-wasserstoff-AiInternTask.

Rock-Paper-Scissors AI Game is a web-based game where you play Rock, Paper, Scissors against an AI. The game remembers past moves and lets the AI try to guess strategy to make the game more challenging. It’s built using FastAPI for the backend, React for the frontend, Redis for caching and Docker to make setup and deployment easy.

## SETUP:

### 1. Cloning the repository
git clone https://github.com/<Sakshi773>/<Sakshi-.-wasserstoff-AiInternTask.>.git
cd <Sakshi-.-wasserstoff-AiInternTask.>

### 2. Running the application
docker-compose up --build

### 3. Accessing the Application
Backend API Docs (Swagger UI): http://localhost:9000/docs

### 4. Stopping the Application
docker-compose down

## HOW TO PLAY THE GAME?

### 1. Start a Game Session
a) Endpoint: POST /start-session
b) What to do: Provide an initial seed word i.e. rock.
c) Purpose: This sets the  base idea for the session.
d) Result: The API returns a session_id like 4. Use this ID to make guesses.

### 2.Make a Guess
a) Endpoint: POST /guess
b) What to do: Use the session ID from the previous step and submit a word guess.
c) Purpose: The API checks if the guess is valid, compares it to internal associations and possibly updates the game state.

### 3. Check Guess History 
a) Endpoint: GET /history/{session_id}
b) What it does: Retrieves the last 5 guesses made in the current session.
c) Why it helps: Useful if you want to track your progress, avoid repeating guesses or get inspired for the next move.

## Architectural Choices
1. FastAPI was used to build a clean and responsive backend with automatic docs (Swagger UI).

2. The API has three main routes:
a) /start-session: begins a game
b) /guess: makes a word guess
c) /history/{session_id}: shows last 5 guesses

3. Each game is tracked using a unique session_id to separate user sessions.

4. For simplicity, all data (sessions and guesses) is stored in memory using Python dictionaries.

5. Proper error handling is included (404, 422, 500) with clear messages.

6. The built-in Swagger UI at localhost:9000/docs makes it easy to test the API manually.



