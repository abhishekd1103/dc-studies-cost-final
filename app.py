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

# Advanced Dark Theme CSS with Data Center Background
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Global Dark Theme */
    .main > div {
        padding-top: 0.5rem;
    }
    
    .stApp {
        background: 
            linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 25%, rgba(51, 65, 85, 0.85) 50%, rgba(71, 85, 105, 0.8) 75%, rgba(15, 23, 42, 0.95) 100%),
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23334155' fill-opacity='0.1'%3E%3Ccircle cx='6' cy='6' r='1'/%3E%3Ccircle cx='18' cy='18' r='1'/%3E%3Ccircle cx='30' cy='6' r='1'/%3E%3Ccircle cx='42' cy='18' r='1'/%3E%3Ccircle cx='54' cy='6' r='1'/%3E%3Ccircle cx='6' cy='30' r='1'/%3E%3Ccircle cx='18' cy='42' r='1'/%3E%3Ccircle cx='30' cy='30' r='1'/%3E%3Ccircle cx='42' cy='42' r='1'/%3E%3Ccircle cx='54' cy='30' r='1'/%3E%3Ccircle cx='6' cy='54' r='1'/%3E%3Ccircle cx='18' cy='6' r='1'/%3E%3Ccircle cx='30' cy='54' r='1'/%3E%3Ccircle cx='42' cy='6' r='1'/%3E%3Ccircle cx='54' cy='54' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
        color: #e2e8f0;
        animation: backgroundFlow 20s ease-in-out infinite;
    }
    
    @keyframes backgroundFlow {
        0%, 100% { 
            background-position: 0% 50%;
            filter: hue-rotate(0deg);
        }
        25% { 
            background-position: 100% 50%;
            filter: hue-rotate(90deg);
        }
        50% { 
            background-position: 50% 100%;
            filter: hue-rotate(180deg);
        }
        75% { 
            background-position: 0% 0%;
            filter: hue-rotate(270deg);
        }
    }
    
    /* Floating Data Center Elements Animation */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(16, 185, 129, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(139, 92, 246, 0.15) 0%, transparent 50%);
        pointer-events: none;
        animation: dataFlow 15s ease-in-out infinite;
        z-index: -1;
    }
    
    @keyframes dataFlow {
        0%, 100% { opacity: 0.6; transform: scale(1) rotate(0deg); }
        33% { opacity: 0.8; transform: scale(1.1) rotate(120deg); }
        66% { opacity: 0.4; transform: scale(0.9) rotate(240deg); }
    }
    
    /* Header Styling with Advanced Animations */
    .main-header {
        background: linear-gradient(135deg, 
            rgba(15, 23, 42, 0.95) 0%, 
            rgba(30, 41, 59, 0.9) 25%, 
            rgba(59, 130, 246, 0.2) 50%,
            rgba(16, 185, 129, 0.2) 75%,
            rgba(15, 23, 42, 0.95) 100%);
        backdrop-filter: blur(20px) saturate(150%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 3rem;
        border-radius: 24px;
        color: #f1f5f9;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 
            0 25px 50px -12px rgba(0, 0, 0, 0.8),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
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
        background: conic-gradient(from 0deg, transparent, rgba(59, 130, 246, 0.3), transparent);
        animation: headerRotate 8s linear infinite;
        z-index: -1;
    }
    
    @keyframes headerRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .main-header h1 {
        font-size: 3.2rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(135deg, #3b82f6, #10b981, #8b5cf6);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        letter-spacing: -2px;
        position: relative;
        z-index: 1;
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        0% { filter: brightness(1) drop-shadow(0 0 10px rgba(59, 130, 246, 0.5)); }
        100% { filter: brightness(1.2) drop-shadow(0 0 20px rgba(16, 185, 129, 0.7)); }
    }
    
    .main-header h2 {
        font-size: 1.4rem;
        font-weight: 500;
        margin: 1.5rem 0 0 0;
        color: #94a3b8;
        position: relative;
        z-index: 1;
    }
    
    /* Developer Credit with Pulse Animation */
    .developer-credit {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        padding: 1.2rem 2.5rem;
        border-radius: 20px;
        color: #f1f5f9;
        text-align: center;
        font-weight: 700;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
        animation: pulseGlow 4s ease-in-out infinite;
    }
    
    @keyframes pulseGlow {
        0%, 100% { 
            transform: scale(1); 
            box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
        }
        50% { 
            transform: scale(1.02); 
            box-shadow: 0 15px 40px rgba(139, 92, 246, 0.5);
        }
    }
    
    /* Section Headers with Slide Animation */
    .section-header {
        background: linear-gradient(135deg, 
            rgba(59, 130, 246, 0.2) 0%, 
            rgba(16, 185, 129, 0.2) 100%);
        backdrop-filter: blur(15px) saturate(150%);
        border: 1px solid rgba(59, 130, 246, 0.4);
        color: #f1f5f9;
        padding: 2rem 2.5rem;
        border-radius: 20px;
        margin: 2.5rem 0 2rem 0;
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.2);
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .section-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .section-header:hover::before {
        left: 100%;
    }
    
    .section-header:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
        border-color: rgba(16, 185, 129, 0.5);
    }
    
    .section-header h2 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 800;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
        letter-spacing: -0.5px;
    }
    
    /* Advanced Card Design */
    .metric-card {
        background: linear-gradient(135deg, 
            rgba(30, 41, 59, 0.8) 0%, 
            rgba(51, 65, 85, 0.6) 100%);
        backdrop-filter: blur(20px) saturate(120%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #10b981, #8b5cf6);
        animation: cardGlow 3s linear infinite;
    }
    
    @keyframes cardGlow {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.4);
        border-color: rgba(16, 185, 129, 0.6);
    }
    
    .metric-card h3 {
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 700;
        margin: 0 0 1rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-card .value {
        color: #3b82f6;
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0;
        line-height: 1;
        text-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
        animation: valueGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes valueGlow {
        0% { color: #3b82f6; text-shadow: 0 0 10px rgba(59, 130, 246, 0.5); }
        100% { color: #10b981; text-shadow: 0 0 15px rgba(16, 185, 129, 0.7); }
    }
    
    .metric-card .subtitle {
        color: #64748b;
        font-size: 0.9rem;
        margin: 0.8rem 0 0 0;
        font-weight: 500;
    }
    
    /* Study Cards Enhancement */
    .study-card {
        background: linear-gradient(135deg, 
            rgba(30, 41, 59, 0.9) 0%, 
            rgba(51, 65, 85, 0.7) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .study-card::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        background: linear-gradient(135deg, transparent, rgba(139, 92, 246, 0.1), transparent);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .study-card:hover::after {
        opacity: 1;
    }
    
    .study-card:hover {
        border-color: rgba(16, 185, 129, 0.5);
        box-shadow: 0 20px 50px rgba(139, 92, 246, 0.3);
        transform: translateY(-5px);
    }
    
    .study-card h4 {
        color: #f1f5f9;
        font-size: 1.3rem;
        font-weight: 800;
        margin: 0 0 1.5rem 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    .study-details {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 2.5rem;
        margin-top: 1.5rem;
        align-items: center;
    }
    
    .study-detail-item {
        color: #cbd5e1;
        font-size: 1rem;
        line-height: 1.8;
        font-weight: 500;
    }
    
    .study-detail-item strong {
        color: #f1f5f9;
        font-weight: 700;
    }
    
    .cost-highlight {
        background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .cost-highlight::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .cost-highlight .amount {
        font-size: 1.6rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }
    
    /* Enhanced Results Container */
    .results-container {
        background: linear-gradient(135deg, 
            rgba(15, 23, 42, 0.95) 0%, 
            rgba(30, 41, 59, 0.9) 50%,
            rgba(51, 65, 85, 0.85) 100%);
        backdrop-filter: blur(25px) saturate(150%);
        border: 2px solid rgba(59, 130, 246, 0.4);
        border-radius: 25px;
        padding: 3rem;
        margin: 3rem 0;
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .results-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 30% 20%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 70% 80%, rgba(16, 185, 129, 0.1) 0%, transparent 50%);
        pointer-events: none;
        animation: resultsFlow 10s ease-in-out infinite;
    }
    
    @keyframes resultsFlow {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    /* Advanced Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 1rem 2.5rem;
        font-weight: 800;
        font-size: 1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.6s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.6);
        background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%);
    }
    
    /* Custom Input Styling */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2) !important;
        background: rgba(51, 65, 85, 0.9) !important;
    }
    
    .stCheckbox > label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .stSlider > div > div > div {
        color: #3b82f6 !important;
    }
    
    /* Disclaimer Box Enhancement */
    .disclaimer-box {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(239, 68, 68, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2.5rem 0;
        animation: warningPulse 3s ease-in-out infinite;
    }
    
    @keyframes warningPulse {
        0%, 100% { border-color: rgba(239, 68, 68, 0.3); }
        50% { border-color: rgba(245, 158, 11, 0.5); }
    }
    
    .disclaimer-box h4 {
        color: #f59e0b;
        margin: 0 0 1.5rem 0;
        font-weight: 800;
        font-size: 1.2rem;
    }
    
    .disclaimer-box p {
        color: #fbbf24;
        margin: 1rem 0;
        line-height: 1.8;
        font-weight: 500;
    }
    
    /* Additional Services Section */
    .custom-cost-section {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(139, 92, 246, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .custom-cost-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 20%, rgba(139, 92, 246, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(236, 72, 153, 0.05) 0%, transparent 50%);
        pointer-events: none;
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
    
    /* Work Allocation Section */
    .work-allocation-section {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(16, 185, 129, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2.5rem 0;
    }
    
    /* Summary Section Enhancement */
    .summary-section {
        background: linear-gradient(135deg, 
            rgba(15, 23, 42, 0.98) 0%, 
            rgba(30, 41, 59, 0.95) 25%,
            rgba(59, 130, 246, 0.1) 50%,
            rgba(16, 185, 129, 0.1) 75%,
            rgba(15, 23, 42, 0.98) 100%);
        backdrop-filter: blur(30px) saturate(150%);
        border: 3px solid rgba(59, 130, 246, 0.5);
        border-radius: 30px;
        padding: 4rem;
        margin: 4rem 0;
        box-shadow: 
            0 30px 60px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .summary-section::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #3b82f6, #10b981, #8b5cf6, #ec4899, #3b82f6);
        border-radius: 30px;
        z-index: -1;
        animation: borderFlow 4s linear infinite;
    }
    
    @keyframes borderFlow {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    /* Scope Status Cards */
    .scope-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #fca5a5;
        font-weight: 600;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .scope-card.in-scope {
        border-color: rgba(16, 185, 129, 0.3);
        color: #86efac;
    }
    
    /* Final Total Enhancement */
    .final-total-section {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 25%, #10b981 50%, #ec4899 75%, #3b82f6 100%);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
        border-radius: 25px;
        padding: 3rem;
        text-align: center;
        color: white;
        box-shadow: 0 25px 50px rgba(59, 130, 246, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .final-total-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        animation: totalPulse 3s ease-in-out infinite;
    }
    
    @keyframes totalPulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for study selections and work allocation
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

    # Work Allocation Section (NEW)
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
                "Senior Engineer Allocation (%)", 
                5, 50, st.session_state.work_allocation['senior'], 1
            )
        
        with alloc_col2:
            st.session_state.work_allocation['mid'] = st.slider(
                "Mid-level Engineer Allocation (%)", 
                10, 60, st.session_state.work_allocation['mid'], 1
            )
        
        with alloc_col3:
            st.session_state.work_allocation['junior'] = st.slider(
                "Junior Engineer Allocation (%)", 
                10, 70, st.session_state.work_allocation['junior'], 1
            )
        
        with alloc_col4:
            # Auto-balance button
            if st.button("Auto Balance (20:30:50)", key="auto_balance"):
                st.session_state.work_allocation = {'senior': 20, 'mid': 30, 'junior': 50}
                st.rerun()
        
        # Normalize allocations
        total_allocation = sum(st.session_state.work_allocation.values())
        if total_allocation != 100:
            factor = 100 / total_allocation
            for key in st.session_state.work_allocation:
                st.session_state.work_allocation[key] = round(st.session_state.work_allocation[key] * factor, 1)
        
        # Display normalized values
        st.info(f"Normalized Allocation → Senior: {st.session_state.work_allocation['senior']}%, Mid: {st.session_state.work_allocation['mid']}%, Junior: {st.session_state.work_allocation['junior']}%")
        
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

    # Additional Services Section (ENHANCED)
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
            custom_charges_desc = st.text_input("Description (Optional)", value="Additional Services")
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

# Bus count estimation based on tier level
tier_bus_factors = {"Tier I": 1.5, "Tier II": 1.7, "Tier III": 2.0, "Tier IV": 2.3}
estimated_buses = max(1, math.ceil(total_load * tier_bus_factors[tier_level] * bus_calibration))

# Study complexity factors based on tier
tier_complexity_factors = {"Tier I": 1.0, "Tier II": 1.2, "Tier III": 1.5, "Tier IV": 2.0}
tier_complexity = tier_complexity_factors[tier_level]

# Work allocation percentages (converted to decimals)
senior_allocation = st.session_state.work_allocation['senior'] / 100
mid_allocation = st.session_state.work_allocation['mid'] / 100
junior_allocation = st.session_state.work_allocation['junior'] / 100

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
total_site_visit_cost = site_visits * site_visit_cost if site_visit_enabled else 0
total_label_cost = num_labels * cost_per_label if af_labels_enabled else 0
total_meeting_cost = client_meetings * meeting_cost

# Calculate total additional costs
total_additional_costs = total_site_visit_cost + total_label_cost + stickering_cost + custom_charges_cost

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
            <p style="color: #94a3b8; margin: 0 0 1rem 0; font-weight: 500;">{study['hours']:.1f} total engineering hours</p>
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

    # Resource allocation summary with custom percentages
    st.markdown(f"""
    <div class="results-container">
        <h3 style="color: #3b82f6; text-align: center; margin-bottom: 2rem; font-weight: 800;">Custom Resource Allocation Summary</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; text-align: center;">
            <div>
                <h4 style="color: #10b981; margin: 0 0 0.5rem 0; font-weight: 800;">Senior Engineer</h4>
                <p style="color: #3b82f6; font-size: 2rem; font-weight: 900; margin: 0.5rem 0;">{total_study_hours * senior_allocation:.0f} hrs</p>
                <p style="color: #94a3b8; margin: 0; font-weight: 600;">Rate: ₹{senior_rate:,}/hr • {st.session_state.work_allocation['senior']:.1f}% allocation</p>
                <p style="color: #64748b; margin: 0.5rem 0 0 0;">Total: ₹{sum(study['senior_cost'] for study in study_results.values()):,.0f}</p>
            </div>
            <div>
                <h4 style="color: #10b981; margin: 0 0 0.5rem 0; font-weight: 800;">Mid-level Engineer</h4>
                <p style="color: #3b82f6; font-size: 2rem; font-weight: 900; margin: 0.5rem 0;">{total_study_hours * mid_allocation:.0f} hrs</p>
                <p style="color: #94a3b8; margin: 0; font-weight: 600;">Rate: ₹{mid_rate:,}/hr • {st.session_state.work_allocation['mid']:.1f}% allocation</p>
                <p style="color: #64748b; margin: 0.5rem 0 0 0;">Total: ₹{sum(study['mid_cost'] for study in study_results.values()):,.0f}</p>
            </div>
            <div>
                <h4 style="color: #10b981; margin: 0 0 0.5rem 0; font-weight: 800;">Junior Engineer</h4>
                <p style="color: #3b82f6; font-size: 2rem; font-weight: 900; margin: 0.5rem 0;">{total_study_hours * junior_allocation:.0f} hrs</p>
                <p style="color: #94a3b8; margin: 0; font-weight: 600;">Rate: ₹{junior_rate:,}/hr • {st.session_state.work_allocation['junior']:.1f}% allocation</p>
                <p style="color: #64748b; margin: 0.5rem 0 0 0;">Total: ₹{sum(study['junior_cost'] for study in study_results.values()):,.0f}</p>
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

    # ENHANCED PROJECT COST SUMMARY
    st.markdown(f"""
    <div class="summary-section">
        <h1 style="color: #f1f5f9; text-align: center; margin-bottom: 3rem; font-weight: 900; font-size: 2.5rem;">
            Complete Project Cost Summary
        </h1>
        
        <!-- Studies Summary -->
        <div style="margin-bottom: 3rem;">
            <h3 style="color: #3b82f6; font-weight: 800; margin-bottom: 1.5rem; font-size: 1.4rem;">Studies Breakdown</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
    """, unsafe_allow_html=True)
    
    # Individual study breakdowns
    for study in study_results.values():
        st.markdown(f"""
        <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 12px; padding: 1.5rem;">
            <h5 style="color: #f1f5f9; margin: 0 0 1rem 0; font-weight: 700;">{study['name']}</h5>
            <p style="color: #cbd5e1; margin: 0.3rem 0; font-size: 0.9rem;">Engineering: ₹{study['total_cost']:,.0f}</p>
            <p style="color: #cbd5e1; margin: 0.3rem 0; font-size: 0.9rem;">Report: ₹{study['report_cost']:,.0f}</p>
            <p style="color: #3b82f6; margin: 0.5rem 0 0 0; font-weight: 700; font-size: 1.1rem;">Total: ₹{study['total_cost'] + study['report_cost']:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            </div>
        </div>
        
        <!-- Additional Services Summary -->
        <div style="margin-bottom: 3rem;">
            <h3 style="color: #10b981; font-weight: 800; margin-bottom: 1.5rem; font-size: 1.4rem;">Additional Services Breakdown</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem;">
    """, unsafe_allow_html=True)
    
    # Site visits scope
    if site_visit_enabled:
        st.markdown(f"""
        <div class="scope-card in-scope">
            <strong>Site Visits:</strong> {site_visits} visits × ₹{site_visit_cost:,} = ₹{total_site_visit_cost:,}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="scope-card">
            <strong>Site Visits:</strong> Not included in scope
        </div>
        """, unsafe_allow_html=True)
    
    # Arc Flash Labels scope
    if af_labels_enabled:
        st.markdown(f"""
        <div class="scope-card in-scope">
            <strong>Arc Flash Labels:</strong> {num_labels} labels × ₹{cost_per_label:,} = ₹{total_label_cost:,}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="scope-card">
            <strong>Arc Flash Labels:</strong> Hardcopy labels not in our scope
        </div>
        """, unsafe_allow_html=True)
    
    # Equipment Stickering scope
    if stickering_enabled:
        st.markdown(f"""
        <div class="scope-card in-scope">
            <strong>Equipment Stickering:</strong> ₹{stickering_cost:,}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="scope-card">
            <strong>Equipment Stickering:</strong> Not included in our scope
        </div>
        """, unsafe_allow_html=True)
    
    # Custom charges
    if custom_charges_cost > 0:
        st.markdown(f"""
        <div class="scope-card in-scope">
            <strong>{custom_charges_desc}:</strong> ₹{custom_charges_cost:,}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
            </div>
        </div>
        
        <!-- Final Summary Grid -->
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; margin-bottom: 3rem;">
            <div style="text-align: center; padding: 2rem; background: rgba(59, 130, 246, 0.15); border: 2px solid rgba(59, 130, 246, 0.4); border-radius: 16px;">
                <h4 style="color: #3b82f6; margin: 0; font-weight: 800;">Total Studies</h4>
                <p style="color: #f1f5f9; font-size: 1.6rem; font-weight: 800; margin: 1rem 0;">₹{total_study_cost:,.0f}</p>
                <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">Engineering Services</p>
            </div>
            <div style="text-align: center; padding: 2rem; background: rgba(16, 185, 129, 0.15); border: 2px solid rgba(16, 185, 129, 0.4); border-radius: 16px;">
                <h4 style="color: #10b981; margin: 0; font-weight: 800;">Reports & Docs</h4>
                <p style="color: #f1f5f9; font-size: 1.6rem; font-weight: 800; margin: 1rem 0;">₹{total_report_cost:,.0f}</p>
                <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">{report_complexity} Format</p>
            </div>
            <div style="text-align: center; padding: 2rem; background: rgba(139, 92, 246, 0.15); border: 2px solid rgba(139, 92, 246, 0.4); border-radius: 16px;">
                <h4 style="color: #8b5cf6; margin: 0; font-weight: 800;">Client Meetings</h4>
                <p style="color: #f1f5f9; font-size: 1.6rem; font-weight: 800; margin: 1rem 0;">₹{total_meeting_cost:,.0f}</p>
                <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">{client_meetings} Sessions</p>
            </div>
            <div style="text-align: center; padding: 2rem; background: rgba(236, 72, 153, 0.15); border: 2px solid rgba(236, 72, 153, 0.4); border-radius: 16px;">
                <h4 style="color: #ec4899; margin: 0; font-weight: 800;">Additional</h4>
                <p style="color: #f1f5f9; font-size: 1.6rem; font-weight: 800; margin: 1rem 0;">₹{total_additional_costs:,.0f}</p>
                <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">Extra Services</p>
            </div>
        </div>
        
        <!-- Cost Breakdown -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin-bottom: 3rem;">
            <div style="text-align: center; padding: 1.5rem; background: rgba(51, 65, 85, 0.3); border-radius: 12px;">
                <h4 style="color: #cbd5e1; margin: 0; font-weight: 600;">Subtotal</h4>
                <p style="color: #f1f5f9; font-size: 1.8rem; font-weight: 800; margin: 1rem 0;">₹{subtotal:,.0f}</p>
            </div>
            <div style="text-align: center; padding: 1.5rem; background: rgba(51, 65, 85, 0.3); border-radius: 12px;">
                <h4 style="color: #cbd5e1; margin: 0; font-weight: 600;">Margin ({custom_margin}%)</h4>
                <p style="color: #f1f5f9; font-size: 1.8rem; font-weight: 800; margin: 1rem 0;">₹{total_cost - subtotal:,.0f}</p>
            </div>
            <div style="text-align: center; padding: 1.5rem; background: rgba(51, 65, 85, 0.3); border-radius: 12px;">
                <h4 style="color: #cbd5e1; margin: 0; font-weight: 600;">Discount Applied</h4>
                <p style="color: #f1f5f9; font-size: 1.8rem; font-weight: 800; margin: 1rem 0;">{repeat_discount}%</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # FINAL TOTAL WITH ADVANCED ANIMATION
    st.markdown(f"""
    <div class="final-total-section">
        <h1 style="color: white; margin: 0; font-weight: 900; font-size: 2.2rem; position: relative; z-index: 2;">TOTAL PROJECT COST</h1>
        <p style="color: white; font-size: 4.5rem; font-weight: 900; margin: 1.5rem 0; text-shadow: 0 4px 8px rgba(0,0,0,0.5); position: relative; z-index: 2;">₹{total_cost:,.0f}</p>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.3rem; margin: 0; font-weight: 600; position: relative; z-index: 2;">Professional Power Systems Engineering Services</p>
        <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin: 1rem 0 0 0; position: relative; z-index: 2;">Project: {project_name} | {tier_level} Data Center | {customer_type}</p>
    </div>
    """, unsafe_allow_html=True)

    # Additional details breakdown
    if total_additional_costs > 0:
        st.markdown("### Additional Services Details")
        additional_details = []
        if total_site_visit_cost > 0:
            additional_details.append(f"• Site Visits: {site_visits} visits × ₹{site_visit_cost:,} = ₹{total_site_visit_cost:,}")
        if total_label_cost > 0:
            additional_details.append(f"• Arc Flash Labels: {num_labels} labels × ₹{cost_per_label:,} = ₹{total_label_cost:,}")
        if stickering_cost > 0:
            additional_details.append(f"• Equipment Stickering: ₹{stickering_cost:,}")
        if custom_charges_cost > 0:
            additional_details.append(f"• {custom_charges_desc}: ₹{custom_charges_cost:,}")
        
        for detail in additional_details:
            st.write(detail)

else:
    st.warning("⚠️ Please select at least one study type to generate cost estimates.")

# Footer with animation
import datetime
current_time = datetime.datetime.now()

st.markdown(f"""
<div style="text-align: center; color: #94a3b8; padding: 4rem 2rem 3rem 2rem; margin-top: 5rem; 
     border-top: 3px solid rgba(59, 130, 246, 0.4); 
     background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
     border-radius: 20px; backdrop-filter: blur(15px);">
    <p style="font-size: 1.4rem; font-weight: 800; color: #3b82f6; margin: 0 0 1rem 0;">
        Data Center Power System Studies - Advanced Cost Estimation Platform
    </p>
    <p style="margin: 1rem 0; font-weight: 700; color: #10b981; font-size: 1.1rem;">
        Developed by <strong>Abhishek Diwanji</strong> | Power Systems Engineering Department
    </p>
    <p style="margin: 0; font-size: 1rem; color: #64748b; font-weight: 600;">
        Enhanced Professional Version 4.0 | Advanced Dark Theme with Animations
    </p>
    <p style="margin: 1rem 0 0 0; font-size: 0.9rem; color: #475569; font-style: italic;">
        Generated on: {current_time.strftime("%B %d, %Y at %I:%M %p IST")} | Cutting-edge Technology Stack
    </p>
</div>
""", unsafe_allow_html=True)
