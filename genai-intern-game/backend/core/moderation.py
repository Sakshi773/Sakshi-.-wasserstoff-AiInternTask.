import re

# Basic profanity check (you can integrate with external libraries or APIs)
def check_for_profanity(text: str) -> bool:
    profanity_list = ['badword1', 'badword2']  # Add your own list or API here
    for word in profanity_list:
        if re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE):
            return True
    return False

