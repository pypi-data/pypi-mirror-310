from st_dc.embedding_extractor import EmbeddingExtractor
from st_dc.dimensionality_reduction import DimensionalityReducer
from st_dc.visualizer import EmbeddingVisualizer
import numpy as np

def viz(word, sentences, dim_technique="pca", num_neighbors=5, plot_type="3D"):
    """
    Visualize contextual word embeddings and their neighbors.
    
    :param word: The focus word to analyze.
    :param sentences: List of sentences containing the focus word.
    :param dim_technique: Dimensionality reduction technique (e.g., "pca", "tsne").
    :param num_neighbors: Number of neighbors to visualize for each context.
    :param plot_type: Type of plot ("2D" or "3D").
    """
    # Step 1: Extract embeddings
    extractor = EmbeddingExtractor("bert-base-uncased")
    results = extractor.extract_embeddings(sentences, word, top_n_neighbors=num_neighbors)

    focus_embeddings = np.array(results["focus_embeddings"])
    all_neighbors = results["neighbors"]
    neighbor_embeddings = results["neighbor_embeddings"]

    # Step 2: Perform dimensionality reduction
    n_components = 3 if plot_type == "3D" else 2
    reducer = DimensionalityReducer(method=dim_technique, n_components=n_components)

    reduced_focus_embeddings = reducer.reduce(focus_embeddings)
    reduced_neighbors = [
        reducer.reduce(np.array(neighbors)) for neighbors in neighbor_embeddings
    ]

    # Step 3: Visualize the embeddings
    visualizer = EmbeddingVisualizer()

    fig = visualizer.plot_focus_and_neighbors(
        focus_embeddings=reduced_focus_embeddings,
        focus_labels=sentences,  # Sentences serve as labels for focus word contexts
        neighbors=[
            {"tokens": context_neighbors, "embeddings": reduced_context_neighbors}
            for context_neighbors, reduced_context_neighbors in zip(all_neighbors, reduced_neighbors)
        ],
        title=f"Focus Word: {word} | {plot_type} Viz",
        plot_type=plot_type
    )

    # Show the plot
    fig.show()
