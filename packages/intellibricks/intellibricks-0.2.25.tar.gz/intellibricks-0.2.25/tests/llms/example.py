from dotenv import load_dotenv
from msgspec import Struct
from intellibricks import CompletionEngine

load_dotenv(override=True)


class Joke(Struct):
    joke: str


# One line to rule them all 🔥
output = CompletionEngine().complete("Tell me a joke", response_format=Joke)

joke = output.get_parsed()  # Joke obj
