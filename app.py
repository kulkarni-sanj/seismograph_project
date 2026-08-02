import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Cultural Seismograph", layout="wide")
st.title("📊 The Cultural Seismograph Dashboard")
st.caption("Sanjana V Kulkarni | 2024DA04217")

# Check if files exist locally
if os.path.exists("cdi_results.csv") and os.path.exists("keyword_frequency_monthly.csv"):
    df_cdi = pd.read_csv("cdi_results.csv")
    df_key = pd.read_csv("keyword_frequency_monthly.csv")

    tab1, tab2 = st.tabs(["📉 CDI Seismograph", "🎯 Keyword Validation"])
    
    with tab1:
        st.subheader("Longitudinal Cultural Drift Index")
        fig = px.line(df_cdi, x='window_label', y='cdi_score', 
                      title="CDI Score (Semantic + Topic Drift)", markers=True)
        if "2022-11" in df_cdi['window_key'].values:
            fig.add_vline(x="2022-11", line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Keyword Frequency (Ground Truth)")
        fig2 = px.area(df_key, x='window_key', y='mention_rate', 
                       title="AI-Related Terms Mention Rate (%)")
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.error("Data files not found in the repository. Please ensure CSVs are uploaded.")