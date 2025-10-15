"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    EMOTIONAL INFERENCE ANALYSER                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Module Description:
    Analyses inference sentences for emotional and sentiment content
    using Gemma LLM through Ollama.

Author: Marco
Date: October 2025
Version: 1.1 - Fixed parsing and fully documented
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

import requests  # HTTP library for making API calls to Ollama
import json      # JSON parsing (not actively used but kept for future expansion)
from typing import Dict, List, Tuple  # Type hints for better code documentation


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class EmotionalAnalyser:
    """
    Analyses natural language inferences for emotional and sentiment content.
    
    This class uses the Gemma large language model through the Ollama API
    to classify sentences by their primary emotion and sentiment polarity.
    
    Supported Emotions:
        - Joy: Happiness, excitement, pleasure
        - Sadness: Sorrow, disappointment, grief
        - Anger: Frustration, irritation, rage
        - Fear: Anxiety, worry, terror
        - Surprise: Astonishment, amazement
        - Disgust: Revulsion, distaste
        - Neutral: No strong emotion
    
    Supported Sentiments:
        - Positive: Favourable, good, pleasant
        - Negative: Unfavourable, bad, unpleasant
        - Neutral: Neither positive nor negative
    
    Attributes:
        model_name (str): Name of the Ollama model to use for analysis
        api_url (str): URL endpoint of the Ollama API service
        prompt_template (str): Template for the emotion classification prompt
    
    Example:
        >>> analyser = EmotionalAnalyser()
        >>> emotion, sentiment = analyser.analyse_sentence("Pedro is very happy!")
        >>> print(f"Emotion: {emotion}, Sentiment: {sentiment}")
        Emotion: Joy, Sentiment: Positive
    """
    
    # ───────────────────────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────────────────────
    
    def __init__(self, model_name="gemma:2b", api_url="http://localhost:11434/api/generate"):
        """
        Initialise the emotional analyser with specified model and API endpoint.
        
        Args:
            model_name (str): Name of the Ollama model to use (default: "gemma:2b")
                             Smaller models are faster but less accurate.
                             Larger models (e.g., "gemma:7b") are more accurate but slower.
            api_url (str): URL of the Ollama API generate endpoint
                          (default: "http://localhost:11434/api/generate")
        
        Returns:
            None
        
        Side Effects:
            - Sets self.model_name to the specified model
            - Sets self.api_url to the specified API endpoint
            - Generates and stores the prompt template via _create_prompt_template()
        
        Example:
            >>> analyser = EmotionalAnalyser(model_name="gemma:7b")
            >>> # Creates analyser using the larger 7B parameter model
        """
        # Store the model name for later use in API calls
        self.model_name = model_name
        
        # Store the API URL for making requests to Ollama
        self.api_url = api_url
        
        # Generate and store the specialised prompt template
        # This template instructs the LLM how to classify emotions
        self.prompt_template = self._create_prompt_template()
    
    # ───────────────────────────────────────────────────────────────────────────
    # PROMPT ENGINEERING
    # ───────────────────────────────────────────────────────────────────────────
    
    def _create_prompt_template(self) -> str:
        """
        Creates the specialised prompt template for emotional analysis.
        
        This method generates a carefully crafted prompt using few-shot learning
        techniques to instruct the LLM on exactly how to classify emotions and
        sentiments. The prompt includes:
            - Clear role definition
            - Strict output format rules
            - Multiple examples (few-shot learning)
            - Explicit constraints to prevent unwanted output
        
        Returns:
            str: The complete prompt template with a {sentence} placeholder
        
        Notes:
            - Uses British English spelling ("analyse" not "analyze")
            - Temperature should be set low (0.1) for consistent output
            - Examples cover diverse scenarios to improve accuracy
        
        Prompt Engineering Techniques Used:
            1. Role assignment: "You are an expert AI system..."
            2. Few-shot learning: Multiple input/output examples
            3. Output constraints: "ONLY output..." / "DO NOT add..."
            4. Format specification: "Emotion, Sentiment"
        """
        # Return the complete prompt template as a multi-line string
        # The {sentence} placeholder will be replaced with actual text during analysis
        return """You are an expert AI system specialising in emotional and sentiment analysis. Your task is to analyse a sentence and classify it by its PRIMARY emotion and SENTIMENT.

Follow these rules with ABSOLUTE STRICTNESS:
1. Identify the PRIMARY emotion from this EXACT list: Joy, Sadness, Anger, Fear, Surprise, Disgust, Neutral
2. Identify the SENTIMENT as EXACTLY one of: Positive, Negative, Neutral
3. Output format MUST be EXACTLY: [EmotionName], [SentimentName]
4. Use the EXACT words from the lists above. Do NOT use "Emotion" or "Sentiment" as values.
5. Output ONLY the classification in the exact format specified. NO explanations, NO comments, NO additional text.
6. Your response must be a single line with TWO values separated by a comma.

### Examples (FOLLOW THIS FORMAT EXACTLY) ###

Sentence: Peter is a student.
Joy, Neutral

Sentence: Bob is father of Peter.
Neutral, Neutral

Sentence: Peter kicks the Ball and impacts the Wall.
Neutral, Neutral

Sentence: The Wall stops the Ball with force.
Anger, Negative

Sentence: It was a terrible impact.
Sadness, Negative

Sentence: Pedro is very happy and excited about his success.
Joy, Positive

Sentence: Marco feels afraid of the dark shadows.
Fear, Negative

Sentence: The surprise party was amazing!
Surprise, Positive

### End of Examples ###

Now, analyse the following sentence. Output ONLY in the format "EmotionName, SentimentName" with NO other text:
{sentence}
"""
    
    # ───────────────────────────────────────────────────────────────────────────
    # CORE ANALYSIS METHODS
    # ───────────────────────────────────────────────────────────────────────────
    
    def analyse_sentence(self, sentence: str) -> Tuple[str, str]:
        """
        Analyses a single sentence for emotion and sentiment using the LLM.
        
        This method:
            1. Formats the prompt template with the input sentence
            2. Sends the prompt to the Ollama API
            3. Receives and parses the LLM's response
            4. Returns the classified emotion and sentiment
        
        Args:
            sentence (str): The input sentence to analyse
        
        Returns:
            Tuple[str, str]: A tuple containing (emotion, sentiment)
                            e.g., ("Joy", "Positive")
                            Returns ("Unknown", "Unknown") if analysis fails
        
        Raises:
            Does not raise exceptions; errors are caught and logged
        
        Side Effects:
            - Makes an HTTP POST request to the Ollama API
            - Prints error messages to console if connection fails
        
        Example:
            >>> analyser = EmotionalAnalyser()
            >>> emotion, sentiment = analyser.analyse_sentence("I am very happy!")
            >>> print(f"{emotion}, {sentiment}")
            Joy, Positive
        """
        # Format the prompt template by replacing {sentence} with actual text
        prompt = self.prompt_template.format(sentence=sentence)
        
        # Attempt to call the Ollama API and handle potential errors
        try:
            # Make POST request to Ollama API with the formatted prompt
            response = requests.post(
                self.api_url,  # The API endpoint URL
                json={
                    "model": self.model_name,      # Which model to use
                    "prompt": prompt,              # The formatted prompt
                    "stream": False,               # Get complete response, not streamed
                    "temperature": 0.1             # Low temperature for deterministic output
                },
                timeout=30  # Wait maximum 30 seconds for response
            )
            
            # Check if the API request was successful (HTTP 200)
            if response.status_code == 200:
                # Parse the JSON response from the API
                result = response.json()
                
                # Extract the text response from the 'response' field
                # Strip whitespace from beginning and end
                classification = result.get("response", "").strip()
                
                # Parse the classification string to extract emotion and sentiment
                emotion, sentiment = self._parse_classification(classification)
                
                # Return the parsed emotion and sentiment
                return emotion, sentiment
            else:
                # API returned an error status code
                print(f"Error: API returned status code {response.status_code}")
                
                # Return unknown values to indicate failure
                return "Unknown", "Unknown"
        
        # Catch any network-related exceptions (connection errors, timeouts, etc.)
        except requests.exceptions.RequestException as e:
            # Print the error message for debugging
            print(f"Error connecting to Ollama: {e}")
            
            # Return unknown values to indicate failure
            return "Unknown", "Unknown"
    
    def _parse_classification(self, text: str) -> Tuple[str, str]:
        """
        Parses the LLM response to extract emotion and sentiment values.
        
        This method handles the raw text output from the LLM and extracts
        the emotion and sentiment, cleaning up any formatting issues.
        
        Parsing Strategy:
            1. Take only the first line (ignore any extra explanation)
            2. Split by comma to separate emotion and sentiment
            3. Clean whitespace from both values
            4. Validate that we have exactly two values
        
        Args:
            text (str): Raw response text from the LLM
        
        Returns:
            Tuple[str, str]: A tuple containing (emotion, sentiment)
                            Returns ("Unknown", "Unknown") if parsing fails
        
        Example:
            >>> analyser._parse_classification("Joy, Positive\\nSome extra text")
            ('Joy', 'Positive')
            
            >>> analyser._parse_classification("Neutral, Neutral")
            ('Neutral', 'Neutral')
            
            >>> analyser._parse_classification("Invalid format")
            ('Unknown', 'Unknown')
        """
        # Strip leading/trailing whitespace from the entire response
        text = text.strip()
        
        # Take only the first line (discard any explanations after newline)
        # This prevents the LLM from adding unwanted commentary
        first_line = text.split('\n')[0].strip()
        
        # Split the line by comma to separate emotion and sentiment
        # Also strip whitespace from each part
        parts = [p.strip() for p in first_line.split(',')]
        
        # Verify we have exactly 2 parts (emotion and sentiment)
        if len(parts) >= 2:
            # Extract emotion and sentiment from the parsed parts
            emotion = parts[0]
            sentiment = parts[1]
            
            # Validate that neither value is the literal word "Emotion" or "Sentiment"
            # This catches cases where the LLM didn't follow instructions
            if emotion == "Emotion" or sentiment == "Sentiment":
                # Invalid response - return Unknown
                return "Unknown", "Unknown"
            
            # Return the successfully parsed emotion and sentiment
            return emotion, sentiment
        else:
            # Parsing failed - didn't get exactly 2 comma-separated values
            # Return Unknown to indicate parsing failure
            return "Unknown", "Unknown"
    
    # ───────────────────────────────────────────────────────────────────────────
    # BATCH PROCESSING METHODS
    # ───────────────────────────────────────────────────────────────────────────
    
    def analyse_file(self, input_file: str, verbose: bool = True) -> List[Dict]:
        """
        Analyses all sentences in a text file for emotional content.
        
        This method:
            1. Reads all lines from the input file
            2. Filters out comments (lines starting with #) and empty lines
            3. Analyses each remaining sentence using analyse_sentence()
            4. Collects results in a structured format
            5. Optionally prints progress information
        
        Args:
            input_file (str): Path to the input text file
            verbose (bool): If True, print progress information (default: True)
        
        Returns:
            List[Dict]: List of analysis results, each dict contains:
                       {
                           'sentence': str,    # The original sentence
                           'emotion': str,     # Classified emotion
                           'sentiment': str    # Classified sentiment
                       }
                       Returns empty list if file not found
        
        Side Effects:
            - Reads from file system
            - Prints progress information if verbose=True
        
        Example:
            >>> analyser = EmotionalAnalyser()
            >>> results = analyser.analyse_file("inferences.txt")
            Analysing 5 sentences...
            ======================================================================
            [1/5] Peter is a student.
              → Emotion: Neutral, Sentiment: Neutral
            ...
        """
        # Initialise empty list to store all analysis results
        results = []
        
        # Attempt to read the file and handle potential errors
        try:
            # Open the file in read mode with UTF-8 encoding
            # Use 'with' statement to ensure file is properly closed
            with open(input_file, 'r', encoding='utf-8') as f:
                # Read all lines from the file into a list
                lines = f.readlines()
            
            # Filter lines to remove comments and empty lines
            # Keep only lines that:
            #   - Are not empty after stripping whitespace
            #   - Do not start with '#' (comments)
            sentences = [
                line.strip()  # Remove leading/trailing whitespace
                for line in lines
                if line.strip() and not line.strip().startswith('#')
            ]
            
            # Print progress header if verbose mode is enabled
            if verbose:
                print(f"Analysing {len(sentences)} sentences...")
                print("=" * 70)
            
            # Process each sentence with index for progress tracking
            for i, sentence in enumerate(sentences, 1):
                # Print current sentence if verbose mode is enabled
                if verbose:
                    print(f"\n[{i}/{len(sentences)}] {sentence}")
                
                # Analyse the sentence using the LLM
                emotion, sentiment = self.analyse_sentence(sentence)
                
                # Create result dictionary with all information
                result = {
                    'sentence': sentence,      # Original sentence text
                    'emotion': emotion,        # Classified emotion
                    'sentiment': sentiment     # Classified sentiment
                }
                
                # Add result to the results list
                results.append(result)
                
                # Print analysis result if verbose mode is enabled
                if verbose:
                    print(f"  → Emotion: {emotion}, Sentiment: {sentiment}")
            
            # Print completion summary if verbose mode is enabled
            if verbose:
                print("\n" + "=" * 70)
                print(f"Analysis complete: {len(results)} sentences analysed.")
            
            # Return the list of all results
            return results
        
        # Handle file not found error
        except FileNotFoundError:
            # Print error message indicating which file wasn't found
            print(f"Error: File '{input_file}' not found.")
            
            # Return empty list to indicate failure
            return []
    
    def analyse_and_save(self, input_file: str, output_file: str, verbose: bool = True):
        """
        Analyses a file and saves the results to another file.
        
        This is a convenience method that combines analyse_file() with
        file output functionality. It reads sentences, analyses them,
        and writes formatted results to a new file.
        
        Args:
            input_file (str): Path to input file containing sentences
            output_file (str): Path where results should be saved
            verbose (bool): If True, print progress (default: True)
        
        Returns:
            None
        
        Side Effects:
            - Reads from input_file
            - Writes to output_file
            - Prints progress if verbose=True
        
        Output File Format:
            # Emotional Analysis Results
            # ========================================
            
            Sentence text here.
              Emotion: EmotionName, Sentiment: SentimentName
            
            Another sentence here.
              Emotion: EmotionName, Sentiment: SentimentName
        
        Example:
            >>> analyser = EmotionalAnalyser()
            >>> analyser.analyse_and_save("input.txt", "results.txt")
            Analysing 3 sentences...
            ...
            Results saved to: results.txt
        """
        # Analyse all sentences in the input file
        # This returns a list of result dictionaries
        results = self.analyse_file(input_file, verbose=verbose)
        
        # Open output file in write mode with UTF-8 encoding
        # Use 'with' statement to ensure file is properly closed
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header comment
            f.write("# Emotional Analysis Results\n")
            f.write("# " + "=" * 74 + "\n\n")
            
            # Write each result in a formatted manner
            for result in results:
                # Write the original sentence
                f.write(f"{result['sentence']}\n")
                
                # Write the analysis result indented for readability
                f.write(f"  Emotion: {result['emotion']}, Sentiment: {result['sentiment']}\n\n")
        
        # Print confirmation message if verbose mode is enabled
        if verbose:
            print(f"\nResults saved to: {output_file}")
    
    # ───────────────────────────────────────────────────────────────────────────
    # STATISTICAL ANALYSIS METHODS
    # ───────────────────────────────────────────────────────────────────────────
    
    def get_emotional_summary(self, results: List[Dict]) -> Dict:
        """
        Creates a statistical summary of emotions and sentiments.
        
        This method analyses a list of results and generates aggregate
        statistics showing the distribution of emotions and sentiments.
        
        Args:
            results (List[Dict]): List of analysis results from analyse_file()
                                 Each dict should have 'emotion' and 'sentiment' keys
        
        Returns:
            Dict: Summary statistics containing:
                 {
                     'total_sentences': int,              # Total number of sentences
                     'emotions': Dict[str, int],          # Count of each emotion
                     'sentiments': Dict[str, int]         # Count of each sentiment
                 }
        
        Example:
            >>> results = [
            ...     {'emotion': 'Joy', 'sentiment': 'Positive'},
            ...     {'emotion': 'Joy', 'sentiment': 'Positive'},
            ...     {'emotion': 'Neutral', 'sentiment': 'Neutral'}
            ... ]
            >>> summary = analyser.get_emotional_summary(results)
            >>> print(summary)
            {
                'total_sentences': 3,
                'emotions': {'Joy': 2, 'Neutral': 1},
                'sentiments': {'Positive': 2, 'Neutral': 1}
            }
        """
        # Initialise dictionaries to count occurrences of each emotion/sentiment
        emotion_counts = {}     # Will store: {emotion_name: count}
        sentiment_counts = {}   # Will store: {sentiment_name: count}
        
        # Iterate through each result dictionary
        for result in results:
            # Extract emotion and sentiment from current result
            emotion = result['emotion']
            sentiment = result['sentiment']
            
            # Increment emotion count
            # get() returns current count (or 0 if not yet in dict), then add 1
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            # Increment sentiment count
            # get() returns current count (or 0 if not yet in dict), then add 1
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        
        # Create and return summary dictionary with all statistics
        return {
            'total_sentences': len(results),      # Total number of analysed sentences
            'emotions': emotion_counts,            # Dictionary of emotion frequencies
            'sentiments': sentiment_counts         # Dictionary of sentiment frequencies
        }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION BLOCK (FOR TESTING)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    """
    Main execution block for testing the EmotionalAnalyser module.
    
    This code only runs when the script is executed directly,
    not when it's imported as a module.
    """
    # Create an instance of the EmotionalAnalyser with default settings
    analyser = EmotionalAnalyser()
    
    # Print ASCII art header for the demo
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                 EMOTIONAL INFERENCE ANALYSER - DEMO                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
    
    # Analyse a generated inference file and save results
    # Replace "inferences_output.txt" with your actual file name
    analyser.analyse_and_save("inferences_output.txt", "emotional_analysis.txt")
