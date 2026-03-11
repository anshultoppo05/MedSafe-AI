"""
risk_engine.py - Emergency Risk Scoring and Safety Rules Engine

This module implements risk scoring algorithms for medication interactions 
and safety assessment. Provides deterministic rules-based evaluation of 
potential health risks.
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum
from .med_db import MedicineDatabase, SeverityLevel


class RiskLevel(Enum):
    """Risk level classification"""
    SAFE = "safe"
    LOW_RISK = "low_risk"
    MODERATE_RISK = "moderate_risk"
    HIGH_RISK = "high_risk"
    CRITICAL = "critical"


@dataclass
class RiskAssessment:
    """Data class for risk assessment results"""
    risk_level: RiskLevel
    risk_score: float  # 0.0 to 1.0
    interactions: List[Dict]
    warnings: List[str]
    recommendations: List[str]
    needs_medical_attention: bool


class RiskEngine:
    """
    Risk assessment engine for medication safety evaluation.
    
    Implements deterministic rules for:
    - Drug interaction detection
    - Severity scoring
    - Emergency risk identification
    - Safety recommendations
    """

    # Risk scoring weights for different factors
    INTERACTION_WEIGHTS = {
        SeverityLevel.CRITICAL: 1.0,
        SeverityLevel.HIGH: 0.75,
        SeverityLevel.MODERATE: 0.5,
        SeverityLevel.LOW: 0.25,
    }

    # Severity mapping for risk level determination
    SEVERITY_TO_RISK = {
        SeverityLevel.CRITICAL: RiskLevel.CRITICAL,
        SeverityLevel.HIGH: RiskLevel.HIGH_RISK,
        SeverityLevel.MODERATE: RiskLevel.MODERATE_RISK,
        SeverityLevel.LOW: RiskLevel.LOW_RISK,
    }

    def __init__(self, med_db: MedicineDatabase):
        """
        Initialize risk engine with medicine database
        
        Args:
            med_db: MedicineDatabase instance
        """
        self.med_db = med_db

    def assess_medications(self, medication_names: List[str]) -> RiskAssessment:
        """
        Assess risk level for a list of medications
        
        Args:
            medication_names: List of medication names to assess
            
        Returns:
            RiskAssessment object with detailed risk information
        """
        # Validate medications
        validated_meds = self._validate_medications(medication_names)
        
        if not validated_meds:
            return RiskAssessment(
                risk_level=RiskLevel.SAFE,
                risk_score=0.0,
                interactions=[],
                warnings=["No recognized medications provided"],
                recommendations=["Provide valid medication names"],
                needs_medical_attention=False
            )

        # Check for interactions
        interactions = self.med_db.get_interactions(validated_meds)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(interactions)
        
        # Determine risk level
        risk_level = self._determine_risk_level(risk_score, interactions)
        
        # Generate warnings and recommendations
        warnings = self._generate_warnings(interactions, validated_meds)
        recommendations = self._generate_recommendations(interactions)
        
        # Determine if medical attention is needed
        needs_attention = risk_level in [
            RiskLevel.CRITICAL, 
            RiskLevel.HIGH_RISK
        ]

        return RiskAssessment(
            risk_level=risk_level,
            risk_score=risk_score,
            interactions=[
                {
                    "drug1": i.drug1,
                    "drug2": i.drug2,
                    "severity": i.severity.value,
                    "description": i.description
                }
                for i in interactions
            ],
            warnings=warnings,
            recommendations=recommendations,
            needs_medical_attention=needs_attention
        )

    def check_contraindications(self, medication_name: str, 
                               patient_conditions: List[str]) -> Dict:
        """
        Check if medication has contraindications for patient conditions
        
        Args:
            medication_name: Name of medication
            patient_conditions: List of patient medical conditions
            
        Returns:
            Dictionary with contraindication information
        """
        medicine = self.med_db.get_medicine(medication_name)
        
        if not medicine:
            return {
                "found": False,
                "message": f"Medication '{medication_name}' not found"
            }

        # Check for contraindications
        contraindicated = []
        for condition in patient_conditions:
            if any(condition.lower() in contra.lower() 
                   for contra in medicine.contraindications):
                contraindicated.append(condition)

        return {
            "found": True,
            "medication": medicine.name,
            "has_contraindications": len(contraindicated) > 0,
            "contraindicated_conditions": contraindicated,
            "all_contraindications": medicine.contraindications
        }

    def assess_age_appropriate(self, medication_name: str, 
                              age: int) -> Dict:
        """
        Assess if medication is appropriate for patient age
        
        Args:
            medication_name: Name of medication
            age: Patient age in years
            
        Returns:
            Dictionary with age appropriateness information
        """
        medicine = self.med_db.get_medicine(medication_name)
        
        if not medicine:
            return {
                "found": False,
                "message": f"Medication '{medication_name}' not found"
            }

        # Simple age-based rules
        warnings = []
        
        if age < 18 and medicine.category in ["NSAID", "Antibiotic"]:
            warnings.append(f"{medicine.name} may require parent/guardian supervision for minors")
        
        if age > 65:
            warnings.append(f"Monitor elderly patients on {medicine.name} for side effects")
        
        if age < 2 and medicine.category in ["NSAID", "Antibiotic"]:
            warnings.append(f"CAUTION: {medicine.name} not recommended for infants")

        return {
            "found": True,
            "medication": medicine.name,
            "age": age,
            "warnings": warnings,
            "safe_for_age": len(warnings) == 0
        }

    def _validate_medications(self, medication_names: List[str]) -> List[str]:
        """Validate that medications exist in database"""
        validated = []
        for med_name in medication_names:
            if self.med_db.get_medicine(med_name):
                validated.append(med_name)
        return validated

    def _calculate_risk_score(self, interactions: List) -> float:
        """
        Calculate overall risk score (0.0 to 1.0)
        
        Args:
            interactions: List of DrugInteraction objects
            
        Returns:
            Risk score between 0.0 and 1.0
        """
        if not interactions:
            return 0.0

        total_score = 0.0
        for interaction in interactions:
            weight = self.INTERACTION_WEIGHTS.get(interaction.severity, 0.5)
            total_score += weight

        # Normalize score (cap at 1.0)
        return min(total_score / len(interactions), 1.0)

    def _determine_risk_level(self, risk_score: float, 
                             interactions: List) -> RiskLevel:
        """
        Determine overall risk level based on score and interactions
        
        Args:
            risk_score: Calculated risk score
            interactions: List of interactions
            
        Returns:
            RiskLevel enum value
        """
        if not interactions:
            return RiskLevel.SAFE

        # Check for any critical interactions
        critical = [i for i in interactions 
                   if i.severity == SeverityLevel.CRITICAL]
        if critical:
            return RiskLevel.CRITICAL

        # Use score for other levels
        if risk_score >= 0.75:
            return RiskLevel.HIGH_RISK
        elif risk_score >= 0.5:
            return RiskLevel.MODERATE_RISK
        elif risk_score > 0:
            return RiskLevel.LOW_RISK
        else:
            return RiskLevel.SAFE

    def _generate_warnings(self, interactions: List, 
                         medications: List[str]) -> List[str]:
        """Generate warning messages"""
        warnings = []

        if not interactions:
            return warnings

        for interaction in interactions:
            if interaction.severity == SeverityLevel.CRITICAL:
                warnings.append(
                    f"⚠️ CRITICAL: {interaction.drug1} + {interaction.drug2} - "
                    f"{interaction.description}"
                )
            elif interaction.severity == SeverityLevel.HIGH:
                warnings.append(
                    f"⚠️ HIGH RISK: {interaction.drug1} + {interaction.drug2}"
                )
            elif interaction.severity == SeverityLevel.MODERATE:
                warnings.append(
                    f"⚠️ MODERATE: {interaction.drug1} + {interaction.drug2}"
                )

        return warnings

    def _generate_recommendations(self, interactions: List) -> List[str]:
        """Generate safety recommendations"""
        recommendations = []

        for interaction in interactions:
            recommendations.extend(interaction.recommendations)

        # Add general recommendations
        if interactions:
            recommendations.append("Consult with a healthcare professional")
            recommendations.append("Monitor for any unusual symptoms")

        return recommendations
