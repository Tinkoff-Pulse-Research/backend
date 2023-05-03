import random
from ml import model, vectorizer, Preprocessor

preprocessor = Preprocessor()


def detect_slang(text: str) -> bool:
    """Checking if slang in provided text"""
    return random.choice([True, False])  # Mocking data
