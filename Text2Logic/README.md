```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    TEXT2LOGIC - NATURAL LANGUAGE TO LOGIC                    ║
║                         Version 1.0 - October 2025                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## 📋 Overview

**Text2Logic** is a comprehensive system for converting natural language text to formal logic notation and performing exhaustive logical inference. It combines natural language processing with a complete logical inference engine to automatically extract knowledge and derive all possible conclusions.

### Key Features

- ✨ **Natural Language Processing**: Convert Spanish text to formal logic
- 🔍 **Logical Operator Detection**: Recognizes "y", "o", "si...entonces", "si y solo si"
- 🧠 **Exhaustive Inference**: Derives all possible conclusions using 9+ inference rules
- 🔗 **Forward Chaining**: Data-driven inference with saturation
- 📊 **Explainability**: Tracks reasoning chains for every derived fact
- 🚀 **Three Usage Modes**: Direct script, internal API, or library import
- ✅ **Automatic Verification**: Checks Ollama and Gemma installation

---

## 🏗️ Architecture

```
Text2Logic/
├── README.md              # This file
├── __init__.py           # Module initialization
├── text_to_logic.py      # NLP converter (text → logic)
├── logic_parser.py       # Parser for logical expressions
├── logic_engine.py       # Inference engine with deduction
├── deduction_rules.py    # Inference rules implementation
├── api.py               # Unified API (3 modes)
└── demo_test.py         # Demonstration script
```

### Processing Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT: NATURAL LANGUAGE TEXT                 │
│  "Si Pedro es estudiante entonces estudia. Pedro es estudiante" │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
        ╔════════════════════════════════════════╗
        ║  STAGE 1: TEXT → LOGIC CONVERSION     ║
        ║  (text_to_logic.py)                   ║
        ╚════════════════════════════════════════╝
                    │
                    │  • Sentence decomposition
                    │  • Logical connective detection
                    │  • Entity & relation extraction
                    │  • Format to .inf notation
                    │
                    ▼
        ┌─────────────────────────────────────┐
        │   STRUCTURED LOGIC (.inf format)    │
        │                                     │
        │   (Pedro)IsA(estudiante)            │
        │   Rule: (Pedro)IsA(estudiante) →   │
        │         (Pedro)estudia              │
        └─────────────────┬───────────────────┘
                          │
                          ▼
        ╔════════════════════════════════════════╗
        ║  STAGE 2: LOGICAL INFERENCE           ║
        ║  (logic_engine.py + deduction_rules)  ║
        ╚════════════════════════════════════════╝
                    │
                    │  • Parse expressions
                    │  • Apply inference rules
                    │  • Forward chaining
                    │  • Detect contradictions
                    │
                    ▼
        ┌─────────────────────────────────────┐
        │   DERIVED CONCLUSIONS               │
        │                                     │
        │   (Pedro)estudia                    │
        │   ← Modus Ponens: (Pedro)IsA(...) │
        └─────────────────────────────────────┘
```

---

## 🛠️ Installation & Setup

### Prerequisites

1. **Python 3.8+**
2. **Ollama** - Local LLM runtime
3. **Gemma 2B** - Language model for NLP

### Step 1: Install Ollama

```bash
# Visit https://ollama.ai and download for your platform
# Or use package managers:

# macOS
brew install ollama

# Linux
curl https://ollama.ai/install.sh | sh
```

### Step 2: Install Gemma Model

```bash
# Pull the Gemma 2B model (smaller, faster)
ollama pull gemma:2b

# Or Gemma 7B (larger, more accurate)
ollama pull gemma:7b
```

### Step 3: Start Ollama Service

```bash
# In a separate terminal
ollama serve
```

### Step 4: Install Text2Logic

No additional dependencies required - uses only Python standard library!

```bash
# Simply navigate to the parent directory
cd Inference/

# Import as module
python
>>> import Text2Logic as t2l
>>> t2l.verify_system()
```

---

## 💻 Usage

Text2Logic supports **three usage modes** to fit different needs:

### Mode 1: Direct Usage (Standalone Script)

Best for: Processing text files directly

```python
from Text2Logic import TextToLogicProcessor

# Create processor
processor = TextToLogicProcessor()

# Process a text file
processor.process_file(
    input_file="input.txt",
    output_file="output.inf",
    perform_inference=True,
    verbose=True
)
```

**Demo Script:**

```bash
cd Text2Logic
python demo_test.py
```

This will process `TEST.txt` from the parent directory.

---

### Mode 2: Internal API (Between Modules)

Best for: Integration with other Python modules

```python
from Text2Logic.api import convert_text, deduce_all, analyze_text

# Convert text to logic
facts, rules = convert_text("Pedro es estudiante")
print(facts)  # ['(Pedro)IsA(estudiante)']

# Perform inference
result = deduce_all(facts, rules)
print(f"Derived {len(result.derived_facts)} new facts")

# Or do both at once
analysis = analyze_text("Si Pedro es estudiante entonces estudia. Pedro es estudiante.")
print(analysis.inference.derived_facts)
```

---

### Mode 3: Library Usage (Recommended)

Best for: External programs and applications

```python
import Text2Logic as t2l

# Create system
system = t2l.LogicSystem()

# Verify dependencies (optional)
if not system.verify():
    print("Please install Ollama and Gemma")
    exit(1)

# Add natural language text
system.add_text("Pedro es un estudiante brillante que vive en Madrid")

# Add logical rules
system.add_rule("(X)IsA(estudiante) → (X)estudia")

# Perform inference
system.infer_all(verbose=True)

# Get results
conclusions = system.get_conclusions()
for c in conclusions:
    print(f"  • {c}")

# Get statistics
stats = system.get_statistics()
print(f"Total facts: {stats['total_facts']}")
print(f"Derived: {stats['derived_facts']}")

# Export to file
system.export("results.txt")
```

---

## 📝 Logic Format (.inf)

Text2Logic uses an extended `.inf` format with logical operators:

### Atoms (Facts)

```
(Pedro)IsA(estudiante)
(Bob)WorksAt(Microsoft)
(Ball)Has(color, red)
```

Format: `(Subject)Relation(Object1, Object2, ...)`

### Rules with Logical Operators

```
# Implication (→)
Rule: (Pedro)IsA(estudiante) → (Pedro)estudia

# Conjunction (∧)
Rule: (X)IsA(estudiante) ∧ (X)ViveEn(Madrid) → (X)TieneMetro

# Disjunction (∨)
(Pedro)Feliz ∨ (Pedro)Triste

# Negation (¬)
¬(Pedro)IsA(profesor)

# Biconditional (↔)
Rule: (X)EsMamifero ↔ (X)TienePelo
```

### Supported Operators

| Operator | Symbol | Spanish Keywords | Example |
|----------|--------|------------------|---------|
| AND | ∧ | "y" | A ∧ B |
| OR | ∨ | "o" | A ∨ B |
| NOT | ¬ | "no", "no es" | ¬A |
| IMPLIES | → | "entonces", "luego", "por lo tanto" | A → B |
| IFF | ↔ | "si y solo si", "equivale a" | A ↔ B |

---

## 🧠 Inference Rules

Text2Logic implements 9 fundamental inference rules:

### 1. Modus Ponens
```
A → B, A ⊢ B
```
If A implies B, and A is true, then B is true.

### 2. Modus Tollens
```
A → B, ¬B ⊢ ¬A
```
If A implies B, and B is false, then A is false.

### 3. Hypothetical Syllogism
```
A → B, B → C ⊢ A → C
```
Chain implications together.

### 4. Disjunctive Syllogism
```
A ∨ B, ¬A ⊢ B
```
If A or B, and not A, then B.

### 5. Simplification
```
A ∧ B ⊢ A, B
```
From conjunction, extract individual facts.

### 6. Conjunction
```
A, B ⊢ A ∧ B
```
Combine individual facts.

### 7. Resolution
```
¬A ∨ B, A ∨ C ⊢ B ∨ C
```
Fundamental rule for theorem proving.

### 8. Biconditional Elimination
```
A ↔ B ⊢ (A → B) ∧ (B → A)
```
Convert biconditional to implications.

### 9. Variable Unification
```
(X)IsA(estudiante), (Pedro)IsA(estudiante) ⊢ X=Pedro
```
Match variables with constants.

---

## 🎯 Examples

### Example 1: Simple Inference

**Input:**
```
Pedro es estudiante.
Si Pedro es estudiante entonces estudia.
```

**Processing:**
```python
import Text2Logic as t2l

system = t2l.LogicSystem()
system.add_text("Pedro es estudiante. Si Pedro es estudiante entonces estudia.")
system.infer_all()
print(system.get_conclusions())
```

**Output:**
```
[(Pedro)estudia]
```

**Reasoning Chain:**
```
(Pedro)estudia
  ← Modus Ponens: (Pedro)IsA(estudiante) ∧ ((Pedro)IsA(estudiante) → (Pedro)estudia)
```

---

### Example 2: Universal Rules

**Input:**
```
Pedro es estudiante.
María es estudiante.
Todo estudiante estudia.
Si alguien estudia entonces aprende.
```

**Derived Facts:**
```
(Pedro)estudia        ← Modus Ponens
(María)estudia        ← Modus Ponens
(Pedro)aprende        ← Modus Ponens (chained)
(María)aprende        ← Modus Ponens (chained)
```

---

### Example 3: Logical Operators

**Input:**
```
Pedro está feliz o triste.
Pedro no está feliz.
```

**Derived Facts:**
```
(Pedro)Triste         ← Disjunctive Syllogism
```

---

## 📊 Output Files

### 1. Logic File (.inf)

Contains extracted facts and rules:

```
# ═════════════════════════════════════════════════════════════
# FACTS
# ═════════════════════════════════════════════════════════════

(Pedro)IsA(estudiante)
(Pedro)ViveEn(Madrid)

# ═════════════════════════════════════════════════════════════
# RULES
# ═════════════════════════════════════════════════════════════

Rule: (X)IsA(estudiante) → (X)estudia
```

### 2. Inference Results File (_inferred.txt)

Complete analysis with derivations:

```
═══════════════════════════════════════════════════════════════
ORIGINAL FACTS
═══════════════════════════════════════════════════════════════
(Pedro)IsA(estudiante)
(Pedro)ViveEn(Madrid)

═══════════════════════════════════════════════════════════════
ORIGINAL RULES
═══════════════════════════════════════════════════════════════
(X)IsA(estudiante) → (X)estudia

═══════════════════════════════════════════════════════════════
DERIVED FACTS (BY INFERENCE DEPTH)
═══════════════════════════════════════════════════════════════

--- Depth 1 ---
(Pedro)estudia
  ← Modus Ponens: (Pedro)IsA(estudiante) ∧ ((X)IsA(estudiante) → (X)estudia) ⊢ (Pedro)estudia

═══════════════════════════════════════════════════════════════
SUMMARY
═══════════════════════════════════════════════════════════════
Original facts: 2
Original rules: 1
Derived facts: 1
Total facts: 4
Iterations: 1
```

---

## 🔧 API Reference

### LogicSystem Class

```python
class LogicSystem:
    def __init__(model_name="gemma:2b", auto_verify=False)
    def verify() -> bool
    def add_text(text: str, verbose: bool = False)
    def add_fact(fact: str)
    def add_rule(rule: str)
    def infer_all(verbose: bool = False)
    def get_conclusions() -> List[str]
    def get_all_facts() -> List[str]
    def query(query: str) -> bool
    def get_statistics() -> Dict
    def export(filepath: str)
    def clear()
```

### Functions

```python
def convert_text(text: str, model_name: str = "gemma:2b", verbose: bool = False) -> Tuple[List[str], List[str]]
def deduce_all(facts: List[str], rules: List[str], verbose: bool = False) -> InferenceResult
def analyze_text(text: str, model_name: str = "gemma:2b", verbose: bool = False) -> CompleteAnalysis
```

---

## ⚙️ Configuration

### Change Model

```python
# Use Gemma 7B for better accuracy (slower)
system = t2l.LogicSystem(model_name="gemma:7b")
```

### Adjust Iteration Limit

```python
from Text2Logic import LogicEngine

engine = LogicEngine(max_iterations=200)  # Default: 100
```

### Enable Conjunction Rule

```python
# Warning: Can be computationally expensive
engine = LogicEngine(enable_conjunction=True)
```

---

## 🐛 Troubleshooting

### "Cannot connect to Ollama"

**Solution:**
```bash
# Start Ollama service
ollama serve
```

### "Model gemma:2b not found"

**Solution:**
```bash
# Pull the model
ollama pull gemma:2b
```

### "Conversion produces no results"

**Possible causes:**
- Ollama not responding → Check `ollama serve` is running
- Model timeout → Increase timeout in `text_to_logic.py`
- Prompt not understood → Try rephrasing input text

### "Too many facts derived"

**Solution:**
```python
# Disable conjunction rule to reduce combinatorial explosion
engine = LogicEngine(enable_conjunction=False)
```

---

## 📚 Advanced Usage

### Custom Inference Rules

```python
from Text2Logic.deduction_rules import DeductionRule

class MyCustomRule(DeductionRule):
    def __init__(self):
        super().__init__("My Custom Rule", priority=5)
    
    def apply(self, knowledge_base, new_facts):
        # Implement custom logic
        return derived_facts

# Add to rule manager
from Text2Logic.deduction_rules import RuleManager
manager = RuleManager()
manager.rules.append(MyCustomRule())
```

### Direct Logic Parser Usage

```python
from Text2Logic import parse_expression

expr = parse_expression("(Pedro)IsA(estudiante) → (Pedro)estudia")
print(type(expr))  # LogicalExpression
print(expr.operator)  # LogicalOperator.IMPLIES
print(expr.operands[0])  # (Pedro)IsA(estudiante)
```

---

## 🔮 Future Enhancements

- [ ] Support for temporal logic (before, after, during)
- [ ] Modal logic operators (necessarily, possibly)
- [ ] Probabilistic reasoning
- [ ] Contradiction resolution strategies
- [ ] Interactive query interface
- [ ] Graph visualization of reasoning chains
- [ ] Export to Prolog/Datalog
- [ ] Multi-language support (English, French, etc.)

---

## 📄 License

Open source - Educational and research use.

---

## 👤 Author

**Marco**
- Version 1.0: October 2025
- Enhanced from Inference Engine v2.1

---

## 🙏 Acknowledgments

Built on top of:
- **Inference Engine v2.1** - Human-readable infix notation
- **Ollama** - Local LLM runtime
- **Gemma** - Google's language model

---

## 📞 Support

For issues, questions, or contributions, please refer to the parent Inference project documentation.

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║              Thank you for using Text2Logic!                                 ║
║              Natural • Logical • Powerful                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

