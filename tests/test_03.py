# %% Import
import numpy as np

# %% Define utility functions

# Test
tokens = remove_stopwords(["the", "fox", "jumped", "over", "the", "lazy", "dog"], ["the", "lazy"])

answer = ["fox", "jumped", "over", "dog"]
for i, token in enumerate(tokens):
    assert token == answer[i], f"The function should return {answer} at the index {i}"
assert len(tokens) == 4, f"The function should return {answer}"

# %% Test -----------
