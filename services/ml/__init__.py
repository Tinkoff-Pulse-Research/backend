from .preprocessor import Preprocessor

from pathlib import Path
import pickle
import nltk
import json

nltk.download('stopwords')

BASE = Path(__file__).parent

with open(BASE / "vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open(BASE / "coefs.json", "rb") as f:
    coefs = json.load(f)
