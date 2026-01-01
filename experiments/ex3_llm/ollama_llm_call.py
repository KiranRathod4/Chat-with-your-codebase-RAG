"""
Exercise 4: LLM API Basics with Ollama (100% FREE)
Goal: Make your first LLM calls using local models
"""

import ollama
import time

MODEL = "llama3.2"  # or "codellama" or "mistral"

print("=" * 70)
print("OLLAMA LLM SETUP")
print("=" * 70)

# Verify connection
try:
    models = ollama.list()
    print(f"✓ Connected to Ollama")
    print(f"  Using model: {MODEL}")
    
    # Check if model exists
    model_names = [m['name'] for m in models['models']]
    if not any(MODEL in name for name in model_names):
        print(f"\n⚠️  Model '{MODEL}' not found!")
        print(f"  Available models: {model_names}")
        print(f"\n  Download it with: ollama pull {MODEL}")
        exit(1)
    print()
except Exception as e:
    print(f"❌ Cannot connect to Ollama: {e}")
    print("\nMake sure Ollama is running:")
    print("  ollama serve")
    exit(1)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def call_llm_simple(prompt: str) -> str:
    """Make a simple LLM call"""
    print(f"📤 Sending prompt...")
    print(f"   Length: {len(prompt)} characters")
    
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return f"❌ Error: {e}"


def call_llm_with_system(system_prompt: str, user_prompt: str) -> str:
    """Make an LLM call with system prompt"""
    print(f"📤 Sending prompts...")
    print(f"   System: {len(system_prompt)} chars")
    print(f"   User: {len(user_prompt)} chars")
    
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"❌ Error: {e}"


def call_llm_streaming(prompt: str):
    """Stream response token by token"""
    print(f"📤 Streaming response...")
    print(f"🤖 Assistant: ", end="", flush=True)
    
    try:
        stream = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        
        full_response = ""
        for chunk in stream:
            content = chunk['message']['content']
            print(content, end="", flush=True)
            full_response += content
        
        print()  # New line after streaming
        return full_response
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


# ============================================================================
# EXAMPLE 1: Simple Prompt
# ============================================================================
print("=" * 70)
print("EXAMPLE 1: Simple Prompt (No Context)")
print("=" * 70)
print("\nUse case: Just asking the LLM to explain code\n")

simple_prompt = """Explain what this Python function does in 2-3 sentences:

def authenticate_user(token):
    return jwt.decode(token, SECRET_KEY)"""

start_time = time.time()
response = call_llm_simple(simple_prompt)
elapsed = time.time() - start_time

print(f"\n📥 Response:\n{'-'*70}")
print(response)
print("-"*70)
print(f"⏱️  Time taken: {elapsed:.2f} seconds\n")

input("⏸️  Press Enter to continue to Example 2...")


# ============================================================================
# EXAMPLE 2: RAG-Style Prompt with Context
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 2: RAG-Style Prompt (With Code Context)")
print("=" * 70)
print("\nUse case: Providing retrieved code as context for the LLM\n")

system_prompt = """You are a helpful code assistant. Answer questions based ONLY on the provided code context. 
Always cite which file and line numbers you're referring to.
Keep your answer concise and accurate."""

code_context = """
File: auth.py, Lines: 45-52
```python
def authenticate_user(token: str) -> bool:
    \"\"\"Validates JWT token and returns authentication status\"\"\"
    try:
        payload = jwt.decode(token, SECRET_KEY)
        return payload is not None
    except jwt.InvalidTokenError:
        return False
```

File: middleware.py, Lines: 12-18
```python
def verify_token(token: str) -> dict:
    \"\"\"Decodes JWT and returns payload for middleware\"\"\"
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid token")
```

File: auth.py, Lines: 67-73
```python
def login(username: str, password: str) -> Optional[str]:
    \"\"\"Authenticates user and returns JWT token\"\"\"
    user = db.query(User).filter_by(username=username).first()
    if user and user.check_password(password):
        return generate_token(user.id)
    return None
```
"""

user_question = "Where is user authentication handled in the codebase? List all relevant functions."

full_prompt = f"{code_context}\n\nQuestion: {user_question}"

start_time = time.time()
response = call_llm_with_system(system_prompt, full_prompt)
elapsed = time.time() - start_time

print(f"\n📥 Response:\n{'-'*70}")
print(response)
print("-"*70)
print(f"⏱️  Time taken: {elapsed:.2f} seconds\n")

input("⏸️  Press Enter to continue to Example 3...")


# ============================================================================
# EXAMPLE 3: Streaming Response
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 3: Streaming Response")
print("=" * 70)
print("\nUse case: Show response as it's generated (better UX)\n")

streaming_prompt = """Explain these 3 concepts briefly:
1. Vector embeddings
2. Cosine similarity
3. Semantic search

Keep each explanation to 2 sentences."""

start_time = time.time()
response = call_llm_streaming(streaming_prompt)
elapsed = time.time() - start_time

print(f"\n⏱️  Time taken: {elapsed:.2f} seconds\n")

input("⏸️  Press Enter to continue to Example 4...")


# ============================================================================
# EXAMPLE 4: Multi-turn Conversation
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 4: Multi-turn Conversation")
print("=" * 70)
print("\nUse case: Asking follow-up questions\n")

conversation = []

# First question
question1 = """What does this function do?

def calculate_total(items):
    return sum(item.price for item in items)"""

print(f"👤 User: {question1}\n")

response1 = ollama.chat(
    model=MODEL,
    messages=[{"role": "user", "content": question1}]
)
answer1 = response1['message']['content']

conversation = [
    {"role": "user", "content": question1},
    {"role": "assistant", "content": answer1}
]

print(f"🤖 Assistant: {answer1}\n")

# Follow-up question
question2 = "What if some items don't have a price attribute? How would you fix it?"

print(f"👤 User: {question2}\n")

conversation.append({"role": "user", "content": question2})

response2 = ollama.chat(
    model=MODEL,
    messages=conversation
)
answer2 = response2['message']['content']

print(f"🤖 Assistant: {answer2}\n")

input("⏸️  Press Enter to continue to Example 5...")


# ============================================================================
# EXAMPLE 5: Structured Output (JSON)
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 5: Getting Structured Output (JSON)")
print("=" * 70)
print("\nUse case: When you need the LLM to return data in a specific format\n")

system_prompt = """You are a code analyzer. You MUST return your analysis as valid JSON with these exact fields:
{
  "function_name": "string",
  "purpose": "string (one sentence)",
  "parameters": ["array", "of", "strings"],
  "complexity": "simple" or "moderate" or "complex",
  "line_count": number
}

Return ONLY the JSON, no explanations or markdown."""

code_to_analyze = """
def process_user_data(user_id: int, data: dict, validate: bool = True) -> bool:
    \"\"\"Process and validate user data before saving to database\"\"\"
    if validate:
        if not validate_schema(data):
            raise ValueError("Invalid data schema")
    
    user = get_user(user_id)
    if not user:
        return False
    
    try:
        sanitized_data = sanitize_input(data)
        user.update(sanitized_data)
        db.session.commit()
        send_notification(user_id, "Data updated")
        return True
    except Exception as e:
        db.session.rollback()
        log_error(e)
        return False
"""

user_prompt = f"Analyze this function:\n\n{code_to_analyze}"

response = call_llm_with_system(system_prompt, user_prompt)

print(f"\n📥 Response:\n{'-'*70}")
print(response)
print("-"*70)

# Try to parse as JSON
import json
try:
    # Clean up response (remove markdown code blocks if present)
    clean_response = response.strip()
    if "```json" in clean_response:
        clean_response = clean_response.split("```json")[1].split("```")[0].strip()
    elif "```" in clean_response:
        clean_response = clean_response.split("```")[1].split("```")[0].strip()
    
    parsed = json.loads(clean_response)
    print("\n✅ Successfully parsed as JSON:")
    print(json.dumps(parsed, indent=2))
except Exception as e:
    print(f"\n⚠️  Could not parse as JSON: {e}")
    print("(Ollama models sometimes need more explicit prompting for JSON)")

input("\n⏸️  Press Enter to see summary...")


# ============================================================================
# EXAMPLE 6: Temperature Control
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 6: Temperature Control")
print("=" * 70)
print("\nTemperature controls randomness:")
print("- 0.0 = deterministic, focused")
print("- 1.0 = creative, varied\n")

prompt = "Suggest 3 variable names for storing user authentication status."

for temp in [0.0, 0.5, 1.0]:
    print(f"\n🌡️  Temperature: {temp}")
    print("-" * 50)
    
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": temp}
    )
    
    print(response['message']['content'])

print("\n💡 Notice: Lower temperature → more consistent answers")
print("   For RAG systems, use temperature 0.0-0.3 for factual accuracy")


# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 70)
print("✅ EXERCISE 4 COMPLETE!")
print("=" * 70)

print("""
What you learned:
1. ✓ How to make LLM calls with Ollama (100% FREE!)
2. ✓ Using system prompts to control LLM behavior
3. ✓ RAG-style prompts with code context
4. ✓ Streaming responses for better UX
5. ✓ Multi-turn conversations with history
6. ✓ Getting structured output (JSON)
7. ✓ Temperature control for consistency

Key Takeaways:
- Ollama runs completely locally (no API costs!)
- System prompts = instructions for HOW to respond
- Context in RAG = the retrieved code chunks
- Always include citations (file:line) for code answers
- Streaming gives better user experience
- Lower temperature = more consistent/factual responses

Performance Tips:
- Llama3.2 is good for general tasks
- CodeLlama is better for code-specific tasks
- First query is slower (model loading), then faster
- Responses are slower than cloud APIs but 100% free!

Next: You'll combine this with embeddings and FAISS to build a full RAG system!
""")

print("🎉 Ready to continue to Exercise 5: Mini RAG System?")