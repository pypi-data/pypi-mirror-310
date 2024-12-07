from transformers import AutoModelForMaskedLM, AutoTokenizer
import torch

class EmbeddingExtractor:
    def __init__(self, model_name="bert-base-uncased"):
        """
        Initialize the extractor with a pre-trained model for masked language modeling.
        :param model_name: Name of the pre-trained model (default: bert-base-uncased)
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForMaskedLM.from_pretrained(model_name, output_hidden_states=True)

    def get_masked_predictions(self, masked_sentence, focus_word, top_n=5):
        """
        Predict the top-N tokens for the masked position in the sentence.
        :param masked_sentence: Sentence with a [MASK] token
        :param focus_word: The focus word being replaced
        :param top_n: Number of predictions to return
        :return: List of predicted tokens
        """
        # Tokenize and process the masked sentence
        inputs = self.tokenizer(masked_sentence, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Extract predictions for the [MASK] token
        mask_index = (inputs.input_ids == self.tokenizer.mask_token_id).nonzero(as_tuple=True)[1].item()
        logits = outputs.logits[0, mask_index]
        probabilities = torch.nn.functional.softmax(logits, dim=-1)

        # Get top-N predictions and filter them
        all_indices = torch.topk(probabilities, top_n * 10).indices  # Get more words initially for filtering
        predicted_tokens = [
            self.tokenizer.decode([idx.item()]).strip()  # Convert token ID to int
            for idx in all_indices
            if not self.tokenizer.convert_ids_to_tokens(idx.item()).startswith("##") and
            self.tokenizer.decode([idx.item()]).strip() != focus_word
        ]

        return predicted_tokens[:top_n]

    def get_token_embeddings(self, tokens):
        """
        Compute embeddings for a given list of tokens using the last hidden layer.
        :param tokens: List of tokens to embed
        :return: Embeddings for the tokens
        """
        inputs = self.tokenizer(tokens, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Extract the last hidden layer
        hidden_states = outputs.hidden_states[-2]  # Use hidden_states[-2] for improved contextual embeddings
        embeddings = hidden_states.mean(dim=1).detach().numpy()

        return embeddings

    def extract_embeddings(self, sentences, focus_word, top_n_neighbors=5):
        """
        Extract embeddings for the given sentences and identify neighbors for each context.
        :param sentences: List of sentences for context comparison
        :param focus_word: The target word to highlight
        :param top_n_neighbors: Number of neighbors to generate for each context
        :return: A dictionary containing:
                - focus_embeddings: Embeddings of the focus word in each context
                - neighbor_embeddings: Embeddings of neighbors for each context
                - neighbors: List of neighbor tokens for each context
        """
        # Add augmented sentence
        augmented_sentences = sentences + [focus_word]
        results = {
            "focus_embeddings": [],
            "neighbor_embeddings": [],
            "neighbors": []
        }

        for sentence in augmented_sentences:
            # Tokenize and pass through the model
            inputs = self.tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                outputs = self.model(**inputs)

            # Extract tokens and hidden states
            tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
            hidden_states = outputs.hidden_states[-2]

            # Find the focus word's embedding
            if focus_word in tokens:
                focus_idx = tokens.index(focus_word)
                focus_embedding = hidden_states[0][focus_idx].numpy()
            else:
                raise ValueError(f"Focus word '{focus_word}' not found in sentence: {sentence}")

            # Handle regular sentences (not augmented)
            if sentence != focus_word:
                masked_sentence = sentence.replace(focus_word, "[MASK]")
                neighbors = self.get_masked_predictions(masked_sentence, focus_word, top_n=top_n_neighbors)
                neighbor_embeddings = [
                    self.get_token_embeddings([neighbor])[0] for neighbor in neighbors
                ]
                results["neighbor_embeddings"].append(neighbor_embeddings)
                results["neighbors"].append(neighbors)

            # Append focus word embedding (all sentences)
            results["focus_embeddings"].append(focus_embedding)

        # Exclude augmented sentence embedding

        return results
