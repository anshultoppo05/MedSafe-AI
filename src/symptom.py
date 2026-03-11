"""
symptom.py - Rule-Based Symptom Advice and Guidance Logic

This module provides rule-based advice for medication-related symptoms,
side effects, and health concerns. Offers guidance on when to seek
medical attention and how to manage medication side effects.
"""

from typing import List, Dict, Tuple
from enum import Enum
from dataclasses import dataclass


class SymptomSeverity(Enum):
    """Symptom severity classification"""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    EMERGENCY = "emergency"


class SymptomCategory(Enum):
    """Symptom categories"""
    GASTROINTESTINAL = "gastrointestinal"
    NEUROLOGICAL = "neurological"
    ALLERGIC = "allergic"
    CARDIOVASCULAR = "cardiovascular"
    RESPIRATORY = "respiratory"
    DERMATOLOGICAL = "dermatological"
    OTHER = "other"


@dataclass
class SymptomAdvice:
    """Data class for symptom advice"""
    symptom: str
    category: SymptomCategory
    severity: SymptomSeverity
    description: str
    management_steps: List[str]
    when_to_seek_help: str
    related_medications: List[str]


class SymptomAdvisor:
    """
    Rule-based symptom advisor for medication-related concerns.
    
    Provides:
    - Symptom classification and severity assessment
    - Home management recommendations
    - Guidance on when to seek medical attention
    - Side effect information for medications
    """

    def __init__(self):
        """Initialize symptom advisor with rule base"""
        self.symptom_rules = self._initialize_symptom_rules()
        self.emergency_symptoms = self._initialize_emergency_symptoms()

    def analyze_symptom(self, symptom: str, 
                       medications: List[str] = None) -> SymptomAdvice:
        """
        Analyze a reported symptom and provide advice
        
        Args:
            symptom: Description of symptom
            medications: List of medications patient is taking
            
        Returns:
            SymptomAdvice with recommendations
        """
        # Check if emergency symptom
        is_emergency = self._check_emergency_symptoms(symptom)
        
        # Find matching symptom rule
        matched_rule = self._find_matching_rule(symptom)
        
        if not matched_rule:
            return self._create_unknown_symptom_advice(symptom)

        # Determine severity
        severity = self._assess_severity(symptom, is_emergency)
        
        # Get management steps
        management_steps = self._get_management_steps(
            matched_rule, severity, medications
        )
        
        # Get urgent care guidance
        urgent_guidance = self._get_urgent_care_guidance(severity)

        return SymptomAdvice(
            symptom=symptom,
            category=matched_rule["category"],
            severity=severity,
            description=matched_rule.get("description", ""),
            management_steps=management_steps,
            when_to_seek_help=urgent_guidance,
            related_medications=matched_rule.get("common_causes", [])
        )

    def get_medication_side_effects(self, medication_name: str) -> Dict:
        """
        Get common side effects for a medication
        
        Args:
            medication_name: Name of medication
            
        Returns:
            Dictionary with side effect information
        """
        side_effects_db = {
            "Ibuprofen": {
                "common": ["Stomach upset", "Heartburn", "Dizziness"],
                "management": [
                    "Take with food or milk",
                    "Stay well hydrated",
                    "Rest in a dark, quiet room for dizziness"
                ],
                "serious": ["Severe stomach pain", "Black/tarry stools", "Chest pain"]
            },
            "Aspirin": {
                "common": ["Stomach upset", "Heartburn"],
                "management": [
                    "Take with food",
                    "Use enteric-coated version if available",
                    "Avoid on empty stomach"
                ],
                "serious": ["Bleeding", "Rash", "Wheezing"]
            },
            "Amoxicillin": {
                "common": ["Nausea", "Diarrhea", "Rash"],
                "management": [
                    "Take with food",
                    "Eat probiotic-rich foods",
                    "Avoid dairy products within 2 hours",
                    "Complete full course even if feeling better"
                ],
                "serious": ["Severe rash", "Difficulty breathing", "Swelling"]
            },
            "Lisinopril": {
                "common": ["Dry cough", "Dizziness", "Fatigue"],
                "management": [
                    "Stay hydrated",
                    "Rise slowly from sitting/lying down",
                    "Cough usually decreases over time",
                    "Report persistent cough to doctor"
                ],
                "serious": ["Chest pain", "Severe dizziness", "Fainting"]
            }
        }

        if medication_name not in side_effects_db:
            return {
                "found": False,
                "message": f"Side effects database missing for {medication_name}"
            }

        effects = side_effects_db[medication_name]
        return {
            "found": True,
            "medication": medication_name,
            "common_side_effects": effects["common"],
            "management_tips": effects["management"],
            "serious_side_effects": effects["serious"],
            "seek_immediate_help_for": effects["serious"]
        }

    def is_drug_side_effect(self, symptom: str, 
                           medication: str) -> Tuple[bool, float]:
        """
        Check if symptom is likely a side effect of medication
        
        Args:
            symptom: Symptom description
            medication: Medication name
            
        Returns:
            Tuple of (is_likely_side_effect, confidence)
        """
        side_effects = self.get_medication_side_effects(medication)
        
        if not side_effects.get("found"):
            return False, 0.0

        symptom_lower = symptom.lower()
        
        # Check all side effects
        all_effects = (side_effects.get("common_side_effects", []) + 
                      side_effects.get("serious_side_effects", []))
        
        for effect in all_effects:
            if symptom_lower in effect.lower() or effect.lower() in symptom_lower:
                # Higher confidence for exact matches
                confidence = 0.9 if symptom_lower == effect.lower() else 0.7
                return True, confidence
        
        return False, 0.0

    def _initialize_symptom_rules(self) -> List[Dict]:
        """Initialize symptom classification rules"""
        return [
            {
                "keywords": ["nausea", "vomiting", "upset stomach", "nauseous"],
                "category": SymptomCategory.GASTROINTESTINAL,
                "description": "Digestive system discomfort",
                "common_causes": ["Ibuprofen", "Aspirin", "Amoxicillin"],
            },
            {
                "keywords": ["headache", "dizziness", "dizzy", "vertigo"],
                "category": SymptomCategory.NEUROLOGICAL,
                "description": "Neurological symptoms",
                "common_causes": ["Lisinopril", "Ibuprofen"],
            },
            {
                "keywords": ["rash", "hives", "itching", "skin"],
                "category": SymptomCategory.DERMATOLOGICAL,
                "description": "Skin reaction",
                "common_causes": ["Amoxicillin", "Aspirin"],
            },
            {
                "keywords": ["cough", "dry cough", "throat"],
                "category": SymptomCategory.RESPIRATORY,
                "description": "Respiratory symptoms",
                "common_causes": ["Lisinopril"],
            },
            {
                "keywords": ["chest pain", "chest", "palpitation", "heart"],
                "category": SymptomCategory.CARDIOVASCULAR,
                "description": "Cardiovascular symptom",
                "common_causes": [],
            },
            {
                "keywords": ["diarrhea", "loose stool", "constipation"],
                "category": SymptomCategory.GASTROINTESTINAL,
                "description": "Bowel-related symptoms",
                "common_causes": ["Amoxicillin"],
            },
        ]

    def _initialize_emergency_symptoms(self) -> List[str]:
        """Initialize list of emergency symptoms"""
        return [
            "difficulty breathing",
            "chest pain",
            "severe allergic reaction",
            "anaphylaxis",
            "loss of consciousness",
            "severe bleeding",
            "severe allergic",
            "throat closing",
            "severe swelling",
            "poisoning",
            "overdose",
        ]

    def _check_emergency_symptoms(self, symptom: str) -> bool:
        """Check if symptom is an emergency"""
        symptom_lower = symptom.lower()
        return any(emergency in symptom_lower 
                  for emergency in self.emergency_symptoms)

    def _find_matching_rule(self, symptom: str) -> Dict:
        """Find matching symptom rule"""
        symptom_lower = symptom.lower()
        
        for rule in self.symptom_rules:
            for keyword in rule["keywords"]:
                if keyword in symptom_lower:
                    return rule
        
        return None

    def _assess_severity(self, symptom: str, 
                        is_emergency: bool) -> SymptomSeverity:
        """Assess symptom severity"""
        if is_emergency:
            return SymptomSeverity.EMERGENCY
        
        # Check for severity keywords
        if any(word in symptom.lower() 
               for word in ["severe", "worst", "unbearable", "acute"]):
            return SymptomSeverity.SEVERE
        
        if any(word in symptom.lower() 
               for word in ["moderate", "significant", "notable"]):
            return SymptomSeverity.MODERATE
        
        return SymptomSeverity.MILD

    def _get_management_steps(self, rule: Dict, severity: SymptomSeverity,
                             medications: List[str] = None) -> List[str]:
        """Get management steps for symptom"""
        steps = []
        
        if severity == SymptomSeverity.EMERGENCY:
            steps.append("Call emergency services (911)")
            return steps
        
        # Category-based recommendations
        category = rule["category"]
        
        if category == SymptomCategory.GASTROINTESTINAL:
            steps.extend([
                "Stay hydrated with clear fluids",
                "Eat bland foods (crackers, rice, toast)",
                "Avoid fatty or spicy foods",
                "If using NSAIDs, take with food"
            ])
        
        elif category == SymptomCategory.NEUROLOGICAL:
            steps.extend([
                "Rest in a quiet, dark room",
                "Drink plenty of water",
                "Avoid sudden movements",
                "Rise slowly when getting up"
            ])
        
        elif category == SymptomCategory.DERMATOLOGICAL:
            steps.extend([
                "Wash affected area gently with mild soap",
                "Apply unscented moisturizer",
                "Avoid scratching",
                "Consider antihistamine for itching"
            ])
        
        elif category == SymptomCategory.RESPIRATORY:
            steps.extend([
                "Get fresh air if possible",
                "Use honey to soothe throat",
                "Stay hydrated",
                "Use humidifier if available"
            ])
        
        return steps

    def _get_urgent_care_guidance(self, severity: SymptomSeverity) -> str:
        """Get urgent care guidance based on severity"""
        guidance_map = {
            SymptomSeverity.EMERGENCY: "SEEK EMERGENCY CARE NOW - Call 911",
            SymptomSeverity.SEVERE: "Contact healthcare provider urgently (same day)",
            SymptomSeverity.MODERATE: "Contact healthcare provider within 24-48 hours",
            SymptomSeverity.MILD: "Monitor symptom. Contact if worsens.",
        }
        return guidance_map.get(severity, "Contact healthcare provider")

    def _create_unknown_symptom_advice(self, symptom: str) -> SymptomAdvice:
        """Create advice for unrecognized symptom"""
        return SymptomAdvice(
            symptom=symptom,
            category=SymptomCategory.OTHER,
            severity=SymptomSeverity.MODERATE,
            description="Symptom not recognized in database",
            management_steps=[
                "Monitor the symptom closely",
                "Note when it started and how it progresses",
                "Contact healthcare provider if symptoms persist"
            ],
            when_to_seek_help="Contact healthcare provider for guidance",
            related_medications=[]
        )
