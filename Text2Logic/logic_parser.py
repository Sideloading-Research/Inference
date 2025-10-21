"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    LOGIC PARSER - FORMAL LOGIC EXPRESSIONS                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

Module Description:
    Parser for formal logic expressions with support for logical operators.
    Handles precedence, validation, and conversion to Abstract Syntax Tree (AST).

Author: Marco
Date: October 2025
Version: 1.0
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

import re
from typing import Union, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


# ═══════════════════════════════════════════════════════════════════════════════
# OPERATOR DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

class LogicalOperator(Enum):
    """Enumeration of logical operators with their symbols."""
    AND = "∧"
    OR = "∨"
    NOT = "¬"
    IMPLIES = "→"
    IFF = "↔"
    
    @classmethod
    def from_text(cls, text: str) -> Optional['LogicalOperator']:
        """Convert text representation to operator."""
        mapping = {
            '∧': cls.AND, 'AND': cls.AND, '&': cls.AND, '^': cls.AND,
            '∨': cls.OR, 'OR': cls.OR, '|': cls.OR, 'v': cls.OR,
            '¬': cls.NOT, 'NOT': cls.NOT, '~': cls.NOT, '!': cls.NOT,
            '→': cls.IMPLIES, 'IMPLIES': cls.IMPLIES, '->': cls.IMPLIES, '=>': cls.IMPLIES,
            '↔': cls.IFF, 'IFF': cls.IFF, '<->': cls.IFF, '<=>': cls.IFF
        }
        return mapping.get(text.upper() if isinstance(text, str) else text)


# ═══════════════════════════════════════════════════════════════════════════════
# AST NODE CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Atom:
    """Represents an atomic proposition: (Subject)Relation(Object)"""
    subject: str
    relation: str
    objects: List[str]
    
    def __str__(self):
        if not self.objects:
            return f"({self.subject}){self.relation}()"
        return f"({self.subject}){self.relation}({', '.join(self.objects)})"
    
    def __hash__(self):
        return hash((self.subject, self.relation, tuple(self.objects)))
    
    def __eq__(self, other):
        if not isinstance(other, Atom):
            return False
        return (self.subject == other.subject and 
                self.relation == other.relation and 
                self.objects == other.objects)
    
    def matches(self, other: 'Atom', bindings: dict = None) -> Tuple[bool, dict]:
        """
        Check if this atom matches another, supporting variable unification.
        Variables start with 'X', 'Y', 'Z' or end with numbers like X1, Y2.
        """
        if bindings is None:
            bindings = {}
        
        new_bindings = bindings.copy()
        
        # Relations must match exactly
        if self.relation != other.relation:
            return False, {}
        
        # Match subject
        if not self._match_term(self.subject, other.subject, new_bindings):
            return False, {}
        
        # Match objects (must have same arity)
        if len(self.objects) != len(other.objects):
            return False, {}
        
        for obj1, obj2 in zip(self.objects, other.objects):
            if not self._match_term(obj1, obj2, new_bindings):
                return False, {}
        
        return True, new_bindings
    
    def _match_term(self, term1: str, term2: str, bindings: dict) -> bool:
        """Match two terms, handling variables."""
        is_var1 = self._is_variable(term1)
        is_var2 = self._is_variable(term2)
        
        if not is_var1 and not is_var2:
            # Both constants - must be equal
            return term1 == term2
        
        if is_var1:
            if term1 in bindings:
                # Variable already bound
                return bindings[term1] == term2
            else:
                # Bind variable
                bindings[term1] = term2
                return True
        
        if is_var2:
            if term2 in bindings:
                return bindings[term2] == term1
            else:
                bindings[term2] = term1
                return True
        
        return False
    
    def _is_variable(self, term: str) -> bool:
        """Check if a term is a variable."""
        return (term.startswith('X') or term.startswith('Y') or 
                term.startswith('Z') or 
                re.match(r'^[XYZ]\d+$', term) is not None)
    
    def substitute(self, bindings: dict) -> 'Atom':
        """Create a new atom with variables substituted."""
        new_subject = bindings.get(self.subject, self.subject)
        new_objects = [bindings.get(obj, obj) for obj in self.objects]
        return Atom(new_subject, self.relation, new_objects)


@dataclass
class LogicalExpression:
    """Represents a logical expression with operators."""
    operator: Optional[LogicalOperator]
    operands: List[Union[Atom, 'LogicalExpression']]
    
    def __str__(self):
        if self.operator is None:
            # Single atom
            return str(self.operands[0]) if self.operands else ""
        
        if self.operator == LogicalOperator.NOT:
            return f"¬{self.operands[0]}"
        
        op_symbol = self.operator.value
        operand_strs = [str(op) for op in self.operands]
        return f"({' {} '.format(op_symbol).join(operand_strs)})"
    
    def __hash__(self):
        return hash((self.operator, tuple(self.operands)))
    
    def __eq__(self, other):
        if not isinstance(other, LogicalExpression):
            return False
        return (self.operator == other.operator and 
                self.operands == other.operands)


# ═══════════════════════════════════════════════════════════════════════════════
# PARSER CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class LogicParser:
    """
    Parser for formal logic expressions.
    
    Supports:
        - Atoms: (Subject)Relation(Object)
        - Logical operators: ∧ (AND), ∨ (OR), ¬ (NOT), → (IMPLIES), ↔ (IFF)
        - Precedence: NOT > AND > OR > IMPLIES > IFF
        - Parentheses for grouping
    
    Example:
        >>> parser = LogicParser()
        >>> expr = parser.parse("(Pedro)IsA(estudiante) → (Pedro)estudia")
        >>> print(expr)
    """
    
    def __init__(self):
        """Initialize the parser."""
        self.tokens = []
        self.position = 0
    
    def parse(self, text: str) -> Union[Atom, LogicalExpression]:
        """
        Parse a logical expression from text.
        
        Args:
            text: String containing the logical expression
        
        Returns:
            Atom or LogicalExpression representing the parsed expression
        
        Raises:
            ValueError: If the expression is malformed
        """
        text = text.strip()
        self.tokens = self._tokenize(text)
        self.position = 0
        
        if not self.tokens:
            raise ValueError("Empty expression")
        
        result = self._parse_iff()
        
        if self.position < len(self.tokens):
            raise ValueError(f"Unexpected token: {self.tokens[self.position]}")
        
        return result
    
    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize the input text into atoms and operators.
        
        Returns list of tokens in order.
        """
        tokens = []
        i = 0
        
        while i < len(text):
            # Skip whitespace
            if text[i].isspace():
                i += 1
                continue
            
            # Check for atoms first: (Subject)Relation(Object)
            atom_match = re.match(
                r'\([^)]+\)[A-Za-z_][A-Za-z0-9_]*\([^)]*\)',
                text[i:]
            )
            if atom_match:
                tokens.append(atom_match.group(0))
                i += len(atom_match.group(0))
                continue
            
            # Check for multi-character operators
            if i + 1 < len(text):
                two_char = text[i:i+2]
                if two_char in ['→', '↔', '->', '=>', '<->',  '<=>']: 
                    if two_char == '->':
                        tokens.append('→')
                    elif two_char == '=>':
                        tokens.append('→')
                    elif two_char == '<->':
                        tokens.append('↔')
                    elif two_char == '<=>':
                        tokens.append('↔')
                    else:
                        tokens.append(two_char)
                    i += 2
                    continue
            
            # Check for single-character operators and symbols
            if text[i] in ['∧', '∨', '¬', '→', '↔', '&', '|', '~', '!', '^', 'v']:
                char = text[i]
                # Normalize symbols
                if char == '&' or char == '^':
                    tokens.append('∧')
                elif char == '|' or char == 'v':
                    tokens.append('∨')
                elif char == '~' or char == '!':
                    tokens.append('¬')
                else:
                    tokens.append(char)
                i += 1
                continue
            
            # Unknown character
            raise ValueError(f"Unexpected character: {text[i]} at position {i}")
        
        return tokens
    
    def _parse_iff(self) -> Union[Atom, LogicalExpression]:
        """Parse IFF (biconditional) - lowest precedence."""
        left = self._parse_implies()
        
        while self.position < len(self.tokens) and self.tokens[self.position] == '↔':
            self.position += 1
            right = self._parse_implies()
            left = LogicalExpression(LogicalOperator.IFF, [left, right])
        
        return left
    
    def _parse_implies(self) -> Union[Atom, LogicalExpression]:
        """Parse IMPLIES (implication)."""
        left = self._parse_or()
        
        while self.position < len(self.tokens) and self.tokens[self.position] == '→':
            self.position += 1
            right = self._parse_or()
            left = LogicalExpression(LogicalOperator.IMPLIES, [left, right])
        
        return left
    
    def _parse_or(self) -> Union[Atom, LogicalExpression]:
        """Parse OR (disjunction)."""
        left = self._parse_and()
        
        operands = [left]
        while self.position < len(self.tokens) and self.tokens[self.position] == '∨':
            self.position += 1
            operands.append(self._parse_and())
        
        if len(operands) == 1:
            return operands[0]
        return LogicalExpression(LogicalOperator.OR, operands)
    
    def _parse_and(self) -> Union[Atom, LogicalExpression]:
        """Parse AND (conjunction)."""
        left = self._parse_not()
        
        operands = [left]
        while self.position < len(self.tokens) and self.tokens[self.position] == '∧':
            self.position += 1
            operands.append(self._parse_not())
        
        if len(operands) == 1:
            return operands[0]
        return LogicalExpression(LogicalOperator.AND, operands)
    
    def _parse_not(self) -> Union[Atom, LogicalExpression]:
        """Parse NOT (negation) - highest precedence."""
        if self.position < len(self.tokens) and self.tokens[self.position] == '¬':
            self.position += 1
            operand = self._parse_not()
            return LogicalExpression(LogicalOperator.NOT, [operand])
        
        return self._parse_atom()
    
    def _parse_atom(self) -> Atom:
        """Parse an atomic proposition."""
        if self.position >= len(self.tokens):
            raise ValueError("Unexpected end of expression")
        
        token = self.tokens[self.position]
        self.position += 1
        
        # Parse atom format: (Subject)Relation(Object)
        match = re.match(r'\(([^)]+)\)([A-Za-z_][A-Za-z0-9_]*)\(([^)]*)\)', token)
        if not match:
            raise ValueError(f"Invalid atom format: {token}. Expected: (Subject)Relation(Object)")
        
        subject = match.group(1).strip()
        relation = match.group(2).strip()
        objects_str = match.group(3).strip()
        
        # Validate subject and objects don't contain invalid characters
        if '(' in subject or ')' in subject:
            raise ValueError(f"Subject contains invalid parentheses: {subject}")
        
        if objects_str:
            objects = [obj.strip() for obj in objects_str.split(',')]
            for obj in objects:
                if '(' in obj or ')' in obj:
                    raise ValueError(f"Object contains invalid parentheses: {obj}")
        else:
            objects = []
        
        return Atom(subject, relation, objects)


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def parse_expression(text: str) -> Union[Atom, LogicalExpression]:
    """
    Convenience function to parse a logical expression.
    
    Args:
        text: String containing the logical expression
    
    Returns:
        Parsed Atom or LogicalExpression
    """
    parser = LogicParser()
    return parser.parse(text)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION BLOCK (FOR TESTING)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    """Test the logic parser with examples."""
    
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                    LOGIC PARSER - TEST SUITE                                 ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
    
    test_expressions = [
        "(Pedro)IsA(estudiante)",
        "(Pedro)IsA(estudiante) → (Pedro)estudia",
        "(X)IsA(estudiante) ∧ (X)ViveEn(Madrid) → (X)TieneMetro",
        "(X)Feliz ∨ (X)Triste → (X)TieneEmociones",
        "(X)EsMamifero ↔ (X)TienePelo",
        "¬(Pedro)Feliz",
        "(A)P ∧ (B)Q ∨ (C)R",
    ]
    
    parser = LogicParser()
    
    for expr_text in test_expressions:
        print(f"Input:  {expr_text}")
        try:
            result = parser.parse(expr_text)
            print(f"Parsed: {result}")
            print(f"Type:   {type(result).__name__}")
        except Exception as e:
            print(f"Error:  {e}")
        print("-" * 70)

