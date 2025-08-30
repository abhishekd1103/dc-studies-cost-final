import streamlit as st
import pandas as pd
import numpy as np
import math

# Page configuration
st.set_page_config(
    page_title="DC Power Studies Cost Estimator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Dark Theme CSS (Subtle & Clean)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Professional Theme */
    .main > div {
        padding-top: 0.5rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
        color: #e2e8f0;
    }
    
    /* Subtle Professional Header */
    .main-header {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(51, 65, 85, 0.9) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(59, 130, 246, 0.2);
        padding: 2.5rem;
        border-radius: 16px;
        color: #f1f5f9;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, #3b82f6, #06b6d4);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    
    .main-header h2 {
        font-size: 1.2rem;
        font-weight: 400;
        margin: 1rem 0 0 0;
        color: #94a3b8;
    }
    
    /* Developer Credit */
    .developer-credit {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.2);
        padding: 1rem 2rem;
        border-radius: 12px;
        color: #f1f5f9;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0 2rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Section Headers */
    .section-header {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #f1f5f9;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin: 2rem 0 1.5rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    .section-header h2 {
        margin: 0;
        font-size: 1.3rem;
        font-weight: 700;
        color: #3b82f6;
    }
    
    /* Professional Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
        border-color: rgba(59, 130, 246, 0.4);
    }
    
    .metric-card h3 {
        color: #64748b;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card .value {
        color: #3b82f6;
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        line-height: 1;
    }
    
    .metric-card .subtitle {
        color: #64748b;
        font-size: 0.8rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Study Cards */
    .study-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(71, 85, 105, 0.3);
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    .study-card:hover {
        border-color: rgba(59, 130, 246, 0.4);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15);
    }
    
    .study-card h4 {
        color: #f1f5f9;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0 0 1rem 0;
    }
    
    .study-details {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 2rem;
        margin-top: 1rem;
        align-items: center;
    }
    
    .study-detail-item {
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.7;
        font-weight: 500;
    }
    
    .study-detail-item strong {
        color: #f1f5f9;
        font-weight: 600;
    }
    
    .cost-highlight {
        background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .cost-highlight .amount {
        font-size: 1.4rem;
        font-weight: 800;
        margin: 0;
    }
    
    /* Results Container */
    .results-container {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 16px;
        padding: 2.5rem;
        margin: 2rem 0;
        backdrop-filter: blur(15px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* Input Styling */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 8px !important;
        color: #f1f5f9 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    .stCheckbox > label {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }
    
    .stSlider > div > div > div {
        color: #3b82f6 !important;
    }
    
    /* Disclaimer Box */
    .disclaimer-box {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }
    
    .disclaimer-box h4 {
        color: #f59e0b;
        margin: 0 0 1rem 0;
        font-weight: 700;
    }
    
    .disclaimer-box p {
        color: #fbbf24;
        margin: 0.8rem 0;
        line-height: 1.6;
        font-weight: 500;
    }
    
    /* Model Selection Section */
    .model-section {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Work Allocation Section */
    .work-allocation-section {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Additional Services Section */
    .custom-cost-section {
        background: rgba(236, 72, 153, 0.1);
        border: 1px solid rgba(236, 72, 153, 0.3);
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Summary Section */
    .summary-section {
        background: rgba(15, 23, 42, 0.9);
        border: 2px solid rgba(59, 130, 246, 0.4);
        border-radius: 16px;
        padding: 3rem;
        margin: 3rem 0;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    }
    
    /* Scope Cards */
    .scope-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #fca5a5;
        font-weight: 500;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .scope-card.in-scope {
        border-color: rgba(16, 185, 129, 0.3);
        color: #86efac;
    }
    
    /* Final Total Section */
    .final-total-section {
        background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
        border-radius: 16px;
        padding: 2.5rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        margin: 2rem 0;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Text Colors */
    .stMarkdown, h1, h2, h3, h4, h5, h6 {
        color: #e2e8f0 !important;
    }
    
    /* Toggle Styling */
    .stRadio > div > label > div {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 8px !important;
    }
    
    /* Cost Category Cards */
    .cost-category-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .cost-category-card:hover {
        border-color: rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }
    /* ✨ MIRROR GLASS EFFECT */
.glass-effect {
    position: fixed;
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(59, 130, 246, 0.3);
    pointer-events: none;
    z-index: 9999;
    transition: all 0.1s ease;
    opacity: 0;
}

.glass-effect.active {
    opacity: 0.8;
}

/* ✨ RIPPLE CLICK EFFECT */
@keyframes ripple {
    0% { transform: scale(0); opacity: 1; }
    100% { transform: scale(4); opacity: 0; }
}

.ripple-effect {
    position: absolute;
    border-radius: 50%;
    background: rgba(59, 130, 246, 0.4);
    transform: scale(0);
    animation: ripple 0.6s ease-out;
    pointer-events: none;
    z-index: 9998;
}

</style>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const glassEffect = document.createElement('div');
    glassEffect.className = 'glass-effect';
    document.body.appendChild(glassEffect);
    
    let mouseX = 0, mouseY = 0;
    let glassX = 0, glassY = 0;
    
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        glassEffect.classList.add('active');
    });
    
    function animate() {
        glassX += (mouseX - glassX) * 0.08;
        glassY += (mouseY - glassY) * 0.08;
        
        glassEffect.style.left = (glassX - 90) + 'px';
        glassEffect.style.top = (glassY - 90) + 'px';
        
        requestAnimationFrame(animate);
    }
    animate();
    
    document.addEventListener('click', (e) => {
        const ripple = document.createElement('div');
        ripple.className = 'ripple-effect';
        ripple.style.left = (e.clientX - 20) + 'px';
        ripple.style.top = (e.clientY - 20) + 'px';
        ripple.style.width = '40px';
        ripple.style.height = '40px';
        
        document.body.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    });
    
    document.addEventListener('mouseleave', () => {
        glassEffect.classList.remove('active');
    });
});
</script>

""", unsafe_allow_html=True)

# Initialize session state
if 'studies_selected' not in st.session_state:
    st.session_state.studies_selected = {
        'load_flow': True,
        'short_circuit': True,
        'pdc': True,
        'arc_flash': True
    }

if 'work_allocation' not in st.session_state:
    st.session_state.work_allocation = {
        'senior': 20,
        'mid': 30,
        'junior': 50
    }

# Header
st.markdown("""
<div class="main-header">
    <h1>Data Center Power System Studies- Cost Estimation</h1>
    <h2>PSS Studies Cost Estimation Platform</h2>
    <p>Paramateric Cost EStimation Solution for Power System Studies Projects</p>
</div>
""", unsafe_allow_html=True)

# Developer Credit
st.markdown("""
<div class="developer-credit">
    Developed by <strong>A.D</strong> | Power Systems Studies Department
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class="disclaimer-box">
    <h4>❗Important Note</h4>
    <p><strong>Bus Count Estimation:</strong> This tool focuses on cost estimation for power system studies. Bus count calculations are handled by a separate specialized tool which will be integrated in future versions.</p>
    <p><strong>Professional Application:</strong> Results are estimates based on industry standards. Always validate with qualified electrical engineers for actual project implementation.</p>
</div>
""", unsafe_allow_html=True)

# Main Application
with st.container():
    # Project Information Section
    st.markdown("""
    <div class="section-header">
        <h2>Project Information</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        project_name = st.text_input("Project Name", value="Project-Alpha")
        tier_level = st.selectbox("Tier Level", ["Tier I", "Tier II", "Tier III", "Tier IV"], index=3)
    with col2:
        it_capacity = st.number_input("IT Capacity (MW)", min_value=0.0, max_value=200.0, value=10.0, step=0.1)
        delivery_type = st.selectbox("Delivery Type", ["Standard", "Urgent"])
    with col3:
        mechanical_load = st.number_input("Mechanical Load (MW)", min_value=0.0, max_value=100.0, value=7.0, step=0.1)
        report_complexity = st.selectbox("Report Complexity", ["Basic", "Standard", "Premium"], index=1)
    with col4:
        house_load = st.number_input("House/Auxiliary Load (MW)", min_value=0.0, max_value=50.0, value=3.0, step=0.1)
        client_meetings = st.number_input("Client Meetings", min_value=0, max_value=20, value=3, step=1)

    # Customer Type Section
    st.markdown("""
    <div class="section-header">
        <h2>Customer Information</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        customer_type = st.selectbox("Customer Type", ["New Customer", "Repeat Customer"])
    with col6:
        if customer_type == "Repeat Customer":
            repeat_discount = st.slider("Repeat Customer Discount (%)", 0, 25, 10, 1)
        else:
            repeat_discount = 0
    with col7:
        custom_margin = st.number_input("Project Margins (%)", min_value=0, max_value=50, value=15, step=1)
    with col8:
        bus_calibration = st.slider("Bus Count Calibration", 0.5, 2.5, 1.3, 0.1)

    # NEW: Model Type & Hour Reduction Section
    st.markdown("""
    <div class="section-header">
        <h2>Model Type & Hour Reduction</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="model-section">', unsafe_allow_html=True)
        
        model_col1, model_col2 = st.columns([2, 2])
        
        with model_col1:
            st.markdown("**Select Model Type**")
            model_type = st.radio(
                "Model Type",
                ["Typical Model", "ETAP Model Available"],
                index=0,
                help="ETAP Model reduces manhours due to existing system models"
            )
        
        with model_col2:
            st.markdown("**Hour Reduction Factor**")
            if model_type == "ETAP Model Available":
                hour_reduction = st.slider(
                    "Hour Reduction (%)",
                    min_value=10,
                    max_value=90,
                    value=30,
                    step=5,
                    help="Percentage reduction in manhours when ETAP model is available"
                )
                st.info(f"🎯 **{hour_reduction}% reduction** will be applied to total manhours")
            else:
                hour_reduction = 0
                st.info("🔧 **No reduction** - Using typical modeling approach")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Studies Selection Section
    st.markdown("""
    <div class="section-header">
        <h2>Studies Configuration</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col_studies1, col_studies2 = st.columns([3, 1])
    
    with col_studies1:
        study_col1, study_col2 = st.columns(2)
        
        with study_col1:
            st.session_state.studies_selected['load_flow'] = st.checkbox(
                "Load Flow Study - Steady-state voltage and power analysis", 
                value=st.session_state.studies_selected['load_flow'],
                key="load_flow_cb"
            )
            st.session_state.studies_selected['short_circuit'] = st.checkbox(
                "Short Circuit Study - Fault current calculations", 
                value=st.session_state.studies_selected['short_circuit'],
                key="short_circuit_cb"
            )
        
        with study_col2:
            st.session_state.studies_selected['pdc'] = st.checkbox(
                "Protective Device Coordination - Relay coordination", 
                value=st.session_state.studies_selected['pdc'],
                key="pdc_cb"
            )
            st.session_state.studies_selected['arc_flash'] = st.checkbox(
                "Arc Flash Study - Incident energy calculations", 
                value=st.session_state.studies_selected['arc_flash'],
                key="arc_flash_cb"
            )
    
    with col_studies2:
        if st.button("Select All Studies", key="select_all_studies"):
            for key in st.session_state.studies_selected:
                st.session_state.studies_selected[key] = True
            st.rerun()
        
        if st.button("Clear All Studies", key="clear_all_studies"):
            for key in st.session_state.studies_selected:
                st.session_state.studies_selected[key] = False
            st.rerun()

    # Work Allocation Section
    st.markdown("""
    <div class="section-header">
        <h2>Work Allocation Configuration</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="work-allocation-section">', unsafe_allow_html=True)
        
        alloc_col1, alloc_col2, alloc_col3, alloc_col4 = st.columns(4)
        
        with alloc_col1:
            st.session_state.work_allocation['senior'] = st.slider(
                "Senior Engineer (%)", 
                5, 50, st.session_state.work_allocation['senior'], 1
            )
        
        with alloc_col2:
            st.session_state.work_allocation['mid'] = st.slider(
                "Mid-level Engineer (%)", 
                10, 60, st.session_state.work_allocation['mid'], 1
            )
        
        with alloc_col3:
            st.session_state.work_allocation['junior'] = st.slider(
                "Junior Engineer (%)", 
                10, 70, st.session_state.work_allocation['junior'], 1
            )
        
        with alloc_col4:
            if st.button("Auto Balance (20:30:50)", key="auto_balance"):
                st.session_state.work_allocation = {'senior': 20, 'mid': 30, 'junior': 50}
                st.rerun()
        
        # Normalize allocations
        total_allocation = sum(st.session_state.work_allocation.values())
        if total_allocation != 100:
            factor = 100 / total_allocation
            for key in st.session_state.work_allocation:
                st.session_state.work_allocation[key] = round(st.session_state.work_allocation[key] * factor, 1)
        
        st.success(f"✅ Current Allocation: Senior {st.session_state.work_allocation['senior']:.1f}% | Mid {st.session_state.work_allocation['mid']:.1f}% | Junior {st.session_state.work_allocation['junior']:.1f}%")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Rate Configuration Section
    st.markdown("""
    <div class="section-header">
        <h2>Rate Configuration</h2>
    </div>
    """, unsafe_allow_html=True)
    
    rate_col1, rate_col2, rate_col3 = st.columns(3)
    
    with rate_col1:
        st.markdown("**Hourly Rates (₹)**")
        senior_rate = st.number_input("Senior Engineer Rate", min_value=1000, max_value=8000, value=2200, step=50)
        mid_rate = st.number_input("Mid-level Engineer Rate", min_value=500, max_value=5000, value=1200, step=25)
        junior_rate = st.number_input("Junior Engineer Rate", min_value=300, max_value=2000, value=800, step=25)
    
    with rate_col2:
        st.markdown("**Study Complexity Factors**")
        load_flow_factor = st.slider("Load Flow Factor", 0.3, 3.0, 1.0, 0.1)
        short_circuit_factor = st.slider("Short Circuit Factor", 0.3, 3.0, 1.0, 0.1)
        pdc_factor = st.slider("PDC Factor", 0.3, 3.0, 1.0, 0.1)
        arc_flash_factor = st.slider("Arc Flash Factor", 0.3, 3.0, 1.0, 0.1)
    
    with rate_col3:
        st.markdown("**Additional Settings**")
        urgency_multiplier = st.slider("Urgent Delivery Multiplier", 1.0, 3.0, 1.3, 0.1)
        meeting_cost = st.number_input("Cost per Meeting (₹)", min_value=2000, max_value=25000, value=8000, step=500)

    # Report Costs Section
    st.markdown("""
    <div class="section-header">
        <h2>Report Configuration</h2>
    </div>
    """, unsafe_allow_html=True)
    
    report_col1, report_col2, report_col3, report_col4 = st.columns(4)
    
    with report_col1:
        load_flow_report_cost = st.number_input("Load Flow Report Cost (₹)", min_value=0, max_value=50000, value=8000, step=500)
    with report_col2:
        short_circuit_report_cost = st.number_input("Short Circuit Report Cost (₹)", min_value=0, max_value=50000, value=10000, step=500)
    with report_col3:
        pdc_report_cost = st.number_input("PDC Report Cost (₹)", min_value=0, max_value=50000, value=15000, step=500)
    with report_col4:
        arc_flash_report_cost = st.number_input("Arc Flash Report Cost (₹)", min_value=0, max_value=50000, value=12000, step=500)

    # Additional Services Section
    st.markdown("""
    <div class="section-header">
        <h2>Additional Services</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="custom-cost-section">', unsafe_allow_html=True)
        
        custom_col1, custom_col2, custom_col3, custom_col4 = st.columns(4)
        
        with custom_col1:
            site_visit_enabled = st.checkbox("Site Visits Required", value=True)
            if site_visit_enabled:
                site_visits = st.number_input("Number of Site Visits", min_value=0, max_value=20, value=2, step=1)
                site_visit_cost = st.number_input("Cost per Site Visit (₹)", min_value=0, max_value=50000, value=12000, step=500)
            else:
                site_visits = 0
                site_visit_cost = 0
        
        with custom_col2:
            af_labels_enabled = st.checkbox("Arc Flash Labels Required", value=False)
            if af_labels_enabled:
                num_labels = st.number_input("Number of Labels", min_value=0, max_value=500, value=50, step=1)
                cost_per_label = st.number_input("Cost per Label (₹)", min_value=0, max_value=500, value=150, step=10)
            else:
                num_labels = 0
                cost_per_label = 0
        
        with custom_col3:
            stickering_enabled = st.checkbox("Equipment Stickering Required", value=False)
            if stickering_enabled:
                stickering_cost = st.number_input("Stickering Cost (₹)", min_value=0, max_value=100000, value=25000, step=1000)
            else:
                stickering_cost = 0
        
        with custom_col4:
            st.markdown("**Custom Charges**")
            custom_charges_desc = st.text_input("Description", value="Additional Services", placeholder="Enter description")
            custom_charges_cost = st.number_input("Custom Charges (₹)", min_value=0, max_value=500000, value=0, step=1000)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Engineering Calculations Section
st.markdown("""
<div class="section-header">
    <h2>Engineering Calculations & Results</h2>
</div>
""", unsafe_allow_html=True)

# Core calculations
total_load = it_capacity + mechanical_load + house_load

# Bus count estimation
tier_bus_factors = {"Tier I": 1.5, "Tier II": 1.7, "Tier III": 2.0, "Tier IV": 2.3}
estimated_buses = max(1, math.ceil(total_load * tier_bus_factors[tier_level] * bus_calibration))

# Study complexity factors
tier_complexity_factors = {"Tier I": 1.0, "Tier II": 1.2, "Tier III": 1.5, "Tier IV": 2.0}
tier_complexity = tier_complexity_factors[tier_level]

# Work allocation percentages
senior_allocation = st.session_state.work_allocation['senior'] / 100
mid_allocation = st.session_state.work_allocation['mid'] / 100
junior_allocation = st.session_state.work_allocation['junior'] / 100

# Study definitions
studies_data = {
    'load_flow': {
        'name': 'Load Flow Study', 
        'base_hours_per_bus': 0.8, 
        'factor': load_flow_factor,
        'report_cost': load_flow_report_cost
    },
    'short_circuit': {
        'name': 'Short Circuit Study', 
        'base_hours_per_bus': 1.0, 
        'factor': short_circuit_factor,
        'report_cost': short_circuit_report_cost
    },
    'pdc': {
        'name': 'Protective Device Coordination', 
        'base_hours_per_bus': 1.5, 
        'factor': pdc_factor,
        'report_cost': pdc_report_cost
    },
    'arc_flash': {
        'name': 'Arc Flash Study', 
        'base_hours_per_bus': 1.2, 
        'factor': arc_flash_factor,
        'report_cost': arc_flash_report_cost
    }
}

# Calculate study costs with hour reduction
total_study_hours = 0
total_study_cost = 0
total_report_cost = 0
study_results = {}

for study_key, study_data in studies_data.items():
    if st.session_state.studies_selected.get(study_key, False):
        # Calculate base study hours
        base_study_hours = estimated_buses * study_data['base_hours_per_bus'] * study_data['factor'] * tier_complexity
        
        # Apply hour reduction if ETAP model is available
        if model_type == "ETAP Model Available":
            study_hours = base_study_hours * (1 - hour_reduction/100)
            hours_saved = base_study_hours - study_hours
        else:
            study_hours = base_study_hours
            hours_saved = 0
        
        total_study_hours += study_hours
        
        # Resource allocation
        senior_hours = study_hours * senior_allocation
        mid_hours = study_hours * mid_allocation
        junior_hours = study_hours * junior_allocation
        
        # Apply multipliers
        rate_multiplier = urgency_multiplier if delivery_type == "Urgent" else 1.0
        discount_multiplier = (1 - repeat_discount/100) if customer_type == "Repeat Customer" else 1.0
        
        # Calculate costs
        senior_cost = senior_hours * senior_rate * rate_multiplier * discount_multiplier
        mid_cost = mid_hours * mid_rate * rate_multiplier * discount_multiplier
        junior_cost = junior_hours * junior_rate * rate_multiplier * discount_multiplier
        
        study_total_cost = senior_cost + mid_cost + junior_cost
        total_study_cost += study_total_cost
        
        # Report cost
        report_multipliers = {"Basic": 0.8, "Standard": 1.0, "Premium": 1.5}
        study_report_cost = study_data['report_cost'] * report_multipliers[report_complexity]
        total_report_cost += study_report_cost
        
        study_results[study_key] = {
            'name': study_data['name'],
            'base_hours': base_study_hours,
            'hours': study_hours,
            'hours_saved': hours_saved,
            'senior_hours': senior_hours,
            'mid_hours': mid_hours,
            'junior_hours': junior_hours,
            'senior_cost': senior_cost,
            'mid_cost': mid_cost,
            'junior_cost': junior_cost,
            'total_cost': study_total_cost,
            'report_cost': study_report_cost
        }

# Calculate additional costs
total_site_visit_cost = site_visits * site_visit_cost if site_visit_enabled else 0
total_label_cost = num_labels * cost_per_label if af_labels_enabled else 0
total_meeting_cost = client_meetings * meeting_cost
total_additional_costs = total_site_visit_cost + total_label_cost + stickering_cost + custom_charges_cost

# Final calculations
subtotal = total_study_cost + total_meeting_cost + total_report_cost + total_additional_costs
total_cost = subtotal * (1 + custom_margin/100)

# Calculate total hours saved
total_hours_saved = sum(study['hours_saved'] for study in study_results.values())

# Display Results
if study_results:
    # Main metrics display
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Load</h3>
            <p class="value">{total_load:.1f} MW</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Bus Count</h3>
            <p class="value">{estimated_buses}</p>
            <p class="subtitle">buses</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Hours</h3>
            <p class="value">{total_study_hours:.0f}</p>
            <p class="subtitle">engineering hours</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Hours Saved</h3>
            <p class="value">{total_hours_saved:.0f}</p>
            <p class="subtitle">{model_type}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Customer Type</h3>
            <p class="value">{customer_type.split()[0]}</p>
            <p class="subtitle">{repeat_discount}% discount</p>
        </div>
        """, unsafe_allow_html=True)

    # Model Type Impact Display
    if model_type == "ETAP Model Available" and total_hours_saved > 0:
        st.success(f"🎯 **ETAP Model Benefit**: {hour_reduction}% reduction saved {total_hours_saved:.0f} hours (₹{total_hours_saved * ((senior_rate * senior_allocation) + (mid_rate * mid_allocation) + (junior_rate * junior_allocation)):,.0f})")

    # Study-wise breakdown
    st.markdown("### Study-wise Cost Analysis")
    
    for study_key, study in study_results.items():
        reduction_info = ""
        if study['hours_saved'] > 0:
            reduction_info = f"<br><span style='color: #10b981; font-weight: 600;'>Hours Saved: {study['hours_saved']:.1f}h ({hour_reduction}% reduction)</span>"
        
        st.markdown(f"""
        <div class="study-card">
            <h4>{study['name']}</h4>
            <p style="color: #94a3b8; margin: 0 0 1rem 0; font-weight: 500;">
                {study['hours']:.1f} total engineering hours{reduction_info}
            </p>
            <div class="study-details">
                <div class="study-detail-item">
                    <strong>Senior Engineer:</strong> {study['senior_hours']:.1f}h × ₹{senior_rate:,}/hr = ₹{study['senior_cost']:,.0f}<br>
                    <strong>Mid-level Engineer:</strong> {study['mid_hours']:.1f}h × ₹{mid_rate:,}/hr = ₹{study['mid_cost']:,.0f}<br>
                    <strong>Junior Engineer:</strong> {study['junior_hours']:.1f}h × ₹{junior_rate:,}/hr = ₹{study['junior_cost']:,.0f}<br>
                    <strong>Report Cost ({report_complexity}):</strong> ₹{study['report_cost']:,.0f}
                </div>
                <div class="cost-highlight">
                    <p class="amount">₹{study['total_cost'] + study['report_cost']:,.0f}</p>
                    <small>Total Study Cost</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Resource allocation summary
    st.markdown(f"""
    <div class="results-container">
        <h3 style="color: #3b82f6; text-align: center; margin-bottom: 2rem; font-weight: 700;">Resource Allocation Summary</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; text-align: center;">
            <div class="cost-category-card">
                <h4 style="color: #06b6d4; margin: 0 0 0.5rem 0; font-weight: 700;">Senior Engineer</h4>
                <p style="color: #3b82f6; font-size: 1.6rem; font-weight: 800; margin: 0.5rem 0;">{total_study_hours * senior_allocation:.0f} hrs</p>
                <p style="color: #64748b; margin: 0; font-weight: 500;">Rate: ₹{senior_rate:,}/hr • {st.session_state.work_allocation['senior']:.1f}%</p>
                <p style="color: #94a3b8; margin: 0.5rem 0 0 0;">Total: ₹{sum(study['senior_cost'] for study in study_results.values()):,.0f}</p>
            </div>
            <div class="cost-category-card">
                <h4 style="color: #06b6d4; margin: 0 0 0.5rem 0; font-weight: 700;">Mid-level Engineer</h4>
                <p style="color: #3b82f6; font-size: 1.6rem; font-weight: 800; margin: 0.5rem 0;">{total_study_hours * mid_allocation:.0f} hrs</p>
                <p style="color: #64748b; margin: 0; font-weight: 500;">Rate: ₹{mid_rate:,}/hr • {st.session_state.work_allocation['mid']:.1f}%</p>
                <p style="color: #94a3b8; margin: 0.5rem 0 0 0;">Total: ₹{sum(study['mid_cost'] for study in study_results.values()):,.0f}</p>
            </div>
            <div class="cost-category-card">
                <h4 style="color: #06b6d4; margin: 0 0 0.5rem 0; font-weight: 700;">Junior Engineer</h4>
                <p style="color: #3b82f6; font-size: 1.6rem; font-weight: 800; margin: 0.5rem 0;">{total_study_hours * junior_allocation:.0f} hrs</p>
                <p style="color: #64748b; margin: 0; font-weight: 500;">Rate: ₹{junior_rate:,}/hr • {st.session_state.work_allocation['junior']:.1f}%</p>
                <p style="color: #94a3b8; margin: 0.5rem 0 0 0;">Total: ₹{sum(study['junior_cost'] for study in study_results.values()):,.0f}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Cost visualization chart
    st.markdown("### Cost Distribution Analysis")
    chart_components = []
    chart_costs = []
    
    # Add study costs
    for study in study_results.values():
        chart_components.append(study['name'])
        chart_costs.append(study['total_cost'])
    
    # Add additional services if applicable
    if total_site_visit_cost > 0:
        chart_components.append('Site Visits')
        chart_costs.append(total_site_visit_cost)
    
    if total_label_cost > 0:
        chart_components.append('AF Labels')
        chart_costs.append(total_label_cost)
    
    if stickering_cost > 0:
        chart_components.append('Stickering')
        chart_costs.append(stickering_cost)
    
    if custom_charges_cost > 0:
        chart_components.append('Custom Charges')
        chart_costs.append(custom_charges_cost)
    
    # Add meetings and reports
    chart_components.extend(['Client Meetings', 'Reports'])
    chart_costs.extend([total_meeting_cost, total_report_cost])
    
    # Create chart data
    chart_data = pd.DataFrame({
        'Component': chart_components,
        'Cost': chart_costs
    })
    
    st.bar_chart(chart_data.set_index('Component'))

    # ENHANCED PROJECT COST SUMMARY (NO RAW CODE)
    st.markdown("""
    <div class="summary-section">
        <h2 style="color: #f1f5f9; text-align: center; margin-bottom: 2rem; font-weight: 800;">
            Complete Project Cost Summary
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Studies Summary Grid
    st.markdown("#### Studies Breakdown")
    studies_cols = st.columns(len(study_results))
    
    for idx, (study_key, study) in enumerate(study_results.items()):
        with studies_cols[idx]:
            st.markdown(f"""
            <div class="cost-category-card">
                <h5 style="color: #f1f5f9; margin: 0 0 0.8rem 0; font-weight: 600;">{study['name']}</h5>
                <p style="color: #cbd5e1; margin: 0.2rem 0; font-size: 0.85rem;">Engineering: ₹{study['total_cost']:,.0f}</p>
                <p style="color: #cbd5e1; margin: 0.2rem 0; font-size: 0.85rem;">Report: ₹{study['report_cost']:,.0f}</p>
                <p style="color: #3b82f6; margin: 0.5rem 0 0 0; font-weight: 700;">Total: ₹{study['total_cost'] + study['report_cost']:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("#### Additional Services Status")
    
    # Additional Services Grid
    services_col1, services_col2, services_col3, services_col4 = st.columns(4)
    
    with services_col1:
        if site_visit_enabled:
            st.success(f"✅ Site Visits: {site_visits} visits × ₹{site_visit_cost:,} = ₹{total_site_visit_cost:,}")
        else:
            st.error("❌ Site Visits: Not included in scope")
    
    with services_col2:
        if af_labels_enabled:
            st.success(f"✅ Arc Flash Labels: {num_labels} labels × ₹{cost_per_label:,} = ₹{total_label_cost:,}")
        else:
            st.error("❌ Arc Flash Labels: Hardcopy labels not in our scope")
    
    with services_col3:
        if stickering_enabled:
            st.success(f"✅ Equipment Stickering: ₹{stickering_cost:,}")
        else:
            st.error("❌ Equipment Stickering: Not included in our scope")
    
    with services_col4:
        if custom_charges_cost > 0:
            st.success(f"✅ {custom_charges_desc}: ₹{custom_charges_cost:,}")
        else:
            st.info("ℹ️ No custom charges added")

    # Final Cost Summary Grid
    st.markdown("#### Final Cost Summary")
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.markdown(f"""
        <div class="cost-category-card">
            <h4 style="color: #3b82f6; margin: 0; font-weight: 700;">Studies</h4>
            <p style="color: #f1f5f9; font-size: 1.4rem; font-weight: 700; margin: 0.5rem 0;">₹{total_study_cost:,.0f}</p>
            <p style="color: #64748b; margin: 0; font-size: 0.8rem;">Engineering Services</p>
        </div>
        """, unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown(f"""
        <div class="cost-category-card">
            <h4 style="color: #06b6d4; margin: 0; font-weight: 700;">Reports</h4>
            <p style="color: #f1f5f9; font-size: 1.4rem; font-weight: 700; margin: 0.5rem 0;">₹{total_report_cost:,.0f}</p>
            <p style="color: #64748b; margin: 0; font-size: 0.8rem;">{report_complexity} Format</p>
        </div>
        """, unsafe_allow_html=True)
    
    with summary_col3:
        st.markdown(f"""
        <div class="cost-category-card">
            <h4 style="color: #8b5cf6; margin: 0; font-weight: 700;">Meetings</h4>
            <p style="color: #f1f5f9; font-size: 1.4rem; font-weight: 700; margin: 0.5rem 0;">₹{total_meeting_cost:,.0f}</p>
            <p style="color: #64748b; margin: 0; font-size: 0.8rem;">{client_meetings} Sessions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with summary_col4:
        st.markdown(f"""
        <div class="cost-category-card">
            <h4 style="color: #ec4899; margin: 0; font-weight: 700;">Additional</h4>
            <p style="color: #f1f5f9; font-size: 1.4rem; font-weight: 700; margin: 0.5rem 0;">₹{total_additional_costs:,.0f}</p>
            <p style="color: #64748b; margin: 0; font-size: 0.8rem;">Extra Services</p>
        </div>
        """, unsafe_allow_html=True)

    # Cost Breakdown
    breakdown_col1, breakdown_col2, breakdown_col3 = st.columns(3)
    
    with breakdown_col1:
        st.info(f"**Subtotal:** ₹{subtotal:,.0f}")
    
    with breakdown_col2:
        st.info(f"**Margin ({custom_margin}%):** ₹{total_cost - subtotal:,.0f}")
    
    with breakdown_col3:
        st.info(f"**Discount Applied:** {repeat_discount}%")

    # FINAL TOTAL
    st.markdown(f"""
    <div class="final-total-section">
        <h1 style="color: white; margin: 0; font-weight: 800; font-size: 2rem;">TOTAL PROJECT COST</h1>
        <p style="color: white; font-size: 3.5rem; font-weight: 900; margin: 1rem 0;">₹{total_cost:,.0f}</p>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin: 0; font-weight: 500;">
            {project_name} | {tier_level} Data Center | {customer_type} | {model_type}
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.warning("⚠️ Please select at least one study type to generate cost estimates.")

# Footer
import datetime
current_time = datetime.datetime.now()

st.markdown(f"""
<div style="text-align: center; color: #64748b; padding: 3rem 2rem 2rem 2rem; margin-top: 4rem; 
     border-top: 2px solid rgba(59, 130, 246, 0.3); 
     background: rgba(15, 23, 42, 0.8); border-radius: 12px; backdrop-filter: blur(10px);">
    <p style="font-size: 1.2rem; font-weight: 700; color: #3b82f6; margin: 0 0 0.5rem 0;">
        Data Center Power System Studies - Professional Cost Estimation Platform
    </p>
    <p style="margin: 0.5rem 0; font-weight: 600; color: #06b6d4;">
        Developed by <strong>Abhishek Diwanji</strong> | Power Systems Studies Department
    </p>
    <p style="margin: 0; font-size: 0.9rem; color: #64748b;">
    Cal-Version 4.1 | Enhanced with Reportings Cost/Custom Cost-Typical Modeling
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #475569;">
        Generated on: {current_time.strftime("%B %d, %Y at %I:%M %p IST")}
    </p>
</div>
""", unsafe_allow_html=True)
