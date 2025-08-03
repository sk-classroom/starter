# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy",
# ]
# ///

# %% Import
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from assignment.assignment import calc_square

# %% Test -----------
x = np.random.randn(10)

z = calc_square(x)

assert z.shape == x.shape, "The shape of the output should be the same as the input"
assert np.all(np.isclose(z, x**2)), "The output should be the square of the input"
