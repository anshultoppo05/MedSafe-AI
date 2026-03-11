"""
med_db.py - Medicine Database and Drug Interaction Metadata

This module manages the medicine database, drug interactions, and related metadata.
Provides functionality for querying medicines, detecting interactions, and 
retrieving safety information.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class SeverityLevel(Enum):
    """Drug interaction severity levels"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Medicine:
    """Data class representing a medicine"""
    name: str
    generic_name: str
    category: str
    dosage: str
    manufacturer: str
    uses: List[str]
    side_effects: List[str]
    contraindications: List[str]


@dataclass
class DrugInteraction:
    """Data class representing a drug interaction"""
    drug1: str
    drug2: str
    severity: SeverityLevel
    description: str
    recommendations: List[str]


class MedicineDatabase:
    """
    Manages medicine database and drug interactions.
    
    This is the central repository for all medicine-related information,
    including drug interactions, side effects, and safety data.
    """

    def __init__(self):
        """Initialize the medicine database with sample data"""
        self.medicines: Dict[str, Medicine] = {}
        self.interactions: List[DrugInteraction] = []
        self._initialize_sample_data()

    def _initialize_sample_data(self) -> None:
        """Initialize database with sample medication data"""
        
        # Sample medicines
        sample_medicines = [
            Medicine(
                name="Ibuprofen",
                generic_name="Ibuprofen",
                category="NSAID",
                dosage="200mg, 400mg, 600mg, 800mg",
                manufacturer="Various",
                uses=["Pain relief", "Fever reduction", "Inflammation"],
                side_effects=["Stomach upset", "Heartburn", "Dizziness"],
                contraindications=["Pregnancy", "Ulcers", "Asthma"]
            ),
            Medicine(
                name="Aspirin",
                generic_name="Acetylsalicylic acid",
                category="NSAID",
                dosage="100mg, 325mg, 500mg",
                manufacturer="Various",
                uses=["Pain relief", "Blood clotting prevention", "Heart disease"],
                side_effects=["Stomach upset", "Bleeding", "Rash"],
                contraindications=["Bleeding disorders", "Asthma", "Pregnancy"]
            ),
            Medicine(
                name="Metformin",
                generic_name="Metformin",
                category="Antidiabetic",
                dosage="500mg, 1000mg",
                manufacturer="Various",
                uses=["Type 2 diabetes management"],
                side_effects=["Nausea", "Diarrhea", "Metallic taste"],
                contraindications=["Kidney disease", "Liver disease"]
            ),
            Medicine(
                name="Lisinopril",
                generic_name="Lisinopril",
                category="ACE Inhibitor",
                dosage="5mg, 10mg, 20mg",
                manufacturer="Various",
                uses=["Hypertension", "Heart failure"],
                side_effects=["Dry cough", "Dizziness", "Fatigue"],
                contraindications=["Pregnancy", "Angioedema"]
            ),
            Medicine(
                name="Amoxicillin",
                generic_name="Amoxicillin",
                category="Antibiotic",
                dosage="250mg, 500mg",
                manufacturer="Various",
                uses=["Bacterial infections"],
                side_effects=["Rash", "Nausea", "Diarrhea"],
                contraindications=["Penicillin allergy"]
            ),
        ]

        for med in sample_medicines:
            self.medicines[med.name.lower()] = med

        # Sample interactions
        sample_interactions = [
            DrugInteraction(
                drug1="Ibuprofen",
                drug2="Aspirin",
                severity=SeverityLevel.HIGH,
                description="Both NSAIDs increase risk of GI bleeding and ulcers",
                recommendations=[
                    "Avoid combining these medications",
                    "If unavoidable, add gastroprotection (PPI)",
                    "Monitor for signs of bleeding"
                ]
            ),
            DrugInteraction(
                drug1="Metformin",
                drug2="Lisinopril",
                severity=SeverityLevel.LOW,
                description="No direct interaction, but combined effect may affect kidney function",
                recommendations=[
                    "Monitor kidney function regularly",
                    "Safe to use together with monitoring"
                ]
            ),
            DrugInteraction(
                drug1="Aspirin",
                drug2="Amoxicillin",
                severity=SeverityLevel.MODERATE,
                description="May increase risk of bleeding and GI effects",
                recommendations=[
                    "Space doses apart if possible",
                    "Take with food",
                    "Monitor for bleeding signs"
                ]
            ),
        ]

        self.interactions = sample_interactions

    def get_medicine(self, name: str) -> Optional[Medicine]:
        """
        Get medicine information by name (case-insensitive)
        
        Args:
            name: Medicine name
            
        Returns:
            Medicine object or None if not found
        """
        return self.medicines.get(name.lower())

    def search_medicines(self, query: str) -> List[Medicine]:
        """
        Search medicines by name or category
        
        Args:
            query: Search query
            
        Returns:
            List of matching medicines
        """
        query_lower = query.lower()
        results = []
        
        for med in self.medicines.values():
            if (query_lower in med.name.lower() or 
                query_lower in med.generic_name.lower() or
                query_lower in med.category.lower()):
                results.append(med)
        
        return results

    def get_interactions(self, drug_names: List[str]) -> List[DrugInteraction]:
        """
        Get interactions between multiple drugs
        
        Args:
            drug_names: List of drug names to check
            
        Returns:
            List of relevant interactions
        """
        relevant_interactions = []
        drug_names_lower = [d.lower() for d in drug_names]
        
        for interaction in self.interactions:
            drug1_lower = interaction.drug1.lower()
            drug2_lower = interaction.drug2.lower()
            
            if (drug1_lower in drug_names_lower and 
                drug2_lower in drug_names_lower):
                relevant_interactions.append(interaction)
        
        return relevant_interactions

    def add_medicine(self, medicine: Medicine) -> None:
        """
        Add a new medicine to the database
        
        Args:
            medicine: Medicine object to add
        """
        self.medicines[medicine.name.lower()] = medicine

    def add_interaction(self, interaction: DrugInteraction) -> None:
        """
        Add a new drug interaction to the database
        
        Args:
            interaction: DrugInteraction object to add
        """
        self.interactions.append(interaction)

    def get_all_medicines(self) -> List[Medicine]:
        """Get all medicines in database"""
        return list(self.medicines.values())

    def get_interactions_by_severity(self, severity: SeverityLevel) -> List[DrugInteraction]:
        """
        Get all interactions of a specific severity level
        
        Args:
            severity: SeverityLevel to filter by
            
        Returns:
            List of interactions at that severity level
        """
        return [i for i in self.interactions if i.severity == severity]
