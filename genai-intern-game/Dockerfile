# Start with a base Python image
FROM python:3.10-slim

# Set the working directory inside the container to /genai-intern-game
WORKDIR /genai-intern-game

# Copy all files from the current directory (your local machine) to /genai-intern-game in the container
COPY . /genai-intern-game

# Install dependencies (if you have a requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 9000 (if that's what your app runs on)
EXPOSE 9000

# Set the environment variable to specify the Python path
ENV PYTHONPATH=/genai-intern-game/backend


# Run the app using Uvicorn (adjust according to your setup)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]







