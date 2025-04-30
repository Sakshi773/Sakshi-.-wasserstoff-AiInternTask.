async function submitGuess() {
    const guess = document.getElementById('guess').value;                          // Get the guess input value
    const sessionId = 1;                                                         
    const persona = 'serious';                        

    // Send the guess to the backend via a POST request
    const response = await fetch('http://localhost:8000/guess/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ guess: guess, session_id: sessionId, persona: persona }),
    });

    // Get the response data
    const data = await response.json();

    // Display the result in the 'result' div
    document.getElementById('result').innerText = data.message;
}

 
