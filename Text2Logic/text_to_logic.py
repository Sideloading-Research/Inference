"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                TEXT TO LOGIC CONVERTER - ENHANCED NLP CONVERTER              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Module Description:
    Enhanced converter from natural language text to formal logic (.inf format).
    Includes Ollama/Gemma verification, logical connective detection, and
    improved sentence decomposition.

Author: Marco
Date: October 2025
Version: 1.0 - Enhanced from nlp_to_inference.py
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

import re
import json
import requests
import subprocess
import sys
from typing import List, Optional, Tuple, Dict


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

class SystemVerifier:
    """Verifies that Ollama and Gemma are properly installed."""
    
    @staticmethod
    def check_ollama_installed() -> Tuple[bool, str]:
        """
        Check if Ollama is installed and accessible.
        
        Returns:
            Tuple of (is_installed, message)
        """
        try:
            result = subprocess.run(
                ['ollama', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return True, f"Ollama installed: {result.stdout.strip()}"
            else:
                return False, "Ollama command found but returned error"
        except FileNotFoundError:
            return False, "Ollama not found. Please install from https://ollama.ai"
        except subprocess.TimeoutExpired:
            return False, "Ollama command timed out"
        except Exception as e:
            return False, f"Error checking Ollama: {e}"
    
    @staticmethod
    def check_ollama_running() -> Tuple[bool, str]:
        """
        Check if Ollama service is running.
        
        Returns:
            Tuple of (is_running, message)
        """
        try:
            response = requests.get(
                "http://localhost:11434/api/tags",
                timeout=5
            )
            if response.status_code == 200:
                return True, "Ollama service is running"
            else:
                return False, f"Ollama service returned status {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "Cannot connect to Ollama. Please run: ollama serve"
        except Exception as e:
            return False, f"Error connecting to Ollama: {e}"
    
    @staticmethod
    def check_gemma_installed(model_name: str = "gemma:2b") -> Tuple[bool, str]:
        """
        Check if specified Gemma model is installed.
        
        Args:
            model_name: Name of the model to check
        
        Returns:
            Tuple of (is_installed, message)
        """
        try:
            response = requests.get(
                "http://localhost:11434/api/tags",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                model_names = [m.get('name', '') for m in models]
                
                # Check for exact match or with :latest
                if model_name in model_names or f"{model_name}:latest" in model_names:
                    return True, f"Model {model_name} is installed"
                else:
                    available = ", ".join(model_names) if model_names else "none"
                    return False, f"Model {model_name} not found. Available: {available}"
            else:
                return False, "Could not retrieve model list"
        except Exception as e:
            return False, f"Error checking models: {e}"
    
    @classmethod
    def verify_system(cls, model_name: str = "gemma:2b") -> Tuple[bool, List[str]]:
        """
        Perform complete system verification.
        
        Args:
            model_name: Name of the model to verify
        
        Returns:
            Tuple of (all_ok, messages)
        """
        messages = []
        all_ok = True
        
        # Check Ollama installed
        is_installed, msg = cls.check_ollama_installed()
        messages.append(f"{'✓' if is_installed else '✗'} {msg}")
        if not is_installed:
            all_ok = False
            return all_ok, messages
        
        # Check Ollama running
        is_running, msg = cls.check_ollama_running()
        messages.append(f"{'✓' if is_running else '✗'} {msg}")
        if not is_running:
            all_ok = False
            return all_ok, messages
        
        # Check Gemma installed
        has_model, msg = cls.check_gemma_installed(model_name)
        messages.append(f"{'✓' if has_model else '✗'} {msg}")
        if not has_model:
            all_ok = False
        
        return all_ok, messages


# ═══════════════════════════════════════════════════════════════════════════════
# TEXT TO LOGIC CONVERTER
# ═══════════════════════════════════════════════════════════════════════════════

class TextToLogicConverter:
    """
    Enhanced converter from natural language to formal logic.
    
    Improvements over nlp_to_inference.py:
        - System verification (Ollama, Gemma)
        - Logical connective detection
        - Improved sentence splitting
        - Better error handling and retries
        - Support for logical operators in output
    
    Example:
        >>> converter = TextToLogicConverter()
        >>> converter.verify_dependencies()
        >>> facts, rules = converter.convert_text("Si Pedro es estudiante entonces estudia")
    """
    
    # Logical connectives in Spanish
    CONNECTIVES = {
        'y': '∧',
        'o': '∨',
        'no': '¬',
        'entonces': '→',
        'luego': '→',
        'por lo tanto': '→',
        'si y solo si': '↔',
        'equivale a': '↔',
    }
    
    def __init__(self, model_name: str = "gemma:2b", api_url: str = "http://localhost:11434/api/generate"):
        """
        Initialize the enhanced text to logic converter.
        
        Args:
            model_name: Ollama model to use
            api_url: Ollama API endpoint
        """
        self.model_name = model_name
        self.api_url = api_url
        self.prompt_template = self._create_prompt_template()
        self.verified = False
    
    def verify_dependencies(self) -> bool:
        """
        Verify that all dependencies are installed and running.
        
        Returns:
            True if all dependencies are OK, False otherwise
        """
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                    SYSTEM VERIFICATION                                       ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
        
        all_ok, messages = SystemVerifier.verify_system(self.model_name)
        
        for msg in messages:
            print(f"  {msg}")
        
        print()
        
        if all_ok:
            print("✓ All dependencies verified successfully\n")
            self.verified = True
        else:
            print("✗ Some dependencies are missing. Please install them.\n")
            print("Installation instructions:")
            print("  1. Install Ollama: https://ollama.ai")
            print("  2. Run Ollama service: ollama serve")
            print(f"  3. Pull Gemma model: ollama pull {self.model_name}\n")
            self.verified = False
        
        return all_ok
    
    def _create_prompt_template(self) -> str:
        """
        Create enhanced prompt template with logical operators support.
        
        Returns:
            Prompt template string
        """
        return """You are an expert in knowledge engineering. Your ONLY task is to convert sentences to formal logic notation.

STRICT RULES:
1. Output format MUST be: (Subject)RelationInCamelCase(Object)
2. Subject and Object must be SINGLE words or short names - NO spaces, NO extra parentheses
3. Relation must be CamelCase - NO spaces
4. For simple facts: (Subject)Relation(Object)
5. For logical rules with "if...then": Rule: (Subject)Relation(Object) -> (Subject2)Relation2(Object2)
6. NEVER put parentheses inside Subject or Object
7. NEVER use symbols like =, ∈, or operators inside atoms
8. NO explanations - ONLY the logic lines
9. If you cannot convert cleanly, output nothing

### CORRECT Examples ###

Input: Pedro is a student.
Output: (Pedro)IsA(student)

Input: The alarm rang at seven.
Output: (Alarm)RanAt(seven)

Input: Bob works at Microsoft.
Output: (Bob)WorksAt(Microsoft)

Input: If Pedro is a student then he studies.
Output: Rule: (Pedro)IsA(student) -> (Pedro)Studies()

Input: I made breakfast.
Output: (I)Made(breakfast)

Input: The sky was cloudy.
Output: (Sky)Was(cloudy)

### WRONG Examples (DO NOT DO THIS) ###

WRONG: (El despertador)Sonó(a)a(las siete)en(punto)
CORRECT: (Alarm)RanAt(seven)

WRONG: (X)Fuerza(X) → (X)ViajóAlBaño
CORRECT: Rule: (X)Went() -> (X)WentToBathroom()

WRONG: (Persona) lavarse(cara) ∧ (Temperatura) = (Persona) despertarse
CORRECT: Rule: (Person)Washed(face) -> (Person)WokeUp()

### End of Examples ###

Now convert this sentence (ONLY output logic lines, nothing else):
{sentence}
"""
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences with improved logic.
        
        Args:
            text: Input text
        
        Returns:
            List of sentences
        """
        # Replace common abbreviations to avoid false splits
        text = re.sub(r'\bDr\.', 'Dr', text)
        text = re.sub(r'\bSr\.', 'Sr', text)
        text = re.sub(r'\bSra\.', 'Sra', text)
        
        # Split on sentence endings
        sentences = re.split(r'[.!?]+', text)
        
        # Clean and filter
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def detect_logical_structure(self, sentence: str) -> Dict[str, bool]:
        """
        Detect logical connectives in the sentence.
        
        Args:
            sentence: Input sentence
        
        Returns:
            Dictionary with detected structures
        """
        sentence_lower = sentence.lower()
        
        return {
            'has_implication': any(word in sentence_lower for word in ['si', 'entonces', 'luego', 'por lo tanto']),
            'has_biconditional': any(phrase in sentence_lower for phrase in ['si y solo si', 'equivale a']),
            'has_conjunction': ' y ' in sentence_lower,
            'has_disjunction': ' o ' in sentence_lower,
            'has_negation': any(word in sentence_lower for word in ['no es', 'no ', 'nunca']),
        }
    
    def convert_sentence(self, sentence: str, max_retries: int = 3) -> Optional[str]:
        """
        Convert a single sentence to logic format with retries.
        
        Args:
            sentence: Input sentence
            max_retries: Number of retry attempts
        
        Returns:
            Converted logic notation or None if failed
        """
        prompt = self.prompt_template.format(sentence=sentence)
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False,
                        "temperature": 0.1
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    inference_text = result.get("response", "").strip()
                    inference_text = self._clean_response(inference_text)
                    
                    if inference_text:
                        return inference_text
                
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    print(f"Error after {max_retries} attempts: {e}")
                    return None
                continue
        
        return None
    
    def _clean_response(self, text: str) -> str:
        """
        Clean LLM response to extract only valid inference lines.
        
        Args:
            text: Raw LLM response
        
        Returns:
            Cleaned inference text
        """
        lines = text.split('\n')
        valid_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Check if line is a valid inference or rule
            if re.match(r'Rule:\s*\(', line) or re.match(r'\([^)]+\)[A-Za-z_]', line):
                valid_lines.append(line)
        
        return '\n'.join(valid_lines)
    
    def convert_text(self, text: str, verbose: bool = True) -> Tuple[List[str], List[str]]:
        """
        Convert entire text to logic format.
        
        Args:
            text: Input text
            verbose: Print progress
        
        Returns:
            Tuple of (facts, rules)
        """
        if not self.verified:
            print("⚠️  Warning: Dependencies not verified. Run verify_dependencies() first.")
        
        sentences = self.split_into_sentences(text)
        all_facts = []
        all_rules = []
        
        if verbose:
            print(f"Processing {len(sentences)} sentences...\n")
            print("=" * 70)
        
        for i, sentence in enumerate(sentences, 1):
            if verbose:
                print(f"\n[{i}/{len(sentences)}] {sentence}")
            
            # Detect logical structure
            structure = self.detect_logical_structure(sentence)
            
            if verbose and any(structure.values()):
                detected = [k.replace('has_', '') for k, v in structure.items() if v]
                print(f"  Detected: {', '.join(detected)}")
            
            # Convert
            result = self.convert_sentence(sentence)
            
            if result:
                if verbose:
                    print(f"  → {result.replace(chr(10), chr(10) + '     ')}")
                
                # Separate facts and rules
                for line in result.split('\n'):
                    if line.strip().startswith('Rule:'):
                        all_rules.append(line.strip())
                    else:
                        all_facts.append(line.strip())
            else:
                if verbose:
                    print(f"  → (Could not convert)")
        
        if verbose:
            print("\n" + "=" * 70)
            print(f"Conversion complete: {len(all_facts)} facts, {len(all_rules)} rules")
        
        return all_facts, all_rules
    
    def convert_file(self, input_file: str, output_file: str, verbose: bool = True):
        """
        Convert a text file to .inf format.
        
        Args:
            input_file: Path to input text file
            output_file: Path to output .inf file
            verbose: Print progress
        """
        # Read input file with multiple encoding support
        encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
        text = None
        
        for encoding in encodings:
            try:
                with open(input_file, 'r', encoding=encoding) as f:
                    text = f.read()
                break
            except (UnicodeDecodeError, FileNotFoundError):
                continue
        
        if text is None:
            raise ValueError(f"Could not read file: {input_file}")
        
        # Convert
        facts, rules = self.convert_text(text, verbose=verbose)
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Generated logic file from natural language\n")
            f.write("# " + "=" * 74 + "\n")
            f.write(f"# Source: {input_file}\n")
            f.write("# " + "=" * 74 + "\n\n")
            
            if facts:
                f.write("# ═════════════════════════════════════════════════════════════\n")
                f.write("# FACTS\n")
                f.write("# ═════════════════════════════════════════════════════════════\n\n")
                for fact in facts:
                    if fact:
                        f.write(fact + "\n")
                f.write("\n")
            
            if rules:
                f.write("# ═════════════════════════════════════════════════════════════\n")
                f.write("# RULES\n")
                f.write("# ═════════════════════════════════════════════════════════════\n\n")
                for rule in rules:
                    if rule:
                        f.write(rule + "\n")
        
        if verbose:
            print(f"\n✓ Output saved to: {output_file}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION BLOCK (FOR TESTING)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    """Test the text to logic converter."""
    
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║              TEXT TO LOGIC CONVERTER - TEST SUITE                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
    
    # Create converter
    converter = TextToLogicConverter(model_name="gemma:2b")
    
    # Verify dependencies
    if not converter.verify_dependencies():
        print("Cannot proceed without dependencies.")
        sys.exit(1)
    
    # Test conversion
    test_text = """
    Pedro es un estudiante brillante. Si Pedro es estudiante entonces estudia.
    Bob trabaja en Microsoft y es padre de Pedro. Si alguien es estudiante y vive en Madrid entonces tiene metro.
    """
    
    facts, rules = converter.convert_text(test_text, verbose=True)
    
    print("\n" + "=" * 70)
    print("EXTRACTED FACTS:")
    for fact in facts:
        print(f"  {fact}")
    
    print("\nEXTRACTED RULES:")
    for rule in rules:
        print(f"  {rule}")

