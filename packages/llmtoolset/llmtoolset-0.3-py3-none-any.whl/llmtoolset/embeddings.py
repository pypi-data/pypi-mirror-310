import torch
from sentence_transformers import SentenceTransformer as _sentencetransformer
from transformers.utils.logging import set_verbosity_warning, set_verbosity_info
import numpy as np


class SentenceEncoder:
    """
    A class for encoding sentences into vector representations using a SentenceTransformer model.

    :param cache_folder: Optional path to store the SentenceTransformer model locally. Defaults to None.
    """

    def __init__(self, cache_folder: str = None, print_loading_progress: bool = True) -> None:
        """
        Initializes the SentenceEncoder with the specified model and sets the device to CUDA if available.

        :param cache_folder: Optional path to store the SentenceTransformer model locally. Defaults to None.
        """
        # Set device to CUDA if available, otherwise fallback to CPU
        if print_loading_progress:
            set_verbosity_info()
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.encoder = _sentencetransformer(
            'all-MiniLM-L6-v2', device=device, cache_folder=cache_folder, backend="torch")
        if print_loading_progress:
            set_verbosity_warning()

    def encode(self, texts: str | list[str]):
        """
        Encodes a single string or a list of strings into their vector representations.

        :param texts: A single string or a list of strings to encode.
        :returns: A NumPy array containing the encoded vectors.
        """
        return self.encoder.encode(texts, convert_to_numpy=True)


def save_embeddings(file_path: str, embeddings: np.ndarray):
    """
    Saves embeddings to a file in NumPy's .npy format.

    :param file_path: Path to the file where embeddings will be saved.
    :param embeddings: The NumPy array containing embeddings to save.
    """
    np.save(file_path, embeddings)


def load_embeddings(file_path: str) -> np.ndarray:
    """
    Loads embeddings from a file in NumPy's .npy format.

    :param file_path: Path to the file from which embeddings will be loaded.
    :returns: The NumPy array containing the loaded embeddings.
    """
    return np.load(file_path)


def cosine_similarity(vec1, vec2):
    """
    Computes the cosine similarity between two vectors or batches of vectors.

    :param vec1: A single vector (1D array) or a batch of vectors (2D array).
    :param vec2: A single vector (1D array) or a batch of vectors (2D array).
    :returns: A float if vec1 and vec2 are single vectors (1D).
              A 1D NumPy array if vec1 or vec2 contains multiple vectors (2D).
    """
    # Ensure inputs are NumPy arrays
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    # Handle single vectors as 1D arrays
    if vec1.ndim == 1:
        vec1 = vec1[np.newaxis, :]  # Convert to 2D array
    if vec2.ndim == 1:
        vec2 = vec2[np.newaxis, :]  # Convert to 2D array

    # Compute dot product and norms
    dot_product = np.dot(vec1, vec2.T)
    magnitude_vec1 = np.linalg.norm(vec1, axis=1, keepdims=True)
    magnitude_vec2 = np.linalg.norm(vec2, axis=1, keepdims=True)

    # Prevent division by zero
    magnitude_product = np.dot(magnitude_vec1, magnitude_vec2.T)
    # Small epsilon to avoid division by zero
    magnitude_product[magnitude_product == 0] = 1e-10

    # Compute cosine similarity
    similarity = dot_product / magnitude_product

    # Return scalar if single pair, or array for batches
    if similarity.size == 1:
        return float(similarity[0, 0])
    return similarity


def batch_pairwise_cosine_similarity(vecs1, vecs2):
    """
    Computes pairwise cosine similarity between all vectors in two batches.

    :param vecs1: A 2D NumPy array of vectors.
    :param vecs2: A 2D NumPy array of vectors.
    :returns: A 2D NumPy array where entry (i, j) is the similarity between vecs1[i] and vecs2[j].
    """
    vecs1 = np.array(vecs1)
    vecs2 = np.array(vecs2)

    # Normalize the vectors
    vecs1_norm = vecs1 / np.linalg.norm(vecs1, axis=1, keepdims=True)
    vecs2_norm = vecs2 / np.linalg.norm(vecs2, axis=1, keepdims=True)

    # Compute cosine similarity
    return np.dot(vecs1_norm, vecs2_norm.T)


def find_nearest_neighbors(query_vector, candidate_vectors, top_k=1):
    """
    Finds the nearest neighbors for a given query vector among candidate vectors.

    :param query_vector: A 1D or 2D NumPy array (single vector or batch of vectors).
    :param candidate_vectors: A 2D NumPy array of candidate vectors.
    :param top_k: The number of top neighbors to return.
    :returns: A tuple of (indices, similarities) of the top_k neighbors.
    """
    similarities = batch_pairwise_cosine_similarity(
        query_vector, candidate_vectors)
    top_k_indices = np.argsort(-similarities, axis=1)[:, :top_k]
    top_k_similarities = np.take_along_axis(
        similarities, top_k_indices, axis=1)
    return top_k_indices, top_k_similarities


def group_similar_embeddings(embeddings: list[np.ndarray], similarity_threshold: float = 0.8) -> list[list[tuple[int, np.ndarray]]]:
    """
    Groups similar embeddings based on a cosine similarity threshold.

    :param embeddings: A list of embeddings (NumPy arrays).
    :param similarity_threshold: The minimum cosine similarity to group embeddings together.
    :returns: A list of lists where each inner list contains tuples of the form (index, embedding).
    """
    # Convert embeddings to a 2D NumPy array
    embeddings_array = np.array(embeddings)

    # Compute pairwise cosine similarity
    pairwise_similarities = batch_pairwise_cosine_similarity(
        embeddings_array, embeddings_array)

    # Keep track of grouped embeddings
    visited = set()
    groups = []

    for i in range(len(embeddings)):
        if i in visited:
            continue

        # Start a new group
        group = [(i, embeddings[i])]
        visited.add(i)

        for j in range(i + 1, len(embeddings)):
            if j not in visited and pairwise_similarities[i, j] >= similarity_threshold:
                group.append((j, embeddings[j]))
                visited.add(j)

        groups.append(group)

    return groups
