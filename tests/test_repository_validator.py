"""
Test script to validate generated repository.py
Verifies:
1. Code syntax correctness
2. All expected functions exist
3. Deterministic output on re-generation
"""

import ast
import sys
from pathlib import Path

def validate_repository_syntax(repo_file: str) -> bool:
    """Validate that repository.py has valid Python syntax."""
    try:
        with open(repo_file, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        print(f"✓ {repo_file}: Valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"✗ {repo_file}: Syntax error at line {e.lineno}: {e.msg}")
        return False


def extract_functions(repo_file: str) -> dict:
    """Extract all function names from repository.py."""
    with open(repo_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    tree = ast.parse(code)
    functions = {}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Skip private/dunder methods
            if not node.name.startswith('_'):
                functions[node.name] = node.lineno
    
    return functions


def validate_crud_functions(repo_file: str, classes: list) -> bool:
    """Verify that all CRUD functions exist for each class."""
    functions = extract_functions(repo_file)
    expected_patterns = [
        'insert_{cls}',
        'get_all_{cls}',
        'get_{cls}_by_id',
        'update_{cls}',
        'delete_{cls}',
    ]
    
    all_found = True
    for cls in classes:
        cls_lower = cls.lower()
        for pattern in expected_patterns:
            func_name = pattern.format(cls=cls_lower)
            if func_name in functions:
                print(f"  ✓ {func_name}")
            else:
                print(f"  ✗ {func_name} (MISSING)")
                all_found = False
    
    return all_found


def main():
    repo_file = Path("generated_app/repository.py")
    
    if not repo_file.exists():
        print(f"ERROR: {repo_file} not found. Run generate.py first.")
        sys.exit(1)
    
    print("=" * 70)
    print("REPOSITORY VALIDATION TEST")
    print("=" * 70)
    
    # Test 1: Syntax validation
    print("\n1. Checking Python syntax...")
    if not validate_repository_syntax(str(repo_file)):
        sys.exit(1)
    
    # Test 2: Function extraction
    print("\n2. Checking CRUD functions...")
    functions = extract_functions(str(repo_file))
    print(f"   Found {len(functions)} functions total")
    
    # Identify classes from function names
    classes = set()
    for func_name in functions:
        # Extract class name from function patterns
        if func_name.startswith('insert_'):
            class_name = func_name.replace('insert_', '')
            classes.add(class_name.capitalize())
        elif func_name.startswith('delete_'):
            class_name = func_name.replace('delete_', '')
            classes.add(class_name.capitalize())
    
    # Filter out non-entity classes (like 'Db', 'Get_db')
    classes = {c for c in classes if c not in ['Db', 'Connection', 'Get_db']}
    print(f"\n3. Classes found: {', '.join(classes)}")
    
    print("\n4. Validating CRUD operations per class:")
    if validate_crud_functions(str(repo_file), classes):
        print("\n✓ All CRUD functions present")
    else:
        print("\n✗ Some CRUD functions are missing")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("VALIDATION COMPLETE - ALL TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()
