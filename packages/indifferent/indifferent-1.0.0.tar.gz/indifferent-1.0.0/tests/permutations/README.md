# Permutation tests

These tests are automatically generated. Please do not edit them by hand.

The permutation tests provide a large variety of strings to `indifferent` in all combinations and verify that it can handle all of them. There are a lot of combinations, so they're generated automatically by the script `tests/create_permutation_tests.py`.

These tests don't check for correct answers, but rather ensure there are no failures. The manually-written tests in `tests/test_*.py` should be used to verify correctness.

## How it works

The permutation tests are created by comparing a list of strings with a variety of words and separators, combining them against themselves as the `base` and `revision` values, and then repeating for all `results`.

### Checking more strings

To add more string combinations, add a new item to `test_components` in `tests/create_permutation_tests.py`, re-run the script, and then run `pytest`.

You should do this if you've found a string that makes `indifferent` crash, because it may represent a corner case that isn't tested yet.

### Checking more result formats

To add more result formats (e.g., "html", "table", etc.), add a new item to `results` in `tests/create_permutation_tests.py` re-run the script, and then run `pytest`.

You should do this if you've added a new result format.
