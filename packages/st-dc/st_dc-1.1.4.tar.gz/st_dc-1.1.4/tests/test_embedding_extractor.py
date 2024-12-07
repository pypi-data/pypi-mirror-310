import sys

import numpy as np

sys.path.append("..")

import unittest
from st_dc.embedding_extractor import EmbeddingExtractor

class TestEmbeddingExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = EmbeddingExtractor("bert-base-uncased")
        self.sentences = [
            "The pool is open for swimming.",
            "The stock market pool is rising.",
            
        ]
        self.focus_word = "pool"

    def test_focus_word_embedding(self):
        results = self.extractor.extract_embeddings(self.sentences, self.focus_word, top_n_neighbors=3)
        self.assertEqual(len(results["focus_embeddings"]) - 1, len(self.sentences))
        self.assertTrue(all(isinstance(embedding, list) or isinstance(embedding, np.ndarray) for embedding in results["focus_embeddings"]))

    def test_neighbor_generation(self):
        results = self.extractor.extract_embeddings(self.sentences, self.focus_word, top_n_neighbors=3)
        self.assertEqual(len(results["neighbors"]), len(self.sentences))
        self.assertTrue(all(len(neighbors) == 3 for neighbors in results["neighbors"]))
