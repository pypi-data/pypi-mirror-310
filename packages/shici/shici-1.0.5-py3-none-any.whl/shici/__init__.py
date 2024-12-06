import os
from pathlib import Path
from random import choice as random_choice

__version__ = "1.0.5"
DB = Path(__file__).parent / "favorite.txt"
WORDS = DB.read_text("utf-8").strip().splitlines()
CHOICES = [i for i in WORDS if not i.startswith("#")]


def random(ignore_comment_line: bool = True) -> str:
    ws = CHOICES if ignore_comment_line else [i.strip(" #") for i in WORDS]
    return random_choice(ws)  # nosec


def join(*words) -> bool:
    news = [w for w in words if w not in WORDS]
    try:
        DB.write_text("\n".join(WORDS + news))
    except Exception as e:
        print("Failed to save local:", e)
        return False
    WORDS.extend(news)
    CHOICES.extend([i for i in news if not i.startswith("#")])
    print("Success to extend these words:", news)
    return True


def remove(word: str) -> None:
    if word in WORDS:
        words = [w for w in WORDS if w != word]
        DB.write_text(os.linesep.join(words), encoding="utf-8")
        print("Local data updated!")
