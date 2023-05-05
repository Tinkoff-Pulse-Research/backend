from services.ml import coefs, vectorizer, Preprocessor
from typing import List

preprocessor = Preprocessor()


def detect_slang(text: str) -> List[int]:
    """
    Checking if slang in provided text
    :param text: text to check
    :return: list of indices of words that are slang
    """
    preprocessed_text = preprocessor.preprocess([text])[0]
    vec = vectorizer.transform([preprocessed_text])

    result = {}
    vocab = {value: key for key, value in vectorizer.vocabulary_.items()}
    for i, slang_influence in zip(range(vec.shape[1]), coefs):
        sentence_influence = vec[0, i] * slang_influence
        if sentence_influence > 2.0:
            result[vocab[i]] = slang_influence

    res = []

    for i, word in enumerate(text.split()):
        preprocessed_word = preprocessor.preprocess([word])[0]
        if preprocessed_word in result:
            res += [i]

    return res
