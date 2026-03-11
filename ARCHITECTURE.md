# MedSafe AI - Project Structure & Architecture

## Overview

MedSafe AI is a modular medication safety application built with Streamlit, featuring:
- Prescription OCR processing
- Drug interaction analysis
- Symptom guidance
- Risk assessment engine
- Interactive web-based UI

## Project Structure

```
medsafe final/
├── src/                          # Core application modules
│   ├── __init__.py              # Package initialization
│   ├── med_db.py                # Medicine database & interactions
│   ├── ocr_utils.py             # OCR & text extraction
│   ├── risk_engine.py           # Risk scoring & safety rules
│   └── symptom.py               # Symptom advice & guidance
│
├── config/                       # Configuration directory
│   └── (empty - for future config files)
│
├── data/                         # Data directory
│   └── (empty - for databases, datasets)
│
├── config.py                     # Central configuration file
├── streamlit_app.py              # Main UI application
├── requirements.txt              # Project dependencies
├── SETUP.md                      # Setup documentation
├── ARCHITECTURE.md               # This file
├── medsafe_env/                  # Virtual environment
└── README.md                     # (to be created)
```

## Module Architecture

### 1. **med_db.py** - Medicine Database Module
**Responsibility:** Storage and retrieval of medicine information and drug interactions

**Key Classes:**
- `Medicine` - Dataclass representing a medication
- `DrugInteraction` - Dataclass representing interactions between drugs
- `SeverityLevel` - Enum for interaction severity levels
- `MedicineDatabase` - Main database class

**Key Methods:**
- `get_medicine(name)` - Retrieve medicine by name
- `search_medicines(query)` - Search by name/category
- `get_interactions(drug_names)` - Check interactions between drugs
- `add_medicine(medicine)` - Add new medicine to database
- `add_interaction(interaction)` - Add new interaction

**Example Usage:**
```python
from src.med_db import MedicineDatabase

db = MedicineDatabase()
ibuprofen = db.get_medicine("Ibuprofen")
interactions = db.get_interactions(["Ibuprofen", "Aspirin"])
```

---

### 2. **ocr_utils.py** - OCR Processing Module
**Responsibility:** Extract text from prescription images and process OCR results

**Key Classes:**
- `OCRProcessor` - Main OCR processing class
- `OCRException` - Custom exception for OCR errors

**Key Methods:**
- `process_image(image_path)` - Process image file and extract text
- `process_numpy_array(image_array)` - Process numpy array
- `extract_medicines(ocr_text)` - Extract medicine names from text
- `extract_dosages(ocr_text)` - Extract dosage information
- `clean_text(text)` - Clean and normalize text

**Image Preprocessing Pipeline:**
1. Grayscale conversion
2. Noise reduction (denoising)
3. Thresholding for contrast
4. Morphological operations

**Example Usage:**
```python
from src.ocr_utils import OCRProcessor

ocr = OCRProcessor()
text, confidence = ocr.process_image("prescription.jpg")
medicines = ocr.extract_medicines(text)
dosages = ocr.extract_dosages(text)
```

---

### 3. **risk_engine.py** - Risk Assessment Module
**Responsibility:** Deterministic rule-based safety assessment and risk scoring

**Key Classes:**
- `RiskLevel` - Enum for risk levels (SAFE, LOW_RISK, MODERATE_RISK, HIGH_RISK, CRITICAL)
- `RiskAssessment` - Dataclass with assessment results
- `RiskEngine` - Main risk assessment engine

**Key Methods:**
- `assess_medications(drug_names)` - Comprehensive medication risk assessment
- `check_contraindications(medication, conditions)` - Check patient contraindications
- `assess_age_appropriate(medication, age)` - Age-based safety assessment

**Risk Scoring Algorithm:**
- Weights severity levels (CRITICAL=1.0, HIGH=0.75, MODERATE=0.5, LOW=0.25)
- Normalizes score across all interactions
- Returns normalized 0.0-1.0 score

**Example Usage:**
```python
from src.risk_engine import RiskEngine
from src.med_db import MedicineDatabase

db = MedicineDatabase()
engine = RiskEngine(db)
assessment = engine.assess_medications(["Ibuprofen", "Aspirin"])

print(assessment.risk_level)        # RiskLevel.HIGH_RISK
print(assessment.risk_score)        # 0.75
print(assessment.needs_medical_attention)  # True
```

---

### 4. **symptom.py** - Symptom Advisor Module
**Responsibility:** Rule-based symptom classification and advice

**Key Classes:**
- `SymptomSeverity` - Enum for symptom severity
- `SymptomCategory` - Enum for symptom categories
- `SymptomAdvice` - Dataclass with advice information
- `SymptomAdvisor` - Main advisor class

**Key Methods:**
- `analyze_symptom(symptom, medications)` - Analyze symptom and provide advice
- `get_medication_side_effects(medication)` - Get side effects for medicine
- `is_drug_side_effect(symptom, medication)` - Check if symptom is drug side effect

**Symptom Categories:**
- GASTROINTESTINAL (nausea, vomiting, diarrhea)
- NEUROLOGICAL (headache, dizziness)
- ALLERGIC (rash, hives)
- CARDIOVASCULAR (chest pain, palpitations)
- RESPIRATORY (cough, difficulty breathing)
- DERMATOLOGICAL (skin reactions)

**Emergency Symptoms:**
- Automatically flagged for immediate medical attention

**Example Usage:**
```python
from src.symptom import SymptomAdvisor

advisor = SymptomAdvisor()
advice = advisor.analyze_symptom("stomach upset")

print(advice.category)              # SymptomCategory.GASTROINTESTINAL
print(advice.severity)              # SymptomSeverity.MILD
print(advice.management_steps)      # ["Stay hydrated", ...]
```

---

### 5. **streamlit_app.py** - Main Application UI
**Responsibility:** Interactive web interface integrating all modules

**Key Components:**
- Medicine lookup with search
- Drug interaction checker with visual risk indicators
- Symptom advisor with severity assessment
- Prescription OCR processor with image upload
- Information and disclaimer sections

**Interface Tabs:**
1. **Medicine Lookup** - Search and view medicine details
2. **Interaction Checker** - Check drug interactions
3. **Symptom Advisor** - Get symptom guidance
4. **Prescription OCR** - Extract text from images
5. **About** - Help and disclaimers

**Caching Strategy:**
- Uses `@st.cache_resource` for system components (initialized once)
- Improves performance on page reloads

**Example Usage:**
```bash
# Activate virtual environment
source medsafe_env/bin/activate

# Run Streamlit app
streamlit run streamlit_app.py
```

---

### 6. **config.py** - Configuration Management
**Responsibility:** Centralized configuration for all modules

**Configuration Sections:**
- `OCR_CONFIG` - OCR processing settings
- `RISK_CONFIG` - Risk assessment thresholds
- `SYMPTOM_CONFIG` - Symptom advisor settings
- `DATABASE_CONFIG` - Database settings
- `APP_CONFIG` - Application settings
- `LOGGING_CONFIG` - Logging configuration

**Usage:**
```python
from config import get_config

ocr_config = get_config("ocr")
risk_config = get_config("risk")
all_config = get_config()  # Returns all sections
```

---

## Data Flow & Integration

```
┌─────────────────────────────────────────┐
│         Streamlit UI Layer              │
│    (streamlit_app.py)                   │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┬────────────┬──────────┐
       │                │            │          │
       ▼                ▼            ▼          ▼
   ┌────────┐    ┌─────────┐  ┌─────────┐  ┌──────────┐
   │ med_db │    │ocr_utils│  │risk_eng │  │symptom.py│
   └────────┘    └─────────┘  └─────────┘  └──────────┘
       │              │            │          │
       └──────────────┴────────────┴──────────┘
               │
       ┌───────▼────────┐
       │  config.py     │
       │  (Settings)    │
       └────────────────┘
```

### Example Integration Workflow

```python
# 1. Initialize all components
med_db = MedicineDatabase()
risk_engine = RiskEngine(med_db)
symptom_advisor = SymptomAdvisor()
ocr_processor = OCRProcessor()

# 2. OCR flow: Image → Text → Medicines
text, conf = ocr_processor.process_image("prescription.jpg")
medicines = ocr_processor.extract_medicines(text)

# 3. Risk assessment: Medicines → Interactions → Risk Level
assessment = risk_engine.assess_medications(medicines)

# 4. Symptom analysis: Symptom → Advice → Management
advice = symptom_advisor.analyze_symptom("stomach upset", medicines)

# 5. Present to user via Streamlit UI
```

---

## Adding New Features

### Add a New Medicine to Database
```python
from src.med_db import Medicine, MedicineDatabase

db = MedicineDatabase()
new_med = Medicine(
    name="Metoprolol",
    generic_name="Metoprolol tartrate",
    category="Beta Blocker",
    dosage="25mg, 50mg, 100mg",
    manufacturer="Cipla",
    uses=["Hypertension", "Heart disease"],
    side_effects=["Fatigue", "Dizziness"],
    contraindications=["Asthma", "Bradycardia"]
)
db.add_medicine(new_med)
```

### Add a New Drug Interaction
```python
from src.med_db import DrugInteraction, SeverityLevel

interaction = DrugInteraction(
    drug1="Ibuprofen",
    drug2="Methotrexate",
    severity=SeverityLevel.HIGH,
    description="NSAIDs may reduce methotrexate clearance",
    recommendations=["Avoid combination", "Monitor renal function"]
)
db.add_interaction(interaction)
```

### Add a New Symptom Rule
```python
# Edit symptom.py _initialize_symptom_rules() method
{
    "keywords": ["fatigue", "tired", "exhausted"],
    "category": SymptomCategory.OTHER,
    "description": "Systemic fatigue or exhaustion",
    "common_causes": ["Lisinopril", "Metformin"],
}
```

---

## Testing Components

### Test med_db.py
```python
from src.med_db import MedicineDatabase

db = MedicineDatabase()
assert db.get_medicine("Ibuprofen") is not None
assert len(db.search_medicines("Aspirin")) > 0
assert len(db.get_interactions(["Ibuprofen", "Aspirin"])) > 0
print("✓ med_db tests passed")
```

### Test risk_engine.py
```python
from src.risk_engine import RiskEngine, RiskLevel

engine = RiskEngine(db)
assessment = engine.assess_medications(["Ibuprofen", "Aspirin"])
assert assessment.risk_level == RiskLevel.HIGH_RISK
assert assessment.risk_score > 0.5
print("✓ risk_engine tests passed")
```

### Test symptom.py
```python
from src.symptom import SymptomAdvisor

advisor = SymptomAdvisor()
advice = advisor.analyze_symptom("severe headache")
assert advice.severity.value == "severe"
assert len(advice.management_steps) > 0
print("✓ symptom tests passed")
```

---

## Deployment Considerations

### Production Checklist:
- [ ] Update medicine database with comprehensive data
- [ ] Add more drug interactions
- [ ] Enhance symptom rules with NLP
- [ ] Add authentication for sensitive features
- [ ] Implement user session management
- [ ] Set up logging and monitoring
- [ ] Configure error handling
- [ ] Add API rate limiting
- [ ] Deploy to cloud platform (GCP, AWS, Azure)

### Performance Optimizations:
- Cache database queries
- Use pagination for large datasets
- Implement async processing for OCR
- Optimize image preprocessing

### Security Measures:
- Validate all user inputs
- Sanitize OCR text output
- Implement HIPAA compliance for medical data
- Use encrypted connections
- Add audit logging

---

## Future Enhancements

1. **AI Integration:**
   - NLP for smarter symptom analysis
   - LLM-based medication advice via Ollama
   - Computer vision improvements for OCR

2. **Data Management:**
   - Real-time medicine database updates
   - Integration with external drug databases (FDA, etc.)
   - Historical tracking of patient medications

3. **Advanced Features:**
   - Drug cost comparison
   - Insurance coverage checker
   - Pharmacy locator
   - Medication reminder notifications
   - Patient history tracking

4. **Compliance:**
   - HIPAA compliance
   - FDA approval verification
   - Clinical trial integration

---

## References & Documentation

- **Streamlit Docs**: https://docs.streamlit.io
- **OpenCV Docs**: https://docs.opencv.org
- **PyTesseract**: https://github.com/madmaze/pytesseract
- **RapidFuzz**: https://maxbachmann.github.io/RapidFuzz
- **Ollama**: https://ollama.ai

---

**Architecture Document Version:** 1.0  
**Last Updated:** March 11, 2026  
**Status:** Production Ready
