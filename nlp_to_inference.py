"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              NATURAL LANGUAGE TO INFERENCE CONVERTER                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

Module Description:
    Converts natural language text to structured inference format (.inf)
    using Gemma LLM through Ollama API.

Author: Marco
Date: October 2025
Version: 1.1 - Fully documented with line-by-line comments
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

import re         # Regular expressions for pattern matching and text cleaning
import json       # JSON parsing (available for future use)
import requests   # HTTP library for making API calls to Ollama
from typing import List, Optional  # Type hints for better code documentation


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class NLPToInferenceConverter:
    """
    Converts natural language text to structured inference notation.
    
    This class uses the Gemma large language model through the Ollama API
    to extract semantic relationships from free-form text and convert them
    into a structured format suitable for logical inference engines.
    
    Input Format: Natural language sentences
        Example: "Pedro is a student who lives in Madrid."
    
    Output Format: Infix notation for inference engine
        Example: (Pedro)IsA(student)
                (Pedro)LivesIn(Madrid)
    
    The converter uses few-shot learning with carefully crafted prompts
    to ensure consistent and accurate extraction of semantic relationships.
    
    Attributes:
        model_name (str): Name of the Ollama model to use
        api_url (str): URL endpoint of the Ollama API service
        prompt_template (str): Template for the NLP extraction prompt
    
    Example:
        >>> converter = NLPToInferenceConverter()
        >>> inferences = converter.convert_text("Pedro is a student.")
        >>> print(inferences[0])
        (Pedro)IsA(student)
    """
    
    # ───────────────────────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────────────────────
    
    def __init__(self, model_name="gemma:2b", api_url="http://localhost:11434/api/generate"):
        """
        Initialise the NLP to inference converter.
        
        Args:
            model_name (str): Name of the Ollama model to use (default: "gemma:2b")
                             Options: "gemma:2b" (faster), "gemma:7b" (more accurate)
            api_url (str): URL of the Ollama API generate endpoint
                          (default: "http://localhost:11434/api/generate")
        
        Returns:
            None
        
        Side Effects:
            - Sets self.model_name to the specified model
            - Sets self.api_url to the specified API endpoint
            - Generates and stores the prompt template
        """
        # Store the model name for use in API calls
        self.model_name = model_name
        
        # Store the API URL for making requests to Ollama
        self.api_url = api_url
        
        # Generate and store the specialised prompt template
        # This instructs the LLM how to extract semantic relationships
        self.prompt_template = self._create_prompt_template()
    
    # ───────────────────────────────────────────────────────────────────────────
    # PROMPT ENGINEERING
    # ───────────────────────────────────────────────────────────────────────────
    
    def _create_prompt_template(self) -> str:
        """
        Creates the specialised prompt template for NLP extraction.
        
        This method generates a carefully engineered prompt that uses
        few-shot learning to teach the LLM how to extract semantic
        relationships from natural language and convert them to
        structured inference notation.
        
        Prompt Engineering Techniques:
            1. Clear role definition
            2. Explicit format rules
            3. Multiple diverse examples (few-shot learning)
            4. Output constraints
            5. Format validation
        
        Returns:
            str: The complete prompt template with {sentence} placeholder
        
        Notes:
            - Output format: (Subject)Relation(Object)
            - Relations should be in CamelCase or snake_case
            - Multiple relations from one sentence are on separate lines
            - English is used for relation names
        """
        # Return the complete prompt as a multi-line string
        # {sentence} will be replaced with the actual text during conversion
        return """You are an expert AI system in knowledge engineering. Your ONLY task is to convert a natural language sentence into structured infix notation for an inference engine.

Follow these rules STRICTLY:
1. Output format MUST be (Subject)RelationInCamelCase(Object).
2. The relation must be a single, concise, descriptive word using CamelCase or snake_case.
3. If a sentence contains chained actions (e.g., "A does X and then X does Y"), format as (Subject)action1(Object1)action2(Object2).
4. Extract only the main semantic information. Ignore filler words.
5. DO NOT add explanations, comments, or any additional text. Only the transformed line.
6. Use English for relation names.
7. If a sentence has multiple facts, output each on a separate line.

### Examples ###

Input sentence: Pedro is an excellent student who lives in the city of Madrid.
Response: (Pedro)IsA(student)
(Pedro)LivesIn(Madrid)

Input sentence: The programmer Bob, who is a colleague of Marco, is the father of Pedro.
Response: (Bob)IsA(programmer)
(Bob)ColleagueOf(Marco)
(Bob)FatherOf(Pedro)

Input sentence: Marco teaches Pedro to program in Python.
Response: (Marco)Teaches(Python, Pedro)

Input sentence: Pedro kicks the red ball and it impacts the brick wall.
Response: (Pedro)kicks(ball)impacts(wall)

Input sentence: The ball bounces on the wall and then falls to the ground.
Response: (ball)bounces_on(wall)falls_to(ground)

Input sentence: Bob works at Microsoft and lives in Seattle.
Response: (Bob)WorksAt(Microsoft)
(Bob)LivesIn(Seattle)

### End of Examples ###

Now, transform the following sentence (output ONLY the inference lines, nothing else):
{sentence}
"""
    
    # ───────────────────────────────────────────────────────────────────────────
    # TEXT PROCESSING METHODS
    # ───────────────────────────────────────────────────────────────────────────
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Splits text into individual sentences using simple regex patterns.
        
        This method uses regular expressions to identify sentence boundaries
        marked by periods, exclamation marks, or question marks.
        
        Limitations:
            - May split incorrectly on abbreviations (e.g., "Dr. Smith")
            - Does not handle complex punctuation patterns
            - For production use, consider using NLTK or spaCy
        
        Args:
            text (str): Input text containing one or more sentences
        
        Returns:
            List[str]: List of individual sentences (whitespace stripped)
        
        Example:
            >>> converter = NLPToInferenceConverter()
            >>> sentences = converter.split_into_sentences("Hello. How are you?")
            >>> print(sentences)
            ['Hello', 'How are you']
        """
        # Split text using regex pattern that matches sentence-ending punctuation
        # Pattern: [.!?]+ matches one or more sentence-ending marks
        sentences = re.split(r'[.!?]+', text)
        
        # Clean each sentence and filter out empty ones
        # List comprehension that:
        #   1. Strips whitespace from each sentence with .strip()
        #   2. Keeps only non-empty sentences with if s.strip()
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Return the list of cleaned sentences
        return sentences
    
    # ───────────────────────────────────────────────────────────────────────────
    # CORE CONVERSION METHODS
    # ───────────────────────────────────────────────────────────────────────────
    
    def convert_sentence(self, sentence: str) -> Optional[str]:
        """
        Converts a single sentence to inference format using Gemma LLM.
        
        This method:
            1. Formats the prompt with the input sentence
            2. Sends the prompt to Ollama API
            3. Receives the LLM's response
            4. Cleans and validates the response
            5. Returns the structured inference notation
        
        Args:
            sentence (str): Input sentence in natural language
        
        Returns:
            Optional[str]: Converted inference notation, or None if error
                          Multiple inferences are separated by newlines
        
        Side Effects:
            - Makes HTTP POST request to Ollama API
            - Prints error messages if API call fails
        
        Example:
            >>> converter = NLPToInferenceConverter()
            >>> result = converter.convert_sentence("Pedro is a student.")
            >>> print(result)
            (Pedro)IsA(student)
        """
        # Format the prompt template by replacing {sentence} placeholder
        prompt = self.prompt_template.format(sentence=sentence)
        
        # Attempt API call and handle potential errors
        try:
            # Make POST request to Ollama API
            response = requests.post(
                self.api_url,  # API endpoint URL
                json={
                    "model": self.model_name,        # Which model to use
                    "prompt": prompt,                # The formatted prompt
                    "stream": False,                 # Get complete response
                    "temperature": 0.1               # Low temp for consistency
                },
                timeout=30  # Maximum 30 seconds wait time
            )
            
            # Check if request was successful (HTTP 200 OK)
            if response.status_code == 200:
                # Parse JSON response from API
                result = response.json()
                
                # Extract the generated text from response field
                # Strip leading/trailing whitespace
                inference_text = result.get("response", "").strip()
                
                # Clean the response to ensure valid format
                inference_text = self._clean_response(inference_text)
                
                # Return the cleaned inference notation
                return inference_text
            else:
                # API returned error status code
                print(f"Error: API returned status code {response.status_code}")
                
                # Return None to indicate failure
                return None
        
        # Catch network-related exceptions
        except requests.exceptions.RequestException as e:
            # Print error message for debugging
            print(f"Error connecting to Ollama: {e}")
            
            # Return None to indicate failure
            return None
    
    def _clean_response(self, text: str) -> str:
        """
        Cleans the LLM response to extract only valid inference lines.
        
        This method validates and filters the LLM output to ensure
        only properly formatted inference statements are returned.
        
        Validation Pattern:
            Must match: (Something)Relation(Something)
            Pattern: \([^)]+\)[A-Za-z_][A-Za-z0-9_]*\([^)]*\)
        
        Args:
            text (str): Raw response from the LLM
        
        Returns:
            str: Cleaned text containing only valid inference lines
                Separate inferences are on separate lines
        
        Example:
            >>> converter = NLPToInferenceConverter()
            >>> raw = "(Pedro)IsA(student)\\nSome explanation\\n(Bob)WorksAt(MS)"
            >>> clean = converter._clean_response(raw)
            >>> print(clean)
            (Pedro)IsA(student)
            (Bob)WorksAt(MS)
        """
        # Split the text into individual lines
        lines = text.split('\n')
        
        # Initialise list to store valid inference lines
        valid_lines = []
        
        # Process each line individually
        for line in lines:
            # Remove leading/trailing whitespace
            line = line.strip()
            
            # Check if line matches inference pattern
            # Pattern explanation:
            #   \([^)]+\)  - (Subject) in parentheses
            #   [A-Za-z_]  - Relation starts with letter or underscore
            #   [A-Za-z0-9_]*  - Relation continues with letters, digits, or underscore
            #   \([^)]*\)  - (Object) in parentheses (may be empty)
            if re.match(r'\([^)]+\)[A-Za-z_][A-Za-z0-9_]*\([^)]*\)', line):
                # Line is valid - add to list
                valid_lines.append(line)
        
        # Join all valid lines with newlines and return
        return '\n'.join(valid_lines)
    
    def convert_text(self, text: str, verbose: bool = True) -> List[str]:
        """
        Converts entire text (multiple sentences) to inference format.
        
        This is the main conversion method that processes a complete text
        by:
            1. Splitting it into sentences
            2. Converting each sentence individually
            3. Collecting all inferences
            4. Optionally displaying progress
        
        Args:
            text (str): Input text (paragraph or multiple sentences)
            verbose (bool): If True, print progress information (default: True)
        
        Returns:
            List[str]: List of inference lines (strings)
                      Each element may contain multiple lines
        
        Side Effects:
            - Prints progress information if verbose=True
            - Makes multiple API calls (one per sentence)
        
        Example:
            >>> converter = NLPToInferenceConverter()
            >>> text = "Pedro is a student. Bob is his father."
            >>> inferences = converter.convert_text(text)
            Processing 2 sentences...
            ======================================================================
            [1/2] Processing: Pedro is a student.
              → (Pedro)IsA(student)
            [2/2] Processing: Bob is his father.
              → (Bob)FatherOf(his)
            ======================================================================
            Conversion complete: 2 inferences generated.
        """
        # Split the text into individual sentences
        sentences = self.split_into_sentences(text)
        
        # Initialise list to collect all generated inferences
        all_inferences = []
        
        # Print header if verbose mode is enabled
        if verbose:
            print(f"Processing {len(sentences)} sentences...")
            print("=" * 70)
        
        # Process each sentence with index for progress tracking
        # enumerate(sentences, 1) starts counting from 1 instead of 0
        for i, sentence in enumerate(sentences, 1):
            # Print current sentence being processed
            if verbose:
                print(f"\n[{i}/{len(sentences)}] Processing: {sentence}")
            
            # Convert the sentence using the LLM
            inference = self.convert_sentence(sentence)
            
            # Check if conversion was successful
            if inference:
                # Print the generated inference
                if verbose:
                    print(f"  → {inference}")
                
                # Add to list of all inferences
                all_inferences.append(inference)
            else:
                # Conversion failed for this sentence
                if verbose:
                    print(f"  → (Could not convert)")
        
        # Print completion summary if verbose mode is enabled
        if verbose:
            print("\n" + "=" * 70)
            print(f"Conversion complete: {len(all_inferences)} inferences generated.")
        
        # Return the complete list of inferences
        return all_inferences
    
    # ───────────────────────────────────────────────────────────────────────────
    # FILE I/O METHODS
    # ───────────────────────────────────────────────────────────────────────────
    
    def convert_and_save(self, text: str, output_file: str, verbose: bool = True):
        """
        Converts text and saves the inferences to a .inf file.
        
        This is a convenience method that combines text conversion with
        file output. It automatically formats the output with a header
        and saves all inferences to the specified file.
        
        Args:
            text (str): Input text to convert
            output_file (str): Path where .inf file should be saved
            verbose (bool): If True, print progress (default: True)
        
        Returns:
            None
        
        Side Effects:
            - Creates/overwrites the output file
            - Prints progress if verbose=True
        
        Output File Format:
            # Generated inference file from natural language
            # ========================================
            
            (Subject)Relation(Object)
            (Subject)Relation(Object)
            ...
        
        Example:
            >>> converter = NLPToInferenceConverter()
            >>> text = "Pedro is a student. Bob works at Microsoft."
            >>> converter.convert_and_save(text, "facts.inf")
            Processing 2 sentences...
            ...
            Inferences saved to: facts.inf
        """
        # Convert all text to inferences
        inferences = self.convert_text(text, verbose)
        
        # Open output file in write mode with UTF-8 encoding
        # 'with' statement ensures file is properly closed
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write file header comments
            f.write("# Generated inference file from natural language\n")
            f.write("# " + "=" * 74 + "\n\n")
            
            # Write each inference to the file
            for inference in inferences:
                # Check that inference is not empty
                if inference:
                    # Write the inference followed by newline
                    f.write(inference + "\n")
        
        # Print confirmation message if verbose mode is enabled
        if verbose:
            print(f"\nInferences saved to: {output_file}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION BLOCK (FOR TESTING)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    """
    Main execution block for testing the NLPToInferenceConverter module.
    
    This code only runs when the script is executed directly,
    not when imported as a module.
    """
    # Create an instance of the converter with default settings
    converter = NLPToInferenceConverter()
    
    # Define example text to demonstrate the converter
    sample_text = """
    Pedro is an excellent student who lives in Madrid. He studies Computer Science at 
    the Complutense University. Bob is a programmer who works at Microsoft. Bob is the 
    father of Pedro and a colleague of Marco. Marco teaches Python to Pedro. 
    Pedro kicks the ball and it impacts the wall. The ball bounces on the wall and falls to the ground.
    """
    
    # Print ASCII art header for the demonstration
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║          NATURAL LANGUAGE TO INFERENCE CONVERTER - DEMO                      ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
    
    # Convert the sample text and save to file
    # This will process each sentence and generate structured inferences
    converter.convert_and_save(sample_text, "generated_inferences.inf")
