"""
streamlit_app.py - MedSafe AI Front-End Application

Main Streamlit application that integrates all modules:
- Medicine database lookup
- OCR prescription processing
- Drug interaction checking
- Symptom advice
- Risk assessment

This is the user-facing interface for the MedSafe AI system.
"""

import streamlit as st
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.med_db import MedicineDatabase, SeverityLevel
from src.ocr_utils import OCRProcessor, OCRException
from src.risk_engine import RiskEngine, RiskLevel
from src.symptom import SymptomAdvisor


# Configure page
st.set_page_config(
    page_title="MedSafe AI - Medication Safety Assistant",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .title { font-size: 2.5rem; color: #1f77b4; }
    .section-header { font-size: 1.5rem; color: #ff7f0e; margin-top: 1.5rem; }
    .success { color: #2ca02c; }
    .warning { color: #d62728; }
    .info { color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)


@st.cache_resource
def initialize_system():
    """Initialize and cache all components"""
    med_db = MedicineDatabase()
    risk_engine = RiskEngine(med_db)
    symptom_advisor = SymptomAdvisor()
    ocr_processor = OCRProcessor()
    
    return {
        "med_db": med_db,
        "risk_engine": risk_engine,
        "symptom_advisor": symptom_advisor,
        "ocr_processor": ocr_processor
    }


def display_header():
    """Display application header"""
    st.markdown('<h1 class="title">💊 MedSafe AI</h1>', unsafe_allow_html=True)
    st.markdown("### Your Intelligent Medication Safety Assistant")
    st.write("""
    MedSafe AI helps you understand your medications, detect potential drug 
    interactions, and make informed decisions about medication safety.
    """)
    st.divider()


def render_medicine_lookup(system):
    """Render medicine lookup interface"""
    st.markdown('<h2 class="section-header">🔍 Medicine Lookup</h2>', 
                unsafe_allow_html=True)
    
    med_db = system["med_db"]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        med_query = st.text_input(
            "Search for a medicine:",
            placeholder="e.g., Ibuprofen, Aspirin, Amoxicillin..."
        )
    
    with col2:
        search = st.button("Search", key="med_search")
    
    if search and med_query:
        results = med_db.search_medicines(med_query)
        
        if results:
            for med in results:
                with st.expander(f"📋 {med.name}"):
                    st.write(f"**Generic Name:** {med.generic_name}")
                    st.write(f"**Category:** {med.category}")
                    st.write(f"**Dosage:** {med.dosage}")
                    st.write(f"**Manufacturer:** {med.manufacturer}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Uses:**")
                        for use in med.uses:
                            st.write(f"• {use}")
                    
                    with col2:
                        st.write("**Side Effects:**")
                        for effect in med.side_effects:
                            st.write(f"• {effect}")
                    
                    st.write("**Contraindications:**")
                    for contra in med.contraindications:
                        st.write(f"• {contra}")
        else:
            st.warning(f"No medicines found matching '{med_query}'")


def render_interaction_checker(system):
    """Render drug interaction checker"""
    st.markdown('<h2 class="section-header">⚠️ Drug Interaction Checker</h2>', 
                unsafe_allow_html=True)
    
    risk_engine = system["risk_engine"]
    med_db = system["med_db"]
    
    # Get available medicines
    all_medicines = med_db.get_all_medicines()
    med_names = [m.name for m in all_medicines]
    
    st.write("Select the medications you're taking:")
    
    selected_meds = st.multiselect(
        "Choose medications:",
        options=med_names,
        default=[],
        key="interaction_checker"
    )
    
    if st.button("Check Interactions"):
        if selected_meds:
            assessment = risk_engine.assess_medications(selected_meds)
            
            # Display risk level
            risk_colors = {
                RiskLevel.SAFE: "🟢",
                RiskLevel.LOW_RISK: "🟡",
                RiskLevel.MODERATE_RISK: "🟠",
                RiskLevel.HIGH_RISK: "🔴",
                RiskLevel.CRITICAL: "⚫"
            }
            
            risk_color = risk_colors.get(assessment.risk_level, "⚪")
            st.markdown(
                f"### {risk_color} Risk Level: {assessment.risk_level.value.upper()}"
            )
            st.write(f"Risk Score: {assessment.risk_score:.1%}")
            
            # Display interactions
            if assessment.interactions:
                st.write("**Detected Interactions:**")
                for interaction in assessment.interactions:
                    severity_emoji = {
                        "critical": "🔴",
                        "high": "🟠",
                        "moderate": "🟡",
                        "low": "🟢"
                    }
                    emoji = severity_emoji.get(interaction["severity"], "⚪")
                    
                    st.markdown(
                        f"{emoji} **{interaction['drug1']} + {interaction['drug2']}**"
                    )
                    st.write(f"*{interaction['description']}*")
            
            # Display warnings
            if assessment.warnings:
                st.warning("⚠️ **Warnings:**")
                for warning in assessment.warnings:
                    st.write(f"• {warning}")
            
            # Display recommendations
            if assessment.recommendations:
                st.info("💡 **Recommendations:**")
                for rec in assessment.recommendations:
                    st.write(f"• {rec}")
            
            # Medical attention notice
            if assessment.needs_medical_attention:
                st.error(
                    "🚨 **IMPORTANT**: Please consult a healthcare professional "
                    "before taking these medications together."
                )
        else:
            st.warning("Please select at least one medication")


def render_symptom_advisor(system):
    """Render symptom advisor interface"""
    st.markdown('<h2 class="section-header">🩺 Symptom Advisor</h2>', 
                unsafe_allow_html=True)
    
    symptom_advisor = system["symptom_advisor"]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        symptom = st.text_input(
            "Describe your symptom:",
            placeholder="e.g., stomach upset, headache, rash..."
        )
    
    with col2:
        analyze = st.button("Analyze", key="symptom_analyze")
    
    if analyze and symptom:
        advice = symptom_advisor.analyze_symptom(symptom)
        
        # Severity indicator
        severity_emoji = {
            "mild": "🟢",
            "moderate": "🟡",
            "severe": "🔴",
            "emergency": "⚫"
        }
        emoji = severity_emoji.get(advice.severity.value, "⚪")
        
        st.markdown(f"### {emoji} {advice.category.value.upper()}")
        st.write(f"**Severity:** {advice.severity.value}")
        st.write(f"**Description:** {advice.description}")
        
        st.write("**Management Steps:**")
        for i, step in enumerate(advice.management_steps, 1):
            st.write(f"{i}. {step}")
        
        st.info(f"**When to Seek Medical Help:** {advice.when_to_seek_help}")
        
        if advice.related_medications:
            st.write("**Possible Related Medications:**")
            for med in advice.related_medications:
                st.write(f"• {med}")


def render_ocr_processor(system):
    """Render OCR prescription processor"""
    st.markdown('<h2 class="section-header">📸 Prescription OCR</h2>', 
                unsafe_allow_html=True)
    
    ocr_processor = system["ocr_processor"]
    
    st.write("Upload a prescription image to extract medication information:")
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["jpg", "jpeg", "png", "bmp"],
        key="ocr_upload"
    )
    
    if uploaded_file is not None:
        try:
            # Display uploaded image
            st.image(uploaded_file, caption="Uploaded Prescription", width=300)
            
            # Save temporarily and process
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(uploaded_file.getbuffer())
                tmp_path = tmp.name
            
            # Process with OCR
            if st.button("Extract Text from Prescription"):
                with st.spinner("Processing image..."):
                    text, confidence = ocr_processor.process_image(tmp_path)
                    
                    st.success(f"Extraction Confidence: {confidence:.1%}")
                    
                    st.write("**Extracted Text:**")
                    st.text_area("OCR Output", value=text, height=150)
                    
                    # Extract medicines and dosages
                    medicines = ocr_processor.extract_medicines(text)
                    dosages = ocr_processor.extract_dosages(text)
                    
                    if medicines:
                        st.write("**Detected Medicines:**")
                        for med in medicines:
                            st.write(f"• {med}")
                    
                    if dosages:
                        st.write("**Detected Dosages:**")
                        for dosage in dosages:
                            st.write(f"• {dosage}")
        
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")


def render_info_section():
    """Render information section"""
    st.markdown('<h2 class="section-header">ℹ️ About MedSafe AI</h2>', 
                unsafe_allow_html=True)
    
    with st.expander("How to use MedSafe AI"):
        st.write("""
        1. **Medicine Lookup**: Search for information about your medications
        2. **Interaction Checker**: Check for dangerous drug interactions
        3. **Symptom Advisor**: Get guidance on medication side effects
        4. **Prescription OCR**: Upload images to extract medication information
        
        **Important:** This tool provides information only. Always consult 
        with a healthcare professional before making medication decisions.
        """)
    
    with st.expander("Disclaimer"):
        st.warning("""
        **Medical Disclaimer:**
        
        MedSafe AI is an informational tool and should NOT replace professional 
        medical advice. If you experience severe symptoms or think you may have 
        a medical emergency, please call emergency services or visit an 
        emergency room immediately.
        
        Always consult with a licensed healthcare provider before starting, 
        stopping, or changing any medication regimen.
        """)


def main():
    """Main application"""
    display_header()
    
    # Initialize system
    system = initialize_system()
    
    # Create tabs for different features
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Medicine Lookup",
        "Interaction Checker",
        "Symptom Advisor",
        "Prescription OCR",
        "About"
    ])
    
    with tab1:
        render_medicine_lookup(system)
    
    with tab2:
        render_interaction_checker(system)
    
    with tab3:
        render_symptom_advisor(system)
    
    with tab4:
        render_ocr_processor(system)
    
    with tab5:
        render_info_section()
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: gray; font-size: 0.9rem;'>
        💊 MedSafe AI v1.0 | Your Medication Safety Assistant
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
