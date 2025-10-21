"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    LOGIC ENGINE - EXTENDED INFERENCE ENGINE                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

Module Description:
    Extended inference engine with complete deduction capabilities.
    Performs forward chaining, backward chaining, and exhaustive inference
    until all possible conclusions are derived.

Author: Marco
Date: October 2025
Version: 1.0
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

import sys
import os

# Add parent directory to path to import engine
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Set, List, Tuple, Dict, Optional, Union
from dataclasses import dataclass, field
from logic_parser import Atom, LogicalExpression, LogicalOperator, parse_expression
from deduction_rules import RuleManager


# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class DerivationChain:
    """Represents a chain of reasoning leading to a conclusion."""
    conclusion: Union[Atom, LogicalExpression]
    justification: str
    depth: int
    premises: List[Union[Atom, LogicalExpression]] = field(default_factory=list)
    
    def __str__(self):
        return f"[Depth {self.depth}] {self.conclusion} ← {self.justification}"


@dataclass
class InferenceResult:
    """Complete result of inference process."""
    original_facts: Set[Union[Atom, LogicalExpression]]
    original_rules: Set[LogicalExpression]
    derived_facts: List[DerivationChain]
    iterations: int
    contradictions: List[str]
    
    def get_all_facts(self) -> Set:
        """Get all facts (original + derived)."""
        all_facts = self.original_facts.copy()
        for chain in self.derived_facts:
            all_facts.add(chain.conclusion)
        return all_facts
    
    def get_facts_by_depth(self) -> Dict[int, List]:
        """Group derived facts by derivation depth."""
        by_depth = {}
        for chain in self.derived_facts:
            if chain.depth not in by_depth:
                by_depth[chain.depth] = []
            by_depth[chain.depth].append(chain)
        return by_depth


# ═══════════════════════════════════════════════════════════════════════════════
# LOGIC ENGINE CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class LogicEngine:
    """
    Extended inference engine with exhaustive deduction capabilities.
    
    Features:
        - Forward chaining (data-driven inference)
        - Exhaustive inference (saturate knowledge base)
        - Contradiction detection
        - Derivation tracking for explainability
        - Configurable iteration limits
    
    Example:
        >>> engine = LogicEngine()
        >>> engine.add_fact("(Pedro)IsA(estudiante)")
        >>> engine.add_rule("(X)IsA(estudiante) → (X)estudia")
        >>> result = engine.infer_all()
        >>> print(result.derived_facts)
    """
    
    def __init__(self, max_iterations: int = 100, enable_conjunction: bool = False):
        """
        Initialize the logic engine.
        
        Args:
            max_iterations: Maximum number of inference iterations
            enable_conjunction: Enable conjunction rule (can be expensive)
        """
        self.knowledge_base: Set[Union[Atom, LogicalExpression]] = set()
        self.original_facts: Set[Union[Atom, LogicalExpression]] = set()
        self.original_rules: Set[LogicalExpression] = set()
        self.derivation_chains: List[DerivationChain] = []
        self.max_iterations = max_iterations
        self.rule_manager = RuleManager(enable_conjunction=enable_conjunction)
        self.contradictions: List[str] = []
    
    def clear(self):
        """Clear all knowledge from the engine."""
        self.knowledge_base.clear()
        self.original_facts.clear()
        self.original_rules.clear()
        self.derivation_chains.clear()
        self.contradictions.clear()
    
    def add_fact(self, fact: Union[str, Atom, LogicalExpression]):
        """
        Add a fact to the knowledge base.
        
        Args:
            fact: Fact as string or parsed expression
        """
        if isinstance(fact, str):
            fact = parse_expression(fact)
        
        self.knowledge_base.add(fact)
        self.original_facts.add(fact)
    
    def add_rule(self, rule: Union[str, LogicalExpression]):
        """
        Add a rule to the knowledge base.
        
        Args:
            rule: Rule as string or parsed expression (should be implication)
        """
        if isinstance(rule, str):
            rule = parse_expression(rule)
        
        self.knowledge_base.add(rule)
        
        # Track as rule if it's an implication or biconditional
        if isinstance(rule, LogicalExpression) and rule.operator in [
            LogicalOperator.IMPLIES, LogicalOperator.IFF
        ]:
            self.original_rules.add(rule)
        else:
            self.original_facts.add(rule)
    
    def load_from_file(self, filepath: str):
        """
        Load facts and rules from a .inf file.
        
        Args:
            filepath: Path to the .inf file
        """
        encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
        
        content = None
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except (UnicodeDecodeError, FileNotFoundError):
                continue
        
        if content is None:
            raise ValueError(f"Could not read file: {filepath}")
        
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Remove inline comments
            if '#' in line:
                line = line.split('#')[0].strip()
            
            try:
                # Check if it's a rule (starts with "Rule:")
                if line.startswith('Rule:'):
                    rule_text = line[5:].strip()
                    self.add_rule(rule_text)
                else:
                    # It's a fact
                    self.add_fact(line)
            except Exception as e:
                print(f"Warning: Could not parse line: {line}")
                print(f"  Error: {e}")
    
    def infer_all(self, verbose: bool = False) -> InferenceResult:
        """
        Perform exhaustive inference until no new facts can be derived.
        
        This implements forward chaining with saturation:
        1. Apply all inference rules to current knowledge base
        2. Add newly derived facts to knowledge base
        3. Repeat until no new facts are derived or max iterations reached
        
        Args:
            verbose: If True, print progress information
        
        Returns:
            InferenceResult containing all derived facts and metadata
        """
        if verbose:
            print("╔══════════════════════════════════════════════════════════════════════════════╗")
            print("║                    EXHAUSTIVE INFERENCE - FORWARD CHAINING                   ║")
            print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
            print(f"Initial facts: {len(self.original_facts)}")
            print(f"Initial rules: {len(self.original_rules)}")
            print(f"Active inference rules: {', '.join(self.rule_manager.get_rule_names())}")
            print("\n" + "=" * 70)
        
        iteration = 0
        total_derived = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            
            if verbose:
                print(f"\nIteration {iteration}:")
                print(f"  Knowledge base size: {len(self.knowledge_base)}")
            
            # Apply all inference rules
            derived = self.rule_manager.apply_all_rules(self.knowledge_base)
            
            if not derived:
                if verbose:
                    print(f"  No new facts derived. Inference complete.")
                break
            
            # Add derived facts to knowledge base and track derivations
            for fact, justification in derived:
                self.knowledge_base.add(fact)
                chain = DerivationChain(
                    conclusion=fact,
                    justification=justification,
                    depth=iteration
                )
                self.derivation_chains.append(chain)
                total_derived += 1
                
                if verbose:
                    print(f"  ✓ {fact}")
            
            if verbose:
                print(f"  Derived {len(derived)} new facts in this iteration")
        
        # Check for contradictions
        self._detect_contradictions()
        
        if verbose:
            print("\n" + "=" * 70)
            print(f"\nInference complete after {iteration} iterations")
            print(f"Total facts derived: {total_derived}")
            print(f"Final knowledge base size: {len(self.knowledge_base)}")
            
            if self.contradictions:
                print(f"\n⚠️  Contradictions detected: {len(self.contradictions)}")
                for contradiction in self.contradictions:
                    print(f"  • {contradiction}")
        
        return InferenceResult(
            original_facts=self.original_facts.copy(),
            original_rules=self.original_rules.copy(),
            derived_facts=self.derivation_chains.copy(),
            iterations=iteration,
            contradictions=self.contradictions.copy()
        )
    
    def _detect_contradictions(self):
        """Detect logical contradictions in the knowledge base."""
        self.contradictions.clear()
        
        # Look for P and ¬P
        atoms = {item for item in self.knowledge_base if isinstance(item, Atom)}
        negations = {item for item in self.knowledge_base 
                    if isinstance(item, LogicalExpression) and 
                    item.operator == LogicalOperator.NOT}
        
        for neg in negations:
            negated_expr = neg.operands[0]
            if negated_expr in atoms:
                self.contradictions.append(
                    f"Contradiction: {negated_expr} and {neg} both present"
                )
    
    def query(self, query: Union[str, Atom, LogicalExpression]) -> bool:
        """
        Query if a fact is in the knowledge base (after inference).
        
        Args:
            query: Fact to check
        
        Returns:
            True if fact is in knowledge base, False otherwise
        """
        if isinstance(query, str):
            query = parse_expression(query)
        
        return query in self.knowledge_base
    
    def get_derivation_chain(self, fact: Union[str, Atom, LogicalExpression]) -> Optional[DerivationChain]:
        """
        Get the derivation chain for a specific fact.
        
        Args:
            fact: Fact to get derivation for
        
        Returns:
            DerivationChain if fact was derived, None otherwise
        """
        if isinstance(fact, str):
            fact = parse_expression(fact)
        
        for chain in self.derivation_chains:
            if chain.conclusion == fact:
                return chain
        
        return None
    
    def export_results(self, filepath: str, result: InferenceResult):
        """
        Export inference results to a file.
        
        Args:
            filepath: Path to output file
            result: InferenceResult to export
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("╔══════════════════════════════════════════════════════════════════════════════╗\n")
            f.write("║                    INFERENCE RESULTS - LOGIC ENGINE                          ║\n")
            f.write("╚══════════════════════════════════════════════════════════════════════════════╝\n\n")
            
            # Original facts
            f.write("═" * 70 + "\n")
            f.write("ORIGINAL FACTS\n")
            f.write("═" * 70 + "\n")
            for fact in sorted(result.original_facts, key=str):
                if fact not in result.original_rules:
                    f.write(f"{fact}\n")
            f.write("\n")
            
            # Original rules
            f.write("═" * 70 + "\n")
            f.write("ORIGINAL RULES\n")
            f.write("═" * 70 + "\n")
            for rule in sorted(result.original_rules, key=str):
                f.write(f"{rule}\n")
            f.write("\n")
            
            # Derived facts by depth
            f.write("═" * 70 + "\n")
            f.write("DERIVED FACTS (BY INFERENCE DEPTH)\n")
            f.write("═" * 70 + "\n")
            
            by_depth = result.get_facts_by_depth()
            for depth in sorted(by_depth.keys()):
                f.write(f"\n--- Depth {depth} ---\n")
                for chain in by_depth[depth]:
                    f.write(f"{chain.conclusion}\n")
                    f.write(f"  ← {chain.justification}\n")
            
            f.write("\n")
            
            # Summary
            f.write("═" * 70 + "\n")
            f.write("SUMMARY\n")
            f.write("═" * 70 + "\n")
            f.write(f"Original facts: {len(result.original_facts) - len(result.original_rules)}\n")
            f.write(f"Original rules: {len(result.original_rules)}\n")
            f.write(f"Derived facts: {len(result.derived_facts)}\n")
            f.write(f"Total facts: {len(result.get_all_facts())}\n")
            f.write(f"Iterations: {result.iterations}\n")
            
            # Contradictions
            if result.contradictions:
                f.write("\n")
                f.write("═" * 70 + "\n")
                f.write("⚠️  CONTRADICTIONS DETECTED\n")
                f.write("═" * 70 + "\n")
                for contradiction in result.contradictions:
                    f.write(f"{contradiction}\n")
            
            f.write("\n" + "═" * 70 + "\n")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION BLOCK (FOR TESTING)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    """Test the logic engine."""
    
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                    LOGIC ENGINE - TEST SUITE                                 ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
    
    # Create engine
    engine = LogicEngine(max_iterations=10)
    
    # Add facts
    print("Adding facts:")
    engine.add_fact("(Pedro)IsA(estudiante)")
    engine.add_fact("(Pedro)ViveEn(Madrid)")
    print("  ✓ (Pedro)IsA(estudiante)")
    print("  ✓ (Pedro)ViveEn(Madrid)")
    
    # Add rules
    print("\nAdding rules:")
    engine.add_rule("(X)IsA(estudiante) → (X)estudia")
    engine.add_rule("(X)estudia → (X)aprende")
    engine.add_rule("(X)IsA(estudiante) ∧ (X)ViveEn(Madrid) → (X)TieneMetro")
    print("  ✓ (X)IsA(estudiante) → (X)estudia")
    print("  ✓ (X)estudia → (X)aprende")
    print("  ✓ (X)IsA(estudiante) ∧ (X)ViveEn(Madrid) → (X)TieneMetro")
    
    # Perform inference
    print("\n" + "=" * 70)
    result = engine.infer_all(verbose=True)
    
    # Export results
    print("\n" + "=" * 70)
    print("Exporting results to 'test_logic_engine_results.txt'...")
    engine.export_results("test_logic_engine_results.txt", result)
    print("✓ Export complete")

