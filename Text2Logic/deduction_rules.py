"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DEDUCTION RULES - INFERENCE RULES                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

Module Description:
    Implementation of formal logic inference rules for automated deduction.
    Supports classical propositional and first-order logic rules.

Author: Marco
Date: October 2025
Version: 1.0
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

from typing import List, Set, Tuple, Optional
from logic_parser import Atom, LogicalExpression, LogicalOperator


# ═══════════════════════════════════════════════════════════════════════════════
# DEDUCTION RULE BASE CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class DeductionRule:
    """Base class for all deduction rules."""
    
    def __init__(self, name: str, priority: int = 5):
        """
        Initialize a deduction rule.
        
        Args:
            name: Name of the rule (e.g., "Modus Ponens")
            priority: Priority for rule application (1-10, higher = more priority)
        """
        self.name = name
        self.priority = priority
    
    def apply(self, knowledge_base: Set, new_facts: Set) -> List[Tuple]:
        """
        Apply this rule to the knowledge base.
        
        Args:
            knowledge_base: Set of known facts and rules
            new_facts: Set to collect newly derived facts
        
        Returns:
            List of tuples: (new_fact, justification)
        """
        raise NotImplementedError("Subclasses must implement apply()")
    
    def __repr__(self):
        return f"{self.name} (priority: {self.priority})"


# ═══════════════════════════════════════════════════════════════════════════════
# RULE 1: MODUS PONENS
# ═══════════════════════════════════════════════════════════════════════════════

class ModusPonens(DeductionRule):
    """
    Modus Ponens: If A → B and A, then B
    
    Example:
        Given: (Pedro)IsA(estudiante) → (Pedro)estudia
        Given: (Pedro)IsA(estudiante)
        Infer: (Pedro)estudia
    """
    
    def __init__(self):
        super().__init__("Modus Ponens", priority=10)
    
    def apply(self, knowledge_base: Set, new_facts: Set) -> List[Tuple]:
        """Apply Modus Ponens rule."""
        derived = []
        
        # Find all implications in knowledge base
        implications = [item for item in knowledge_base 
                       if isinstance(item, LogicalExpression) and 
                       item.operator == LogicalOperator.IMPLIES]
        
        # Find all facts in knowledge base
        facts = [item for item in knowledge_base 
                if isinstance(item, Atom) or 
                (isinstance(item, LogicalExpression) and 
                 item.operator != LogicalOperator.IMPLIES)]
        
        for impl in implications:
            antecedent = impl.operands[0]
            consequent = impl.operands[1]
            
            # Check if antecedent is in facts
            for fact in facts:
                if self._match(antecedent, fact):
                    # Apply substitution if there are variables
                    if isinstance(antecedent, Atom) and isinstance(fact, Atom):
                        matches, bindings = antecedent.matches(fact)
                        if matches:
                            # Substitute in consequent
                            new_fact = self._substitute(consequent, bindings)
                            if new_fact not in knowledge_base and new_fact not in new_facts:
                                justification = f"Modus Ponens: {fact} ∧ ({impl}) ⊢ {new_fact}"
                                derived.append((new_fact, justification))
                                new_facts.add(new_fact)
                    elif self._equals(antecedent, fact):
                        if consequent not in knowledge_base and consequent not in new_facts:
                            justification = f"Modus Ponens: {fact} ∧ ({impl}) ⊢ {consequent}"
                            derived.append((consequent, justification))
                            new_facts.add(consequent)
        
        return derived
    
    def _match(self, expr1, expr2) -> bool:
        """Check if two expressions match."""
        if isinstance(expr1, Atom) and isinstance(expr2, Atom):
            matches, _ = expr1.matches(expr2)
            return matches
        return self._equals(expr1, expr2)
    
    def _equals(self, expr1, expr2) -> bool:
        """Check if two expressions are equal."""
        return expr1 == expr2
    
    def _substitute(self, expr, bindings: dict):
        """Substitute variables in expression."""
        if isinstance(expr, Atom):
            return expr.substitute(bindings)
        elif isinstance(expr, LogicalExpression):
            new_operands = [self._substitute(op, bindings) for op in expr.operands]
            return LogicalExpression(expr.operator, new_operands)
        return expr


# ═══════════════════════════════════════════════════════════════════════════════
# RULE 2: MODUS TOLLENS
# ═══════════════════════════════════════════════════════════════════════════════

class ModusTollens(DeductionRule):
    """
    Modus Tollens: If A → B and ¬B, then ¬A
    
    Example:
        Given: (X)IsA(estudiante) → (X)estudia
        Given: ¬(Pedro)estudia
        Infer: ¬(Pedro)IsA(estudiante)
    """
    
    def __init__(self):
        super().__init__("Modus Tollens", priority=9)
    
    def apply(self, knowledge_base: Set, new_facts: Set) -> List[Tuple]:
        """Apply Modus Tollens rule."""
        derived = []
        
        # Find all implications
        implications = [item for item in knowledge_base 
                       if isinstance(item, LogicalExpression) and 
                       item.operator == LogicalOperator.IMPLIES]
        
        # Find all negations
        negations = [item for item in knowledge_base 
                    if isinstance(item, LogicalExpression) and 
                    item.operator == LogicalOperator.NOT]
        
        for impl in implications:
            antecedent = impl.operands[0]
            consequent = impl.operands[1]
            
            for neg in negations:
                negated_expr = neg.operands[0]
                
                # Check if negated expression matches consequent
                if self._match(consequent, negated_expr):
                    # Create negation of antecedent
                    new_fact = LogicalExpression(LogicalOperator.NOT, [antecedent])
                    
                    if new_fact not in knowledge_base and new_fact not in new_facts:
                        justification = f"Modus Tollens: {neg} ∧ ({impl}) ⊢ {new_fact}"
                        derived.append((new_fact, justification))
                        new_facts.add(new_fact)
        
        return derived
    
    def _match(self, expr1, expr2) -> bool:
        """Check if two expressions match."""
        if isinstance(expr1, Atom) and isinstance(expr2, Atom):
            matches, _ = expr1.matches(expr2)
            return matches
        return expr1 == expr2


# ═══════════════════════════════════════════════════════════════════════════════
# RULE 3: HYPOTHETICAL SYLLOGISM
# ═══════════════════════════════════════════════════════════════════════════════

class HypotheticalSyllogism(DeductionRule):
    """
    Hypothetical Syllogism: If A → B and B → C, then A → C
    
    Example:
        Given: (X)IsA(estudiante) → (X)estudia
        Given: (X)estudia → (X)aprende
        Infer: (X)IsA(estudiante) → (X)aprende
    """
    
    def __init__(self):
        super().__init__("Hypothetical Syllogism", priority=7)
    
    def apply(self, knowledge_base: Set, new_facts: Set) -> List[Tuple]:
        """Apply Hypothetical Syllogism."""
        derived = []
        
        implications = [item for item in knowledge_base 
                       if isinstance(item, LogicalExpression) and 
                       item.operator == LogicalOperator.IMPLIES]
        
        for impl1 in implications:
            for impl2 in implications:
                if impl1 == impl2:
                    continue
                
                # Check if consequent of impl1 matches antecedent of impl2
                if impl1.operands[1] == impl2.operands[0]:
                    # Create A → C
                    new_fact = LogicalExpression(
                        LogicalOperator.IMPLIES,
                        [impl1.operands[0], impl2.operands[1]]
                    )
                    
                    if new_fact not in knowledge_base and new_fact not in new_facts:
                        justification = f"Hypothetical Syllogism: ({impl1}) ∧ ({impl2}) ⊢ {new_fact}"
                        derived.append((new_fact, justification))
                        new_facts.add(new_fact)
        
        return derived


# ═══════════════════════════════════════════════════════════════════════════════
# RULE 4: DISJUNCTIVE SYLLOGISM
# ═══════════════════════════════════════════════════════════════════════════════

class DisjunctiveSyllogism(DeductionRule):
    """
    Disjunctive Syllogism: If A ∨ B and ¬A, then B
    
    Example:
        Given: (Pedro)Feliz ∨ (Pedro)Triste
        Given: ¬(Pedro)Feliz
        Infer: (Pedro)Triste
    """
    
    def __init__(self):
        super().__init__("Disjunctive Syllogism", priority=8)
    
    def apply(self, knowledge_base: Set, new_facts: Set) -> List[Tuple]:
        """Apply Disjunctive Syllogism."""
        derived = []
        
        # Find all disjunctions
        disjunctions = [item for item in knowledge_base 
                       if isinstance(item, LogicalExpression) and 
                       item.operator == LogicalOperator.OR]
        
        # Find all negations
        negations = [item for item in knowledge_base 
                    if isinstance(item, LogicalExpression) and 
                    item.operator == LogicalOperator.NOT]
        
        for disj in disjunctions:
            for neg in negations:
                negated_expr = neg.operands[0]
                
                # Check if negated expression is in disjunction
                for i, operand in enumerate(disj.operands):
                    if operand == negated_expr:
                        # Infer the other disjuncts
                        for j, other in enumerate(disj.operands):
                            if i != j:
                                if other not in knowledge_base and other not in new_facts:
                                    justification = f"Disjunctive Syllogism: ({disj}) ∧ {neg} ⊢ {other}"
                                    derived.append((other, justification))
                                    new_facts.add(other)
        
        return derived


# ═══════════════════════════════════════════════════════════════════════════════
# RULE 5: SIMPLIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

class Simplification(DeductionRule):
    """
    Simplification: If A ∧ B, then A (and also B)
    
    Example:
        Given: (Pedro)IsA(estudiante) ∧ (Pedro)ViveEn(Madrid)
        Infer: (Pedro)IsA(estudiante)
        Infer: (Pedro)ViveEn(Madrid)
    """
    
    def __init__(self):
        super().__init__("Simplification", priority=10)
    
    def apply(self, knowledge_base: Set, new_facts: Set) -> List[Tuple]:
        """Apply Simplification."""
        derived = []
        
        # Find all conjunctions
        conjunctions = [item for item in knowledge_base 
                       if isinstance(item, LogicalExpression) and 
                       item.operator == LogicalOperator.AND]
        
        for conj in conjunctions:
            for operand in conj.operands:
                if operand not in knowledge_base and operand not in new_facts:
                    justification = f"Simplification: ({conj}) ⊢ {operand}"
                    derived.append((operand, justification))
                    new_facts.add(operand)
        
        return derived


# ═══════════════════════════════════════════════════════════════════════════════
# RULE 6: CONJUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

class Conjunction(DeductionRule):
    """
    Conjunction: If A and B, then A ∧ B
    
    Example:
        Given: (Pedro)IsA(estudiante)
        Given: (Pedro)ViveEn(Madrid)
        Infer: (Pedro)IsA(estudiante) ∧ (Pedro)ViveEn(Madrid)
    """
    
    def __init__(self):
        super().__init__("Conjunction", priority=3)
    
    def apply(self, knowledge_base: Set, new_facts: Set) -> List[Tuple]:
        """Apply Conjunction."""
        derived = []
        
        # Get all atomic facts
        facts = [item for item in knowledge_base if isinstance(item, Atom)]
        
        # Limit to avoid combinatorial explosion
        if len(facts) > 20:
            return derived
        
        # Create conjunctions of pairs
        for i, fact1 in enumerate(facts):
            for fact2 in facts[i+1:]:
                new_fact = LogicalExpression(LogicalOperator.AND, [fact1, fact2])
                
                if new_fact not in knowledge_base and new_fact not in new_facts:
                    justification = f"Conjunction: {fact1} ∧ {fact2} ⊢ {new_fact}"
                    derived.append((new_fact, justification))
                    new_facts.add(new_fact)
        
        return derived


# ═══════════════════════════════════════════════════════════════════════════════
# RULE 7: ADDITION
# ═══════════════════════════════════════════════════════════════════════════════

class Addition(DeductionRule):
    """
    Addition: If A, then A ∨ B (for any B)
    
    Note: This rule is disabled by default as it creates infinite possibilities.
    """
    
    def __init__(self):
        super().__init__("Addition", priority=1)
    
    def apply(self, knowledge_base: Set, new_facts: Set) -> List[Tuple]:
        """Apply Addition (disabled to avoid explosion)."""
        # This rule is typically not applied automatically
        # as it generates infinite disjunctions
        return []


# ═══════════════════════════════════════════════════════════════════════════════
# RULE 8: RESOLUTION
# ═══════════════════════════════════════════════════════════════════════════════

class Resolution(DeductionRule):
    """
    Resolution: If (¬A ∨ B) and (A ∨ C), then (B ∨ C)
    
    This is the fundamental rule used in automated theorem proving.
    """
    
    def __init__(self):
        super().__init__("Resolution", priority=6)
    
    def apply(self, knowledge_base: Set, new_facts: Set) -> List[Tuple]:
        """Apply Resolution."""
        derived = []
        
        # Find all disjunctions
        disjunctions = [item for item in knowledge_base 
                       if isinstance(item, LogicalExpression) and 
                       item.operator == LogicalOperator.OR]
        
        for disj1 in disjunctions:
            for disj2 in disjunctions:
                if disj1 == disj2:
                    continue
                
                # Look for complementary literals
                for op1 in disj1.operands:
                    for op2 in disj2.operands:
                        # Check if op1 is ¬op2 or op2 is ¬op1
                        if self._are_complementary(op1, op2):
                            # Create resolvent
                            remaining1 = [op for op in disj1.operands if op != op1]
                            remaining2 = [op for op in disj2.operands if op != op2]
                            
                            if not remaining1 and not remaining2:
                                # Empty clause - contradiction
                                continue
                            
                            all_remaining = remaining1 + remaining2
                            
                            if len(all_remaining) == 1:
                                new_fact = all_remaining[0]
                            else:
                                new_fact = LogicalExpression(LogicalOperator.OR, all_remaining)
                            
                            if new_fact not in knowledge_base and new_fact not in new_facts:
                                justification = f"Resolution: ({disj1}) ∧ ({disj2}) ⊢ {new_fact}"
                                derived.append((new_fact, justification))
                                new_facts.add(new_fact)
        
        return derived
    
    def _are_complementary(self, expr1, expr2) -> bool:
        """Check if two expressions are complementary (one is negation of other)."""
        if isinstance(expr1, LogicalExpression) and expr1.operator == LogicalOperator.NOT:
            return expr1.operands[0] == expr2
        if isinstance(expr2, LogicalExpression) and expr2.operator == LogicalOperator.NOT:
            return expr2.operands[0] == expr1
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# RULE 9: BICONDITIONAL ELIMINATION
# ═══════════════════════════════════════════════════════════════════════════════

class BiconditionalElimination(DeductionRule):
    """
    Biconditional Elimination: If A ↔ B, then (A → B) ∧ (B → A)
    
    Example:
        Given: (X)EsMamifero ↔ (X)TienePelo
        Infer: (X)EsMamifero → (X)TienePelo
        Infer: (X)TienePelo → (X)EsMamifero
    """
    
    def __init__(self):
        super().__init__("Biconditional Elimination", priority=9)
    
    def apply(self, knowledge_base: Set, new_facts: Set) -> List[Tuple]:
        """Apply Biconditional Elimination."""
        derived = []
        
        # Find all biconditionals
        biconditionals = [item for item in knowledge_base 
                         if isinstance(item, LogicalExpression) and 
                         item.operator == LogicalOperator.IFF]
        
        for iff in biconditionals:
            left = iff.operands[0]
            right = iff.operands[1]
            
            # Create A → B
            impl1 = LogicalExpression(LogicalOperator.IMPLIES, [left, right])
            if impl1 not in knowledge_base and impl1 not in new_facts:
                justification = f"Biconditional Elimination: ({iff}) ⊢ {impl1}"
                derived.append((impl1, justification))
                new_facts.add(impl1)
            
            # Create B → A
            impl2 = LogicalExpression(LogicalOperator.IMPLIES, [right, left])
            if impl2 not in knowledge_base and impl2 not in new_facts:
                justification = f"Biconditional Elimination: ({iff}) ⊢ {impl2}"
                derived.append((impl2, justification))
                new_facts.add(impl2)
        
        return derived


# ═══════════════════════════════════════════════════════════════════════════════
# RULE MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

class RuleManager:
    """Manages and applies all deduction rules."""
    
    def __init__(self, enable_conjunction: bool = False):
        """
        Initialize the rule manager.
        
        Args:
            enable_conjunction: Whether to enable conjunction rule (can be expensive)
        """
        self.rules = [
            ModusPonens(),
            ModusTollens(),
            HypotheticalSyllogism(),
            DisjunctiveSyllogism(),
            Simplification(),
            Resolution(),
            BiconditionalElimination(),
        ]
        
        if enable_conjunction:
            self.rules.append(Conjunction())
        
        # Sort by priority (highest first)
        self.rules.sort(key=lambda r: r.priority, reverse=True)
    
    def apply_all_rules(self, knowledge_base: Set) -> List[Tuple]:
        """
        Apply all rules to the knowledge base.
        
        Args:
            knowledge_base: Set of known facts and rules
        
        Returns:
            List of tuples: (new_fact, justification)
        """
        new_facts = set()
        all_derived = []
        
        for rule in self.rules:
            derived = rule.apply(knowledge_base, new_facts)
            all_derived.extend(derived)
        
        return all_derived
    
    def get_rule_names(self) -> List[str]:
        """Get names of all active rules."""
        return [rule.name for rule in self.rules]


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION BLOCK (FOR TESTING)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    """Test the deduction rules."""
    from logic_parser import parse_expression
    
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                    DEDUCTION RULES - TEST SUITE                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
    
    # Test Modus Ponens
    print("Testing Modus Ponens:")
    kb = {
        parse_expression("(Pedro)IsA(estudiante) → (Pedro)estudia"),
        parse_expression("(Pedro)IsA(estudiante)")
    }
    
    mp = ModusPonens()
    new_facts = set()
    results = mp.apply(kb, new_facts)
    
    for fact, justification in results:
        print(f"  Derived: {fact}")
        print(f"  Justification: {justification}")
    
    print("\n" + "-" * 70)

