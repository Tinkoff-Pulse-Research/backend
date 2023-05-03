import json
import re
import string
import typing
from pathlib import Path
import pymorphy2

glossary = json.loads((Path(__file__).parent / "glossary.json").read_text(encoding="utf-8"))
morph = pymorphy2.MorphAnalyzer(lang='ru')


def get_term_definition(term: str) -> typing.Optional[str]:
    definition = glossary.get(term.capitalize().strip(), None)
    if definition is None:
        return glossary.get(morph.parse(term)[0].normal_form.capitalize().strip(), None)


def get_terms(text: str) -> typing.Optional[list[dict]]:
    """Returning a list of terms found in provided text"""
    result = []
    for word in text.split():
        word = re.sub(re.escape(string.punctuation), "", word)
        if definition := get_term_definition(word):
            result.append({
                word: definition
            })
    return result


if __name__ == '__main__':
    print(get_term_definition("памп"))
