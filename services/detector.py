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

    word_slang_influence = {}
    for i, coefficient in enumerate(coefs):
        if coefficient > 0.7:
            word_slang_influence[i] = coefficient

    vocab = {value: key for key, value in vectorizer.vocabulary_.items()}

    for i in range(vec.shape[1]):
        sentence_influence = vec[0, i]
        if sentence_influence > 0.2 and i in word_slang_influence:
            slang_influence = word_slang_influence[i]
            result[vocab[i]] = slang_influence
    
    res = []

    for i, word in enumerate(text.split()):
        preprocessed_word = preprocessor.preprocess([word])[0]
        if preprocessed_word in result:
            res += [i]

    return res
