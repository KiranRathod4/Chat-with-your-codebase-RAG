"""
Exercise 1: Understanding Embeddings
Goal: See how similar text creates similar vectors
"""

from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model (downloads ~80MB first time)
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print(f"Model loaded! Creates {model.get_sentence_embedding_dimension()}-dimensional vectors\n")

# Sample texts
texts = [
    "def authenticate_user(token): pass",
    "def login_with_credentials(username, password): pass",
    "def calculate_shipping_cost(weight, distance): pass",
    "def verify_jwt_token(token): pass",
    "def send_email_notification(recipient, message): pass"
]

# Create embeddings
print("Creating embeddings...")
embeddings = model.encode(texts)

print(f"Created {len(embeddings)} embeddings")
print(f"Each embedding has {len(embeddings[0])} dimensions")
print(f"\nFirst embedding (truncated): {embeddings[0][:10]}...\n")

# Calculate similarities
def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

# Compare embeddings
print("=" * 70)
print("SIMILARITY ANALYSIS")
print("=" * 70)

query = "def authenticate_user(token): pass"
query_embedding = embeddings[0]

for i, text in enumerate(texts):
    similarity = cosine_similarity(query_embedding, embeddings[i])
    print(f"\nSimilarity: {similarity:.4f}")
    print(f"Text: {text}")
    
print("\n" + "=" * 70)
print("OBSERVATIONS:")
print("=" * 70)
print("- Authentication functions have HIGH similarity (>0.7)")
print("- Unrelated functions have LOW similarity (<0.5)")
print("- This is how semantic search works!")