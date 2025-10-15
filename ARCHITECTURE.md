```
╔══════════════════════════════════════════════════════════════════════════════╗
║            INTEGRATED COGNITIVE SYSTEM - ARCHITECTURE                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## 🏗️ System Architecture

### Complete Pipeline Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          INPUT: NATURAL LANGUAGE                         │
│                                                                          │
│  "Pedro is a student who lives in Madrid. Bob is his father and          │
│   works at Microsoft. Pedro feels happy about his achievements."         │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 │
                                 ▼
        ╔════════════════════════════════════════════════════╗
        ║  STAGE 1: NLP TO INFERENCE CONVERTER               ║
        ║  (nlp_to_inference.py)                             ║
        ╚════════════════════════════════════════════════════╝
                    │
                    │  Uses: Gemma LLM via Ollama
                    │  Process: Few-shot learning prompt
                    │
                    ▼
        ┌─────────────────────────────────────────┐
        │   STRUCTURED FACTS (.inf format)        │
        │                                         │
        │   (Pedro)IsA(student)                   │
        │   (Pedro)LivesIn(Madrid)                │
        │   (Bob)FatherOf(Pedro)                  │
        │   (Bob)WorksAt(Microsoft)               │
        │   (Pedro)FeelsHappy(achievements)       │
        └─────────────────┬───────────────────────┘
                          │
                          ▼
        ╔════════════════════════════════════════════════════╗
        ║  STAGE 2: INFERENCE ENGINE                         ║
        ║  (engine.py)                                       ║
        ╚════════════════════════════════════════════════════╝
                    │
                    │  Process: 
                    │  - Parse infix notation
                    │  - Group by subject
                    │  - Convert to natural language
                    │  - Concatenate with "and"
                    │
                    ▼
        ┌─────────────────────────────────────────┐
        │   NATURAL LANGUAGE INFERENCES           │
        │                                         │
        │   Pedro is a student and lives in       │
        │   Madrid and feels happy achievements.  │
        │   Bob father of Pedro and works at      │
        │   Microsoft.                            │
        └─────────────────┬───────────────────────┘
                          │
                          ▼
        ╔════════════════════════════════════════════════════╗
        ║  STAGE 3: EMOTIONAL ANALYZER                       ║
        ║  (emotional_analyzer.py)                           ║
        ╚════════════════════════════════════════════════════╝
                    │
                    │  Uses: Gemma LLM via Ollama
                    │  Process: Emotion & sentiment classification
                    │
                    ▼
        ┌─────────────────────────────────────────┐
        │   EMOTIONALLY ENRICHED KNOWLEDGE        │
        │                                         │
        │   Pedro is a student and lives in       │
        │   Madrid and feels happy achievements.  │
        │   → Emotion: Joy, Sentiment: Positive   │
        │                                         │
        │   Bob father of Pedro and works at      │
        │   Microsoft.                            │
        │   → Emotion: Neutral, Sentiment: Neutral│
        └─────────────────┬───────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────┐
        │        FINAL OUTPUT + SUMMARY           │
        │                                         │
        │  • Complete analysis report             │
        │  • Emotional distribution statistics    │
        │  • Sentiment analysis summary           │
        └─────────────────────────────────────────┘
```

---

## 📦 Module Breakdown

### 1. nlp_to_inference.py

**Class:** `NLPToInferenceConverter`

**Responsibility:** Convert free-form text to structured inference format

**Key Methods:**
- `split_into_sentences(text)` → Breaks text into individual sentences
- `convert_sentence(sentence)` → Converts one sentence using Gemma
- `convert_text(text)` → Processes entire text
- `convert_and_save(text, file)` → Saves to .inf file

**External Dependencies:**
- Ollama API (http://localhost:11434)
- Gemma LLM model

**Input Example:**
```
"Pedro is a student who lives in Madrid."
```

**Output Example:**
```
(Pedro)IsA(student)
(Pedro)LivesIn(Madrid)
```

---

### 2. engine.py

**Class:** `InferenceEngine`

**Responsibility:** Process structured facts and generate natural language

**Key Methods:**
- `parse_line(line)` → Parses infix notation
- `_parse_infix(line)` → Handles (Subject)Relation(Object) format
- `format_relation(text)` → Converts CamelCase/snake_case to natural language
- `to_natural_language()` → Generates sentences with concatenation
- `load_file(path)` → Loads and processes .inf file

**External Dependencies:**
- None (pure Python)

**Input Example:**
```
(Pedro)IsA(student)
(Pedro)LivesIn(Madrid)
```

**Output Example:**
```
Pedro is a student and lives in Madrid.
```

---

### 3. emotional_analyzer.py

**Class:** `EmotionalAnalyzer`

**Responsibility:** Analyze emotional content and sentiment

**Key Methods:**
- `analyze_sentence(sentence)` → Classifies one sentence using Gemma
- `analyze_file(file)` → Analyzes all sentences in a file
- `get_emotional_summary(results)` → Generates statistics
- `analyze_and_save(input, output)` → Saves analysis results

**External Dependencies:**
- Ollama API (http://localhost:11434)
- Gemma LLM model

**Emotions Detected:**
- Joy, Sadness, Anger, Fear, Surprise, Disgust, Neutral

**Sentiments Detected:**
- Positive, Negative, Neutral

**Input Example:**
```
"Pedro is a student and lives in Madrid."
```

**Output Example:**
```
Emotion: Neutral, Sentiment: Neutral
```

---

### 4. integrated_system.py

**Class:** `IntegratedCognitiveSystem`

**Responsibility:** Orchestrate the complete pipeline

**Key Methods:**
- `process_text(text)` → Runs all 3 stages
- `process_and_save(text, file)` → Saves complete analysis
- `_cleanup_temp_files()` → Removes intermediate files

**External Dependencies:**
- All three modules above
- Ollama API

**Workflow:**
1. Instantiates all three components
2. Coordinates data flow between stages
3. Manages temporary files
4. Generates comprehensive reports

---

## 🔄 Data Flow

### Stage 1: Text → Facts

```python
# Input
text = "Pedro is a student."

# NLPToInferenceConverter
converter.convert_sentence(text)

# Gemma processes with few-shot prompt
# Returns: "(Pedro)IsA(student)"

# Output saved to .inf file
```

### Stage 2: Facts → Inferences

```python
# Input from .inf file
"(Pedro)IsA(student)"
"(Pedro)LivesIn(Madrid)"

# InferenceEngine
engine.load_file("facts.inf")

# Parsing and grouping
# Subject "Pedro" has 2 relations

# Output with concatenation
"Pedro is a student and lives in Madrid."
```

### Stage 3: Inferences → Emotions

```python
# Input
"Pedro is a student and lives in Madrid."

# EmotionalAnalyzer
analyzer.analyze_sentence(inference)

# Gemma classifies emotion and sentiment

# Output
{
  'emotion': 'Neutral',
  'sentiment': 'Neutral'
}
```

---

## 🔌 Integration Points

### Between Stage 1 and 2

**Interface:** `.inf` file format

**Data Structure:**
```
(Subject)Relation(Object)
(Subject)Relation(Object)
...
```

**Validation:** Engine validates syntax during parsing

---

### Between Stage 2 and 3

**Interface:** Plain text file

**Data Structure:**
```
Natural language sentence.
Natural language sentence.
...
```

**Format:** One inference per line

---

## 🎯 Design Patterns Used

### 1. Pipeline Pattern
- Sequential processing stages
- Each stage transforms data for the next

### 2. Strategy Pattern
- Different parsing strategies (infix, n-ary, definition)
- Pluggable LLM models

### 3. Template Method Pattern
- Prompt templates with placeholders
- Consistent LLM interaction pattern

### 4. Facade Pattern
- `IntegratedCognitiveSystem` provides simple interface
- Hides complexity of individual components

---

## 🔧 Extension Points

### Add New Inference Format

1. Extend `InferenceEngine._parse_line()`
2. Add new parsing method
3. Update `to_natural_language()` if needed

### Add New Emotion

1. Update prompt in `EmotionalAnalyzer._create_prompt_template()`
2. Add examples for the new emotion
3. Update documentation

### Use Different LLM

1. Replace Ollama calls with new API
2. Adjust prompt format if needed
3. Update temperature/parameters

### Add New Pipeline Stage

1. Create new module with similar structure
2. Integrate in `IntegratedCognitiveSystem`
3. Update data flow

---

## 📊 Performance Considerations

### Bottlenecks

1. **LLM API Calls** (Stages 1 & 3)
   - Solution: Batch processing, caching

2. **File I/O** (All stages)
   - Solution: Stream processing for large files

3. **Sentence Splitting** (Stage 1)
   - Solution: Use faster regex patterns

### Optimization Strategies

1. **Parallel Processing**: Process sentences in parallel
2. **Caching**: Cache LLM responses for repeated sentences
3. **Streaming**: Process data streams instead of loading entire files
4. **Model Selection**: Use smaller models for faster processing

---

## 🛡️ Error Handling

### Stage 1: NLP Conversion
- **Connection errors**: Retry with exponential backoff
- **Invalid responses**: Log and skip sentence
- **Timeout**: Use longer timeout for complex sentences

### Stage 2: Inference Engine
- **Syntax errors**: Skip invalid lines, log warning
- **Empty file**: Return empty list
- **Encoding issues**: Try multiple encodings

### Stage 3: Emotional Analysis
- **Classification errors**: Default to "Unknown"
- **API failures**: Retry or skip
- **Invalid format**: Parse robustly with fallbacks

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      End of Architecture Documentation                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

