"""
Exercise 2: FAISS Vector Store
Goal: Store embeddings and search them efficiently
"""

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Sample code snippets (simulating a codebase)
code_snippets = [
    {
        "code": "def authenticate_user(token: str) -> bool:\n    return jwt.decode(token, SECRET_KEY)",
        "file": "auth.py",
        "line": 45,
        "function": "authenticate_user"
    },
    {
        "code": "def login(username: str, password: str) -> Token:\n    user = verify_credentials(username, password)",
        "file": "auth.py",
        "line": 67,
        "function": "login"
    },
    {
        "code": "def calculate_total(items: List[Item]) -> float:\n    return sum(item.price for item in items)",
        "file": "billing.py",
        "line": 23,
        "function": "calculate_total"
    },
    {
        "code": "def verify_token(token: str) -> dict:\n    try:\n        payload = jwt.decode(token)\n        return payload",
        "file": "middleware.py",
        "line": 12,
        "function": "verify_token"
    },
    {
        "code": "def send_notification(user_id: int, message: str):\n    email = get_user_email(user_id)\n    send_email(email, message)",
        "file": "notifications.py",
        "line": 89,
        "function": "send_notification"
    },
    {
        "code": "def process_payment(amount: float, card: Card) -> bool:\n    return payment_gateway.charge(card, amount)",
        "file": "billing.py",
        "line": 45,
        "function": "process_payment"
    },
]

print("=" * 70)
print("BUILDING FAISS VECTOR STORE")
print("=" * 70)

# Step 1: Create embeddings
print("\n1. Creating embeddings for code snippets...")
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode([snippet["code"] for snippet in code_snippets])
print(f"   ✓ Created {len(embeddings)} embeddings")

# Step 2: Create FAISS index
print("\n2. Initializing FAISS index...")
dimension = embeddings.shape[1]  # 384 for this model
index = faiss.IndexFlatL2(dimension)  # L2 (Euclidean) distance
print(f"   ✓ Index created (dimension={dimension})")

# Step 3: Add embeddings to index
print("\n3. Adding embeddings to index...")
index.add(embeddings.astype('float32'))  # FAISS requires float32
print(f"   ✓ Index now contains {index.ntotal} vectors")

# Step 4: Search the index
print("\n" + "=" * 70)
print("SEARCHING THE INDEX")
print("=" * 70)

queries = [
    "Where is user authentication handled?",
    "How do we process payments?",
    "Show me notification logic"
]

for query in queries:
    print(f"\n🔍 Query: '{query}'")
    print("-" * 70)
    
    # Embed the query
    query_embedding = model.encode([query])[0].reshape(1, -1).astype('float32')
    
    # Search for top 3 most similar
    k = 3
    distances, indices = index.search(query_embedding, k)
    
    print(f"\nTop {k} Results:")
    for rank, (distance, idx) in enumerate(zip(distances[0], indices[0]), 1):
        snippet = code_snippets[idx]
        # Convert L2 distance to similarity score (lower distance = higher similarity)
        similarity_score = 1 / (1 + distance)
        
        print(f"\n  [{rank}] Similarity: {similarity_score:.4f}")
        print(f"      File: {snippet['file']}:{snippet['line']}")
        print(f"      Function: {snippet['function']}")
        print(f"      Code: {snippet['code'][:60]}...")

print("\n" + "=" * 70)
print("✅ EXERCISE COMPLETE!")
print("=" * 70)
print("\nKey Takeaways:")
print("- FAISS makes vector search fast (milliseconds even with millions of vectors)")
print("- Lower L2 distance = more similar")
print("- Top-k search returns the k nearest neighbors")
print("- This is the foundation of RAG retrieval!")