"""
Exercise 5: Mini RAG System
Goal: Combine parsing, embeddings, FAISS, and LLM into one pipeline
"""

import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from anthropic import Anthropic

load_dotenv()

# Initialize components
print("🚀 Initializing Mini RAG System...\n")

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
llm_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Simulated "codebase" (in reality, this would come from tree-sitter parsing)
codebase = [
    {
        "code": """def authenticate_user(token: str) -> bool:
    \"\"\"Validates JWT token and returns auth status\"\"\"
    try:
        payload = jwt.decode(token, SECRET_KEY)
        return payload is not None
    except jwt.InvalidTokenError:
        return False""",
        "file": "auth.py",
        "function": "authenticate_user",
        "start_line": 45,
        "end_line": 52
    },
    {
        "code": """def login(username: str, password: str) -> Optional[str]:
    \"\"\"Authenticates user and returns JWT token\"\"\"
    user = db.query(User).filter_by(username=username).first()
    if user and user.check_password(password):
        return generate_token(user.id)
    return None""",
        "file": "auth.py",
        "function": "login",
        "start_line": 67,
        "end_line": 73
    },
    {
        "code": """def verify_token(token: str) -> dict:
    \"\"\"Decodes JWT and returns payload\"\"\"
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])""",
        "file": "middleware.py",
        "function": "verify_token",
        "start_line": 12,
        "end_line": 14
    },
    {
        "code": """def calculate_total(items: List[Item]) -> float:
    \"\"\"Calculates total price from items\"\"\"
    return sum(item.price * item.quantity for itemin items)""",
"file": "billing.py",
"function": "calculate_total",
"start_line": 23,
"end_line": 25
},
{
"code": """def process_payment(user_id: int, amount: float) -> bool:
"""Processes payment via payment gateway"""
card = get_user_card(user_id)
return payment_gateway.charge(card, amount)""",
"file": "billing.py",
"function": "process_payment",
"start_line": 45,
"end_line": 48
},
]
print(f"📚 Loaded {len(codebase)} code chunks")