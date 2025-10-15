"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    GENERIC LINGUISTIC INFERENCE ENGINE                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

Module Description:
    A generic inference engine that processes logical statements with arbitrary
    relations and converts them into natural language sentences. Supports
    relations of any arity (0, 1, 2, N arguments) with automatic format detection.

Author: Marco
Date: October 2025
Version: 2.0

Features:
    - Supports relations of any arity (0 to N arguments)
    - Automatic CamelCase and snake_case conversion
    - No hardcoded relation names
    - Flexible syntax parsing
    - Chained relation support

Usage:
    engine = InferenceEngine()
    inferences = engine.load_file("test.inf")
    for inference in inferences:
        print(inference)
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

import re  # Regular expressions for pattern matching


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class InferenceEngine:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                    GENERIC INFERENCE ENGINE CLASS                       │
    └─────────────────────────────────────────────────────────────────────────┘
    
    A flexible linguistic inference engine that processes logical statements
    with arbitrary relations and converts them into natural language.
    
    Supports multiple relation formats:
        1. Unary relations: Relation(Entity)
        2. Binary infix: (Subject)Relation(Object)
        3. N-ary relations: Relation(Arg1, Arg2, ..., ArgN)
        4. Chained relations: (A)Rel1(B)Rel2(C)
        5. Definition syntax: Relation(args):=Value
    
    All relation names are automatically converted from CamelCase or snake_case
    to natural language format.
    
    Attributes:
        statements (list): List of tuples representing parsed statements.
                          Format: (relation_name, list_of_arguments)
    
    Example:
        >>> engine = InferenceEngine()
        >>> engine.parse_line("EsUn(estudiante, Pedro)")
        >>> engine.parse_line("(Bob)PadreDE(Peter)")
        >>> print(engine.to_natural_language())
    """
    
    # ───────────────────────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────────────────────
    
    def __init__(self):
        """
        Initializes the generic inference engine.
        
        Creates an empty list to store all parsed statements.
        Each statement is stored as a tuple: (relation_name, [args])
        
        Args:
            None
        
        Returns:
            None
        """
        # List to store all parsed statements
        # Format: [(relation, [arg1, arg2, ...]), ...]
        self.statements = []
    
    # ───────────────────────────────────────────────────────────────────────────
    # PARSING METHODS
    # ───────────────────────────────────────────────────────────────────────────

    def parse_line(self, line):
        """
        Parses a single line from an inference file using generic patterns.
        
        Automatically detects and handles multiple syntax formats:
            - Definition syntax: Relation(args):=Value
            - N-ary syntax: Relation(arg1, arg2, ..., argN)
            - Binary infix: (Subject)Relation(Object)
            - Chained infix: (A)Rel1(B)Rel2(C)...
        
        Args:
            line (str): A line from the inference file to parse.
        
        Returns:
            None (updates internal state: self.statements)
        
        Example:
            >>> engine.parse_line("EsUn(estudiante, Pedro)")
            >>> engine.parse_line("(Bob)PadreDE(Peter)")
        """
        # Remove leading and trailing whitespace
        line = line.strip()
        
        # Remove inline comments (anything after #)
        if "#" in line:
            line = line.split("#")[0].strip()
        
        # Skip empty lines or comment lines (starting with #)
        if not line:
            return
        
        # ─────────────────────────────────────────────────────────────────────
        # CASE 1: DEFINITION SYNTAX - Pattern: "Relation(args):=Value"
        # ─────────────────────────────────────────────────────────────────────
        
        if ":=" in line:
            # Parse definition: Relation(args):=Value
            self._parse_definition(line)
            return
        
        # ─────────────────────────────────────────────────────────────────────
        # CASE 2: BINARY INFIX SYNTAX - Pattern: "(Subject)Relation(Object)"
        # ─────────────────────────────────────────────────────────────────────
        
        if line.startswith("("):
            # Parse infix notation (potentially chained)
            self._parse_infix(line)
            return
        
        # ─────────────────────────────────────────────────────────────────────
        # CASE 3: N-ARY SYNTAX - Pattern: "Relation(arg1, arg2, ...)"
        # ─────────────────────────────────────────────────────────────────────
        
        # Match pattern: RelationName(arguments)
        match = re.match(r"([a-zA-Z_][a-zA-Z0-9_]*)\((.*?)\)\s*$", line)
        if match:
            # Parse n-ary relation
            self._parse_nary(match)
            return
    
    def _parse_definition(self, line):
        """
        Parses definition syntax: Relation(args):=Value
        
        Creates a statement where the value is assigned to the relation with args.
        Example: "IsA(type):=Peter" becomes ("IsA", ["Peter", "type"])
        
        Args:
            line (str): Line containing definition syntax
        
        Returns:
            None (updates self.statements)
        """
        # Split by := to get left and right sides
        parts = line.split(":=")
        if len(parts) != 2:
            return
        
        left, value = parts[0].strip(), parts[1].strip()
        
        # Match relation name and arguments on left side
        match = re.match(r"([a-zA-Z_][a-zA-Z0-9_]*)\((.*?)\)", left)
        if not match:
            return
        
        relation = match.group(1)
        args_str = match.group(2).strip()
        
        # Parse arguments (comma-separated or single)
        if args_str:
            args = [arg.strip() for arg in args_str.split(",")]
        else:
            args = []
        
        # Add value as first argument, then other args
        # This makes "IsA(type):=Peter" equivalent to "IsA(Peter, type)"
        self.statements.append((relation, [value] + args))
    
    def _parse_nary(self, match):
        """
        Parses n-ary relation syntax: Relation(arg1, arg2, ..., argN)
        
        Supports any number of arguments including zero.
        Example: "FatherOf(Bob, Peter)" or "Exists()" or "Color(ball, red)"
        
        Args:
            match: Regex match object containing relation and arguments
        
        Returns:
            None (updates self.statements)
        """
        relation = match.group(1)
        args_str = match.group(2).strip()
        
        # Parse arguments separated by commas
        if args_str:
            # Split by comma and strip whitespace from each argument
            args = [arg.strip() for arg in args_str.split(",") if arg.strip()]
        else:
            # No arguments (arity 0)
            args = []
        
        # Store the statement
        self.statements.append((relation, args))
    
    def _parse_infix(self, line):
        """
        Parses binary infix syntax: (Subject)Relation(Object)
        Also supports chained relations: (A)Rel1(B)Rel2(C)
        
        Args:
            line (str): Line containing infix notation
        
        Returns:
            None (updates self.statements)
        """
        # Extract the initial subject from the beginning
        initial_match = re.match(r"\(([^)]+)\)", line)
        if not initial_match:
            return
        
        # Get the first subject
        current_subject = initial_match.group(1).strip()
        
        # Get the remaining part after the first subject
        remaining = line[initial_match.end():]
        
        # Find all relation(object) pairs
        # Pattern: RelationName(content)
        pattern = re.compile(r"([a-zA-Z_][a-zA-Z0-9_]*)\(([^)]+)\)")
        
        # Process each relation(object) pair found
        for match in pattern.finditer(remaining):
            relation = match.group(1)
            obj = match.group(2).strip()
            
            # Store as binary relation
            self.statements.append((relation, [current_subject, obj]))
            
            # Chain: object becomes subject for next relation
            current_subject = obj

    # ───────────────────────────────────────────────────────────────────────────
    # FORMATTING METHODS
    # ───────────────────────────────────────────────────────────────────────────
    
    def format_relation(self, text):
        """
        Converts relation names to natural language format.
        
        Handles multiple naming conventions:
            - CamelCase: "FatherOf" → "father of"
            - snake_case: "kick_the" → "kick the"
            - Mixed: "FatherOf_Person" → "father of person"
        
        Preserves capital letters to detect word boundaries in CamelCase.
        
        Args:
            text (str): Relation name in programming format
        
        Returns:
            str: Natural language formatted text in lowercase
        
        Example:
            >>> engine.format_relation("EsUn")
            'es un'
            >>> engine.format_relation("padre_de")
            'padre de'
            >>> engine.format_relation("PareceUn")
            'parece un'
        """
        # First, handle snake_case: replace underscores with spaces
        text = text.replace("_", " ")
        
        # Then, handle CamelCase: insert space before capital letters
        # Pattern 1: lowercase followed by uppercase
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        
        # Pattern 2: multiple capitals followed by lowercase (e.g., "XMLParser" → "XML Parser")
        text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', text)
        
        # Convert to lowercase for natural language
        return text.lower()

    # ───────────────────────────────────────────────────────────────────────────
    # CONVERSION METHODS
    # ───────────────────────────────────────────────────────────────────────────
    
    def to_natural_language(self):
        """
        Converts all stored statements into natural language sentences (English).
        
        Groups consecutive statements with the same subject using "and".
        
        Example:
            (Pedro)Is(programmer)
            (Pedro)FatherOf(Peter)
            (Pedro)LivesIn(Madrid)
            
            Becomes: "Pedro is programmer and father of Peter and lives in Madrid."
        
        Handles statements of different arities:
            - Arity 0: "Relation()" → "relation."
            - Arity 1: "Relation(X)" → "X relation."
            - Arity 2: "Relation(X, Y)" → "X relation Y."
            - Arity N: "Relation(X, Y, Z)" → "X relation Y, Z."
        
        Args:
            None
        
        Returns:
            list: List of natural language sentences as strings (in English)
        
        Example:
            >>> engine.to_natural_language()
            ['Peter is a student and lives in Madrid.', 'Bob father of Peter.']
        """
        output_lines = []
        
        # Group consecutive statements by first argument (subject)
        i = 0
        while i < len(self.statements):
            relation, args = self.statements[i]
            
            # Get the subject (first argument if exists, otherwise None)
            subject = args[0] if len(args) > 0 else None
            
            # Start building the sentence with this statement (include subject)
            statement_parts = [self._format_statement_part(relation, args, include_subject=True)]
            
            # Look ahead for more statements with the same subject
            j = i + 1
            while j < len(self.statements):
                next_relation, next_args = self.statements[j]
                next_subject = next_args[0] if len(next_args) > 0 else None
                
                # Only group if subjects match
                if next_subject == subject and subject is not None:
                    # Don't include subject in subsequent parts
                    statement_parts.append(self._format_statement_part(next_relation, next_args, include_subject=False))
                    j += 1
                else:
                    break
            
            # Join all parts with " and " (English)
            if len(statement_parts) == 1:
                sentence = f"{statement_parts[0]}."
            else:
                sentence = f"{' and '.join(statement_parts)}."
            
            output_lines.append(sentence)
            
            # Move to the next different subject
            i = j
        
        return output_lines
    
    def _format_statement_part(self, relation, args, include_subject=True):
        """
        Formats a single statement part (for concatenation) in English.
        
        Args:
            relation (str): Relation name
            args (list): List of arguments
            include_subject (bool): Whether to include the subject (first arg) in output
        
        Returns:
            str: Formatted statement part without ending punctuation
        
        Example:
            >>> engine._format_statement_part("FatherOf", ["Bob", "Peter"], True)
            'Bob father of Peter'
            >>> engine._format_statement_part("FatherOf", ["Bob", "Peter"], False)
            'father of Peter'
        """
        # Format the relation name to natural language (English)
        formatted_rel = self.format_relation(relation)
        
        # Handle different arities
        arity = len(args)
        
        if arity == 0:
            # Arity 0: just the relation
            return formatted_rel
        
        elif arity == 1:
            # Arity 1: "X relation" or just "relation"
            if include_subject:
                return f"{args[0]} {formatted_rel}"
            else:
                return formatted_rel
        
        elif arity == 2:
            # Arity 2: "X relation Y" or just "relation Y"
            if include_subject:
                return f"{args[0]} {formatted_rel} {args[1]}"
            else:
                return f"{formatted_rel} {args[1]}"
        
        else:
            # Arity N (N > 2): "X relation Y, Z, W, ..." or "relation Y, Z, W, ..."
            if include_subject:
                first_arg = args[0]
                remaining_args = ", ".join(args[1:])
                return f"{first_arg} {formatted_rel} {remaining_args}"
            else:
                remaining_args = ", ".join(args[1:])
                return f"{formatted_rel} {remaining_args}"

    # ───────────────────────────────────────────────────────────────────────────
    # FILE I/O METHODS
    # ───────────────────────────────────────────────────────────────────────────
    
    def load_file(self, path):
        """
        Loads and processes an inference file with automatic encoding detection.
        
        This method:
            1. Clears any previously loaded statements
            2. Attempts to open file with multiple encodings
            3. Parses each line generically
            4. Converts statements to natural language
        
        Args:
            path (str): Path to the inference file
        
        Returns:
            list: Natural language sentences generated from the file
        
        Raises:
            FileNotFoundError: If file doesn't exist
            UnicodeDecodeError: If file can't be decoded with any encoding
        
        Example:
            >>> engine.load_file("test.inf")
            ['Peter is a student.', ...]
        """
        # Clear previous statements
        self.statements = []
        
        # List of encodings to try
        encodings = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 
                     'latin-1', 'cp1252', 'iso-8859-1']
        
        # Try each encoding until one succeeds
        for encoding in encodings:
            try:
                with open(path, "r", encoding=encoding) as f:
                    for line in f:
                        self.parse_line(line)
                break
            except UnicodeDecodeError:
                continue
        
        # Convert to natural language and return
        return self.to_natural_language()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN PROGRAM
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    """
    Main execution block - demonstrates the generic inference engine.
    
    This block:
        1. Creates an instance of the InferenceEngine
        2. Loads and processes the test.inf file
        3. Displays the generated natural language inferences
    """
    
    # ───────────────────────────────────────────────────────────────────────────
    # INITIALIZATION
    # ───────────────────────────────────────────────────────────────────────────
    
    # Create a new generic inference engine instance
    engine = InferenceEngine()
    
    # ───────────────────────────────────────────────────────────────────────────
    # LOAD AND PROCESS
    # ───────────────────────────────────────────────────────────────────────────
    
    # Load the inference file and get natural language output
    inferences = engine.load_file("test.inf")
    
    # ───────────────────────────────────────────────────────────────────────────
    # DISPLAY RESULTS
    # ───────────────────────────────────────────────────────────────────────────
    
    # Print header
    print("Natural Language Inferences:")
    print("-" * 50)
    
    # Print each inference on a separate line
    for inference in inferences:
        print(inference)
