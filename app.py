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

# Professional CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styling */
    .main > div {
        padding-top: 1rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }
    
    .main-header h2 {
        font-size: 1.3rem;
        font-weight: 400;
        margin: 1rem 0 0 0;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }
    
    /* Developer Credit */
    .developer-credit {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 8px 25px rgba(245, 87, 108, 0.3);
    }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin: 2rem 0 1.5rem 0;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .section-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .section-header:hover::before {
        left: 100%;
    }
    
    .section-header h2 {
        margin: 0;
        font-size: 1.4rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(79, 172, 254, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4facfe, #00f2fe);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(79, 172, 254, 0.2);
        border-color: rgba(79, 172, 254, 0.5);
    }
    
    .metric-card h3 {
        color: #2d3748;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0 0 0.8rem 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card .value {
        color: #4facfe;
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        line-height: 1;
    }
    
    .metric-card .subtitle {
        color: #718096;
        font-size: 0.85rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Study Cards */
    .study-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,249,255,0.9) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 15px;
        padding: 1.8rem;
        margin: 1.2rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
    }
    
    .study-card:hover {
        border-color: rgba(102, 126, 234, 0.4);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.15);
        transform: translateY(-2px);
    }
    
    .study-card h4 {
        color: #2d3748;
        font-size: 1.15rem;
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
        color: #4a5568;
        font-size: 0.9rem;
        line-height: 1.7;
        font-weight: 500;
    }
    
    .study-detail-item strong {
        color: #2d3748;
        font-weight: 600;
    }
    
    .cost-highlight {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
    }
    
    .cost-highlight .amount {
        font-size: 1.4rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
    
    /* Results Section */
    .results-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,249,255,0.9) 100%);
        border: 2px solid rgba(79, 172, 254, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        backdrop-filter: blur(20px);
        box-shadow: 0 15px 40px rgba(79, 172, 254, 0.15);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 2rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.9rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Disclaimer Box */
    .disclaimer-box {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(251, 191, 36, 0.1) 100%);
        border: 2px solid rgba(245, 158, 11, 0.3);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }
    
    .disclaimer-box h4 {
        color: #d97706;
        margin: 0 0 1rem 0;
        font-weight: 700;
    }
    
    .disclaimer-box p {
        color: #92400e;
        margin: 0.8rem 0;
        line-height: 1.7;
        font-weight: 500;
    }
    
    /* Input Styling */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(79, 172, 254, 0.2);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: #4facfe;
        box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Text Colors */
    .stMarkdown, h1, h2, h3, h4, h5, h6 {
        color: #2d3748;
    }
    
    .stCheckbox > label {
        color: #2d3748;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    /* Custom Cost Section */
    .custom-cost-section {
        background: linear-gradient(135deg, rgba(240, 147, 251, 0.1) 0%, rgba(245, 87, 108, 0.1) 100%);
        border: 2px solid rgba(240, 147, 251, 0.3);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for study selections
if 'studies_selected' not in st.session_state:
    st.session_state.studies_selected = {
        'load_flow': True,
        'short_circuit': True,
        'pdc': True,
        'arc_flash': True
    }

# Header
st.markdown("""
<div class="main-header">
    <h1>Data Center Power System Studies</h1>
    <h2>Professional Cost Estimation Platform</h2>
    <p>Advanced Engineering Solution for Comprehensive Power Studies Analysis</p>
</div>
""", unsafe_allow_html=True)

# Developer Credit
st.markdown("""
<div class="developer-credit">
    Developed by <strong>Abhishek Diwanji</strong> | Power Systems Engineering Department
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class="disclaimer-box">
    <h4>Important Notice</h4>
    <p><strong>Bus Count Estimation:</strong> This platform provides cost estimation for power system studies. 
    Bus count calculations utilize industry-standard methodologies.</p>
    <p><strong>Professional Application:</strong> Results represent engineering estimates based on established industry practices. 
    Final validation by certified electrical engineers is recommended for project implementation.</p>
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
        
        # Resource allocation percentages
        senior_allocation = 0.2
        mid_allocation = 0.3
        junior_allocation = 0.5

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
            site_visits = st.number_input("Number of Site Visits", min_value=0, max_value=20, value=2, step=1)
            site_visit_cost = st.number_input("Cost per Site Visit (₹)", min_value=0, max_value=50000, value=12000, step=500)
        
        with custom_col2:
            af_labels_required = st.checkbox("Arc Flash Labels Required")
            if af_labels_required:
                num_labels = st.number_input("Number of Labels", min_value=0, max_value=500, value=50, step=1)
                cost_per_label = st.number_input("Cost per Label (₹)", min_value=0, max_value=500, value=150, step=10)
            else:
                num_labels = 0
                cost_per_label = 0
        
        with custom_col3:
            stickering_required = st.checkbox("Equipment Stickering Required")
            if stickering_required:
                stickering_cost = st.number_input("Stickering Cost (₹)", min_value=0, max_value=100000, value=25000, step=1000)
            else:
                stickering_cost = 0
        
        with custom_col4:
            training_required = st.checkbox("Safety Training Required")
            if training_required:
                training_sessions = st.number_input("Training Sessions", min_value=0, max_value=10, value=1, step=1)
                training_cost_per_session = st.number_input("Cost per Session (₹)", min_value=0, max_value=50000, value=15000, step=500)
            else:
                training_sessions = 0
                training_cost_per_session = 0
        
        st.markdown('</div>', unsafe_allow_html=True)

# Engineering Calculations Section
st.markdown("""
<div class="section-header">
    <h2>Engineering Calculations & Results</h2>
</div>
""", unsafe_allow_html=True)

# Core calculations
total_load = it_capacity + mechanical_load + house_load

# Bus count estimation based on tier level
tier_bus_factors = {"Tier I": 1.5, "Tier II": 1.7, "Tier III": 2.0, "Tier IV": 2.3}
estimated_buses = max(1, math.ceil(total_load * tier_bus_factors[tier_level] * bus_calibration))

# Study complexity factors based on tier
tier_complexity_factors = {"Tier I": 1.0, "Tier II": 1.2, "Tier III": 1.5, "Tier IV": 2.0}
tier_complexity = tier_complexity_factors[tier_level]

# Study definitions with base hours per bus
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

# Calculate study costs
total_study_hours = 0
total_study_cost = 0
total_report_cost = 0
study_results = {}

for study_key, study_data in studies_data.items():
    if st.session_state.studies_selected.get(study_key, False):
        # Calculate study hours
        study_hours = estimated_buses * study_data['base_hours_per_bus'] * study_data['factor'] * tier_complexity
        total_study_hours += study_hours
        
        # Resource allocation
        senior_hours = study_hours * senior_allocation
        mid_hours = study_hours * mid_allocation
        junior_hours = study_hours * junior_allocation
        
        # Apply urgency and discount multipliers
        rate_multiplier = urgency_multiplier if delivery_type == "Urgent" else 1.0
        discount_multiplier = (1 - repeat_discount/100) if customer_type == "Repeat Customer" else 1.0
        
        # Calculate costs by resource level
        senior_cost = senior_hours * senior_rate * rate_multiplier * discount_multiplier
        mid_cost = mid_hours * mid_rate * rate_multiplier * discount_multiplier
        junior_cost = junior_hours * junior_rate * rate_multiplier * discount_multiplier
        
        study_total_cost = senior_cost + mid_cost + junior_cost
        total_study_cost += study_total_cost
        
        # Report cost with complexity multiplier
        report_multipliers = {"Basic": 0.8, "Standard": 1.0, "Premium": 1.5}
        study_report_cost = study_data['report_cost'] * report_multipliers[report_complexity]
        total_report_cost += study_report_cost
        
        study_results[study_key] = {
            'name': study_data['name'],
            'hours': study_hours,
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
total_site_visit_cost = site_visits * site_visit_cost
total_label_cost = num_labels * cost_per_label if af_labels_required else 0
total_training_cost = training_sessions * training_cost_per_session if training_required else 0
total_meeting_cost = client_meetings * meeting_cost

# Calculate total additional costs
total_additional_costs = total_site_visit_cost + total_label_cost + stickering_cost + total_training_cost

# Final cost calculation
subtotal = total_study_cost + total_meeting_cost + total_report_cost + total_additional_costs
total_cost = subtotal * (1 + custom_margin/100)

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
            <h3>Tier Level</h3>
            <p class="value">{tier_level}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Bus Count</h3>
            <p class="value">{estimated_buses}</p>
            <p class="subtitle">buses</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Hours</h3>
            <p class="value">{total_study_hours:.0f}</p>
            <p class="subtitle">engineering hours</p>
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

    # Study-wise breakdown
    st.markdown("### Study-wise Cost Analysis")
    
    for study_key, study in study_results.items():
        st.markdown(f"""
        <div class="study-card">
            <h4>{study['name']}</h4>
            <p style="color: #718096; margin: 0 0 1rem 0; font-weight: 500;">{study['hours']:.1f} total engineering hours</p>
            <div class="study-details">
                <div class="study-detail-item">
                    <strong>Senior Engineer:</strong> {study['senior_hours']:.1f}h → ₹{study['senior_cost']:,.0f}<br>
                    <strong>Mid-level Engineer:</strong> {study['mid_hours']:.1f}h → ₹{study['mid_cost']:,.0f}<br>
                    <strong>Junior Engineer:</strong> {study['junior_hours']:.1f}h → ₹{study['junior_cost']:,.0f}<br>
                    <strong>Report Cost:</strong> ₹{study['report_cost']:,.0f}
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
        <h3 style="color: #4facfe; text-align: center; margin-bottom: 2rem; font-weight: 700;">Resource Allocation Summary</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; text-align: center;">
            <div>
                <h4 style="color: #667eea; margin: 0 0 0.5rem 0; font-weight: 700;">Senior Engineer</h4>
                <p style="color: #4facfe; font-size: 1.8rem; font-weight: 800; margin: 0.5rem 0;">{total_study_hours * senior_allocation:.0f} hrs</p>
                <p style="color: #718096; margin: 0; font-weight: 500;">Rate: ₹{senior_rate}/hr • {senior_allocation*100:.0f}% allocation</p>
            </div>
            <div>
                <h4 style="color: #667eea; margin: 0 0 0.5rem 0; font-weight: 700;">Mid-level Engineer</h4>
                <p style="color: #4facfe; font-size: 1.8rem; font-weight: 800; margin: 0.5rem 0;">{total_study_hours * mid_allocation:.0f} hrs</p>
                <p style="color: #718096; margin: 0; font-weight: 500;">Rate: ₹{mid_rate}/hr • {mid_allocation*100:.0f}% allocation</p>
            </div>
            <div>
                <h4 style="color: #667eea; margin: 0 0 0.5rem 0; font-weight: 700;">Junior Engineer</h4>
                <p style="color: #4facfe; font-size: 1.8rem; font-weight: 800; margin: 0.5rem 0;">{total_study_hours * junior_allocation:.0f} hrs</p>
                <p style="color: #718096; margin: 0; font-weight: 500;">Rate: ₹{junior_rate}/hr • {junior_allocation*100:.0f}% allocation</p>
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
    
    if total_training_cost > 0:
        chart_components.append('Training')
        chart_costs.append(total_training_cost)
    
    # Add meetings and reports
    chart_components.extend(['Client Meetings', 'Reports'])
    chart_costs.extend([total_meeting_cost, total_report_cost])
    
    # Create chart data
    chart_data = pd.DataFrame({
        'Component': chart_components,
        'Cost': chart_costs
    })
    
    st.bar_chart(chart_data.set_index('Component'))

    # Final comprehensive cost summary
    st.markdown(f"""
    <div class="results-container">
        <h2 style="color: #4facfe; text-align: center; margin-bottom: 2.5rem; font-weight: 800;">Comprehensive Project Cost Summary</h2>
        
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; margin-bottom: 2rem;">
            <div style="text-align: center; padding: 1rem; background: rgba(79, 172, 254, 0.1); border-radius: 12px;">
                <h4 style="color: #667eea; margin: 0; font-weight: 700;">Studies</h4>
                <p style="color: #2d3748; font-size: 1.3rem; font-weight: 700; margin: 0.5rem 0;">₹{total_study_cost:,.0f}</p>
            </div>
            <div style="text-align: center; padding: 1rem; background: rgba(240, 147, 251, 0.1); border-radius: 12px;">
                <h4 style="color: #8b5cf6; margin: 0; font-weight: 700;">Reports</h4>
                <p style="color: #2d3748; font-size: 1.3rem; font-weight: 700; margin: 0.5rem 0;">₹{total_report_cost:,.0f}</p>
            </div>
            <div style="text-align: center; padding: 1rem; background: rgba(34, 197, 94, 0.1); border-radius: 12px;">
                <h4 style="color: #059669; margin: 0; font-weight: 700;">Meetings</h4>
                <p style="color: #2d3748; font-size: 1.3rem; font-weight: 700; margin: 0.5rem 0;">₹{total_meeting_cost:,.0f}</p>
            </div>
            <div style="text-align: center; padding: 1rem; background: rgba(245, 158, 11, 0.1); border-radius: 12px;">
                <h4 style="color: #d97706; margin: 0; font-weight: 700;">Additional</h4>
                <p style="color: #2d3748; font-size: 1.3rem; font-weight: 700; margin: 0.5rem 0;">₹{total_additional_costs:,.0f}</p>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-bottom: 2rem;">
            <div style="text-align: center;">
                <h4 style="color: #4a5568; margin: 0; font-weight: 600;">Subtotal</h4>
                <p style="color: #2d3748; font-size: 1.4rem; font-weight: 700; margin: 0.5rem 0;">₹{subtotal:,.0f}</p>
            </div>
            <div style="text-align: center;">
                <h4 style="color: #4a5568; margin: 0; font-weight: 600;">Margin ({custom_margin}%)</h4>
                <p style="color: #2d3748; font-size: 1.4rem; font-weight: 700; margin: 0.5rem 0;">₹{total_cost - subtotal:,.0f}</p>
            </div>
            <div style="text-align: center;">
                <h4 style="color: #4a5568; margin: 0; font-weight: 600;">Discount Applied</h4>
                <p style="color: #2d3748; font-size: 1.4rem; font-weight: 700; margin: 0.5rem 0;">{repeat_discount}%</p>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 2rem; padding: 2.5rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 20px; color: white;">
            <h1 style="color: white; margin: 0; font-weight: 800; font-size: 2rem;">TOTAL PROJECT COST</h1>
            <p style="color: white; font-size: 3.5rem; font-weight: 900; margin: 1rem 0; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">₹{total_cost:,.0f}</p>
            <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin: 0;">Professional Power Systems Engineering Services</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Additional details breakdown
    if total_additional_costs > 0:
        st.markdown("### Additional Services Breakdown")
        additional_details = []
        if total_site_visit_cost > 0:
            additional_details.append(f"• Site Visits: {site_visits} visits × ₹{site_visit_cost:,} = ₹{total_site_visit_cost:,}")
        if total_label_cost > 0:
            additional_details.append(f"• Arc Flash Labels: {num_labels} labels × ₹{cost_per_label:,} = ₹{total_label_cost:,}")
        if stickering_cost > 0:
            additional_details.append(f"• Equipment Stickering: ₹{stickering_cost:,}")
        if total_training_cost > 0:
            additional_details.append(f"• Safety Training: {training_sessions} sessions × ₹{training_cost_per_session:,} = ₹{total_training_cost:,}")
        
        for detail in additional_details:
            st.write(detail)

else:
    st.warning("⚠️ Please select at least one study type to generate cost estimates.")

# Footer
import datetime
current_time = datetime.datetime.now()

st.markdown(f"""
<div style="text-align: center; color: #4a5568; padding: 3rem 2rem 2rem 2rem; margin-top: 4rem; 
     border-top: 2px solid rgba(79, 172, 254, 0.2); background: linear-gradient(135deg, rgba(255,255,255,0.8) 0%, rgba(240,249,255,0.6) 100%);
     border-radius: 15px;">
    <p style="font-size: 1.2rem; font-weight: 700; color: #4facfe; margin: 0 0 0.5rem 0;">
        Data Center Power System Studies - Professional Cost Estimation Platform
    </p>
    <p style="margin: 0.5rem 0; font-weight: 600; color: #667eea;">
        Developed by <strong>Abhishek Diwanji</strong> | Power Systems Engineering Department
    </p>
    <p style="margin: 0; font-size: 0.9rem; color: #718096; font-weight: 500;">
        Enhanced Professional Version 3.0 | Advanced Engineering Calculations & Cost Analysis
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #a0aec0;">
        Generated on: {current_time.strftime("%B %d, %Y at %I:%M %p")}
    </p>
</div>
""", unsafe_allow_html=True)