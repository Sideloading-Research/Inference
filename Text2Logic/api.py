"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    TEXT2LOGIC API - UNIFIED INTERFACE                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

Module Description:
    Unified API for Text2Logic system supporting three usage modes:
    1. Direct usage (standalone script)
    2. Internal API (between modules)
    3. Library import (for external programs)

Author: Marco
Date: October 2025
Version: 1.0
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

from typing import List, Tuple, Dict, Optional, Union
from dataclasses import dataclass
from text_to_logic import TextToLogicConverter, SystemVerifier
from logic_engine import LogicEngine, InferenceResult
from logic_parser import Atom, LogicalExpression


# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ConversionResult:
    """Result of text-to-logic conversion."""
    facts: List[str]
    rules: List[str]
    source_text: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'facts': self.facts,
            'rules': self.rules,
            'source_text': self.source_text
        }


@dataclass
class CompleteAnalysis:
    """Complete analysis result including conversion and inference."""
    conversion: ConversionResult
    inference: InferenceResult
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'conversion': self.conversion.to_dict(),
            'inference': {
                'original_facts_count': len(self.inference.original_facts),
                'original_rules_count': len(self.inference.original_rules),
                'derived_facts_count': len(self.inference.derived_facts),
                'iterations': self.inference.iterations,
                'has_contradictions': len(self.inference.contradictions) > 0
            }
        }


# ═══════════════════════════════════════════════════════════════════════════════
# MODE 1: DIRECT USAGE API
# ═══════════════════════════════════════════════════════════════════════════════

class TextToLogicProcessor:
    """
    High-level processor for direct usage.
    
    Example:
        >>> processor = TextToLogicProcessor()
        >>> processor.process_file("input.txt", "output.inf")
    """
    
    def __init__(self, model_name: str = "gemma:2b", verify_on_init: bool = True):
        """
        Initialize the processor.
        
        Args:
            model_name: Ollama model to use
            verify_on_init: Verify dependencies on initialization
        """
        self.converter = TextToLogicConverter(model_name=model_name)
        self.engine = LogicEngine()
        
        if verify_on_init:
            self.verify_system()
    
    def verify_system(self) -> bool:
        """
        Verify system dependencies.
        
        Returns:
            True if all OK, False otherwise
        """
        return self.converter.verify_dependencies()
    
    def process_file(self, input_file: str, output_file: str, 
                    perform_inference: bool = True, verbose: bool = True) -> Optional[CompleteAnalysis]:
        """
        Process a text file to logic format with optional inference.
        
        Args:
            input_file: Path to input text file
            output_file: Path to output .inf file
            perform_inference: Whether to perform inference
            verbose: Print progress
        
        Returns:
            CompleteAnalysis if perform_inference=True, None otherwise
        """
        if verbose:
            print("╔══════════════════════════════════════════════════════════════════════════════╗")
            print("║                    TEXT2LOGIC PROCESSOR                                       ║")
            print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
        
        # Convert text to logic
        if verbose:
            print("STEP 1: Converting text to logic format...")
            print("=" * 70)
        
        self.converter.convert_file(input_file, output_file, verbose=verbose)
        
        if not perform_inference:
            return None
        
        # Perform inference
        if verbose:
            print("\n\nSTEP 2: Performing logical inference...")
            print("=" * 70)
        
        self.engine.clear()
        self.engine.load_from_file(output_file)
        result = self.engine.infer_all(verbose=verbose)
        
        # Export inference results
        if verbose:
            print("\n\nSTEP 3: Exporting inference results...")
            print("=" * 70)
        
        inference_output = output_file.replace('.inf', '_inferred.txt')
        self.engine.export_results(inference_output, result)
        
        if verbose:
            print(f"✓ Inference results saved to: {inference_output}")
        
        # Read original text
        with open(input_file, 'r', encoding='utf-8') as f:
            source_text = f.read()
        
        # Read facts and rules
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            facts = []
            rules = []
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    if line.startswith('Rule:'):
                        rules.append(line)
                    else:
                        facts.append(line)
        
        conversion = ConversionResult(facts=facts, rules=rules, source_text=source_text)
        
        return CompleteAnalysis(conversion=conversion, inference=result)


# ═══════════════════════════════════════════════════════════════════════════════
# MODE 2: INTERNAL API (BETWEEN MODULES)
# ═══════════════════════════════════════════════════════════════════════════════

def convert_text(text: str, model_name: str = "gemma:2b", verbose: bool = False) -> Tuple[List[str], List[str]]:
    """
    Convert text to logic format (facts and rules).
    
    Args:
        text: Input text
        model_name: Ollama model to use
        verbose: Print progress
    
    Returns:
        Tuple of (facts, rules)
    
    Example:
        >>> facts, rules = convert_text("Pedro es estudiante")
        >>> print(facts)
        ['(Pedro)IsA(estudiante)']
    """
    converter = TextToLogicConverter(model_name=model_name)
    return converter.convert_text(text, verbose=verbose)


def deduce_all(facts: List[str], rules: List[str], verbose: bool = False) -> InferenceResult:
    """
    Perform exhaustive inference on facts and rules.
    
    Args:
        facts: List of fact strings
        rules: List of rule strings
        verbose: Print progress
    
    Returns:
        InferenceResult with all derived facts
    
    Example:
        >>> facts = ["(Pedro)IsA(estudiante)"]
        >>> rules = ["Rule: (X)IsA(estudiante) → (X)estudia"]
        >>> result = deduce_all(facts, rules)
        >>> print(len(result.derived_facts))
    """
    engine = LogicEngine()
    
    for fact in facts:
        engine.add_fact(fact)
    
    for rule in rules:
        # Remove "Rule:" prefix if present
        rule = rule.replace('Rule:', '').strip()
        engine.add_rule(rule)
    
    return engine.infer_all(verbose=verbose)


def analyze_text(text: str, model_name: str = "gemma:2b", verbose: bool = False) -> CompleteAnalysis:
    """
    Complete analysis: convert text and perform inference.
    
    Args:
        text: Input text
        model_name: Ollama model to use
        verbose: Print progress
    
    Returns:
        CompleteAnalysis with conversion and inference results
    
    Example:
        >>> analysis = analyze_text("Pedro es estudiante. Si Pedro es estudiante entonces estudia.")
        >>> print(analysis.inference.derived_facts)
    """
    # Convert
    facts, rules = convert_text(text, model_name=model_name, verbose=verbose)
    
    # Infer
    result = deduce_all(facts, rules, verbose=verbose)
    
    conversion = ConversionResult(facts=facts, rules=rules, source_text=text)
    
    return CompleteAnalysis(conversion=conversion, inference=result)


# ═══════════════════════════════════════════════════════════════════════════════
# MODE 3: LIBRARY IMPORT (FOR EXTERNAL PROGRAMS)
# ═══════════════════════════════════════════════════════════════════════════════

class LogicSystem:
    """
    High-level logic system for library usage.
    
    This provides the simplest interface for external programs.
    
    Example:
        >>> import Text2Logic as t2l
        >>> system = t2l.LogicSystem()
        >>> system.add_text("Pedro es estudiante")
        >>> system.add_rule("Si alguien es estudiante entonces estudia")
        >>> system.infer_all()
        >>> conclusions = system.get_conclusions()
        >>> print(conclusions)
    """
    
    def __init__(self, model_name: str = "gemma:2b", auto_verify: bool = False):
        """
        Initialize the logic system.
        
        Args:
            model_name: Ollama model to use
            auto_verify: Automatically verify dependencies
        """
        self.converter = TextToLogicConverter(model_name=model_name)
        self.engine = LogicEngine()
        self._inference_result = None
        
        if auto_verify:
            self.verify()
    
    def verify(self) -> bool:
        """
        Verify system dependencies.
        
        Returns:
            True if all OK
        """
        return self.converter.verify_dependencies()
    
    def add_text(self, text: str, verbose: bool = False):
        """
        Add natural language text to the system.
        
        Args:
            text: Natural language text
            verbose: Print conversion progress
        """
        facts, rules = self.converter.convert_text(text, verbose=verbose)
        
        for fact in facts:
            self.engine.add_fact(fact)
        
        for rule in rules:
            rule = rule.replace('Rule:', '').strip()
            self.engine.add_rule(rule)
    
    def add_fact(self, fact: str):
        """
        Add a fact directly (in logic notation).
        
        Args:
            fact: Fact in logic notation
        """
        self.engine.add_fact(fact)
    
    def add_rule(self, rule: str):
        """
        Add a rule directly (in logic notation).
        
        Args:
            rule: Rule in logic notation
        """
        self.engine.add_rule(rule)
    
    def infer_all(self, verbose: bool = False):
        """
        Perform exhaustive inference.
        
        Args:
            verbose: Print inference progress
        """
        self._inference_result = self.engine.infer_all(verbose=verbose)
    
    def get_conclusions(self) -> List[str]:
        """
        Get all derived conclusions.
        
        Returns:
            List of conclusion strings
        """
        if self._inference_result is None:
            return []
        
        return [str(chain.conclusion) for chain in self._inference_result.derived_facts]
    
    def get_all_facts(self) -> List[str]:
        """
        Get all facts (original + derived).
        
        Returns:
            List of all facts
        """
        if self._inference_result is None:
            return [str(f) for f in self.engine.original_facts]
        
        all_facts = self._inference_result.get_all_facts()
        return [str(f) for f in all_facts]
    
    def query(self, query: str) -> bool:
        """
        Query if a fact is known.
        
        Args:
            query: Fact to query (logic notation)
        
        Returns:
            True if fact is known
        """
        return self.engine.query(query)
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the knowledge base.
        
        Returns:
            Dictionary with statistics
        """
        if self._inference_result is None:
            return {
                'original_facts': len(self.engine.original_facts),
                'original_rules': len(self.engine.original_rules),
                'derived_facts': 0,
                'total_facts': len(self.engine.original_facts),
                'iterations': 0
            }
        
        return {
            'original_facts': len(self._inference_result.original_facts),
            'original_rules': len(self._inference_result.original_rules),
            'derived_facts': len(self._inference_result.derived_facts),
            'total_facts': len(self._inference_result.get_all_facts()),
            'iterations': self._inference_result.iterations,
            'has_contradictions': len(self._inference_result.contradictions) > 0
        }
    
    def export(self, filepath: str):
        """
        Export complete analysis to file.
        
        Args:
            filepath: Output file path
        """
        if self._inference_result is None:
            raise ValueError("No inference result available. Run infer_all() first.")
        
        self.engine.export_results(filepath, self._inference_result)
    
    def clear(self):
        """Clear all knowledge from the system."""
        self.engine.clear()
        self._inference_result = None


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION BLOCK (FOR TESTING)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    """Test all three API modes."""
    
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                    TEXT2LOGIC API - TEST ALL MODES                           ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
    
    # Mode 3 test (simplest for users)
    print("=" * 70)
    print("MODE 3: Library Usage (Recommended for external programs)")
    print("=" * 70)
    
    system = LogicSystem(model_name="gemma:2b")
    
    if not system.verify():
        print("Cannot proceed without dependencies.")
    else:
        # Add some facts directly
        system.add_fact("(Pedro)IsA(estudiante)")
        system.add_rule("(X)IsA(estudiante) → (X)estudia")
        
        # Perform inference
        system.infer_all(verbose=True)
        
        # Get results
        print("\nConclusions:")
        for conclusion in system.get_conclusions():
            print(f"  • {conclusion}")
        
        # Statistics
        print("\nStatistics:")
        stats = system.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    print("\n" + "=" * 70)
    print("API test complete!")

