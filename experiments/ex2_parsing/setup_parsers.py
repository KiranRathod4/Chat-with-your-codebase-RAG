"""
Setup script for tree-sitter parsers
Run this once to download and build language grammars
"""

from tree_sitter import Language, Parser
import os

# Create directory for language files
os.makedirs('build', exist_ok=True)

print("Building tree-sitter language libraries...")
print("This may take a minute...\n")

try:
    # Build the language libraries
    Language.build_library(
        'build/languages.so',  # Output file (.so on Mac/Linux, .dll on Windows)
        [
            'tree-sitter-python',  # Will be installed by pip
            'tree-sitter-javascript'
        ]
    )
    print("✓ Successfully built language libraries!")
    print("  Created: build/languages.so")
    
except Exception as e:
    print(f"❌ Error building languages: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure you have a C compiler installed")
    print("   - Mac: xcode-select --install")
    print("   - Windows: Install Visual Studio Build Tools")
    print("   - Linux: sudo apt-get install build-essential")
    print("\n2. Try installing manually:")
    print("   git clone https://github.com/tree-sitter/tree-sitter-python")
    print("   git clone https://github.com/tree-sitter/tree-sitter-javascript")