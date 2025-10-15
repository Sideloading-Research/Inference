"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SIMPLE EXAMPLE - QUICK START                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Module Description:
    A simple example to quickly test the integrated cognitive system.
    Demonstrates the complete three-stage pipeline with minimal code.

Author: Marco
Date: October 2025
Version: 1.1 - Fully documented in English
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

from integrated_system import IntegratedCognitiveSystem  # Main system class


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """
    Main function demonstrating a simple usage of the cognitive system.
    
    This function:
        1. Prints a header
        2. Initialises the integrated system
        3. Processes example text through all three stages
        4. Saves comprehensive results to a file
        5. Handles potential errors gracefully
    
    Returns:
        None
    
    Side Effects:
        - Prints to console
        - Creates output file
        - Makes API calls to Ollama
    """
    # Print ASCII art header for visual appeal
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║              COGNITIVE SYSTEM - SIMPLE EXAMPLE                               ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
    
    # Print initialisation message
    print("🔧 Initialising Integrated Cognitive System...")
    
    # Create instance of the integrated cognitive system
    # Uses "gemma:2b" model by default (faster, but less accurate than 7b)
    system = IntegratedCognitiveSystem(model_name="gemma:2b")
    
    # Print confirmation that system is ready
    print("✓ System ready!\n")
    
    # Define example text with multiple facts and emotional content
    # This text includes:
    #   - Entity definitions (Pedro is a student, Bob works at...)
    #   - Relationships (Bob is Pedro's father, Marco teaches...)
    #   - Emotional content (excited, happy)
    example_text = """
    Pedro is a brilliant student who lives in Madrid. He studies Computer Science
    and loves programming. Bob is Pedro's father and he works at Microsoft as a
    senior developer. Marco is an excellent teacher who teaches Python to Pedro.
    Pedro is very excited about learning and feels happy when he masters new concepts.
    """
    
    # Print processing message
    print("📝 Processing example text...")
    print("=" * 78)
    
    # Attempt to process the text and handle potential errors
    try:
        # Process through the complete three-stage pipeline
        # This will:
        #   1. Extract structured facts from natural language
        #   2. Convert facts to natural language inferences
        #   3. Analyse emotional content and sentiment
        #   4. Save all results to a file
        system.process_and_save(
            text=example_text,                       # Text to process
            output_file="simple_example_results.txt",  # Where to save results
            verbose=True                              # Print progress information
        )
        
        # Print success message with separator line
        print("\n" + "=" * 78)
        print("✅ SUCCESS! Analysis complete.")
        
        # Inform user where to find detailed results
        print("\n📁 Check 'simple_example_results.txt' for detailed results.\n")
        
    # Catch any exceptions that occur during processing
    except Exception as e:
        # Print error message with exception details
        print(f"\n❌ Error occurred: {e}")
        
        # Print troubleshooting tips to help user resolve the issue
        print("\nTroubleshooting tips:")
        print("  1. Make sure Ollama is running: ollama serve")
        print("  2. Make sure gemma:2b is installed: ollama pull gemma:2b")
        print("  3. Check that engine.py is in the same directory\n")


# ═══════════════════════════════════════════════════════════════════════════════
# SCRIPT ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

# Execute main function if this script is run directly
# (Not when imported as a module)
if __name__ == "__main__":
    main()
