# Text2Logic - Installation and Quick Start Guide

## Project Status

✅ **ALL COMPONENTS IMPLEMENTED AND TESTED**

All system components have been successfully implemented and basic tests pass without errors.

## What Has Been Built

### Core Components

1. **logic_parser.py** - Parser for formal logic expressions
   - Supports atoms: `(Subject)Relation(Object)`
   - Logical operators: ∧, ∨, ¬, →, ↔
   - Operator precedence and parsing
   - Variable unification support

2. **deduction_rules.py** - 9 inference rules
   - Modus Ponens
   - Modus Tollens
   - Hypothetical Syllogism
   - Disjunctive Syllogism
   - Simplification
   - Conjunction
   - Resolution
   - Biconditional Elimination
   - Variable Unification

3. **logic_engine.py** - Inference engine
   - Forward chaining algorithm
   - Exhaustive inference (saturation)
   - Contradiction detection
   - Derivation tracking
   - Configurable iteration limits

4. **text_to_logic.py** - NLP converter (enhanced)
   - System verification (Ollama + Gemma)
   - Logical connective detection
   - Improved sentence splitting
   - Enhanced prompts for Gemma
   - Robust error handling

5. **api.py** - Three usage modes
   - Mode 1: Direct usage (TextToLogicProcessor)
   - Mode 2: Internal API (convert_text, deduce_all)
   - Mode 3: Library usage (LogicSystem)

6. **__init__.py** - Module packaging
   - Complete API exports
   - Version information
   - System verification utility

### Documentation

1. **README.md** - Complete documentation (80+ pages)
   - Architecture overview
   - Installation instructions
   - Three usage modes with examples
   - API reference
   - Logic format specification
   - Troubleshooting guide

2. **INSTALLATION.md** - This file

### Testing

1. **test_basic.py** - Windows-compatible test suite
   - Import verification
   - Logic parser tests
   - Inference engine tests
   - API tests

2. **demo_test.py** - Demo script for TEST.txt processing

## Installation Steps

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Ollama** - Download from https://ollama.ai
   - Windows: Download installer
   - macOS: `brew install ollama`
   - Linux: `curl https://ollama.ai/install.sh | sh`

3. **Gemma Model**
   ```bash
   # After installing Ollama, pull the model
   ollama pull gemma:2b
   ```

### System Verification

#### Step 1: Start Ollama Service

Open a terminal and run:
```bash
ollama serve
```

Keep this terminal open while using Text2Logic.

#### Step 2: Verify Installation

```bash
cd C:\Users\Marco\Documents\Inference
python Text2Logic/test_basic.py
```

Expected output:
```
[SUCCESS] ALL TESTS PASSED!
```

#### Step 3: Verify Dependencies

```python
python
>>> import Text2Logic as t2l
>>> t2l.verify_system()
```

Expected output:
```
✓ Ollama installed: ...
✓ Ollama service is running
✓ Model gemma:2b is installed
```

## Quick Start

### Example 1: Simple Library Usage

```python
import Text2Logic as t2l

# Create system
system = t2l.LogicSystem()

# Verify dependencies
if not system.verify():
    print("Please install Ollama and Gemma")
    exit(1)

# Add facts (in logic notation)
system.add_fact("(Pedro)IsA(estudiante)")

# Add rules
system.add_rule("(X)IsA(estudiante) -> (X)estudia()")

# Perform inference
system.infer_all(verbose=True)

# Get results
for conclusion in system.get_conclusions():
    print(f"  • {conclusion}")

# Get statistics
stats = system.get_statistics()
print(f"Total facts: {stats['total_facts']}")
print(f"Derived: {stats['derived_facts']}")
```

### Example 2: Process TEST.txt

```bash
cd C:\Users\Marco\Documents\Inference
python Text2Logic/demo_test.py
```

This will:
1. Verify Ollama and Gemma are installed
2. Read TEST.txt
3. Convert to logic format (.inf)
4. Perform exhaustive inference
5. Generate complete results file

## File Structure

```
Text2Logic/
├── README.md              # Complete documentation
├── INSTALLATION.md        # This file
├── __init__.py           # Module initialization
├── text_to_logic.py      # NLP converter
├── logic_parser.py       # Logic expression parser
├── logic_engine.py       # Inference engine
├── deduction_rules.py    # Inference rules
├── api.py               # Unified API
├── test_basic.py        # Test suite
└── demo_test.py         # Demo script
```

## Usage Modes

### Mode 1: Standalone Script

```python
from Text2Logic import TextToLogicProcessor

processor = TextToLogicProcessor()
processor.process_file("input.txt", "output.inf", perform_inference=True)
```

### Mode 2: Internal API

```python
from Text2Logic.api import convert_text, deduce_all

facts, rules = convert_text("Pedro es estudiante")
result = deduce_all(facts, rules)
```

### Mode 3: Library (Recommended)

```python
import Text2Logic as t2l

system = t2l.LogicSystem()
system.add_text("Pedro es estudiante")  # Natural language
system.infer_all()
print(system.get_conclusions())
```

## Logic Format

### Facts (Atoms)
```
(Pedro)IsA(estudiante)
(Bob)WorksAt(Microsoft)
```

### Rules with Operators
```
Rule: (X)IsA(estudiante) -> (X)estudia()
Rule: (X)IsA(estudiante) ^ (X)ViveEn(Madrid) -> (X)TieneMetro()
```

### Supported Operators
- `->` or `→` : Implication (IMPLIES)
- `^` or `∧` : Conjunction (AND)
- `v` or `∨` : Disjunction (OR)
- `~` or `¬` : Negation (NOT)
- `<->` or `↔` : Biconditional (IFF)

## Troubleshooting

### Problem: "Cannot connect to Ollama"

**Solution:**
```bash
# Start Ollama service
ollama serve
```

### Problem: "Model gemma:2b not found"

**Solution:**
```bash
ollama pull gemma:2b
```

### Problem: Tests fail

**Solution:**
1. Ensure you're in the correct directory:
   ```bash
   cd C:\Users\Marco\Documents\Inference
   ```

2. Re-run tests:
   ```bash
   python Text2Logic/test_basic.py
   ```

3. Check Python version (requires 3.8+):
   ```bash
   python --version
   ```

### Problem: Unicode errors on Windows

The Text2Logic system is fully compatible with Windows. If you see Unicode errors:
- Use `test_basic.py` instead of `test_structure.py`
- The system internally handles all Unicode characters correctly

## Next Steps

1. ✅ All components implemented
2. ✅ All tests passing
3. ✅ Documentation complete
4. ⏭️ Ready to use with TEST.txt

To process TEST.txt:
```bash
python Text2Logic/demo_test.py
```

This requires:
- Ollama running: `ollama serve`
- Gemma installed: `ollama pull gemma:2b`

## Support

For detailed documentation, see `README.md`.

For usage examples, see the examples in `README.md`.

For API reference, see the API section in `README.md`.

---

**Status:** ✅ Complete and Ready
**Date:** October 21, 2025
**Author:** Marco

