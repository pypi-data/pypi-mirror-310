# Small Language Model

Final project for Matt Harrison / MetaSnake's [Professional Python](https://store.metasnake.com/propy) course.

The core code in this repo is the class `SmallLanguageModel` in the file `small_language_model.py`. However, that code is largely irrelevant, and exists just as a vehicle for us to explore modern tools used in Python development:

  * `uv` instead of `pip` for installing packages
  * LLMs to write code
  * Automated tests with `pytest`
  * Type Annotations
  * pre-commit and GitHub Actions to automate testing, linting with `ruff`, etc.
  * Deploying a package to PyPI

If, despite the above warning, you still want to run the code in this repo, you can do so like this:

```python
from small_language_model import SmallLanguageModel

slm = SmallLanguageModel()
slm.train("The quick brown fox jumped over the lazy dogs")

slm.predict_next("a")
slm.get_character_training_frequency()
```
