"""
Quick test to verify Ollama is working
"""

import ollama

print("Testing Ollama connection...")

try:
    # List available models
    models = ollama.list()
    print(f"✓ Connected to Ollama!")
    print(f"  Available models: {[m['name'] for m in models['models']]}\n")
    
    # Test a simple query
    print("Testing simple query...")
    response = ollama.chat(
        model='llama3.2',
        messages=[{
            'role': 'user',
            'content': 'Say "Hello! I am working!" in one sentence.'
        }]
    )
    
    print(f"✓ Response received:")
    print(f"  {response['message']['content']}\n")
    
    print("✅ Ollama is ready to use!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure Ollama is installed: ollama --version")
    print("2. Make sure a model is downloaded: ollama pull llama3.2")
    print("3. Make sure server is running: ollama serve")