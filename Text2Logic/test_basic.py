"""
TEXT2LOGIC - Basic Structure Test (Windows-compatible)
Tests the structure without Unicode characters.

Author: Marco
Date: October 2025
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from Text2Logic import logic_parser
        print("  [OK] logic_parser imported")
        
        from Text2Logic import deduction_rules
        print("  [OK] deduction_rules imported")
        
        from Text2Logic import logic_engine
        print("  [OK] logic_engine imported")
        
        from Text2Logic import text_to_logic
        print("  [OK] text_to_logic imported")
        
        from Text2Logic import api
        print("  [OK] api imported")
        
        import Text2Logic as t2l
        print("  [OK] Text2Logic package imported")
        
        return True
    except Exception as e:
        print(f"  [ERROR] Import error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_logic_parser():
    """Test the logic parser."""
    print("\nTesting logic parser...")
    try:
        from Text2Logic.logic_parser import parse_expression, Atom, LogicalExpression, LogicalOperator
        
        # Test simple atom
        expr1 = parse_expression("(Pedro)IsA(estudiante)")
        assert isinstance(expr1, Atom), "Should be Atom"
        print("  [OK] Simple atom parsing works")
        
        # Test implication
        expr2 = parse_expression("(Pedro)IsA(estudiante) -> (Pedro)estudia()")
        assert isinstance(expr2, LogicalExpression), "Should be LogicalExpression"
        print("  [OK] Implication parsing works")
        
        return True
    except Exception as e:
        print(f"  [ERROR] Parser error: {e}")
        return False


def test_logic_engine():
    """Test the logic engine."""
    print("\nTesting logic engine...")
    try:
        from Text2Logic.logic_engine import LogicEngine
        
        engine = LogicEngine(max_iterations=5)
        
        # Add facts
        engine.add_fact("(Pedro)IsA(estudiante)")
        print("  [OK] Facts added")
        
        # Add rules
        engine.add_rule("(X)IsA(estudiante) -> (X)estudia()")
        print("  [OK] Rules added")
        
        # Perform inference
        result = engine.infer_all(verbose=False)
        print(f"  [OK] Inference complete: {len(result.derived_facts)} facts derived")
        
        return True
    except Exception as e:
        print(f"  [ERROR] Engine error: {e}")
        return False


def test_api_basic():
    """Test the API without Ollama."""
    print("\nTesting API (without Ollama)...")
    try:
        import Text2Logic as t2l
        
        # Test LogicSystem creation
        system = t2l.LogicSystem(auto_verify=False)
        print("  [OK] LogicSystem created")
        
        # Add facts directly (no NLP)
        system.add_fact("(Pedro)IsA(estudiante)")
        system.add_rule("(X)IsA(estudiante) -> (X)estudia()")
        print("  [OK] Facts and rules added")
        
        # Perform inference
        system.infer_all(verbose=False)
        print("  [OK] Inference performed")
        
        # Get results
        conclusions = system.get_conclusions()
        stats = system.get_statistics()
        
        print(f"  [OK] Got {len(conclusions)} conclusions")
        print(f"  [OK] Statistics: {stats['total_facts']} total facts")
        
        return True
    except Exception as e:
        print(f"  [ERROR] API error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 80)
    print("TEXT2LOGIC STRUCTURE TEST")
    print("=" * 80 + "\n")
    
    tests = [
        ("Imports", test_imports),
        ("Logic Parser", test_logic_parser),
        ("Logic Engine", test_logic_engine),
        ("API Basic", test_api_basic),
    ]
    
    results = []
    
    for name, test_func in tests:
        print("\n" + "=" * 70)
        print(f"TEST: {name}")
        print("=" * 70)
        result = test_func()
        results.append((name, result))
    
    # Summary
    print("\n\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80 + "\n")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "[PASSED]" if result else "[FAILED]"
        print(f"  {status}: {name}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] ALL TESTS PASSED!")
        print("\nThe Text2Logic system is working correctly.")
        print("\nNext steps to use with TEST.txt:")
        print("  1. Ensure Ollama is running: ollama serve")
        print("  2. Ensure Gemma is installed: ollama pull gemma:2b")
        print("  3. Run demo: python Text2Logic/demo_test.py")
        return 0
    else:
        print("\n[WARNING] SOME TESTS FAILED")
        print("Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

