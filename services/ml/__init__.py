from .preprocessor import Preprocessor

from pathlib import Path
import pickle
import nltk

nltk.download('stopwords')

BASE = Path(__file__).parent

with open(BASE / "vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open(BASE / "model.pkl", "rb") as f:
    model = pickle.load(f)
