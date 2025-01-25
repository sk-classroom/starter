# %% Import
import numpy as np

# %% Define utility functions

# Test
# Test
tokens = ["the", "fox", "jumped", "over", "the", "lazy", "dog"]
answer = dict(zip(["the", "fox", "jumped", "over", "lazy", "dog"], [2, 1, 1, 1, 1, 1]))
result = calculate_word_frequency(tokens)
for i, (word, freq) in enumerate(result):
    assert freq == answer[word], f"The function should return {answer} at the index {i}"
assert len(result) == 6, f"The function should return {answer}"

# %% Test -----------
