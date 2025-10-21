```
╔══════════════════════════════════════════════════════════════════════════════╗
║                  HUMAN-READABLE INFERENCE ENGINE                             ║
║                            Version 2.1                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## 📋 Overview

A **human-readable** inference engine focused on **infix notation** for natural expression of relationships. Unlike Prolog's prefix notation, this engine uses intuitive `(Subject)relation(Object)` syntax that reads naturally.

**New in V2.1:** Automatic concatenation of multiple relations with the same subject using "y" (and)!

---

## 🚀 Key Features

### ✨ Human-Readable Infix Notation
- **Primary syntax**: `(Pedro)EsAmigoDe(Miguel)` ← Natural to read!
- **NOT**: `EsAmigoDe(Pedro, Miguel)` ← Prolog style (less readable)
- Reads like natural language

### 🔗 Automatic Concatenation
**New Feature!** Multiple relations with the same subject are automatically grouped:

```
Input:
(Pedro)Es(programador)
(Pedro)PadreDe(Peter)
(Pedro)ViveEn(Madrid)

Output:
Pedro es programador y padre de Peter y vive en Madrid.
```

### 🔤 Intelligent Name Conversion
- **CamelCase**: `PadreDe` → "padre de"
- **snake_case**: `padre_de` → "padre de"  
- **Mixed**: `Parece_Un` → "parece un"

### ⛓️ Chained Relations
Express causality and sequences naturally:
```
(Pedro)patea(Ball)impacta(Wall)
→ Pedro patea Ball.
  Ball impacta Wall.
```

---

## 📁 Project Structure

```
Inference/
├── engine.py          # Human-readable inference engine (Version 2.1)
├── test.inf          # Comprehensive test file with examples
└── README.md         # This file
```

---

## 🛠️ Installation

No dependencies required. Uses only Python standard library.

**Requirements:**
- Python 3.6 or higher

---

## 💻 Usage

### Basic Usage

```python
from engine import InferenceEngine

# Create engine instance
engine = InferenceEngine()

# Load and process inference file
inferences = engine.load_file("test.inf")

# Display results
for inference in inferences:
    print(inference)
```

### Command Line

```bash
python engine.py
```

---

## 📝 Syntax - Human-Readable Infix Notation

### Primary Format: (Subject)Relation(Object)

This is the **main and recommended** syntax - it's natural and easy to read!

```
(Pedro)EsAmigoDe(Miguel)        ✓ Natural, reads like language
(Bob)PadreDe(Pedro)             ✓ Easy to understand
(Marco)TrabajaEn(OpenAI)        ✓ Intuitive

EsAmigoDe(Pedro, Miguel)        ✗ Prolog style, less readable
```

---

## 🎯 Complete Examples

### Example 1: Basic Relations

**Input:**
```
(Pedro)EsUn(estudiante)
(Bob)EsUn(programador)
(Bob)PadreDe(Pedro)
```

**Output:**
```
Pedro es un estudiante.
Bob es un programador y padre de Pedro.
```

Notice how Bob's two relations are automatically concatenated!

### Example 2: Multiple Properties

**Input:**
```
(Pedro)EsUn(estudiante)
(Pedro)Estudia(Informatica)
(Pedro)ViveEn(Madrid)
(Pedro)EsAmigoDe(Miguel)

(Miguel)EsUn(estudiante)
(Miguel)Estudia(Matematicas)
(Miguel)ViveEn(Barcelona)
```

**Output:**
```
Pedro es un estudiante y estudia Informatica y vive en Madrid y es amigo de Miguel.
Miguel es un estudiante y estudia Matematicas y vive en Barcelona.
```

### Example 3: Chained Actions

**Input:**
```
(Pedro)patea(Ball)impacta(Wall)
(Ball)rebota_en(Wall)cae_al(suelo)
```

**Output:**
```
Pedro patea Ball.
Ball impacta Wall y rebota en Wall.
Wall cae al suelo.
```

### Example 4: Mixed Formats

**Input:**
```
(Pedro)EsAmigoDe(Miguel)        # CamelCase
(Pedro)es_amigo_de(Juan)        # snake_case
(Pedro)vive_en(Madrid)          # snake_case
```

**Output:**
```
Pedro es amigo de Miguel y es amigo de Juan y vive en Madrid.
```

Both CamelCase and snake_case work perfectly!

---

## 🔧 Supported Syntaxes

### 1. Simple Binary Relations

Syntax: `(Subject)Relation(Object)`

```
(Pedro)EsAmigoDe(Miguel)        → Pedro es amigo de Miguel.
(Bob)PadreDe(Pedro)             → Bob padre de Pedro.
(Marco)TrabajaEn(OpenAI)        → Marco trabaja en OpenAI.
```

### 2. Multi-Object Relations

Syntax: `(Subject)Relation(obj1, obj2, ...)`

```
(Ball)Tiene(color, rojo)        → Ball tiene color, rojo.
(Marco)Enseña(Python, Pedro)    → Marco enseña Python, Pedro.
```

### 3. Nullary Relations (Properties)

Syntax: `(Subject)Relation()`

```
(Pedro)EstaFeliz()              → Pedro esta feliz.
(Ball)EstaEnMovimiento()        → Ball esta en movimiento.
```

### 4. Chained Relations

Syntax: `(A)rel1(B)rel2(C)...`

```
(Pedro)patea(Ball)impacta(Wall)
→ Creates two relations:
  - Pedro patea Ball.
  - Ball impacta Wall.
```

### 5. Automatic Concatenation

When consecutive relations have the same subject, they're joined with "y":

```
(Pedro)EsUn(estudiante)
(Pedro)ViveEn(Madrid)
(Pedro)Estudia(Informatica)

→ Pedro es un estudiante y vive en Madrid y estudia Informatica.
```

### 6. Comments

```
# Full line comment
(Pedro)EsAmigoDe(Miguel)        # Inline comment
```

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│             Human-Readable Inference Engine                        │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Input: (Subject)Relation(Object)  ← Infix Notation               │
│         ↓                                                          │
│  ┌──────────────┐                                                  │
│  │  parse_line  │  ─→  Parse Infix Format                         │
│  └──────────────┘                                                  │
│         ↓                                                          │
│  ┌──────────────┐                                                  │
│  │ _parse_infix │  ─→  Extract (Subject) and relation(Object)     │
│  └──────────────┘                                                  │
│         ↓                                                          │
│  ┌──────────────┐                                                  │
│  │  relations   │  ─→  [(subject, relation, [objects]), ...]      │
│  └──────────────┘                                                  │
│         ↓                                                          │
│  ┌──────────────────────┐                                          │
│  │ to_natural_language  │  ─→  Group by subject                   │
│  └──────────────────────┘      Concatenate with "y"               │
│         ↓                                                          │
│  Natural Language Sentences                                        │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 API Reference

### Class: `InferenceEngine`

A human-readable inference engine using infix notation.

#### Methods

##### `__init__()`
Initializes the engine with empty relation storage.

##### `load_file(path: str) -> list`
Loads and processes an inference file.

**Parameters:**
- `path` (str): Path to the .inf file

**Returns:**
- `list`: Natural language sentences

**Example:**
```python
engine = InferenceEngine()
sentences = engine.load_file("test.inf")
```

##### `parse_line(line: str) -> None`
Parses a line using infix notation.

**Supports:**
- Simple: `(Subject)Relation(Object)`
- Chained: `(A)Rel1(B)Rel2(C)`
- Multi-object: `(Subject)Relation(obj1, obj2)`
- Nullary: `(Subject)Relation()`

##### `format_relation(text: str) -> str`
Converts relation names to natural language.

**Example:**
```python
engine.format_relation("PadreDe")      # Returns: "padre de"
engine.format_relation("trabaja_en")   # Returns: "trabaja en"
```

##### `to_natural_language() -> list`
Converts stored relations to natural language with automatic concatenation.

**Returns:**
- `list`: Natural language sentences (grouped by subject)

---

## 🆚 Comparison: Infix vs Prefix

### This Engine (Infix - Human Readable)
```
(Pedro)EsAmigoDe(Miguel)            ✓ Natural
(Bob)PadreDe(Pedro)                 ✓ Easy to read
(Marco)TrabajaEn(OpenAI)            ✓ Intuitive
```

### Prolog Style (Prefix - Less Readable)
```
EsAmigoDe(Pedro, Miguel)            ✗ Less natural
PadreDe(Bob, Pedro)                 ✗ Harder to read
TrabajaEn(Marco, OpenAI)            ✗ Not intuitive
```

**Why Infix is Better for Humans:**
- Reads like natural language: "(Pedro) is friend of (Miguel)"
- Subject comes first, like in Spanish/English sentences
- Relation connects subject and object naturally
- Easier to write and understand at a glance

---

## 🎨 Name Conversion Examples

| Input Format | Output Format |
|-------------|---------------|
| `PadreDe` | padre de |
| `padre_de` | padre de |
| `EsAmigoDe` | es amigo de |
| `es_amigo_de` | es amigo de |
| `TrabajaEn` | trabaja en |
| `trabaja_en` | trabaja en |
| `PareceUn` | parece un |

---

## 🧪 Testing

Run the test file with comprehensive examples:

```bash
python engine.py
```

Expected output shows:
- Automatic concatenation of same-subject relations
- CamelCase and snake_case conversions
- Chained relation processing
- Multi-object relation handling

---

## 📚 Advanced Features

### Automatic Concatenation Logic

Relations are grouped by subject **only if consecutive**:

```
(Pedro)Es(estudiante)       ─┐
(Pedro)ViveEn(Madrid)        ├─→ Concatenated: "Pedro es estudiante y vive en Madrid."
                            ─┘

(Bob)Es(programador)        ─→ Separate: "Bob es programador."

(Pedro)Estudia(Informatica) ─→ Separate: "Pedro estudia Informatica."
```

### Chained Relation Processing

Chains are processed left-to-right with object becoming next subject:

```
(A)Rel1(B)Rel2(C)Rel3(D)

Produces:
- (A, Rel1, [B])
- (B, Rel2, [C])
- (C, Rel3, [D])

Then grouped by subject:
- A Rel1 B.
- B Rel2 C.
- C Rel3 D.
```

### Encoding Support

Automatically detects file encoding:
- UTF-8 (standard)
- UTF-16 (Windows Notepad)
- Latin-1, CP1252, ISO-8859-1 (legacy)

---

## 🤝 Contributing

Contributions welcome!

Guidelines:
1. Maintain infix notation as primary syntax
2. Keep human readability as top priority
3. Document all new features clearly
4. Add test cases for new syntax

---

## 🐛 Known Issues

- Console may display special characters (ñ, á, é) incorrectly on Windows
  - This is a console encoding issue, not a logic problem
  - The .inf files and internal processing handle UTF-8 correctly

---

## 🔮 Future Enhancements

- Configurable conjunction word (use "and" instead of "y")
- Support for negation: `(Pedro)NoEs(programador)`
- Conditional statements: `Si(Pedro)Es(estudiante)Entonces(estudia)`
- Query system: Ask questions about stored relations
- Graph visualization of relationships
- Export to natural language in multiple languages

---

## 📄 License

Open source - Educational and research use.

---

## 👤 Author

**Marco**
- Version 2.1: October 2025 (Automatic concatenation)
- Version 2.0: October 2025 (Generic rewrite)
- Version 1.0: October 2025 (Initial release)

---

## 🎓 Use Cases

- **Knowledge bases**: Express facts naturally
- **Natural language generation**: Convert logic to readable text
- **Educational tool**: Teach logic and inference
- **Rapid prototyping**: Test logical models quickly
- **Storytelling**: Express narratives as logical relations
- **Data modeling**: Document domain relationships

---

## 💡 Philosophy

This engine prioritizes **human readability** over computational efficiency:

```
(Pedro)EsAmigoDe(Miguel)        ← Reads naturally
```

vs

```
friend_of(pedro, miguel).       ← Prolog: machine-oriented
```

**The goal:** Make logical inference accessible to humans, not just computers.

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║              Thank you for using Human-Readable Inference Engine!            ║
║                      Natural • Intuitive • Powerful                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
