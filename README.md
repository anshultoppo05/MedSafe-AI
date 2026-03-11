# MedSafe AI - Medication Safety Assistant

A comprehensive, modular medication safety application built with Streamlit, providing medicine information lookup, drug interaction detection, symptom guidance, and OCR-based prescription processing.

## 🎯 Features

- **💊 Medicine Lookup** - Search and view detailed medication information
- **⚠️ Drug Interaction Checker** - Detect dangerous medication interactions with risk scoring
- **🩺 Symptom Advisor** - Rule-based guidance on medication side effects and symptoms
- **📸 Prescription OCR** - Extract medication information from prescription images
- **🔬 Risk Assessment Engine** - Deterministic safety rules and emergency detection
- **🎨 Interactive Web UI** - User-friendly Streamlit interface

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Virtual environment setup (done)
- All dependencies installed from `requirements.txt`

### Activate Environment

```bash
cd "/Users/anshultoppo/Desktop/projects/medsafe final"
source activate_medsafe.sh
```

### Run the Application

```bash
streamlit run streamlit_app.py
```

The application will open at `http://localhost:8501`

### Run Verification Tests

```bash
python verify_imports.py
```

## 📁 Project Structure

```
medsafe final/
├── src/                          # Core modules
│   ├── __init__.py
│   ├── med_db.py                # Medicine database
│   ├── ocr_utils.py             # OCR processing
│   ├── risk_engine.py           # Risk assessment
│   └── symptom.py               # Symptom advisor
├── config.py                     # Configuration management
├── streamlit_app.py              # Main UI application
├── requirements.txt              # Python dependencies
├── SETUP.md                      # Setup guide
├── ARCHITECTURE.md               # Technical architecture
└── README.md                     # This file
```

## 🔧 Configuration

Configuration is centralized in `config.py`:

```python
from config import get_config

# Get specific configuration
ocr_config = get_config("ocr")
risk_config = get_config("risk")

# Get all configurations
all_config = get_config()
```

### Configuration Sections:
- `OCR_CONFIG` - OCR and image processing settings
- `RISK_CONFIG` - Risk assessment thresholds
- `SYMPTOM_CONFIG` - Symptom analyzer settings
- `DATABASE_CONFIG` - Database settings
- `APP_CONFIG` - Application settings
- `LOGGING_CONFIG` - Logging configuration

## 📖 Module Documentation

### med_db.py - Medicine Database
Manages medicine information and drug interactions

```python
from src.med_db import MedicineDatabase

db = MedicineDatabase()
med = db.get_medicine("Ibuprofen")
interactions = db.get_interactions(["Ibuprofen", "Aspirin"])
```

### ocr_utils.py - OCR Processor
Extracts text from prescription images

```python
from src.ocr_utils import OCRProcessor

ocr = OCRProcessor()
text, confidence = ocr.process_image("prescription.jpg")
medicines = ocr.extract_medicines(text)
dosages = ocr.extract_dosages(text)
```

### risk_engine.py - Risk Assessment
Evaluates medication safety and interactions

```python
from src.risk_engine import RiskEngine

engine = RiskEngine(db)
assessment = engine.assess_medications(["Ibuprofen", "Aspirin"])
print(assessment.risk_level)  # RiskLevel.HIGH_RISK
```

### symptom.py - Symptom Advisor
Provides rule-based symptom guidance

```python
from src.symptom import SymptomAdvisor

advisor = SymptomAdvisor()
advice = advisor.analyze_symptom("stomach upset")
print(advice.management_steps)
```

## 🔐 System Requirements for OCR

For prescription OCR to work fully, install the Tesseract-OCR system package:

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download from GitHub: https://github.com/UB-Mannheim/tesseract/wiki

## 🤖 AI Integration (Optional)

To use Ollama for AI-powered analysis:

1. Install Ollama: https://ollama.ai
2. Start Ollama service
3. Pull a model: `ollama pull llama2`

The Ollama client is already installed and ready to use in the environment.

## 💻 Development

### Running Tests

```bash
# Test imports
python verify_imports.py

# Test individual modules
python -c "from src.med_db import MedicineDatabase; db = MedicineDatabase(); print('✓ med_db works')"
```

### Adding New Features

1. **Add Medicine to Database:**
   - Edit `_initialize_sample_data()` in `src/med_db.py`
   - Or use `db.add_medicine(medicine)` method

2. **Add Drug Interaction:**
   - Create `DrugInteraction` object
   - Add via `db.add_interaction(interaction)`

3. **Add Symptom Rules:**
   - Edit symptom rules in `src/symptom.py`
   - Follow existing pattern in `_initialize_symptom_rules()`

4. **Customize UI:**
   - Modify `streamlit_app.py` tabs and layouts
   - Update styling in set_page_config()

## ⚠️ Important Disclaimer

**Medical Disclaimer:**

MedSafe AI is an informational tool designed to assist users in understanding medications and drug interactions. It should **NOT** be used as a substitute for professional medical advice.

- Always consult a licensed healthcare provider before starting, stopping, or changing medications
- In case of medical emergency, call emergency services (911) immediately
- The information provided is based on general knowledge and may not reflect individual patient circumstances

## 🐛 Troubleshooting

### Streamlit App Won't Start
```bash
# Ensure environment is activated
source activate_medsafe.sh

# Clear Streamlit cache if needed
streamlit cache clear

# Run with verbose output
streamlit run streamlit_app.py --logger.level=debug
```

### OCR Not Working
```bash
# Verify Tesseract is installed
which tesseract  # macOS/Linux
tesseract --version

# Update OCR path in config if needed
# Edit TESSERACT_PATH in config.py
```

### Import Errors
```bash
# Verify virtual environment is activated
which python  # Should show medsafe_env path

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📚 Additional Resources

- **Streamlit Documentation**: https://docs.streamlit.io
- **OpenCV**: https://docs.opencv.org
- **PyTesseract**: https://github.com/madmaze/pytesseract
- **RapidFuzz**: https://maxbachmann.github.io/RapidFuzz
- **Ollama**: https://ollama.ai

## 🤝 Contributing

To contribute to MedSafe AI:

1. Create a new branch for your feature
2. Follow the existing code structure and style
3. Add docstrings to all functions
4. Test thoroughly before submitting
5. Update documentation as needed

## 📄 License

MedSafe AI is provided as-is for educational and informational purposes.

## 👨‍💼 About

MedSafe AI is a comprehensive medication safety platform designed to help users:
- Understand their medications
- Detect dangerous drug interactions
- Make informed medication decisions
- Process and analyze prescriptions

**Version**: 1.0.0  
**Last Updated**: March 11, 2026  
**Status**: Production Ready

## 📞 Support

For issues, suggestions, or contributions:
1. Check the ARCHITECTURE.md for technical details
2. Review existing code in the src/ directory
3. Consult the troubleshooting section above

---

**Remember**: Always consult healthcare professionals for medical advice. MedSafe AI is a tool to assist, not replace, professional medical guidance.
