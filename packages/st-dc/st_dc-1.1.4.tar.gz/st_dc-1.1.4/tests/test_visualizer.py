import sys

sys.path.append("..")

import unittest
from st_dc.visualizer import EmbeddingVisualizer
import numpy as np

class TestEmbeddingVisualizer(unittest.TestCase):
    def setUp(self):
        self.visualizer = EmbeddingVisualizer()
        self.focus_embeddings = np.random.rand(3, 3)  # Mock 3D embeddings
        self.focus_labels = ["Context 1", "Context 2", "Context 3"]
        self.neighbors = [
            {"tokens": ["neighbor1", "neighbor2"], "embeddings": np.random.rand(2, 3)},
            {"tokens": ["neighbor3", "neighbor4"], "embeddings": np.random.rand(2, 3)},
            {"tokens": ["neighbor5", "neighbor6"], "embeddings": np.random.rand(2, 3)},
        ]

    def test_plot_focus_and_neighbors(self):
        fig = self.visualizer.plot_focus_and_neighbors(
            focus_embeddings=self.focus_embeddings,
            focus_labels=self.focus_labels,
            neighbors=self.neighbors,
            title="Test Viz",
            plot_type="3D"
        )
        self.assertIsNotNone(fig)
