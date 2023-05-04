from services.ml import model, vectorizer, Preprocessor

preprocessor = Preprocessor()


def detect_slang(text: str) -> list:
    """Checking if slang in provided text"""
    return model.predict_proba(
        vectorizer.transform(
            preprocessor.preprocess([text])
        )
    )[0]
