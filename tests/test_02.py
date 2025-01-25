# %% Import
import numpy as np

# %% Define utility functions

# Test
tokens = tokenize_sentence("Hello world!")
assert tokens[0] == "hello", "The function should return ['hello', 'world!']"
assert tokens[1] == "world!", "The function should return ['hello', 'world!']"
assert len(tokens) == 2, "The function should return ['hello', 'world!']"

# %% Test -----------
