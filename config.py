"""
config.py - Application Configuration

Centralized configuration for MedSafe AI application.
Includes settings for OCR, risk assessment, and other components.
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.absolute()
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"

# OCR Configuration
OCR_CONFIG = {
    "tesseract_path": os.getenv("TESSERACT_PATH", None),
    "image_preprocessing": True,
    "confidence_threshold": 0.5,
    "supported_formats": ["jpg", "jpeg", "png", "bmp", "tiff"],
    "max_image_size": 10 * 1024 * 1024,  # 10MB
}

# Risk Assessment Configuration
RISK_CONFIG = {
    "critical_threshold": 0.9,
    "high_risk_threshold": 0.75,
    "moderate_risk_threshold": 0.5,
    "low_risk_threshold": 0.25,
    "enable_age_checks": True,
    "enable_contraindication_checks": True,
}

# Symptom Advisor Configuration
SYMPTOM_CONFIG = {
    "enable_nlp_analysis": False,  # Set to True if NLP models available
    "confidence_threshold": 0.6,
    "emergency_response_enabled": True,
}

# Database Configuration
DATABASE_CONFIG = {
    "use_sample_data": True,
    "database_path": DATA_DIR / "medicines.db",
    "cache_enabled": True,
}

# Application Configuration
APP_CONFIG = {
    "app_name": "MedSafe AI",
    "version": "1.0.0",
    "debug_mode": os.getenv("DEBUG", "False").lower() == "true",
    "log_level": os.getenv("LOG_LEVEL", "INFO"),
    "theme": "light",
    "max_upload_size": 10 * 1024 * 1024,  # 10MB
}

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(funcName)s() - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "detailed",
            "filename": PROJECT_ROOT / "logs" / "medsafe.log",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
        "src": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
}

def get_config(section: str = None) -> dict:
    """
    Get configuration dictionary
    
    Args:
        section: Specific configuration section or None for all
        
    Returns:
        Configuration dictionary
    """
    if section == "ocr":
        return OCR_CONFIG
    elif section == "risk":
        return RISK_CONFIG
    elif section == "symptom":
        return SYMPTOM_CONFIG
    elif section == "database":
        return DATABASE_CONFIG
    elif section == "app":
        return APP_CONFIG
    elif section == "logging":
        return LOGGING_CONFIG
    else:
        # Return all configurations
        return {
            "ocr": OCR_CONFIG,
            "risk": RISK_CONFIG,
            "symptom": SYMPTOM_CONFIG,
            "database": DATABASE_CONFIG,
            "app": APP_CONFIG,
            "logging": LOGGING_CONFIG,
        }
