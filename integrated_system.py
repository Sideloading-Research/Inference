"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              INTEGRATED COGNITIVE INFERENCE SYSTEM                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Module Description:
    Complete pipeline that integrates three cognitive processing stages:
    1. Natural language to inference conversion (NLP → .inf)
    2. Inference engine processing (.inf → natural language)
    3. Emotional analysis (inferences → emotional classification)

Author: Marco
Date: October 2025
Version: 1.1 - Fixed imports and fully documented in English
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

import os                      # Operating system interface for file operations
import sys                     # System-specific parameters and functions
from typing import List, Dict  # Type hints for better code documentation

# Import the three main cognitive processing modules
from nlp_to_inference import NLPToInferenceConverter  # Stage 1: NLP extraction
from emotional_analyzer import EmotionalAnalyser       # Stage 3: Emotion analysis (British spelling)
from engine import InferenceEngine                     # Stage 2: Inference processing


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class IntegratedCognitiveSystem:
    """
    Integrates the complete cognitive processing pipeline.
    
    This class orchestrates three distinct processing stages to transform
    natural language text into emotionally enriched knowledge:
    
    Pipeline Stages:
        1. NLP Extraction: Text → Structured Facts (.inf format)
        2. Inference Engine: Facts → Natural Language (with concatenation)
        3. Emotional Analysis: Inferences → Emotion + Sentiment classification
    
    The system automatically manages data flow between stages, handles
    temporary files, and generates comprehensive analysis reports.
    
    Attributes:
        nlp_converter (NLPToInferenceConverter): Stage 1 processor
        inference_engine (InferenceEngine): Stage 2 processor
        emotional_analyser (EmotionalAnalyser): Stage 3 processor
        temp_inf_file (str): Path for temporary .inf file
        temp_inferences_file (str): Path for temporary inferences file
    
    Example:
        >>> system = IntegratedCognitiveSystem()
        >>> system.process_and_save("Pedro is a student.", "results.txt")
        # Processes through all three stages and saves results
    """
    
    # ───────────────────────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────────────────────
    
    def __init__(self, model_name="gemma:2b"):
        """
        Initialise the integrated cognitive system.
        
        Creates instances of all three processing components and sets up
        file paths for intermediate data storage.
        
        Args:
            model_name (str): Name of the LLM model to use for NLP and emotion
                             analysis. Options: "gemma:2b" (faster) or 
                             "gemma:7b" (more accurate). Default: "gemma:2b"
        
        Returns:
            None
        
        Side Effects:
            - Creates three processor instances
            - Sets up temporary file paths
        
        Example:
            >>> system = IntegratedCognitiveSystem(model_name="gemma:7b")
            >>> # Uses larger model for better accuracy
        """
        # Initialise Stage 1: Natural Language to Inference Converter
        # This extracts semantic relationships from free-form text
        self.nlp_converter = NLPToInferenceConverter(model_name=model_name)
        
        # Initialise Stage 2: Inference Engine
        # This processes structured facts and generates natural language
        self.inference_engine = InferenceEngine()
        
        # Initialise Stage 3: Emotional Analyser (British spelling)
        # This classifies emotions and sentiments in the inferences
        self.emotional_analyser = EmotionalAnalyser(model_name=model_name)
        
        # Set up temporary file paths for inter-stage data transfer
        # These files are created during processing and cleaned up afterwards
        self.temp_inf_file = "temp_facts.inf"              # Structured facts from Stage 1
        self.temp_inferences_file = "temp_inferences.txt"  # Natural language from Stage 2
    
    # ───────────────────────────────────────────────────────────────────────────
    # CORE PROCESSING METHODS
    # ───────────────────────────────────────────────────────────────────────────
    
    def process_text(self, text: str, verbose: bool = True) -> Dict:
        """
        Processes text through the complete three-stage pipeline.
        
        This is the main processing method that:
            1. Converts natural language to structured facts
            2. Processes facts through inference engine
            3. Analyses emotional content
            4. Generates statistical summary
        
        Args:
            text (str): Input natural language text to process
            verbose (bool): If True, print progress information (default: True)
        
        Returns:
            Dict: Complete analysis results containing:
                {
                    'input_text': str,              # Original input
                    'structured_facts': List[str],  # Stage 1 output
                    'natural_inferences': List[str],# Stage 2 output
                    'emotional_analysis': List[Dict], # Stage 3 output
                    'summary': Dict                  # Statistical summary
                }
        
        Side Effects:
            - Creates temporary files (cleaned up after processing)
            - Makes multiple API calls to LLM
            - Prints progress if verbose=True
        
        Example:
            >>> system = IntegratedCognitiveSystem()
            >>> results = system.process_text("Pedro is happy.")
            >>> print(results['natural_inferences'])
            ['Pedro is happy.']
        """
        # Print header if verbose mode is enabled
        if verbose:
            self._print_header("INTEGRATED COGNITIVE INFERENCE SYSTEM")
            print("\n📝 INPUT TEXT:")
            print("-" * 70)
            print(text)
            print("-" * 70)
        
        # ═════════════════════════════════════════════════════════════════════
        # STAGE 1: NATURAL LANGUAGE → STRUCTURED FACTS
        # ═════════════════════════════════════════════════════════════════════
        
        # Print stage header if verbose
        if verbose:
            self._print_stage_header(1, "Natural Language → Structured Facts")
        
        # Convert natural language text to structured inference format
        # Returns list of inference lines like "(Pedro)IsA(student)"
        inferences_structured = self.nlp_converter.convert_text(text, verbose=verbose)
        
        # Save structured facts to temporary .inf file for Stage 2
        with open(self.temp_inf_file, 'w', encoding='utf-8') as f:
            # Write each inference on a separate line
            for inf in inferences_structured:
                if inf:  # Skip empty inferences
                    f.write(inf + "\n")
        
        # Print Stage 1 completion summary if verbose
        if verbose:
            print(f"\n✓ Generated {len(inferences_structured)} structured facts")
            print(f"✓ Saved to: {self.temp_inf_file}")
        
        # ═════════════════════════════════════════════════════════════════════
        # STAGE 2: STRUCTURED FACTS → NATURAL LANGUAGE INFERENCES
        # ═════════════════════════════════════════════════════════════════════
        
        # Print stage header if verbose
        if verbose:
            self._print_stage_header(2, "Structured Facts → Natural Language Inferences")
        
        # Process the .inf file through the inference engine
        # This converts facts to natural language and concatenates related facts
        inferences_natural = self.inference_engine.load_file(self.temp_inf_file)
        
        # Save natural language inferences to temporary file for Stage 3
        with open(self.temp_inferences_file, 'w', encoding='utf-8') as f:
            # Write each inference on a separate line
            for inf in inferences_natural:
                f.write(inf + "\n")
        
        # Print Stage 2 completion summary and results if verbose
        if verbose:
            print(f"\n✓ Generated {len(inferences_natural)} natural language inferences")
            print("\nGenerated Inferences:")
            print("-" * 70)
            for inf in inferences_natural:
                print(f"  • {inf}")
            print("-" * 70)
        
        # ═════════════════════════════════════════════════════════════════════
        # STAGE 3: EMOTIONAL & SENTIMENT ANALYSIS
        # ═════════════════════════════════════════════════════════════════════
        
        # Print stage header if verbose
        if verbose:
            self._print_stage_header(3, "Emotional & Sentiment Analysis")
        
        # Analyse each inference for emotional content and sentiment
        # Returns list of dicts with 'sentence', 'emotion', and 'sentiment' keys
        emotional_results = self.emotional_analyser.analyse_file(
            self.temp_inferences_file, 
            verbose=verbose
        )
        
        # Generate statistical summary of emotions and sentiments
        summary = self.emotional_analyser.get_emotional_summary(emotional_results)
        
        # Print emotional summary if verbose
        if verbose:
            self._print_emotional_summary(summary)
        
        # ═════════════════════════════════════════════════════════════════════
        # COMPILE AND RETURN COMPLETE RESULTS
        # ═════════════════════════════════════════════════════════════════════
        
        # Create comprehensive results dictionary
        results = {
            'input_text': text,                      # Original input text
            'structured_facts': inferences_structured, # Stage 1 output
            'natural_inferences': inferences_natural,  # Stage 2 output
            'emotional_analysis': emotional_results,   # Stage 3 output
            'summary': summary                         # Statistical summary
        }
        
        # Return the complete analysis results
        return results
    
    # ───────────────────────────────────────────────────────────────────────────
    # FILE OUTPUT METHODS
    # ───────────────────────────────────────────────────────────────────────────
    
    def process_and_save(self, text: str, output_file: str = "analysis_results.txt", verbose: bool = True):
        """
        Processes text and saves complete results to a formatted file.
        
        This convenience method combines processing with file output,
        creating a comprehensive report with all three stages and
        statistical summaries.
        
        Args:
            text (str): Input text to process
            output_file (str): Path where results should be saved
                              Default: "analysis_results.txt"
            verbose (bool): If True, print progress (default: True)
        
        Returns:
            None
        
        Side Effects:
            - Creates/overwrites output file
            - Creates and removes temporary files
            - Makes multiple API calls
            - Prints progress if verbose=True
        
        Output File Format:
            # ASCII art header
            # Input text
            # Stage 1: Structured facts
            # Stage 2: Natural inferences
            # Stage 3: Emotional analysis
            # Emotional summary statistics
        
        Example:
            >>> system = IntegratedCognitiveSystem()
            >>> system.process_and_save("Pedro is happy.", "results.txt")
            # Creates results.txt with complete analysis
        """
        # Process the text through all three stages
        results = self.process_text(text, verbose=verbose)
        
        # Open output file in write mode with UTF-8 encoding
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write ASCII art header
            f.write("╔══════════════════════════════════════════════════════════════════════════════╗\n")
            f.write("║              INTEGRATED COGNITIVE ANALYSIS RESULTS                           ║\n")
            f.write("╚══════════════════════════════════════════════════════════════════════════════╝\n\n")
            
            # ═════════════════════════════════════════════════════════════════
            # SECTION 1: INPUT TEXT
            # ═════════════════════════════════════════════════════════════════
            f.write("📝 INPUT TEXT:\n")
            f.write("-" * 70 + "\n")
            f.write(results['input_text'] + "\n")
            f.write("-" * 70 + "\n\n")
            
            # ═════════════════════════════════════════════════════════════════
            # SECTION 2: STRUCTURED FACTS (STAGE 1 OUTPUT)
            # ═════════════════════════════════════════════════════════════════
            f.write("🔹 STAGE 1: STRUCTURED FACTS (Inference Format)\n")
            f.write("-" * 70 + "\n")
            for fact in results['structured_facts']:
                if fact:  # Skip empty facts
                    f.write(f"{fact}\n")
            f.write("\n")
            
            # ═════════════════════════════════════════════════════════════════
            # SECTION 3: NATURAL LANGUAGE INFERENCES (STAGE 2 OUTPUT)
            # ═════════════════════════════════════════════════════════════════
            f.write("🔹 STAGE 2: NATURAL LANGUAGE INFERENCES\n")
            f.write("-" * 70 + "\n")
            for inf in results['natural_inferences']:
                f.write(f"{inf}\n")
            f.write("\n")
            
            # ═════════════════════════════════════════════════════════════════
            # SECTION 4: EMOTIONAL ANALYSIS (STAGE 3 OUTPUT)
            # ═════════════════════════════════════════════════════════════════
            f.write("🔹 STAGE 3: EMOTIONAL & SENTIMENT ANALYSIS\n")
            f.write("-" * 70 + "\n")
            for result in results['emotional_analysis']:
                # Write sentence
                f.write(f"{result['sentence']}\n")
                # Write emotion and sentiment classification
                f.write(f"  → Emotion: {result['emotion']}, Sentiment: {result['sentiment']}\n\n")
            
            # ═════════════════════════════════════════════════════════════════
            # SECTION 5: EMOTIONAL SUMMARY STATISTICS
            # ═════════════════════════════════════════════════════════════════
            f.write("📊 EMOTIONAL SUMMARY\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total Sentences: {results['summary']['total_sentences']}\n\n")
            
            # Write emotion distribution
            f.write("Emotions:\n")
            for emotion, count in results['summary']['emotions'].items():
                f.write(f"  • {emotion}: {count}\n")
            
            # Write sentiment distribution
            f.write("\nSentiments:\n")
            for sentiment, count in results['summary']['sentiments'].items():
                f.write(f"  • {sentiment}: {count}\n")
        
        # Print confirmation if verbose
        if verbose:
            print(f"\n✓ Complete analysis saved to: {output_file}")
        
        # Clean up temporary files
        self._cleanup_temp_files()
    
    # ───────────────────────────────────────────────────────────────────────────
    # UTILITY METHODS
    # ───────────────────────────────────────────────────────────────────────────
    
    def _cleanup_temp_files(self):
        """
        Removes temporary files created during processing.
        
        Deletes intermediate files used for data transfer between stages.
        Does not raise errors if files don't exist.
        
        Args:
            None
        
        Returns:
            None
        
        Side Effects:
            - Deletes temp_facts.inf if it exists
            - Deletes temp_inferences.txt if it exists
        """
        # List of temporary files to remove
        temp_files = [self.temp_inf_file, self.temp_inferences_file]
        
        # Attempt to remove each temporary file
        for temp_file in temp_files:
            # Check if file exists before attempting deletion
            if os.path.exists(temp_file):
                # Remove the file
                os.remove(temp_file)
    
    def _print_header(self, title: str):
        """
        Prints a formatted ASCII art header.
        
        Args:
            title (str): Title text to display in header
        
        Returns:
            None
        
        Side Effects:
            - Prints to console
        """
        # Print ASCII art box with title centered
        print("\n" + "╔" + "=" * 78 + "╗")
        print(f"║{title.center(78)}║")
        print("╚" + "=" * 78 + "╝")
    
    def _print_stage_header(self, stage_num: int, description: str):
        """
        Prints a formatted stage header.
        
        Args:
            stage_num (int): Stage number (1, 2, or 3)
            description (str): Stage description
        
        Returns:
            None
        
        Side Effects:
            - Prints to console
        """
        # Print double newline for spacing
        print(f"\n\n{'='*70}")
        # Print stage number and description in uppercase
        print(f"🔹 STAGE {stage_num}: {description.upper()}")
        # Print separator line
        print("=" * 70)
    
    def _print_emotional_summary(self, summary: Dict):
        """
        Prints a formatted emotional analysis summary with statistics.
        
        Displays:
            - Total number of sentences analysed
            - Distribution of emotions with percentages
            - Distribution of sentiments with percentages
        
        Args:
            summary (Dict): Summary dictionary from get_emotional_summary()
                           Must contain 'total_sentences', 'emotions', and 'sentiments' keys
        
        Returns:
            None
        
        Side Effects:
            - Prints to console
        """
        # Print section header
        print("\n\n📊 EMOTIONAL SUMMARY:")
        print("-" * 70)
        
        # Print total sentences count
        print(f"Total Sentences: {summary['total_sentences']}\n")
        
        # Print emotion distribution with percentages
        print("Emotions Distribution:")
        for emotion, count in summary['emotions'].items():
            # Calculate percentage of total
            percentage = (count / summary['total_sentences']) * 100
            # Print emotion name, count, and percentage
            print(f"  • {emotion}: {count} ({percentage:.1f}%)")
        
        # Print sentiment distribution with percentages
        print("\nSentiment Distribution:")
        for sentiment, count in summary['sentiments'].items():
            # Calculate percentage of total
            percentage = (count / summary['total_sentences']) * 100
            # Print sentiment name, count, and percentage
            print(f"  • {sentiment}: {count} ({percentage:.1f}%)")
        
        # Print closing separator
        print("-" * 70)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION BLOCK (FOR TESTING)
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """
    Main function demonstrating the integrated cognitive system.
    
    This function runs when the script is executed directly (not imported).
    It demonstrates the complete pipeline with example text.
    """
    # Define example text with multiple sentences and emotional content
    sample_text = """
    Pedro is an excellent student who lives in Madrid. He studies Computer Science at 
    the Complutense University and is very passionate about programming. Bob is an 
    experienced programmer who works at Microsoft. Bob is the father of Pedro and 
    a colleague of Marco. Marco is a talented teacher who loves helping students learn. 
    Marco teaches Python to Pedro with great enthusiasm. One day, Pedro was playing 
    football in the park. He kicked the ball with force and it impacted the wall violently. 
    The impact was terrible and broke the wall. The ball bounced back and hit Pedro, 
    making him feel sad. Marco was surprised by the incident and felt worried about Pedro.
    """
    
    # Create instance of the integrated system
    # Uses default "gemma:2b" model for faster processing
    system = IntegratedCognitiveSystem(model_name="gemma:2b")
    
    # Process the sample text through all three stages
    # Results are saved to "cognitive_analysis_results.txt"
    system.process_and_save(
        text=sample_text,
        output_file="cognitive_analysis_results.txt",
        verbose=True  # Print progress information
    )
    
    # Print success message
    print("\n✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print("\nCheck 'cognitive_analysis_results.txt' for complete results.\n")


# Execute main function if script is run directly
if __name__ == "__main__":
    main()
