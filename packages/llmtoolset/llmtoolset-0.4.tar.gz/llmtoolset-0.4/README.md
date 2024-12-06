# llmtoolset

[![PyPI version](https://badge.fury.io/py/llmtoolset.svg)](https://badge.fury.io/py/llmtoolset)

`llmtoolset` is a Python library designed to provide tools for working with large language models (LLMs) and embeddings without relying on APIs like OpenAI or Hugging Face tokens. It focuses on flexibility and performance using Ollama and PyTorch for embeddings. This toolkit streamlines common operations such as sentence encoding, similarity computation, clustering, and utility functions for LLM-driven workflows.

## Installation Requirements

Before installing `llmtoolset`, ensure you have the correct version of PyTorch installed. Use the command below for CUDA-enabled systems to maximize performance. Optionally, include `torchvision` and `torchaudio` for broader PyTorch functionality:

```
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

If PyTorch isn't pre-installed, `llmtoolset` will automatically install a default version of PyTorch.

## Features

- **Sentence Encoding**: Encode text into vector representations using SentenceTransformer.
- **Cosine Similarity**: Calculate similarity between vectors or batches for clustering, ranking, and comparison.
- **Embedding Storage**: Save and load embeddings seamlessly in `.npy` format.
- **Nearest Neighbors**: Find similar embeddings with customizable thresholds and top-k results.
- **Clustering**: Group embeddings based on similarity thresholds.
- **Tag Extraction**: Utility functions to extract and process tags or lists from text.
- **Stream Management**: Real-time interaction support for LLM streams.

## Examples

### Encoding Sentences

```python
from llmtoolset.embeddings import SentenceEncoder

encoder = SentenceEncoder()
embeddings = encoder.encode(["This is a test sentence.", "Another sentence to encode."])
print(embeddings)  # Outputs a NumPy array of encoded vectors
```

### Calculating Cosine Similarity

```python
from llmtoolset.embeddings import SentenceEncoder, cosine_similarity

# Initialize the encoder
encoder = SentenceEncoder()

# Define the animals
animals = ["cat", "tiger", "fish"]

# Encode the animal names
embeddings = encoder.encode(animals)

# Calculate cosine similarity between the animals
similarity_cat_tiger = cosine_similarity(embeddings[0], embeddings[1])
similarity_cat_fish = cosine_similarity(embeddings[0], embeddings[2])
similarity_tiger_fish = cosine_similarity(embeddings[1], embeddings[2])

print(f"Cosine Similarity between 'cat' and 'tiger': {similarity_cat_tiger}")
print(f"Cosine Similarity between 'cat' and 'fish': {similarity_cat_fish}")
print(f"Cosine Similarity between 'tiger' and 'fish': {similarity_tiger_fish}")
```

### Generating Tags from Text

```python
from llmtoolset import make_tags

text = "This text discusses machine learning and artificial intelligence."
tags = make_tags(text)
print(tags)  # Example output: ['machine learning', 'artificial intelligence']
```

### Clustering Similar Embeddings

```python
from llmtoolset.embeddings import SentenceEncoder, group_similar_embeddings

# Initialize the encoder
encoder = SentenceEncoder()

# Define the animals
animals = ["cat", "tiger", "lion", "dog", "wolf", "fish", "shark", "whale"]

# Encode the animal names
embeddings = encoder.encode(animals)

# Group similar embeddings
clusters = group_similar_embeddings(embeddings, similarity_threshold=0.5)

# Visually print the clustering
for cluster in clusters:
    print("[Cluster]:")
    for item in cluster:
        print(f"   {animals[item[0]]}")

# Results of this code in testing (tweaking would be needed for perfection)
# [Cluster]:
#    cat
#    tiger
#    lion
#    dog
# [Cluster]:
#    wolf
# [Cluster]:
#    fish
#    shark
#    whale
```

### Stream Interaction

```python
from llmtoolset import activate_stream_printing, deactivate_stream_printing

# Enable real-time stream printing
activate_stream_printing()

# Disable it when no longer needed
deactivate_stream_printing()
```
