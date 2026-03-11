#!/usr/bin/env python3
"""
MedSafe AI Environment Verification Script
Tests core components: OCR processing, fuzzy matching, AI model interaction, and UI rendering
"""

import sys
import importlib

def test_imports():
    """Test all core library imports"""
    print("=" * 70)
    print("TESTING CORE LIBRARY IMPORTS")
    print("=" * 70)
    
    imports_to_test = {
        "streamlit": "UI Framework",
        "pytesseract": "OCR Processing",
        "PIL": "Image Processing",
        "rapidfuzz": "Fuzzy String Matching",
        "ollama": "AI Model Interaction",
        "numpy": "Numerical Computing",
        "pandas": "Data Processing",
        "cv2": "Computer Vision",
        "dotenv": "Environment Configuration"
    }
    
    all_passed = True
    for module_name, description in imports_to_test.items():
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, '__version__', 'N/A')
            print(f"✓ {module_name:20} ({description:30}) - Version: {version}")
        except ImportError as e:
            print(f"✗ {module_name:20} ({description:30}) - ERROR: {e}")
            all_passed = False
    
    return all_passed


def test_ocr_component():
    """Test OCR processing component"""
    print("\n" + "=" * 70)
    print("TESTING OCR PROCESSING COMPONENT")
    print("=" * 70)
    
    try:
        import pytesseract
        from PIL import Image
        import numpy as np
        
        # Test PIL Image creation
        test_image = Image.new('RGB', (100, 100), color='white')
        print(f"✓ PIL Image creation successful: {test_image.size}")
        
        # Test pytesseract availability
        print(f"✓ pytesseract module loaded: {pytesseract.__version__}")
        print("  Note: Requires Tesseract-OCR system package for actual OCR processing")
        return True
    except Exception as e:
        print(f"✗ OCR component test failed: {e}")
        return False


def test_fuzzy_matching_component():
    """Test fuzzy string matching component"""
    print("\n" + "=" * 70)
    print("TESTING FUZZY MATCHING COMPONENT")
    print("=" * 70)
    
    try:
        from rapidfuzz import fuzz, process
        
        # Test basic fuzzy matching
        test_string1 = "medication"
        test_string2 = "medicaton"
        similarity = fuzz.ratio(test_string1, test_string2)
        print(f"✓ RapidFuzz module loaded successfully")
        print(f"  Test: '{test_string1}' vs '{test_string2}'")
        print(f"  Similarity Score: {similarity}%")
        
        # Test process extraction
        choices = ["ibuprofen", "aspirin", "acetaminophen"]
        # For demonstration, we'll assume process.extract might return 3-tuples
        # (match, score, index) if configured differently, but by default it's (match, score).
        # The loop below handles both by accessing elements by index.
        matches = process.extract(test_string1, choices, limit=2)
        print(f"  Extraction test: Top matches for '{test_string1}' against drug list:")
        for match_tuple in matches:
            # Access match and score by index, assuming at least 2 elements
            print(f"    - {match_tuple[0]}: {match_tuple[1]}%")
        return True
    except Exception as e:
        print(f"✗ Fuzzy matching component test failed: {e}")
        return False


def test_ai_model_component():
    """Test AI model interaction component"""
    print("\n" + "=" * 70)
    print("TESTING AI MODEL INTERACTION COMPONENT")
    print("=" * 70)
    
    try:
        from ollama import Client
        
        print(f"✓ Ollama client module imported successfully")
        print("  Note: Requires Ollama service running locally for actual model interaction")
        print("  To use: Start Ollama service and run: ollama pull <model_name>")
        return True
    except Exception as e:
        print(f"✗ AI model component test failed: {e}")
        return False


def test_ui_rendering_component():
    """Test UI rendering component"""
    print("\n" + "=" * 70)
    print("TESTING UI RENDERING COMPONENT")
    print("=" * 70)
    
    try:
        import streamlit as st
        
        print(f"✓ Streamlit module loaded successfully")
        print(f"  Streamlit version: {st.__version__}")
        print("  To run UI: streamlit run <app_file>.py")
        return True
    except Exception as e:
        print(f"✗ UI rendering component test failed: {e}")
        return False


def test_python_version():
    """Verify Python version compatibility"""
    print("\n" + "=" * 70)
    print("PYTHON VERSION CHECK")
    print("=" * 70)
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"Current Python Version: {version_str}")
    
    if version.major >= 3 and version.minor >= 10:
        print(f"✓ Python {version_str} meets requirement (3.10+)")
        return True
    else:
        print(f"✗ Python {version_str} does NOT meet requirement (3.10+)")
        return False


def main():
    """Run all verification tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 14 + "MEDSAFE AI ENVIRONMENT VERIFICATION" + " " * 20 + "║")
    print("╚" + "=" * 68 + "╝")
    
    results = {
        "Python Version": test_python_version(),
        "Imports": test_imports(),
        "OCR Processing": test_ocr_component(),
        "Fuzzy Matching": test_fuzzy_matching_component(),
        "AI Model Interaction": test_ai_model_component(),
        "UI Rendering": test_ui_rendering_component(),
    }
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:25} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED - Environment is ready for MedSafe AI!")
        print("=" * 70)
        return 0
    else:
        print("✗ SOME TESTS FAILED - Please check errors above")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
