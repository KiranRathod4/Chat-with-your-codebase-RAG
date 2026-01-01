"""
Fixed Ollama Test - Better error handling
"""

import ollama
import sys

print("=" * 70)
print("OLLAMA CONNECTION TEST")
print("=" * 70)

# Test 1: Check if ollama package is installed
print("\n1. Checking ollama package...")
try:
    import ollama
    print("   ✓ ollama package installed")
except ImportError:
    print("   ❌ ollama package not found")
    print("   Install with: pip install ollama")
    sys.exit(1)

# Test 2: Try to list models
print("\n2. Checking available models...")
try:
    response = ollama.list()
    print(f"   ✓ Connected to Ollama server")
    print(f"   Response type: {type(response)}")
    print(f"   Response keys: {response.keys() if isinstance(response, dict) else 'Not a dict'}")
    
    # Handle different response formats
    if isinstance(response, dict) and 'models' in response:
        models = response['models']
        print(f"   Found {len(models)} models:")
        for model in models:
            if isinstance(model, dict):
                model_name = model.get('name', model.get('model', 'unknown'))
                print(f"     - {model_name}")
            else:
                print(f"     - {model}")
    else:
        print(f"   Unexpected response format: {response}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    print("\n   Troubleshooting steps:")
    print("   1. Check if Ollama is installed:")
    print("      ollama --version")
    print("   2. Start Ollama server:")
    print("      Windows: Ollama should start automatically")
    print("      Mac/Linux: ollama serve")
    print("   3. Download a model:")
    print("      ollama pull llama3.2")
    sys.exit(1)

# Test 3: Try a simple chat
print("\n3. Testing simple chat...")
try:
    response = ollama.chat(
        model='llama3.2',
        messages=[
            {'role': 'user', 'content': 'Reply with just: Hello!'}
        ]
    )
    
    print(f"   ✓ Chat successful!")
    print(f"   Response type: {type(response)}")
    print(f"   Response keys: {response.keys() if isinstance(response, dict) else 'Not a dict'}")
    
    if isinstance(response, dict) and 'message' in response:
        message = response['message']
        if isinstance(message, dict) and 'content' in message:
            print(f"   Content: {message['content']}")
        else:
            print(f"   Message format: {message}")
    else:
        print(f"   Full response: {response}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    print(f"\n   Make sure you have the model:")
    print(f"      ollama pull llama3.2")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70)
print("\nOllama is working correctly. You can proceed with the exercises.")