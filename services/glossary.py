import json
import re
import string
import typing
from difflib import get_close_matches
from pathlib import Path
import pymorphy2

glossary = json.loads((Path(__file__).parent / "glossary.json").read_text(encoding="utf-8"))
morph = pymorphy2.MorphAnalyzer(lang='ru')


def remove_punctuation(s: str) -> str:
    """Removes all punctuation in text excluding dashes and hyphens"""
    for sign in ",.!?<>@#$%^&*()_+=:;'\"/\\":
        s = s.replace(sign, "")
    return s


def get_term_definition(term: str) -> typing.Optional[typing.Tuple[typing.Optional[str], typing.Optional[str]]]:
    key = term.capitalize().strip()
    definition = glossary.get(key, None)
    if definition is None:
        key = morph.parse(term)[0].normal_form.capitalize().strip()
        definition = glossary.get(key, None)
    if definition is None:
        match = get_close_matches(
            term.capitalize().strip().lower(),
            map(lambda x: x.lower(), glossary), cutoff=0.9, n=1
        )
        # print(match)
        if not match:
            return None, None
        key = str(match[0]).capitalize()
        definition = glossary.get(key, None)
    return definition, key


def get_terms(text: str) -> typing.Optional[list[dict]]:
    """Returning a list of terms found in provided text"""
    result = []
    words = text.split()
    for i in range(len(words)):
        word = remove_punctuation(words[i])
        pair = remove_punctuation(" ".join(words[i:i + 2]) if i + 2 <= len(words) else "")
        triple = remove_punctuation(" ".join(words[i:i + 3]) if i + 3 <= len(words) else "")
        # pair = ""
        # triple = ""
        word, pair, triple = map(lambda x: x.replace(".", "").replace(",", ""), (word, pair, triple))
        for seq in {word, pair, triple}:
            if not seq:
                continue
            if any(len(word) == 1 for word in seq.split()):
                continue
            # print(seq)
            definition = get_term_definition(seq)[0]
            if not definition:
                if match := get_close_matches(
                    seq.lower(),
                    map(lambda x: x.lower(), glossary),
                    cutoff=0.9,
                    n=1,
                ):
                    definition = glossary.get(str(match[0]).capitalize(), None)
            if definition:
                result.append({
                    seq: definition
                })
    return result


if __name__ == '__main__':
    print(get_terms("Пампить или не пампить, вот в чем вопрос. Входить в лангусты или ждать лучших дивгэпов?"))
