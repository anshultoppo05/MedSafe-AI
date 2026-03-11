"""
MedSafe AI - Medication Safety and Analysis System
A modular application for prescription analysis, drug interaction detection, 
and safety risk assessment using OCR, fuzzy matching, and AI.
"""

__version__ = "1.0.0"
__author__ = "MedSafe AI Team"

from .med_db import MedicineDatabase
from .symptom import SymptomAdvisor  
from .risk_engine import RiskEngine
from .ocr_utils import OCRProcessor

__all__ = [
    "MedicineDatabase",
    "SymptomAdvisor",
    "RiskEngine",
    "OCRProcessor",
]
