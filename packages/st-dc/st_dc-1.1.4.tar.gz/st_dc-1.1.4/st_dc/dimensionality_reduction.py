from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import numpy as np

class DimensionalityReducer:
    def __init__(self, method="pca", n_components=2):
        """
        Initialize the dimensionality reducer.
        :param method: Reduction method ('pca', 'tsne', or 'umap')
        :param n_components: Number of dimensions for reduction (default: 2)
        """
        self.method = method.lower()
        self.n_components = n_components

    def reduce(self, embeddings):
        """
        Reduce the dimensionality of embeddings.
        :param embeddings: High-dimensional embeddings (numpy array or torch.Tensor)
        :return: Reduced embeddings (numpy array)
        """
        if isinstance(embeddings, np.ndarray):
            data = embeddings
        else:
            data = embeddings.detach().numpy()

        if self.method == "pca":
            reducer = PCA(n_components=self.n_components)
        elif self.method == "tsne":
            reducer = TSNE(n_components=self.n_components, perplexity=min(len(data) - 1, 1), random_state=42)
        else:
            raise ValueError(f"Unsupported method: {self.method}. Use 'pca' or 'tsne'.")

        reduced_embeddings = reducer.fit_transform(data)
        return reduced_embeddings
