# Text2Logic - 2 Minute Guide

## What Does It Do?

Converts text → formal logic → automatically derives conclusions

```
"Pedro is a student. Students study."
           ↓
(Pedro)IsA(student)
Rule: (X)IsA(student) -> (X)Studies()
           ↓
CONCLUSION: (Pedro)Studies() ✓
```

## Install (3 steps)

```bash
# 1. Install Ollama from https://ollama.ai

# 2. Get Gemma model
ollama pull gemma:2b

# 3. Start Ollama (keep it running)
ollama serve
```

## Use (3 lines of code)

```python
import Text2Logic as t2l

system = t2l.LogicSystem()
system.add_fact("(Pedro)IsA(student)")
system.add_rule("(X)IsA(student) -> (X)Studies()")
system.infer_all()
print(system.get_conclusions())  # [(Pedro)Studies()]
```

## That's It!

**More examples:** See `QUICK_START.md`  
**Full docs:** See `README.md`  
**Run demo:** `python Text2Logic/demo_test.py`

---

## Format Rules

✅ **Correct:**
```
(Pedro)IsA(student)
(Bob)WorksAt(Microsoft)
Rule: (X)IsA(student) -> (X)Studies()
```

❌ **Wrong:**
```
(Pedro is a) IsA (student)  ← NO spaces in names
Pedro IsA student            ← NO missing parentheses
(Pedro)IsA(X)IsA(Y)         ← NO chained without arrows
```

---

## Inference Rules (9 total)

The system automatically applies:

1. **Modus Ponens**: If A→B and A, then B
2. **Modus Tollens**: If A→B and not B, then not A
3. **Hypothetical Syllogism**: If A→B and B→C, then A→C
4. **+6 more rules**

---

## Troubleshoot

| Problem | Solution |
|---------|----------|
| "Cannot connect to Ollama" | Run `ollama serve` |
| "Model not found" | Run `ollama pull gemma:2b` |
| Tests fail | Run `python Text2Logic/test_basic.py` |

---

**Quick Test:**

```bash
python Text2Logic/test_basic.py
```

Should see: `[SUCCESS] ALL TESTS PASSED!`

---

**Version:** 1.0 | **Status:** Ready ✅ | **Author:** Marco

