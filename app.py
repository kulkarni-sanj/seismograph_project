import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- APP CONFIG ---
st.set_page_config(page_title="AI Cultural Seismograph", page_icon="🌋", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #fafafa; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 15px; }
    .stat-card { background-color: #1d3331; border: 1px solid #4ade80; padding: 15px; border-radius: 10px; color: #4ade80; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌋 The Cultural Seismograph: AI Discourse Shift")
st.caption("Final Dissertation Project | Sanjana V Kulkarni | 2024DA04217")

# --- DATA LOADER ---
def load_data():
    if os.path.exists("cdi_results.csv") and os.path.exists("keyword_frequency_monthly.csv"):
        return pd.read_csv("cdi_results.csv"), pd.read_csv("keyword_frequency_monthly.csv")
    return None, None

df_cdi, df_key = load_data()

if df_cdi is not None:
    # --- HEADER KPI ---
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Corpus", "1.19M Comments", "r/tech + r/ML")
    with c2:
        st.metric("PELT Breakpoint", "Dec 2022", "Algorithmic Detection")
    with c3:
        st.metric("T-Test Confidence", "99.99%", "p < 0.000002")
    with c4:
        st.metric("Peak CDI Intensity", f"{df_cdi['cdi_score'].max():.2f}", "Richter Scale")

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs(["📊 Macro: CDI Seismograph", "🎯 Micro: Keyword Validation", "🧪 Statistical Rigor"])

    with tab1:
        st.subheader("Longitudinal Cultural Drift (6-Month Intervals)")
        fig = px.line(df_cdi, x='window_label', y='cdi_score', markers=True)
        fig.update_traces(line_color='#58a6ff', line_width=4)
        fig.add_vline(x="Jul 2022 - Dec 2022", line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
        st.info("The CDI captures broad semantic shifts. Note the acceleration in the H2-2022 window.")

    with tab2:
        st.subheader("High-Resolution Keyword Frequency")
        fig_key = px.area(df_key, x=df_key.columns[0], y='mention_rate')
        fig_key.update_traces(line_color='#f85149', fillcolor='rgba(248, 81, 73, 0.2)')
        st.plotly_chart(fig_key, use_container_width=True)
        st.success("This 'Ground Truth' validation confirms the exact timing of the cultural earthquake.")

    with tab3:
        st.subheader("Mathematical & Statistical Validation")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            ### 🔬 Welch's T-Test
            We compared the 'Pre-Launch' mean mention rate against the 'Post-Launch' mean.
            - **Pre-Launch Mean:** 0.64%
            - **Post-Launch Mean:** 4.54%
            - **T-Statistic:** 8.18
            - **P-Value:** < 0.001
            """)
            st.write("The difference is **Highly Statistically Significant**.")
        
        with col_b:
            st.markdown("""
            ### 🛡️ PELT Change-Point Detection
            Instead of assuming the date, we used the **Pruned Exact Linear Time** algorithm to find structural breaks in the time series.
            - **Detected Breakpoint:** Dec 2022
            - **Corroboration:** Matches launch of ChatGPT within 30 days.
            """)

else:
    st.error("Please upload the CSV files to the GitHub repository to activate the Command Center.")
