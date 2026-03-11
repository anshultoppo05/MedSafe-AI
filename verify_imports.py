#!/usr/bin/env python3
import sys
print(f'Python: {sys.version}')
print('\nTesting Core Libraries:')
try:
    import streamlit
    print('✓ Streamlit', streamlit.__version__)
except Exception as e:
    print('✗ Streamlit:', e)

try:
    import pytesseract
    print('✓ PyTesseract')
except Exception as e:
    print('✗ PyTesseract:', e)

try:
    from PIL import Image
    print('✓ Pillow (PIL)')
except Exception as e:
    print('✗ Pillow:', e)

try:
    from rapidfuzz import fuzz
    print('✓ RapidFuzz')
except Exception as e:
    print('✗ RapidFuzz:', e)

try:
    import ollama
    print('✓ Ollama')
except Exception as e:
    print('✗ Ollama:', e)

try:
    import numpy
    print('✓ NumPy', numpy.__version__)
except Exception as e:
    print('✗ NumPy:', e)

try:
    import pandas
    print('✓ Pandas', pandas.__version__)
except Exception as e:
    print('✗ Pandas:', e)

try:
    import cv2
    print('✓ OpenCV', cv2.__version__)
except Exception as e:
    print('✗ OpenCV:', e)

print('\n✓ ALL CORE LIBRARIES IMPORTED SUCCESSFULLY!')
