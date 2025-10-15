```
╔══════════════════════════════════════════════════════════════════════════════╗
║          INTEGRATED COGNITIVE INFERENCE SYSTEM - DOCUMENTATION               ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## 📋 Overview

This is a complete **Cognitive AI Pipeline** that transforms natural language text into structured knowledge, processes it through logical inference, and enriches it with emotional analysis.

### 🎯 What It Does

```
Natural Language Text
        ↓
[STAGE 1: NLP Extraction]
        ↓
Structured Facts (.inf format)
        ↓
[STAGE 2: Inference Engine]
        ↓
Natural Language Inferences
        ↓
[STAGE 3: Emotional Analysis]
        ↓
Emotionally Enriched Knowledge
```

---

## 🚀 Quick Start

### Prerequisites

1. **Install Ollama**
   ```bash
   # Visit https://ollama.ai/ and install Ollama
   # Then download the Gemma model:
   ollama pull gemma:2b
   ```

2. **Install Python Dependencies**
   ```bash
   pip install requests
   ```

3. **Have the inference engine ready**
   - Make sure `engine.py` is in the same directory

### Running the Complete System

```bash
python integrated_system.py
```

---

## 📁 File Structure

```
Inference/
├── engine.py                      # Core inference engine
├── nlp_to_inference.py           # NLP → Structured facts converter
├── emotional_analyzer.py         # Emotional analysis module
├── integrated_system.py          # Main integrated pipeline
├── test.inf                      # Sample inference file
├── README.md                     # Engine documentation
└── COGNITIVE_SYSTEM_README.md    # This file
```

---

## 🔧 How Each Component Works

### 1️⃣ NLP to Inference Converter (`nlp_to_inference.py`)

**Purpose:** Converts natural language sentences into structured inference format.

**Input:**
```
Pedro is an excellent student who lives in Madrid.
Bob is the father of Pedro and works at Microsoft.
```

**Output (.inf format):**
```
(Pedro)IsA(student)
(Pedro)LivesIn(Madrid)
(Bob)FatherOf(Pedro)
(Bob)WorksAt(Microsoft)
```

**Usage:**
```python
from nlp_to_inference import NLPToInferenceConverter

converter = NLPToInferenceConverter()
converter.convert_and_save("Your text here...", "output.inf")
```

---

### 2️⃣ Inference Engine (`engine.py`)

**Purpose:** Processes structured facts and generates natural language inferences with automatic concatenation.

**Input (.inf format):**
```
(Pedro)IsA(student)
(Pedro)LivesIn(Madrid)
(Bob)FatherOf(Pedro)
```

**Output:**
```
Pedro is a student and lives in Madrid.
Bob father of Pedro.
```

**Usage:**
```python
from engine import InferenceEngine

engine = InferenceEngine()
inferences = engine.load_file("input.inf")
for inference in inferences:
    print(inference)
```

---

### 3️⃣ Emotional Analyzer (`emotional_analyzer.py`)

**Purpose:** Analyzes inferences for emotional content and sentiment.

**Input:**
```
Pedro is a student and lives in Madrid.
The impact was terrible and broke the wall.
Pedro felt very happy about his success.
```

**Output:**
```
Pedro is a student and lives in Madrid.
  → Emotion: Neutral, Sentiment: Neutral

The impact was terrible and broke the wall.
  → Emotion: Sadness, Sentiment: Negative

Pedro felt very happy about his success.
  → Emotion: Joy, Sentiment: Positive
```

**Usage:**
```python
from emotional_analyzer import EmotionalAnalyzer

analyzer = EmotionalAnalyzer()
analyzer.analyze_and_save("inferences.txt", "emotional_analysis.txt")
```

---

### 4️⃣ Integrated System (`integrated_system.py`)

**Purpose:** Runs the complete pipeline automatically.

**Example:**
```python
from integrated_system import IntegratedCognitiveSystem

system = IntegratedCognitiveSystem()

text = """
Pedro is an excellent student who lives in Madrid. 
Bob is his father and works at Microsoft.
"""

system.process_and_save(text, "results.txt")
```

---

## 💻 Usage Examples

### Example 1: Process a Paragraph

```python
from integrated_system import IntegratedCognitiveSystem

system = IntegratedCognitiveSystem()

text = """
Marco is a talented teacher who loves helping students. 
He teaches Python to Pedro with great enthusiasm. 
Pedro feels very happy about learning programming.
"""

results = system.process_text(text, verbose=True)

# Access different parts of the analysis
print("Structured Facts:", results['structured_facts'])
print("Natural Inferences:", results['natural_inferences'])
print("Emotional Analysis:", results['emotional_analysis'])
print("Summary:", results['summary'])
```

### Example 2: Analyze a Story

```python
from integrated_system import IntegratedCognitiveSystem

system = IntegratedCognitiveSystem()

story = """
Once upon a time, there was a young boy named Pedro. Pedro was an 
excellent student who lived in the beautiful city of Madrid. He studied 
Computer Science and was very passionate about programming. His father, 
Bob, was an experienced programmer who worked at Microsoft. Bob was very 
proud of his son. One day, Marco, Pedro's teacher, taught him Python 
programming. Pedro was thrilled and excited to learn. However, later that 
day, while playing football, Pedro kicked the ball too hard. The ball 
impacted the wall violently and broke it. Pedro felt terrible about the 
incident and became very sad.
```

system.process_and_save(story, "story_analysis.txt")
```

### Example 3: Batch Processing

```python
from integrated_system import IntegratedCognitiveSystem

system = IntegratedCognitiveSystem()

texts = [
    "Bob is a programmer who lives in Seattle.",
    "Marco teaches Python to students.",
    "Pedro feels happy about his achievements."
]

for i, text in enumerate(texts, 1):
    results = system.process_text(text, verbose=False)
    print(f"\n--- Text {i} ---")
    for inf in results['natural_inferences']:
        emotion = results['emotional_analysis'][0]['emotion']
        sentiment = results['emotional_analysis'][0]['sentiment']
        print(f"{inf} [{emotion}, {sentiment}]")
```

---

## 📊 Output Format

The integrated system generates a comprehensive report with three stages:

### Stage 1: Structured Facts
```
(Pedro)IsA(student)
(Pedro)LivesIn(Madrid)
(Bob)FatherOf(Pedro)
```

### Stage 2: Natural Language Inferences
```
Pedro is a student and lives in Madrid.
Bob father of Pedro.
```

### Stage 3: Emotional Analysis
```
Pedro is a student and lives in Madrid.
  → Emotion: Neutral, Sentiment: Neutral

Bob father of Pedro.
  → Emotion: Neutral, Sentiment: Neutral
```

### Emotional Summary
```
Total Sentences: 2
Emotions:
  • Neutral: 2 (100.0%)
Sentiments:
  • Neutral: 2 (100.0%)
```

---

## 🎯 Supported Emotions

- **Joy**: Happiness, excitement, pleasure
- **Sadness**: Sorrow, disappointment, grief
- **Anger**: Frustration, irritation, rage
- **Fear**: Anxiety, worry, terror
- **Surprise**: Astonishment, amazement
- **Disgust**: Revulsion, distaste
- **Neutral**: No strong emotion

## 🎯 Supported Sentiments

- **Positive**: Favorable, good, pleasant
- **Negative**: Unfavorable, bad, unpleasant
- **Neutral**: Neither positive nor negative

---

## 🔧 Configuration

### Change the LLM Model

```python
system = IntegratedCognitiveSystem(model_name="gemma:7b")  # Use larger model
```

### Adjust Temperature for More Creative Output

Edit the temperature parameter in `nlp_to_inference.py` or `emotional_analyzer.py`:

```python
"temperature": 0.3  # Higher = more creative, Lower = more deterministic
```

---

## 🐛 Troubleshooting

### Error: "Connection refused to Ollama"

**Solution:** Make sure Ollama is running:
```bash
ollama serve
```

### Error: "Model not found"

**Solution:** Download the model:
```bash
ollama pull gemma:2b
```

### Inaccurate Conversions

**Solution:** Try a larger model:
```bash
ollama pull gemma:7b
# Then use: IntegratedCognitiveSystem(model_name="gemma:7b")
```

---

## 🚀 Future Enhancements

Potential improvements:

1. **Query System**: Ask questions about the knowledge base
2. **Relationship Graph**: Visualize connections between entities
3. **Temporal Reasoning**: Track changes over time
4. **Contradiction Detection**: Identify conflicting facts
5. **Multi-language Support**: Process text in Spanish, French, etc.
6. **Confidence Scores**: Assign certainty levels to inferences
7. **Interactive Mode**: Real-time processing with user feedback

---

## 📄 License

Open source - Educational and research use.

---

## 👤 Author

**Marco**
- Integrated Cognitive System: October 2025

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║           Thank you for using the Integrated Cognitive System!               ║
║                    Knowledge • Inference • Emotion                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

