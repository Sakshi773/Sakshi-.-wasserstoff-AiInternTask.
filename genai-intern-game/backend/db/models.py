from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.db.database import Base


# This table stores one row for each new game session.
class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, index=True)
    seed_word = Column(String)                                      # The word to beat in the game
    score = Column(Integer, default=0)                              # Tracks the player's score

    # This helps SQLAlchemy know guesses are linked to sessions
    guesses = relationship("GuessHistory", back_populates="session")


# This table records each guess made in a session.
class GuessHistory(Base):
    __tablename__ = "guess_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('game_sessions.id'))    # Link to GameSession
    guess = Column(String)

    # Back reference to the session
    session = relationship("GameSession", back_populates="guesses")



class GuessCounter(Base):
    __tablename__ = "guess_counter"

    id = Column(Integer, primary_key=True, index=True)
    guess = Column(String, unique=True)                            # We only want one row per unique guess
    count = Column(Integer, default=0)                             # How many times this guess was made



