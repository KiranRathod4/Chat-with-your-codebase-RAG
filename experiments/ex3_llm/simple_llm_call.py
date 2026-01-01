"""
Exercise 4: LLM API Basics
Goal: Make your first API call and understand prompt structure
"""

import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()

# Choose your LLM (uncomment one)
USE_ANTHROPIC = False  #claude 
USE_OPENAI = True   
# USE_ANTHROPIC = False  # OpenAI

if USE_ANTHROPIC:
    from anthropic import Anthropic
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    MODEL = "claude-sonnet-4-20250514"
else:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    MODEL = "gpt-4-turbo-preview"


def call_llm_simple(prompt: str) -> str:
    """Make a simple LLM call"""
    print(f"📤 Sending prompt ({len(prompt)} chars)...")
    
    if USE_ANTHROPIC:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    else:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        )
        return response.choices[0].message.content


def call_llm_with_system(system_prompt: str, user_prompt: str) -> str:
    """Make an LLM call with system prompt (better control)"""
    print(f"📤 Sending prompts...")
    print(f"   System: {len(system_prompt)} chars")
    print(f"   User: {len(user_prompt)} chars")
    
    if USE_ANTHROPIC:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return response.content[0].text
    else:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1024
        )
        return response.choices[0].message.content


# Example 1: Simple prompt
print("=" * 70)
print("EXAMPLE 1: Simple Prompt")
print("=" * 70)

simple_prompt = "Explain what this Python function does:\n\ndef authenticate_user(token):\n    return jwt.decode(token, SECRET_KEY)"

response = call_llm_simple(simple_prompt)
print(f"\n📥 Response:\n{response}\n")

# Example 2: RAG-style prompt with context
print("=" * 70)
print("EXAMPLE 2: RAG-Style Prompt (with context)")
print("=" * 70)

system_prompt = """You are a helpful code assistant. Answer questions based on the provided code context. Always cite which file and line number you're referring to."""

code_context = """
File: auth.py, Lines: 45-52
```python
def authenticate_user(token: str) -> bool:
    \"\"\"Validates JWT token\"\"\"
    try:
        payload = jwt.decode(token, SECRET_KEY)
        return payload is not None
    except:
        return False
```

File: middleware.py, Lines: 12-18
```python
def verify_token(token: str) -> dict:
    \"\"\"Decodes JWT and returns payload\"\"\"
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
```
"""

user_question = "Where is user authentication handled in the codebase?"

full_prompt = f"{code_context}\n\nQuestion: {user_question}"

response = call_llm_with_system(system_prompt, full_prompt)
print(f"\n📥 Response:\n{response}\n")

# Example 3: Token counting
print("=" * 70)
print("EXAMPLE 3: Token Counting")
print("=" * 70)

import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4")
prompt_text = full_prompt

tokens = encoding.encode(prompt_text)
print(f"Prompt length: {len(prompt_text)} characters")
print(f"Token count: {len(tokens)} tokens")
print(f"First 10 tokens: {tokens[:10]}")
print(f"Decoded: {encoding.decode(tokens[:10])}")

print("\n✅ All examples complete!")