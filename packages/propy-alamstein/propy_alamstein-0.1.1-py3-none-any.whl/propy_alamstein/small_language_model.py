from collections import defaultdict, Counter
import random
from typing import DefaultDict, Counter as TypingCounter, List, Tuple


class SmallLanguageModel:
    def __init__(self) -> None:
        self.char_map: DefaultDict[str, TypingCounter[str]] = defaultdict(Counter)

    def train(self, text: str) -> None:
        if len(text) < 2:
            raise Exception("Text is too short")

        for i in range(len(text) - 1):
            current_char = text[i]
            next_char = text[i + 1]
            self.char_map[current_char][next_char] += 1

    def predict_next(self, current_char: str) -> str | None:
        if current_char not in self.char_map:
            return None
        next_chars, weights = zip(*self.char_map[current_char].items())
        if next_chars:
            chosen_char: str | None = random.choices(next_chars, weights=weights)[0]
        else:
            chosen_char = None
        return chosen_char

    def get_character_training_frequency(self) -> List[Tuple[str, int]]:
        """
        Returns the number of times each character appears in the training data.

        Returns a list of tuples. The first character in the tuple is the character.
        The second character is the number of times it appears. The list is sorted
        in descending order.
        """
        # The total frequency of a letter is the sum of all the letters which come after it
        num_occurences: dict[str, int] = {}
        for k, v in self.char_map.items():
            num_occurences[k] = sum(v.values())

        # Now sort and return the frequency data
        return sorted(num_occurences.items(), key=lambda x: x[1], reverse=True)


# Example usage
if __name__ == "__main__":
    slm = SmallLanguageModel()
    slm.train("hello")
    print(slm.char_map)
    print(slm.predict_next("l"))
    print(slm.predict_next("l"))
    print(slm.get_character_training_frequency())
