# Text2Logic - Quick Start Guide

## What is Text2Logic?

**Text2Logic** converts everyday text into formal logic and automatically derives all possible conclusions using 9 inference rules.

**Example:**
```
Input: "Pedro is a student. If Pedro is a student then he studies."

Output: 
- Fact: (Pedro)IsA(student)
- Rule: (Pedro)IsA(student) -> (Pedro)Studies()
- DERIVED: (Pedro)Studies() ← Modus Ponens
```

---

## How to Install

### 1. Install Ollama (AI Model Runner)

Download from: https://ollama.ai

### 2. Install Gemma Model

```bash
ollama pull gemma:2b
```

### 3. Start Ollama

```bash
ollama serve
```

Keep this terminal open.

---

## How to Use

### Method 1: Simple Library Usage (Recommended)

```python
import Text2Logic as t2l

# Create system
system = t2l.LogicSystem()

# Add a fact
system.add_fact("(Pedro)IsA(student)")

# Add a rule
system.add_rule("(X)IsA(student) -> (X)Studies()")

# Run inference
system.infer_all(verbose=True)

# See results
for conclusion in system.get_conclusions():
    print(conclusion)
```

### Method 2: Process a Text File

```python
from Text2Logic import TextToLogicProcessor

processor = TextToLogicProcessor()
processor.process_file("input.txt", "output.inf", perform_inference=True)
```

### Method 3: Quick Functions

```python
from Text2Logic.api import convert_text, deduce_all

# Convert text to logic
facts, rules = convert_text("Pedro is a student")

# Perform inference
result = deduce_all(facts, rules)

print(f"Derived {len(result.derived_facts)} new facts!")
```

---

## Logic Format

### Facts (Atoms)
```
(Subject)Relation(Object)
```

Examples:
```
(Pedro)IsA(student)
(Bob)WorksAt(Microsoft)
(Ball)HasColor(red)
```

### Rules with Operators
```
Rule: (Premise) -> (Conclusion)
```

Examples:
```
Rule: (X)IsA(student) -> (X)Studies()
Rule: (X)IsA(student) ^ (X)LivesIn(Madrid) -> (X)HasMetro()
```

### Operators
- `->` : Implication (IF...THEN)
- `^` or `∧` : AND
- `v` or `∨` : OR
- `~` or `¬` : NOT
- `<->` or `↔` : IF AND ONLY IF

---

## Demo with TEST.txt

```bash
python Text2Logic/demo_test.py
```

This will:
1. Read TEST.txt
2. Convert to logic format
3. Derive all possible conclusions
4. Save results to TEST_logic_inferred.txt

---

## Inference Rules

The system uses 9 inference rules:

1. **Modus Ponens**: A → B, A ⊢ B
2. **Modus Tollens**: A → B, ¬B ⊢ ¬A
3. **Hypothetical Syllogism**: A → B, B → C ⊢ A → C
4. **Disjunctive Syllogism**: A ∨ B, ¬A ⊢ B
5. **Simplification**: A ∧ B ⊢ A, B
6. **Conjunction**: A, B ⊢ A ∧ B
7. **Resolution**: ¬A ∨ B, A ∨ C ⊢ B ∨ C
8. **Biconditional Elimination**: A ↔ B ⊢ (A → B) ∧ (B → A)
9. **Variable Unification**: Matches patterns with variables

---

## Troubleshooting

### "Cannot connect to Ollama"
**Solution:** Run `ollama serve` in a terminal

### "Model not found"
**Solution:** Run `ollama pull gemma:2b`

### No facts derived
**Solution:** Check that your logic format is correct:
- Must use parentheses: `(Subject)Relation(Object)`
- No spaces in Subject, Relation, or Object
- Use CamelCase for relations

---

## Complete Example

```python
import Text2Logic as t2l

# Create system
system = t2l.LogicSystem()

# Add facts
system.add_fact("(Socrates)IsA(man)")
system.add_fact("(Plato)IsA(man)")

# Add universal rule
system.add_rule("(X)IsA(man) -> (X)IsMortal()")

# Infer
system.infer_all(verbose=True)

# Results
print("\nDerived conclusions:")
for c in system.get_conclusions():
    print(f"  • {c}")

# Statistics
stats = system.get_statistics()
print(f"\nTotal facts: {stats['total_facts']}")
print(f"Derived: {stats['derived_facts']}")
```

**Output:**
```
Derived conclusions:
  • (Socrates)IsMortal()
  • (Plato)IsMortal()

Total facts: 4
Derived: 2
```

---

## File Structure

```
Text2Logic/
├── QUICK_START.md      ← You are here
├── README.md           ← Full documentation (80+ pages)
├── __init__.py         ← Module initialization
├── text_to_logic.py    ← Text → Logic converter
├── logic_engine.py     ← Inference engine
├── logic_parser.py     ← Logic parser
├── deduction_rules.py  ← Inference rules
├── api.py              ← API (3 usage modes)
├── demo_test.py        ← Demo script
└── test_basic.py       ← Test suite
```

---

## Next Steps

1. ✅ Run test: `python Text2Logic/test_basic.py`
2. ✅ Try demo: `python Text2Logic/demo_test.py`
3. 📖 Read full docs: `Text2Logic/README.md`
4. 🚀 Build your own logic system!

---

**Need More Help?**
- Full Documentation: See `README.md` (80+ pages)
- Installation Guide: See `INSTALLATION.md`
- Project Summary: See `PROJECT_SUMMARY.md`

---

**Quick Reference Card**

| Task | Command |
|------|---------|
| Install Ollama | Visit https://ollama.ai |
| Install Gemma | `ollama pull gemma:2b` |
| Start Ollama | `ollama serve` |
| Run tests | `python Text2Logic/test_basic.py` |
| Run demo | `python Text2Logic/demo_test.py` |
| Import library | `import Text2Logic as t2l` |

---

**Status:** ✅ Ready to Use  
**Version:** 1.0  
**Date:** October 2025  
**Author:** Marco

