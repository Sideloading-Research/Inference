"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    TEXT2LOGIC DEMO - TEST.TXT PROCESSOR                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

Demonstration script that processes TEST.txt and generates complete inference results.

Author: Marco
Date: October 2025
Version: 1.0
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Text2Logic import TextToLogicProcessor


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """
    Main demonstration function.
    
    This script:
    1. Verifies Ollama and Gemma are installed
    2. Reads TEST.txt from parent directory
    3. Converts text to logical format (.inf)
    4. Performs exhaustive inference
    5. Generates complete results file
    """
    
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                    TEXT2LOGIC DEMONSTRATION                                   ║")
    print("║                    Processing TEST.txt                                       ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
    
    # Initialize processor
    print("Initializing Text2Logic processor...")
    processor = TextToLogicProcessor(model_name="gemma:2b", verify_on_init=True)
    
    # Check if verification passed
    if not processor.converter.verified:
        print("\n❌ Cannot proceed without required dependencies.")
        print("\nPlease ensure:")
        print("  1. Ollama is installed: https://ollama.ai")
        print("  2. Ollama service is running: ollama serve")
        print("  3. Gemma model is available: ollama pull gemma:2b")
        sys.exit(1)
    
    # Define file paths
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(parent_dir, "TEST.txt")
    output_file = os.path.join(parent_dir, "TEST_logic.inf")
    
    # Check if TEST.txt exists
    if not os.path.exists(input_file):
        print(f"\n❌ Input file not found: {input_file}")
        print("\nPlease ensure TEST.txt exists in the parent directory.")
        sys.exit(1)
    
    print(f"\n✓ Found input file: {input_file}")
    print(f"✓ Output will be saved to: {output_file}")
    
    # Process the file
    print("\n" + "=" * 70)
    print("Starting processing pipeline...")
    print("=" * 70 + "\n")
    
    try:
        analysis = processor.process_file(
            input_file=input_file,
            output_file=output_file,
            perform_inference=True,
            verbose=True
        )
        
        # Display summary
        print("\n\n")
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                    PROCESSING COMPLETE - SUMMARY                             ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
        
        print("📊 STATISTICS:")
        print("-" * 70)
        print(f"  Original Facts:    {len(analysis.conversion.facts)}")
        print(f"  Original Rules:    {len(analysis.conversion.rules)}")
        print(f"  Derived Facts:     {len(analysis.inference.derived_facts)}")
        print(f"  Inference Depth:   {analysis.inference.iterations} iterations")
        print(f"  Total Knowledge:   {len(analysis.inference.get_all_facts())} items")
        
        if analysis.inference.contradictions:
            print(f"\n  ⚠️  Contradictions: {len(analysis.inference.contradictions)}")
            for contradiction in analysis.inference.contradictions:
                print(f"    • {contradiction}")
        
        print("\n📁 OUTPUT FILES:")
        print("-" * 70)
        print(f"  Logic format:      {output_file}")
        print(f"  Inference results: {output_file.replace('.inf', '_inferred.txt')}")
        
        print("\n✅ DEMONSTRATION COMPLETE!")
        print("\nYou can now:")
        print("  1. Review the generated .inf file with facts and rules")
        print("  2. Check the inference results file for all derived conclusions")
        print("  3. Examine the reasoning chains for each derived fact")
        
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()

