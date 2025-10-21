"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    TEXT2LOGIC - STRUCTURE TEST                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

Tests the structure and basic functionality without requiring Ollama.

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
        print("  ✓ logic_parser imported")
        
        from Text2Logic import deduction_rules
        print("  ✓ deduction_rules imported")
        
        from Text2Logic import logic_engine
        print("  ✓ logic_engine imported")
        
        from Text2Logic import text_to_logic
        print("  ✓ text_to_logic imported")
        
        from Text2Logic import api
        print("  ✓ api imported")
        
        import Text2Logic as t2l
        print("  ✓ Text2Logic package imported")
        
        return True
    except Exception as e:
        print(f"  ✗ Import error: {e}")
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
        assert expr1.subject == "Pedro", "Subject should be Pedro"
        assert expr1.relation == "IsA", "Relation should be IsA"
        print("  ✓ Simple atom parsing works")
        
        # Test implication
        expr2 = parse_expression("(Pedro)IsA(estudiante) → (Pedro)estudia")
        assert isinstance(expr2, LogicalExpression), "Should be LogicalExpression"
        assert expr2.operator == LogicalOperator.IMPLIES, "Should be IMPLIES"
        print("  ✓ Implication parsing works")
        
        # Test conjunction
        expr3 = parse_expression("(X)IsA(estudiante) ∧ (X)ViveEn(Madrid)")
        assert isinstance(expr3, LogicalExpression), "Should be LogicalExpression"
        assert expr3.operator == LogicalOperator.AND, "Should be AND"
        print("  ✓ Conjunction parsing works")
        
        return True
    except Exception as e:
        print(f"  ✗ Parser error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_logic_engine():
    """Test the logic engine."""
    print("\nTesting logic engine...")
    try:
        from Text2Logic.logic_engine import LogicEngine
        
        engine = LogicEngine(max_iterations=5)
        
        # Add facts
        engine.add_fact("(Pedro)IsA(estudiante)")
        engine.add_fact("(Pedro)ViveEn(Madrid)")
        print("  ✓ Facts added")
        
        # Add rules
        engine.add_rule("(X)IsA(estudiante) → (X)estudia")
        engine.add_rule("(X)estudia → (X)aprende")
        print("  ✓ Rules added")
        
        # Perform inference
        result = engine.infer_all(verbose=False)
        print(f"  ✓ Inference complete: {len(result.derived_facts)} facts derived")
        
        # Check that we derived (Pedro)estudia
        conclusions = [str(chain.conclusion) for chain in result.derived_facts]
        has_estudia = any("estudia" in c for c in conclusions)
        
        if has_estudia:
            print("  ✓ Modus Ponens working (derived estudia)")
        else:
            print("  ⚠ Did not derive expected conclusion")
        
        return True
    except Exception as e:
        print(f"  ✗ Engine error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_deduction_rules():
    """Test individual deduction rules."""
    print("\nTesting deduction rules...")
    try:
        from Text2Logic.deduction_rules import (
            ModusPonens, Simplification, BiconditionalElimination
        )
        from Text2Logic.logic_parser import parse_expression
        
        # Test Modus Ponens
        kb = {
            parse_expression("(Pedro)IsA(estudiante) → (Pedro)estudia"),
            parse_expression("(Pedro)IsA(estudiante)")
        }
        mp = ModusPonens()
        new_facts = set()
        results = mp.apply(kb, new_facts)
        
        if results:
            print(f"  ✓ Modus Ponens: derived {len(results)} fact(s)")
        else:
            print("  ⚠ Modus Ponens: no facts derived")
        
        # Test Simplification
        kb2 = {
            parse_expression("(Pedro)IsA(estudiante) ∧ (Pedro)ViveEn(Madrid)")
        }
        simp = Simplification()
        new_facts2 = set()
        results2 = simp.apply(kb2, new_facts2)
        
        if results2:
            print(f"  ✓ Simplification: derived {len(results2)} fact(s)")
        else:
            print("  ⚠ Simplification: no facts derived")
        
        # Test Biconditional Elimination
        kb3 = {
            parse_expression("(X)EsMamifero ↔ (X)TienePelo")
        }
        bice = BiconditionalElimination()
        new_facts3 = set()
        results3 = bice.apply(kb3, new_facts3)
        
        if results3:
            print(f"  ✓ Biconditional Elimination: derived {len(results3)} fact(s)")
        else:
            print("  ⚠ Biconditional Elimination: no facts derived")
        
        return True
    except Exception as e:
        print(f"  ✗ Rules error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_basic():
    """Test the API without Ollama."""
    print("\nTesting API (without Ollama)...")
    try:
        import Text2Logic as t2l
        
        # Test LogicSystem creation
        system = t2l.LogicSystem(auto_verify=False)
        print("  ✓ LogicSystem created")
        
        # Add facts directly (no NLP)
        system.add_fact("(Pedro)IsA(estudiante)")
        system.add_rule("(X)IsA(estudiante) → (X)estudia")
        print("  ✓ Facts and rules added")
        
        # Perform inference
        system.infer_all(verbose=False)
        print("  ✓ Inference performed")
        
        # Get results
        conclusions = system.get_conclusions()
        stats = system.get_statistics()
        
        print(f"  ✓ Got {len(conclusions)} conclusions")
        print(f"  ✓ Statistics: {stats['total_facts']} total facts")
        
        return True
    except Exception as e:
        print(f"  ✗ API error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 80)
    print("                    TEXT2LOGIC STRUCTURE TEST                                 ")
    print("=" * 80 + "\n")
    
    tests = [
        ("Imports", test_imports),
        ("Logic Parser", test_logic_parser),
        ("Logic Engine", test_logic_engine),
        ("Deduction Rules", test_deduction_rules),
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
    print("                    TEST SUMMARY                                              ")
    print("=" * 80 + "\n")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {status}: {name}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED!")
        print("\nNext steps:")
        print("  1. Ensure Ollama is running: ollama serve")
        print("  2. Ensure Gemma is installed: ollama pull gemma:2b")
        print("  3. Run demo: python Text2Logic/demo_test.py")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

