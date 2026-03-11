"""
ocr_utils.py - Prescription OCR and Text Extraction Utilities

This module provides OCR capabilities for extracting text from prescription images.
Handles image preprocessing, OCR processing, and text cleaning.
"""

import pytesseract
from PIL import Image
import cv2
import numpy as np
from typing import Optional, List, Tuple
import os


class OCRProcessor:
    """
    Handles OCR processing for prescription images.
    
    Provides functionality for:
    - Image preprocessing and optimization
    - Text extraction using Tesseract OCR
    - Medicine name extraction
    - Dosage parsing
    - Confidence scoring
    """

    def __init__(self, tesseract_path: Optional[str] = None):
        """
        Initialize OCR processor
        
        Args:
            tesseract_path: Path to Tesseract executable (if not in PATH)
        """
        self.tesseract_path = tesseract_path
        if tesseract_path and os.path.exists(tesseract_path):
            pytesseract.pytesseract.pytesseract_cmd = tesseract_path

    def process_image(self, image_path: str) -> Tuple[str, float]:
        """
        Process an image file and extract text
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Tuple of (extracted_text, confidence_score)
        """
        try:
            # Load and preprocess image
            image = self._load_image(image_path)
            preprocessed = self._preprocess_image(image)
            
            # Extract text with confidence
            text = pytesseract.image_to_string(preprocessed)
            confidence = self._estimate_confidence(text)
            
            return text, confidence
        except Exception as e:
            raise OCRException(f"Error processing image: {str(e)}")

    def process_numpy_array(self, image_array: np.ndarray) -> Tuple[str, float]:
        """
        Process a numpy array (image) and extract text
        
        Args:
            image_array: Numpy array representing an image
            
        Returns:
            Tuple of (extracted_text, confidence_score)
        """
        try:
            preprocessed = self._preprocess_image(image_array)
            text = pytesseract.image_to_string(preprocessed)
            confidence = self._estimate_confidence(text)
            
            return text, confidence
        except Exception as e:
            raise OCRException(f"Error processing image array: {str(e)}")

    def extract_medicines(self, ocr_text: str) -> List[str]:
        """
        Extract potential medicine names from OCR text
        
        Args:
            ocr_text: Text extracted from OCR
            
        Returns:
            List of potential medicine names
        """
        # Simple medicine name extraction (filtered by common patterns)
        lines = ocr_text.split('\n')
        medicines = []
        
        # Common medicine name patterns and indicators
        medicine_keywords = ['mg', 'tablet', 'capsule', 'dose', 'rx', 'prescription']
        
        for line in lines:
            # Clean line
            clean_line = line.strip()
            
            # Skip very short or very long lines
            if len(clean_line) < 3 or len(clean_line) > 100:
                continue
            
            # Check for medicine indicators
            if any(keyword in clean_line.lower() for keyword in medicine_keywords):
                medicines.append(clean_line)
        
        return medicines

    def extract_dosages(self, ocr_text: str) -> List[str]:
        """
        Extract dosage information from OCR text
        
        Args:
            ocr_text: Text extracted from OCR
            
        Returns:
            List of potential dosages
        """
        import re
        
        # Pattern for dosages (number + unit)
        dosage_pattern = r'(\d+(?:\.\d+)?)\s*(mg|ml|g|ug|mcg|%)\b'
        matches = re.findall(dosage_pattern, ocr_text, re.IGNORECASE)
        
        dosages = [f"{amount}{unit}" for amount, unit in matches]
        return dosages

    def clean_text(self, text: str) -> str:
        """
        Clean extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        import re
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters while keeping important ones
        text = re.sub(r'[^\w\s\-\/\.]', '', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text

    def _load_image(self, image_path: str) -> np.ndarray:
        """Load image from file"""
        image = cv2.imread(image_path)
        if image is None:
            raise OCRException(f"Could not load image: {image_path}")
        return image

    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR results
        
        Applies: grayscale conversion, noise reduction, thresholding
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray, h=10)

        # Apply thresholding for better contrast
        _, thresh = cv2.threshold(denoised, 150, 255, cv2.THRESH_BINARY)

        # Increase contrast
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        return morph

    def _estimate_confidence(self, text: str) -> float:
        """
        Estimate confidence score of OCR extraction
        
        Args:
            text: Extracted text
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        # Simple confidence estimation based on text quality
        if not text.strip():
            return 0.0
        
        # Check for readable characters
        readable_chars = sum(1 for c in text if c.isalnum())
        total_chars = len(text.strip())
        
        if total_chars == 0:
            return 0.0
        
        confidence = readable_chars / total_chars
        return min(confidence, 1.0)


class OCRException(Exception):
    """Custom exception for OCR processing errors"""
    pass
