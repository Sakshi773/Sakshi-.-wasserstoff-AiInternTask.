import requests
import time

BASE_URL = "http://localhost:9000"  

def test_start_session():
    """
    Test the `/start-session/` endpoint.
    It should create a session and return a session ID.
    """
    print("Testing Start Session Endpoint...")
    response = requests.post(f"{BASE_URL}/start-session/?seed_word=Rock")
    assert response.status_code == 200, f"Failed to start session: {response.text}"
    
    data = response.json()
    assert "session_id" in data, "Session ID not returned"
    
    session_id = data["session_id"]
    print(f"Session started successfully with session_id: {session_id}")
    return session_id


def test_make_guess(session_id):
    """
    Test the `/guess/` endpoint.
    It should accept a guess and return a message about whether the guess is correct or not.
    """
    print("Testing Make Guess Endpoint...")
    payload = {"guess": "Paper", "session_id": session_id, "persona": "serious"}
    response = requests.post(f"{BASE_URL}/guess/", json=payload)
    assert response.status_code == 200, f"Failed to make a guess: {response.text}"
    
    data = response.json()
    assert "message" in data, "Message not returned in response"
    
    print(f"Response: {data['message']}")

    # Test duplicate guess
    print("Testing Duplicate Guess...")
    response_duplicate = requests.post(f"{BASE_URL}/guess/", json=payload)
    assert response_duplicate.status_code == 200, f"Failed to make duplicate guess: {response_duplicate.text}"
    
    data_duplicate = response_duplicate.json()
    assert "duplicate" in data_duplicate["message"].lower(), "Duplicate guess not handled correctly"
    print(f"Duplicate Guess Response: {data_duplicate['message']}")

    
def test_profanity_check(session_id):
    """
    Test that the profanity filter works correctly for disallowed words.
    """
    print("Testing Profanity Check...")
    payload = {"guess": "badword1", "session_id": session_id, "persona": "serious"}
    response = requests.post(f"{BASE_URL}/guess/", json=payload)
    assert response.status_code == 400, f"Profanity filter failed: {response.text}"
    
    data = response.json()
    assert "contains disallowed content" in data["detail"], "Profanity filter message is missing or incorrect"
    print(f"Profanity Check Response: {data['detail']}")


def run_tests():
    """
    Run the full test flow: start session, make guesses, test profanity filter.
    """
    print("Running E2E Tests...\n")
    
    session_id = test_start_session()              # Step 1: Start session
    test_make_guess(session_id)                    # Step 2: Make guesses
    test_profanity_check(session_id)               # Step 3: Test profanity filtering

    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    run_tests()
