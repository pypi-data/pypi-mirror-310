import pytest
from collections import Counter

from small_language_model import SmallLanguageModel


def test_initializes_with_empty_dict() -> None:
    slm = SmallLanguageModel()

    assert len(slm.char_map) == 0


@pytest.fixture
def initialized_slm() -> SmallLanguageModel:
    slm = SmallLanguageModel()
    slm.train("Hello")

    return slm


def test_train(initialized_slm):
    correct_H = Counter({"e": 1})
    assert initialized_slm.char_map["H"] == correct_H

    correct_e = Counter({"l": 1})
    assert initialized_slm.char_map["e"] == correct_e

    correct_l = Counter({"l": 1, "o": 1})
    assert initialized_slm.char_map["l"] == correct_l

    # There should not be any extra letters in the dict.
    # Note the final "o" in "Hello" should not be in the dict.
    assert set(initialized_slm.char_map.keys()) == set("Hell")


def test_predict(initialized_slm: SmallLanguageModel) -> None:
    assert initialized_slm.predict_next("H") == "e"

    assert initialized_slm.predict_next("e") == "l"


# This mark + the function below are intended to be equal to the test_predict method above
@pytest.mark.parametrize("input, expected_prediction", [("H", "e"), ("e", "l")])
def test_predicted_expected(
    initialized_slm: SmallLanguageModel, input: str, expected_prediction: str
) -> None:
    assert initialized_slm.predict_next(input) == expected_prediction


def test_edge_cases(initialized_slm: SmallLanguageModel) -> None:
    assert initialized_slm.predict_next("o") is None
    assert initialized_slm.predict_next("z") is None
