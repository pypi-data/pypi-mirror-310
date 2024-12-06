import plotly.graph_objects as go
import random

class EmbeddingVisualizer:
    @staticmethod
    def plot_focus_and_neighbors(
        focus_embeddings, focus_labels, neighbors, title, plot_type="3D"
    ):
        """
        Plot embeddings for the focus word and its nearest neighbors in 2D or 3D.
        :param focus_embeddings: 2D or 3D numpy array of shape (n_focus, n_components)
        :param focus_labels: Labels for focus word contexts (e.g., sentences)
        :param neighbors: List of dictionaries for each context, with 'tokens' and 'embeddings'
        :param title: Title of the plot (e.g., "Focus Word: [focus_word] | Viz")
        :param plot_type: "2D" or "3D" for visualization type
        :return: Plotly figure
        """
        fig = go.Figure()

        # Predefined palette of contrasting colors
        contrasting_colors = [
            "#FF5733",  # Red-orange
            "#33FF57",  # Green
            "#3357FF",  # Blue
            "#FF33A8",  # Pink
            "#A833FF",  # Purple
            "#FFC300",  # Yellow
        ]

        # Randomly pick distinct colors for contexts
        colors = random.sample(contrasting_colors, len(focus_embeddings))

        # Plot focus word embeddings
        for i, (focus_embedding, label, color) in enumerate(zip(focus_embeddings, focus_labels, colors)):
            if plot_type == "3D":
                fig.add_trace(
                    go.Scatter3d(
                        x=[focus_embedding[0]],
                        y=[focus_embedding[1]],
                        z=[focus_embedding[2]],
                        mode="markers",
                        marker=dict(size=10, color=color, symbol="circle"),
                        name=f"{label}"
                    )
                )
            elif plot_type == "2D":
                fig.add_trace(
                    go.Scatter(
                        x=[focus_embedding[0]],
                        y=[focus_embedding[1]],
                        mode="markers",
                        marker=dict(size=10, color=color, symbol="circle"),
                        name=f"{label}"
                    )
                )

        # Plot neighbors for each context
        for i, (neighbor_set, color) in enumerate(zip(neighbors, colors)):
            for token, embedding in zip(neighbor_set["tokens"], neighbor_set["embeddings"]):
                if plot_type == "3D":
                    fig.add_trace(
                        go.Scatter3d(
                            x=[embedding[0]],
                            y=[embedding[1]],
                            z=[embedding[2]],
                            mode="markers+text",
                            marker=dict(size=6, color=color, symbol="diamond"),
                            text=[token],  # Display token directly above the point
                            textfont=dict(size=10),
                            showlegend=False  # Exclude neighbors from legend
                        )
                    )
                elif plot_type == "2D":
                    fig.add_trace(
                        go.Scatter(
                            x=[embedding[0]],
                            y=[embedding[1]],
                            mode="markers+text",
                            marker=dict(size=6, color=color, symbol="diamond"),
                            text=[token],
                            textfont=dict(size=10),
                            showlegend=False
                        )
                    )

        # Customize layout
        if plot_type == "3D":
            fig.update_layout(
                title=title,
                scene=dict(
                    xaxis_title="Dimension 1",
                    yaxis_title="Dimension 2",
                    zaxis_title="Dimension 3",
                ),
                showlegend=True
            )
        elif plot_type == "2D":
            fig.update_layout(
                title=title,
                xaxis_title="Dimension 1",
                yaxis_title="Dimension 2",
                showlegend=True
            )

        return fig
