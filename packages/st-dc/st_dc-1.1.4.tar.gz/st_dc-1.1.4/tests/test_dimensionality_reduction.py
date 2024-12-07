import sys

import numpy as np

sys.path.append("..")

import unittest
import numpy as np
from st_dc.dimensionality_reduction import DimensionalityReducer

class TestDimensionalityReducer(unittest.TestCase):
    def setUp(self):
        self.reducer = DimensionalityReducer(method="pca", n_components=2)
        self.embeddings = np.random.rand(10, 768)  # Mock embeddings

    def test_reduce_dimensions(self):
        reduced = self.reducer.reduce(self.embeddings)
        self.assertEqual(reduced.shape, (10, 2))
