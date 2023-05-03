import json
import typing
from pathlib import Path

glossary = json.loads((Path(__file__).parent / "glossary.json").read_text(encoding="utf-8"))


def get_term_definition(term: str) -> typing.Optional[str]:
    return glossary.get(term.capitalize().strip(), None)


if __name__ == '__main__':
    print(get_term_definition("памп"))
