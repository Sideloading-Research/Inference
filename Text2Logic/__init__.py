"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    TEXT2LOGIC - NATURAL LANGUAGE TO LOGIC                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

Text2Logic Module
-----------------
A complete system for converting natural language text to formal logic and
performing exhaustive logical inference.

Author: Marco
Date: October 2025
Version: 1.0

Usage:
    # Simple library usage
    import Text2Logic as t2l
    
    system = t2l.LogicSystem()
    system.add_text("Pedro es estudiante")
    system.infer_all()
    print(system.get_conclusions())

    # Internal API usage
    from Text2Logic.api import convert_text, deduce_all
    
    facts, rules = convert_text("Pedro es estudiante")
    result = deduce_all(facts, rules)

    # Direct processor usage
    from Text2Logic import TextToLogicProcessor
    
    processor = TextToLogicProcessor()
    processor.process_file("input.txt", "output.inf")
"""

# ═══════════════════════════════════════════════════════════════════════════════
# VERSION INFORMATION
# ═══════════════════════════════════════════════════════════════════════════════

__version__ = "1.0.0"
__author__ = "Marco"
__email__ = ""
__description__ = "Natural Language to Formal Logic Converter with Inference Engine"


# ═══════════════════════════════════════════════════════════════════════════════
# PUBLIC API EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

# Mode 1: Direct usage
from .api import TextToLogicProcessor

# Mode 2: Internal API
from .api import convert_text, deduce_all, analyze_text

# Mode 3: Library usage (recommended)
from .api import LogicSystem

# Core components (for advanced usage)
from .text_to_logic import TextToLogicConverter, SystemVerifier
from .logic_engine import LogicEngine, InferenceResult, DerivationChain
from .logic_parser import Atom, LogicalExpression, LogicalOperator, parse_expression
from .deduction_rules import (
    ModusPonens, ModusTollens, HypotheticalSyllogism,
    DisjunctiveSyllogism, Simplification, Conjunction,
    Resolution, BiconditionalElimination, RuleManager
)


# ═══════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Main API classes
    'LogicSystem',
    'TextToLogicProcessor',
    
    # Functions
    'convert_text',
    'deduce_all',
    'analyze_text',
    
    # Core components
    'TextToLogicConverter',
    'SystemVerifier',
    'LogicEngine',
    'InferenceResult',
    'DerivationChain',
    
    # Logic structures
    'Atom',
    'LogicalExpression',
    'LogicalOperator',
    'parse_expression',
    
    # Deduction rules
    'ModusPonens',
    'ModusTollens',
    'HypotheticalSyllogism',
    'DisjunctiveSyllogism',
    'Simplification',
    'Conjunction',
    'Resolution',
    'BiconditionalElimination',
    'RuleManager',
    
    # Version info
    '__version__',
    '__author__',
    '__description__',
]


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def get_version() -> str:
    """Get the version string."""
    return __version__


def verify_system(model_name: str = "gemma:2b") -> bool:
    """
    Verify that all system dependencies are installed.
    
    Args:
        model_name: Ollama model to verify
    
    Returns:
        True if all dependencies are OK
    """
    verifier = SystemVerifier()
    all_ok, messages = verifier.verify_system(model_name)
    
    for msg in messages:
        print(f"  {msg}")
    
    return all_ok

