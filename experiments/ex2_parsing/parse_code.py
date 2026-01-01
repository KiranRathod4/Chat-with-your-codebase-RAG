"""
Exercise 3: Parsing Code with Tree-sitter
Goal: Extract functions, classes, and metadata from Python files
"""

from tree_sitter import Language, Parser
import os

# Load the language library
PY_LANGUAGE = Language('build/languages.so', 'python')

# Create parser
parser = Parser()
parser.set_language(PY_LANGUAGE)


def read_file(filepath):
    """Read file and return bytes (tree-sitter needs bytes)"""
    with open(filepath, 'rb') as f:
        return f.read()


def extract_functions(tree, source_code):
    """
    Extract all function definitions from the AST
    
    Returns list of dicts with function metadata
    """
    functions = []
    
    def traverse(node):
        """Recursively traverse the tree"""
        if node.type == 'function_definition':
            # Extract function name
            name_node = node.child_by_field_name('name')
            func_name = source_code[name_node.start_byte:name_node.end_byte].decode('utf8')
            
            # Extract parameters
            params_node = node.child_by_field_name('parameters')
            params = source_code[params_node.start_byte:params_node.end_byte].decode('utf8')
            
            # Extract docstring if exists
            body = node.child_by_field_name('body')
            docstring = None
            if body and body.child_count > 0:
                first_stmt = body.children[0]
                if first_stmt.type == 'expression_statement':
                    expr = first_stmt.children[0]
                    if expr.type == 'string':
                        docstring = source_code[expr.start_byte:expr.end_byte].decode('utf8')
                        docstring = docstring.strip('"""').strip("'''").strip()
            
            # Extract full function code
            full_code = source_code[node.start_byte:node.end_byte].decode('utf8')
            
            functions.append({
                'name': func_name,
                'parameters': params,
                'docstring': docstring,
                'start_line': node.start_point[0] + 1,
                'end_line': node.end_point[0] + 1,
                'code': full_code
            })
        
        # Recursively process children
        for child in node.children:
            traverse(child)
    
    # Start traversal from root
    traverse(tree.root_node)
    return functions


def extract_classes(tree, source_code):
    """Extract all class definitions from the AST"""
    classes = []
    
    def traverse(node):
        if node.type == 'class_definition':
            # Extract class name
            name_node = node.child_by_field_name('name')
            class_name = source_code[name_node.start_byte:name_node.end_byte].decode('utf8')
            
            # Extract docstring
            body = node.child_by_field_name('body')
            docstring = None
            if body and body.child_count > 0:
                first_stmt = body.children[0]
                if first_stmt.type == 'expression_statement':
                    expr = first_stmt.children[0]
                    if expr.type == 'string':
                        docstring = source_code[expr.start_byte:expr.end_byte].decode('utf8')
                        docstring = docstring.strip('"""').strip("'''").strip()
            
            # Extract methods (functions inside the class)
            methods = []
            for child in node.children:
                if child.type == 'block':
                    for stmt in child.children:
                        if stmt.type == 'function_definition':
                            method_name_node = stmt.child_by_field_name('name')
                            method_name = source_code[method_name_node.start_byte:method_name_node.end_byte].decode('utf8')
                            methods.append(method_name)
            
            classes.append({
                'name': class_name,
                'docstring': docstring,
                'methods': methods,
                'start_line': node.start_point[0] + 1,
                'end_line': node.end_point[0] + 1
            })
        
        for child in node.children:
            traverse(child)
    
    traverse(tree.root_node)
    return classes


# Main execution
if __name__ == "__main__":
    print("=" * 70)
    print("PARSING PYTHON CODE WITH TREE-SITTER")
    print("=" * 70)
    
    # Read the sample file
    filepath = 'sample_code.py'
    source_code = read_file(filepath)
    
    # Parse the code
    tree = parser.parse(source_code)
    
    print(f"\n📄 File: {filepath}")
    print(f"✓ Successfully parsed {len(source_code)} bytes\n")
    
    # Extract functions
    print("=" * 70)
    print("FUNCTIONS FOUND")
    print("=" * 70)
    functions = extract_functions(tree, source_code)
    
    for func in functions:
        print(f"\n🔹 {func['name']}{func['parameters']}")
        print(f"   Lines: {func['start_line']}-{func['end_line']}")
        if func['docstring']:
            # Show first line of docstring
            first_line = func['docstring'].split('\n')[0]
            print(f"   Doc: {first_line}")
        print(f"   Code preview: {func['code'][:80]}...")
    
    # Extract classes
    print("\n" + "=" * 70)
    print("CLASSES FOUND")
    print("=" * 70)
    classes = extract_classes(tree, source_code)
    
    for cls in classes:
        print(f"\n🔸 class {cls['name']}")
        print(f"   Lines: {cls['start_line']}-{cls['end_line']}")
        if cls['docstring']:
            print(f"   Doc: {cls['docstring']}")
        print(f"   Methods: {', '.join(cls['methods'])}")
    
    # Summary statistics
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total functions: {len(functions)}")
    print(f"Total classes: {len(classes)}")
    print(f"Functions with docstrings: {sum(1 for f in functions if f['docstring'])}")
    print("\n✅ Parsing complete!")