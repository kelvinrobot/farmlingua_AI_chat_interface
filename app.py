# app.py
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from math import pi

# Configure page with improved theme settings
st.set_page_config(
    page_title="Flood Detection Dashboard",
    layout="wide",
    page_icon="⛈️",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for better visibility
st.markdown("""
<style>
    /* Main text color */
    .stApp, .css-1v0mbdj, .stMarkdown, .stAlert, .stJson, .st-b7, .st-c0 {
        color: #000000 !important;
    }
    
    /* Metric values */
    .stMetric {
        color: #000000 !important;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: 15px;
        background-color: #f6f8fa;
    }
    
    /* Sidebar text */
    .sidebar .stMarkdown {
        color: #000000 !important;
    }
    
    /* Tab headers */
    .stTabs [data-baseweb="tab"] {
        color: #000000 !important;
        padding: 8px 16px;
        border-radius: 4px 4px 0 0;
    }
    
    /* Fix JSON viewer */
    .stJson {
        background-color: #f0f2f6 !important;
        padding: 10px !important;
        border-radius: 5px !important;
    }
    
    /* Better spacing */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    /* Dark mode compatibility */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #0e1117;
        }
        .stMetric {
            background-color: #1e2130 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Main title with better contrast
st.title("⛈️ Real-time Flood Prediction Dashboard")
st.markdown("""
This interactive dashboard predicts flood risks using environmental sensor data and machine learning models.
""", unsafe_allow_html=True)

# Sidebar with improved organization
with st.sidebar:
    st.header("📊 Sensor Input Parameters")
    with st.form("flood_form"):
        # Weather parameters section
        st.subheader("🌤️ Weather Conditions")
        avg_temp = st.number_input("Average Temperature (°C)", value=28.5)
        humidity = st.number_input("Humidity (%)", value=76.2)
        precip = st.number_input("Precipitation (mm)", value=12.3)
        windspeed = st.number_input("Wind Speed (km/h)", value=8.1)
        sealevelpressure = st.number_input("Sea Level Pressure (hPa)", value=1012.5)
        cloudcover = st.slider("Cloud Cover (%)", 0, 100, value=68)
        solarradiation = st.number_input("Solar Radiation (W/m²)", value=140.5)
        severerisk = st.slider("Severe Risk Level", 0.0, 1.0, value=0.2)

        # Historical data section
        st.subheader("📅 Historical Flood Data")
        flood_lag_1 = st.selectbox("Flood Yesterday?", [0, 1], index=0)
        flood_lag_2 = st.selectbox("Flood 2 Days Ago?", [0, 1], index=0)
        flood_lag_3 = st.selectbox("Flood 3 Days Ago?", [0, 1], index=0)
        flood_lag_4 = st.selectbox("Flood 4 Days Ago?", [0, 1], index=0)
        flood_lag_5 = st.selectbox("Flood 5 Days Ago?", [0, 1], index=0)

        # Soil and time parameters
        st.subheader("🌱 Soil & Temporal Data")
        smi_linear_norm = st.slider("Soil Moisture Index", 0.0, 1.0, 0.53)
        month = st.selectbox("Month", list(range(1, 13)), index=6)

        submit = st.form_submit_button("🚀 Predict Flood Risk", type="primary")

# Prediction logic
if submit:
    payload = {
        "Average_temp": avg_temp,
        "humidity": humidity,
        "precip": precip,
        "windspeed": windspeed,
        "sealevelpressure": sealevelpressure,
        "cloudcover": cloudcover,
        "solarradiation": solarradiation,
        "severerisk": severerisk,
        "flood_lag_1": flood_lag_1,
        "flood_lag_2": flood_lag_2,
        "flood_lag_3": flood_lag_3,
        "flood_lag_4": flood_lag_4,
        "flood_lag_5": flood_lag_5,
        "SMI_linear_norm": smi_linear_norm,
        "month": month
    }

    with st.spinner("🔮 Predicting flood risk..."):
        try:
            response = requests.post(
                "https://flood-ai-backend-3.onrender.com/predict",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            if response.status_code == 200:
                result = response.json()
                
                # Success message with better visibility
                st.success("✅ Prediction completed!", icon="✅")
                
                # Results section with improved layout
                st.subheader("📈 Flood Risk Assessment")
                
                # Metrics in columns with better spacing
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "🌊 Flood Probability", 
                        f"{result['flood_probability_percent']:.1f}%",
                        help="Probability of flood occurrence",
                        delta_color="off"
                    )
                
                with col2:
                    st.metric(
                        "⚠️ Risk Score", 
                        f"{result['flood_risk_score_percent']:.1f}%",
                        help="Composite risk score from all models",
                        delta_color="off"
                    )
                
                with col3:
                    status = "YES" if result["final_flood"] else "NO"
                    st.metric(
                        "🔮 Flood Predicted", 
                        status,
                        help="Final prediction from ensemble model",
                        delta_color="off"
                    )
                
                # Visualization tabs with better icons
                tab1, tab2, tab3 = st.tabs([
                    "📊 Probability Charts", 
                    "📈 Risk Analysis", 
                    "🔧 Technical Details"
                ])

                with tab1:
                    # Probability visualizations
                    fig_col1, fig_col2 = st.columns(2)
                    
                    with fig_col1:
                        # Donut chart with improved styling
                        fig, ax = plt.subplots(figsize=(5, 5))
                        prob = result["flood_probability_percent"]
                        ax.pie(
                            [prob, 100 - prob], 
                            labels=["Flood", "Safe"], 
                            colors=["#FF4B4B", "#3DDC84"],
                            startangle=90, 
                            wedgeprops={"width": 0.4},
                            textprops={'color': '#000000', 'fontsize': 12}
                        )
                        ax.set_title("Flood Probability", pad=20, color='#000000')
                        st.pyplot(fig)
                    
                    with fig_col2:
                        # Gauge chart with better visibility
                        fig, ax = plt.subplots(figsize=(7, 2))
                        risk_score = result["flood_risk_score_percent"]
                        ax.barh([""], [risk_score], color="#FF4B4B", height=0.3)
                        ax.set_xlim(0, 100)
                        ax.set_xlabel("Risk Score (%)", color='#000000')
                        ax.axvline(30, color='green', linestyle='--', label='Low')
                        ax.axvline(60, color='orange', linestyle='--', label='Medium')
                        ax.axvline(90, color='red', linestyle='--', label='High')
                        ax.legend(loc='lower right')
                        ax.set_title("Risk Level Gauge", color='#000000')
                        ax.tick_params(colors='#000000')
                        st.pyplot(fig)

                with tab2:
                    # Risk analysis with better formatting
                    st.subheader("🤖 Model Consensus")
                    
                    # Model votes with improved display
                    for vote in result["model_votes"]:
                        st.markdown(f"- **{vote}**")
                    
                    # Severity histogram with better colors
                    st.subheader("⚠️ Risk Severity")
                    fig, ax = plt.subplots(figsize=(8, 3))
                    risk_score = result["flood_risk_score_percent"]
                    bins = [0, 30, 60, 100]
                    labels = ['Low', 'Medium', 'High']
                    severity_zone = pd.cut([risk_score], bins=bins, labels=labels)[0]
                    
                    sns.histplot(
                        [risk_score], 
                        bins=30, 
                        kde=False, 
                        ax=ax, 
                        color='#1f77b4'
                    )
                    ax.axvline(risk_score, color='red', linestyle='--')
                    ax.set_title(f"Risk Severity: {severity_zone}", color='#000000')
                    ax.set_xlim(0, 100)
                    ax.set_xlabel("Risk Score (%)", color='#000000')
                    ax.tick_params(colors='#000000')
                    st.pyplot(fig)

                with tab3:
                    # Technical details with better formatting
                    st.subheader("⚙️ Input Parameters")
                    st.json(payload)
                    
                    st.subheader("📄 Raw Prediction Data")
                    st.json(result)

            else:
                st.error(f"❌ API returned status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Failed to connect to prediction service: {str(e)}")
            st.info("ℹ️ Please ensure the backend API is available")

# Footer with better styling
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 10px;">
    <p style="color: #666666;">🌊 AI Flood Detection System v1.0 | Powered by Machine Learning</p>
</div>
""", unsafe_allow_html=True)